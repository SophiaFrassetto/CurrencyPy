# build-in imports
import json
from datetime import date
from decimal import Decimal
from urllib.request import urlopen

# project imports
from .source_base import Sources


# set config to use Exchange Rate API v4
URL = 'https://api.exchangerate-api.com/v4'


class ExchangeRateAPIV4(Sources):
    """
        API: Exchange Rate
        API Verion: 4
    """

    @classmethod
    def check_pair_available_convertion(self, code_from: str, code_to: str) -> bool:
        try:
            response = urlopen(f'{URL}/latest/{code_from}')
            body_json = json.loads(response.read())

            supported_codes = list(body_json.get('rates').keys())

            return code_to in supported_codes
        except Exception as e:
            raise Exception(f'Error to get supported codes - {e}')

    @classmethod
    def get_pair_tax(self, code_from: str, code_to: str) -> Decimal:
        if self.check_pair_available_convertion(code_from, code_to):
            try:
                response = urlopen(f'{URL}/latest/{code_from}')
                body_json = json.loads(response.read())
                return Decimal(body_json.get('rates')[code_to])
            except Exception as e:
                raise Exception(f'Error to get tax for pair {code_from}/{code_to} codes - {e}')

    @classmethod
    def get_pair_tax_by_date(self, code_from: str, code_to: str, date: date) -> Decimal:
        raise NotImplementedError()
