import serial


class SerialStudio:

    def __init__(self, baudrate):
        ports_to_try = ['/dev/ttyACM0', '/dev/ttyACM1']

        for port in ports_to_try:
            print(f"Trying port {port}")
            self.ser = serial.Serial('/dev/ttyACM0', baudrate)
            if self.ser:
                print(f"Serial connection established on {port}")
                break

        if not self.ser:
            print("Unable to establish a serial connection. Exiting.")
            return
    
    def get_send_errorXY(self):
        #Get the string sended by the main PC and send it via serial to the tiva
        #TODO
        pass

    def close(self):
        self.ser.close()


