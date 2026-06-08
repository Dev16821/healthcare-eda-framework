"""Business Intelligence: risk drivers, clinical recommendations, KPIs."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

from config import NUMERIC_COLS, TARGET


class InsightsEngine:
    def __init__(self, df: pd.DataFrame, eda_report: Dict, stats_report: Dict):
        self.df = df.copy()
        self.eda = eda_report
        self.stats = stats_report

    def generate(self) -> Dict[str, Any]:
        return {
            "executive_summary": self._executive_summary(),
            "key_metrics": self._key_metrics(),
            "risk_drivers": self._risk_drivers(),
            "demographic_insights": self._demographic_insights(),
            "clinical_recommendations": self._clinical_recommendations(),
            "data_quality_score": self._quality_score()
        }

    def _executive_summary(self) -> Dict[str, str]:
        total = len(self.df)
        if TARGET not in self.df.columns:
            return {"dataset_size": f"{total:,}"}

        dist = self.df[TARGET].value_counts(normalize=True)
        high_risk = sum([v for k, v in dist.items() if k in ["High", "Critical"]]) * 100

        predictors = self.eda.get("feature_importance", [])
        top = predictors[0]["feature"] if predictors else "multiple factors"

        return {
            "dataset_size": f"{total:,} patients",
            "high_risk_population": f"{high_risk:.1f}%",
            "top_predictor": top,
            "primary_finding": f"{top} is the strongest predictor of health risk."
        }

    def _key_metrics(self) -> Dict[str, Any]:
        m = {"total_patients": len(self.df)}
        if "age" in self.df.columns:
            m["avg_age"] = round(self.df["age"].mean(), 1)
        if "bmi" in self.df.columns:
            m["avg_bmi"] = round(self.df["bmi"].mean(), 1)
        if TARGET in self.df.columns:
            m["high_risk_count"] = int(self.df[TARGET].isin(["high"]).sum())
            m["high_risk_rate"] = round(m["high_risk_count"] / len(self.df) * 100, 1)
        return m

    def _risk_drivers(self) -> List[Dict]:
        if TARGET not in self.df.columns:
            return []

        high = self.df[self.df[TARGET].isin(["high"])]
        low = self.df[self.df[TARGET] == "low"]
        drivers = []

        for col in NUMERIC_COLS:
            if col not in self.df.columns:
                continue
            hm, lm = high[col].mean(), low[col].mean()
            if pd.isna(hm) or pd.isna(lm) or lm == 0:
                continue
            lift = ((hm - lm) / lm) * 100
            if abs(lift) > 10:
                drivers.append({
                    "factor": col,
                    "high_risk_mean": round(hm, 2),
                    "low_risk_mean": round(lm, 2),
                    "difference_pct": round(lift, 1),
                    "direction": "higher" if lift > 0 else "lower"
                })

        return sorted(drivers, key=lambda x: abs(x["difference_pct"]), reverse=True)

    def _demographic_insights(self) -> Dict[str, Any]:
        out = {}
        if "age" in self.df.columns and TARGET in self.df.columns:
            self.df["age_group"] = pd.cut(self.df["age"], bins=[0, 30, 45, 60, 100], labels=["<<30", "30-45", "45-60", "60+"])
            age_risk = pd.crosstab(self.df["age_group"], self.df[TARGET], normalize="index")
            high = age_risk[["high"]].sum(axis=1) if "high" in age_risk.columns else pd.Series()
            out["highest_risk_age_group"] = str(high.idxmax()) if not high.empty else "N/A"

        if "gender" in self.df.columns and TARGET in self.df.columns:
            chi = self.stats.get("chi2_gender_risk", {})
            out["gender_significance"] = "Significant" if chi.get("significant") else "Not Significant"
        return out

    def _clinical_recommendations(self) -> List[Dict]:
        recs = []
        drivers = self._risk_drivers()

        if drivers:
            top = drivers[0]
            recs.append({
                "priority": "High",
                "action": f"Monitor {top['factor']} closely",
                "rationale": f"High-risk patients show {top['difference_pct']}% {top['direction']} {top['factor']} vs low-risk."
            })

        if any(d["factor"] == "bmi" for d in drivers):
            recs.append({
                "priority": "High",
                "action": "Weight management programs",
                "rationale": "BMI significantly differentiates risk categories."
            })

        if any(d["factor"] in ["glucose_level", "cholesterol"] for d in drivers):
            recs.append({
                "priority": "Medium",
                "action": "Metabolic screening protocols",
                "rationale": "Glucose/Cholesterol correlate with risk escalation."
            })
        return recs

    def _quality_score(self) -> Dict[str, Any]:
        scores = {
            "completeness": round(100 - self.df.isnull().mean().mean() * 100, 1),
            "uniqueness": round(100 - (self.df.duplicated().sum() / len(self.df) * 100), 1),
        }
        scores["overall"] = round(sum(scores.values()) / len(scores), 1)
        scores["grade"] = "A" if scores["overall"] >= 90 else "B" if scores["overall"] >= 80 else "C"
        return scores