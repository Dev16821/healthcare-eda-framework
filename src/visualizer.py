"""Generates and saves all EDA figures."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List

from config import (
    NUMERIC_COLS, TARGET, RISK_ORDER, FIGURES_DIR, FIG_DPI, FIG_STYLE, COLOR_MAP
)

plt.style.use(FIG_STYLE)
sns.set_palette(COLOR_MAP)


class Visualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def generate_all(self) -> List[str]:
        paths = []
        paths.append(self._plot_distributions())
        paths.append(self._plot_boxplots_by_risk())
        paths.append(self._plot_correlation_heatmap())
        paths.append(self._plot_violin_by_risk())
        paths.append(self._plot_risk_distribution())
        paths.append(self._plot_gender_risk_heatmap())
        paths.append(self._plot_smoking_risk())
        paths.append(self._plot_pairplot())
        paths.append(self._plot_bmi_glucose_scatter())
        paths.append(self._plot_radar_chart())
        return [p for p in paths if p]

    def _save(self, fig, name: str) -> str:
        path = FIGURES_DIR / name
        fig.savefig(path, dpi=FIG_DPI, bbox_inches="tight")
        plt.close(fig)
        return str(path)

    def _plot_distributions(self) -> str:
        cols = [c for c in NUMERIC_COLS if c in self.df.columns]
        n = len(cols)
        fig, axes = plt.subplots((n + 2) // 3, 3, figsize=(16, 4 * ((n + 2) // 3)))
        axes = axes.flatten() if n > 1 else [axes]

        for idx, col in enumerate(cols):
            ax = axes[idx]
            sns.histplot(self.df[col], kde=True, ax=ax, color="steelblue")
            ax.axvline(self.df[col].mean(), color="red", ls="--", label=f"Mean: {self.df[col].mean():.1f}")
            ax.axvline(self.df[col].median(), color="green", ls="--", label=f"Median: {self.df[col].median():.1f}")
            ax.set_title(f"Distribution: {col}")
            ax.legend()

        for idx in range(n, len(axes)):
            fig.delaxes(axes[idx])

        fig.suptitle("Univariate Distributions", fontsize=16, y=1.02)
        return self._save(fig, "01_distributions.png")

    def _plot_boxplots_by_risk(self) -> str:
        cols = [c for c in NUMERIC_COLS if c in self.df.columns]
        n = len(cols)
        fig, axes = plt.subplots((n + 2) // 3, 3, figsize=(16, 4 * ((n + 2) // 3)))
        axes = axes.flatten() if n > 1 else [axes]

        order = [r for r in RISK_ORDER if r in self.df[TARGET].unique()]

        for idx, col in enumerate(cols):
            ax = axes[idx]
            sns.boxplot(data=self.df, x=TARGET, y=col, order=order, hue=TARGET, ax=ax, palette=COLOR_MAP, legend=False)
            ax.set_title(f"{col} by Risk")

        for idx in range(n, len(axes)):
            fig.delaxes(axes[idx])

        fig.suptitle("Feature Distributions by Health Risk", fontsize=16, y=1.02)
        return self._save(fig, "02_boxplots_by_risk.png")

    def _plot_correlation_heatmap(self) -> str:
        fig, ax = plt.subplots(figsize=(10, 8))
        corr = self.df[NUMERIC_COLS].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
        ax.set_title("Correlation Matrix")
        return self._save(fig, "03_correlation_heatmap.png")

    def _plot_violin_by_risk(self) -> str:
        key = [c for c in ["bmi", "cholesterol", "glucose_level"] if c in self.df.columns]
        if not key:
            return ""
        fig, axes = plt.subplots(1, len(key), figsize=(6 * len(key), 5))
        axes = [axes] if len(key) == 1 else axes.flatten()
        order = [r for r in RISK_ORDER if r in self.df[TARGET].unique()]

        for idx, col in enumerate(key):
            sns.violinplot(data=self.df, x=TARGET, y=col, order=order, hue=TARGET, ax=axes[idx], palette="Spectral", legend=False)
            axes[idx].set_title(f"{col} Density by Risk")

        fig.suptitle("Density Analysis by Risk Category", fontsize=14)
        return self._save(fig, "04_violin_plots.png")

    def _plot_risk_distribution(self) -> str:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        risk_counts = self.df[TARGET].value_counts()
        colors = sns.color_palette(COLOR_MAP, len(risk_counts))

        ax1.pie(risk_counts, labels=risk_counts.index, autopct="%1.1f%%", colors=colors, startangle=90)
        ax1.set_title("Risk Proportion")

        order = [r for r in RISK_ORDER if r in risk_counts.index]
        sns.countplot(data=self.df, x=TARGET, hue=TARGET, order=order, palette=COLOR_MAP, ax=ax2, legend=False)
        ax2.set_title("Risk Counts")
        for container in ax2.containers:
            ax2.bar_label(container, fmt="%d")

        fig.suptitle("Health Risk Distribution", fontsize=14)
        return self._save(fig, "05_risk_distribution.png")

    def _plot_gender_risk_heatmap(self) -> str:
        if "Gender" not in self.df.columns:
            return ""
        fig, ax = plt.subplots(figsize=(10, 6))
        ct = pd.crosstab(self.df[TARGET], self.df["Gender"], normalize="index") * 100
        sns.heatmap(ct, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax)
        ax.set_title("Gender % Within Each Risk Category")
        return self._save(fig, "06_gender_risk_heatmap.png")

    def _plot_smoking_risk(self) -> str:
        if "smoking_status" not in self.df.columns:
            return ""
        fig, ax = plt.subplots(figsize=(12, 6))
        ct = pd.crosstab(self.df[TARGET], self.df["smoking_status"], normalize="index")
        ct.plot(kind="bar", stacked=True, colormap="Set2", ax=ax)
        ax.set_title("Smoking Status by Risk Category")
        ax.set_xlabel("Risk Category")
        ax.legend(title="Smoking", bbox_to_anchor=(1.05, 1))
        plt.xticks(rotation=0)
        return self._save(fig, "07_smoking_risk.png")

    def _plot_pairplot(self) -> str:
        plot_cols = [c for c in NUMERIC_COLS[:4] if c in self.df.columns]
        if len(plot_cols) < 2:
            return ""
        plot_df = self.df.sample(min(2000, len(self.df)), random_state=42)
        g = sns.pairplot(plot_df, vars=plot_cols, hue=TARGET, palette=COLOR_MAP, diag_kind="kde", plot_kws={"alpha": 0.6, "s": 30})
        g.fig.suptitle("Pairwise Relationships", y=1.02, fontsize=14)
        path = FIGURES_DIR / "08_pairplot.png"
        g.savefig(path, dpi=FIG_DPI)
        plt.close()
        return str(path)

    def _plot_bmi_glucose_scatter(self) -> str:
        if "bmi" not in self.df.columns or "glucose_level" not in self.df.columns:
            return ""
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(data=self.df, x="bmi", y="glucose_level", hue=TARGET, palette=COLOR_MAP, alpha=0.6, ax=ax)
        ax.set_title("BMI vs Glucose by Risk")
        return self._save(fig, "09_bmi_glucose.png")

    def _plot_radar_chart(self) -> str:
        from math import pi
        categories = [c for c in ["bmi", "cholesterol", "glucose_level", "blood_pressure"] if c in self.df.columns]
        if not categories or TARGET not in self.df.columns:
            return ""

        means = self.df.groupby(TARGET)[categories].mean()
        normalized = (means - means.min()) / (means.max() - means.min())
        normalized = normalized.fillna(0)

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(normalized)))

        for idx, (risk, row) in enumerate(normalized.iterrows()):
            vals = row.values.tolist() + row.values.tolist()[:1]
            ax.plot(angles, vals, "o-", linewidth=2, label=risk, color=colors[idx])
            ax.fill(angles, vals, alpha=0.15, color=colors[idx])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
        plt.title("Risk Profile Comparison (Normalized)", y=1.08, fontsize=14)
        return self._save(fig, "10_radar_chart.png")