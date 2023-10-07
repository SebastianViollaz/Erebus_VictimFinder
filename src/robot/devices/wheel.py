# Controlls a wheel
class Wheel:
    """Represent a wheel for the robot
    Parameters:
    wheel: datatype provied from Erebus's robot
    maxVElocity: Max velcity for the wheel
        """

    def __init__(self, wheel, maxVelocity):

        self.maxVelocity = maxVelocity
        self.wheel = wheel
        self.velocity = 0
        self.wheel.setPosition(float("inf"))
        self.wheel.setVelocity(0)

    def move(self, ratio):
        """Moves the wheel at a ratio of the maximum speed (between 0 and 1)
        """
        ratio = max(-1, min(1, ratio))
        self.velocity = ratio * self.maxVelocity
        self.wheel.setVelocity(self.velocity)