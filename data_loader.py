import pandas as pd
from typing import Union

def load_dataset(file_path: str) -> pd.DataFrame:
    """Load a dataset from a CSV or Excel file."""
    if file_path.lower().endswith('.csv'):
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='latin1')
    elif file_path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError('Unsupported file format. Please provide a CSV or Excel file.')
    return df

def show_head(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return the first n rows of the DataFrame."""
    return df.head(n)
