import time
from datetime import datetime
from config import pins, COMB, DATA_FILE
from utils import sensor_select, sensor_acquire_mean
from data_logging import write_csv_header, save_data_to_csv, rearrange_csv_columns

def setup_pins():
    """Initialize all pins to a safe default state."""
    try:
        for name in ["air_valve", "pump", "sample_valve", "chamber_valve"]:
            pins[name].write(0)
        print("All valves and pump set to closed/off.")
    except Exception as e:
        print(f"Error in setup_pins: {e}")
    finally:
        print("Pin setup completed.")

def clean_process(duration):
    """Run the air cleaning process for the given duration (seconds)."""
    print("Starting cleaning process...")
    try:
        for name in ["air_valve", "chamber_valve", "pump", "sample_valve"]:
            pins[name].write(1)
        time.sleep(duration)
    except Exception as e:
        print(f"Error during cleaning process: {e}")
    finally:
        for name in ["pump", "air_valve", "sample_valve", "chamber_valve"]:
            pins[name].write(0)
        print("Cleaning process completed.")

def vacuum_process(duration):
    """Run the vacuum process for the given duration (seconds)."""
    print("Starting vacuum process...")
    try:
        pins["chamber_valve"].write(0)
        pins["pump"].write(1)
        time.sleep(duration)
    except Exception as e:
        print(f"Error during vacuum process: {e}")
    finally:
        pins["pump"].write(0)
        print("Vacuum process completed.")

def sample_process(duration):
    """Collect samples from sensors and store them in CSV."""
    print("Starting sampling process...")
    try:
        pins["air_valve"].write(0)
        pins["pump"].write(0)
        pins["sample_valve"].write(1)
        pins["chamber_valve"].write(1)

        write_csv_header(DATA_FILE)
        start_time = time.time()

        while time.time() - start_time < duration:
            sensor_data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            for comb in COMB:
                sensor_select(comb)
                val1 = sensor_acquire_mean('OUT1', 1)
                val2 = sensor_acquire_mean('OUT2', 1)
                sensor_data.append(val1)
                sensor_data.append(val2)
            save_data_to_csv(sensor_data)

        pins["pump"].write(1)  # Optional: keep pump on after sampling
    except Exception as e:
        print(f"Error during sampling process: {e}")
    finally:
        rearrange_csv_columns(DATA_FILE)
        for name in ["air_valve", "chamber_valve", "pump", "sample_valve"]:
            pins[name].write(0)
        print("Sampling process completed, valves and pump closed.")