"""
weather_monitor.py
Short-term Rainfall Forecasting & Alert System

Run:
    streamlit run weather_monitor.py

Before running, install:
    pip install streamlit requests pandas

OpenWeatherMap API key:
    1) Put it in the sidebar when the app opens, OR
    2) Set environment variable: OPENWEATHER_API_KEY="your_key"
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import pandas as pd
import requests
import streamlit as st

API_URL = "https://api.openweathermap.org/data/2.5/weather"
ALERT_LOG_FILE = Path("alert_log.txt")


def fetch_weather(city: str, api_key: str) -> Dict[str, Any]:
    """Fetch current weather data from OpenWeatherMap for a city."""
    if not api_key:
        raise ValueError("Missing OpenWeatherMap API key.")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        # Give a clear message for common API problems.
        status_code = getattr(error.response, "status_code", "unknown")
        if status_code == 401:
            raise RuntimeError("API key is invalid or not active yet.") from error
        if status_code == 404:
            raise RuntimeError(f"City not found: {city}") from error
        raise RuntimeError(f"API HTTP error: {status_code}") from error
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Network/API request failed: {error}") from error


def extract_rainfall_mm_per_hour(data: Dict[str, Any]) -> float:
    """
    Extract rainfall intensity in mm/h.

    OpenWeatherMap current weather usually returns rain data as:
        rain: {"1h": value}
    If only 3-hour rain exists, approximate hourly intensity as value / 3.
    If there is no rain field, assume 0 mm/h.
    """
    rain = data.get("rain", {}) or {}

    if "1h" in rain:
        return float(rain["1h"])
    if "3h" in rain:
        return float(rain["3h"]) / 3.0
    return 0.0


def check_alert(rainfall: float) -> Tuple[str, str, str]:
    """Return alert level, status text, and display color."""
    if rainfall < 10:
        return "Green", "Normal", "green"
    if rainfall < 20:
        return "Yellow", "Moderate", "orange"
    return "Red", "Heavy Rainfall - ALERT", "red"


def log_alert(city: str, rainfall: float, level: str) -> None:
    """Log red rainfall alerts to a text file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{timestamp} | City: {city} | Rainfall: {rainfall:.2f} mm/h | Level: {level}\n"
    with ALERT_LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(message)


def add_to_history(city: str, rainfall: float, level: str) -> None:
    """Save measurements in Streamlit session state for the chart."""
    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "city": city,
            "rainfall_mm_h": rainfall,
            "alert_level": level,
        }
    )

    # Keep the chart simple and not too long.
    st.session_state.history = st.session_state.history[-30:]


def show_dashboard(city: str, rainfall: float, level: str, status: str, color: str, data_source: str) -> None:
    """Build the Streamlit dashboard UI."""
    st.title(f"Rainfall Monitor - {city}")
    st.caption(f"Data source: {data_source}. The page auto-refreshes every 5 minutes.")

    # Auto refresh using browser reload. No extra Streamlit package is needed.
    st.components.v1.html(
        """
        <script>
        setTimeout(function(){ window.parent.location.reload(); }, 300000);
        </script>
        """,
        height=0,
    )

    metric_col, alert_col = st.columns(2)

    with metric_col:
        st.metric("Current Rainfall", f"{rainfall:.2f} mm/h")

    with alert_col:
        st.markdown(
            f"""
            <div style='padding: 18px; border-radius: 12px; border: 2px solid {color};'>
                <h3 style='color:{color}; margin:0;'>Alert Status: {level}</h3>
                <p style='font-size:20px; margin:8px 0 0 0;'>{status}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if level == "Red":
        st.error("Warning: Heavy rainfall threshold reached. Urban flood risk may increase.")

    st.subheader("Historical Rainfall Data")
    add_to_history(city, rainfall, level)
    history_df = pd.DataFrame(st.session_state.history)

    if not history_df.empty:
        st.line_chart(history_df.set_index("time")["rainfall_mm_h"])
        with st.expander("Show history table"):
            st.dataframe(history_df, use_container_width=True)

    st.subheader("Threshold Rules")
    st.write("Green: rainfall < 10 mm/h = Normal")
    st.write("Yellow: 10 ≤ rainfall < 20 mm/h = Moderate")
    st.write("Red: rainfall ≥ 20 mm/h = Heavy Rainfall - ALERT")


def main() -> None:
    st.set_page_config(page_title="Rainfall Monitor", page_icon="🌧️", layout="wide")

    st.sidebar.header("Settings")
    city = st.sidebar.text_input("City", value="Beijing")
    api_key = st.sidebar.text_input(
        "OpenWeatherMap API Key",
        value=os.getenv("OPENWEATHER_API_KEY", ""),
        type="password",
    )

    test_mode = st.sidebar.checkbox("Test mode without API", value=False)
    test_rainfall = st.sidebar.slider("Test rainfall (mm/h)", 0.0, 50.0, 0.0, 0.5)

    st.sidebar.info("Use test mode to prove the Green/Yellow/Red thresholds work before submitting.")

    try:
        if test_mode:
            rainfall = float(test_rainfall)
            data_source = "Manual test value"
        else:
            weather_data = fetch_weather(city, api_key)
            rainfall = extract_rainfall_mm_per_hour(weather_data)
            data_source = "OpenWeatherMap Current Weather API"

        level, status, color = check_alert(rainfall)

        if level == "Red":
            log_alert(city, rainfall, level)

        show_dashboard(city, rainfall, level, status, color, data_source)

    except Exception as error:
        st.error(str(error))
        st.warning(
            "To keep testing without an API key, turn on 'Test mode without API' in the sidebar."
        )


if __name__ == "__main__":
    main()
