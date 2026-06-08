#!/usr/bin/env python3
"""
Task 2 Entry Point
==================
Run: python main.py
"""

import sys
from pathlib import Path

# Allow importing src
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from config import CLEANED_DATA, REPORTS_DIR

from src.eda_analyser import EDAAnalyser
from src.statistical_tests import StatisticalTester
from src.visualizer import Visualizer
from src.insights_engine import InsightsEngine
from src.report_generator import ReportGenerator


def main():
    print("=" * 60)
    print("TASK 2: EDA & BUSINESS INTELLIGENCE")
    print("=" * 60)

    # Load cleaned data from Task 1
    print(f"\n[1/5] Loading cleaned data from Task 1...")
    if not CLEANED_DATA.exists():
        print(f"ERROR: Cleaned data not found at {CLEANED_DATA}")
        print("Run Task 1 first to generate cleaned data.")
        sys.exit(1)

    df = pd.read_csv(CLEANED_DATA)
    print(f"      Loaded {len(df):,} records")

    # EDA
    print("\n[2/5] Running descriptive & correlation analysis...")
    eda = EDAAnalyser(df)
    eda_report = eda.run()
    eda.save_json(REPORTS_DIR / "eda_statistics.json")

    # Statistical Tests
    print("\n[3/5] Performing hypothesis tests...")
    tester = StatisticalTester(df)
    stats_report = tester.run_all()

    # Visualizations
    print("\n[4/5] Generating visualizations...")
    viz = Visualizer(df)
    figure_paths = viz.generate_all()
    print(f"      Generated {len(figure_paths)} figures")

    # Insights
    print("\n[5/5] Extracting business insights...")
    insights_engine = InsightsEngine(df, eda_report, stats_report)
    insights = insights_engine.generate()

    # Report
    print("\n[✓] Writing reports...")
    reporter = ReportGenerator(eda_report, stats_report, insights, figure_paths)
    reporter.save()

    # Console summary
    print("\n" + "-" * 60)
    print("EXECUTIVE SUMMARY")
    print("-" * 60)
    print(f"Dataset:       {insights['executive_summary']['dataset_size']}")
    print(f"High-Risk:     {insights['executive_summary']['high_risk_population']}")
    print(f"Top Predictor: {insights['executive_summary']['top_predictor']}")
    print(f"Quality Grade: {insights['data_quality_score']['grade']}")
    print("-" * 60)
    print("\n✅ Task 2 complete! Check outputs/figures/ and outputs/reports/")


if __name__ == "__main__":
    main()