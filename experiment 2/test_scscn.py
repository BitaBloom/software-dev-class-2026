"""
test_scscn.py
Run:
    python test_scscn.py
"""

from scscn_runoff import calculate_runoff, calculate_retention


def almost_equal(a: float, b: float, tolerance: float = 0.05) -> bool:
    return abs(a - b) <= tolerance


def run_tests() -> None:
    # 1. P = 0: Expected Q = 0
    assert calculate_runoff(0, 80) == 0.0

    # 2. P < Ia: Expected Q = 0
    # For CN = 80, S = 63.5 and Ia = 12.7, so P = 10 is below Ia.
    assert calculate_runoff(10, 80) == 0.0

    # 3. P = Ia: Expected Q = 0
    S = calculate_retention(80)
    Ia = 0.2 * S
    assert calculate_runoff(Ia, 80) == 0.0

    # 4. Normal case: P = 50 mm, CN = 80
    q_normal = calculate_runoff(50, 80)
    assert almost_equal(q_normal, 13.8), f"Expected about 13.8, got {q_normal}"

    # 5. Maximum CN: CN = 100
    assert calculate_runoff(50, 100) == 50.0

    # 6. CN = 0: All water infiltrates
    assert calculate_runoff(50, 0) == 0.0

    # 7. Verify Q <= P for all cases
    rainfall_values = [0, 5, 10, 20, 50, 100, 200]
    cn_values = [0, 30, 60, 70, 80, 90, 95, 100]
    for P in rainfall_values:
        for CN in cn_values:
            Q = calculate_runoff(P, CN)
            assert Q >= 0, f"Negative runoff: P={P}, CN={CN}, Q={Q}"
            assert Q <= P, f"Runoff exceeds rainfall: P={P}, CN={CN}, Q={Q}"

    # 8. Higher CN should produce more runoff for fixed rainfall
    previous_q = -1.0
    for CN in [60, 70, 80, 90, 95, 100]:
        Q = calculate_runoff(50, CN)
        assert Q >= previous_q, f"Runoff did not increase at CN={CN}"
        previous_q = Q

    print("All SCS-CN tests passed successfully.")


if __name__ == "__main__":
    run_tests()
