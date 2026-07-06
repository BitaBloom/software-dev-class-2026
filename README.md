# Software Development 2026 - Smart Water Lab Experiments

This repository contains four software development experiments from the Smart Water Lab series.
Each experiment focuses on a different water resources or hydrology-related programming task.

## Repository Structure

```text
software-dev-class-2026/
│
├── experiment 1/   Rainfall Alert System
├── experiment 2/   SCS-CN Runoff Calculation
├── experiment 3/   Reservoir Dispatch Optimization
└── experiment 4/   Flood Inundation Analysis
```

Each folder contains the source code, required output files, prompt log, and screenshots or validation results.

---

## Experiment 1 - Short-term Rainfall Forecasting and Alert System

This experiment builds a rainfall monitoring dashboard using Streamlit.
The system checks rainfall intensity and shows different warning levels based on threshold rules.

Main functions:

* Fetch or test rainfall data
* Display rainfall status in a dashboard
* Apply Green, Yellow, and Red alert rules
* Record red alert events in a log file

Main files:

```text
weather_monitor.py
alert_log.txt
prompt_log.md
requirements.txt
```

Run:

```bash
pip install -r requirements.txt
streamlit run weather_monitor.py
```

---

## Experiment 2 - SCS-CN Runoff Calculation

This experiment implements the SCS-CN method for estimating direct runoff from rainfall.
It includes formula implementation, boundary condition tests, and sensitivity analysis.

Main functions:

* Calculate runoff using the SCS-CN formula
* Test physical boundary conditions
* Check that runoff does not exceed rainfall
* Analyze how runoff changes with Curve Number values

Main files:

```text
scscn_runoff.py
test_scscn.py
sensitivity_analysis.py
runoff_comparison.png
cn_vs_runoff.png
prompt_log.md
```

Run:

```bash
pip install -r requirements.txt
python test_scscn.py
python sensitivity_analysis.py
```

---

## Experiment 3 - Reservoir Dispatch Optimization

This experiment solves a 7-day reservoir release optimization problem.
The objective is to balance hydropower revenue and downstream ecological flow requirements.

Main functions:

* Define reservoir release decision variables
* Apply storage and release constraints
* Solve the optimization problem using scipy.optimize
* Generate an optimal release schedule
* Create a trade-off analysis between ecology and revenue

Main files:

```text
reservoir_optimize.py
tradeoff_analysis.py
optimal_schedule.csv
tradeoff_analysis.png
validation_report.txt
prompt_log.md
```

Run:

```bash
pip install -r requirements.txt
python reservoir_optimize.py
python tradeoff_analysis.py
```

---

## Experiment 4 - DEM-based Flood Inundation Analysis

This experiment analyzes flood inundation using synthetic DEM data.
It calculates flooded cells at different water levels and creates flood extent maps.

Main functions:

* Generate DEM elevation data
* Calculate flood mask and inundation depth
* Create flood extent maps at 40 m and 50 m
* Plot water level versus flooded area percentage
* Validate that flooded area increases with water level

Main files:

```text
flood_inundation.py
dem_data.npy
flood_extent_40m.png
flood_extent_50m.png
flood_curve.png
validation_report.txt
prompt_log.md
```

Run:

```bash
pip install -r requirements.txt
python flood_inundation.py
```

---

## Tools and Libraries

The experiments use:

```text
Python
NumPy
pandas
matplotlib
scipy
Streamlit
requests
OpenWeatherMap API
```

---

## Validation

The experiments include screenshots, generated plots, logs, or validation reports to show that the programs were tested.

Validation examples:

* Rainfall alert thresholds were tested.
* SCS-CN runoff boundary conditions passed.
* Reservoir storage and release constraints were checked.
* Flooded area was confirmed to increase as water level increased.

---

## Notes

Prompt logs are included in each experiment folder to document the development process and the questions asked during implementation.
