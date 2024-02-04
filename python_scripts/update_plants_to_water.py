# Constants
HYSTERESIS = 10
UNKNOWN_STATES = ['unknown', 'unavailable']

# Get all sensors objects that are moisture sensors (start with sensor.ble_moisture_)
moisture_sensors = [sensor for sensor in hass.states.all() if sensor.entity_id.startswith('sensor.ble_moisture_')]

plants_to_water = hass.states.get('input_text.plants_to_water')
if plants_to_water is None:
    plants_to_water = ''
else:
    plants_to_water = plants_to_water.state.split(', ')

# Get low threshold for moisture
try:
    low_threshold = float(hass.states.get('input_number.moisture_low_threshold').state)
except ValueError:
    logger.error('input_number.moisture_low_threshold is not a number: %s', hass.states.get('input_number.moisture_low_threshold').state)
    # Set default value
    low_threshold = 50

# For testing purposes
# low_threshold = 101

# Loop through all moisture sensors and check if they need water
for sensor in moisture_sensors:
    # Get plant moisture level
    plant_moisture_str = sensor.state
    if plant_moisture_str in UNKNOWN_STATES:
        continue
    try:
        moisture_level = float(plant_moisture_str)
    except ValueError:
        logger.error('Moisture level is not a number: %s', plant_moisture_str)
        continue

    # Get plant friendly name
    plant_name = sensor.attributes.get('friendly_name', sensor.entity_id)

    # Check if the plant needs water
    if moisture_level < low_threshold and plant_name not in plants_to_water:
        plants_to_water.append(plant_name)
    elif moisture_level > low_threshold + HYSTERESIS and plant_name in plants_to_water:
        plants_to_water.remove(plant_name)

plants_to_water = ', '.join(plants_to_water).lstrip(', ')

hass.states.set('input_text.plants_to_water', plants_to_water)
