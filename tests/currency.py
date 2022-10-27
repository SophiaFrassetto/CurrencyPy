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


if __name__ == '__main__':
    main()
