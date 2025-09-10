import argparse
from data_loader import load_dataset, show_head
from data_cleaner import remove_nulls, remove_duplicates, rename_column, convert_numeric
from analyzer import summary_statistics, group_by, filter_rows
from visualizer import line_chart, bar_chart, histogram, pie_chart
from reporter import export_summary_csv
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

    # Visualization
    chart_path = None
    if args.chart:
        try:
            if args.chart == 'line' and args.x and args.y:
                chart_path = line_chart(df, args.x, args.y, 'line_chart')
            elif args.chart == 'bar' and args.x and args.y:
                chart_path = bar_chart(df, args.x, args.y, 'bar_chart')
            elif args.chart == 'hist' and args.col:
                chart_path = histogram(df, args.col, 'histogram')
            elif args.chart == 'pie' and args.col:
                chart_path = pie_chart(df, args.col, 'pie_chart')
            else:
                print("Please specify --x and --y for line/bar, or --col for hist/pie.")
            if chart_path:
                print(f"Chart saved to: {chart_path}")
        except Exception as e:
            print(f"Error creating chart: {e}")

if __name__ == '__main__':
    main()
