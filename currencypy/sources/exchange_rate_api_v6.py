# build-in imports
import os
import json
from datetime import date
from decimal import Decimal
from urllib.request import urlopen

# project imports
from .source_base import Sources


# set config to use Exchange Rate API v6
URL_BASE = 'https://v6.exchangerate-api.com/v6'
APIKEY = os.environ.get('EXCHANGERATE_API_KEY') or None
URL = f'{URL_BASE}/{APIKEY}'


class ExchangeRateAPIV6(Sources):
    """
        API: Exchange Rate
        Documentation: https://www.exchangerate-api.com/docs/standard-requests
        API Verion: 6
    """
    @staticmethod
    def _check_api_key():
        if not APIKEY:
            raise ValueError('For use thi API is necessary API_KEY - For more information https://www.exchangerate-api.com/docs/standard-requests')

    @classmethod
    def check_pair_available_convertion(self, code_from: str, code_to: str) -> bool:
        self._check_api_key()

        try:
            response = urlopen(f'{URL}/codes')
            body_json = json.loads(response.read())

            # this API return supported codes in the structure
            # [ ['CODE', 'NAME'], ['BRL', 'Brazilian Real'], ...]
            # Abstract list to get only code
            # ['USD', ['BRL'], ...]
            supported_codes = [x[0] for x in body_json.get('supported_codes')]

            return code_from in supported_codes and code_to in supported_codes
        except Exception as e:
            raise Exception(f'Error to get supported codes - {e}')

    @classmethod
    def get_pair_tax(self, code_from: str, code_to: str) -> Decimal:
        self._check_api_key()

        if self.check_pair_available_convertion(code_from, code_to):
            try:
                response = urlopen(f'{URL}/pair/{code_from}/{code_to}')
                body_json = json.loads(response.read())
                return Decimal(body_json.get('conversion_rate'))
            except Exception as e:
                raise Exception(f'Error to get tax for pair {code_from}/{code_to} codes - {e}')

    @classmethod
    def get_pair_tax_by_date(self, code_from: str, code_to: str, date: date) -> Decimal:
        self._check_api_key()

        if self.check_pair_available_convertion(code_from, code_to):
            try:
                response = urlopen(f'{URL}/history/{code_from}/{date.year}/{date.month}/{date.day}')
                body_json = json.loads(response.read())
                convertion_rates = body_json.get('conversion_rates')
                return Decimal(convertion_rates[code_to])
            except Exception as e:
                raise Exception(f'Error to get tax for pair {code_from}/{code_to} codes in date {date} - {e}')
