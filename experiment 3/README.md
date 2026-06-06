# Experiment 3 - Reservoir Dispatch Optimization

This project solves a 7-day reservoir release optimization problem using `scipy.optimize`.

## Files
- `reservoir_optimize.py`: main optimization implementation
- `optimal_schedule.csv`: generated 7-day release schedule
- `tradeoff_analysis.py`: trade-off analysis code
- `tradeoff_analysis.png`: Pareto-style trade-off plot
- `validation_report.txt`: constraint verification report
- `prompt_log.md`: prompt log documenting AI interactions
- `requirements.txt`: required libraries

## How to Run

Install requirements:

```bash
pip install -r requirements.txt
```

Run the main optimization:

```bash
python reservoir_optimize.py
```

Run the trade-off analysis:

```bash
python tradeoff_analysis.py
```

## Physical Constraints Checked
- Storage stays between minimum and maximum storage.
- Release stays between ecological minimum and maximum release.
- Mass balance is satisfied for each day.
- Ecological deficit is calculated.
- Revenue is calculated from release and price.
