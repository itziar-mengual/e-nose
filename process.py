import time
import csv
from datetime import datetime
from pyfirmata import util
from config import board, AIR_VALVE_PIN, PUMP_PIN, SAMPLE_VALVE_PIN, CLEANING_DURATION, \
    SAMPLING_DURATION, COMB, DATA_FILE
from utils import sensor_select, sensor_acquire_mean

def setup_pins():
    # Set pin modes for the air valve, pump, and sample valve
    board.digital[AIR_VALVE_PIN].mode = 1  # Output mode
    board.digital[PUMP_PIN].mode = 1  # Output mode
    board.digital[SAMPLE_VALVE_PIN].mode = 1  # Output mode
    print("Set up done")

def write_csv_header(file_path):
    """Initialize the CSV file with headers."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing the header row with sensor data columns and timestamp
        header = ['Timestamp']
        for idx in range(len(COMB)):
            header.append(f'Sensor {idx + 1} (A1)')
            header.append(f'Sensor {idx + 1} (A2)')
        writer.writerow(header)

def save_data_to_csv(sensor_data):
    """Save the sensor data row to the CSV file."""
    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(sensor_data)

def clean_process(duration):
    """Run the cleaning process."""
    print("Starting cleaning process...")

    try:
        # Open air valve and pump, close sample valve
        board.digital[AIR_VALVE_PIN].write(1)
        board.digital[PUMP_PIN].write(1)
        board.digital[SAMPLE_VALVE_PIN].write(0)  # Ensure sample valve is closed

        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(1)  # Wait 1 second per iteration

    except Exception as e:
        print(f"Error during cleaning process: {e}")

    finally:
        # Stop the cleaning process
        board.digital[PUMP_PIN].write(0)
        board.digital[AIR_VALVE_PIN].write(0)
        print("Cleaning process completed.")

def sample_process(duration):
    """Run the sample acquisition process and save data to CSV."""
    print("Starting sampling process...")

    # Open air valve, pump, and sample valve
    board.digital[AIR_VALVE_PIN].write(1)
    board.digital[PUMP_PIN].write(1)
    board.digital[SAMPLE_VALVE_PIN].write(1)

    # Initialize CSV with headers
    write_csv_header(DATA_FILE)

    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            # Acquire data from each sensor in the comb
            sensor_data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]  # Timestamp
            for idx, comb in enumerate(COMB):
                sensor_select(board, comb)
                sensor_value_a1 = sensor_acquire_mean(board, 'OUT1', 1)
                sensor_value_a2 = sensor_acquire_mean(board, 'OUT2', 1)
                sensor_data.append(sensor_value_a1 if sensor_value_a1 is not None else 'N/A')
                sensor_data.append(sensor_value_a2 if sensor_value_a2 is not None else 'N/A')

            # Save data to CSV
            save_data_to_csv(sensor_data)
            time.sleep(1)  # Adjust sampling frequency as needed

    except Exception as e:
        print(f"Error during sampling process: {e}")

    finally:
        # Stop the sampling process
        board.digital[PUMP_PIN].write(0)
        board.digital[AIR_VALVE_PIN].write(0)
        board.digital[SAMPLE_VALVE_PIN].write(0)
        print("Sampling process completed.")