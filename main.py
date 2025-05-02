# main.py
from hardware_control import setup_pins, clean_process, sample_process, vacuum_process
from config import CLEANING_DURATION, SAMPLING_DURATION, VACUUM_DURATION

if __name__ == "__main__":

    # Set up the Arduino pins
    setup_pins()

    # Perform cleaning process
    clean_process(CLEANING_DURATION)

    # Perform cleaning process
    vacuum_process(VACUUM_DURATION)

    # Perform sampling process
    sample_process(SAMPLING_DURATION)

    # Ensure the Arduino connection is properly closed
    #board.exit()
    print("Disconnected from Arduino.")
