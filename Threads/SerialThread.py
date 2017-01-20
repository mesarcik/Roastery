import sys
import serial
from pyqtgraph.Qt import QtGui, QtCore
import glob
import time

class SerialThread(QtCore.QThread):
    def __init__(self, baud, parent,timer):
        super(SerialThread, self).__init__(parent)
        self.baud = baud
        self.arduino = serial.Serial()
        self.state = True
        self.arduino.baudrate = self.baud
        self.arduino.timeout = 0.2
        self.timer = timer
        self.parent = parent
        self.port_bool = 0
        # self.lock = QtCore.QReadWriteLock()


    def serial_ports(self):
        print("Serial Ports()")
        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            print('Darwin Detected')
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Unsupported platform")

        # result = []
        # for port in ports:
        #     try:
        #         s = serial.Serial(port)
        #         s.close()
        #         result.append(port)
        #     except (OSError, serial.SerialException):
        #         pass
        return ports

    def run(self):
        # temp = 0
        # if sys.platform.startswith('darwin'):
        #     temp=1
        port_a = ''
        print("list of ports:")
        ports = (self.serial_ports())
        for port in ports:
            print (port)
            if sys.platform.startswith("darwin"):
                if("tty.usbmodem" in port):
                    print('PORT FOUND')
                    self.port_bool = 1
                    port_a = port
            elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
                if ("ttyACM" in port):
                    self.port_bool = 1
                    port_a = port

        print(self.port_bool)
        if(self.port_bool == 0):
            self.terminate()

        if (self.port_bool== 1):
            # while ("tty.usbmodem" not in ports[i]):
            #     i = i +1
            #     print (ports[i])

            # print ("connecting to %s",ports[i])

            self.arduino = serial.Serial(port_a)
            print ("connecting")
            timer = 0
            self.arduino.flushOutput()
            self.arduino.flushInput()
            while ((timer < 5)):
                timer += 1
            if (self.arduino.readline() is not None):
                # self.lock.lockForRead()
                self.timer.timeout.connect(self.parent.update)
                self.timer.start(1000)
                print("Connected")


    def disconnect(self):
        # self.lock.unlock()
        print("Aquiring Write Lock")
        # self.lock.lockForWrite()
        print("Locked")
        self.arduino.write("E")
        # self.lock.unlock()
        self.arduino.close()
        self.state = False


    def readline(self):
        # temp_time = time.time()
        val = self.arduino.readline()
        return val


    def flushOutput(self):
        self.arduino.flushOutput()
    def flushInput(self):
        self.arduino.flushInput()


