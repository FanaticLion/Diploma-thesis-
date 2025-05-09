import pandas as pd
from datetime import datetime
import logging


def load_data(filepath: str) -> pd.DataFrame:
    """Load data from Excel file"""
    try:
        df = pd.read_excel(filepath)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'])
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


def filter_data_by_date(
        df: pd.DataFrame,
        date: str,
        period: str = 'M'
) -> pd.DataFrame:
    """Filter data by date period"""
    target_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    if period == 'W':
        start_date = target_date - pd.Timedelta(days=target_date.weekday())
    elif period == 'M':
        start_date = target_date.replace(day=1)
    elif period == 'Y':
        start_date = target_date.replace(month=1, day=1)
    elif period == 'ALL':
        start_date = df['Дата операции'].min()
    else:
        raise ValueError("Invalid period. Use 'W', 'M', 'Y' or 'ALL'")

    return df[(df['Дата операции'] >= start_date) &
              (df['Дата операции'] <= target_date)]


def get_greeting(time: datetime) -> str:
    """Get greeting based on time of day"""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
