# Drive Computer Core Library
# Speed Controller Module
#
# This module controls the cart's built-in speed controller.
# Controls:
#   Acceleration
#   Fwd/Rev
#   Motor Control Enable
#
# Hardware definition class to store messages for this module
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class Drive_Controller:

    def __init__(self):
        # CAN Address
        self.can_address = 3

    def setAccelPos(self, pos):
        return f"({self.can_address}) 10 10 10 {pos} 0 0 0 0"

    def increment(self):
        return f"({self.can_address}) 11 10 1 0 0 0 0 0"

    def increment(self, count):
        return f"({self.can_address}) 11 10 1 {count} 0 0 0 0"

    def decrement(self):
        return f"({self.can_address}) 11 10 2 0 0 0 0 0"

    def decrement(self, count):
        return f"({self.can_address}) 11 10 2 {count} 0 0 0 0"

    def reqAccelPos(self):
        return f"({self.can_address}) 12 10 10 0 0 0 0 0"

    def enable(self):
        return f"({self.can_address}) 10 10 14 2 0 0 0 0"

    def disable(self):
        return f"({self.can_address}) 10 10 14 1 0 0 0 0"

    def reqEn(self):
        return f"({self.can_address}) 12 10 14 0 0 0 0 0"

    def reqPedalPos(self):
        return f"({self.can_address} 12 10 13 0 0 0 0 0"

    def reverse(self):
        return f"({self.can_address}) 10 13 2 0 0 0 0 0"

    def forwards(self):
        return f"({self.can_address}) 10 13 1 0 0 0 0 0"

    def reqDirection(self):
        return f"({self.can_address}) 10 12 0 0 0 0 0 0"
