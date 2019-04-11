import voluptuous as vol

from esphome import pins
import esphome.config_validation as cv
from esphome.const import CONF_ENABLE_TIME, CONF_ID, CONF_KEEP_ON_TIME, CONF_PIN
from esphome.cpp_generator import Pvariable, add
from esphome.cpp_helpers import gpio_output_pin_expression, register_component
from esphome.cpp_types import App, Component, esphome_ns

PowerSupplyComponent = esphome_ns.class_('PowerSupplyComponent', Component)

MULTI_CONF = True

CONFIG_SCHEMA = cv.Schema({
    vol.Required(CONF_ID): cv.declare_variable_id(PowerSupplyComponent),
    vol.Required(CONF_PIN): pins.gpio_output_pin_schema,
    vol.Optional(CONF_ENABLE_TIME): cv.positive_time_period_milliseconds,
    vol.Optional(CONF_KEEP_ON_TIME): cv.positive_time_period_milliseconds,
}).extend(cv.COMPONENT_SCHEMA)


def to_code(config):
    pin = yield gpio_output_pin_expression(config[CONF_PIN])

    rhs = App.make_power_supply(pin)
    psu = Pvariable(config[CONF_ID], rhs)
    if CONF_ENABLE_TIME in config:
        add(psu.set_enable_time(config[CONF_ENABLE_TIME]))
    if CONF_KEEP_ON_TIME in config:
        add(psu.set_keep_on_time(config[CONF_KEEP_ON_TIME]))

    register_component(psu, config)


BUILD_FLAGS = '-DUSE_OUTPUT'