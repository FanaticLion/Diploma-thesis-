import re
from typing import List, Dict, Any
import pandas as pd
import logging
from datetime import datetime
from functools import wraps


def profitable_cashback_categories(data: pd.DataFrame, year: int, month: int) -> Dict[str, float]:
    """Analyze most profitable cashback categories"""
    try:
        filtered = data[
            (data['Дата операции'].dt.year == year) &
            (data['Дата операции'].dt.month == month)
            ]

        cashback_by_category = filtered.groupby('Категория')['Бонусы (включая кэшбэк)'].sum()
        return cashback_by_category.sort_values(ascending=False).to_dict()

    except Exception as e:
        logging.error(f"Error analyzing cashback categories: {e}")
        raise


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Calculate investment savings"""
    try:
        year, month = map(int, month.split('-'))
        total_savings = 0.0

        for t in transactions:
            t_date = datetime.strptime(t['Дата операции'], '%Y-%m-%d')
            if t_date.year == year and t_date.month == month:
                amount = t['Сумма операции']
                if amount < 0:  # Only expenses
                    rounded = ((abs(amount) // limit) + 1) * limit
                    savings = rounded - abs(amount)
                    total_savings += savings

        return round(total_savings, 2)

    except Exception as e:
        logging.error(f"Error calculating investment savings: {e}")
        raise


def simple_search(data: pd.DataFrame, query: str) -> List[Dict[str, Any]]:
    """Search transactions by description or category"""
    try:
        mask = (data['Описание'].str.contains(query, case=False, na=False) |
                data['Категория'].str.contains(query, case=False, na=False))
        return data[mask].to_dict('records')

    except Exception as e:
        logging.error(f"Error in simple search: {e}")
        raise


def phone_number_search(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """Search transactions with phone numbers"""
    try:
        phone_pattern = re.compile(r'\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}')
        mask = data['Описание'].apply(
            lambda x: bool(phone_pattern.search(str(x)))
        )
        return data[mask].to_dict('records')

    except Exception as e:
        logging.error(f"Error in phone number search: {e}")
        raise


def person_transfers_search(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """Search person-to-person transfers"""
    try:
        person_pattern = re.compile(r'[А-Я][а-я]+\s[А-Я]\.')
        mask = (data['Категория'] == 'Переводы') & data['Описание'].apply(
            lambda x: bool(person_pattern.search(str(x)))
        )
        return data[mask].to_dict('records')
    except Exception as e:
        logging.error(f"Error in person transfers search: {e}")
        raise
