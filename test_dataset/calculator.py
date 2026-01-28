"""
Module providing basic arithmetic operations: addition and division.
"""


def add(number_a: float, number_b: float) -> float:
    """Return the sum of two floating-point numbers."""
    return number_a + number_b


def divide(dividend: float, divisor: float) -> float:
    """
    Divide two numbers and return the result.

    Raises ZeroDivisionError if the divisor is zero.
    """
    if divisor == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return dividend / divisor


def main() -> None:
    """Run demonstration tests for the arithmetic functions."""
    print("Testing Calculator...")
    print(f"Addition result: {add(2.0, 3.0)}")
    try:
        print(f"Division result: {divide(10.0, 2.0)}")
    except ZeroDivisionError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()