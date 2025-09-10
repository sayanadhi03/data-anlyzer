# Data Analyzer CLI

A lightweight, modular Python CLI tool for quick dataset exploration, cleaning, analysis, visualization, and reporting. Perfect for students, developers, and analysts who want fast insights from CSV/Excel files without heavy BI tools.

## Features
- Load CSV/Excel datasets from the command line
- Data cleaning (remove nulls, handle duplicates, column renaming)
- Summary statistics (mean, median, std, min, max)
- Group by any column
- Filter rows by custom conditions
- Visualizations: line, bar, histogram, and pie charts
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

- **Show the first 5 rows:**
  ```bash
  python main.py "Diwali Sales Data.csv" --head
  ```
- **Clean data and show summary statistics:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --stats --export
  ```
- **Filter for female customers and get stats:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --filter "Gender == 'F'" --stats --export
  ```
- **Group by State for female customers:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --filter "Gender == 'F'" --groupby State --export
  ```
- **Create a bar chart of Gender vs Amount:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x Gender --y Amount --export
  ```
- **Create a bar chart of State vs Amount:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x State --y Amount --export
  ```
- **Create a bar chart of Product_Category vs Orders:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x Product_Category --y Orders --export
  ```
- **Create a bar chart of Occupation vs Amount for Female Customers:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --filter "Gender == 'F'" --chart bar --x Occupation --y Amount --export
  ```
- **Create a bar chart of Age Group vs Amount:**
  ```bash
  python main.py "Diwali Sales Data.csv" --clean --chart bar --x "Age Group" --y Amount --export
  ```

> **Tip:** You can customize the X and Y columns for bar charts to visualize any relationship in your dataset. Each chart will be saved as `bar_chart.png` in the `/reports` folder (overwrite if run multiple times).

All exported files and charts will be saved in the `/reports` folder.

## CLI Options
Run `python main.py --help` to see all options:
```
usage: main.py [-h] [--head] [--clean] [--rename OLD NEW] [--stats] [--groupby GROUPBY]
               [--filter FILTER] [--chart {line,bar,hist,pie}] [--x X] [--y Y] [--col COL]
               [--export]
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
  --export              Export summary and charts to /reports
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change or add.

## License
[MIT](LICENSE)
