"""
Streamlit app — Bike Demand Forecaster.
========================================

CONTRACT — build a single-page Streamlit app with TWO parts:

  1. Analytics dashboard: load the cleaned data and show >= 2 EDA visualisations
     (e.g. average demand by hour, demand vs. temperature, demand by weather situation).
  2. Prediction form: collect weather + time inputs from the user, call
     ``src.predict.predict`` with the loaded champion, and display the predicted demand.

This is the file Hugging Face Spaces runs (see README front-matter: ``app_file: app.py``).
Keep it runnable with ``streamlit run app.py``.
"""
import streamlit as st

# from src.data_prep import add_features, load_and_clean
# from src.predict import load_model, predict


def main() -> None:
    st.set_page_config(page_title="Bike Demand Forecaster", page_icon="🚲", layout="wide")
    st.title("🚲 Bike Demand Forecaster")

    # TODO: Part 1 — Analytics
    #   df = add_features(load_and_clean("data/hour.csv"))
    #   ...render >= 2 charts (st.bar_chart / st.plotly_chart / etc.)

    # TODO: Part 2 — Prediction form
    #   model = load_model()
    #   with st.form("predict"):
    #       collect hour, weekday, weathersit, temp, hum, windspeed ...
    #       on submit: st.metric("Predicted rentals", round(predict(model, inputs)))

    st.info("Scaffold stub — implement the dashboard and prediction form (see app.py docstring).")


if __name__ == "__main__":
    main()
