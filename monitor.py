import random
import queue
import threading
import collections
import time


data_queue      = queue.Queue()         
stop_event      = threading.Event()      


stats_lock           = threading.Lock()
total_received       = 0
overall_sum          = 0.0
threshold_warnings   = 0

UPPER_THRESHOLD = 3000
LOWER_THRESHOLD = 500
DURATION_SEC    = 20    


def encode(value: int) -> tuple[int, int]:
    high = value >> 8
    low  = value & 0xFF
    return high, low


def decode(high: int, low: int) -> int:
    return (high << 8) | low


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
        time.sleep(0.1)         


def monitor_thread():
    global total_received, overall_sum, threshold_warnings

    window = collections.deque(maxlen=10)   

    while not stop_event.is_set() or not data_queue.empty():
        try:
            high, low = data_queue.get(timeout=0.2)
        except queue.Empty:
            continue

        value = decode(high, low)

        with stats_lock:
            total_received += 1
            overall_sum    += value

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

    time.sleep(DURATION_SEC)
    stop_event.set()

    t_sensor.join(timeout=2)
    t_monitor.join(timeout=2)

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
