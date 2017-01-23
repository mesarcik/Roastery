from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import medfilt
import sys
import os
import copy

class RoCSmoothingThread(QThread):
    finished = pyqtSignal()

    def __init__(self, window):
        QThread.__init__(self)
        self.window = window

    def __del__(self):
        self.wait()

    def run(self):
        try:
            # print("Smoothing Thread Spawned.")
            if (self.window.smoothAlgorithm == "avg"):
                print ("Moving Window Average")
                if (self.window.roc_window_size < len(self.window.roc_data) and  self.window.rocSmooth == "True"):
                    self.mov_avg_roc()
            elif (self.window.smoothAlgorithm == "ewma"):
                print ("Exponential Windowed Moving Average")
                if (self.window.roc_window_size < len(self.window.roc_data) and self.window.rocSmooth == "True"):
                    self.ewma_roc()
            elif (self.window.smoothAlgorithm == "savgol"):
                print ("Savitzky Golay Filter")
                if (self.window.roc_window_size < len(self.window.roc_data) and self.window.rocSmooth == "True"):
                    self.savgol_roc()
            elif (self.window.smoothAlgorithm == "median"):
                print ("Median Filter")
                if (self.window.roc_window_size < len(self.window.roc_data) and self.window.rocSmooth == "True"):
                    self.median_roc()

        except ():
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass
        finally:
            self.finished.emit()

    ####################################

    def savgol_roc(self):
        # Create a temporary data array with the new roc data appended.
        roc_d = copy.deepcopy (self.window.roc_data)
        roc_d.append(self.window.roc_temp)
        # Smooth the values.
        yhat = savgol_filter(roc_d, self.window.temp_window_size, 3)  # window size 51, polynomial order 3
        # pop the last value off and set that as the incomming temperature value.
        self.window.roc_temp = round(float(yhat[-1]), 1)
        self.window.roc_data= np.ndarray.tolist(yhat[:-1])

    #####################################

    def mov_avg_roc(self):
        pass

    ##################################333

    def ewma_roc(self):
        pass

    ####################################


    def median_roc(self):
        pass
        ######################################
