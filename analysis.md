# analysis.md — Written Answers

**Internship Assessment Task: Python Development**
MyUpsideDownLab LLP

---

## Q1. Why can't 2850 fit in one byte? What is the maximum value a single byte can hold, and why?

A byte is made up of 8 bits. Each bit can be either 0 or 1, so 8 bits together give 2⁸ = 256 possible combinations, meaning a single byte can hold values from **0 to 255** only.

2850 is larger than 255, so it simply cannot be represented using only 8 bits. You need at least 12 bits (2¹² = 4096 combinations, covering 0–4095) to store a value like 2850. That is why it must be split across **two bytes**.

---

## Q2. For value = 2850, show step-by-step what `value >> 8` and `value & 0xFF` give you.

**Step 1 — Convert 2850 to binary (12 bits):**

```
2850 in binary = 0000 1011 0010 0010
               = 0000 1011  |  0010 0010
                  high byte     low byte
```

**Step 2 — `high = value >> 8` (right-shift by 8 positions):**

```
2850 >> 8  →  drops the lower 8 bits, keeps the upper 8
           =  0000 1011  (in binary)
           =  11  (decimal)
```

**Step 3 — `low = value & 0xFF` (bitwise AND with 0xFF = 1111 1111):**

```
  0000 1011 0010 0010   (2850)
& 0000 0000 1111 1111   (0xFF = 255)
= 0000 0000 0010 0010   = 34 (decimal)
```

**Result:** `high = 11`, `low = 34` → matches the expected output in the task sheet.

---

## Q3. Explain what `(high << 8) | low` does during decoding. How does it reverse what `encode()` did?

During encoding, the original value was split by shifting bits and masking:

- `high` holds the upper 8 bits (bits 11–8 of the original value).
- `low` holds the lower 8 bits (bits 7–0).

Decoding reverses this in two steps:

1. **`high << 8`** — shifts `high` back to the left by 8 positions, restoring its bits to their original positions (bits 11–8). For `high = 11`: `11 << 8 = 2816`.

2. **`| low`** — the bitwise OR combines the shifted `high` with `low`. Since the upper 8 bits of `low` are all zeros (it was masked to 0–255), OR simply fills those empty lower 8 positions with `low`'s bits. `2816 | 34 = 2850`.

Together they rebuild the original 12-bit integer exactly as it was before encoding.

---

## Q4. What is the difference between a running average of the last 10 values and the total average of all values so far? Why does it matter for live data?

| | Running Average (last 10) | Overall Average (all values) |
|---|---|---|
| **Scope** | Only the most recent 10 readings | Every reading since start |
| **Sensitivity** | Reacts quickly to recent changes | Slow to reflect new trends |
| **Memory needed** | Constant (just 10 values) | Grows with time |

For live sensor data, the **running average matters more** for real-time alerting. If a sensor suddenly spikes, the overall average — diluted by hundreds of past normal readings — will barely move and miss the event. The running average, covering only the last 10 readings, will reflect that spike almost immediately, making it far more useful for triggering timely warnings. The overall average is better suited for a post-session summary or long-term trend analysis.

---

## Q5. Why use `queue.Queue` between threads instead of a plain Python list?

A plain Python `list` is **not thread-safe**. When two threads read and write to the same list at the same time, they can corrupt data or cause a crash — for example, one thread might read a partially updated index while another is mid-write.

`queue.Queue` solves this with **built-in locking**. It guarantees that only one thread accesses the internal data structure at a time, so:

- The sensor thread can `put()` items safely without clashing with the monitor thread's `get()`.
- `get(timeout=...)` lets the monitor thread **block and wait** for data rather than busy-looping.
- It naturally enforces a **producer–consumer** flow: the sensor produces, the monitor consumes, and the queue manages the ordering and synchronisation automatically.

Using a plain list would require writing your own lock logic (`threading.Lock`) around every read and write — `queue.Queue` handles all of that internally, making the code simpler and safer.

---
