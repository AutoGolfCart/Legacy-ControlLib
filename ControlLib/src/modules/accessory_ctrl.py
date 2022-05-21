import logging

# Drive Computer Core Library
# Accessory Controller Module
#
# This module controls the lights and horn.
#   - It also monitors the brake switch as that is normally considered 
#     a part of the accessory system (usually used to engage tail lights on braking)
#
# Hardware definition class to store messages for this module
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class Accessory_Controller:

    # Constructor
    #
    # can_address: CAN Address of the module

    def __int__(self):
        # CAN Address
        self.can_address = 2

        # Setup the message logging
        self.logger = logging.getLogger("accessory_controller")
        file_handler = logging.FileHandler("logs/accessory_ctrl.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(file_handler)

    # ----------------------------
    # Right Turn Signal
    # ----------------------------

    # Blink the Right Signal
    def right_signal_blink(self):
        self.logger.debug(f"Blink Right Signal")
        return f"({self.can_address}) 11 1 0 0 0 0 0 0"

    # Turn on the Right Signal
    def right_signal_on(self):
        self.logger.debug("Turn On Right Signal")
        return f"({self.can_address}) 10 1 1 0 0 0 0 0"

    # Turn off the Right Signal
    def right_signal_off(self):
        self.logger.debug("Turn Off Right Signal")
        return f"({self.can_address}) 10 1 2 0 0 0 0 0"

    # Request the Right Signal Setting
    def right_signal_get(self):
        self.logger.debug("Get Right Signal Setting")
        return f"({self.can_address}) 12 1 0 0 0 0 0 0"


    # ----------------------------
    # Left Turn Signal
    # ----------------------------

    # Blink the Left Signal
    def left_signal_blink(self):
        self.logger.debug(f"Blink Left Signal")
        return f"({self.can_address}) 11 2 0 0 0 0 0 0"

    # Turn on the Left Signal
    def left_signal_on(self):
        self.logger.debug("Turn On Left Signal")
        return f"({self.can_address}) 10 2 1 0 0 0 0 0"

    # Turn off the Left Signal
    def left_signal_off(self):
        self.logger.debug("Turn Off Left Signal")
        return f"({self.can_address}) 10 2 2 0 0 0 0 0"

    # Request the Left Signal Setting
    def left_signal_get(self):
        self.logger.debug("Get Left Signal Setting")
        return f"({self.can_address}) 12 2 0 0 0 0 0 0"


    # ----------------------------
    # Head Lights
    # ----------------------------

    # Blink the Head Lights
    def head_lights_blink(self):
        self.logger.debug(f"Blink Head Lights")
        return f"({self.can_address}) 11 3 0 0 0 0 0 0"

    # Turn on the Head Lights
    def head_lights_on(self):
        self.logger.debug("Turn On Head Lights")
        return f"({self.can_address}) 10 3 1 0 0 0 0 0"

    # Turn off the Head Lights
    def head_lights_off(self):
        self.logger.debug("Turn Off Head Lights")
        return f"({self.can_address}) 10 3 2 0 0 0 0 0"

    # Request the Head Light Setting
    def head_lights_get(self):
        self.logger.debug("Get Head Light Setting")
        return f"({self.can_address}) 12 3 0 0 0 0 0 0"


    # ----------------------------
    # Tail Lights
    # ----------------------------

    # Blink the Tail Lights
    def tail_lights_blink(self):
        self.logger.debug(f"Blink Tail Lights")
        return f"({self.can_address}) 11 4 0 0 0 0 0 0"

    # Turn on the Tail Lights
    def tail_lights_on(self):
        self.logger.debug("Turn On Tail Lights")
        return f"({self.can_address}) 10 4 1 0 0 0 0 0"

    # Turn off the Tail Lights
    def tail_lights_off(self):
        self.logger.debug("Turn Off Tail Lights")
        return f"({self.can_address}) 10 4 2 0 0 0 0 0"

    # Request the Tail Light Setting
    def tail_lights_get(self):
        self.logger.debug("Get Tail Light Setting")
        return f"({self.can_address}) 12 4 0 0 0 0 0 0"


    # ----------------------------
    # Horn
    # ----------------------------

    # Honk the Horn
    def horn_honk(self):
        self.logger.debug(f"Honk Horn")
        return f"({self.can_address}) 11 1 5 0 0 0 0 0"

    # Turn on the horn
    def horn_on(self):
        self.logger.debug("Turn on Horn")
        return f"({self.can_address}) 10 5 1 0 0 0 0 0"

    # Turn off the horn
    def horn_off(self):
        self.logger.debug("Turn Off Horn")
        return f"({self.can_address}) 10 5 2 0 0 0 0 0"

    # Request the horn status
    def horn_get(self):
        self.logger.debug("Get Horn Status")
        return f"({self.can_address}) 12 5 0 0 0 0 0 0"


    # ----------------------------
    # Rear Buzzer
    # ----------------------------

    # Turn on the Rear Buzzer
    def rear_buzz_on(self):
        self.logger.debug("Turning on Rear Buzzer")
        return f"({self.can_address}) 10 6 1 0 0 0 0 0"

    # Turn off the Rear Buzzer
    def ear_buzz_off(self):
        self.logger.debug("Turning Off Rear Buzzer")
        return f"({self.can_address}) 10 6 2 0 0 0 0 0"

    # Request the Rear Buzzer status
    def ear_buzz_get(self):
        self.logger.debug("Get Rear Buzzer Status")
        return f"({self.can_address}) 12 6 0 0 0 0 0 0"
