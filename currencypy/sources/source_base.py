# build-in imports
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from typing import List


class Sources(ABC):
    @abstractmethod
    def check_pair_available_convertion(self, code_from: str, code_to: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_pair_tax(self, code_from: str, code_to: str) -> Decimal:
        raise NotImplementedError()

    @abstractmethod
    def get_pair_tax_by_date(self, code_from: str, code_to: str, date: date) -> Decimal:
        raise NotImplementedError()