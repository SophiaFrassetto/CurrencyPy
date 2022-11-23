# build-in imports
import platform
from datetime import date
from locale import LC_MONETARY
from locale import setlocale
from locale import getlocale
from locale import currency
from locale import localeconv

# project imports
from .sources import EconomiaAwesomeAPI
from .utils import iso_code_alias
from .utils import iso_code_alias_windows

__all__ = ['Currency', 'QUOTATION_REFERENCES', 'LOCALE_ALIAS', 'DEFAULT_ISO_CODE']

QUOTATION_REFERENCES = ['buy', 'sell']
LOCALE_ALIAS = {'Windows': iso_code_alias_windows, 'Linux': iso_code_alias, 'Darwin': iso_code_alias}[platform.system()]
DEFAULT_ISO_CODE = {y: x for x, y in LOCALE_ALIAS.items()}[getlocale()[0]]


class Currency:
    def __init__(self, value: float, iso_code: str = None, quoting_reference: str = 'buy'):
        self.iso_code = iso_code or DEFAULT_ISO_CODE

        self.settings = {}
        setlocale(LC_MONETARY, LOCALE_ALIAS[self.iso_code])
        self.settings = localeconv()

        self.value = value
        self.quoting_reference = quoting_reference

    @property
    def iso_code(self):
        return self._iso_code

    @iso_code.setter
    def iso_code(self, iso_code):
        self._iso_code = iso_code
        self._iso_code_validate(iso_code)

    def _iso_code_validate(self, iso_code):
        if not isinstance(iso_code, str):
            raise TypeError('The iso_code must be of type str')
        if len(iso_code) != 3:
            raise ValueError('The iso_code value must be size 3 and follow the ISO 4217 standard')
        if not iso_code in LOCALE_ALIAS:
            raise ValueError(f'This iso code is not supported - {iso_code}')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self._value_validate(value)

    def _value_validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('The value must be of type (int, float...), or be of type str which contains currency value.')
        return round(float(value), self.settings['frac_digits'])

    @property
    def quoting_reference(self):
        return self._quoting_reference

    @quoting_reference.setter
    def quoting_reference(self, quoting_reference):
        self._quoting_reference = self._quoting_reference_validate(quoting_reference)

    def _quoting_reference_validate(self, quoting_reference):
        if not isinstance(quoting_reference, str):
            raise TypeError('The quoting_reference must be of type str')
        elif quoting_reference not in QUOTATION_REFERENCES:
            raise TypeError(f'This quoting reference is not supported - {quoting_reference}')
        return quoting_reference

    def convert_to(self, to_iso_code: str, date: date = None):
        sources = [EconomiaAwesomeAPI]
        pair = f'{self.iso_code}-{to_iso_code}'.upper()
        for source in sources:
            if source.check_available_convertion(pair):
                if date:
                    quote = source.convert_by_date(pair, date)
                else:
                    quote = source.convert(pair)
                refereces = {'buy': quote.buy, 'sell': quote.sell}
                value_reference = refereces[self.quoting_reference]
                return Currency(self.value * self._value_validate(value_reference), to_iso_code)
        return NotImplemented

    def __str__(self):
        setlocale(LC_MONETARY, LOCALE_ALIAS[self.iso_code])
        return currency(self.value, symbol=True, grouping=True, international=False)

    def __repr__(self):
        setlocale(LC_MONETARY, LOCALE_ALIAS[self.iso_code])
        return currency(self.value, symbol=True, grouping=True, international=True)

    # def __add__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return Currency(round(self.value + other.convert_to(self.iso_code).value, self.settings['frac_digits']), self.iso_code)
    #         return Currency(round(self.value + other.value, self.settings['frac_digits']), self.iso_code)
    #     return NotImplemented

    # def __sub__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return Currency(round(self.value - other.convert_to(self.iso_code).value, self.settings['frac_digits']), self.iso_code)
    #         return Currency(round(self.value - other.value, self.settings['frac_digits']), self.iso_code)
    #     return NotImplemented

    # def __eq__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return self.value == other.convert_to(self.iso_code).value
    #         return self.value == other.value
    #     return NotImplemented

    # def __ne__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return self.value != other.convert_to(self.iso_code).value
    #         return self.value != other.value
    #     return NotImplemented

    # def __lt__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return self.value < other.convert_to(self.iso_code).value
    #         return self.value < other.value
    #     return NotImplemented

    # def __le__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return self.value <= other.convert_to(self.iso_code).value
    #         return self.value <= other.value
    #     return NotImplemented

    # def __gt__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return self.value > other.convert_to(self.iso_code).value
    #         return self.value > other.value
    #     return NotImplemented

    # def __ge__(self, other):
    #     if isinstance(other, Currency):
    #         if other.iso_code != self.iso_code:
    #             return self.value >= other.convert_to(self.iso_code).value
    #         return self.value >= other.value
    #     return NotImplemented
