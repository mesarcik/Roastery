from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import medfilt
import sys
import os
import copy
import math

class RoCSmoothingThread(QThread):
    finished = pyqtSignal()

    def __init__(self, window):
        QThread.__init__(self)
        self.window = window
        self.weighted_roc = 0

    def __del__(self):
        self.wait()

    def run(self):
        try:
            # print("Smoothing Thread Spawned.")
            if (self.window.smoothAlgorithm == "avg"):
                #print ("Moving Window Average")
                if (self.window.roc_window_size < len(self.window.roc_data) and  self.window.rocSmooth == "True"):
                    self.mov_avg_roc()
            elif (self.window.smoothAlgorithm == "ewma"):
                #print ("Exponential Windowed Moving Average")
                if (self.window.roc_window_size < len(self.window.roc_data) and self.window.rocSmooth == "True"):
                    self.ewma_roc()
            elif (self.window.smoothAlgorithm == "savgol"):
                #print ("Savitzky Golay Filter")
                if (self.window.roc_window_size < len(self.window.roc_data) and self.window.rocSmooth == "True"):
                    self.savgol_roc()
            elif (self.window.smoothAlgorithm == "median"):
                #print ("Median Filter")
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

        self.weighted_roc = self.window.exp_weight* self.window.roc_temp
        exp = 1;
        for i in range (1,self.window.roc_window_size):
            #print("exp weight: " , round(self.window.exp_weight*math.pow((1-self.window.exp_weight),exp),4))
            #print("exp: " ,exp)
            #print("index:" , -i)
            # print('weighted roc : ',self.weighted_roc)
            temp =   round(self.window.exp_weight*math.pow((1-self.window.exp_weight),exp),4) * self.window.roc_data[-i]
            self.weighted_roc += temp
            exp+=1

        self.weighted_roc = round(self.weighted_roc,2)
        print("Previous RoC",self.window.roc_temp)

        print("Weighted RoC",self.weighted_roc)

        self.window.roc_temp = self.weighted_roc

    ####################################


    def median_roc(self):
        # print ("This is parent roc data: " ,self.window.roc_data)
        roc_d = copy.deepcopy(self.window.roc_data)
        roc_d.append(self.window.roc_temp)
        median_ar = roc_d[-self.window.roc_window_size:]
       # print("This is median arr:" , median_ar)
        median_ar=np.trim_zeros(median_ar)
        #print("This is trimmed median arr: " , median_ar)

        if int(self.window.kernel_size) > len(median_ar):
            pass

        else:
            output = medfilt(median_ar, int(self.window.kernel_size))
            # print("This is output: " , output)
            temp = round(output[-1], 2)
            print("Previous RoC", self.window.roc_temp)
            print("Filtered Temp", output[-1])
            self.window.roc_temp = output[-1]
