# UDL – [First Name] – [Roll Number] – Python

Internship Assessment Task submission for the **Software Engineering Intern** role at **MyUpsideDownLab LLP**.

---

## Repository Structure

```
.
├── encode_decode.py   # Part 1 — encode() / decode() functions + 10-value test loop
├── monitor.py         # Part 2 — Two-thread real-time sensor monitor
├── analysis.md        # Written answers to all 5 analysis questions
└── README.md          # This file
```

---

## Part 1 — Split and Reconstruct (`encode_decode.py`)

Implements `encode(value)` and `decode(high, low)` using **bitwise operators only**:

| Operation | Purpose |
|---|---|
| `value >> 8` | Extracts the upper byte (high) |
| `value & 0xFF` | Extracts the lower byte (low) |
| `(high << 8) \| low` | Reassembles the original value |

### Run

```bash
python encode_decode.py
```

### Sample Output

```
=======================================================
  Encode / Decode Test — 10 Random Values (0–4095)
=======================================================
Original: 2850  →  High:  11, Low:  34  →  Decoded: 2850  ✓
Original:  413  →  High:   1, Low: 157  →  Decoded:  413  ✓
...
All tests passed! ✓
=======================================================
```

---

## Part 2 — Real-Time Monitor (`monitor.py`)

Simulates a two-thread sensor pipeline:

- **Thread 1 (Sensor):** Generates a random value (0–4095) every 100 ms, encodes it, and puts `(high, low)` into a `queue.Queue`.
- **Thread 2 (Monitor):** Decodes each pair, maintains a **running average of the last 10 values** using `collections.deque(maxlen=10)`, and prints a warning if the average goes above 3000 or below 500.
- Runs for **20 seconds**, then stops both threads cleanly and prints a summary.

### Run

```bash
python monitor.py
```

### Sample Output

```
==================================================
  Real-Time Sensor Monitor — starting …
  Duration : 20 s  |  Sample rate : 100 ms
  Thresholds : < 500 (low)  /  > 3000 (high)
==================================================
WARNING: Running avg = 3142.0 - too high!
WARNING: Running avg = 423.5 - too low!
...

==================================================
  Simulation complete.
  Total values received : 198
  Overall average       : 2041.3
  Threshold warnings    : 14
==================================================
```

---

## Requirements

- Python 3.10+
- No external libraries — uses only the standard library (`random`, `queue`, `threading`, `collections`, `time`).

---

## Analysis

See [`analysis.md`](analysis.md) for written answers to all 5 questions covering byte limits, bitwise operations, running vs overall averages, and thread-safe queues.
