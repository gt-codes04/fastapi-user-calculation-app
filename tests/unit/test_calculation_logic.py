# tests/unit/test_calculation_logic.py

from app import crud


def test_compute_pow():
    # 2^3 = 8
    result = crud._compute(2, 3, "pow")
    assert result == 8


def test_compute_add():
    assert crud._compute(1, 2, "add") == 3


def test_compute_invalid_operation_raises():
    from pytest import raises

    with raises(ValueError):
        crud._compute(1, 2, "unknown_op")
