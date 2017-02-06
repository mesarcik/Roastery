from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import numpy as np
import sys
import os




class GrapherThread(QThread):

    finished = pyqtSignal()


    def __init__(self,window):
        QThread.__init__(self)
        self.window = window
        self.y_air = []
        self.x_time = []
        # self.window.line = round(self.window.line,2)
        # self.window.roc_temp = round(self.window.roc_temp,2)

    def __del__(self):
        self.wait()

    def run(self):
        #   print("Graph Thread Spawned")
        try:
            self.devTime()
            self.window.refresh_counter += 1
            self.serialFlush()
            self.turnP()
            self.correctNone()
            self.updateTemp()
            self.updateValues()
        except ():
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        finally:
            self.finished.emit()

    def updateValues(self):
        self.window.roc_label.setText('ROC ' + str(round(self.window.roc_temp, 1)))

        self.window.roc_data.append(float(self.window.roc_temp))
        self.window.roc_time_data.append(self.window.t.elapsed())
        x_roc_time = np.array(self.window.roc_time_data)
        y_roc_data = np.array(self.window.roc_data)

        if (len(self.window.roc_first_crack_data) != len(x_roc_time)):
            self.window.roc_first_crack_data.append(0)
            self.window.roc_second_crack_data.append(0)
            self.window.roc_drop_out_data.append(0)
            self.window.roc_tp_data.append(0)
            self.window.gas_lvl = float(self.window.gas_slider.value())
            self.window.gas_data.append(float((self.window.gas_lvl * 1.0) / 333.3333))

        self.window.roc_curve.setData(x=x_roc_time, y=y_roc_data)
        self.window.roc_first_crack.setData(x=x_roc_time, y=np.array(self.window.roc_first_crack_data))
        self.window.roc_second_crack.setData(x=x_roc_time,
                                             y=np.array(self.window.roc_second_crack_data))
        self.window.roc_drop_out.setData(x=x_roc_time, y=np.array(self.window.roc_drop_out_data))
        self.window.roc_tp.setData(x=x_roc_time, y=np.array(self.window.roc_tp_data))
        self.window.roc_gas_curve.setData(x=x_roc_time, y=np.array(self.window.gas_data))

        # Normalize the RoC Air Scale
        y_roc_air_temp = np.divide(self.y_air, 2.4)
        y_roc_air = np.divide(y_roc_air_temp, 333.3333)

        self.window.roc_air_curve.setData(x=self.x_time, y=y_roc_air)

        self.window.roc_tp_data.append(float(0))
        self.window.roc_first_crack_data.append((float(0)))
        self.window.roc_second_crack_data.append((float(0)))
        self.window.roc_drop_out_data.append(float(0))
        self.window.gas_lvl = float(self.window.gas_slider.value())
        self.window.gas_data.append(float((self.window.gas_lvl * 1.0) / 333.3333))

    def devTime(self):
        # DEV TIME STUFF
        if (self.window.first_crack_bool):
            # print ("This is elasped time: " + str(self.window.minute_count*60 + self.window.second_count) )
            # print("This is first crack time " + str( self.window.fcrack_time_s) )

            dev_amount_s = (self.window.minute_count * 60 + self.window.second_count) - self.window.fcrack_time_s
            dev_percentage = (1 - round(
                float((float(self.window.fcrack_time_s) / float(
                    (self.window.minute_count * 60 + self.window.second_count)))), 2)) * 100
            self.window.dev_second_count += 1

            if (self.window.dev_second_count == 60):
                self.window.dev_minute_count += 1
                self.window.dev_second_count = 0

            dev_amount_str = str(self.window.dev_minute_count) + ":" + str(self.window.dev_second_count)
            self.window.dev_label.setText("DEV: " + dev_amount_str + " | " + str(dev_percentage) + "%")

    def serialFlush(self):
        # SERIAL PORT FLUSHER
        if (self.window.refresh_counter == self.window.refresh_rate):
            self.window.arduino.arduino.flushOutput()
            self.window.arduino.arduino.flushInput()
            self.window.refresh_counter = 0

    def turnP(self):
        zeroless =  np.trim_zeros(self.window.roc_data)
        if (self.window.tp_bool == False):
            if (len(zeroless) > 10):
                if (self.window.roc_data[-9] < 0):
                    if (self.window.roc_data[-1] > 0):
                        self.window.temp_tp_data[-1] = float(240)
                        self.window.roc_tp_data[-1] = float(0.3)
                        self.window.turn()
                        self.window.tp_bool = True

    def updateTemp(self):
        if (self.window.count > 1):
            #try:

            self.window.time_data.append(self.window.t.elapsed())
            # if (self.window.tempSmooth == "True"):
            #     try:
            #         self.window.temp_data.append(
            #             round(float((self.window.line * 0.1 + self.window.temp_data[-1] * 0.9)), 1))
            #     except:
            #         self.window.temp_data.append(float(self.window.line))
            #         pass
            # else:
            self.window.temp_data.append(float(self.window.line))

            air_lvl = float(self.window.air_slider.value())

            self.window.air_data.append(air_lvl * 2.4)

            self.window.global_count += 1

            self.x_time = np.array(self.window.time_data)
            y_temp = np.array(self.window.temp_data)
            self.y_air = np.array(self.window.air_data)

            self.window.temp_tp_data.append(float(0))
            self.window.temp_first_crack_data.append((float(0)))
            self.window.temp_second_crack_data.append((float(0)))
            self.window.temp_drop_out_data.append(float(0))

            self.window.temp_curve.setData(x=self.x_time, y=y_temp)
            self.window.temp_air_curve.setData(x=self.x_time, y=self.y_air)
            self.window.temp_first_crack.setData(x=self.x_time, y=np.array(self.window.temp_first_crack_data))
            self.window.temp_second_crack_curve.setData(x=self.x_time,
                                                        y=np.array(self.window.temp_second_crack_data))
            self.window.temp_drop_out.setData(x=self.x_time, y=np.array(self.window.temp_drop_out_data))
            self.window.temp_tp.setData(x=self.x_time, y=np.array(self.window.temp_tp_data))


            # self.window.count += 1
            # except:
            #     exc_type, exc_obj, exc_tb = sys.exc_info()
            #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #     print(exc_type, fname, exc_tb.tb_lineno)
            #     # self.window.count += 1
            #     pass


    def correctNone(self):
        try:
            if (self.window.temp_data[0] == 0):
                self.window.temp_data[0] = self.window.line
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            # self.window.count += 1
            pass

