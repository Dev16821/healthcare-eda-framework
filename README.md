# Task 2: Exploratory Data Analysis (EDA) Pipeline

## Overview

This project implements a complete Exploratory Data Analysis (EDA) pipeline for healthcare risk assessment data. The system automatically performs statistical analysis, generates visualizations, extracts insights, and creates reports.

The objective is to transform raw healthcare data into meaningful business and analytical insights through automated data exploration.

---

## Features

### Data Analysis

* Dataset overview and structure analysis
* Missing value detection
* Descriptive statistics generation
* Correlation analysis
* Risk-level analysis

### Statistical Testing

* Correlation testing
* Group comparison analysis
* Feature significance evaluation

### Visualization Suite

* Distribution plots
* Box plots by risk category
* Correlation heatmaps
* Violin plots
* Risk distribution charts
* Smoking vs Risk analysis
* Pair plots
* BMI vs Glucose relationship analysis
* Radar charts

### Insight Generation

* Automatic identification of key patterns
* Risk factor discovery
* Feature relationship analysis
* Actionable analytical insights

### Reporting

* Markdown report generation
* JSON statistics export
* JSON insights export

---

## Project Structure

```text
task_2/
│
├── config.py
├── main.py
│
├── src/
│   ├── eda_analyser.py
│   ├── visualizer.py
│   ├── statistical_tests.py
│   ├── insights_engine.py
│   └── report_generator.py
│
├── outputs/
│   ├── figures/
│   └── reports/
│
└── README.md
```

---

## Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

---

## Running the Project

Execute the pipeline:

```bash
python3 main.py
```

The pipeline will:

1. Load the dataset
2. Perform exploratory analysis
3. Execute statistical tests
4. Generate visualizations
5. Extract insights
6. Create reports

---

## Generated Outputs

### Visualizations

Stored in:

```text
outputs/figures/
```

Examples:

* Distribution Analysis
* Correlation Heatmap
* Risk Distribution
* BMI vs Glucose Analysis
* Smoking Risk Analysis
* Radar Charts

### Reports

Stored in:

```text
outputs/reports/
```

Generated files:

```text
eda_statistics.json
task2_insights.json
task2_eda_report.md
```

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* SciPy
* Scikit-Learn

---

## Learning Outcomes

This project demonstrates:

* Data preprocessing
* Exploratory Data Analysis (EDA)
* Statistical analysis
* Data visualization
* Insight generation
* Automated reporting

---

## Author

Vicky

Data Analytics Internship - Task 2
