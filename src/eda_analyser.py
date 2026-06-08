"""Core EDA: statistics, correlations, distributions."""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any
import json

from config import NUMERIC_COLS, CATEGORICAL_COLS, TARGET


class EDAAnalyser:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.report: Dict[str, Any] = {}

    def run(self) -> Dict[str, Any]:
        self.report["shape"] = self.df.shape
        self.report["dtypes"] = self.df.dtypes.astype(str).to_dict()
        self.report["missing"] = self.df.isnull().sum().to_dict()
        self.report["descriptive"] = self._descriptive_stats()
        self.report["correlations"] = self._correlation_matrix()
        self.report["feature_importance"] = self._feature_importance()
        self.report["distributions"] = self._distribution_tests()
        return self.report

    def _descriptive_stats(self) -> Dict[str, Any]:
        desc = self.df[NUMERIC_COLS].describe().to_dict()
        advanced = {}
        for col in NUMERIC_COLS:
            if col in self.df.columns:
                advanced[col] = {
                    "skewness": round(self.df[col].skew(), 3),
                    "kurtosis": round(self.df[col].kurtosis(), 3),
                    "variance": round(self.df[col].var(), 3),
                    "cv": round(self.df[col].std() / self.df[col].mean(), 3) if self.df[col].mean() != 0 else 0
                }
        return {"basic": desc, "advanced": advanced}

    def _correlation_matrix(self) -> Dict[str, Any]:
        corr = self.df[NUMERIC_COLS].corr().round(3)
        strong = []
        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):
                v = corr.iloc[i, j]
                if abs(v) >= 0.5:
                    strong.append({
                        "feature_1": corr.columns[i],
                        "feature_2": corr.columns[j],
                        "correlation": float(v),
                        "strength": "Strong Positive" if v > 0 else "Strong Negative"
                    })
        return {"matrix": corr.to_dict(), "strong_pairs": strong}

    def _feature_importance(self) -> list:
        """ANOVA F-score to find which numeric feature best predicts risk."""
        from sklearn.feature_selection import f_classif
        from sklearn.preprocessing import LabelEncoder

        if TARGET not in self.df.columns:
            return []

        le = LabelEncoder()
        y = le.fit_transform(self.df[TARGET].astype(str))
        X = self.df[NUMERIC_COLS].fillna(self.df[NUMERIC_COLS].median())

        f_scores, p_values = f_classif(X, y)
        results = []
        for col, f, p in zip(NUMERIC_COLS, f_scores, p_values):
            results.append({
                "feature": col,
                "f_score": round(f, 2),
                "p_value": round(p, 5),
                "significant": bool(p < 0.05)
            })
        return sorted(results, key=lambda x: x["f_score"], reverse=True)

    def _distribution_tests(self) -> Dict[str, Any]:
        out = {}
        for col in NUMERIC_COLS:
            if col not in self.df.columns:
                continue
            data = self.df[col].dropna()
            if len(data) < 3:
                continue
            sample = data.sample(min(5000, len(data)), random_state=42)
            stat, p = stats.shapiro(sample)
            out[col] = {
                "shapiro_p": round(p, 5),
                "normal": bool(p > 0.05),
                "skew": round(data.skew(), 3)
            }
        return out

    def save_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.report, f, indent=4, default=str)