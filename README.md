# Arduino Sensor Control and Data Acquisition

This project provides a Python-based control system for managing an Arduino-powered sensor array. It automates cleaning, vacuum, and sampling processes with precise timing, controls multiple valves and a pump, and logs sensor data into a structured CSV file for further analysis.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware Setup](#hardware-setup)
- [Software Setup](#software-setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Functionality Details](#functionality-details)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The system connects to an Arduino board via USB using the `pyfirmata` Python library. It controls valves and pumps through digital pins and reads analog sensor values. The workflow includes three main phases:

1. **Cleaning Process:** Opens air and chamber valves and activates the pump to clean the sensor environment.
2. **Vacuum Process:** Activates the pump to create a vacuum state in the sensor chamber.
3. **Sampling Process:** Selects sensor combinations, acquires analog readings, and logs them with timestamps into a CSV file.

---

## Features

- Automated control of valves and pump via Arduino pins
- Configurable durations for cleaning, vacuum, and sampling
- Selection of sensor combinations via digital pins
- Analog sensor data acquisition and averaging
- Robust CSV logging with header management and column reordering
- Safe pin setup and cleanup
- Error handling and status messages for easier debugging

---

## Hardware Setup

- **Arduino board** connected via USB (e.g., Arduino Uno, Mega).
- Digital pins:
  - S0: Digital pin 10 (output)
  - S1: Digital pin 11 (output)
  - S2: Digital pin 12 (output)
  - Pump: Digital pin 4 (output, active-low)
  - Air Valve: Digital pin 6 (output)
  - Sample Valve: Digital pin 5 (output)
  - Chamber Valve: Digital pin 7 (output)
- Analog pins:
  - OUT1: Analog pin A1 (input)
  - OUT2: Analog pin A2 (input)
- Ensure the sensor array and valves are connected accordingly.

---

## Software Setup

### Prerequisites

- Python 3.x
- `pyfirmata` library
- Arduino IDE (for initial board setup, if needed)

### Install dependencies

```bash
pip install pyfirmata
```

# Configure Arduino Port
Modify the ARDUINO_PORT variable in config.py to match your system's Arduino port.

- On Windows, it might be like `COM3`
- On macOS/Linux, it could be `/dev/tty.usbmodemXXXX` or `/dev/ttyACM0`
Use `ls /dev/tty.*` or device manager to find the correct port.

# Usage
Run the main control script:

```bash
python main.py
```

This will:
1. Initialize pins and Arduino connection
2. Run the cleaning process for the configured duration
3. Run the vacuum process
4. Run the sampling process, collecting sensor data
5. Save sensor data to `data/data.csv`
6. Close Arduino connection gracefully

# Configuration
Modify parameters in `config.py`:
- `CLEANING_DURATION`: Duration in seconds for cleaning (default: 5)
- `VACUUM_DURATION`: Duration in seconds for vacuuming (default: 5)
- `SAMPLING_DURATION`: Duration in seconds for sampling (default: 5)
- `ARDUINO_PORT`: USB port where the Arduino is connected
- `pins`: Mapping of Arduino pins to functional names

# File Structure
`main.py` — Main program that runs the entire process

`config.py` — Hardware and timing configurations

`hardware_control.py` — Functions controlling hardware states and processes

`utils.py` — Utility functions for sensor selection and data acquisition

`data_logging.py` — CSV header management and data saving

`data/` — Folder where sensor CSV data is stored

# Author
Itziar Mengual, 2025