input_boolean = data.get("input_boolean")
light_id = data.get("light_id")
delta = data.get("delta")
attribute_id = data.get("light_attribute", "brightness")
delay = data.get("delay", 150)

attribute_mapping = {
    "brightness": {"min": 1, "max": 255},
    "color_temp_kelvin": {"min": 153, "max": 500},
}

exit_service = False
while True:
    switch_input = hass.states.get(input_boolean).state
    if switch_input == "off":
        break
    light = hass.states.get(light_id)

    attr_value = light.attributes[attribute_id]
    attr_value = attr_value + delta
    if attr_value < attribute_mapping[attribute_id]["min"]:
        attr_value = attribute_mapping[attribute_id]["min"]
        exit_service = True
    elif attr_value > attribute_mapping[attribute_id]["max"]:
        attr_value = attribute_mapping[attribute_id]["max"]
        exit_service = True

    service_data = {"entity_id": light_id, attribute_id: attr_value}
    # logger.warning(f"Service data: {service_data}")
    hass.services.call("light", "turn_on", service_data)
    if exit_service:
        break
    time.sleep(delay / 1000)
