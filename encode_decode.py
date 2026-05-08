"""
encode_decode.py
Part 1 - Split and Reconstruct
Internship Assessment Task: Python Development
MyUpsideDownLab LLP
"""

import random


def encode(value: int) -> tuple[int, int]:
    """
    Splits a 12-bit integer (0–4095) into two bytes using bitwise operators.

    Args:
        value: An integer in range 0 to 4095.

    Returns:
        A tuple (high, low) where:
            high = upper 8 bits (value >> 8)
            low  = lower 8 bits (value & 0xFF)
    """
    if not (0 <= value <= 4095):
        raise ValueError(f"Value {value} out of range. Must be 0–4095.")

    high = value >> 8       # shift right by 8 bits to isolate upper byte
    low  = value & 0xFF     # mask lower 8 bits to isolate lower byte
    return high, low


def decode(high: int, low: int) -> int:
    """
    Reconstructs the original integer from two bytes using bitwise operators.

    Args:
        high: Upper byte (0–255)
        low:  Lower byte (0–255)

    Returns:
        Original integer reconstructed as (high << 8) | low
    """
    if not (0 <= high <= 255 and 0 <= low <= 255):
        raise ValueError("high and low must each be in range 0–255.")

    value = (high << 8) | low   # shift high byte back up, OR with low byte
    return value


def run_tests():
    """
    Generates 10 random values, encodes and decodes each one,
    asserts correctness, and prints the result.
    """
    print("=" * 55)
    print("  Encode / Decode Test — 10 Random Values (0–4095)")
    print("=" * 55)

    random_values = random.sample(range(0, 4096), 10)  # 10 unique random values

    all_passed = True
    for original in random_values:
        high, low = encode(original)
        decoded   = decode(high, low)

        match = decoded == original
        status = "✓" if match else "✗ MISMATCH"
        if not match:
            all_passed = False

        print(
            f"Original: {original:>4}  →  "
            f"High: {high:>3}, Low: {low:>3}  →  "
            f"Decoded: {decoded:>4}  {status}"
        )

    print("=" * 55)
    print("All tests passed! ✓" if all_passed else "Some tests FAILED! ✗")
    print("=" * 55)


if __name__ == "__main__":
    run_tests()
