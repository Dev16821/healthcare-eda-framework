# Task 2 Report: Exploratory Data Analysis & Business Intelligence

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
| Total Records | 11,397 patients |
| High-Risk Population | 0.0% |
| Data Quality Grade | A |

---

## 2. Statistical Analysis

### Descriptive Statistics
Key numerical features were analyzed for central tendency, dispersion, and distribution shape.

### Correlation Analysis
Strong correlations (|r| >= 0.5) identified:

### Feature Importance (ANOVA F-Score)
Top predictors of **glucose_level**:
- glucose_level: F=1580.31, p=0.0 (✅ Significant)
- blood_pressure: F=935.92, p=0.0 (✅ Significant)
- cholesterol: F=515.91, p=0.0 (✅ Significant)

### Hypothesis Testing
- **ANOVA across Risk Groups**: Tested if numerical means differ significantly across health risk categories.
- **Chi-Square (Gender vs Risk)**: Not Significant
- **Chi-Square (Smoking vs Risk)**: False

---

## 3. Key Visualizations

The following figures were generated in `outputs/figures/`:
1. `01_distributions.png`
2. `02_boxplots_by_risk.png`
3. `03_correlation_heatmap.png`
4. `04_violin_plots.png`
5. `05_risk_distribution.png`
6. `07_smoking_risk.png`
7. `08_pairplot.png`
8. `09_bmi_glucose.png`
9. `10_radar_chart.png`

---

## 4. Business Insights

### Risk Drivers
Factors most differentiated between high-risk and low-risk patients:
- **glucose_level**: 43.3% higher in high-risk patients
- **blood_pressure**: 18.7% higher in high-risk patients
- **cholesterol**: 18.1% higher in high-risk patients
- **bmi**: 11.1% higher in high-risk patients

### Clinical Recommendations
- **[High]** Monitor glucose_level closely: High-risk patients show 43.3% higher glucose_level vs low-risk.
- **[High]** Weight management programs: BMI significantly differentiates risk categories.
- **[Medium]** Metabolic screening protocols: Glucose/Cholesterol correlate with risk escalation.

---

## 5. Key Metrics

| KPI | Value |
|-----|-------|
| Total Patients | 11397 |
| Avg Age | 48.4 |
| Avg Bmi | 27.1 |
| High Risk Count | 9958 |
| High Risk Rate | 87.4 |

---

## 6. Tools and Technologies

- **Python** (Pandas, NumPy, SciPy, Scikit-learn)
- **Matplotlib & Seaborn** (Data Visualization)
- **Visual Studio Code** (Development Environment)

---

## 7. Conclusion

Task 2 successfully transformed the cleaned dataset into actionable intelligence. Statistical tests confirmed significant relationships between patient vitals and health risk categories. The generated visualizations and insights provide a foundation for predictive modeling and clinical decision support in subsequent internship phases.

*Report generated automatically on 2026-06-08 08:25*
