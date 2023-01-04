# build-in imports
from unittest import main, TestCase

# project imports
from currencypy.currency import Currency, DEFAULT_ISO_CODE


class TestCurrency(TestCase):
    def test_currency_creation(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "EUR")
        c3 = Currency(10)

        self.assertEqual(c1.value, 100)
        self.assertEqual(c1.iso_code, "USD")
        self.assertEqual(c2.value, 50)
        self.assertEqual(c2.iso_code, "EUR")
        self.assertEqual(c3.value, 10)
        self.assertEqual(c3.iso_code, DEFAULT_ISO_CODE)

    def test_currency_repr(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "EUR")

        self.assertEqual(repr(c1), "USD100.00")
        self.assertEqual(repr(c2), "EUR+50.00")

    def test_currency_str(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "EUR")

        self.assertEqual(str(c1), "$100.00")
        self.assertEqual(str(c2), "€+50.00")

    def test_currency_addition(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "USD")
        c3 = Currency(50, "EUR")

        self.assertEqual(c1 + c2, Currency(150, "USD"))
        with self.assertRaises(ValueError):
            c1 + c3
        with self.assertRaises(TypeError):
            c1 - 10
        with self.assertRaises(TypeError):
            c1 - 10.1
        with self.assertRaises(TypeError):
            c1 - 'foo'


    def test_currency_subtraction(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "USD")
        c3 = Currency(50, "EUR")

        self.assertEqual(c1 - c2, Currency(50, "USD"))

        with self.assertRaises(ValueError):
            c1 - c3
        with self.assertRaises(TypeError):
            c1 - 10
        with self.assertRaises(TypeError):
            c1 - 10.1
        with self.assertRaises(TypeError):
            c1 - 'foo'

    def test_currency_multiplication(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "USD")
        c3 = Currency(50, "EUR")

        self.assertEqual(c1 * c2, Currency(5000, "USD"))

        with self.assertRaises(ValueError):
            c1 * c3
        with self.assertRaises(TypeError):
            c1 * 1
        with self.assertRaises(TypeError):
            c1 * 1.1
        with self.assertRaises(TypeError):
            c1 * "foo"

    def test_currency_division(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "USD")
        c3 = Currency(50, "EUR")

        self.assertEqual(c1 / c2, Currency(2, "USD"))

        with self.assertRaises(ValueError):
            c1 / c3
        with self.assertRaises(TypeError):
            c1 / 1
        with self.assertRaises(TypeError):
            c1 / 1.1
        with self.assertRaises(TypeError):
            c1 / "foo"

    def test_currency_equality(self):
        c1 = Currency(100, "USD")
        c2 = Currency(100, "USD")
        c3 = Currency(50, "EUR")
        c4 = Currency(10, "EUR")

        self.assertEqual(c1, c2)
        self.assertNotEqual(c3, c4)
        self.assertNotEqual(c1, c3)

        with self.assertRaises(TypeError):
            c1 == 1
        with self.assertRaises(TypeError):
            c1 == 1.1
        with self.assertRaises(TypeError):
            c1 == "foo"

    def test_currency_less_than(self):
        c1 = Currency(50, "USD")
        c2 = Currency(100, "USD")
        c3 = Currency(50, "EUR")

        self.assertEqual(c1 < c2, True)
        self.assertEqual(c2 < c1, False)

        with self.assertRaises(ValueError):
            c1 < c3
        with self.assertRaises(TypeError):
            c1 < 1
        with self.assertRaises(TypeError):
            c1 < 1.1
        with self.assertRaises(TypeError):
            c1 < "foo"

    def test_currency_less_than_or_equal(self):
        c1 = Currency(50, "USD")
        c2 = Currency(100, "USD")
        c3 = Currency(100, "USD")
        c4 = Currency(50, "EUR")

        self.assertEqual(c1 <= c2, True)
        self.assertEqual(c2 <= c3, True)
        self.assertEqual(c3 <= c1, False)
        self.assertEqual(c2 <= c1, False)

        with self.assertRaises(ValueError):
            c1 <= c4
        with self.assertRaises(TypeError):
            c1 <= 1
        with self.assertRaises(TypeError):
            c1 <= 1.1
        with self.assertRaises(TypeError):
            c1 <= "foo"

    def test_currency_greather_than(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "USD")
        c3 = Currency(100, "USD")
        c4 = Currency(50, "EUR")

        self.assertEqual(c1 > c2, True)
        self.assertEqual(c2 > c3, False)
        self.assertEqual(c1 > c3, False)
        self.assertEqual(c2 > c1, False)

        with self.assertRaises(ValueError):
            c1 > c4
        with self.assertRaises(TypeError):
            c1 > 1
        with self.assertRaises(TypeError):
            c1 > 1.1
        with self.assertRaises(TypeError):
            c1 > "foo"

    def test_currency_greather_than_or_equal(self):
        c1 = Currency(100, "USD")
        c2 = Currency(50, "USD")
        c3 = Currency(100, "USD")
        c4 = Currency(50, "EUR")

        self.assertEqual(c1 >= c2, True)
        self.assertEqual(c2 >= c3, False)
        self.assertEqual(c1 >= c3, True)
        self.assertEqual(c2 >= c1, False)

        with self.assertRaises(ValueError):
            c1 >= c4
        with self.assertRaises(TypeError):
            c1 >= 1
        with self.assertRaises(TypeError):
            c1 >= 1.1
        with self.assertRaises(TypeError):
            c1 >= "foo"



if __name__ == "__main__":
    main()
