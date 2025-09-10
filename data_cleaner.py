import pandas as pd
from typing import Optional

def remove_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where all values are null."""
    return df.dropna(how='all')

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows."""
    return df.drop_duplicates()

def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """Rename a column in the DataFrame."""
    return df.rename(columns={old_name: new_name})

def convert_numeric(df: pd.DataFrame, columns: Optional[list] = None) -> pd.DataFrame:
    """Convert specified columns to numeric, or all columns that look numeric if columns=None."""
    if columns is None:
        columns = df.columns
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
    return df
