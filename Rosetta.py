from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtGui import QPixmap
import numpy as np
import sys
import pyqtgraph as pg
import csv
import os
from os.path import expanduser
import datetime
import time
import gc

sys.path.insert(0, '/home/misha/Google Drive/PycharmProjects/Rosetta-November2016/Dialogs')
sys.path.insert(0, '/home/misha/Google Drive/PycharmProjects/Rosetta-November2016/Threads')
sys.path.insert(0, '/home/misha/Google Drive/PycharmProjects/Rosetta-November2016/GraphingTools')
sys.path.insert(0, '/home/misha/Google Drive/PycharmProjects/Rosetta-November2016/Layout')
sys.path.insert(0, '/home/misha/Google Drive/PycharmProjects/Rosetta-November2016/MultiWindow')

from RocDialog import RocDialog
from Dock_Widget import Dock_Widget
from TimeAxisItem import TimeAxisItem
from MultiWindows import MultiWindows
from SerialThread import SerialThread
from BorderLessDiaglogs import BorderLessDiaglogs
from ChildWindow import ChildWindow
from GrapherThread import GrapherThread
from RecoveryThread import RecoveryThread
from GraphPrefDialog import GraphPrefDialog
from SmoothingDialog import SmoothingDialog
from RoCThread import RoCThread
from SmoothingThread import SmoothingThread

###########################################
windows = MultiWindows()

import_temp_time = []
import_roc_time = []
import_temp = []
import_roc = []

import_air = []
import_temp_fcrack = []
import_temp_scrack = []
import_temp_tp = []
import_temp_do = []

import_gas = []
import_roc_fcrack = []
import_roc_scrack = []
import_roc_tp = []
import_roc_do = []
now = datetime.datetime.now()
counter = 0
current_bean = ""


################################################


class Window(QtGui.QMainWindow):
    # initilize main window
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None)  # , QtCore.Qt.WindowStaysOnTopHint

        # super(Window, self).__init__()
        self.first = False

        self.s_time = time.time()
        self.elapsed = 0

        self.current_temp = []
        self.start_time = 0
        self.import_bool = False
        self.line = ''

        self.new_window = None
        self.count = 1
        self.global_count = 0
        self.tp_bool = False

        self.temp_temp = []

        self.temp_data = [0]
        self.time_data = [0]
        self.roc_time_data = [0]
        self.gas_data = [0]
        self.air_data = [0]
        self.roc_data = [0]
        self.temp_drop_out_data = [0]
        self.temp_tp_data = [0]
        self.temp_first_crack_data = [0]
        self.temp_second_crack_data = [0]
        self.roc_drop_out_data = [0]
        self.roc_tp_data = [0]
        self.roc_first_crack_data = [0]
        self.roc_second_crack_data = [0]
        self.start_stop = False

        # Lable timer init
        self.timer_thread = QtCore.QTimer()
        self.minute_count = 0
        self.second_count = 0
        self.corrective_counter = 0
        self.offset = 0;
        self.second_count_minus_1 = 0

        self.timer = QtCore.QTimer()

        self.t = QtCore.QTime()

        # Roc properties
        self.sampling_interval = None
        self.rocMethod = ''
        self.delta = None
        self.refresh_rate = None
        self.refresh_counter = 0
        self.tempSmooth = ''
        self.rocSmooth = ''
        self.smoothAlgorithm = ''
        self.showLegend = ''
        self.int = ''
        self.scale = 2
        self.ratio = 8.325

        self.beans = []
        self.roc_temp = 0

        #######Place holder for development time
        self.fcrack_time_s = 0;
        self.first_crack_bool = False
        self.dev_minute_count = 0
        self.dev_second_count = 0

        # Toolbar init
        self.fcrack_action = QtGui.QAction(QtGui.QIcon.fromTheme(''), 'First Crack (f)', self)
        self.start_stop_action = QtGui.QAction(QtGui.QIcon.fromTheme(''), 'Start/Stop (F2)', self)
        self.scrack_action = QtGui.QAction(QtGui.QIcon.fromTheme(''), 'Second Crack (s)', self)
        self.tp_action = QtGui.QAction(QtGui.QIcon.fromTheme(''), 'Turning Point (t)', self)
        self.do_action = QtGui.QAction(QtGui.QIcon.fromTheme(''), 'Drop Out (d)', self)
        self.gas_action = QtGui.QAction(QtGui.QIcon.fromTheme(''), 'Gas Level (g)', self)
        self.air_action = QtGui.QAction(QtGui.QIcon.fromTheme(''), 'Air Level (a)', self)

        self.directory = '/' + now.strftime("%Y-%m-%d %H:%M")

        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            home = expanduser("~")
            self.roastPreflocation = home + '/Roastery/RoastPref'



        elif sys.platform.startswith('darwin'):
            self.roastPreflocation = os.path.expanduser("~/Roastery/RoastPref")

        self.arduino = None

        self.initBeans()
        self.initUI()

        # Makeing fonts
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPointSize(10)

        self.font_b = QtGui.QFont()
        self.font_b.setBold(True)
        self.font_b.setPointSize(25)

        # STATUS BAR LABELS
        self.time_label = QtGui.QLabel()
        self.temp_label = QtGui.QLabel()
        self.roc_label = QtGui.QLabel()
        self.dev_label = QtGui.QLabel()

        self.time_label.setFont(self.font_b)
        self.temp_label.setFont(self.font_b)
        self.roc_label.setFont(self.font_b)
        self.dev_label.setFont(self.font_b)

        self.time_label.setAlignment(QtCore.Qt.AlignLeft)
        self.temp_label.setAlignment(QtCore.Qt.AlignLeft)
        self.roc_label.setAlignment(QtCore.Qt.AlignLeft)
        self.dev_label.setAlignment(QtCore.Qt.AlignLeft)

        self.statusbar = QtGui.QStatusBar()
        self.color = QtGui.QColor()
        self.color.setNamedColor('light grey')

        self.palette = QtGui.QPalette()
        self.palette.setColor(QtGui.QPalette.Background, self.color)
        self.statusbar.setPalette(self.palette)
        self.statusbar.addPermanentWidget(self.temp_label, 20)
        self.statusbar.addPermanentWidget(self.time_label, 20)
        self.statusbar.addPermanentWidget(self.roc_label, 20)
        self.statusbar.addPermanentWidget(self.dev_label, 20)
        self.setStatusBar(self.statusbar)

        # adding the central Widget
        self.top_right_layout = QtGui.QGridLayout()
        self.top_right_layout.setMargin(15)

        self.top_left_layout = QtGui.QGridLayout()
        self.top_left_layout.setMargin(15)

        self.bottom_layout = QtGui.QGridLayout()
        self.bottom_layout.setMargin(15)

        # ADDING GUI ELEMENTS

        self.gas_slider = QtGui.QSlider()
        self.gas_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.gas_slider.setTickInterval(20)
        self.gas_slider.setSingleStep(5)
        self.gas_slider_label = QtGui.QLabel('           Gas Level')
        self.gas_slider.setOrientation(QtCore.Qt.Horizontal)
        # gas_slider.setMaximumSize(QtCore.QSize(200,300))


        self.air_slider = QtGui.QSlider()
        self.air_slider.setValue(33.33333)
        self.air_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.air_slider.setTickInterval(33.33333)
        self.air_slider.setSingleStep(5)
        self.air_slider_label = QtGui.QLabel('Air Level')
        self.air_slider.setOrientation(QtCore.Qt.Horizontal)
        # air_slider.setMaximumSize(QtCore.QSize(200,300))
        #
        # def __init__(self, parent, Top_right_layout, Top_left_layout, Bottom_layout, gas_slider, gas_slider_label, air_slider,
        #              air_slider_label, font, window):

        # //    def __init__(self, parent, , , ,,,,,window):


        self.dock_widget = Dock_Widget(self.top_right_layout, self.top_left_layout, self.bottom_layout, self.gas_slider,
                                       self.gas_slider_label, self.air_slider, self.air_slider_label, self, self)
        self.setCentralWidget(self.dock_widget)

        ##########################################

        self.initPref()
        self.setup_graph()

        self.setup_tables()

        self.current_lbl = QtGui.QLabel('                                                Current Data')
        self.current_lbl.setFont(self.font)

        self.import_lbl = QtGui.QLabel('                                                 Imported Data')
        self.import_lbl.setFont(self.font)

        stats_lbl = QtGui.QLabel('                                                   Weight Data')
        stats_lbl.setFont(self.font)

        # Add widgets to the layout in their proper positions


        self.top_bottom_layout = QtGui.QGridLayout()

        self.top_bottom_layout.addWidget(self.air_slider_label, 0, 0)
        self.top_bottom_layout.addWidget(self.air_slider, 0, 1)

        self.top_bottom_layout.addWidget(self.gas_slider_label, 0, 2)
        self.top_bottom_layout.addWidget(self.gas_slider, 0, 3)

        self.bottom_layout.addLayout(self.top_bottom_layout, 0, 0, 1, 3)

        self.bottom_layout.addWidget(self.current_lbl, 2, 0)
        self.bottom_layout.addWidget(self.import_lbl, 2, 1)
        self.bottom_layout.addWidget(stats_lbl, 2, 2)
        self.bottom_layout.addWidget(self.current_tbl, 3, 0)
        self.bottom_layout.addWidget(self.import_tbl, 3, 1)
        self.bottom_layout.addWidget(self.stats_tbl, 3, 2)

        # layout.addWidget(text, 1, 0)  # text edit goes in middle-left
        self.top_right_layout.addWidget(self.roc, 0, 1, 1, 1)  # list widget goes in bottom-left
        self.top_left_layout.addWidget(self.temp, 0, 0, 1, 1)  # plot goes on right side, spanning 3 rows

        self.showMaximized()

        print("EVERYTHING IS INITIALIZED")

    # initlize tables (import/export)
    def setup_tables(self):
        ############### TABLE ELEMENTS ######################

        self.current_tbl = QtGui.QTableWidget()
        self.current_tbl.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.current_tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.current_tbl.setRowCount(6)
        self.current_tbl.setColumnCount(2)
        # current_tbl.resizeColumnsToContents()
        self.current_tbl.resizeRowsToContents()
        self.current_tbl.setHorizontalHeaderLabels(QtCore.QString("Time;Temp").split(";"))
        self.current_tbl.setVerticalHeaderLabels(
            QtCore.QString("Start;First Crack;Second Crack;Turning Point;Drop Out; Roast End").split(";"))
        self.current_tbl.horizontalHeader().setStretchLastSection(True)

        for col in range(0, 2):  # Initialize table to blanks
            for row in range(0, 6):
                self.current_tbl.setItem(row, col, QtGui.QTableWidgetItem(" "))

        self.import_tbl = QtGui.QTableWidget()
        self.import_tbl.setRowCount(6)
        self.import_tbl.setColumnCount(2)
        self.import_tbl.setHorizontalHeaderLabels(QtCore.QString("Time;Temp").split(";"))
        self.import_tbl.setVerticalHeaderLabels(
            QtCore.QString("Start;First Crack;Second Crack;Turning Point;Drop Out; Roast End").split(";"))

        self.import_tbl.horizontalHeader().setStretchLastSection(True)
        # import_tbl.verticalHeader().setStretchLastSection(True)
        # import_tbl.resizeColumnsToContents()
        self.import_tbl.resizeRowsToContents()
        self.import_tbl.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.import_tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.stats_tbl = QtGui.QTableWidget()
        self.stats_tbl.setRowCount(3)
        self.stats_tbl.setColumnCount(1)
        self.stats_tbl.setHorizontalHeaderLabels(QtCore.QString("Value").split(";"))
        self.stats_tbl.setVerticalHeaderLabels(
            QtCore.QString("Green Weight;Roasted Weight;Percentage Weight Loss").split(";"))
        self.stats_tbl.horizontalHeader().setStretchLastSection(True)
        self.stats_tbl.verticalHeader().setStretchLastSection(True)
        self.stats_tbl.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.stats_tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.stats_tbl.resizeRowsToContents()

    # initilize pyqtgraph
    def setup_graph(self):
        print("Configuring graphs")

        if (self.import_bool):
            print("Impoort Bool is True")
            self.temp.close()
            self.roc.close()

        # GRAPHING ELEMENTS ###################################
        self.TempAxis = TimeAxisItem(orientation='bottom')
        self.TempAxis.setScale(
            self.scale * self.ratio)  # Scale to get accurate minute measurements. -- 16.65 is one minute measures
        self.temp = pg.PlotWidget(title='Temperature vs. Time Graph', axisItems={'bottom': self.TempAxis})

        if (self.int == "False"):
            self.temp.setInteractive(False)
        else:
            self.temp.setInteractive(True)

        self.pen = pg.mkPen(color='c', width=1)
        self.gas_pen = pg.mkPen(color='m', width=1.5)
        self.air_pen = pg.mkPen(color='b', width=1.5)
        self.fc_pen = pg.mkPen(color='r', width=1.5)
        self.sc_pen = pg.mkPen(color='y', width=1.5)
        self.tp_pen = pg.mkPen(color='w', width=1.5)
        self.do_pen = pg.mkPen(color='g', width=1.5)

        self.ipen = pg.mkPen(color='c', style=QtCore.Qt.DashLine, width=0.25)
        self.igas_pen = pg.mkPen(color='m', style=QtCore.Qt.DashLine, width=0.25)
        self.iair_pen = pg.mkPen(color='m', style=QtCore.Qt.DashLine, width=0.25)
        self.ifc_pen = pg.mkPen(color='r', style=QtCore.Qt.DashLine, width=0.25)
        self.isc_pen = pg.mkPen(color='y', style=QtCore.Qt.DashLine, width=0.25)
        self.itp_pen = pg.mkPen(color='w', style=QtCore.Qt.DashLine, width=0.25)
        self.ido_pen = pg.mkPen(color='g', style=QtCore.Qt.DashLine, width=0.25)

        self.temp_curve = self.temp.plot(pen=self.pen, name='Temperature')
        self.import_temp_curve = self.temp.plot(pen=self.ipen)

        self.temp_air_curve = self.temp.plot(pen=self.air_pen, name='Air Flow')
        self.import_temp_air_curve = self.temp.plot(pen=self.iair_pen)
        self.temp_first_crack = self.temp.plot(pen=self.fc_pen, name='First Crack')
        self.import_temp_first_crack = self.temp.plot(pen=self.ifc_pen)
        self.temp_second_crack_curve = self.temp.plot(pen=self.sc_pen, name='Second Crack')
        self.import_temp_second_crack_curve = self.temp.plot(pen=self.isc_pen)
        self.temp_tp = self.temp.plot(pen=self.tp_pen, name='Turning Point')
        self.import_temp_tp_curve = self.temp.plot(pen=self.itp_pen)
        self.temp_drop_out = self.temp.plot(pen=self.do_pen, name='Drop Out')
        self.import_temp_drop_out_curve = self.temp.plot(pen=self.ido_pen)

        self.temp.setXRange(0, 800000., padding=0)
        self.temp.setYRange(0, 255, padding=0)
        self.temp.showGrid(x=True, y=True, alpha=0.3)
        self.RoCaxis = TimeAxisItem(orientation='bottom')
        self.RoCaxis.setScale(self.scale * self.ratio)
        # self.tickFont = QtGui.QFont()
        # self.tickFont.setPointSize(8.5)
        # self.tickFont.
        # self.RoCaxis.setTickFont(self.tickFont)


        self.roc = pg.PlotWidget(title='RoC vs. Time Graph', axisItems={'bottom': self.RoCaxis})
        self.roc.setXRange(0, 800000., padding=0)

        #    def tickSpacing(self, minVal, maxVal, size):


        if (self.showLegend == "True"):
            self.roc.addLegend(size=(110, 0), offset=(480, 130))
            print("Show legend")
        else:
            self.roc.plotItem.removeItem(self.roc.plotItem.legend)
            print("Hide legend")

        if (self.int == "False"):
            self.roc.setInteractive(False)
        else:
            self.roc.setInteractive(True)
        # except:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno)
        #     pass
        self.roc_curve = self.roc.plot(pen=self.pen, name='Rate of Change/Temperature')
        self.import_roc_curve = self.roc.plot(pen=self.ipen)

        self.roc_gas_curve = self.roc.plot(pen=self.gas_pen, name='Gas Level')
        self.import_roc_gas_curve = self.roc.plot(pen=self.igas_pen)

        self.roc_air_curve = self.roc.plot(pen=self.air_pen, name='Air Flow')
        self.import_roc_air_curve = self.roc.plot(pen=self.iair_pen)

        self.roc_first_crack = self.roc.plot(pen=self.fc_pen, name='First Crack')
        self.import_roc_first_crack = self.roc.plot(pen=self.ifc_pen)

        self.roc_second_crack = self.roc.plot(pen=self.sc_pen, name='Second Crack')
        self.import_roc_second_crack = self.roc.plot(pen=self.isc_pen)

        self.roc_tp = self.roc.plot(pen=self.tp_pen, name='Turning Point')
        self.import_roc_tp_curve = self.roc.plot(pen=self.itp_pen)

        self.roc_drop_out = self.roc.plot(pen=self.do_pen, name='Drop Out')
        self.import_roc_drop_out_curve = self.roc.plot(pen=self.ido_pen)

        self.roc.setYRange(0, 0.33, padding=0)

        self.roc.showGrid(x=True, y=True, alpha=0.3)

    # spawn serialthread to determine Serial connections
    def connect(self):
        self.arduino = SerialThread(9600, self, self.timer)
        self.arduino.start()
        while (self.arduino.isRunning()):
            continue
        if (self.arduino.port_bool == 0):
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Thermocouple systems cannot be reached\n\nError Encountered: ")
            msgBox.setInformativeText("Please diconnect and reconnect USB cable")
            msgBox.setWindowTitle("ERROR")
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Ok:
                self.quit()

    # add all the graphical stuff to the interface -- initialize shortcuts
    def initUI(self):
        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit'), 'Terminate Application', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.quit)

        newWindowAction = QtGui.QAction(QtGui.QIcon.fromTheme('new'), 'New Window', self)
        newWindowAction.setShortcut('Ctrl+N')
        newWindowAction.setStatusTip('New Window')
        newWindowAction.triggered.connect(self.showChildWindow)

        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&File')

        editMenu = self.menubar.addMenu('Edit')

        toolMenu = self.menubar.addMenu('Tools')

        import_Action = editMenu.addAction('Import Data')
        import_Action.triggered.connect(self.importAction)
        import_Action.setShortcut('Ctrl+I')
        import_Action.setStatusTip('Import Data')

        export_Action = editMenu.addAction('Export Data')
        export_Action.triggered.connect(self.exportAction)
        export_Action.setShortcut('Ctrl+E')
        export_Action.setStatusTip('Export Data')

        bean_pref = toolMenu.addMenu('Bean Preferences')
        cb_action = bean_pref.addAction("Select Bean Type")
        add_bean_action = bean_pref.addAction('Add New Bean Type')
        remove_bean_action = bean_pref.addAction('Remove New Bean')
        add_bean_action.triggered.connect(self.addBean)
        remove_bean_action.triggered.connect(self.removeBean)
        cb_action.triggered.connect(self.selectBean)
        graph_pref_action = QtGui.QAction(QtGui.QIcon.fromTheme('somethingelse'), 'Graph Preferences', self)
        roc_pref_action = QtGui.QAction(QtGui.QIcon.fromTheme('somethingelse'), 'Rate of Change Preferences', self)
        smooth_pref_action = QtGui.QAction(QtGui.QIcon.fromTheme('somethingelse'), 'Smoothing Preferences', self)

        roc_pref_action.triggered.connect(self.rocPref)
        graph_pref_action.triggered.connect(self.graphPref)
        smooth_pref_action.triggered.connect(self.smoothPref)

        toolMenu.addAction(roc_pref_action)
        toolMenu.addAction(graph_pref_action)
        toolMenu.addAction(smooth_pref_action)

        fileMenu.addAction(exitAction)
        fileMenu.addAction(newWindowAction)

        self.start_stop_action.setShortcut('F2')
        self.start_stop_action.triggered.connect(self.ss)
        self.fcrack_action.setShortcut('f')
        self.fcrack_action.triggered.connect(self.fcrack)
        self.scrack_action.setShortcut('s')
        self.scrack_action.triggered.connect(self.scrack)
        self.tp_action.setShortcut('t')
        self.tp_action.triggered.connect(self.turn)
        self.do_action.setShortcut('d')
        self.do_action.triggered.connect(self.drop)

        self.gas_action.setShortcut('g')
        self.gas_action.triggered.connect(self.gas)
        self.air_action.setShortcut('a')
        self.air_action.triggered.connect(self.air)

        self.toolbar = self.addToolBar('ToolBar')

        self.toolbar.addAction(self.start_stop_action)
        self.toolbar.addAction(self.fcrack_action)
        self.toolbar.addAction(self.scrack_action)
        self.toolbar.addAction(self.tp_action)
        self.toolbar.addAction(self.do_action)
        self.toolbar.addAction(self.gas_action)
        self.toolbar.addAction(self.air_action)

        self.fcrack_action.setEnabled(False)
        self.scrack_action.setEnabled(False)
        self.tp_action.setEnabled(False)
        self.do_action.setEnabled(False)
        self.gas_action.setEnabled(False)
        self.air_action.setEnabled(False)

    # Fuction for making a new window
    def showChildWindow(self):
        if (self.arduino.state == False):
            gc.collect()
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            start = time.time()
            splash = QtGui.QSplashScreen(QPixmap((os.path.expanduser("/~/Roastery/loading.png"))),
                                         QtCore.Qt.WindowStaysOnTopHint)
            splash.show()
            progressBar = QtGui.QProgressBar(splash)
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(QtCore.Qt.red))

            progressBar.setPalette(palette)

            splash.setMask(QPixmap((os.path.expanduser("~/Roastery/loading.png"))).mask())

            splash.show()
            for i in range(0, 100):
                progressBar.setValue(i)
                t = time.time()
                while time.time() < t + 0.1:
                    app.processEvents()

            self.child_win = ChildWindow()
            self.child_win.show()
            self.child_win.connect()

            splash.finish(self.child_win)
            QtGui.QApplication.restoreOverrideCursor()


        else:
            print("Another Thread running")

    # timed thread that calls update function to collect serial data, smooth, etc
    def update(self):
        self.elapsed = round(time.time() - self.s_time, 1)
        if (self.elapsed > 1):
            print("Elapsed Time: " + str(self.elapsed))

        self.line = self.arduino.readline()
        self.first = True
        self.line = round(float(self.line), 1)

        self.temp_temp.append(float(self.line))
        if (self.tempSmooth == "True"):
            try:
                # self.temp_label.setText('        TEMP:' + str(round(float((self.temp_temp[-1] + self.temp_temp[-2] + self.temp_temp[-3]) / 3),1)))
                self.temp_label.setText(
                    '        TEMP:' + str(round((self.temp_temp[-1] * 0.1 + self.temp_temp[-2] * 0.9), 1)))

            except:
                self.temp_label.setText('        TEMP:' + str((self.line)))
                if (self.start_stop == False):
                    self.offset += 1
                pass
        else:
            self.temp_label.setText('        TEMP:' + str((self.line)))

        if (self.start_stop == True):

            if ((self.second_count == 59) or ((self.second_count_minus_1 > 50) and (self.second_count < 10))):
                self.minute_count += 1
                self.second_count = 0
            if (self.second_count < 10):
                if (self.minute_count < 10):
                    self.time_label.setText('TIME 0' + str(self.minute_count) + ":0" + str(self.second_count))
                else:
                    self.time_label.setText('TIME ' + str(self.minute_count) + ":0" + str(self.second_count))
            else:
                if (self.minute_count < 10):
                    self.time_label.setText('TIME 0' + str(self.minute_count) + ":" + str(self.second_count))
                else:
                    self.time_label.setText('TIME ' + str(self.minute_count) + ":" + str(self.second_count))
            self.second_count_minus_1 = self.second_count
            self.second_count = int(((time.time() - self.start_time) % 60))

            recoveryThread = RecoveryThread(self)

            while (self.elapsed > 1):
                recoveryThread.start()
                while (recoveryThread.isRunning()):
                    continue

            self.count += 1

            rocThread = RoCThread(self)
            rocThread.finished.connect(self.onRoCFinished)
            rocThread.start()



            # while (self.grapherThread.isRunning()):
            #     continue

        self.s_time = time.time()
        # time.sleep()

    def onRoCFinished(self):
        try:
            print("RoC calcucalted: Graph results.")

            ###################SMOOTHIONG THREADS ###############################

            rocSmoothingThread = SmoothingThread(self)
            tempSmoothingThread = SmoothingThread(self)

            ####################################################################
            grapherThread = GrapherThread(self)
            grapherThread.start()
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass

    # terminate application on shortcut keys
    def quit(self):
        self.deleteLater()
        self.close()
        sys.exit()

    # def closeEvent(self, event):

    # initialize the preference files
    def initPref(self):
        print'init Pref'

        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            pre_file = open(os.path.expanduser("~/Roastery/Pref"), "r")
        elif sys.platform.startswith('darwin'):
            pre_file = open(os.path.expanduser("~/Roastery/Pref"), "r")

        line = pre_file.readline()

        while line != '':
            if (line.__contains__('sampling_interval')):
                val = line.split('=')
                self.sampling_interval = float(val[1])
                print("Sampling interval", self.sampling_interval)
            if (line.__contains__('rocMethod')):
                val = line.split('=')
                # print"This is val 1 " + val[1]
                self.rocMethod = str(val[1]).strip('\n')
                print("ROC Method", self.rocMethod)
            if (line.__contains__('delta')):
                val = line.split('=')
                self.delta = float(val[1])
                print("Delta Amount", self.delta)
            if (line.__contains__('refresh_rate')):
                val = line.split('=')
                self.refresh_rate = float(val[1])
                print("Refresh rate ", self.refresh_rate)
            if (line.__contains__('temp_smooth')):
                val = line.split('=')
                self.tempSmooth = str(val[1]).strip('\n')
                print("Temp smooth: ", self.tempSmooth)
            if (line.__contains__('roc_smooth')):
                val = line.split('=')
                self.rocSmooth = str(val[1]).strip('\n')
                print("RoC smooth: ", self.rocSmooth)
            if (line.__contains__('smooth_algorithm')):
                val = line.split('=')
                self.smoothAlgorithm = str(val[1]).strip('\n')
                print("Smoothing Algorithm: ", self.smoothAlgorithm)
            if (line.__contains__('show_legend')):
                val = line.split('=')
                self.showLegend = str(val[1]).strip('\n')
                print("Show Legend: ", self.showLegend)
            if (line.__contains__('int')):
                val = line.split('=')
                self.int = str(val[1]).strip('\n')
                print("Interactive graphs: ", self.int)
            if (line.__contains__('scale')):
                val = line.split('=')
                self.scale = float(str(val[1]).strip('\n'))
                print("Scale: ", self.scale)
            line = pre_file.readline()

    # save initialzed preferences to disk
    def savePref(self):

        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            pref_file = open(os.path.expanduser("~/Roastery/Pref"), "w")
            pref_file.write('sampling_interval =' + str(self.sampling_interval) + '\n')
            pref_file.write('rocMethod =' + str(self.rocMethod) + '\n')
            pref_file.write('delta =' + str(self.delta) + '\n')
            pref_file.write('refresh_rate =' + str(self.refresh_rate) + "\n")
            pref_file.write('temp_smooth=' + str(self.tempSmooth) + "\n")
            pref_file.write('roc_smooth=' + str(self.rocSmooth) + "\n")
            pref_file.write('smooth_algorithm=' + str(self.smoothAlgorithm) + "\n")
            pref_file.write('show_legend=' + str(self.showLegend) + "\n")
            pref_file.write('int=' + str(self.int) + "\n")
            pref_file.write('scale=' + str(self.scale))

            pref_file.close()

        elif sys.platform.startswith('darwin'):
            pref_file = open(os.path.expanduser("~/Roastery/Pref"), "w")
            pref_file.write('sampling_interval =' + str(self.sampling_interval) + '\n')
            pref_file.write('rocMethod =' + str(self.rocMethod) + '\n')
            pref_file.write('delta =' + str(self.delta) + '\n')
            pref_file.write('refresh_rate =' + str(self.refresh_rate) + "\n")
            pref_file.write('temp_smooth=' + str(self.tempSmooth) + "\n")
            pref_file.write('roc_smooth=' + str(self.rocSmooth) + "\n")
            pref_file.write('smooth_algorithm=' + str(self.smoothAlgorithm) + "\n")
            pref_file.write('show_legend=' + str(self.showLegend) + "\n")
            pref_file.write('int=' + str(self.int) + "\n")
            pref_file.write('scale=' + str(self.scale))

            pref_file.close()

    # call ROC preference dialog in a new thread
    def rocPref(self):
        roc_dialog = RocDialog(self, self.font)
        roc_dialog.exec_()
        roc_dialog.show()
        roc_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.savePref()
        self.initPref()

        print'ROC PREF'

    # call smoothing preference dialog in a new thread
    def smoothPref(self):
        smooth_dialog = SmoothingDialog(self, self.font)
        smooth_dialog.exec_()
        smooth_dialog.show()
        smooth_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.savePref()
        self.initPref()

        print'ROC PREF'

    # call graph preferences dialog
    def graphPref(self):

        QtGui.QMessageBox.information(self, "Restart Notice",
                                      "This session must be restarted for graph changes to take place.")

        graph_dialog = GraphPrefDialog(self, self.font)
        graph_dialog.exec_()
        graph_dialog.show()
        graph_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.savePref()
        self.initPref()

        print'Graph PREF'

    # load in the bean preferenecs
    def initBeans(self):
        try:
            with open(self.roastPreflocation, 'r') as f:
                line = f.readline()
                self.beans = line.split(',')
            self.setWindowTitle(str(self.beans[0]))
        except Exception as e:
            print e
            msgBox = QtGui.QMessageBox()

            fg = msgBox.frameGeometry()
            cp = QtGui.QDesktopWidget().availableGeometry().center()
            fg.moveCenter(cp)
            msgBox.move(fg.center())

            msgBox.setText('Cannot Find Preference Files')
            msgBox.setInformativeText('Please contact support')
            msgBox.setWindowTitle("ERROR")
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()

            if ret == QtGui.QMessageBox.Ok:
                self.quit()

    # allows for the saving and track keeping of selected beans
    def selectBean(self):
        item, ok = QtGui.QInputDialog.getItem(self, "Select Bean", "Beans: ", self.beans, 0, False)
        current_bean = item
        if ok and item:
            file_writer = open(self.roastPreflocation, 'w')
            file_writer.write(current_bean + ",")
            for bean in self.beans:
                if bean != current_bean:
                    file_writer.write(bean + ',')
            file_writer.seek(-1, os.SEEK_END)
            file_writer.truncate()

            file_writer.close()
        self.initBeans()
        self.setWindowTitle(current_bean)

    # reads in .csv for import
    def importAction(self):
        x = False
        rcount = 0
        ccount = 0
        fname = QtGui.QFileDialog.getExistingDirectory(self, 'Open file', '/home')
        tempFile = fname + '/Temp.csv'
        rocFile = fname + '/RoC.csv'

        self.setFocus(True)
        self.show()

        try:
            temp_f = open(tempFile, 'r')
            roc_f = open(rocFile, 'r')

            with temp_f:
                try:
                    temp_reader = csv.reader(temp_f, dialect='excel')
                    roc_reader = csv.reader(roc_f, dialect='excel')

                    for row in temp_reader:
                        try:
                            rcount += 1
                            if (not (str(row).__contains__('Comments:'))) and (x is False):
                                import_temp_time.append((float(row[0])) * 1000)
                                import_temp.append(float(row[1]))
                                import_air.append(float(row[2]))
                                import_temp_fcrack.append(float(row[3]))
                                import_temp_scrack.append(float(row[4]))
                                import_temp_tp.append(float(row[5]))
                                import_temp_do.append(float(row[6]))

                            if x is True:
                                print(row[0])
                                if (row[0].__contains__("Green Weight")):
                                    self.stats_tbl.setItem(0, 0, QtGui.QTableWidgetItem(row[1]))
                                if (row[0].__contains__("Roasted Weight")):
                                    self.stats_tbl.setItem(0, 1, QtGui.QTableWidgetItem(row[1]))
                                if (row[0].__contains__("Percentage Loss")):
                                    self.stats_tbl.setItem(0, 2, QtGui.QTableWidgetItem(row[1]))
                                if (row[0].__contains__("Start")):
                                    self.import_tbl.setItem(0, 0, QtGui.QTableWidgetItem(row[1]))
                                    self.import_tbl.setItem(0, 1, QtGui.QTableWidgetItem(row[2]))
                                if (row[0].__contains__("First Crack")):
                                    self.import_tbl.setItem(1, 0, QtGui.QTableWidgetItem(row[1]))
                                    self.import_tbl.setItem(1, 1, QtGui.QTableWidgetItem(row[2]))
                                if (row[0].__contains__("Second Crack")):
                                    self.import_tbl.setItem(2, 0, QtGui.QTableWidgetItem(row[1]))
                                    self.import_tbl.setItem(2, 1, QtGui.QTableWidgetItem(row[2]))
                                if (row[0].__contains__("Turning Point")):
                                    self.import_tbl.setItem(3, 0, QtGui.QTableWidgetItem(row[1]))
                                    self.import_tbl.setItem(3, 1, QtGui.QTableWidgetItem(row[2]))
                                if (row[0].__contains__("Drop Out")):
                                    self.import_tbl.setItem(4, 0, QtGui.QTableWidgetItem(row[1]))
                                    self.import_tbl.setItem(4, 1, QtGui.QTableWidgetItem(row[2]))
                                if (row[0].__contains__("End")):
                                    self.import_tbl.setItem(5, 0, QtGui.QTableWidgetItem(row[1]))
                                    self.import_tbl.setItem(5, 1, QtGui.QTableWidgetItem(row[2]))
                                print str(row)

                            if (str(row).__contains__('Comments:')):
                                print 'comment found'
                                x = True



                        except Exception, e:
                            print e
                            print "Unexpect ed error:", sys.exc_info()[0]
                            pass

                    x = False
                    for r in roc_reader:
                        try:
                            if (not (str(r).__contains__('Comments:'))) and (x is False):
                                import_roc_time.append((float(r[0])) * 1000)
                                import_roc.append(float(r[1]))
                                import_gas.append(float(r[2]))
                                import_roc_fcrack.append(float(r[3]))
                                import_roc_scrack.append(float(r[4]))
                                import_roc_tp.append(float(r[5]))
                                import_roc_do.append(float(r[6]))

                            if (str(r).__contains__('Comments:')):
                                print 'comment found'
                                break


                        except:
                            print "Unexpected error:", sys.exc_info()[0]
                            pass


                finally:
                    temp_f.close()
                    roc_f.close()
                    self.import_temp_curve.setData(x=np.array(import_temp_time), y=np.array(import_temp))
                    self.import_temp_air_curve.setData(x=np.array(import_temp_time), y=(np.array(import_air)))
                    self.import_temp_first_crack.setData(x=np.array(import_temp_time), y=(np.array(import_temp_fcrack)))
                    self.import_temp_second_crack_curve.setData(x=np.array(import_temp_time),
                                                                y=(np.array(import_temp_scrack)))
                    self.import_temp_tp_curve.setData(x=np.array(import_temp_time), y=(np.array(import_temp_tp)))
                    self.import_temp_drop_out_curve.setData(x=np.array(import_temp_time), y=(np.array(import_temp_do)))

                    self.import_roc_curve.setData(x=np.array(import_roc_time), y=np.array(import_roc))
                    self.import_roc_gas_curve.setData(x=np.array(import_roc_time), y=(np.array(import_gas)))
                    self.import_roc_first_crack.setData(x=np.array(import_roc_time), y=(np.array(import_roc_fcrack)))
                    self.import_roc_second_crack.setData(x=np.array(import_roc_time), y=(np.array(import_roc_scrack)))
                    self.import_roc_tp_curve.setData(x=np.array(import_roc_time), y=(np.array(import_roc_tp)))
                    self.import_roc_drop_out_curve.setData(x=np.array(import_roc_time), y=(np.array(import_roc_do)))

                    # Normalize the RoC Air Scale
                    y_air = np.array(import_air)
                    y_roc_air_temp = np.divide(y_air, 2.4)
                    y_roc_air = np.divide(y_roc_air_temp, 333.3333)
                    self.import_roc_air_curve.setData(x=import_temp_time, y=y_roc_air)

                    self.import_bool = True
                    self.setFocus()


        except Exception as e:
            print e
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You have not selected a roast data file')
            msgBox.setInformativeText('Please reopen import dialog and select correct file')
            msgBox.setWindowTitle("ERROR")
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()

            if ret == QtGui.QMessageBox.Ok:
                pass

    # add bean to disk
    def addBean(self):
        bean_file = open(self.roastPreflocation, 'a')
        text, result = QtGui.QInputDialog.getText(self, "Add New Bean Dialog", "Please Enter New Bean Name")
        if result:
            bean_file.write(',' + text)
            bean_file.close()
        self.initBeans()

    # remove bean from disk
    def removeBean(self):

        item, ok = QtGui.QInputDialog.getItem(self, "Select Bean to Remove", "Beans: ", self.beans, 0, False)

        if ok and item:
            file_writer = open(self.roastPreflocation, 'w')
            for bean in self.beans:
                if bean != item:
                    file_writer.write(bean + ',')
            file_writer.seek(-1, os.SEEK_END)
            file_writer.truncate()

            file_writer.close()
        self.initBeans()

    # writes .csv file for all the current data
    def exportAction(self):
        global directory
        print'export'
        reply = QtGui.QMessageBox.question(self, 'Confirmation',
                                           "Exporting data requires ending the roasting session\nAre you sure you want to do this?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            try:
                self.timer.stop()
            except:
                dne = QtGui.QMessageBox.question(self, 'Confirmation',
                                                 "Please start a roasting session before exporting.",
                                                 QtGui.QMessageBox.Ok)

                if (dne == QtGui.QMessageBox.Ok):
                    return
            if (not self.start_stop):
                self.current_temp = self.temp_label.text().split(":")
                self.current_tbl.setItem(5, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
            self.current_tbl.setItem(5, 0,
                                     QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))
            self.timer.stop()
            export_dir = QtGui.QFileDialog.getExistingDirectory(self, 'Select Export Directory', '/home')
            self.setExportBean()
            self.directory = str(export_dir + "/" + self.directory)
            print("This is direcetory:  " + self.directory)

            if not os.path.exists(self.directory):
                os.makedirs(self.directory, mode=0o777)

            _tempFile = self.directory + '/Temp.csv'
            export_tempFile = open(_tempFile, 'w+')
            _rocFile = self.directory + '/RoC.csv'
            export_rocFile = open(_rocFile, 'w+')

            temp_writer = csv.writer(export_tempFile, dialect='excel')
            roc_writer = csv.writer(export_rocFile, dialect='excel')
            try:
                roc_writer.writerow(
                    ['Time', 'RoC', 'Gas', 'Air', 'First Crack', 'Second Crack', 'Turning Point', 'Drop Out'])
                temp_writer.writerow(['Time', 'Temp', 'Air', 'First Crack', 'Second Crack', 'Turing Point', 'Drop Out'])

                for i in range(0, (len(self.temp_data) - 1)):
                    temp_writer.writerow(
                        [i, self.temp_data[i], self.air_data[i], self.temp_first_crack_data[i],
                         self.temp_second_crack_data[i],
                         self.temp_tp_data[i], self.temp_drop_out_data[i]])

                for i in range(0, (len(self.roc_data) - 1)):
                    roc_writer.writerow(
                        [i, self.roc_data[i], self.gas_data[i], self.air_data[i], self.roc_first_crack_data[i],
                         self.roc_second_crack_data[i],
                         self.roc_tp_data[i], self.roc_drop_out_data[i]])
            except:
                print "Unexpected error:", sys.exc_info()[0]
                pass
            finally:
                try:

                    temp_writer.writerow(['Comments:'])
                    temp_writer.writerow(['', 'Time', 'Temp'])
                    temp_writer.writerow(
                        ['Roast Start', self.current_tbl.item(0, 0).text(), self.current_tbl.item(0, 1).text()])
                    temp_writer.writerow(
                        ['First Crack', self.current_tbl.item(1, 0).text(), self.current_tbl.item(1, 1).text()])
                    temp_writer.writerow(
                        ['Second Crack', self.current_tbl.item(2, 0).text(), self.current_tbl.item(2, 1).text()])
                    temp_writer.writerow(
                        ['Turning Point', self.current_tbl.item(3, 0).text(), self.current_tbl.item(3, 1).text()])
                    temp_writer.writerow(
                        ['Drop Out', self.current_tbl.item(4, 0).text(), self.current_tbl.item(4, 1).text()])
                    temp_writer.writerow(
                        ['Roast End', self.current_tbl.item(5, 0).text(), self.current_tbl.item(5, 1).text()])
                    temp_writer.writerow(['Development Time', str(self.dev_label.text()), ""])

                    roc_writer.writerow(['Comments:'])
                    roc_writer.writerow(['', 'Time', 'Temp'])
                    roc_writer.writerow(
                        ['Roast Start', self.current_tbl.item(0, 0).text(), self.current_tbl.item(0, 1).text()])
                    roc_writer.writerow(
                        ['First Crack', self.current_tbl.item(1, 0).text(), self.current_tbl.item(1, 1).text()])
                    roc_writer.writerow(
                        ['Second Crack', self.current_tbl.item(2, 0).text(), self.current_tbl.item(2, 1).text()])
                    roc_writer.writerow(
                        ['Turning Point', self.current_tbl.item(3, 0).text(), self.current_tbl.item(3, 1).text()])
                    roc_writer.writerow(
                        ['Drop Out', self.current_tbl.item(4, 0).text(), self.current_tbl.item(4, 1).text()])
                    roc_writer.writerow(
                        ['Roast End', self.current_tbl.item(5, 0).text(), self.current_tbl.item(5, 1).text()])
                    roc_writer.writerow(['Development Time', self.dev_label.text(), ""])
                    export_tempFile.close()
                    export_rocFile.close()

                    print("exported to: " + self.directory)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    pass

                finally:
                    try:
                        self.timer.stop()
                        self.timer.disconnect(self.timer, QtCore.SIGNAL('timeout()'), self.update)
                        self.timer_thread.stop()
                        # self.timer_thread.disconnect(self.timer_thread, QtCore.SIGNAL('timeout()'), self.updateTime)
                        self.arduino.disconnect()
                        print'arduino port closed'
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        pass
                    finally:
                        self.hide()
                        self.exportImages()
                        self.dock_widget.endRoast()

    def exportImages(self):
        print("Exporting Images")
        try:
            QPixmap.grabWidget(self.temp).save(self.directory + '/Temperature vs Time.jpg', 'jpg', -1)
            QPixmap.grabWidget(self.temp).save(self.directory + '/Roc vs Time.jpg', 'jpg', -1)
            QPixmap.grabWidget(self).save(self.directory + '/screenshot.jpg', 'jpg', -1)

        except:
            print "Unexpected error:", sys.exc_info()[0]
            pass

    # function for file management and ensuring that all beans are in the same folder.
    def setExportBean(self):
        self.directory = self.beans[0] + self.directory

    # start/stop function
    def ss(self):
        global timer
        if (self.first == True):

            self.fcrack_action.setEnabled(True)
            self.scrack_action.setEnabled(True)
            self.tp_action.setEnabled(True)
            self.do_action.setEnabled(True)
            self.gas_action.setEnabled(True)
            self.air_action.setEnabled(True)

            if (self.start_stop is False):
                self.start_time = time.time()
                self.t.start()
                # self.timer.start(self.sampling_interval)
                self.current_temp = self.temp_label.text().split(":")
                self.start_stop = True
                self.current_tbl.setItem(0, 1, QtGui.QTableWidgetItem(self.current_temp[1]))
                self.current_tbl.setItem(0, 0, QtGui.QTableWidgetItem(str('00:00')))


            elif (self.start_stop is True):

                reply = QtGui.QMessageBox.question(self, 'Confirmation', "Are you sure to stop this roasting Session?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

                if reply == QtGui.QMessageBox.Yes:
                    print("Start Stop")
                    # arduino.close()
                    self.savePref()
                    self.current_temp = self.temp_label.text().split(":")
                    self.current_tbl.setItem(5, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
                    self.current_tbl.setItem(5, 0, QtGui.QTableWidgetItem(
                        str(self.minute_count) + ":" + str(self.second_count)))
                    self.timer.stop()
                    self.timer.disconnect(self.timer, QtCore.SIGNAL('timeout()'), self.update)
                    self.timer_thread.stop()
                    self.arduino.disconnect()
                    # self.setVisible(False)
                    print'arduino port closed'
                    # self.dock_widget.endRoast()



                elif reply == QtGui.QMessageBox.No:
                    pass

    # first crack fucntion
    def fcrack(self):

        self.temp_first_crack_data[-1] = float(240)
        self.roc_first_crack_data[-1] = float(0.3)
        self.current_temp = self.temp_label.text().split(":")
        self.current_tbl.setItem(1, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(1, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))
        self.first_crack_bool = True
        self.fcrack_time_s = self.minute_count * 60 + self.second_count

        print 'First Crack'

    # second crack function
    def scrack(self):
        self.current_temp = self.temp_label.text().split(":")
        self.temp_second_crack_data[-1] = float(240)
        self.roc_second_crack_data[-1] = float(0.3)
        self.current_tbl.setItem(2, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(2, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))

        print 'Second Crack'

    # turning point function
    def turn(self):
        self.current_temp = self.temp_label.text().split(":")
        self.temp_tp_data[-1] = float(240)
        self.roc_tp_data[-1] = float(0.3)
        self.current_tbl.setItem(3, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(3, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))

        print 'Turning point'

    # drop out function
    def drop(self):
        self.current_temp = self.temp_label.text().split(":")
        self.temp_drop_out_data[-1] = float(240)
        self.roc_drop_out_data[-1] = float(0.3)
        self.current_tbl.setItem(4, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(4, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))
        self.first_crack_bool = False

        print"Drop Out"

    # gas level change function
    def gas(self, event):
        self.gas_slider.setFocus(True)

        air_gas_dialog = BorderLessDiaglogs(self, "gas")
        air_gas_dialog.exec_()
        air_gas_dialog.show()
        air_gas_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        b_font = QtGui.QFont()
        b_font.setBold(True)
        self.gas_slider_label.setFont(b_font)
        b_font.setBold(False)
        self.air_slider_label.setFont(b_font)

    # air level change funciton
    def air(self):
        self.air_slider.setFocus(True)

        air_gas_dialog = BorderLessDiaglogs(self, "air")
        air_gas_dialog.exec_()
        air_gas_dialog.show()
        air_gas_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        b_font = QtGui.QFont()
        b_font.setBold(True)
        self.air_slider_label.setFont(b_font)
        b_font.setBold(False)
        self.gas_slider_label.setFont(b_font)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    splash = QtGui.QSplashScreen(QPixmap((os.path.expanduser("~/Roastery/loading.png"))))
    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    splash.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    splash.show()

    window = Window()
    # window.connect()
    app.processEvents()

    splash.finish(window.connect())

    QtGui.QApplication.restoreOverrideCursor()
    app.setApplicationName('Roastery')
    os.system("defaults write com.SVT.Roastery NSAppSleepDisabled -bool YES")
    window.show()

    sys.exit(app.exec_())
