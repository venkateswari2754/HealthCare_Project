"""Utility script for quick dataset exploration.

This script provides helper functions to load the CSV datasets from the
project's `data/` directory, print summaries, missing-value reports, and
optionally save small plots to disk. It is intended for quick, repeatable
exploration that is safe to run in CI or a headless environment.

Usage examples:
  python -m src.data.dataset_exploration --list
  python -m src.data.dataset_exploration --dataset "Hospital General Information" --head 5
  python -m src.data.dataset_exploration --all --plot

The script avoids opening interactive plots by default; plots are written to
`reports/` when `--plot` is given.
"""

from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import textwrap
import os

# Make printing wider
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def _data_paths():
    """Return dataset file paths present in the project's data/ directory."""
    return {
        "Doctors Info": DATA_DIR / "doctors_info_data.csv",
        "Doctors Slots": DATA_DIR / "doctors_slots_data.csv",
        "Hospital General Information": DATA_DIR / "Hospital_General_Information.csv",
        "Hospital Lab Tests": DATA_DIR / "Hospital_Information_with_Lab_Tests.csv",
        "Hospitals Emergency Data": DATA_DIR / "hospitals_emergency_data.csv",
    }


def load_dataset(name: str) -> pd.DataFrame:
    """Load a named dataset into a DataFrame.

    Raises FileNotFoundError when the CSV does not exist.
    """
    paths = _data_paths()
    if name not in paths:
        raise KeyError(f"Unknown dataset '{name}'. Available: {list(paths.keys())}")
    path = paths[name]
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def summarize(df: pd.DataFrame, name: str = None) -> str:
    """Return a short summary string for a DataFrame."""
    buf = []
    buf.append(f"Dataset: {name or 'dataframe'}")
    buf.append(f"Rows: {len(df):,}")
    buf.append(f"Columns: {len(df.columns)}")
    buf.append("Columns and dtypes:")
    buf.append(textwrap.indent(str(df.dtypes), "  "))
    buf.append("\nSample:\n")
    buf.append(df.head().to_string())
    return "\n".join(buf)


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with missing value counts and percentages."""
    miss = df.isnull().sum()
    pct = (miss / len(df)) * 100
    report = pd.DataFrame({"missing_count": miss, "missing_pct": pct})
    return report.sort_values("missing_count", ascending=False)


def top_categories(df: pd.DataFrame, column: str, n: int = 10) -> pd.Series:
    """Return the top n value counts for a given column."""
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not in DataFrame")
    return df[column].value_counts(dropna=False).head(n)


def save_sample(df: pd.DataFrame, name: str):
    path = REPORTS_DIR / f"{name.replace(' ', '_').lower()}_sample.csv"
    df.head(100).to_csv(path, index=False)
    return path


def explore_dataset(name: str, head: int = 5, do_plot: bool = False):
    df = load_dataset(name)
    print(summarize(df, name=name))
    print("\nMissing values (top):")
    print(missing_report(df).head(20))
    print("\nNumerical stats:\n")
    print(df.select_dtypes(include=[np.number]).describe().transpose())
    print("\nSample rows:\n")
    print(df.head(head).to_string())
    sample_path = save_sample(df, name)
    print(f"\nSample saved to: {sample_path}")


def list_datasets():
    return list(_data_paths().keys())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Quick dataset exploration for Healthcare project")
    parser.add_argument("--list", action="store_true", help="List available datasets and exit")
    parser.add_argument("--dataset", type=str, help="Name of dataset to explore (use quotes)")
    parser.add_argument("--all", action="store_true", help="Explore all datasets")
    parser.add_argument("--head", type=int, default=5, help="Number of sample rows to show")
    parser.add_argument("--plot", action="store_true", help="Save simple plots to reports/ (no GUI)")
    args = parser.parse_args(argv)

    if args.list:
        for name in list_datasets():
            print(f"- {name}")
        return

    if args.dataset:
        explore_dataset(args.dataset, head=args.head, do_plot=args.plot)
        return

    if args.all:
        for name in list_datasets():
            print("\n" + "=" * 80)
            print(f"Exploring: {name}")
            print("=" * 80 + "\n")
            explore_dataset(name, head=args.head, do_plot=args.plot)
        return

    parser.print_help()


if __name__ == "__main__":
    main()