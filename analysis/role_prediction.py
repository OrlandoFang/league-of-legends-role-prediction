"""Reproduce the League of Legends role-prediction project.

Predicts the role a player played in a competitive match (top / jng / mid / bot / sup)
from their post-game statistics, following the methodology described in the project
write-up (README.md):

* Baseline model:  champion (one-hot) + total cs  ->  DecisionTreeClassifier
* Final model:     baseline features
                   + damageshare           (standardized)
                   + damagetakenperminute  (standardized)
                   + minionkills           (binarized on its mean)
                   + monsterkills          (binarized on its mean)
                   + vspm                  (binarized on its mean)
                   with hyper-parameters tuned via GridSearchCV.
* Confusion matrix of the final model.
* Fairness analysis: a permutation test comparing accuracy for damage-dealers
  (damageshare > 0.2) versus supports (damageshare <= 0.2).

Run:
    python download_data.py        # fetch the dataset (once)
    python role_prediction.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless rendering
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
CSV_PATH = HERE / "data" / "2022_LoL_esports_match_data_from_OraclesElixir.csv"
OUTPUT_DIR = HERE / "output"

ROLES = ["top", "jng", "mid", "bot", "sup"]
RANDOM_STATE = 42

# Features used by each model.
BASELINE_FEATURES = ["champion", "total cs"]
FINAL_NUMERIC_STD = ["damageshare", "damagetakenperminute"]
FINAL_BINARIZE = ["minionkills", "monsterkills", "vspm"]
FINAL_FEATURES = BASELINE_FEATURES + FINAL_NUMERIC_STD + FINAL_BINARIZE
TARGET = "position"


class MeanBinarizer(BaseEstimator, TransformerMixin):
    """Binarize each column using the column mean learned on the training data.

    Mirrors the write-up's "binarize with a threshold on the mean" step while
    avoiding train/test leakage (the threshold is learned in ``fit``).
    """

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=float)
        self.thresholds_ = np.nanmean(X, axis=0)
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=float)
        return (X > self.thresholds_).astype(float)


def load_player_data() -> pd.DataFrame:
    """Load the dataset and keep only individual-player rows for the 5 roles."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"{CSV_PATH} not found. Run `python download_data.py` first."
        )
    df = pd.read_csv(CSV_PATH, low_memory=False)
    # Drop the aggregated "team" rows; keep only the five player positions.
    players = df[df[TARGET].isin(ROLES)].copy()
    # Keep only the columns we model on, and drop rows with missing values there.
    players = players[FINAL_FEATURES + [TARGET]].dropna()
    return players


def build_baseline_pipeline() -> Pipeline:
    pre = ColumnTransformer(
        transformers=[
            ("champion", OneHotEncoder(handle_unknown="ignore"), ["champion"]),
        ],
        remainder="passthrough",  # leave `total cs` as-is
    )
    return Pipeline([
        ("pre", pre),
        ("tree", DecisionTreeClassifier(random_state=RANDOM_STATE)),
    ])


def build_final_pipeline() -> Pipeline:
    pre = ColumnTransformer(
        transformers=[
            ("champion", OneHotEncoder(handle_unknown="ignore"), ["champion"]),
            ("standardize", StandardScaler(), FINAL_NUMERIC_STD),
            ("binarize", MeanBinarizer(), FINAL_BINARIZE),
        ],
        remainder="passthrough",  # leave `total cs` as-is
    )
    return Pipeline([
        ("pre", pre),
        ("tree", DecisionTreeClassifier(random_state=RANDOM_STATE)),
    ])


def run_baseline(X_train, X_test, y_train, y_test) -> None:
    print("\n" + "=" * 70)
    print("BASELINE MODEL  (champion + total cs)")
    print("=" * 70)
    pipe = build_baseline_pipeline()
    pipe.fit(X_train[BASELINE_FEATURES], y_train)
    train_acc = pipe.score(X_train[BASELINE_FEATURES], y_train)
    test_acc = pipe.score(X_test[BASELINE_FEATURES], y_test)
    print(f"Training accuracy: {train_acc:.3f}")
    print(f"Testing accuracy:  {test_acc:.3f}")


def run_final(X_train, X_test, y_train, y_test):
    print("\n" + "=" * 70)
    print("FINAL MODEL  (+ damageshare, damagetakenperminute, minionkills,")
    print("              monsterkills, vspm  with GridSearchCV)")
    print("=" * 70)
    pipe = build_final_pipeline()

    # 8 x 5 x 2 = 80 hyper-parameter combinations (matches the write-up).
    param_grid = {
        "tree__max_depth": [2, 5, 10, 20, 40, 60, 77, 100],
        "tree__min_samples_split": [2, 10, 50, 100, 200],
        "tree__criterion": ["gini", "entropy"],
    }
    search = GridSearchCV(pipe, param_grid, scoring="accuracy", cv=5, n_jobs=-1)
    search.fit(X_train[FINAL_FEATURES], y_train)

    print(f"Best hyper-parameters: {search.best_params_}")
    best = search.best_estimator_
    train_acc = best.score(X_train[FINAL_FEATURES], y_train)
    test_acc = best.score(X_test[FINAL_FEATURES], y_test)
    print(f"Training accuracy: {train_acc:.3f}")
    print(f"Testing accuracy:  {test_acc:.3f}")
    return best


def plot_confusion_matrix(model, X_test, y_test) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    y_pred = model.predict(X_test[FINAL_FEATURES])
    cm = confusion_matrix(y_test, y_pred, labels=ROLES)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=ROLES)
    fig, ax = plt.subplots(figsize=(7, 6))
    disp.plot(ax=ax, cmap="viridis", colorbar=True)
    ax.set_title("Final Model — Confusion Matrix")
    out = OUTPUT_DIR / "conf_mat.png"
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"\nSaved confusion matrix -> {out}")
    return out


def fairness_analysis(model, X_test, y_test, n_reps: int = 1000) -> Path:
    """Permutation test: is accuracy the same for damage-dealers vs supports?

    Group split on damageshare > 0.2 (each of 5 players is expected to deal 0.2
    of team damage). Test statistic = accuracy(support) - accuracy(damage-dealer).
    """
    print("\n" + "=" * 70)
    print("FAIRNESS ANALYSIS  (damage-dealer vs support, permutation test)")
    print("=" * 70)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    y_pred = model.predict(X_test[FINAL_FEATURES])
    correct = (np.asarray(y_pred) == np.asarray(y_test)).astype(float)
    is_support = (X_test["damageshare"].to_numpy() <= 0.2)

    def diff(corr, supp):
        return corr[supp].mean() - corr[~supp].mean()

    observed = diff(correct, is_support)
    print(f"Accuracy (support):       {correct[is_support].mean():.4f}")
    print(f"Accuracy (damage-dealer): {correct[~is_support].mean():.4f}")
    print(f"Observed difference (support - damage-dealer): {observed:.4f}")

    rng = np.random.default_rng(RANDOM_STATE)
    perm = np.empty(n_reps)
    for i in range(n_reps):
        shuffled = rng.permutation(is_support)
        perm[i] = diff(correct, shuffled)
    p_value = float(np.mean(perm >= observed))
    print(f"Permutation p-value ({n_reps} reps): {p_value:.4f}")

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=perm, nbinsx=40, name="Permuted differences"))
    fig.add_vline(
        x=observed, line_color="red", line_width=3,
        annotation_text=f"observed = {observed:.4f}", annotation_position="top",
    )
    fig.update_layout(
        title=f"Difference in Accuracy (Support - Damage-dealer)  |  p-value = {p_value:.3f}",
        xaxis_title="Difference in accuracy",
        yaxis_title="Count",
        bargap=0.05,
    )
    out = OUTPUT_DIR / "accuracy_diff.html"
    fig.write_html(str(out))
    print(f"Saved fairness chart -> {out}")
    return out


def main() -> None:
    print("Loading data...")
    data = load_player_data()
    print(f"Player rows used: {len(data):,}")
    print("Role distribution:")
    print(data[TARGET].value_counts().to_string())

    X = data[FINAL_FEATURES]
    y = data[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )

    run_baseline(X_train, X_test, y_train, y_test)
    best = run_final(X_train, X_test, y_train, y_test)
    plot_confusion_matrix(best, X_test, y_test)
    fairness_analysis(best, X_test, y_test)
    print("\nDone.")


if __name__ == "__main__":
    main()
