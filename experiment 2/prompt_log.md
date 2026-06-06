# Prompt Log - Experiment 2: SCS-CN Runoff Calculation

## Experiment Goal
In this experiment, I used AI assistance to help implement and test the SCS-CN runoff calculation method in Python. The main goal was to translate the hydrological formula into code, check boundary conditions, and create plots for sensitivity analysis.

## Prompt 1: Understanding the Formula
**Tool used:** OpenCode / AI assistant

**My prompt:** I need to implement the SCS-CN runoff method in Python. The formula is Q = (P - Ia)^2 / (P - Ia + S), where S = 25400 / CN - 254 and Ia = 0.2S. Please help me write a simple function with boundary conditions.

**AI output summary:** The AI suggested a `calculate_runoff(P, CN)` function. It calculated S, Ia, and Q based on the SCS-CN equation.

**My check/correction:** I checked the physical conditions from the experiment guide. I made sure that when rainfall is less than or equal to initial abstraction, the function returns 0. I also added safety conditions so runoff cannot be negative or greater than rainfall.

## Prompt 2: Boundary Condition Tests
**Tool used:** OpenCode / AI assistant

**My prompt:** Help me write simple tests for this runoff function. I need to test P = 0, P < Ia, P = Ia, P = 50 with CN = 80, CN = 100, and also check that Q is never greater than P.

**AI output summary:** The AI helped generate a test file using Python `assert` statements.

**My check/correction:** I manually checked the expected example from the guide: P = 50 mm, CN = 80, S = 63.5 mm, Ia = 12.7 mm, and Q is about 13.8 mm. The result from the code matched this expected value.

## Prompt 3: Sensitivity Analysis
**Tool used:** OpenCode / AI assistant

**My prompt:** Please help me create sensitivity analysis code. I want to fix rainfall at 50 mm and calculate runoff for CN values 60, 70, 80, 90, 95, and 100. Also generate plots to compare rainfall and runoff.

**AI output summary:** The AI suggested code using NumPy, pandas, and matplotlib. The script prints a CN/runoff table and saves two plot images.

**My check/correction:** I checked the output table and confirmed that runoff increases as CN increases. This makes physical sense because higher CN values represent more urban or impervious land surfaces.

## Validation Results
The tests passed successfully in PyCharm.

Important results for P = 50 mm:

| CN | Runoff Q (mm) |
|---:|--------------:|
| 60 | 1.40 |
| 70 | 5.81 |
| 80 | 13.80 |
| 90 | 27.11 |
| 95 | 36.90 |
| 100 | 50.00 |

## Observations
1. Higher CN values produce higher runoff.
2. Lower CN values produce less runoff because more water infiltrates into the soil.
3. CN = 100 behaves like an impervious surface, so runoff equals rainfall.
4. The code keeps Q less than or equal to P, which is physically reasonable.
5. The boundary tests helped catch possible mistakes before making the plots.

## Files Created
- `scscn_runoff.py`
- `test_scscn.py`
- `sensitivity_analysis.py`
- `runoff_comparison.png`
- `cn_vs_runoff.png`
