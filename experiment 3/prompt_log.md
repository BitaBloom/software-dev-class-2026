# Prompt Log - Experiment 3: Reservoir Dispatch Optimization

## Experiment Goal
In this experiment, I used OpenCode / AI assistance to formulate and implement a 7-day reservoir release optimization problem. The goal was to balance hydropower revenue with ecological flow requirements and verify that all physical constraints were satisfied.

## Prompt 1: Problem Formulation
**Tool used:** OpenCode / AI assistant

**My prompt:** I need to formulate a reservoir dispatch optimization problem. There are 7 daily release decision variables, storage balance, storage bounds, release bounds, inflow forecast, and hydropower prices. Help me write the mathematical formulation.

**AI output summary:** The AI helped express the decision variables as daily releases and wrote the mass balance equation `V(t+1) = V(t) + (inflow - release) * delta_t`.

**My check/correction:** I checked that the units are consistent. Inflow and release are in m3/s, so I used 86400 seconds per day to convert the daily water balance into cubic meters.

## Prompt 2: scipy.optimize Implementation
**Tool used:** OpenCode / AI assistant

**My prompt:** Please help me implement this reservoir optimization using `scipy.optimize.minimize`. I need an objective function, release bounds, storage constraints, and output of the optimal schedule.

**AI output summary:** The AI suggested using SLSQP because it supports bounds and inequality constraints. It also helped structure the objective function and constraint functions.

**My check/correction:** I checked that scipy minimizes by default, so I used negative revenue to represent revenue maximization. I also checked that the release bounds are set from 10 to 100 m3/s.

## Prompt 3: Validation Report
**Tool used:** OpenCode / AI assistant

**My prompt:** Help me write validation code to check release limits, storage limits, mass balance, ecological deficit, and total revenue.

**AI output summary:** The AI suggested a text validation report with true/false checks for all constraints.

**My check/correction:** I added a mass balance check for every day by recalculating the next storage from the previous storage, inflow, release, and time step.

## Prompt 4: Trade-off Analysis
**Tool used:** OpenCode / AI assistant

**My prompt:** Help me create a trade-off analysis by running the optimization with different ecology weights and plotting ecological deficit against hydropower revenue.

**AI output summary:** The AI helped create a Pareto-style plot and compare cases with different ecology weights.

**My check/correction:** Since the main optimization has a strict release lower bound of 10 m3/s, ecological deficit is normally zero. For the trade-off plot, I used a relaxed version where releases below 10 m3/s are possible but penalized. This makes the ecology-revenue trade-off visible.

## Validation Notes
- The optimization was solved using SLSQP.
- Release bounds were checked.
- Storage bounds were checked.
- Mass balance was checked for every day.
- The optimal schedule was exported to `optimal_schedule.csv`.
- Trade-off analysis was exported to `tradeoff_analysis.png`.
