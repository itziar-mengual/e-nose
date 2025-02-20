from pyfirmata import Arduino, util

# Arduino port configuration (ls /dev/tty.*)
ARDUINO_PORT = "/dev/cu.usbmodem14201"
BAUD_RATE = 9600

# Initialize Arduino board
board = Arduino(ARDUINO_PORT)

it = util.Iterator(board)
it.start()

# Timing configuration (in seconds)
CLEANING_DURATION = 5  # Duration for the cleaning process
SAMPLING_DURATION = 5  # Duration for the sampling process

# File paths
DATA_FILE = "data/data.csv"

# Sensor combination settings
COMB = [
    [0, 0, 0],  # U1, U9
    [0, 0, 1],  # U2, U10
    [0, 1, 0],  # U3, U11
    [0, 1, 1],  # U4, U12
    [1, 0, 0],  # U5, U13
    [1, 0, 1],  # U6, U14
    [1, 1, 0],  # U7, U15
    [1, 1, 1]   # U8, U16
]

# Define pins
pins = {
    "S0": board.get_pin('d:10:o'),  # Digital pin 10 for S0
    "S1": board.get_pin('d:11:o'),  # Digital pin 11 for S1
    "S2": board.get_pin('d:12:o'),  # Digital pin 12 for S2
    "OUT1": board.get_pin('a:1:i'), # Analog pin A1 for OUT1
    "OUT2": board.get_pin('a:2:i'), # Analog pin A2 for OUT2
    "air_valve": board.get_pin('d:13:o'),  # Digital pin 13 (air valve)
    "pump": board.get_pin('d:7:o'),         # Digital pin 7 (pump)
    "sample_valve": board.get_pin('d:6:o'), # Digital pin 6 (sample valve)
    "temp_sensor": board.get_pin('d:5:i')   # Digital pin 5 (temperature sensor)
}
