"""
tradeoff_analysis.py
Experiment 3: Trade-off Analysis for Reservoir Dispatch

Run:
    python tradeoff_analysis.py

Output:
    tradeoff_analysis.png
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from reservoir_optimize import (
    DAYS,
    INFLOW,
    PRICE,
    SECONDS_PER_DAY,
    INITIAL_STORAGE,
    V_MIN,
    V_MAX,
    Q_ECO,
    Q_MAX,
    REVENUE_COEFFICIENT,
    calculate_revenue,
    calculate_storage,
    solve_reservoir_optimization,
)


def ecological_deficit(releases: np.ndarray) -> float:
    """Total deficit below ecological release, measured in m3/s-days."""
    return float(np.sum(np.maximum(0.0, Q_ECO - releases)))


def solve_relaxed_tradeoff(ecology_weight: float) -> dict:
    """
    Solve a relaxed trade-off problem.

    In the main solution, Q_release >= Q_ECO is a hard constraint.
    Here, the lower release bound is relaxed to 0 so that the Pareto trade-off
    between ecology and revenue can be visualized. Ecological deficit is then
    penalized in the objective function.
    """

    def objective(x: np.ndarray) -> float:
        revenue = calculate_revenue(x)
        deficit = ecological_deficit(x)
        # Minimize negative revenue plus ecology penalty.
        return -revenue + ecology_weight * deficit * 5000.0

    def storage_min_constraint(x: np.ndarray) -> np.ndarray:
        return (calculate_storage(x)[1:] - (V_MIN + 100.0)) / 100000.0

    def storage_max_constraint(x: np.ndarray) -> np.ndarray:
        return ((V_MAX - 100.0) - calculate_storage(x)[1:]) / 100000.0

    x0 = np.maximum(0.0, INFLOW.copy())
    bounds = [(0.0, Q_MAX) for _ in range(DAYS)]
    constraints = [
        {"type": "ineq", "fun": storage_min_constraint},
        {"type": "ineq", "fun": storage_max_constraint},
    ]

    result = minimize(
        objective,
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000, "ftol": 1e-9, "disp": False},
    )

    releases = result.x
    return {
        "weight": ecology_weight,
        "success": bool(result.success),
        "releases": releases,
        "revenue": calculate_revenue(releases),
        "ecological_deficit": ecological_deficit(releases),
    }


def create_tradeoff_plot() -> None:
    weights = [0, 0.5, 1, 2, 5, 10, 20, 50, 100]
    solutions = [solve_relaxed_tradeoff(w) for w in weights]

    revenues = [s["revenue"] for s in solutions]
    deficits = [s["ecological_deficit"] for s in solutions]

    plt.figure(figsize=(8, 5))
    plt.plot(deficits, revenues, marker="o")
    for s in solutions:
        plt.annotate(f"w={s['weight']}", (s["ecological_deficit"], s["revenue"]), fontsize=8)

    plt.xlabel("Ecological Deficit (m3/s-days)")
    plt.ylabel("Hydropower Revenue ($)")
    plt.title("Pareto-style Trade-off: Ecology vs Hydropower Revenue")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("tradeoff_analysis.png", dpi=300)
    plt.close()

    strict_solution = solve_reservoir_optimization(ecology_weight=0.0)
    no_ecology_solution = solutions[0]
    cost = no_ecology_solution["revenue"] - strict_solution["revenue"]

    print("Trade-off analysis completed.")
    print("Generated file: tradeoff_analysis.png")
    print()
    print("Weight | Revenue | Ecological Deficit")
    for s in solutions:
        print(f"{s['weight']:>6} | ${s['revenue']:>10,.2f} | {s['ecological_deficit']:>8.3f}")

    print()
    print("Cost of maintaining minimum ecological flow:")
    print(f"Revenue without strict ecological lower bound: ${no_ecology_solution['revenue']:,.2f}")
    print(f"Revenue with Q >= {Q_ECO} m3/s: ${strict_solution['revenue']:,.2f}")
    print(f"Estimated revenue difference: ${cost:,.2f}")
    print()
    print("Observation:")
    print("When ecology is prioritized, ecological deficit decreases.")
    print("The strict main optimization keeps ecological deficit equal to zero.")
    print("All results should still be checked using the validation report.")


if __name__ == "__main__":
    create_tradeoff_plot()
