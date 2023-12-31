from abc import ABC

class Sensor(ABC):
    def __init__(self, webots_device, time_step):
        self.time_step = time_step
        self.device = webots_device
        self.device.enable(time_step)

    #AbstractMethonFor
    def update(self):
        pass

class TimedSensor(Sensor):
    def __init__(self, webots_device, time_step, step_counter):
        super().__init__(webots_device, time_step)
        self.step_counter = step_counter

    def update(self):
        self.step_counter.increase()
