"""
Data preparation for bike-share demand forecasting.
=====================================================

CONTRACT — implement these so the rest of the pipeline works. Keep the signatures;
your AI agent fills the bodies.

This module is responsible for turning the raw hourly CSV into a clean, leakage-free,
feature-rich DataFrame ready for modelling.
"""
from __future__ import annotations

from typing import List

import pandas as pd

#: Columns that leak the target. `casual + registered == cnt`, and both are only known
#: AFTER the hour ends — so they must be dropped before training. `instant` is just a row id.
#: Leaving these in produces a fake R² ~= 1.0. See data/README.md.
LEAKAGE_COLUMNS: List[str] = ["casual", "registered", "instant"]

#: The prediction target.
TARGET: str = "cnt"


def load_and_clean(path: str) -> pd.DataFrame:
    """Load the raw hourly CSV and return a clean DataFrame.

    Must:
      - read the CSV at ``path``,
      - parse ``dteday`` to datetime,
      - drop ``LEAKAGE_COLUMNS``,
      - impute missing ``hum`` / ``windspeed`` (do NOT drop those rows wholesale),
      - remove duplicate rows,
      - return a DataFrame that still contains ``TARGET``.

    Args:
        path: Path to ``hour.csv`` (or the bundled sample CSV).

    Returns:
        Cleaned DataFrame with no leakage columns.
    """
    df = pd.read_csv(path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    df = df.drop(columns=LEAKAGE_COLUMNS)
    for col in ["hum", "windspeed"]:
        df[col] = df[col].fillna(df[col].median())
    df = df.drop_duplicates()
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer datetime and cyclical features from a cleaned DataFrame.

    Suggested features:
      - ``dayofweek`` / ``is_weekend`` from ``dteday``,
      - cyclical encodings of ``hr`` and ``mnth`` (sin/cos),
      - keep weather features (``temp``, ``atemp``, ``hum``, ``windspeed``, ``weathersit``).

    Args:
        df: Output of :func:`load_and_clean`.

    Returns:
        DataFrame with engineered feature columns added.
    """
    import numpy as np

    df = df.copy()
    df["dayofweek"] = df["dteday"].dt.dayofweek
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
    df["hr_sin"] = np.sin(2 * np.pi * df["hr"] / 24)
    df["hr_cos"] = np.cos(2 * np.pi * df["hr"] / 24)
    df["mnth_sin"] = np.sin(2 * np.pi * df["mnth"] / 12)
    df["mnth_cos"] = np.cos(2 * np.pi * df["mnth"] / 12)
    return df