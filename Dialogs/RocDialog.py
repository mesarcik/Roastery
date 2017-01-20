from pyqtgraph.Qt import QtGui, QtCore

class RocDialog(QtGui.QDialog):
    def __init__(self, window,font,parent=None):
        super(RocDialog, self).__init__()
        self.window = window
        self.font = font


        self.dialog_layout = QtGui.QGridLayout()
        self.setLayout(self.dialog_layout)

        self.title = QtGui.QLabel('Rate of Change Preferences')
        self.title.setFont(self.font)


        self.temp_title = QtGui.QLabel("Temperature Smoothing Preferences")
        self.temp_title.setFont(self.font)



        self.cb = QtGui.QCheckBox('Temperature Smoothing', self)
        if(self.window.tempSmooth=="True"):
            self.cb.setChecked(True)
        else:
            self.cb.setChecked(False)

        self.cb.stateChanged.connect(self.checkbox_change)


        self.radio_group = QtGui.QButtonGroup()
        self.ewma_button = QtGui.QRadioButton('EWMA Filter')
        self.ewma_button.setToolTip("Exponential Weighted Moving Average")
        self.ewma_button.setEnabled(False)
        self.median_button = QtGui.QRadioButton('Median Filter')
        self.median_button.setEnabled(False)
        self.savgol_button = QtGui.QRadioButton('Savitzky-Golay Filter')
        self.savgol_button.setEnabled(False)
        self.window_button = QtGui.QRadioButton('Moving Average Filter')

        self.window_size_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.window_size_slider.setValue(window.delta)
        self.window_size_slider.setRange(1,100)
        # self.window_size_slider.setTickInterval()
        self.window_size_label = QtGui.QLabel('Delta Size')
        self.window_size_val = QtGui.QLabel(str(window.delta) + ' samples')
        # self.window_size_val.setFont(font)

        self.sampling_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.sampling_slider.setValue(window.sampling_interval)
        self.sampling_label = QtGui.QLabel('Sampling Interval')
        self.sampling_val = QtGui.QLabel(str(window.sampling_interval) + ' ms')
        # self.sampling_val.setFont(font)
        self.sampling_slider.setEnabled(False)

        self.refresh_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.referesh_label = QtGui.QLabel('Referesh Rate')
        self.refresh_slider.setValue(window.refresh_rate)
        self.refresh_val = QtGui.QLabel(str(window.refresh_rate) + ' samples')
        # self.refresh_val.setFont(font)
        self.refresh_slider.setEnabled(False)

        # #Roc properties
        # window.sampling_interval = 100
        # window.rocMethod = 'point'
        # window.delta =15
        # window.refresh_rate = 10
        # window.refresh_counter = 0
        self.initUI()

    def checkbox_change(self,state):
        if state == QtCore.Qt.Checked:
            self.window.tempSmooth ='True'
        else:
            self.window.tempSmooth ='False'



    def initUI(self):
        self.ewma_button.toggled.connect(self.radio_change)
        self.window_button.toggled.connect(self.radio_change)
        self.savgol_button.toggled.connect(self.radio_change)
        self.median_button.toggled.connect(self.radio_change)

        if (str(self.window.rocMethod).__contains__('point')):
            self.ewma_button.setChecked(True)

        if (str(self.window.rocMethod).__contains__('self.window')):
            self.window_button.setChecked(True)

        self.radio_group.addButton(self.ewma_button)
        self.radio_group.addButton(self.window_button)
        self.radio_group.addButton(self.savgol_button)
        self.radio_group.addButton(self.median_button)

        self.dialog_layout.addWidget(self.temp_title, 0, 0)
        self.dialog_layout.addWidget(self.cb,1,0)


        self.dialog_layout.addWidget(self.title, 2, 0)
        self.dialog_layout.addWidget(self.savgol_button, 3, 0)
        self.dialog_layout.addWidget(self.window_button, 3, 1)
        self.dialog_layout.addWidget(self.ewma_button, 3, 2)
        self.dialog_layout.addWidget(self.median_button, 3, 3)
        self.dialog_layout.setAlignment(QtCore.Qt.AlignLeft)



        delta_layout = QtGui.QGridLayout()
        sampleing_layout = QtGui.QGridLayout()
        refresh_layout = QtGui.QGridLayout()

        self.window_size_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.window_size_slider.setTickInterval(10)
        self.window_size_slider.setSingleStep(10)
        self.window_size_slider.valueChanged.connect(self.slider_change)

        self.sampling_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.sampling_slider.setTickInterval(100)
        self.sampling_slider.setSingleStep(10)
        self.sampling_slider.setMaximum(1000)
        self.sampling_slider.valueChanged.connect(self.slider_change)

        self.refresh_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.refresh_slider.setTickInterval(50)
        self.refresh_slider.setSingleStep(1)
        self.refresh_slider.setMinimum(1)
        self.refresh_slider.setMaximum(500)
        self.refresh_slider.valueChanged.connect(self.slider_change)

        delta_layout.addWidget(self.window_size_label, 0, 0)
        delta_layout.addWidget(self.window_size_slider, 0, 1)
        delta_layout.addWidget(self.window_size_val, 0, 2)

        sampleing_layout.addWidget(self.sampling_label, 0, 0)
        sampleing_layout.addWidget(self.sampling_slider, 0, 1)
        sampleing_layout.addWidget(self.sampling_val, 0, 2)

        refresh_layout.addWidget(self.referesh_label, 0, 0)
        refresh_layout.addWidget(self.refresh_slider, 0, 1)
        refresh_layout.addWidget(self.refresh_val, 0, 2)

        self.dialog_layout.addLayout(delta_layout, 4, 0, 1, 3)
        self.dialog_layout.addLayout(sampleing_layout, 5, 0, 1, 3)
        self.dialog_layout.addLayout(refresh_layout, 6, 0, 1, 3)

        # self.setGeometry(300, 300, 250, 150)

        self.show()

    def slider_change(self):
        self.window_size_val.setText(str(self.window_size_slider.value()) + ' samples')
        self.window.delta = self.window_size_slider.value()
        self.sampling_val.setText(str(self.sampling_slider.value()) + " ms")
        self.window.sampling_interval = self.sampling_slider.value()
        self.refresh_val.setText(str(self.refresh_slider.value()) + ' samples')
        self.window.refresh_rate = self.refresh_slider.value()

    def radio_change(self):

        if (self.window_button.isChecked()):
            self.window.rocMethod = 'self.window'

        elif (self.ewma_button.isChecked()):
            self.window.rocMethod = 'ewma'

        elif (self.savgol_button.isChecked()):
            self.window.rocMethod = 'savgol'

        elif (self.median_button.isChecked()):
            self.window.rocMethod = 'median'

    def showEvent(self, event):
        # geom = self.frameGeometry()
        # cp = QtGui.QDesktopWidget().availableGeometry().center()
        # geom.moveCenter(cp)
        # self.setGeometry(geom)
        # self.move(geom.center())
        self.setWindowTitle("Rate Of Change Preference Dialog")


        super(RocDialog, self).showEvent(event)
