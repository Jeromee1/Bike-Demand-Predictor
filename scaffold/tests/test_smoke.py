"""
Smoke tests — keep the CI workflow honest.
===========================================

CONTRACT — make these real assertions pass once your pipeline works. They are intentionally
minimal: at least prove (1) cleaning removes leakage columns, and (2) prediction returns a
non-negative float. Add more as you go.
"""
import pytest

from src.data_prep import LEAKAGE_COLUMNS, load_and_clean

SAMPLE = "data/bike_sharing_hourly_sample.csv"


def test_no_leakage_columns_after_cleaning():
    """Cleaned data must not contain any leakage columns."""
    df = load_and_clean(SAMPLE)
    for col in LEAKAGE_COLUMNS:
        assert col not in df.columns, f"leakage column {col!r} survived cleaning"


@pytest.mark.skip(reason="enable once train.py + predict.py are implemented")
def test_prediction_is_non_negative_float():
    """A prediction should be a sane, non-negative number."""
    from src.predict import load_model, predict

    model = load_model()
    value = predict(model, {"hr": 8, "weekday": 1, "weathersit": 1,
                            "temp": 0.5, "hum": 0.5, "windspeed": 0.2})
    assert isinstance(value, float)
    assert value >= 0
