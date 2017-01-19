from PyQt4.QtCore import QThread
import numpy as np


class RecoveryThread(QThread):

    def __init__(self,window):
        QThread.__init__(self)
        self.window = window

    def __del__(self):
        self.wait()

    def run(self):
        if (self.window.elapsed > 1):
            print('Recovery Thread Spawned')
            self.window.elapsed -=1
            self.window.t.addSecs(1)
            self.window.global_count += 1
            self.window.second_count+=1

            ###########R O  C DATA TO BE APPENDED############

            self.window.roc_data.append(float(self.window.roc_data[-1]))
            self.window.roc_time_data.append(self.window.t.elapsed())

            self.window.roc_tp_data.append(float(0))
            self.window.roc_first_crack_data.append(0)
            self.window.roc_second_crack_data.append(0)
            self.window.roc_drop_out_data.append(0)
            self.window.gas_lvl = float(self.window.gas_slider.value())
            self.window.gas_data.append(float((self.window.gas_lvl * 1.0) / 333.3333))

            #########T E  M  P    D A T A   T O    B E   A P P E N D E D ############
            self.window.temp_data.append(float(self.window.temp_data[-1]))
            self.window.time_data.append(self.window.t.elapsed())

            self.window.temp_tp_data.append(float(0))
            self.window.temp_first_crack_data.append((float(0)))
            self.window.temp_second_crack_data.append((float(0)))
            self.window.temp_drop_out_data.append(float(0))
            air_lvl = float(self.window.air_slider.value())
            self.window.air_data.append(air_lvl * 2.4)



