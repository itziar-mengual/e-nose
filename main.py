# main.py
from process import setup_pins, clean_process, sample_process, board
from config import CLEANING_DURATION, SAMPLING_DURATION, pins

if __name__ == "__main__":
    # Set up the Arduino pins
    setup_pins()

    # Perform cleaning process
    clean_process(CLEANING_DURATION)
    print(f"OUT1 read: {pins['OUT1'].read()}")
    print(f"OUT2 read: {pins['OUT2'].read()}")
    # Perform sampling process
    sample_process(SAMPLING_DURATION)

    # Ensure the Arduino connection is properly closed
    board.exit()
    print("Disconnected from Arduino.")
