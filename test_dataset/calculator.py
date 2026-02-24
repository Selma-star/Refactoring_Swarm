"""
Module providing basic arithmetic operations: addition and division with validation.
"""

import math


def add(number_a: float, number_b: float) -> float:
    """Return the sum of two finite floating-point numbers."""
    if not (math.isfinite(number_a) and math.isfinite(number_b)):
        raise ValueError("Inputs must be finite numbers (not NaN or Inf).")
    return number_a + number_b


def divide(dividend: float, divisor: float) -> float:
    """
    Divide two finite numbers and return the result.

    Raises ZeroDivisionError if the divisor is near zero.
    Raises ValueError if inputs are not finite.
    """
    if not (math.isfinite(dividend) and math.isfinite(divisor)):
        raise ValueError("Inputs must be finite numbers (not NaN or Inf).")

    if math.isclose(divisor, 0.0, abs_tol=1e-12):
        raise ZeroDivisionError("Cannot divide by zero or a value near zero.")

    return dividend / divisor


def main() -> None:
    """Run demonstration tests for the arithmetic functions."""
    print("Testing Calculator...")

    try:
        res_add = add(2.0, 3.0)
        print(f"Addition result: {res_add}")
    except (ValueError, TypeError):
        print("Error: Invalid input for addition.")

    try:
        res_div = divide(10.0, 2.0)
        print(f"Division result: {res_div}")
    except (ZeroDivisionError, ValueError, TypeError) as error:
        # Use a controlled error message to avoid internal leak
        if isinstance(error, ZeroDivisionError):
            print("Error: Division by zero or near-zero value.")
        else:
            print("Error: Invalid input for division.")


if __name__ == "__main__":
    main()