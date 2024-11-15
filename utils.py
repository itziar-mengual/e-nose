# utils.py
from config import board, pins
import time

def sensor_select(combination):
    """Select sensor using digital pins S0, S1, S2."""
    pins['S0'].write(combination[0])
    pins['S1'].write(combination[1])
    pins['S2'].write(combination[2])

def sensor_acquire_mean(pin_name, interval=5):
    """Acquire mean value from the specified sensor pin over an interval."""
    if pin_name not in pins:
        raise ValueError(f"Pin {pin_name} not configured.")
    
    sensor_pin = pins[pin_name]
    readings = []
    
    for _ in range(interval):
        readings.append(sensor_pin.read())
        time.sleep(0.1)  # Adjust sample delay if needed
    
    # Remove None values that could come from `read()` returning None initially
    valid_readings = [r for r in readings if r is not None]
    return sum(valid_readings) / len(valid_readings) if valid_readings else None
