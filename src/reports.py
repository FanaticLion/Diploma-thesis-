import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging
from functools import wraps


def report_decorator(filename=None):
    """Decorator to save report results to file"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Determine filename
            if filename is None:
                fname = f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d')}.txt"
            else:
                fname = filename

            # Save to file
            try:
                with open(fname, 'w') as f:
                    if isinstance(result, pd.DataFrame):
                        f.write(result.to_string())
                    else:
                        f.write(str(result))
            except Exception as e:
                logging.warning(f"Could not save report to file: {e}")

            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    """Get spending by category for last 3 months"""
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, '%Y-%m-%d')

        start_date = date - timedelta(days=90)

        filtered = transactions[
            (transactions['Дата операции'] >= start_date) &
            (transactions['Дата операции'] <= date) &
            (transactions['Категория'] == category) &
            (transactions['Сумма операции'] < 0)
            ]

        return filtered.groupby(
            pd.Grouper(key='Дата операции', freq='M')
        )['Сумма операции'].sum().abs().reset_index()

    except Exception as e:
        logging.error(f"Error in spending_by_category: {e}")
        raise


@report_decorator()
def spending_by_weekday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> pd.DataFrame:
    """Get average spending by weekday for last 3 months"""
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, '%Y-%m-%d')

        start_date = date - timedelta(days=90)

        filtered = transactions[
            (transactions['Дата операции'] >= start_date) &
            (transactions['Дата операции'] <= date) &
            (transactions['Сумма операции'] < 0)
            ]

        filtered['День недели'] = filtered['Дата операции'].dt.day_name()
        return filtered.groupby('День недели')['Сумма операции'].mean().abs().reset_index()

    except Exception as e:
        logging.error(f"Error in spending_by_weekday: {e}")
        raise


@report_decorator()
def spending_by_workday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> pd.DataFrame:
    """Get average spending on workdays vs weekends"""
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, '%Y-%m-%d')

        start_date = date - timedelta(days=90)

        filtered = transactions[
            (transactions['Дата операции'] >= start_date) &
            (transactions['Дата операции'] <= date) &
            (transactions['Сумма операции'] < 0)
            ]

        filtered['Тип дня'] = filtered['Дата операции'].dt.weekday.apply(
            lambda x: 'Выходной' if x >= 5 else 'Рабочий'
        )

        return filtered.groupby('Тип дня')['Сумма операции'].mean().abs().reset_index()

    except Exception as e:
        logging.error(f"Error in spending_by_workday: {e}")
        raise
