import argparse
from data_loader import load_dataset, show_head
from data_cleaner import remove_nulls, remove_duplicates, rename_column, convert_numeric
from analyzer import summary_statistics, group_by, filter_rows, correlation_matrix
from visualizer import line_chart, bar_chart, histogram, pie_chart, heatmap
from reporter import export_summary_csv, export_pdf_report
import sys
import os

def main():
    parser = argparse.ArgumentParser(description='Data Analyzer CLI')
    parser.add_argument('file', type=str, help='Path to CSV or Excel file')
    parser.add_argument('--head', action='store_true', help='Show first 5 rows')
    parser.add_argument('--clean', action='store_true', help='Clean data (nulls, duplicates)')
    parser.add_argument('--rename', nargs=2, metavar=('OLD','NEW'), help='Rename column')
    parser.add_argument('--stats', action='store_true', help='Show summary statistics')
    parser.add_argument('--groupby', type=str, help='Group by column')
    parser.add_argument('--filter', type=str, help='Filter condition (e.g., "col>5")')
    parser.add_argument('--chart', type=str, choices=['line','bar','hist','pie'], help='Chart type')
    parser.add_argument('--x', type=str, help='X column for chart (line/bar)')
    parser.add_argument('--y', type=str, help='Y column for chart (line/bar)')
    parser.add_argument('--col', type=str, help='Column for histogram/pie')
    parser.add_argument('--export', action='store_true', help='Export summary and charts to /reports')
    parser.add_argument('--pdf', action='store_true', help='Generate PDF report with summary and charts')
    parser.add_argument('--chart-title', type=str, help='Title for the chart in the PDF')
    parser.add_argument('--chart-desc', type=str, help='Description for the chart in the PDF')
    parser.add_argument('--color', type=str, help='Color or color palette for the chart (e.g., "red" or "Blues")')
    parser.add_argument('--fontsize', type=int, help='Base font size for chart text')
    parser.add_argument('--figsize', type=str, help='Figure size as WIDTH,HEIGHT (e.g., "10,6")')
    parser.add_argument('--horizontal', action='store_true', help='Plot horizontal bar chart')
    parser.add_argument('--grid', action='store_true', help='Show gridlines on chart')
    parser.add_argument('--correlation', action='store_true', help='Export correlation CSV and heatmap PNG')
    args = parser.parse_args()

    # Load dataset
    try:
        df = load_dataset(args.file)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)

    # Show head
    if args.head:
        print("\nFirst 5 rows:")
        print(show_head(df))

    # Clean data
    if args.clean:
        df = remove_nulls(df)
        df = remove_duplicates(df)
        df = convert_numeric(df)
        print("\nData cleaned (nulls and duplicates removed).")
        print("Data types after cleaning:")
        print(df.dtypes)

    # Rename column
    if args.rename:
        old, new = args.rename
        try:
            df = rename_column(df, old, new)
            print(f"\nRenamed column {old} to {new}.")
        except Exception as e:
            print(f"Error renaming column: {e}")

    # Filter rows
    if args.filter:
        try:
            df = filter_rows(df, args.filter)
            print(f"\nFiltered rows with condition: {args.filter}")
        except Exception as e:
            print(f"Error filtering rows: {e}")

    # Always export cleaned dataset if --export is used
    if args.export:
        export_summary_csv(df, 'cleaned_data.csv')
        print("Cleaned data exported to /reports/cleaned_data.csv")

    # Group by
    if args.groupby:
        try:
            grouped = group_by(df, args.groupby)
            print(f"\nGrouped by {args.groupby}:")
            print(grouped)
            if args.export:
                export_summary_csv(grouped, f'groupby_{args.groupby}.csv')
                print(f"Grouped data exported to /reports/groupby_{args.groupby}.csv")
        except Exception as e:
            print(f"Error in group by: {e}")

    # Summary statistics
    if args.stats:
        stats = summary_statistics(df)
        print("\nSummary statistics:")
        print(stats)
        if args.export:
            export_summary_csv(stats, 'summary_statistics.csv')
            print("Summary statistics exported to /reports/summary_statistics.csv")

    chart_infos = []
    # Parse figsize
    figsize = (10, 6)
    if args.figsize:
        try:
            w, h = map(float, args.figsize.split(','))
            figsize = (w, h)
        except Exception:
            print('Invalid --figsize format. Using default (10,6).')
    fontsize = args.fontsize if args.fontsize else 12
    color = args.color if args.color else None
    # Visualization
    if args.chart:
        try:
            chart_path = None
            if args.chart == 'line' and args.x and args.y:
                chart_path = line_chart(df, args.x, args.y, 'line_chart', title=args.chart_title, color=color, fontsize=fontsize, figsize=figsize, grid=args.grid)
            elif args.chart == 'bar' and args.x and args.y:
                chart_path = bar_chart(df, args.x, args.y, 'bar_chart', title=args.chart_title, color=color, fontsize=fontsize, figsize=figsize, horizontal=args.horizontal, grid=args.grid)
            elif args.chart == 'hist' and args.col:
                chart_path = histogram(df, args.col, 'histogram', title=args.chart_title, color=color, fontsize=fontsize, figsize=figsize, grid=args.grid)
            elif args.chart == 'pie' and args.col:
                chart_path = pie_chart(df, args.col, 'pie_chart', title=args.chart_title, color=color, fontsize=fontsize, figsize=figsize)
            else:
                print("Please specify --x and --y for line/bar, or --col for hist/pie.")
            if chart_path:
                print(f"Chart saved to: {chart_path}")
                chart_infos.append((chart_path, args.chart_title, args.chart_desc))
        except Exception as e:
            print(f"Error creating chart: {e}")

    # Correlation + Heatmap
    if args.correlation:
        try:
            corr = correlation_matrix(df)
            if corr.empty:
                print('No numeric columns available for correlation.')
            else:
                corr_csv = export_summary_csv(corr, 'correlation.csv')
                print('Correlation matrix exported to /reports/correlation.csv')
                # Use color as cmap if provided, else default
                cmap = args.color if args.color else 'coolwarm'
                heatmap_path = heatmap(corr, chart_name='correlation_heatmap', title=args.chart_title or 'Correlation Heatmap', cmap=cmap, fontsize=fontsize, figsize=figsize)
                print(f'Heatmap saved to: {heatmap_path}')
                chart_infos.append((heatmap_path, args.chart_title or 'Correlation Heatmap', args.chart_desc))
        except Exception as e:
            print(f'Error computing correlation/heatmap: {e}')

    # PDF report generation (append new charts if PDF exists)
    if args.pdf:
        summary_path = os.path.join('reports', 'summary_statistics.csv')
        pdf_path = os.path.join('reports', 'report.pdf')
        from reporter import export_pdf_report
        export_pdf_report(summary_path, chart_infos, pdf_path)
        print(f"PDF report updated at {pdf_path}")

if __name__ == '__main__':
    main()
