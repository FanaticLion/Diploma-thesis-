import unittest
from datetime import datetime
from src.views import get_main_page_data, get_events_page_data
from src.utils import load_data
import pandas as pd


class TestViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = load_data('data/operations.xlsx')

    def test_get_main_page_data(self):
        date_str = '2021-12-31 23:59:59'
        result = get_main_page_data(date_str)

        self.assertIn('greeting', result)
        self.assertIn('cards', result)
        self.assertIn('top_transactions', result)
        self.assertIn('currency_rates', result)
        self.assertIn('stock_prices', result)

        self.assertTrue(isinstance(result['cards'], list))
        self.assertTrue(isinstance(result['top_transactions'], list))

    def test_get_events_page_data(self):
        date_str = '2021-12-31 23:59:59'
        result = get_events_page_data(date_str)

        self.assertIn('expenses', result)
        self.assertIn('income', result)
        self.assertIn('currency_rates', result)
        self.assertIn('stock_prices', result)

        self.assertIn('total_amount', result['expenses'])
        self.assertIn('main', result['expenses'])
        self.assertIn('transfers_and_cash', result['expenses'])

        self.assertIn('total_amount', result['income'])
        self.assertIn('main', result['income'])
