# build-in imports
from unittest import main, TestCase

# project imports
from currencypy.currency import Currency


class TestCurrency(TestCase):
    def test_currency_instance(self):
        brl_currency = Currency(value=10.99)
        self.assertIsInstance(brl_currency, Currency)

    def test_currency_value(self):
        brl_currency = Currency(value=10.99)
        self.assertEqual(brl_currency.value, 10.99)

    def test_currency_iso_code(self):
        brl_currency = Currency(value=10.99, iso_code='BRL')
        self.assertEqual(brl_currency.iso_code, 'BRL')

    def test_currency_convert_instance(self):
        brl_currency = Currency(value=10.99, iso_code='BRL')
        usd_currency = brl_currency.convert_to('USD')
        self.assertIsInstance(usd_currency, Currency)

    def test_currency_convert_iso_code(self):
        brl_currency = Currency(value=10.99, iso_code='BRL')
        usd_currency = brl_currency.convert_to('USD')
        self.assertEqual(usd_currency.iso_code, 'USD')

if __name__ == '__main__':
    main()
