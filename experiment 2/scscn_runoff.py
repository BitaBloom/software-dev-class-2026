"""
scscn_runoff.py
Hydrological Modeling: SCS-CN Runoff Calculation
"""

from __future__ import annotations
from typing import Union

Number = Union[int, float]


def calculate_runoff(P: Number, CN: Number) -> float:
    """
    Calculate direct runoff depth using the SCS-CN method.

    S = (25400 / CN) - 254
    Ia = 0.2 * S
    Q = (P - Ia)^2 / (P - Ia + S), when P > Ia
    Q = 0, when P <= Ia

    Parameters:
        P: Rainfall depth in millimeters.
        CN: Curve Number, normally between 0 and 100.

    Returns:
        Runoff depth Q in millimeters.
    """
    P = float(P)
    CN = float(CN)

    if P <= 0:
        return 0.0
    if CN <= 0:
        return 0.0
    if CN >= 100:
        return P

    S = (25400.0 / CN) - 254.0
    Ia = 0.2 * S

    if P <= Ia:
        return 0.0

    Q = ((P - Ia) ** 2) / (P - Ia + S)
    return max(0.0, min(Q, P))


def calculate_retention(CN: Number) -> float:
    """Calculate potential maximum retention S from Curve Number."""
    CN = float(CN)
    if CN <= 0:
        return float("inf")
    if CN >= 100:
        return 0.0
    return (25400.0 / CN) - 254.0


if __name__ == "__main__":
    P = 50
    CN = 80
    Q = calculate_runoff(P, CN)
    print("SCS-CN Runoff Calculation Example")
    print(f"Rainfall P = {P} mm")
    print(f"Curve Number CN = {CN}")
    print(f"Runoff Q = {Q:.2f} mm")
