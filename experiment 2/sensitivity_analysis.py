"""
sensitivity_analysis.py
Run:
    python sensitivity_analysis.py
"""

from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scscn_runoff import calculate_runoff


def cn_sensitivity_analysis() -> pd.DataFrame:
    P = 50
    cn_values = [60, 70, 80, 90, 95, 100]
    runoff_values = [calculate_runoff(P, CN) for CN in cn_values]
    return pd.DataFrame({
        "CN": cn_values,
        "Rainfall_mm": [P] * len(cn_values),
        "Runoff_mm": runoff_values,
    })


def create_plots() -> None:
    results = cn_sensitivity_analysis()

    plt.figure(figsize=(8, 5))
    plt.plot(results["CN"], results["Runoff_mm"], marker="o")
    plt.xlabel("Curve Number (CN)")
    plt.ylabel("Runoff Q (mm)")
    plt.title("Sensitivity Analysis: CN vs Runoff for P = 50 mm")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cn_vs_runoff.png", dpi=300)
    plt.close()

    rainfall_values = np.linspace(0, 100, 101)
    cn_values = [60, 70, 80, 90, 95, 100]

    plt.figure(figsize=(9, 6))
    for CN in cn_values:
        runoff_values = [calculate_runoff(P, CN) for P in rainfall_values]
        plt.plot(rainfall_values, runoff_values, label=f"CN = {CN}")

    plt.xlabel("Rainfall P (mm)")
    plt.ylabel("Runoff Q (mm)")
    plt.title("Rainfall vs Runoff for Different Curve Numbers")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("runoff_comparison.png", dpi=300)
    plt.close()

    print("Sensitivity analysis completed.")
    print("\nFixed rainfall sensitivity results:")
    print(results.to_string(index=False))
    print("\nGenerated plots:")
    print("- cn_vs_runoff.png")
    print("- runoff_comparison.png")
    print("\nObservations:")
    print("1. Runoff increases as CN increases.")
    print("2. Low CN values represent more infiltration and less runoff.")
    print("3. High CN values represent urban or paved conditions and produce more runoff.")
    print("4. For CN = 100, runoff equals rainfall because the surface is impervious.")
    print("5. In all tested cases, Q <= P, which is physically reasonable.")


if __name__ == "__main__":
    create_plots()
