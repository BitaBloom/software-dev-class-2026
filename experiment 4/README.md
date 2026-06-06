# Experiment 4 - Flood Inundation Analysis

This project performs a simple DEM-based flood inundation analysis.

## Files
- `flood_inundation.py`: main implementation
- `dem_data.npy`: generated DEM data
- `flood_extent_40m.png`: flood visualization at 40 m water level
- `flood_extent_50m.png`: flood visualization at 50 m water level
- `flood_curve.png`: water level vs flooded percentage plot
- `validation_report.txt`: physical validation output
- `prompt_log.md`: prompt log for AI/OpenCode assistance
- `requirements.txt`: required libraries

## How to Run

```bash
pip install -r requirements.txt
python flood_inundation.py
```

## Main Logic

A cell is flooded when:

```text
elevation < water_level
```

Inundation depth is:

```text
depth = water_level - elevation
```

for flooded cells, and 0 for non-flooded cells.
