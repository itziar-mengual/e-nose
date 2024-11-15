from pyfirmata import Arduino

# Arduino port configuration
ARDUINO_PORT = "/dev/cu.usbmodem14101"
BAUD_RATE = 9600

# Initialize Arduino board
board = Arduino(ARDUINO_PORT)

# Pin configuration
AIR_VALVE_PIN = 'D13'
PUMP_PIN = 'D7'
SAMPLE_VALVE_PIN = 'D6'

# Timing configuration (in seconds)
CLEANING_DURATION = 120  # Duration for the cleaning process
SAMPLING_DURATION = 50  # Duration for the sampling process

# Sensor combination settings
COMB = [
    [0, 0, 0],  # U1, U9
    [0, 0, 1],  # U2, U10
    [0, 1, 0],  # U3, U10
    [0, 1, 1],  # U4, U11
    [1, 0, 0],  # U5, U12
    [1, 0, 1],  # U6, U13
    [1, 1, 0],  # U7, U14
    [1, 1, 1]   # U8, U15
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
# File paths
DATA_FILE = "data.csv"