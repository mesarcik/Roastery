from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import sys
import os


class RoCThread(QThread):

    finished = pyqtSignal()


    def __init__(self, window):
        QThread.__init__(self)
        self.window = window

    def __del__(self):
        self.wait()

    def run(self):
        try:
            self.updateRoC()
        except ():
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass
        finally:
            self.finished.emit()

    def updateRoC(self):
        try:
            if (len(self.window.temp_data) - 3 > self.window.delta - 1):
                # print("GOT IN!")
                if (self.window.count > self.window.delta):

                    if (self.window.rocMethod.__contains__('point')):  # Point Average
                        self.window.roc_temp = (self.window.temp_data[self.window.count - 1] - self.window.temp_data[
                            self.window.count - int(self.window.delta)]) / int(self.window.delta)
                    elif (self.window.rocMethod.__contains__('window')):  # Moving self.window Average
                        frame_tot = 0
                        for point in range(self.window.count - 3 - int(self.window.delta + 1),
                                           self.window.count - 3):  # self.window.delta + 1 because it needs to go to zero
                            frame_tot += self.window.temp_data[point] - self.window.temp_data[point - 1]

                        self.window.roc_temp = frame_tot / self.window.delta

                else:
                    self.window.roc_temp = 0

            else:
                self.window.roc_temp = 0
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass

