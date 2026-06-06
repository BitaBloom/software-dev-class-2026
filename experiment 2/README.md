# Experiment 2 - SCS-CN Runoff Calculation

This project implements the Soil Conservation Service Curve Number method for estimating direct runoff from rainfall.

## Files
- `scscn_runoff.py`: main implementation with `calculate_runoff(P, CN)`
- `test_scscn.py`: boundary condition and validation tests
- `sensitivity_analysis.py`: sensitivity analysis and plot generation
- `runoff_comparison.png`: generated comparison plot
- `cn_vs_runoff.png`: generated CN sensitivity plot
- `prompt_log.md`: documentation of AI interactions
- `requirements.txt`: required Python libraries

## How to Run

```bash
pip install -r requirements.txt
python test_scscn.py
python sensitivity_analysis.py
```

## Expected Result

For `P = 50 mm` and `CN = 80`, the runoff should be approximately `13.8 mm`.

## Physical Checks

- If `P <= Ia`, runoff is 0.
- If `CN = 0`, runoff is 0.
- If `CN = 100`, runoff equals rainfall.
- Runoff is never greater than rainfall.
- Higher CN values produce higher runoff.
