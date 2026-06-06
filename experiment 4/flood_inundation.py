"""
flood_inundation.py
Experiment 4: Flood Inundation Analysis using DEM data

Run:
    python flood_inundation.py
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def load_dem(filepath: str | None = None) -> np.ndarray:
    """
    Load DEM data from a .npy file or generate a synthetic 100x100 DEM.

    The synthetic DEM uses a simple sloped terrain plus small terrain variation.
    Elevation values are kept between 30 m and 80 m.
    """
    if filepath is not None and Path(filepath).exists():
        return np.load(filepath)

    np.random.seed(42)

    rows, cols = 100, 100
    x = np.linspace(0, 1, cols)
    y = np.linspace(0, 1, rows)
    xx, yy = np.meshgrid(x, y)

    slope = 30 + 45 * (0.55 * xx + 0.45 * yy)
    valley = -8 * np.exp(-((yy - 0.45) ** 2) / 0.025)
    noise = np.random.normal(0, 1.2, size=(rows, cols))

    dem = slope + valley + noise
    dem = 30 + (dem - dem.min()) / (dem.max() - dem.min()) * 50

    np.save("dem_data.npy", dem)
    return dem


def calculate_flood(dem: np.ndarray, water_level: float) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Calculate flood extent and inundation depth for a given water level.

    Flooding rule:
        flooded if elevation < water_level

    Returns:
        flooded_mask: boolean array, True where flooded
        depth: water depth array, 0 where not flooded
        percentage: flooded area percentage, 0-100
    """
    flooded_mask = dem < water_level
    depth = np.where(flooded_mask, water_level - dem, 0.0)
    percentage = float(np.sum(flooded_mask) / flooded_mask.size * 100)
    return flooded_mask, depth, percentage


def visualize_flood(dem: np.ndarray, water_level: float, output_file: str) -> None:
    """
    Create flood visualization:
    1. Original DEM
    2. Flood extent overlay
    3. Inundation depth heatmap
    """
    flooded_mask, depth, percentage = calculate_flood(dem, water_level)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    dem_plot = axes[0].imshow(dem, cmap="gray")
    axes[0].set_title("Original DEM Elevation")
    axes[0].set_xlabel("Column")
    axes[0].set_ylabel("Row")
    plt.colorbar(dem_plot, ax=axes[0], fraction=0.046, pad=0.04, label="Elevation (m)")

    axes[1].imshow(dem, cmap="gray")
    flood_overlay = np.ma.masked_where(~flooded_mask, flooded_mask)
    axes[1].imshow(flood_overlay, cmap="Blues", alpha=0.65)
    axes[1].set_title(f"Flood Extent at {water_level:.0f} m\nFlooded Area: {percentage:.2f}%")
    axes[1].set_xlabel("Column")
    axes[1].set_ylabel("Row")

    depth_plot = axes[2].imshow(depth, cmap="Blues")
    axes[2].set_title("Inundation Depth")
    axes[2].set_xlabel("Column")
    axes[2].set_ylabel("Row")
    plt.colorbar(depth_plot, ax=axes[2], fraction=0.046, pad=0.04, label="Depth (m)")

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close(fig)


def simulate_rising_water(dem: np.ndarray, levels: np.ndarray) -> list[dict]:
    """Simulate flooding for multiple rising water levels."""
    results = []

    for level in levels:
        flooded_mask, depth, percentage = calculate_flood(dem, float(level))
        results.append({
            "water_level_m": float(level),
            "flooded_percentage": percentage,
            "max_depth_m": float(depth.max()),
            "flooded_cells": int(np.sum(flooded_mask)),
        })

    return results


def plot_flood_curve(results: list[dict], output_file: str = "flood_curve.png") -> None:
    """Create water level vs flooded percentage plot."""
    levels = [item["water_level_m"] for item in results]
    percentages = [item["flooded_percentage"] for item in results]

    plt.figure(figsize=(8, 5))
    plt.plot(levels, percentages, marker="o")
    plt.xlabel("Water Level (m)")
    plt.ylabel("Flooded Area (%)")
    plt.title("Rising Water Simulation: Water Level vs Flooded Area")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


def validate_results(dem: np.ndarray, results: list[dict]) -> str:
    """Validate physical correctness and save validation_report.txt."""
    lines = []
    lines.append("Validation Report - Flood Inundation Analysis")
    lines.append("=" * 55)
    lines.append(f"DEM shape: {dem.shape}")
    lines.append(f"Minimum elevation: {dem.min():.2f} m")
    lines.append(f"Maximum elevation: {dem.max():.2f} m")
    lines.append("")

    percentages = np.array([item["flooded_percentage"] for item in results])
    monotonic = bool(np.all(np.diff(percentages) >= -1e-9))
    within_range = bool(np.all((percentages >= 0) & (percentages <= 100)))

    lines.append(f"Flooded area increases with water level: {monotonic}")
    lines.append(f"Flooded percentage always between 0 and 100: {within_range}")

    max_depth_checks = []
    for item in results:
        level = item["water_level_m"]
        expected_max_depth = max(0.0, level - float(dem.min()))
        actual_max_depth = item["max_depth_m"]
        max_depth_checks.append(abs(actual_max_depth - expected_max_depth) < 1e-6)

    lines.append(f"Maximum depth check passed for all tested levels: {all(max_depth_checks)}")

    below_min_level = float(dem.min() - 1)
    above_max_level = float(dem.max() + 1)

    _, below_depth, below_pct = calculate_flood(dem, below_min_level)
    _, _, above_pct = calculate_flood(dem, above_max_level)

    below_ok = below_pct == 0.0 and below_depth.max() == 0.0
    above_ok = above_pct == 100.0

    lines.append(f"Edge case water below minimum elevation gives 0% flooded: {below_ok}")
    lines.append(f"Edge case water above maximum elevation gives 100% flooded: {above_ok}")
    lines.append("")

    lines.append("Rising Water Results:")
    for item in results:
        lines.append(
            f"Water level {item['water_level_m']:.1f} m: "
            f"{item['flooded_percentage']:.2f}% flooded, "
            f"max depth {item['max_depth_m']:.2f} m"
        )

    report = "\n".join(lines)
    Path("validation_report.txt").write_text(report, encoding="utf-8")
    return report


def main() -> None:
    """Run the complete DEM-based flood inundation analysis."""
    dem = load_dem()

    visualize_flood(dem, water_level=40, output_file="flood_extent_40m.png")
    visualize_flood(dem, water_level=50, output_file="flood_extent_50m.png")

    levels = np.arange(40, 51, 1)
    results = simulate_rising_water(dem, levels)
    plot_flood_curve(results, output_file="flood_curve.png")

    report = validate_results(dem, results)

    print("Flood inundation analysis completed.")
    print()
    print(report)
    print()
    print("Generated files:")
    print("- dem_data.npy")
    print("- flood_extent_40m.png")
    print("- flood_extent_50m.png")
    print("- flood_curve.png")
    print("- validation_report.txt")


if __name__ == "__main__":
    main()
