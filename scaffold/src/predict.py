"""
Inference: load the champion model and predict hourly demand.
=============================================================

CONTRACT — implement ``load_model`` and ``predict`` so the Streamlit app can serve
predictions. Keep the signatures.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd


@lru_cache(maxsize=1)
def load_model(path: str = str(Path(__file__).parent.parent / "models" / "champion.pkl")) -> Any:
    """Load and return the serialised champion model.

    Args:
        path: Path to the serialised champion (default :data:`CHAMPION_PATH`).

    Returns:
        The loaded model object.
    """
    import joblib

    return joblib.load(path)


def predict(model: Any, inputs: Dict[str, Any]) -> float:
    """Return predicted demand for a single hour.

    ``inputs`` is a dict of raw user choices from the app (e.g. hour, weekday,
    weathersit, temp, hum, windspeed). This function must transform them into the SAME
    feature shape used at training time, then return a single non-negative number.

    Args:
        model: A loaded champion model.
        inputs: User-supplied feature values.

    Returns:
        Predicted total rentals (``cnt``) for the hour, as a non-negative float.
    """
    df = pd.DataFrame([inputs])

    if "hr_sin" not in df.columns or "hr_cos" not in df.columns:
        df["hr_sin"] = np.sin(2 * np.pi * df["hr"] / 24)
        df["hr_cos"] = np.cos(2 * np.pi * df["hr"] / 24)
    if "mnth_sin" not in df.columns or "mnth_cos" not in df.columns:
        df["mnth_sin"] = np.sin(2 * np.pi * df["mnth"] / 12)
        df["mnth_cos"] = np.cos(2 * np.pi * df["mnth"] / 12)
    if "dayofweek" not in df.columns and "weekday" in df.columns:
        df["dayofweek"] = df["weekday"]
    if "is_weekend" not in df.columns and "dayofweek" in df.columns:
        df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    feature_cols = (
        model.feature_names_in_.tolist()
        if hasattr(model, "feature_names_in_")
        else [c for c in df.columns if c != "dteday"]
    )
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0

    pred = model.predict(df[feature_cols])[0]
    return max(float(pred), 0.0)
