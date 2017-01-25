from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import medfilt
import sys
import os
import copy
import math


class TempSmoothingThread(QThread):
    finished = pyqtSignal()

    def __init__(self, window):
        QThread.__init__(self)
        self.window = window
        self.weighted_temp = 0

    def __del__(self):
        self.wait()

    def run(self):
        try:
            # print("Smoothing Thread Spawned.")
            if (self.window.smoothAlgorithm == "avg"):
                # print ("Moving Window Average")
                if (self.window.temp_window_size < len(self.window.temp_data) and self.window.tempSmooth == "True"):
                    self.mov_avg_temp()
            elif (self.window.smoothAlgorithm == "ewma"):
                # print ("Exponential Windowed Moving Average")
                if (self.window.temp_window_size < len(self.window.temp_data) and self.window.tempSmooth == "True"):
                    self.ewma_temp()
            elif (self.window.smoothAlgorithm == "savgol"):
                # print ("Savitzky Golay Filter")
                if (self.window.temp_window_size < len(self.window.temp_data) and self.window.tempSmooth == "True"):
                    self.savgol_temp()

            elif (self.window.smoothAlgorithm == "median"):
                # print ("Median Filter")
                if (self.window.temp_window_size < len(self.window.temp_data) and self.window.tempSmooth == "True"):
                    self.median_temp()


        except ():
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass
        finally:
            self.finished.emit()

    ####################################
    def savgol_temp(self):
        # Create a temporary data array with the new temperature data appended.
        temp_d = copy.deepcopy(self.window.temp_data)
        temp_d.append(self.window.line)
        # Smooth the values.
        yhat = savgol_filter(temp_d, self.window.temp_window_size, 3)  # window size 51, polynomial order 3
        # pop the last value off and set that as the incomming temperature value.
        self.window.line = round(float(yhat[-1]), 1)
        self.window.temp_data = np.ndarray.tolist(yhat[:-1])

    #####################################
    def mov_avg_temp(self):
        pass

    ##################################333
    def ewma_temp(self):

        self.weighted_temp = self.window.exp_weight*self.window.line
        exp = 1;
        for i in range (1,self.window.temp_window_size):
            #print("exp weight: " , round(self.window.exp_weight*math.pow((1-self.window.exp_weight),exp),4))
            #print("exp: " ,exp)
            #print("index:" , -i)
            # print('weighted temp : ',weighted_temp)
            temp =   round(self.window.exp_weight*math.pow((1-self.window.exp_weight),exp),4) * self.window.temp_data[-i]
            self.weighted_temp += temp
            exp+=1

        self.weighted_temp = round(self.weighted_temp,1)
        print("Previous Temp",self.window.line)

        print("Weighted Temp",self.weighted_temp)

        self.window.line = self.weighted_temp

    ####################################
    def median_temp(self):
        temp_d = copy.deepcopy(self.window.temp_data)
        temp_d.append(self.window.line)
        median_ar = temp_d[-self.window.temp_window_size:]
        output = medfilt(median_ar,int(self.window.kernel_size))
        output = round(output[-1],1)

        print("Previous Temp", self.window.line)

        print("Filtered Temp", output)

        self.window.line = output
       ######################################
