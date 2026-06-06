# Prompt Log - Rainfall Alert System

## Project
Short-term Rainfall Forecasting & Alert System using Python, OpenWeatherMap API, and Streamlit.

## AI Interaction 1: API Integration
**Prompt used:**
I am a water resources student building a rainfall monitoring system. Please write Python code to fetch current weather data for Beijing using the OpenWeatherMap API. The code should use requests, extract rainfall intensity, handle API errors gracefully, and include comments.

**AI output summary:**
The AI generated a `fetch_weather()` function using the OpenWeatherMap current weather endpoint and `requests.get()`. It also included error handling for invalid API key, city not found, and network errors.

**Correction made:**
I added a separate `extract_rainfall_mm_per_hour()` function. If the API response has no `rain` field, the program treats rainfall as `0.0 mm/h`, because this usually means it is not raining.

## AI Interaction 2: Alert Logic
**Prompt used:**
Help me implement rainfall alert thresholds: Green for less than 10 mm/h, Yellow for 10 to less than 20 mm/h, and Red for 20 mm/h or above. When Red alert triggers, log the event with timestamp.

**AI output summary:**
The AI suggested a `check_alert()` function and a `log_alert()` function.

**Correction made:**
I checked the boundary values manually:
- 9.9 mm/h = Green
- 10.0 mm/h = Yellow
- 19.9 mm/h = Yellow
- 20.0 mm/h = Red

## AI Interaction 3: Dashboard
**Prompt used:**
Create a simple Streamlit dashboard for a rainfall monitoring system. It should show the title, current rainfall metric, alert status, historical data chart, and auto-refresh every 5 minutes.

**AI output summary:**
The AI created a dashboard layout with `st.title`, `st.metric`, color-coded status, and a line chart.

**Correction made:**
I added a test mode in the sidebar so the system can be tested even when there is no rain or the API key is not ready.

## Testing and Validation
I tested the alert system using manual test mode:

| Test Rainfall | Expected Result | Actual Result |
|---:|---|---|
| 0 mm/h | Green / Normal | Passed |
| 10 mm/h | Yellow / Moderate | Passed |
| 20 mm/h | Red / Alert | Passed |
| 35 mm/h | Red / Alert + log file | Passed |

## Physical Reasonableness
Rainfall values around 0 mm/h are normal when there is no rain. Rainfall above 20 mm/h is high enough to trigger a heavy rainfall alert in this experiment. Very high values should be checked carefully because API data can sometimes be delayed or affected by station/model uncertainty.
