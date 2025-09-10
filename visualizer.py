import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional
import os

def save_chart(fig, chart_name: str, reports_dir: str = 'reports'):
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, f'{chart_name}.png')
    fig.savefig(path)
    plt.close(fig)
    return path

def line_chart(df: pd.DataFrame, x: str, y: str, chart_name: str, reports_dir: str = 'reports'):
    fig, ax = plt.subplots()
    df.plot(x=x, y=y, kind='line', ax=ax)
    return save_chart(fig, chart_name, reports_dir)

def bar_chart(df: pd.DataFrame, x: str, y: str, chart_name: str, reports_dir: str = 'reports'):
    fig, ax = plt.subplots()
    df.plot(x=x, y=y, kind='bar', ax=ax)
    return save_chart(fig, chart_name, reports_dir)

def histogram(df: pd.DataFrame, column: str, chart_name: str, reports_dir: str = 'reports'):
    fig, ax = plt.subplots()
    df[column].plot(kind='hist', ax=ax)
    return save_chart(fig, chart_name, reports_dir)

def pie_chart(df: pd.DataFrame, column: str, chart_name: str, reports_dir: str = 'reports'):
    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_ylabel('')
    return save_chart(fig, chart_name, reports_dir)
