import pandas as pd
import os

def export_summary_csv(df: pd.DataFrame, filename: str, reports_dir: str = 'reports'):
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, filename)
    df.to_csv(path, index=True)
    return path

# Optional: PDF export placeholder
def export_pdf_report(summary_path: str, chart_paths: list, pdf_path: str):
    # Placeholder for PDF export logic (e.g., using reportlab)
    pass
