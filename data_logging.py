import os, csv
from config import DATA_FILE

def write_csv_header(file_path):
    """Create the CSV file and write the header row in the required custom order."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    sensor_labels = [
        f'U{i}' for pair in zip(range(1, 9), range(9, 17)) for i in pair
    ]
    header = ['Timestamp'] + sensor_labels
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            file.flush()
    except Exception as e:
        print(f"Error writing CSV header: {e}")

def save_data_to_csv(sensor_data):
    """Append a row of sensor data to the CSV file."""
    try:
        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(sensor_data)
            file.flush()
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def rearrange_csv_columns(file_path):
    """Rearrange CSV columns to the specified order."""
    column_order = ['Timestamp'] + [f'U{i}' for i in range(1, 17)]
    try:
        with open(file_path, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            data = list(reader)
            missing = [col for col in column_order if col not in reader.fieldnames]
            if missing:
                raise ValueError(f"Missing columns: {missing}")

        with open(file_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=column_order)
            writer.writeheader()
            for row in data:
                writer.writerow({col: row.get(col, 'N/A') for col in column_order})
        print(f"Rearranged CSV columns saved to '{file_path}'.")
    except Exception as e:
        print(f"Error rearranging CSV: {e}")