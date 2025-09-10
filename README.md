# Data Analyzer CLI

A lightweight, modular Python CLI tool for quick dataset exploration, cleaning, analysis, visualization, and reporting. Perfect for students, developers, and analysts who want fast insights from CSV/Excel files without heavy BI tools.

## Features
- Load CSV/Excel datasets from the command line
- Data cleaning (remove nulls, handle duplicates, column renaming)
- Summary statistics (mean, median, std, min, max)
- Group by any column and filter rows by conditions
- Visualizations: line, bar (with annotations), histogram, and pie charts
- PDF reports: append charts and include titles/descriptions per chart
- Correlation analysis: export correlation.csv and correlation heatmap
- Export results as CSV and charts as PNG (all saved in `/reports`)
- Extensible, modular codebase for future enhancements

## Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd data-anlyzer
   ```
2. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage
Place your CSV or Excel file in the project directory. Then run commands like:

### Quick Start
- **Show the first 5 rows:**
  ```bash
  python main.py "Diwali Sales Data.csv" --head
  ```
- **Clean data and show summary statistics (exports CSV):**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --stats --export
  ```

### Filtering & Grouping
- **Filter for female customers and get stats:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --filter "Gender == 'F'" --stats --export
  ```
- **Group by State for female customers:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --filter "Gender == 'F'" --groupby State --export
  ```

### Charts (saved to /reports)
- **Bar chart of Gender vs Amount:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x Gender --y Amount --export
  ```
- **Bar chart of State vs Amount:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x State --y Amount --export
  ```
- **Bar chart of Product_Category vs Orders:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x Product_Category --y Orders --export
  ```
- **Bar chart of Occupation vs Amount for Female Customers:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --filter "Gender == 'F'" --chart bar --x Occupation --y Amount --export
  ```
- **Histogram of Amount:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart hist --col Amount --export
  ```
- **Pie chart of Product_Category:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart pie --col Product_Category --export
  ```

### PDF Reporting
- **Generate a PDF report (append charts to existing report):**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --stats --chart bar --x State --y Amount --export --pdf
  ```
- **Add custom title/description for the chart page in PDF:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart pie --col Gender --export --pdf \
    --chart-title "Gender Distribution" \
    --chart-desc "Pie chart showing male vs female distribution in the dataset."
  ```

### Correlation & Heatmap
- **Export correlation matrix and heatmap:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --correlation --export
  ```
- **Include heatmap in PDF with custom size/title:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --correlation --export --pdf \
    --chart-title "Sales Correlation Heatmap" --figsize "12,8"
  ```
- **Use a different colormap for the heatmap (e.g., viridis):**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --correlation --export --pdf \
    --color "viridis" --chart-title "Correlation Heatmap"
  ```

### Advanced Chart Customization
You can customize charts with these flags:
- `--color` single color name (e.g., `"blue"`, `"green"`, `"skyblue"`)
- `--fontsize` base font size (e.g., `16`)
- `--figsize` figure size as `WIDTH,HEIGHT` (e.g., `"12,8"`)
- `--horizontal` (bar charts only) to plot horizontal bars
- `--grid` to show gridlines
- `--chart-title` and `--chart-desc` to label chart pages in the PDF

Examples:
- **Horizontal bar chart with larger font and grid:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x Occupation --y Amount \
    --export --pdf --horizontal --fontsize 18 --grid --chart-title "Occupation vs Amount"
  ```
- **Pie chart with custom figure size and title:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart pie --col Product_Category \
    --export --pdf --chart-title "Product Category Share" --figsize "10,10"
  ```

> Note: For non-heatmap charts, `--color` must be a single valid matplotlib color (e.g., `"blue"`). For the heatmap, `--color` is treated as a colormap name (e.g., `"viridis"`).

All exported files and charts are saved in the `/reports` folder. The PDF report is `/reports/report.pdf` and appends new charts on each run with `--pdf`.

## CLI Options
Run `python main.py --help` to see all options:
```
usage: main.py [-h] [--head] [--clean] [--rename OLD NEW] [--stats] [--groupby GROUPBY]
               [--filter FILTER] [--chart {line,bar,hist,pie}] [--x X] [--y Y] [--col COL]
               [--export] [--pdf] [--chart-title CHART_TITLE] [--chart-desc CHART_DESC]
               [--color COLOR] [--fontsize FONTSIZE] [--figsize FIGSIZE]
               [--horizontal] [--grid] [--correlation]
               file

positional arguments:
  file                  Path to CSV or Excel file

options:
  -h, --help            show this help message and exit
  --head                Show first 5 rows
  --clean               Clean data (nulls, duplicates)
  --rename OLD NEW      Rename column
  --stats               Show summary statistics
  --groupby GROUPBY     Group by column
  --filter FILTER       Filter condition (e.g., "col>5")
  --chart {line,bar,hist,pie}
                        Chart type
  --x X                 X column for chart (line/bar)
  --y Y                 Y column for chart (line/bar)
  --col COL             Column for histogram/pie
  --export              Export outputs to /reports
  --pdf                 Generate/append a PDF report with charts
  --chart-title CHART_TITLE
                        Title for the chart page in the PDF
  --chart-desc CHART_DESC
                        Description for the chart page in the PDF
  --color COLOR         Single color name (charts) or colormap name (heatmap)
  --fontsize FONTSIZE   Base font size for chart text
  --figsize FIGSIZE     Figure size as WIDTH,HEIGHT (e.g., "12,8")
  --horizontal          Plot horizontal bar chart
  --grid                Show gridlines on chart
  --correlation         Export correlation CSV and heatmap PNG
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change or add.

## License
[MIT](LICENSE)
