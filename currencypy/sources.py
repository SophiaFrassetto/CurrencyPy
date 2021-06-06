from __future__ import annotations
import requests
from datetime import datetime
from datetime import date
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class CurrencyQuote:
    pair: str
    buy: float
    sell: float
    date: datetime


class Sources(ABC):
    @abstractmethod
    def check_available_convertion(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def convert(self) -> CurrencyQuote:
        raise NotImplementedError()

    @abstractmethod
    def convert_by_date(self, pair: str, date: date) -> CurrencyQuote:
        raise NotImplementedError()

    @abstractmethod
    def convert_by_date_range(self, pair: str, start_date: date, end_date: date) -> List[CurrencyQuote]:
        raise NotImplementedError()


class EconomiaAwesomeAPI(Sources):
    @classmethod
    def check_available_convertion(self, pair: str) -> bool:
        response = requests.get('https://economia.awesomeapi.com.br/json/available')
        if response.status_code == 200:
            pairs = response.json()
            return pair in pairs
        return False

    @classmethod
    def convert(self, pair: str) -> CurrencyQuote:
        if self.check_available_convertion(pair):
            response = requests.get(f'https://economia.awesomeapi.com.br/last/{pair}')
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
            response = requests.get(f'https://economia.awesomeapi.com.br/{pair}/1?start_date={timestp}&end_date={timestp}')
            if response.status_code == 200:
                data = response.json()
                if data:
                    data = data[0]
                    quote = CurrencyQuote(pair=pair, buy=float(data['bid']), sell=float(data['ask']), date=datetime.fromtimestamp(int(data['timestamp'])))
                    return quote
            raise NotImplementedError()
