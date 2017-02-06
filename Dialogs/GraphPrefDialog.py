from pyqtgraph.Qt import QtGui, QtCore

class GraphPrefDialog(QtGui.QDialog):
    def __init__(self, window,parent=None):
        super(GraphPrefDialog, self).__init__()

        self.dialog_layout = QtGui.QFormLayout()
        self.setLayout(self.dialog_layout)
        self.ratio = 8.325  # For 1 second

        self.window = window

        self.temp_title = QtGui.QLabel("Graph Setup")
        self.scale_title = QtGui.QLabel("RoC Graph Axis Setup")
        self.newfont = QtGui.QFont()
        self.newfont.setBold(True)
        self.newfont.setPointSize(10)
        self.temp_title.setFont(self.newfont)
        self.scale_title.setFont(self.newfont)

        self.scale_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.scale_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.scale_slider.setSingleStep(1)
        self.scale_slider.setValue(self.window.scale)
        self.scale_slider.setTickInterval(1)
        self.scale_slider.setRange(0.5, 10)
        self.scale_slider.valueChanged.connect(self.slider_change)
        self.scale_slider_lable = QtGui.QLabel("Set X-Axis Scale")
        self.scale_slider_val = QtGui.QLabel(str(self.window.scale))

        self.yrange_label = QtGui.QLabel("Set Y-Axis Range")
        self.yrange_start_txt = QtGui.QLineEdit(str(self.window.ystart))
        self.yrange_mid_label = QtGui.QLabel("to")
        self.yrange_end_txt = QtGui.QLineEdit(str(self.window.yend))

        regexp = QtCore.QRegExp('[+-]?\\d*\\.?\\d+') # regex expression from 0 - 100
        self.validator = QtGui.QRegExpValidator(regexp)
        self.yrange_start_txt.setValidator(self.validator)
        self.yrange_end_txt.setValidator(self.validator)

        self.yrange_start_txt.textChanged.connect(self.range_change)
        self.yrange_end_txt.textChanged.connect(self.range_change)




        self.legend_cb = QtGui.QCheckBox('Show Legend', self)

        if (self.window.showLegend == "True"):
            self.legend_cb.setChecked(True)
        else:
            self.legend_cb.setChecked(False)

        self.legend_cb.stateChanged.connect(self.checkbox_change_leg)

        self.int_cb = QtGui.QCheckBox('Interactive Graphs', self)

        if (self.window.int == "True"):
            self.int_cb.setChecked(True)
        else:
            self.int_cb.setChecked(False)

        self.int_cb.stateChanged.connect(self.checkbox_change_int)

        self.initUI()

    def range_change(self):
        self.window.ystart = float(self.yrange_start_txt.text())
        self.window.yend = float(self.yrange_end_txt.text())
    def checkbox_change_leg(self, state1):
        if state1 == QtCore.Qt.Checked:
            self.window.showLegend = 'True'

        else:
            self.window.showLegend = 'False'

    def checkbox_change_int(self, state2):
        if state2 == QtCore.Qt.Checked:
            self.window.int = 'True'

        else:
            self.window.int = 'False'

    def initUI(self):
        self.dialog_layout.addRow(self.temp_title)
        self.dialog_layout.addRow(self.legend_cb, self.int_cb)

        self.scale_layout = QtGui.QGridLayout()
        self.scale_layout.addWidget(self.scale_slider_lable, 0, 0)
        self.scale_layout.addWidget(self.scale_slider, 0, 1)
        self.scale_layout.addWidget(self.scale_slider_val, 0, 2)

        self.dialog_layout.addRow(self.scale_title)
        self.dialog_layout.addRow(self.scale_layout)

        self.range_layout = QtGui.QGridLayout()
        self.range_layout.addWidget(self.yrange_label,0,0)
        self.range_layout.addWidget(self.yrange_start_txt,0,1)
        self.range_layout.addWidget(self.yrange_mid_label,0,2)
        self.range_layout.addWidget(self.yrange_end_txt,0,3)
        self.dialog_layout.addRow(self.range_layout)

        # self.yrange_label = QtGui.QLabel("Set Y-Axis Range")
        # self.yrange_start_txt = QtGui.QLineEdit(str(self.window.ystart))
        # self.yrange_mid_label = QtGui.QLabel("to")
        # self.yrange_end_txt = QtGui.QLineEdit(str(self.window.yend))

        self.dialog_layout.setAlignment(QtCore.Qt.AlignVCenter)

        self.show()

    def slider_change(self):
        self.scale_slider_val.setText(str(self.scale_slider.value()))
        self.window.scale = self.scale_slider.value()



    def showEvent(self, event):
        # geom = self.frameGeometry()
        # cp = QtGui.QDesktopWidget().availableGeometry().center()
        # geom.moveCenter(cp)
        # self.setGeometry(geom)
        # self.move(geom.center())
        self.setWindowTitle("Graph Preference Dialog")


        super(GraphPrefDialog, self).showEvent(event)
