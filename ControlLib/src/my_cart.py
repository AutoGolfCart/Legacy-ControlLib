import threading
import logging
import time
import json
import sys

from numpy import abs

from ControlLib.ControlLib.src.util.util import to_color

from ControlLib.ControlLib.src.can_adapter import CAN_Adapter
import ControlLib.ControlLib.src.can_adapter as can_util

from ControlLib.ControlLib.src.modules.accessory_ctrl import Accessory_Controller
from ControlLib.ControlLib.src.modules.direction_ctrl import Direction_Controller
from ControlLib.ControlLib.src.modules.drive_ctrl import Drive_Controller

# Drive Computer Core Library
# Cart Control
#
# Class to control the cart's drive hardware
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class MyCart:

    def __init__(self, json_config_path):
        try:
            # Config
            self.config = json.load(open(json_config_path))
        
        except:
            print(to_color("FATAL: Cannot Find MyCart Config JSON", "red"))
            sys.exit(0)


        if self.config["log"]:
            # Setup the message logging
            self.logger = logging.getLogger("drive_hardware_manager")
            self.logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(self.config["logging_path"] + "/drive_hardware_manager.log")
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(threadName)s - %(message)s"))
            self.logger.addHandler(file_handler)

        # Internal Hardware
        self.can = CAN_Adapter(serial_port=self.config["can_adapter_port"], baud=int(self.config["can_adapter_baud"]), log=True, log_path=self.config["logging_path"])
        self.can.send_string("Hello!")

        # Modules
        self.direction_controller = Direction_Controller()
        self.accessory_controller = Accessory_Controller()
        self.drive_controller = Drive_Controller()

        # Sub-Threads 
        self.listener = threading.Thread(target=self.listen, name="message_listener", daemon=True)   # Start Message RX Processing
        
        # System Vars
        self.vars = {
            "accel_pos": 0,
            "accel_enable": 0,
            "direction": 0, # 0 Forwards, 1 Reverse
            "accel_pedal_sw": 0, 
            "accel_pedal_pos": 0,
            "right_signal": 0,
            "left_signal": 0,
            "head_light": 0,
            "tail_light": 0,
            "horn": 0,
            "buzzer": 0,
            "steering_motor_en": 0,
            "steering_motor_direc": 0,
            "steering_motor_pwm": 0,
            "steering_wheel": 0, # 1 No Change, 2 Left, 3 Right
            "steering_pos": 0,
            "brake_motor_en": 0,
            "brake_motor_direc": 0,
            "brake_motor_pwm": 0,
            "brake_pos": 0,
            "brake_pedal": 0

        }

        # Init Message
        self.logger.info("Hardware Manager Initialization Preparation Complete")
        

    def intialize(self):
        # Init Message
        self.logger.info("Initializing Hardware Manager")

        # Starting listener thread
        self.listener.start()

        # Init Message
        self.logger.info("Hardware Manager Initialization Complete")


    # ----------------------------
    # Threads
    # ----------------------------

    # Listen for messages
    def listen(self):
        self.logger.info("CAN Listener Thread Starting")
        
        # Main loop
        while True:
            message = self.can.read()

            if message != "":
                message_id = can_util.getID()
                message = can_util.removeID(message=message).split(" ")

                if message[0] == "12" and message[1] == "12": # Is a data response message
                    if message_id == "3": # Message from drive controller
                        if message[2] == "10":
                            if message[3] == "10":
                                self.vars["accel_pos"] = int(message[7])
                            elif message[3] == "13":
                                self.vars["accel_pedal_pos"] = int(message[7])
                            elif message[3] == "15":
                                self.vars["accel_enable"] = can_util.canbool(int(message[7]))
                        elif message[2] == "13":
                            self.vars["direction"] = can_util.canbool(int(message[7]))
                        elif message[2] == "15":
                            self.vars["accel_pedal_sw"] = can_util.canbool(int(message[7]))
                        elif message[2] == "12":
                            if message_id == "3":
                                self.vars["accel_enable"] = can_util.canbool(int(message[3]))
                                self.vars["direction"] = can_util.canbool(int(message[4]))
                                self.vars["accel_pos"] = int(message[5])
                                self.vars["accel_pedal_pos"] = int(message[6])
                                self.vars["accel_pedal_sw"] = can_util.canbool(int(message[7]))

                    elif message_id == "2":
                        if message[2] == "10":
                            if message[3] == "1":
                                self.vars["right_signal"] = can_util.canbool(int(message[7]))
                            elif message[3] == "2":
                                self.vars["left_signal"] = can_util.canbool(int(message[7]))
                            elif message[3] == "3":
                                self.vars["head_light"] = can_util.canbool(int(message[7]))
                            elif message[3] == "4":
                                self.vars["tail_light"] = can_util.canbool(int(message[7]))
                            elif message[3] == "5":
                                self.vars["horn"] = can_util.canbool(int(message[7]))
                            elif message[3] == "6":
                                self.vars["buzzer"] = can_util.canbool(int(message[7]))
                        elif message[2] == "15":
                            self.vars["brake_pedal"] = can_util.canbool(int(message[7]))
                        elif message[2] == "12":
                            if message[3] == "1":
                                self.vars["right_signal"] = can_util.canbool(int(message[4]))
                                self.vars["left_signal"] = can_util.canbool(int(message[5]))
                                self.vars["head_light"] = can_util.canbool(int(message[6]))
                                self.vars["tail_light"] = can_util.canbool(int(message[7]))

                            elif message[3] == "2":
                                self.vars["horn"] = can_util.canbool(int(message[4]))
                                self.vars["buzzer"] = can_util.canbool(int(message[5]))

                            elif message[3] == "3":
                                self.vars["brake_pedal"] = can_util.canbool(int(message[4]))

                    elif message_id == "1":
                        if message[2] == "1":
                            if message[3] == "10":
                                self.vars["steering_motor_en"] = can_util.canbool(int(message[7]))
                            elif message[3] == "15":
                                self.vars["steering_wheel"] = int(message[7])
                            elif message[3] == "16":
                                self.vars["steering_pos"] = int(message[7])
                        elif message[2] == "2":
                            if message[3] == "10":
                                self.vars["brake_motor_en"] = can_util.canbool(int(message[7]))
                            elif message[3] == "16":
                                self.vars["brake_pos"] = int(message[7])
                        elif message[2] == "12":
                            if message[3] == "1":
                                self.vars["steering_motor_en"] = can_util.canbool(int(message[4]))
                                self.vars["steering_motor_direc"] = can_util.canbool(int(message[5]))
                                self.vars["steering_motor_pwm"] = can_util.canbool(int(message[6]))
                                self.vars["steering_pos"] = int(message[7])

                            elif message[3] == "2":
                                self.vars["brake_motor_en"] = can_util.canbool(int(message[4]))
                                self.vars["brake_motor_direc"] = can_util.canbool(int(message[5]))
                                self.vars["brake_motor_pwm"] = can_util.canbool(int(message[6]))
                                self.vars["brake_pos"] = int(message[7])


    # ----------------------------
    # Wheel
    # ----------------------------

    # Turn left
    def turnLeft(self, power = 128):
        if power == 0:
            if self.vars["steering_motor_en"] == 1:
                self.can.write(self.direction_controller.str_disable())

        else:
            self.can.write(self.direction_controller.str_left(power))

            if self.vars["steering_motor_en"] == 0:
                time.sleep(.1)
                self.can.write(self.direction_controller.str_enable())

    # Turn right
    def turnRight(self, power = 128):
        if power == 0:
            if self.vars["steering_motor_en"] == 1:
                self.can.write(self.direction_controller.str_disable())

        else:
            self.can.write(self.direction_controller.str_right(power))

            if self.vars["steering_motor_en"] == 0:
                time.sleep(.1)
                self.can.write(self.direction_controller.str_enable())

    def stopTurn(self):
        self.can.write(self.direction_controller.str_disable())

    # Run to positon
    def turnToPos(self, position, power = 128):
        if abs(self.vars["steering_pos"] - position) > 500 and not (position < 600 and position > 400):
            if (self.vars["steering_pos"] - position < 0):
                self.leftSignal()
            else:
                self.rightSignal()

        self.can.write(self.direction_controller.str_goTo(position, power))

        if self.vars["steering_motor_en"] != 1:
            time.sleep(.1)
            self.can.write(self.direction_controller.str_enable())

    # ----------------------------
    # Accel
    # ----------------------------

    # Enagage Brakes NOTE: Not recommended, use completestop instead
    def brake(self):
        # Disable the accelerator
        self.can.write(self.drive_controller.disable())
        time.sleep(.1)
        self.setSpeed(0)
        time.sleep(.1)
        
        # Brake
        self.can.write(self.direction_controller.brk_pull())
        time.sleep(.1)
        self.can.write(self.direction_controller.brk_enable())

    # Disengages brakes
    def disengageBrakes(self):
        self.can.write(self.direction_controller.brk_push())
        time.sleep(.1)
        self.can.write(self.direction_controller.brk_enable())

    # Come to a complete stop
    def completeStop(self):
        self.brake()
        time.sleep(15)

    # Set the accelerator speed
    def setSpeed(self, speed: int = 200):
        # Scale
        if (speed < 0):
                speed = 0
        elif (speed > 255):
                speed = 255

        if speed == 0:
            self.can.write(self.drive_controller.disable())

        self.can.write(self.drive_controller.setAccelPos(speed))

    # Enable the Accelerator
    def enableAccelerator(self):
        self.can.write(self.drive_controller.enable())

    # Disable the Accelerator
    def disableAccelerator(self):
        self.can.write(self.drive_controller.disable())

    # Increment the accelerator
    def incAccel(self, count = 0):
        self.can.write(self.drive_controller.increment(count))

    # Decrement the accelerator
    def decAccel(self, count = 0):
        self.can.write(self.drive_controller.decrement(count))


    # ----------------------------
    # Direction
    # ----------------------------

    # Set the direction to forwards
    def forwards(self):
        if (self.vars["direction"] == 0):
            return

        # Come to a complete stop for hardware protection
        self.completeStop()
        
        # Change mode
        self.can.write(self.drive_controller.forwards())
        time.sleep(.1)

        # Disengage brake pull
        self.disengageBrakes()

    # Set the direction to reverse
    def reverse(self):
        if (self.vars["direction"] == 1):
            return

        # Come to a complete stop for hardware protection
        self.completeStop()

        # Change mode
        self.can.write(self.drive_controller.reverse())
        time.sleep(.1)

        # Disengage brake pull
        self.disengageBrakes()

    # ----------------------------
    # Turn Signals
    # ----------------------------

    # Blink the right signal
    def rightSignal(self):
        if self.vars["right_signal"] == 0:
            self.can.write(self.accessory_controller.right_signal_blink())

        else:
            self.can.write(self.accessory_controller.right_signal_off())

    # Blink the left signal
    def leftSignal(self):
        if self.vars["left_signal"] == 0:
            self.can.write(self.accessory_controller.left_signal_blink())

        else:
            self.can.write(self.accessory_controller.left_signal_off())
        
    # Stop signalling
    def stopSignal(self):
        self.can.write(self.accessory_controller.left_signal_off())
        time.sleep(.1)
        self.can.write(self.accessory_controller.right_signal_off())

    # Hazards 
    def hazards(self):
        if self.vars["tail_light"] == 0:
            self.can.write(self.accessory_controller.tail_lights_blink())

        else:
            self.can.write(self.accessory_controller.tail_lights_off())

    # Stop hazards
    def stopHazards(self):
        self.can.write(self.accessory_controller.tail_lights_off())

    # ----------------------------
    # Horn
    # ----------------------------

    def honk(self):
        self.can.write(self.accessory_controller.horn_honk())

