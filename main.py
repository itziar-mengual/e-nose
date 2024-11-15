# main.py
from config import board, pins, calibrate_shutter
from utils import sensor_select, sensor_acquire_mean
import time

if __name__ == "__main__":
    calibrate_shutter()
    
    # Simple connection check to test air valve, pump, and sample valve
    try:
        print("Testing air valve and pump...")
        pins['air_valve'].write(1)
        pins['pump'].write(1)
        time.sleep(10)
        pins['pump'].write(0)
        pins['air_valve'].write(0)
        time.sleep(5)
        
        print("Testing sample valve and pump...")
        pins['sample_valve'].write(1)
        pins['pump'].write(1)
        time.sleep(10)
        pins['pump'].write(0)
        pins['sample_valve'].write(0)
    
    except KeyboardInterrupt:
        print("Process interrupted.")
    
    finally:
        board.exit()
        print("Arduino connection closed.")
