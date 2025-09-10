import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Tuple
import os
import numpy as np

def save_chart(fig, chart_name: str, reports_dir: str = 'reports'):
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, f'{chart_name}.png')
    fig.savefig(path)
    plt.close(fig)
    return path

def line_chart(df: pd.DataFrame, x: str, y: str, chart_name: str, reports_dir: str = 'reports', title: Optional[str] = None, color: Optional[str] = None, fontsize: int = 12, figsize: Tuple[float, float] = (10,6), grid: bool = False):
    fig, ax = plt.subplots(figsize=figsize)
    df.plot(x=x, y=y, kind='line', ax=ax, color=color)
    ax.set_xlabel(x, fontsize=fontsize)
    ax.set_ylabel(y, fontsize=fontsize)
    if title:
        ax.set_title(title, fontsize=fontsize+2)
    if grid:
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    return save_chart(fig, chart_name, reports_dir)

def bar_chart(df: pd.DataFrame, x: str, y: str, chart_name: str, reports_dir: str = 'reports', title: Optional[str] = None, color: Optional[str] = None, fontsize: int = 12, figsize: Tuple[float, float] = (10,6), horizontal: bool = False, grid: bool = False):
    fig, ax = plt.subplots(figsize=figsize)
    grouped = df.groupby(x)[y].sum().sort_values()
    if horizontal:
        bars = grouped.plot(kind='barh', ax=ax, color=color if color else 'skyblue')
        for p in ax.patches:
            ax.annotate(f'{p.get_width():.0f}', (p.get_width(), p.get_y() + p.get_height() / 2),
                        ha='left', va='center', fontsize=fontsize)
        ax.set_xlabel(y, fontsize=fontsize)
        ax.set_ylabel(x, fontsize=fontsize)
    else:
        bars = grouped.plot(kind='bar', ax=ax, color=color if color else 'skyblue')
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2, p.get_height()),
                        ha='center', va='bottom', fontsize=fontsize)
        ax.set_xlabel(x, fontsize=fontsize)
        ax.set_ylabel(y, fontsize=fontsize)
    if title:
        ax.set_title(title, fontsize=fontsize+2)
    if grid:
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    return save_chart(fig, chart_name, reports_dir)

def histogram(df: pd.DataFrame, column: str, chart_name: str, reports_dir: str = 'reports', title: Optional[str] = None, color: Optional[str] = None, fontsize: int = 12, figsize: Tuple[float, float] = (10,6), grid: bool = False):
    fig, ax = plt.subplots(figsize=figsize)
    df[column].plot(kind='hist', ax=ax, color=color if color else 'lightgreen', edgecolor='black')
    ax.set_xlabel(column, fontsize=fontsize)
    ax.set_ylabel('Frequency', fontsize=fontsize)
    if title:
        ax.set_title(title, fontsize=fontsize+2)
    if grid:
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    return save_chart(fig, chart_name, reports_dir)

def pie_chart(df: pd.DataFrame, column: str, chart_name: str, reports_dir: str = 'reports', title: Optional[str] = None, color: Optional[str] = None, fontsize: int = 12, figsize: Tuple[float, float] = (8,8)):
    fig, ax = plt.subplots(figsize=figsize)
    counts = df[column].value_counts()
    wedges, texts, autotexts = ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': fontsize}, colors=plt.get_cmap(color)(range(len(counts))) if color else None)
    for autotext in autotexts:
        autotext.set_color('white')
    if title:
        ax.set_title(title, fontsize=fontsize+2)
    plt.tight_layout()
    return save_chart(fig, chart_name, reports_dir)

def heatmap(corr: pd.DataFrame, chart_name: str = 'correlation_heatmap', reports_dir: str = 'reports', title: Optional[str] = None, cmap: str = 'coolwarm', fontsize: int = 12, figsize: Tuple[float, float] = (10,8)):
    fig, ax = plt.subplots(figsize=figsize)
    cax = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=fontsize-1)
    ax.set_yticklabels(corr.index, fontsize=fontsize-1)
    # Annotate cells
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(j, i, f"{corr.values[i, j]:.2f}", ha='center', va='center', color='black', fontsize=fontsize-2)
    fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    if title:
        ax.set_title(title, fontsize=fontsize+2)
    plt.tight_layout()
    return save_chart(fig, chart_name, reports_dir)
