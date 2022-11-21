import serial
from time import sleep

class SerialIO:
    def __init__(self, shared, port='/dev/ttyUSB0'):
        #shared memeory
        self.shared = shared

        #Variables
        self.state = 0 #0, 1, 2

        # Serial Connect
        self.ser = serial.Serial(port, 115200, timeout=.1)
        print(f"Serial_IO: Serial connecting to {port}...")


    def serial_write(self, x):
        data = bytes(x, 'utf-8')
        self.ser.write(data)

    def serial_read(self):
        #TODO: DAQ
        pass

    def run(self, target):

        while True:
            if target == 'read':
                self.shared.measrued_flow = self.seral_read()
            elif target == 'write':
                self.serial_write(self.shared.control_output)
            sleep(0.01)

