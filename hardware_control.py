import time
from datetime import datetime
from config import pins, COMB, DATA_FILE
from utils import sensor_select, sensor_acquire_mean
from data_logging import write_csv_header, save_data_to_csv, rearrange_csv_columns

ACTIVE_LOW = {"pump"}  # Define which pins are active-low
def set_pins(state_map):
    """Set each pin state, accounting for active-low logic where needed."""
    for name, state in state_map.items():
        if name in ACTIVE_LOW:
            physical_state = 0 if state else 1  # Invert the signal
        else:
            physical_state = state
        pins[name].write(physical_state)

def setup_pins():
    """Initialize all pins to a safe default state."""
    try:
        set_pins({
            "pump": 0,
            "air_valve": 0,
            "sample_valve": 0,
            "chamber_valve": 0
        })
        print("All valves and pump set to closed/off.")
    except Exception as e:
        print(f"Error in setup_pins: {e}")
    finally:
        print("Pin setup completed.")



def clean_process(duration):
    """Run the air cleaning process for the given duration (seconds)."""
    print("Starting cleaning process...")
    if duration <= 0:
        print("Invalid duration for cleaning.")
        return
    try:
        set_pins({
            "air_valve": 1,
            "chamber_valve": 1,
            "pump": 1,
            "sample_valve": 0
        })
        time.sleep(duration)
    except Exception as e:
        print(f"Error during cleaning process: {e}")
    finally:
        set_pins({
            "pump": 0
        })
        print("Cleaning process completed.")

def vacuum_process(duration):
    """Run the vacuum process for the given duration (seconds)."""
    print("Starting vacuum process...")
    if duration <= 0:
        print("Invalid duration for vacuum.")
        return

    try:
        set_pins({
            "pump": 1,
            "air_valve": 0,
            "sample_valve": 0
        })
        time.sleep(duration)
    except Exception as e:
        print(f"Error during vacuum process: {e}")
    finally:
        set_pins({
            "pump": 0
        })
        print("Vacuum process completed.")

def sample_process(duration):
    """Collect samples from sensors and store them in CSV."""
    print("Starting sampling process...")
    try:
        set_pins({
            "pump": 0,
            "air_valve": 0,
            "sample_valve": 1,
            "chamber_valve": 1
        })

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

    except Exception as e:
        print(f"Error during sampling process: {e}")
    finally:
        rearrange_csv_columns(DATA_FILE)
        set_pins({
            "pump": 0,
        })

        print("Sampling process completed, valves and pump closed.")