from serial_io import SerialIO
from pid import PID
import threading
from time import sleep

class SharedMemory:
    def __init__(self):
        self.measured_flow = None
        self.control_output = None
        self.target_profile = None #TODO

if __name__ == "__main__":

    shared = SharedMemory()

    sensor = SerialIO(shared, port='/dev/ttyUSB0')
    actuator = SerialIO(shared, port='/dev/ttyUSB1')
    controller = PID()


    th_sensor = threading.Thread(target=sensor.run, args=('read'))
    th_actuator = threading.Thread(target=actuator.run, args=('write'))

    th_sensor.start()
    th_sensor.start()

    while True:
         
        target = shared.target_profile[3] #TODO
        current = shared.measured_flow
        
        shared.control_output = controller.run(target, current)

        sleep(0.01)