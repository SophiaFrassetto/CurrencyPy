# build-in imports
import logging
import platform
from datetime import date
from decimal import Decimal
from locale import (
    currency,
    getlocale,
    LC_MONETARY,
    localeconv,
    setlocale,
)

# project imports
from .sources import (
    ExchangeRateAPIV6,
)
from .utils import (
    iso_code_alias,
    iso_code_alias_windows,
)

__all__ = ['Currency', 'LOCALE_ALIAS', 'DEFAULT_ISO_CODE']

LOCALE_ALIAS = {'Windows': iso_code_alias_windows, 'Linux': iso_code_alias, 'Darwin': iso_code_alias}[platform.system()]
DEFAULT_ISO_CODE = {y: x for x, y in LOCALE_ALIAS.items()}[getlocale()[0]]


class Currency:
    def __init__(self, value: Decimal, iso_code: str = DEFAULT_ISO_CODE):
        """This Currency is a new type to facilitate the handling of monetary values, with a more human
            visualization and also with conversion functions. DISCLAIMER: not everything can be 100% accurate,
            as this is an educational project.

        Args:
            value (Decimal): Numerical value
            iso_code (str, optional): Iso code 4217 to reference this value. Defaults to DEFAULT_ISO_CODE (Based in your location).
        """
        self.iso_code = iso_code

        self.settings = {}
        setlocale(LC_MONETARY, LOCALE_ALIAS[self.iso_code])
        self.settings = localeconv()

        self.value = value

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
        if not isinstance(value, (int, Decimal, float)):
            raise TypeError('The value must be of type (int, float...), or be of type str which contains currency value.')
        return round(Decimal(value), self.settings['frac_digits'])

    def convert_to(self, to_iso_code: str, date: date = None):
        sources = [
            ExchangeRateAPIV6
        ]

        tax = None
        for source in sources:
            try:
                if source().check_pair_available_convertion(self.iso_code, to_iso_code):
                    if date:
                        try:
                            tax = source().get_pair_tax_by_date(self.iso_code, to_iso_code, date)
                        except NotImplementedError:
                            logging.warning(f'This source {source.__name__} no has possible get pair tax by date.')
                            continue
                    else:
                        tax = source().get_pair_tax(self.iso_code, to_iso_code)
                    break
            except Exception as err:
                logging.warning(f'Error to get tax with source {source.__name__} - {err}')
                continue

        if not tax:
            raise Exception(f'It was not possible to convert the value {self.iso_code} to {to_iso_code}')

        converted_value = self.value * self._value_validate(tax)
        self.value = converted_value
        self.iso_code = to_iso_code
        setlocale(LC_MONETARY, LOCALE_ALIAS[self.iso_code])

    def __str__(self):
        setlocale(LC_MONETARY, LOCALE_ALIAS[self.iso_code])
        return currency(self.value, symbol=True, grouping=True, international=False)

    def __repr__(self):
        setlocale(LC_MONETARY, LOCALE_ALIAS[self.iso_code])
        return currency(self.value, symbol=True, grouping=True, international=True)

    def __add__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot add currencies with different currency codes - ({repr(self)}, {repr(other)})") 
            return Currency(round(self.value + other.value, self.settings['frac_digits']), self.iso_code)
        else:
            raise TypeError(f"Cannot add Currency object to non-Currency object - (Currency, {type(other)})")

    def __sub__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot subtract currencies with different currency codes - ({repr(self)}, {repr(other)})")
            return Currency(round(self.value - other.value, self.settings['frac_digits']), self.iso_code)
        else:
            raise TypeError(f"Cannot subtract Currency object from non-Currency object - (Currency, {type(other)})")

    def __mul__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot multiply currencies with different currency codes - ({repr(self)}, {repr(other)})")
            return Currency(round(self.value * other.value, self.settings['frac_digits']), self.iso_code)
        else:
            raise TypeError(f"Cannot multiply Currency object from non-Currency object - (Currency, {type(other)})")

    def __truediv__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot divide currencies with different currency codes - ({repr(self)}, {repr(other)})")
            return Currency(round(self.value / other.value, self.settings['frac_digits']), self.iso_code)
        else:
            raise TypeError(f"Cannot divide Currency object from non-Currency object - (Currency, {type(other)})")

    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.value == other.value and other.iso_code == self.iso_code
        else:
            raise TypeError(f"Cannot compare Currency object from non-Currency object - (Currency, {type(other)})")

    def __lt__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot compare currencies with different currency codes - ({repr(self)}, {repr(other)})")
            return self.value < other.value
        else:
            raise TypeError(f"Cannot compare Currency object from non-Currency object - (Currency, {type(other)})")

    def __le__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot compare currencies with different currency codes - ({repr(self)}, {repr(other)})")
            return self.value <= other.value
        else:
            raise TypeError(f"Cannot compare Currency object from non-Currency object - (Currency, {type(other)})")

    def __gt__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot compare currencies with different currency codes - ({repr(self)}, {repr(other)})")
            return self.value > other.value
        else:
            raise TypeError(f"Cannot compare Currency object from non-Currency object - (Currency, {type(other)})")

    def __ge__(self, other):
        if isinstance(other, Currency):
            if other.iso_code != self.iso_code:
                raise ValueError(f"Cannot compare currencies with different currency codes - ({repr(self)}, {repr(other)})")
            return self.value >= other.value
        else:
            raise TypeError(f"Cannot compare Currency object from non-Currency object - (Currency, {type(other)})")
