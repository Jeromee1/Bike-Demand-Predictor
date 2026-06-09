"""
Inference: load the champion model and predict hourly demand.
=============================================================

CONTRACT — implement ``load_model`` and ``predict`` so the Streamlit app can serve
predictions. Keep the signatures.
"""
from __future__ import annotations

from typing import Any, Dict

from .train import CHAMPION_PATH


def load_model(path: str = CHAMPION_PATH) -> Any:
    """Load and return the serialised champion model.

    Args:
        path: Path to the serialised champion (default :data:`CHAMPION_PATH`).

    Returns:
        The loaded model object.
    """
    # TODO: implement (e.g. joblib.load). Consider caching with functools.lru_cache.
    raise NotImplementedError


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
    # TODO: implement (build a 1-row frame matching training features, model.predict,
    #       clamp to >= 0)
    raise NotImplementedError
