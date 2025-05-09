import unittest
from src.reports import (
    spending_by_category,
    spending_by_weekday,
    spending_by_workday
)
from src.utils import load_data
import pandas as pd


class TestReports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = load_data('data/operations.xlsx')

    def test_spending_by_category(self):
        result = spending_by_category(self.df, 'Супермаркеты', '2021-12-31')
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertFalse(result.empty)

    def test_spending_by_weekday(self):
        result = spending_by_weekday(self.df, '2021-12-31')
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(result), 7)

    def test_spending_by_workday(self):
        result = spending_by_workday(self.df, '2021-12-31')
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(result), 2)
