from __future__ import division
from pyqtgraph.Qt import QtGui, QtCore

class SmoothingDialog(QtGui.QDialog):
    def __init__(self, window,font,parent=None):
        super(SmoothingDialog, self).__init__()
        self.window = window
        self.font = font


        self.dialog_layout = QtGui.QGridLayout()
        self.setLayout(self.dialog_layout)

        self.title = QtGui.QLabel('Smoothing Algorithm Preferences')
        self.title.setFont(self.font)

        self.temp_title = QtGui.QLabel("Smoothing Preferences")
        self.temp_title.setFont(self.font)


        self.temp_cb = QtGui.QCheckBox('Temperature Smoothing', self)
        self.roc_cb = QtGui.QCheckBox('Rate of Change Smoothing', self)

        if(self.window.tempSmooth=="True"):
            self.temp_cb.setChecked(True)
        else:
            self.temp_cb.setChecked(False)
        if (self.window.rocSmooth == "True"):
            self.roc_cb.setChecked(True)
        else:
            self.roc_cb.setChecked(False)

        self.temp_cb.stateChanged.connect(self.temp_checkbox_change)
        self.roc_cb.stateChanged.connect(self.roc_checkbox_change)



        self.radio_group = QtGui.QButtonGroup()
        self.ewma_button = QtGui.QRadioButton('EWMA Filter')
        self.ewma_button.setToolTip("Exponential Weighted Moving Average")
        self.median_button = QtGui.QRadioButton('Median Filter')
        self.savgol_button = QtGui.QRadioButton('Savitzky-Golay Filter')
        self.window_button = QtGui.QRadioButton('Moving Average Filter')



        self.temp_window_size_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.temp_window_size_slider.setValue(int(self.window.temp_window_size))
        self.temp_window_size_slider.setMinimum(1)
        self.temp_window_size_slider.setMaximum(101)
        self.temp_window_size_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        # self.temp_window_size_slider.setTickInterval(2)
        self.temp_window_size_slider.setSingleStep(2)
        self.temp_window_size_slider.valueChanged.connect(self.slider_change)
        self.temp_window_size_label = QtGui.QLabel('Temperature Smoothing Window Size')
        self.temp_window_size_val = QtGui.QLabel(str(self.window.temp_window_size) + ' samples')


        self.roc_window_size_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.roc_window_size_slider.setValue(int(self.window.roc_window_size))
        self.roc_window_size_slider.setMinimum(1)
        self.roc_window_size_slider.setMaximum(101)
        self.roc_window_size_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        # self.roc_window_size_slider.setTickInterval(2)
        self.roc_window_size_slider.setSingleStep(2)
        self.roc_window_size_slider.valueChanged.connect(self.slider_change)
        self.roc_window_size_label = QtGui.QLabel('RoC Smoothing Window Size')
        self.roc_window_size_val = QtGui.QLabel(str(window.roc_window_size) + ' samples')

        self.exp_weight_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.exp_weight_slider.setValue(int(self.window.exp_weight*100))
        self.exp_weight_slider.setMinimum(10)
        self.exp_weight_slider.setMaximum(100)
        self.exp_weight_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.exp_weight_slider.setSingleStep(10)
        self.exp_weight_slider.valueChanged.connect(self.slider_change)
        self.exp_weight_label = QtGui.QLabel('Exponential Weight')
        self.exp_weight_val = QtGui.QLabel(str(window.exp_weight) )
        self.exp_weight_slider.setEnabled(False)

        self.radio_select()

        self.initUI()

    def temp_checkbox_change(self,state):
        if state == QtCore.Qt.Checked:
            self.window.tempSmooth ='True'
        else:
            self.window.tempSmooth ='False'

    def roc_checkbox_change(self, state):
        if state == QtCore.Qt.Checked:
            self.window.rocSmooth = 'True'
        else:
            self.window.rocSmooth = 'False'


    def initUI(self):
        self.ewma_button.toggled.connect(self.radio_change)
        self.window_button.toggled.connect(self.radio_change)
        self.savgol_button.toggled.connect(self.radio_change)
        self.median_button.toggled.connect(self.radio_change)

        if (str(self.window.rocMethod).__contains__('point')):
            self.ewma_button.setChecked(True)

        if (str(self.window.rocMethod).__contains__('self.window')):
            self.window_button.setChecked(True)


        self.dialog_layout.addWidget(self.temp_title, 0, 0)
        self.dialog_layout.addWidget(self.temp_cb,1,0)
        self.dialog_layout.addWidget(self.roc_cb,1,1)

        temp_window_size_layout = QtGui.QGridLayout()
        temp_window_size_layout.addWidget(self.temp_window_size_label, 0, 0)
        temp_window_size_layout.addWidget(self.temp_window_size_slider, 0, 1)
        temp_window_size_layout.addWidget(self.temp_window_size_val, 0, 2)
        self.dialog_layout.addLayout(temp_window_size_layout,2,0,1,3)

        roc_window_size_layout =QtGui.QGridLayout()
        roc_window_size_layout.addWidget(self.roc_window_size_label, 0, 0)
        roc_window_size_layout.addWidget(self.roc_window_size_slider, 0, 1)
        roc_window_size_layout.addWidget(self.roc_window_size_val, 0, 2)
        self.dialog_layout.addLayout(roc_window_size_layout, 3, 0, 1, 3)

        exp_weight_layout = QtGui.QGridLayout()
        exp_weight_layout.addWidget(self.exp_weight_label, 0, 0)
        exp_weight_layout.addWidget(self.exp_weight_slider, 0, 1)
        exp_weight_layout.addWidget(self.exp_weight_val, 0, 2)
        self.dialog_layout.addLayout(exp_weight_layout, 4, 0, 1, 3)



        self.dialog_layout.addWidget(self.title, 5, 0)
        self.dialog_layout.addWidget(self.savgol_button, 6, 0)
        self.dialog_layout.addWidget(self.window_button, 6, 1)
        self.dialog_layout.addWidget(self.ewma_button, 6, 2)
        self.dialog_layout.addWidget(self.median_button, 6, 3)
        self.dialog_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.show()

    def slider_change(self):
        ##MAKE SURE SLIDER ODD FOR WINDOW SIZE!
        while(int(self.temp_window_size_slider.value())%2 ==0):
            self.temp_window_size_slider.setValue(int(self.temp_window_size_slider.value()) + 1)

        self.temp_window_size_val.setText(str(self.temp_window_size_slider.value()) + ' samples')
        self.window.temp_window_size = self.temp_window_size_slider.value()

        while (int(self.roc_window_size_slider.value()) % 2 == 0):
            self.roc_window_size_slider.setValue(int(self.roc_window_size_slider.value()) + 1)

        self.roc_window_size_val.setText(str(self.roc_window_size_slider.value()) + " samples")
        self.window.roc_window_size = self.roc_window_size_slider.value()

        rounded_val =round(self.exp_weight_slider.value()/100,1)
        self.exp_weight_val.setText(str(rounded_val))
        self.window.exp_weight = rounded_val

    def radio_select(self):
        if (self.window.smoothAlgorithm == "avg"):
            self.window_button.setChecked(True)
        elif (self.window.smoothAlgorithm == "ewma"):
            self.ewma_button.setChecked(True)
            self.exp_weight_slider.setEnabled(True)
        elif (self.window.smoothAlgorithm == "savgol"):
            self.savgol_button.setChecked(True)
        else:
            self.median_button.setChecked(True)

    def radio_change(self):

        if (self.window_button.isChecked()):
            self.window.smoothAlgorithm = 'avg'
            self.exp_weight_slider.setEnabled(False)
        elif (self.ewma_button.isChecked()):
            self.window.smoothAlgorithm = 'ewma'
            self.exp_weight_slider.setEnabled(True)
        elif (self.savgol_button.isChecked()):
            self.window.smoothAlgorithm = 'savgol'
            self.exp_weight_slider.setEnabled(False)
        elif (self.median_button.isChecked()):
            self.window.smoothAlgorithm = 'median'
            self.exp_weight_slider.setEnabled(False)


    def showEvent(self, event):
        self.setWindowTitle("Smoothing Preference Dialog")
        super(SmoothingDialog, self).showEvent(event)
