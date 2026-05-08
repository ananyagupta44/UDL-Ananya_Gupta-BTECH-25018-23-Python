import random


def encode(value: int) -> tuple[int, int]:
    if not (0 <= value <= 4095):
        raise ValueError(f"Value {value} out of range. Must be 0–4095.")

    high = value >> 8      
    low  = value & 0xFF    
    return high, low


def decode(high: int, low: int) -> int:
    if not (0 <= high <= 255 and 0 <= low <= 255):
        raise ValueError("high and low must each be in range 0–255.")

    value = (high << 8) | low   
    return value


def run_tests():
    print("=" * 55)
    print("  Encode / Decode Test — 10 Random Values (0–4095)")
    print("=" * 55)

    random_values = random.sample(range(0, 4096), 10)  

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
