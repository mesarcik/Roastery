from PyQt4.QtCore import QThread
import numpy as np
import sys
import os


class SmoothingThread(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window

    def __del__(self):
        self.wait()

    def run(self):
        try:
            print("Smoothing Thread Spawned.")
            if (self.window.smoothAlgorithm == "avg"):
                print ("Moving Window Average")
                self.mov_avg()
            elif (self.window.smoothAlgorithm == "ewma"):
                print ("Exponential Windowed Moving Average")
                self.ewma()
            elif (self.window.smoothAlgorithm == "savgol"):
                print ("Savitzky–Golay Filter")
                self.savgol()
            elif (self.window.smoothAlgorithm == "median"):
                print ("Median Filter")
                self.median()

        except ():
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass

    def savgol(self):
        pass
    def mov_avg (self):
        pass
    def ewma (self):
        pass
    def median (self):
        pass