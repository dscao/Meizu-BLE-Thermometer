import esphome.codegen as cg
import esphome.config_validation as cv
from typing import Optional
from esphome.components import sensor, esp32_ble_client
from esphome.const import CONF_BATTERY_LEVEL, CONF_HUMIDITY, CONF_MAC_ADDRESS, CONF_TEMPERATURE, CONF_UPDATE_INTERVAL, \
    UNIT_CELSIUS, UNIT_VOLT, UNIT_PERCENT, CONF_ID, DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_BATTERY, \
    DEVICE_CLASS_VOLTAGE, STATE_CLASS_MEASUREMENT, ENTITY_CATEGORY_DIAGNOSTIC

DEPENDENCIES = ['esp32_ble_client']

meizu_ble_ns = cg.esphome_ns.namespace('meizu_ble')
MeizuBLE = meizu_ble_ns.class_('MeizuBLE', esp32_ble_client.ESPBTClientListener, cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MeizuBLE),
    cv.Required(CONF_MAC_ADDRESS): cv.mac_address,
    cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(unit_of_measurement=UNIT_CELSIUS,
                                                        accuracy_decimals=0,
                                                        device_class=DEVICE_CLASS_TEMPERATURE,
                                                        state_class=STATE_CLASS_MEASUREMENT,
                                                        ),
    cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(unit_of_measurement=UNIT_PERCENT,
                                                        accuracy_decimals=0,
                                                        device_class=DEVICE_CLASS_HUMIDITY,
                                                        state_class=STATE_CLASS_MEASUREMENT,
                                                        ),
    cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(unit_of_measurement=UNIT_VOLT,
                                                        accuracy_decimals=1,
                                                        device_class=DEVICE_CLASS_VOLTAGE,
                                                        state_class=STATE_CLASS_MEASUREMENT,
                                                        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
                                                        ),
    cv.Optional(CONF_UPDATE_INTERVAL, default='180s'): cv.positive_time_period_milliseconds,
}).extend(esp32_ble_client.ESP_BLE_DEVICE_SCHEMA).extend(cv.COMPONENT_SCHEMA)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield esp32_ble_client.register_ble_device(var, config)

    cg.add(var.set_address(config[CONF_MAC_ADDRESS].as_hex))
    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))

    if CONF_TEMPERATURE in config:
        sens = yield sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature(sens))
    if CONF_HUMIDITY in config:
        sens = yield sensor.new_sensor(config[CONF_HUMIDITY])
        cg.add(var.set_humidity(sens))
    if CONF_BATTERY_LEVEL in config:
        sens = yield sensor.new_sensor(config[CONF_BATTERY_LEVEL])
        cg.add(var.set_battery_level(sens))
