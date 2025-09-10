import pandas as pd
from typing import Optional

def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Return summary statistics (mean, median, std, min, max) for numeric columns."""
    stats = df.describe().T
    stats['median'] = df.median(numeric_only=True)
    return stats[['mean', 'median', 'std', 'min', 'max']]

def group_by(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Group by a column and return mean of numeric columns."""
    return df.groupby(column).mean(numeric_only=True)

def filter_rows(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    """Filter rows by a condition string, e.g., 'col>5'."""
    return df.query(condition)
