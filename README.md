# README.md — Dataset Analyzer

#### Video Demo: https://youtu.be/J0Kqp3Ic_Jo

## Introduction
Dataset Analyzer is my final project for **CS50’s Introduction to Programming with Python**.
The goal of this tool is to provide a simple, lightweight, and beginner-friendly way to explore CSV datasets without relying on any external libraries. The program performs essential data analysis operations such as loading structured data, computing descriptive statistics, calculating Pearson correlation coefficients, and exporting a clean analysis report. This project allowed me to apply and consolidate all the concepts learned during CS50P, including functions, loops, exception handling, file I/O, numerical reasoning, and automated testing with `pytest`.

Dataset Analyzer is intentionally designed to remain small, easy to read, and entirely based on Python’s standard library. This makes it portable, understandable, and suitable for educational purposes or quick dataset inspections.

## Project Overview
The program is contained in a single file, `project.py`, which defines the following core functions:

- **`load_csv(path)`**
  Reads a CSV file using `csv.DictReader` and returns a list of dictionaries along with the column headers. It handles unreadable files gracefully through exception handling.

- **`is_number(value)`**
  A utility function that checks whether a value can be safely converted to a float. This ensures robustness when working with messy datasets containing missing or textual values.

- **`get_summary_stats(data)`**
  Computes summary statistics for each numeric column:
  *mean, minimum, maximum, and count of valid entries*.
  The function automatically ignores non-numeric values and empty cells.

- **`compute_correlation(data, col1, col2)`**
  Implements the Pearson correlation formula manually, without external libraries.
  It pairs rows where both columns contain valid numeric values, then computes covariance and normalizes it using the product of standard deviations.

- **`export_report(data, output_dir)`**
  Generates a timestamped text report summarizing the dataset’s characteristics and statistics. The report is formatted neatly and saved inside a “reports” directory.

The **`main()`** function acts as a small command-line interface, allowing users to choose between summary statistics, correlation calculation, or report exportation.

## Motivation
I designed Dataset Analyzer with my long-term interest in **data analysis and artificial intelligence**, particularly in the context of agriculture.
The example dataset used in the demo contains variables such as temperature, humidity, rainfall, and soil moisture — all of which are common in agronomic modeling and environmental monitoring.
This project was also a way to practice clean code structuring, numerical reasoning, and simple data processing workflows, which will be fundamental as I begin CS50AI and later develop more advanced tools.

## Testing
All core functions are tested independently using **`pytest`**.
Tests include:

- loading valid and invalid CSV files
- validating numeric detection
- verifying summary statistics
- checking realistic correlation signs
- handling missing or malformed data
- ensuring that report exportation creates a proper file

These automated tests helped ensure reliability across different scenarios and prevent regressions.

## How to Run
1. Clone this repository
2. Run the program:
   ```bash
   python project.py
   ```
3. Follow the prompts to analyze any CSV dataset.

To run the tests:
```bash
pytest -q
```

## Conclusion
Dataset Analyzer was an excellent opportunity to apply everything learned throughout CS50P.
From structuring functions and validating input to generating readable output and writing tests, this project represents a solid foundation for the next steps in my learning journey — especially as I move toward machine learning and AI.

Thanks for reviewing my work!
This is **CS50**.
