import time
import csv, os
from datetime import datetime
from config import pins, COMB, DATA_FILE
from utils import sensor_select, sensor_acquire_mean

def setup_pins():
    # Set pin modes for the air valve, pump, and sample valve
    try:
        # Open air valve and pump, close sample valve
        pins["air_valve"].write(1)
        pins["pump"].write(1)
        pins["sample_valve"].write(0)  # Ensure sample valve is closed
    except Exception as e:
        print(f"An error occurred in setup pins: {e}")
    finally:
        print("Set up done")

def write_csv_header(file_path):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    """Initialize the CSV file with headers."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing the header row with the specified sensor data columns and timestamp
        header = ['Timestamp']

        # Define the column names directly
        sensor_labels = [
            'U1', 'U9', 'U2', 'U10', 'U3', 'U11', 'U4', 'U12',
            'U5', 'U13', 'U6', 'U14', 'U7', 'U15', 'U8', 'U16'
        ]

        # Add both A1 and A2 data columns for each sensor label
        for label in sensor_labels:
            header.append(f'{label}')

        writer.writerow(header)

def save_data_to_csv(sensor_data):
    """Save the sensor data row to the CSV file."""
    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(sensor_data)

def rearrange_csv_columns(file):
    """
    Rearranges the columns of an existing CSV file and saves the result to a new file.

    Args:
        file (str): Path to the input and output CSV file.
    """
    column_order = ['Timestamp'] + [f'U{i}' for i in range(1, 17)]
    try:
        # Read the input CSV file
        with open(file, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            data = list(reader)  # Load all rows into memory

            # Validate that all desired columns exist in the file
            missing_columns = [col for col in column_order if col not in reader.fieldnames]
            if missing_columns:
                raise ValueError(f"Missing columns in the input file: {missing_columns}")

            # Rearrange columns in the specified order
            with open(file, mode='w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=column_order)
                writer.writeheader()  # Write the new header
                for row in data:
                    # Write rows in the new column order
                    writer.writerow({col: row.get(col, 'N/A') for col in column_order})

        print(f"CSV columns rearranged and saved to '{file}'.")

    except Exception as e:
        print(f"Error processing the CSV file: {e}")


def clean_process(duration):
    """Run the cleaning process."""
    print("Starting cleaning process...")

    try:
        # Open air valve and pump, close sample valve
        pins["air_valve"].write(1)
        pins["pump"].write(1)
        pins["sample_valve"].write(0)  # Ensure sample valve is closed

        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(1)  # Wait 1 second per iteration

    except Exception as e:
        print(f"Error during cleaning process: {e}")

    finally:
        # Stop the cleaning process
        pins["pump"].write(0)
        pins["air_valve"].write(0)
        print("Cleaning process completed.")

def sample_process(duration):
    """Run the sample acquisition process and save data to CSV."""
    print("Starting sampling process...")

    # Open air valve, pump, and sample valve
    pins["air_valve"].write(1)
    pins["pump"].write(1)
    pins["sample_valve"].write(1)

    # Initialize CSV with headers
    write_csv_header(DATA_FILE)

    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            # Acquire data from each sensor in the comb
            sensor_data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]  # Timestamp
            for idx, comb in enumerate(COMB):
                sensor_select(comb)
                sensor_value_a1 = sensor_acquire_mean('OUT1', 1)
                sensor_value_a2 = sensor_acquire_mean('OUT2', 1)
                sensor_data.append(sensor_value_a1)
                sensor_data.append(sensor_value_a2)

            # Save data to CSV
            save_data_to_csv(sensor_data)
            time.sleep(0)  # Adjust sampling frequency as needed
        pins["pump"].write(1)
    except Exception as e:
        print(f"Error during sampling process: {e}")

    finally:
        rearrange_csv_columns(DATA_FILE)
        # Stop the sampling process
        pins["air_valve"].write(0)
        pins["pump"].write(0)
        pins["sample_valve"].write(0)
        print("Sampling process completed.")