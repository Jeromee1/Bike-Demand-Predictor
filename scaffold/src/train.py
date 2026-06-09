"""
Model training with MLflow experiment tracking.
================================================

CONTRACT — implement ``train_and_log`` so it trains several models, records each as an
MLflow run, selects a champion, and serialises it. Keep the signature.

Run as a module:  ``python -m src.train``
"""
from __future__ import annotations

from typing import Optional

import pandas as pd

from .data_prep import TARGET, add_features, load_and_clean

#: Where the champion model is written.
CHAMPION_PATH: str = "models/champion.pkl"


def train_and_log(df: pd.DataFrame, champion_path: str = CHAMPION_PATH) -> str:
    """Train 2-3 regressors, log them to MLflow, and save the champion.

    Must:
      - split features/target with NO leakage (``TARGET`` and leakage cols excluded from X),
      - train at least TWO models (e.g. LinearRegression, RandomForestRegressor,
        GradientBoostingRegressor),
      - for EACH model open an ``mlflow.start_run`` and log params + metrics
        (RMSE, MAE, R2) + the model artifact,
      - select the champion by the best held-out RMSE,
      - serialise the champion (e.g. ``joblib.dump``) to ``champion_path``.

    Args:
        df: Feature-engineered DataFrame (post :func:`add_features`).
        champion_path: Destination path for the serialised champion.

    Returns:
        The path the champion was written to.
    """
    # TODO: implement (sklearn models + metrics, mlflow.start_run / log_params / log_metrics
    #       / log_model, joblib.dump). Create the models/ directory if needed.
    raise NotImplementedError


def main(data_path: Optional[str] = None) -> str:
    """Entry point: clean -> feature-engineer -> train_and_log."""
    path = data_path or "data/hour.csv"
    df = add_features(load_and_clean(path))
    return train_and_log(df)


if __name__ == "__main__":
    print(f"Champion saved to: {main()}")
