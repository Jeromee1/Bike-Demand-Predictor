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
from pathlib import Path

import streamlit as st
import plotly.express as px
import pandas as pd

DATA_PATH = "data/bike_sharing_hourly_sample.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    from src.data_prep import add_features, load_and_clean

    return add_features(load_and_clean(path))


def main() -> None:
    st.set_page_config(page_title="Bike Demand Forecaster", page_icon="🚲", layout="wide")
    st.title("🚲 Bike Demand Forecaster")

    # ── Part 1: Analytics Dashboard ──────────────────────────────────────
    st.header("📊 Demand Analytics")

    try:
        df = load_data(DATA_PATH)
    except Exception as e:
        st.error(f"Could not load data: {e}")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        hourly = df.groupby("hr")["cnt"].mean().reset_index()
        fig1 = px.bar(
            hourly, x="hr", y="cnt",
            labels={"hr": "Hour of day", "cnt": "Avg demand"},
            title="Average hourly demand",
            color_discrete_sequence=['#7C3AED'],
        )
        fig1.update_layout(height=350)
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Demand rises during commute hours (8am, 5-6pm) and drops overnight.")

    with col2:
        fig2 = px.scatter(
            df, x="temp", y="cnt", color="weathersit",
            labels={"temp": "Normalized temperature", "cnt": "Hourly demand",
                    "weathersit": "Weather situation"},
            title="Demand vs temperature by weather",
            color_discrete_sequence=['#7C3AED'],
        )
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Milder temperatures and clear weather tend to increase bike rentals.")

    with st.expander("📋 Demand by weather situation", expanded=False):
        fig3 = px.box(
            df, x="weathersit", y="cnt",
            labels={"weathersit": "Weather situation", "cnt": "Hourly demand"},
            color_discrete_sequence=['#7C3AED'],
        )
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Weather 1 (clear) shows the highest median demand; heavy weather (4) dampens it.")

    # ── Part 2: Prediction Form ─────────────────────────────────────────
    st.header("🔮 Predict Hourly Demand")

    try:
        from src.predict import load_model, predict

        model = load_model(Path(__file__).parent / "models" / "champion.pkl")
    except Exception as e:
        st.error(f"Could not load champion model: {e}")
        st.stop()

    with st.form("predict_form"):
        st.subheader("Time & date")
        tcol1, tcol2, tcol3, tcol4 = st.columns(4)
        with tcol1:
            hr = st.slider("Hour", 0, 23, 8)
        with tcol2:
            season = st.selectbox("Season", [1, 2, 3, 4],
                                  format_func=lambda x: {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}[x])
        with tcol3:
            mnth = st.selectbox("Month", list(range(1, 13)),
                                format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][x - 1])
        with tcol4:
            weekday = st.selectbox("Weekday", list(range(7)),
                                   format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])

        dcol1, dcol2 = st.columns(2)
        with dcol1:
            holiday = st.checkbox("Holiday")
        with dcol2:
            workingday = st.checkbox("Working day", value=True)

        st.subheader("Weather conditions")
        wcol1, wcol2, wcol3, wcol4, wcol5 = st.columns(5)
        with wcol1:
            weathersit = st.selectbox("Weather", [1, 2, 3, 4],
                                      format_func=lambda x: {1: "Clear", 2: "Mist/Cloudy",
                                                             3: "Light precip", 4: "Heavy precip"}[x])
        with wcol2:
            temp = st.slider("Temperature (norm.)", 0.0, 1.0, 0.24, 0.01)
        with wcol3:
            atemp = st.slider("Feeling temp (norm.)", 0.0, 1.0, 0.22, 0.01)
        with wcol4:
            hum = st.slider("Humidity (norm.)", 0.0, 1.0, 0.58, 0.01)
        with wcol5:
            windspeed = st.slider("Wind speed (norm.)", 0.0, 1.0, 0.23, 0.01)

        submitted = st.form_submit_button("Predict demand", type="primary")

    if submitted:
        inputs = {
            "season": int(season),
            "yr": 0,
            "mnth": int(mnth),
            "hr": int(hr),
            "holiday": int(holiday),
            "weekday": int(weekday),
            "workingday": int(workingday),
            "weathersit": int(weathersit),
            "temp": temp,
            "atemp": atemp,
            "hum": hum,
            "windspeed": windspeed,
        }
        with st.spinner("Predicting..."):
            try:
                pred = predict(model, inputs)
                st.metric("Predicted hourly demand", f"{pred:.0f} rentals",
                          help="Non-negative forecast of total bike rentals for this hour")
            except Exception as e:
                st.error(f"Prediction failed: {e}")


if __name__ == "__main__":
    main()
