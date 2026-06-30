# config.py
# This file holds every fixed number the simulation needs.
# Nothing here changes while the program runs — these are settings, not calculations.

# --- Temperature (Celsius) ---
TEMP_DANGER_LOW = 10
TEMP_SAFE_LOW = 15
TEMP_TARGET = 25
TEMP_SAFE_HIGH = 38
TEMP_DANGER_HIGH = 50

# --- Temperature physics constants ---
K_AMBIENT_T = 0.001
K_HEATER = 0.2
K_FAN_T = 0.5
K_LIGHT_T = 0.02

# --- Humidity (%) ---
HUM_DANGER_LOW = 20
HUM_SAFE_LOW = 30
HUM_TARGET = 70
HUM_SAFE_HIGH = 80
HUM_DANGER_HIGH = 85

# --- Humidity physics constants ---
K_AMBIENT_H = 0.001
K_HEATER_H = 0.2
K_FAN_H = 0.5
K_LIGHT_H = 0.2

# --- CO2 (ppm) ---
CO2_DANGER_LOW = 300
CO2_SAFE_LOW = 350
CO2_TARGET = 450
CO2_SAFE_HIGH = 1000
CO2_DANGER_HIGH = 1200

# --- CO2 physics constants ---
# K_FAN_C must be LARGER than ANIMAL_CO2_OUTPUT, otherwise the fan can never
# bring CO2 back down — it would only ever rise. With the fan on, net effect
# per step = ANIMAL_CO2_OUTPUT - K_FAN_C = 0.02 - 0.05 = -0.03 (CO2 falls).
# With the fan off, only ANIMAL_CO2_OUTPUT applies (CO2 rises).
ANIMAL_CO2_OUTPUT = 0.02
K_FAN_C = 0.05

# --- Ambient room conditions (what temp/humidity drift toward when idle) ---
AMBIENT_TEMP = 22
AMBIENT_HUMIDITY = 40

# --- Episode structure ---
MAX_STEPS_PER_EPISODE = 1000   # truncation limit; one "episode" = this many steps

# --- Reward weights ---
W_SWITCH = 0.5      # penalty per actuator that changes state this step
W_DANGER = 50        # large penalty if any variable crosses into a danger zone