from datetime import datetime
import logging
from typing import Dict, List, Any
import pandas as pd
import requests
import json
from .utils import load_data, filter_data_by_date, get_greeting


def get_main_page_data(date_str: str) -> Dict[str, Any]:
    """Generate data for main page"""
    try:
        # Load data
        df = load_data('data/operations.xlsx')

        # Filter data for current month
        current_month_df = filter_data_by_date(df, date_str, 'M')

        # Get greeting
        current_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        greeting = get_greeting(current_time)

        # Process cards data
        cards_data = []
        for card in df['Номер карты'].unique():
            if pd.isna(card):
                continue

            last_digits = str(card)[-4:]
            card_df = current_month_df[current_month_df['Номер карты'] == card]
            total_spent = card_df[card_df['Сумма операции'] < 0]['Сумма операции'].sum() * -1
            cashback = total_spent * 0.01  # 1% cashback

            cards_data.append({
                'last_digits': last_digits,
                'total_spent': round(total_spent, 2),
                'cashback': round(cashback, 2)
            })

        # Get top 5 transactions
        top_transactions = current_month_df.nlargest(5, 'Сумма платежа')[
            ['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]
        top_transactions = top_transactions.to_dict('records')

        # Get currency rates and stock prices from user settings
        with open('user_settings.json') as f:
            settings = json.load(f)

        # This would be replaced with actual API calls in production
        currency_rates = [{'currency': c, 'rate': 75.0} for c in settings['user_currencies']]
        stock_prices = [{'stock': s, 'price': 100.0} for s in settings['user_stocks']]

        return {
            'greeting': greeting,
            'cards': cards_data,
            'top_transactions': top_transactions,
            'currency_rates': currency_rates,
            'stock_prices': stock_prices
        }

    except Exception as e:
        logging.error(f"Error generating main page data: {e}")
        raise


def get_events_page_data(date_str: str, period: str = 'M') -> Dict[str, Any]:
    """Generate data for events page"""
    try:
        df = load_data('data/operations.xlsx')
        filtered_df = filter_data_by_date(df, date_str, period)

        # Expenses
        expenses_df = filtered_df[filtered_df['Сумма операции'] < 0]
        expenses_total = round(expenses_df['Сумма операции'].sum() * -1)

        # Main expenses categories (top 7)
        main_expenses = expenses_df.groupby('Категория')['Сумма операции'].sum().sort_values()
        main_expenses = main_expenses * -1  # Convert to positive
        if len(main_expenses) > 7:
            other = main_expenses[7:].sum()
            main_expenses = main_expenses[:7]
            main_expenses['Остальное'] = other

        # Transfers and cash
        transfers_cash = expenses_df[
            expenses_df['Категория'].isin(['Переводы', 'Наличные'])
        ]
        transfers_cash = transfers_cash.groupby('Категория')['Сумма операции'].sum().sort_values()
        transfers_cash = transfers_cash * -1  # Convert to positive

        # Income
        income_df = filtered_df[filtered_df['Сумма операции'] > 0]
        income_total = round(income_df['Сумма операции'].sum())
        main_income = income_df.groupby('Категория')['Сумма операции'].sum().sort_values(ascending=False)

        # Get currency rates and stock prices from user settings
        with open('user_settings.json') as f:
            settings = json.load(f)

        # This would be replaced with actual API calls in production
        currency_rates = [{'currency': c, 'rate': 75.0} for c in settings['user_currencies']]
        stock_prices = [{'stock': s, 'price': 100.0} for s in settings['user_stocks']]

        return {
            'expenses': {
                'total_amount': expenses_total,
                'main': [{'category': k, 'amount': round(v)} for k, v in main_expenses.items()],
                'transfers_and_cash': [{'category': k, 'amount': round(v)} for k, v in transfers_cash.items()]
            },
            'income': {
                'total_amount': income_total,
                'main': [{'category': k, 'amount': round(v)} for k, v in main_income.items()]
            },
            'currency_rates': currency_rates,
            'stock_prices': stock_prices
        }

    except Exception as e:
        logging.error(f"Error generating events page data: {e}")
        raise
