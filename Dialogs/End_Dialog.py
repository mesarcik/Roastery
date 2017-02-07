import sys
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtGui import QPixmap
import subprocess
import datetime
import csv
import os
# from Rosetta import Window




class End_Dialog(QtGui.QMainWindow):
    def __init__(self,window,parent):
        super(End_Dialog, self).__init__(parent)

        self.window= window
        self.new = False

        # layout = QtGui.QHBoxLayout()

        self.myQMenuBar = self.menuBar()
        exitMenu = self.myQMenuBar.addMenu('File')


        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setShortcut('Ctrl+W')
        exitAction.triggered.connect(self.exit)
        exitMenu.addAction(exitAction)


        newWindowAction = QtGui.QAction(QtGui.QIcon.fromTheme('new'), 'New Window', self)
        newWindowAction.setShortcut('Ctrl+N')
        newWindowAction.setStatusTip('New Window')
        newWindowAction.triggered.connect(self.newWindow)
        exitMenu.addAction(newWindowAction)

        self.centralWidget =   QtGui.QWidget()
        layout = QtGui.QFormLayout()


        self.green_weight_lbl = QtGui.QLabel("Green Weight ")

        self.green_weight_fld = QtGui.QLineEdit()
        layout.addRow(self.green_weight_lbl, self.green_weight_fld)
        self.roasted_weight_lbl = QtGui.QLabel("Roasted Weight")

        self.roasted_weight_fld = QtGui.QLineEdit()
        layout.addRow(self.roasted_weight_lbl, self.roasted_weight_fld)
        self.comments = QtGui.QLabel("Comments")

        self.percentage_loss = QtGui.QLabel()
        layout.addRow(QtGui.QLabel("   "),self.percentage_loss)

        self.le2 = QtGui.QLineEdit()
        layout.addRow(self.comments, self.le2)


        self.xit = QtGui.QPushButton("Confirm and Exit")
        layout.addRow(self.xit)
        self.xit.clicked.connect(self.confirm)

        self.roasted_weight_fld.textChanged.connect(self.updateLoss)
        self.green_weight_fld.textChanged.connect(self.updateLoss)

        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Roast End")
        # self.showMaximized()

        self._tempFile = self.window.directory + '/Temp.csv'
        self.export_tempFile = open(self._tempFile, 'a')

        self.temp_writer = csv.writer(self.export_tempFile, dialect='excel')


    def exit(self):
        self.hide()

    def confirm(self):
        print("Confirmed")



        self.temp_writer.writerow(['Green Weight', str(self.green_weight_fld.text())])
        self.temp_writer.writerow(['Roasted Weight', str(self.roasted_weight_fld.text())])
        self.temp_writer.writerow(['Percentage Loss', str(self.percentage_loss.text())])
        self.temp_writer.writerow(['Comments: ', str(self.le2.text())])
        self.export_tempFile.close()
        if(self.new):
            self.hide()
        else:
            sys.exit()

    def updateLoss(self):
        print (self.roasted_weight_fld.text())
        print(self.green_weight_fld.text())
        try:
            self.perc = round(abs(1 - float(str(self.roasted_weight_fld.text())) / float(str(self.green_weight_fld.text()))),4) * 100
            self.percentage_loss.setText(str(self.perc) + '%')

        except Exception as e:
            print e
            pass

    def newWindow(self):
        self.new = True
        self.parent().parent().arduino.disconnect()
        self.parent().parent().arduino.arduino.close()
        del(self.parent().parent().arduino)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        QtGui.QApplication.processEvents()
        self.parent().parent().__init__()
        self.parent().parent().hide()
        self.parent().parent().connect()
        now = datetime.datetime.now()
        self.parent().parent().directory = '/' + now.strftime("%Y-%m-%d %H:%M:%S") 
        QtGui.QApplication.restoreOverrideCursor()
        self.parent().parent().show()
