# utils.py
from config import pins
import time

def sensor_select(combination):
    """Select sensor using digital pins S0, S1, S2."""
    print(f"Selecting sensor with combination: {combination}")
    try:
        pins['S0'].write(combination[0])
        pins['S1'].write(combination[1])
        pins['S2'].write(combination[2])
    except Exception as e:
        print(f"Error in sensor_select: {e}")
        raise

def sensor_acquire_mean(pin_name, interval):
    """Acquire mean value from the specified sensor pin over an interval."""
    if pin_name not in pins:
        raise ValueError(f"Pin {pin_name} not configured.")

    sensor_pin = pins[pin_name]
    readings = []

    for i in range(interval):
        try:
            reading = sensor_pin.read()
            readings.append(reading)
        except Exception as e:
            print(f"Error during read: {e}")

        time.sleep(0.1)

    valid_readings = [r for r in readings if r is not None]
    print(f"Valid readings: {valid_readings}")
    return sum(valid_readings) / len(valid_readings) if valid_readings else None
