import pandas as pd
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader, PdfWriter
import tempfile

def export_summary_csv(df: pd.DataFrame, filename: str, reports_dir: str = 'reports'):
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, filename)
    df.to_csv(path, index=True)
    return path

def export_pdf_report(summary_path: str, chart_info: list, pdf_path: str):
    """
    Append new chart images (with titles/descriptions) to the existing PDF report, preserving all previous pages.
    summary_path: path to summary CSV
    chart_info: list of (chart_path, title, desc)
    pdf_path: output PDF path
    """
    from pandas.plotting import table
    # Step 1: Create a temporary PDF with new content
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
        tmp_pdf_path = tmpfile.name
    with PdfPages(tmp_pdf_path) as pdf:
        # Add summary statistics as a table (only if summary_path is provided and PDF does not exist)
        if summary_path and os.path.exists(summary_path) and not os.path.exists(pdf_path):
            df = pd.read_csv(summary_path, index_col=0)
            fig, ax = plt.subplots(figsize=(8.5, min(11, 0.5 + 0.5*len(df))))
            ax.axis('off')
            tbl = table(ax, df, loc='center', cellLoc='center')
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(8)
            tbl.scale(1, 1.5)
            plt.title('Summary Statistics', fontsize=14)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
        # Add each chart with title/desc
        for chart_path, title, desc in chart_info:
            if os.path.exists(chart_path):
                img = plt.imread(chart_path)
                fig, ax = plt.subplots(figsize=(8.5, 7))
                ax.imshow(img)
                ax.axis('off')
                if title:
                    plt.title(title, fontsize=16)
                if desc:
                    plt.figtext(0.5, 0.01, desc, wrap=True, horizontalalignment='center', fontsize=10)
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
    # Step 2: Merge existing PDF (if any) with new content
    writer = PdfWriter()
    # Add existing pages
    if os.path.exists(pdf_path):
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
    # Add new pages
    new_reader = PdfReader(tmp_pdf_path)
    for page in new_reader.pages:
        writer.add_page(page)
    # Write out the merged PDF
    with open(pdf_path, 'wb') as f_out:
        writer.write(f_out)
    # Clean up temp file
    os.remove(tmp_pdf_path)
    return pdf_path
