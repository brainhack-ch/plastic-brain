import serial


class ArduinoCommHandler:
    def __init__(self, port_name, baudrate=115200):
        self.serial_obj = serial.Serial()
        self.serial_obj.port = port_name
        self.serial_obj.baudrate = baudrate

    def start_communication(self):
        try:
            self.serial_obj.open()
            print("Starting Communication with {} at {}."
                  .format(self.serial_obj.port, self.serial_obj.baudrate))
        except Exception as e:
            print("WARNING: Impossible to communicate with {} at {}."
                  .format(self.serial_obj.port, self.serial_obj.baudrate))
            print(e)

    def stop_communication(self):
        self.serial_obj.close()

    def send_led_values(self, values_array):
        values_array.insert(0, ord('S'))
        b_array = bytearray(values_array)
        if self.serial_obj.isOpen():
            self.serial_obj.write(b_array)
            # print("Sending...")
            # print(b_array)
        else:
            print(len(values_array))
