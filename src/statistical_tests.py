"""Hypothesis testing: ANOVA, Chi-square, t-tests."""

import pandas as pd
from scipy import stats
from typing import Dict, Any


class StatisticalTester:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def run_all(self) -> Dict[str, Any]:
        results = {}
        results["anova"] = self._anova_numeric_by_risk()
        results["chi2_gender_risk"] = self._chi2_gender_risk()
        results["chi2_smoking_risk"] = self._chi2_smoking_risk()
        return results

    def _anova_numeric_by_risk(self) -> Dict[str, Any]:
        from config import NUMERIC_COLS, TARGET
        if TARGET not in self.df.columns:
            return {}

        groups = [g[NUMERIC_COLS].values for _, g in self.df.groupby(TARGET)]
        anova = {}

        for idx, col in enumerate(NUMERIC_COLS):
            cols = [g[:, idx] for g in groups if len(g) > 1]
            if len(cols) >= 2:
                f, p = stats.f_oneway(*cols)
                anova[col] = {"f": round(f, 3), "p": round(p, 5), "significant": bool(p < 0.05)}
        return anova

    def _chi2_gender_risk(self) -> Dict[str, Any]:
        from config import TARGET
        if "gender" not in self.df.columns or TARGET not in self.df.columns:
            return {}
        ct = pd.crosstab(self.df["gender"], self.df[TARGET])
        chi2, p, dof, expected = stats.chi2_contingency(ct)
        return {"chi2": round(chi2, 3), "p": round(p, 5), "significant": bool(p < 0.05), "dof": dof}

    def _chi2_smoking_risk(self) -> Dict[str, Any]:
        from config import TARGET
        if "smoking_status" not in self.df.columns or TARGET not in self.df.columns:
            return {}
        ct = pd.crosstab(self.df["smoking_status"], self.df[TARGET])
        chi2, p, dof, expected = stats.chi2_contingency(ct)
        return {"chi2": round(chi2, 3), "p": round(p, 5), "significant": bool(p < 0.05), "dof": dof}