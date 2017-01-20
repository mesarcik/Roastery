from pyqtgraph.Qt import QtGui, QtCore
from End_Dialog import End_Dialog
import sys
import csv

class Dock_Widget(QtGui.QWidget):
    def __init__(self,  Top_right_layout, Top_left_layout, Bottom_layout,gas_slider,gas_slider_label,air_slider,air_slider_label,window,parent):
        super(Dock_Widget, self).__init__(parent)
        self.top_right_layout = QtGui.QGridLayout
        self.top_right_layout = Top_right_layout

        self.top_left_layout = QtGui.QGridLayout
        self.top_left_layout = Top_left_layout

        self.bottom_layout = QtGui.QGridLayout
        self.bottom_layout = Bottom_layout

        self.gas_slider = gas_slider
        self.gas_slider_label = gas_slider_label
        self.air_slider = air_slider
        self.air_slider_label = air_slider_label

        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPointSize(10)

        self.window = window

        self.yes_lbl = QtGui.QPushButton("Confirm and Exit")
        self.yes_lbl.setFixedSize(100,27)
        self.percentage_loss = QtGui.QLabel("")
        self.green_weight_fld = QtGui.QTextEdit("0")
        self.roasted_weight_fld = QtGui.QTextEdit("0")
        # self.roasted_weight_fld.textChanged.connect(self.updateLoss)
        # self.green_weight_fld.textChanged.connect(self.updateLoss)

        self.bottom = QtGui.QFrame(self)
        self.splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.initUI()

    def initUI(self):
        self.perc = 0
        hbox = QtGui.QHBoxLayout(self)

        topleft = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        topleft.setLayout(self.top_left_layout)

        topright = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)
        topright.setLayout(self.top_right_layout)


        self.bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bottom.setLayout(self.bottom_layout)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)
        splitter1.setSizes([66.66666, 100])


        self.splitter2.addWidget(splitter1)
        self.splitter2.addWidget(self.bottom)

        hbox.addWidget(self.splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

    def endRoast(self):
        for i in reversed(range(self.bottom_layout.count())):
            try:
                self.bottom_layout.itemAt(i).widget().deleteLater()
            except:
                self.gas_slider.hide()
                self.gas_slider_label.hide()
                self.air_slider.hide()
                self.air_slider_label.hide()
                pass


        end_dialog = End_Dialog(self.window,self)
        # end_dialog.exec_()
        end_dialog.show()
        # end_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
