# build-in imports
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from datetime import datetime
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