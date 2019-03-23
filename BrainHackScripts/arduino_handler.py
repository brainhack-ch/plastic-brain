import serial


class ArduinoCommHandler:
    def __init__(self, port_name, baudrate=115200):
        self.serial_obj = serial.Serial()
        self.serial_obj.port_name = port_name
        self.serial_obj.baudrate = baudrate

    def start_communication(self):
        self.serial_obj.open()

    def stop_communication(self):
        self.serial_obj.close()

    def send_led_values(values_array):
        values_array.insert(0, 'S')
        b_array = bytearray(values_array)
        #self.serial_obj.write('S')
        #self.serial_obj.write(b_array)
        print(values_array)
