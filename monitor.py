"""
monitor.py
Part 2 - Real-Time Monitor (2 Threads)
Internship Assessment Task: Python Development
MyUpsideDownLab LLP
"""

import random
import queue
import threading
import collections
import time


# ── Shared state ─────────────────────────────────────────────────────────────
data_queue      = queue.Queue()          # thread-safe channel between threads
stop_event      = threading.Event()      # signals both threads to shut down

# Counters shared between threads (protected by a lock for safe writes)
stats_lock           = threading.Lock()
total_received       = 0
overall_sum          = 0.0
threshold_warnings   = 0

UPPER_THRESHOLD = 3000
LOWER_THRESHOLD = 500
DURATION_SEC    = 20     # how long the simulation runs


# ── Encode / Decode helpers (same logic as encode_decode.py) ─────────────────
def encode(value: int) -> tuple[int, int]:
    high = value >> 8
    low  = value & 0xFF
    return high, low


def decode(high: int, low: int) -> int:
    return (high << 8) | low


# ── Thread 1 : Sensor ────────────────────────────────────────────────────────
def sensor_thread():
    """
    Generates a random sensor value every 100 ms, encodes it to (high, low),
    and puts the pair into the shared queue.
    Stops when stop_event is set.
    """
    while not stop_event.is_set():
        raw_value   = random.randint(0, 4095)
        high, low   = encode(raw_value)
        data_queue.put((high, low))
        time.sleep(0.1)          # 100 ms sampling interval


# ── Thread 2 : Monitor ───────────────────────────────────────────────────────
def monitor_thread():
    """
    Reads (high, low) pairs from the queue, decodes them,
    maintains a running average of the last 10 values,
    and prints a warning if the running average crosses thresholds.
    Stops when stop_event is set AND the queue is drained.
    """
    global total_received, overall_sum, threshold_warnings

    window = collections.deque(maxlen=10)   # automatically drops oldest entry

    while not stop_event.is_set() or not data_queue.empty():
        try:
            high, low = data_queue.get(timeout=0.2)
        except queue.Empty:
            continue

        value = decode(high, low)

        # Update shared statistics safely
        with stats_lock:
            total_received += 1
            overall_sum    += value

        # Update the sliding window and compute running average
        window.append(value)
        running_avg = sum(window) / len(window)

        if running_avg > UPPER_THRESHOLD:
            with stats_lock:
                threshold_warnings += 1
            print(f"WARNING: Running avg = {running_avg:.1f} - too high!")

        elif running_avg < LOWER_THRESHOLD:
            with stats_lock:
                threshold_warnings += 1
            print(f"WARNING: Running avg = {running_avg:.1f} - too low!")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Real-Time Sensor Monitor — starting …")
    print(f"  Duration : {DURATION_SEC} s  |  Sample rate : 100 ms")
    print(f"  Thresholds : < {LOWER_THRESHOLD} (low)  /  > {UPPER_THRESHOLD} (high)")
    print("=" * 50)

    t_sensor  = threading.Thread(target=sensor_thread,  daemon=True, name="Sensor")
    t_monitor = threading.Thread(target=monitor_thread, daemon=True, name="Monitor")

    t_sensor.start()
    t_monitor.start()

    # Run for the configured duration, then signal threads to stop
    time.sleep(DURATION_SEC)
    stop_event.set()

    # Wait for both threads to finish cleanly
    t_sensor.join(timeout=2)
    t_monitor.join(timeout=2)

    # Final summary
    with stats_lock:
        received  = total_received
        warnings  = threshold_warnings
        overall   = overall_sum / received if received else 0.0

    print("\n" + "=" * 50)
    print("  Simulation complete.")
    print(f"  Total values received : {received}")
    print(f"  Overall average       : {overall:.1f}")
    print(f"  Threshold warnings    : {warnings}")
    print("=" * 50)


if __name__ == "__main__":
    main()
