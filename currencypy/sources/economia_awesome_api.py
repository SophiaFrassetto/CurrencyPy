# build-in imports
from datetime import datetime
from datetime import date

# external imports
from requests import get as rGet

# project imports
from .source_base import Sources
from .source_base import CurrencyQuote


class EconomiaAwesomeAPI(Sources):
    @classmethod
    def check_available_convertion(self, pair: str) -> bool:
        response = rGet('https://economia.awesomeapi.com.br/json/available')
        if response.status_code == 200:
            pairs = response.json()
            return pair in pairs
        return False

    @classmethod
    def convert(self, pair: str) -> CurrencyQuote:
        if self.check_available_convertion(pair):
            response = rGet(f'https://economia.awesomeapi.com.br/last/{pair}')
            if response.status_code == 200:
                data = response.json()
                if data:
                    data = data[pair.replace('-', '')]
                    quote = CurrencyQuote(pair=pair, buy=float(data['bid']), sell=float(data['ask']), date=datetime.fromtimestamp(int(data['timestamp'])))
                    return quote
            raise NotImplementedError()

    @classmethod
    def convert_by_date(self, pair: str, date: date) -> CurrencyQuote:
        if self.check_available_convertion(pair):
            timestp = date.strftime('%Y%m%d')
            response = rGet(f'https://economia.awesomeapi.com.br/{pair}/1?start_date={timestp}&end_date={timestp}')
            if response.status_code == 200:
                data = response.json()
                if data:
                    data = data[0]
                    quote = CurrencyQuote(pair=pair, buy=float(data['bid']), sell=float(data['ask']), date=datetime.fromtimestamp(int(data['timestamp'])))
                    return quote
            raise NotImplementedError()