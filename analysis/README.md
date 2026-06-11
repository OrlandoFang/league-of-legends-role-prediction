# Role Prediction — Python reproduction

Python code that reproduces the analysis described in the project write-up
([`../README.md`](../README.md)): predicting the role a player played
(`top` / `jng` / `mid` / `bot` / `sup`) in a 2022 League of Legends competitive
match from their post-game statistics.

## Data

The dataset is the **2022 Oracle's Elixir** LoL esports match data
(<https://oracleselixir.com/tools/downloads>), released by Tim "Magic" Sevenhuysen.
It is not committed to the repo (≈98 MB); download it with the helper script.

## Setup & run

```bash
cd analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python download_data.py        # downloads data/2022_LoL_..._OraclesElixir.csv
python role_prediction.py      # runs the full pipeline
```

Outputs are written to `analysis/output/`:

- `conf_mat.png` — confusion matrix of the final model
- `accuracy_diff.html` — fairness-test permutation distribution (Plotly)

## What the pipeline does (`role_prediction.py`)

1. **Load & clean** — keep only individual-player rows for the five roles
   (drop aggregated `team` rows) and drop rows with missing modelled values.
2. **Baseline model** — `champion` (one-hot) + `total cs` →
   `DecisionTreeClassifier`.
3. **Final model** — adds `damageshare` & `damagetakenperminute` (standardized),
   and `minionkills`, `monsterkills`, `vspm` (binarized on each column's mean),
   then tunes `max_depth` / `min_samples_split` / `criterion` over 80
   combinations with `GridSearchCV`.
4. **Confusion matrix** of the tuned final model.
5. **Fairness analysis** — a 1000-rep permutation test comparing accuracy for
   damage-dealers (`damageshare > 0.2`) vs supports.

## Reproduction notes

The **final model** reproduces the write-up closely: GridSearchCV selects
`criterion=gini, max_depth=77` and reaches ~0.97 test accuracy, and the fairness
test reaches the same conclusion (supports are predicted slightly more
accurately than damage-dealers, p ≈ 0). The **baseline** accuracy comes out
higher than the write-up's 0.672 because Oracle's Elixir continuously updates
its published CSV — the current snapshot has more rows and is more separable.
The modelling methodology is identical to the write-up; only the data snapshot
and (unspecified) random seed differ.
