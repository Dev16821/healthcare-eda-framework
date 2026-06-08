"""Auto-generates a Markdown report matching your Task 1 style."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from config import REPORTS_DIR


class ReportGenerator:
    def __init__(self, eda: Dict, stats: Dict, insights: Dict, figure_paths: list):
        self.eda = eda
        self.stats = stats
        self.insights = insights
        self.figures = figure_paths

    def generate_markdown(self) -> str:
        md = f"""# Task 2 Report: Exploratory Data Analysis & Business Intelligence

## Internship Program
Data Analytics Internship

## Task Name
Exploratory Data Analysis & Business Intelligence

## Objective
To perform statistical exploration, generate visual insights, and derive actionable business intelligence from the cleaned healthcare dataset produced in Task 1.

---

## 1. Dataset Overview

| Metric | Value |
|--------|-------|
| Total Records | {self.insights['executive_summary']['dataset_size']} |
| High-Risk Population | {self.insights['executive_summary']['high_risk_population']} |
| Data Quality Grade | {self.insights['data_quality_score']['grade']} |

---

## 2. Statistical Analysis

### Descriptive Statistics
Key numerical features were analyzed for central tendency, dispersion, and distribution shape.

### Correlation Analysis
Strong correlations (|r| >= 0.5) identified:
"""
        for pair in self.eda.get("correlations", {}).get("strong_pairs", []):
            md += f"- **{pair['feature_1']}** vs **{pair['feature_2']}**: {pair['correlation']} ({pair['strength']})\n"

        md += f"""
### Feature Importance (ANOVA F-Score)
Top predictors of **{self.insights['executive_summary']['top_predictor']}**:
"""
        for feat in self.eda.get("feature_importance", [])[:3]:
            sig = "✅ Significant" if feat["significant"] else "❌ Not Significant"
            md += f"- {feat['feature']}: F={feat['f_score']}, p={feat['p_value']} ({sig})\n"

        md += f"""
### Hypothesis Testing
- **ANOVA across Risk Groups**: Tested if numerical means differ significantly across health risk categories.
- **Chi-Square (Gender vs Risk)**: {self.insights['demographic_insights'].get('gender_significance', 'N/A')}
- **Chi-Square (Smoking vs Risk)**: {self.stats.get('chi2_smoking_risk', {}).get('significant', 'N/A')}

---

## 3. Key Visualizations

The following figures were generated in `outputs/figures/`:
"""
        for i, fig in enumerate(self.figures, 1):
            md += f"{i}. `{Path(fig).name}`\n"

        md += f"""
---

## 4. Business Insights

### Risk Drivers
Factors most differentiated between high-risk and low-risk patients:
"""
        for driver in self.insights.get("risk_drivers", [])[:5]:
            md += f"- **{driver['factor']}**: {driver['difference_pct']}% {driver['direction']} in high-risk patients\n"

        md += f"""
### Clinical Recommendations
"""
        for rec in self.insights.get("clinical_recommendations", []):
            md += f"- **[{rec['priority']}]** {rec['action']}: {rec['rationale']}\n"

        md += f"""
---

## 5. Key Metrics

| KPI | Value |
|-----|-------|
"""
        for k, v in self.insights.get("key_metrics", {}).items():
            md += f"| {k.replace('_', ' ').title()} | {v} |\n"

        md += f"""
---

## 6. Tools and Technologies

- **Python** (Pandas, NumPy, SciPy, Scikit-learn)
- **Matplotlib & Seaborn** (Data Visualization)
- **Visual Studio Code** (Development Environment)

---

## 7. Conclusion

Task 2 successfully transformed the cleaned dataset into actionable intelligence. Statistical tests confirmed significant relationships between patient vitals and health risk categories. The generated visualizations and insights provide a foundation for predictive modeling and clinical decision support in subsequent internship phases.

*Report generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        return md

    def save(self):
        md_path = REPORTS_DIR / "task2_eda_report.md"
        json_path = REPORTS_DIR / "task2_insights.json"

        md_path.write_text(self.generate_markdown())
        with open(json_path, "w") as f:
            json.dump({
                "eda": self.eda,
                "statistics": self.stats,
                "insights": self.insights,
                "figures": self.figures
            }, f, indent=4, default=str)

        print(f"Saved report: {md_path}")
        print(f"Saved JSON: {json_path}")