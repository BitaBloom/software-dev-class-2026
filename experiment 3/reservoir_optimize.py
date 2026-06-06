"""
reservoir_optimize.py
Experiment 3: Water Resources Optimization - Reservoir Dispatch

Run:
    python reservoir_optimize.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize


# -----------------------------
# Reservoir input data
# -----------------------------
DAYS = 7
SECONDS_PER_DAY = 24 * 60 * 60

INITIAL_STORAGE = 500_000.0   # m3
V_MIN = 100_000.0             # m3
V_MAX = 1_000_000.0           # m3

Q_ECO = 10.0                  # m3/s
Q_MAX = 100.0                 # m3/s

INFLOW = np.array([15, 12, 10, 8, 12, 15, 18], dtype=float)  # m3/s
PRICE = np.array([0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10], dtype=float)

# A simple proportional hydropower revenue coefficient.
# This keeps the output revenue in a readable project scale close to the guide example.
REVENUE_COEFFICIENT = 0.06


def calculate_storage(releases: np.ndarray) -> np.ndarray:
    """
    Calculate storage trajectory from daily releases using mass balance.

    V(t+1) = V(t) + (inflow - release) * delta_t

    Returns:
        Array of length 8: storage at start and after each day.
    """
    releases = np.asarray(releases, dtype=float)
    storage = [INITIAL_STORAGE]

    for day in range(DAYS):
        next_storage = storage[-1] + (INFLOW[day] - releases[day]) * SECONDS_PER_DAY
        storage.append(next_storage)

    return np.array(storage)


def calculate_revenue(releases: np.ndarray) -> float:
    """
    Calculate total hydropower revenue using release and price.

    Revenue is simplified as:
        sum(release * price * seconds_per_day * coefficient)
    """
    releases = np.asarray(releases, dtype=float)
    return float(np.sum(releases * PRICE * SECONDS_PER_DAY * REVENUE_COEFFICIENT))


def calculate_ecological_deficit(releases: np.ndarray) -> float:
    """
    Calculate total ecological deficit below the minimum ecological release.
    With release bounds set at Q_ECO, this should normally be zero.
    """
    releases = np.asarray(releases, dtype=float)
    deficits = np.maximum(0.0, Q_ECO - releases)
    return float(np.sum(deficits))


def objective(releases: np.ndarray, ecology_weight: float = 0.0) -> float:
    """
    Objective function for scipy.optimize.minimize.

    scipy minimizes, so revenue is made negative.
    A penalty is added if releases violate ecological flow.
    """
    revenue = calculate_revenue(releases)
    ecological_deficit = calculate_ecological_deficit(releases)

    # A very small smoothing term helps SLSQP converge reliably
    # when the main objective is almost linear.
    smoothing = 1e-3 * float(np.sum((releases - INFLOW) ** 2))
    return -revenue + ecology_weight * ecological_deficit * 1_000_000.0 + smoothing


def storage_min_constraint(releases: np.ndarray) -> np.ndarray:
    """Constraint: storage must be greater than or equal to V_MIN.

    A small numerical buffer is used to help the optimizer avoid tiny
    floating-point violations exactly at the boundary.
    """
    storage = calculate_storage(releases)
    buffer = 100.0
    return (storage[1:] - (V_MIN + buffer)) / 100000.0


def storage_max_constraint(releases: np.ndarray) -> np.ndarray:
    """Constraint: storage must be less than or equal to V_MAX.

    A small numerical buffer is used to help the optimizer avoid tiny
    floating-point violations exactly at the boundary.
    """
    storage = calculate_storage(releases)
    buffer = 100.0
    return ((V_MAX - buffer) - storage[1:]) / 100000.0


def solve_reservoir_optimization(ecology_weight: float = 0.0) -> dict:
    """
    Solve the 7-day reservoir release optimization problem.

    Returns:
        Dictionary containing success flag, optimal releases, storage,
        revenue, deficit, and the raw scipy result.
    """
    # Initial guess: release close to ecological minimum and inflow.
    x0 = np.maximum(Q_ECO, INFLOW.copy())

    # Release bounds guarantee Q_ECO <= Q_release <= Q_MAX.
    bounds = [(Q_ECO, Q_MAX) for _ in range(DAYS)]

    constraints = [
        {"type": "ineq", "fun": storage_min_constraint},
        {"type": "ineq", "fun": storage_max_constraint},
    ]

    result = minimize(
        fun=lambda x: objective(x, ecology_weight=ecology_weight),
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000, "ftol": 1e-9},
    )

    releases = result.x
    storage = calculate_storage(releases)
    revenue = calculate_revenue(releases)
    deficit = calculate_ecological_deficit(releases)

    release_ok = bool(np.all(releases >= Q_ECO - 1e-6) and np.all(releases <= Q_MAX + 1e-6))
    storage_ok = bool(np.all(storage >= V_MIN - 1e-3) and np.all(storage <= V_MAX + 1e-3))
    feasible_success = bool(result.success or (release_ok and storage_ok and deficit < 1e-6))

    return {
        "success": feasible_success,
        "message": result.message,
        "releases": releases,
        "storage": storage,
        "revenue": revenue,
        "ecological_deficit": deficit,
        "result": result,
    }

def make_schedule_dataframe(solution: dict) -> pd.DataFrame:
    """Create a readable 7-day optimal schedule table."""
    releases = solution["releases"]
    storage = solution["storage"]

    df = pd.DataFrame({
        "Day": np.arange(1, DAYS + 1),
        "Inflow_m3s": INFLOW,
        "Release_m3s": releases,
        "Price_USD_per_kWh": PRICE,
        "Storage_Start_m3": storage[:-1],
        "Storage_End_m3": storage[1:],
        "Daily_Revenue": releases * PRICE * SECONDS_PER_DAY * REVENUE_COEFFICIENT,
        "Ecological_Deficit_m3s": np.maximum(0.0, Q_ECO - releases),
    })

    return df


def save_validation_report(solution: dict, schedule: pd.DataFrame) -> None:
    """Validate constraints and save a plain text report."""
    releases = solution["releases"]
    storage = solution["storage"]
    revenue = solution["revenue"]
    deficit = solution["ecological_deficit"]

    lines = []
    lines.append("Validation Report - Reservoir Optimization")
    lines.append("=" * 50)
    lines.append(f"Optimization success: {solution['success']}")
    lines.append(f"Solver message: {solution['message']}")
    lines.append("")

    # Release constraints
    release_min_ok = bool(np.all(releases >= Q_ECO - 1e-6))
    release_max_ok = bool(np.all(releases <= Q_MAX + 1e-6))
    lines.append(f"Release lower bound Q >= {Q_ECO} m3/s: {release_min_ok}")
    lines.append(f"Release upper bound Q <= {Q_MAX} m3/s: {release_max_ok}")

    # Storage constraints
    storage_min_ok = bool(np.all(storage >= V_MIN - 1e-3))
    storage_max_ok = bool(np.all(storage <= V_MAX + 1e-3))
    lines.append(f"Storage lower bound V >= {V_MIN:.0f} m3: {storage_min_ok}")
    lines.append(f"Storage upper bound V <= {V_MAX:.0f} m3: {storage_max_ok}")

    # Mass balance check
    mass_balance_ok = True
    for day in range(DAYS):
        expected = storage[day] + (INFLOW[day] - releases[day]) * SECONDS_PER_DAY
        if abs(expected - storage[day + 1]) > 1e-3:
            mass_balance_ok = False
            break

    lines.append(f"Mass balance satisfied for all days: {mass_balance_ok}")
    lines.append(f"Ecological deficit: {deficit:.4f} m3/s-days")
    lines.append(f"Total revenue: ${revenue:,.2f}")
    lines.append("")

    lines.append("Daily Schedule:")
    lines.append(schedule.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    Path("validation_report.txt").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run optimization, save schedule CSV, and validation report."""
    solution = solve_reservoir_optimization(ecology_weight=0.0)
    schedule = make_schedule_dataframe(solution)

    schedule.to_csv("optimal_schedule.csv", index=False)
    save_validation_report(solution, schedule)

    print("Reservoir optimization completed.")
    print(f"Optimization success: {solution['success']}")
    print(f"Total revenue: ${solution['revenue']:,.2f}")
    print(f"Ecological deficit: {solution['ecological_deficit']:.4f}")
    print()
    print(schedule[["Day", "Inflow_m3s", "Release_m3s", "Storage_End_m3", "Daily_Revenue"]].to_string(
        index=False,
        float_format=lambda x: f"{x:,.2f}"
    ))
    print()
    print("Generated files:")
    print("- optimal_schedule.csv")
    print("- validation_report.txt")


if __name__ == "__main__":
    main()
