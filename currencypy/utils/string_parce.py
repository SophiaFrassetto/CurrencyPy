
import re
from locale import LC_MONETARY, localeconv, setlocale
from typing import Tuple, Optional, Union
from . import (symbol_alias)

__ALL__ = ['parse_currency_string']


def build_currency_regex(currency_symbols: dict) -> str:
    escaped_symbols = [re.escape(symbol) for symbol in currency_symbols.keys()]
    symbols_regex = '|'.join(escaped_symbols)
    regex_pattern = rf'({symbols_regex})*([\d.,\s]+)({symbols_regex})*'
    return regex_pattern

def determine_iso_code(symbol, amount_str, currency_symbols, locale_alias):
    if symbol in currency_symbols:
        possible_isos = currency_symbols[symbol]
        if len(possible_isos) == 1:
            return possible_isos[0]
        else:
            for iso in possible_isos:
                try:
                    setlocale(LC_MONETARY, locale_alias[iso])
                    loc_info = localeconv()
                    if matches_format(amount_str, loc_info):
                        return iso
                except Exception as e:
                    print(f"Erro ao definir locale para {iso}: {e}")
        return None

def matches_format(amount_str, loc_info):
    # Extrai informações do localeconv
    decimal_point = loc_info['mon_decimal_point']
    thousands_sep = loc_info['mon_thousands_sep']
    grouping = loc_info['mon_grouping']
    currency_symbol = loc_info['currency_symbol']
    p_cs_precedes = loc_info['p_cs_precedes']
    p_sep_by_space = loc_info['p_sep_by_space']
    p_sign_posn = loc_info['p_sign_posn']
    n_sign_posn = loc_info['n_sign_posn']
    positive_sign = loc_info['positive_sign']
    negative_sign = loc_info['negative_sign']

    # Verifica separador decimal e de milhares
    parts = amount_str.split(decimal_point)
    if len(parts) > 2:
        return False  # Mais de um separador decimal
    if thousands_sep:
        for part in parts[0].split(thousands_sep):
            if len(part) > 3:
                return False  # Grupo de dígitos maior que 3

    # Verifica agrupamento de dígitos
    if grouping:
        grouped_parts = parts[0].split(thousands_sep) if thousands_sep else [parts[0]]
        if any(len(group) not in grouping for group in grouped_parts[:-1]):
            return False  # Agrupamento incorreto

    # Verifica símbolo da moeda e sua posição
    if currency_symbol:
        if p_cs_precedes == 1:  # Símbolo antes do valor
            symbol_index = 0 if p_sign_posn in [1, 3] else len(amount_str) - len(currency_symbol) - 1
            if not amount_str.startswith(currency_symbol + (' ' if p_sep_by_space else '')):
                return False
        else:  # Símbolo depois do valor
            symbol_index = len(amount_str) - len(currency_symbol)
            if not amount_str.endswith((' ' if p_sep_by_space else '') + currency_symbol):
                return False

    # Verifica posição do sinal positivo/negativo
    if positive_sign or negative_sign:
        sign = positive_sign if amount_str[0] in positive_sign else negative_sign
        if p_sign_posn == 0 and amount_str[0] != sign:
            return False  # Sinal junto ao símbolo
        elif p_sign_posn == 1 and amount_str[0] != sign:
            return False  # Sinal antes do valor
        elif p_sign_posn == 2 and amount_str[-1] != sign:
            return False  # Sinal depois do valor
        elif p_sign_posn == 3 and amount_str[symbol_index - 1] != sign:
            return False  # Sinal antes do símbolo
        elif p_sign_posn == 4 and amount_str[symbol_index + 1] != sign:
            return False  # Sinal depois do símbolo

    return True

def parse_currency_string(currency_str: str, locale_alias, iso_code: Optional[str] = None) -> Tuple[Union[int, float], str]:
    regex_pattern = build_currency_regex(symbol_alias)
    match = re.search(regex_pattern, currency_str.strip())

    if not match:
        raise ValueError("String de moeda inválida")

    symbol_before, amount_str, symbol_after = match.groups()
    symbol = symbol_before or symbol_after

    iso_code = determine_iso_code(symbol, amount_str, symbol_alias, locale_alias)

    if amount_str.count('.') > 1 and amount_str.count(',') > 1:
        raise ValueError("String de moeda ambígua")

    cleaned_str = re.sub(r'[^\d.,]', '', amount_str)

    if '.' in cleaned_str and ',' in cleaned_str:
        if cleaned_str.rfind('.') < cleaned_str.rfind(','):
            cleaned_str = cleaned_str.replace('.', '').replace(',', '.')
        else:
            cleaned_str = cleaned_str.replace(',', '')
    elif ',' in cleaned_str and cleaned_str.count(',') == 1:
        cleaned_str = cleaned_str.replace(',', '.')

    try:
        amount_parts = cleaned_str.split('.')
        amount = int(amount_parts[0]) + int(amount_parts[1]) / (10 ** len(amount_parts[1]))
    except ValueError:
        raise ValueError("String de moeda inválida")

    return amount, iso_code
