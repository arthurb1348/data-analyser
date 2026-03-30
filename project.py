import csv
import math
import os
from datetime import datetime


def main():

    print("Welcome to Dataset Analyzer!")
    path = input("Enter the path to your dataset (CSV): ")

    data, headers = load_csv(path)
    if not data:
        print("❌ Could not load Dataset.")
        return

    print(f"\nColumns found: {', '.join(headers)}")
    print("Choose an analysis:\n1. Summary stats\n2. Correlation\n3. Export report")
    choice = input("Your choice: ")

    if choice == "1":
        stats = get_summary_stats(data)
        for col, summary in stats.items():
            print(f"\n--- {col} ---")
            for k, v in summary.items():
                print(f"{k}: {v}")

    elif choice == "2":
        col1 = input("First column: ")
        col2 = input("Second column: ")
        corr = compute_correlation(data, col1, col2)
        print(f"Correlation between {col1} and {col2}: {corr:.3f}")

    elif choice == "3":
        export_report(data)

    else:
        print("Invalid choice.")


def load_csv(filepath):
    """Load CSV and return data as list of dicts + headers."""

    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            data = list(reader)
            return data, reader.fieldnames

    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None


def get_summary_stats(data):
    """Compute min, max, mean for each numeric column."""

    stats = {}
    if not data:
        return stats

    for col in data[0].keys():
        values = [float(row[col]) for row in data if is_number(row.get(col))]
        if values:
            stats[col] = {
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "count": len(values),
            }
    return stats


def is_number(value):
    """Check if value is numeric."""

    try:
        float(value)
        return True

    except ValueError:
        return False


def compute_correlation(data, col1, col2):
    """Compute simple Pearson correlation."""

    pairs = [
        (float(row[col1]), float(row[col2]))
        for row in data
        if is_number(row.get(col1)) and is_number(row.get(col2))
    ]
    n = len(pairs)
    if n == 0:
        return 0

    xs, ys = zip(*pairs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n

    num = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    den = den_x * den_y

    return num / den if den != 0 else 0


def export_report(data, output_dir="reports"):
    """Export simple stats to a text file."""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    stats = get_summary_stats(data)

    col_order = []
    if data and isinstance(data[0], dict):
        for k in data[0].keys():
            if k in stats:
                col_order.append(k)
    else:
        col_order = sorted(stats.keys())

    lines = []
    lines.append("=== DATASET ANALYZER REPORT ===")
    lines.append(f"Generated on: {datetime.now()}")
    lines.append(f"Number of rows: {len(data)}")
    lines.append("------------------------------")
    lines.append("")

    for col in col_order:
        summary = stats[col]
        lines.append(f"Column: {col}")
        for key in ("mean", "min", "max", "count"):
            if key in summary:
                val = summary[key]
                if key == "count":
                    lines.append(f"  {key}: {int(val)}")
                else:
                    lines.append(f"  {key}: {_fmt_num(val, ndigits=2)}")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Report exported successfully to: {filepath}")


def _fmt_num(x, ndigits=2):
    """
    Properly formats a number:
    - displays integers as is
    - rounds floats to ndigits (2 by default)
    - handles None/NaN/inf properly
    """

    if x is None:
        return "None"
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return str(x)

    if math.isnan(xf):
        return "NaN"
    if math.isinf(xf):
        return "Infinity" if xf > 0 else "-Infinity"

    if xf.is_integer():
        return str(int(xf))
    return f"{round(xf, ndigits)}"


if __name__ == "__main__":
    main()
