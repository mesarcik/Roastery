from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtGui import QPixmap
import numpy as np
from RocDialog import RocDialog
from Dock_Widget import Dock_Widget
from TimeAxisItem import TimeAxisItem
from MultiWindows import MultiWindows
from SerialThread import SerialThread
import pyqtgraph as pg
import pyqtgraph.exporters
import sys
import csv
import os
import datetime
import time
import gc




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


current_bean =""


class ChildWindow(QtGui.QMainWindow):
    def __init__(self):
        super(ChildWindow, self).__init__()
        self.current_temp = []
        self.start_time = 0
        self.import_bool  = False

        self.new_window = None
        self.count = 0
        self.global_count = 0
        self.tp_bool = False

        self.temp_temp = []

        self.temp_data = []
        self.time_data = []
        self.roc_time_data = []
        self.gas_data = [0]
        self.air_data = []
        self.roc_data = []
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
        self.second_count_minus_1 = 0


        self.timer = QtCore.QTimer()

        self.t = QtCore.QTime()

        # Roc properties
        self.sampling_interval = None
        self.rocMethod = ''
        self.delta = None
        self.refresh_rate = None
        self.refresh_counter = 0
        self.tempSmooth =''
        self.initPref()

        self.beans = []

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
            self.roastPreflocation = '/home/RoastPref'

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


        self.dock_widget = Dock_Widget(self.top_right_layout, self.top_left_layout, self.bottom_layout, self.gas_slider, self.gas_slider_label, self.air_slider, self.air_slider_label, self,self)
        self.setCentralWidget(self.dock_widget)

        ##########################################

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

        print("EVERYTHING IS INITIALIZED")
        self.showMaximized()
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

    def setup_graph(self):

        if (self.import_bool):
            print("Impoort Bool is True")
            self.temp.close()
            self.roc.close()


        # GRAPHING ELEMENTS ###################################
        self.temp = pg.PlotWidget(title='Temperature vs. Time Graph',
                                  axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        # self.temp.addLegend(size=(110, 0), offset=(480, 130))
        # r(b, g, r, c, m, y, k, w)

        self.pen = pg.mkPen(color='c', width=1)
        self.gas_pen = pg.mkPen(color='m', width=1.5)
        self.fc_pen = pg.mkPen(color='r', width=1.5)
        self.sc_pen = pg.mkPen(color='y', width=1.5)
        self.tp_pen = pg.mkPen(color='w', width=1.5)
        self.do_pen = pg.mkPen(color='g', width=1.5)

        self.ipen = pg.mkPen(color='c', style=QtCore.Qt.DashLine, width=0.25)
        self.igas_pen = pg.mkPen(color='m', style=QtCore.Qt.DashLine, width=0.25)
        self.ifc_pen = pg.mkPen(color='r', style=QtCore.Qt.DashLine, width=0.25)
        self.isc_pen = pg.mkPen(color='y', style=QtCore.Qt.DashLine, width=0.25)
        self.itp_pen = pg.mkPen(color='w', style=QtCore.Qt.DashLine, width=0.25)
        self.ido_pen = pg.mkPen(color='g', style=QtCore.Qt.DashLine, width=0.25)

        self.temp_curve = self.temp.plot(pen=self.pen, name='Temperature')
        self.import_temp_curve = self.temp.plot(pen=self.ipen)

        self.temp_air_curve = self.temp.plot(pen=self.gas_pen, name='Air Flow')
        self.import_temp_air_curve = self.temp.plot(pen=self.igas_pen)
        self.temp_first_crack = self.temp.plot(pen=self.fc_pen, name='First Crack')
        self.import_temp_first_crack = self.temp.plot(pen=self.ifc_pen)
        self.temp_second_crack_curve = self.temp.plot(pen=self.sc_pen, name='Second Crack')
        self.import_temp_second_crack_curve = self.temp.plot(pen=self.isc_pen)
        self.temp_tp = self.temp.plot(pen=self.tp_pen, name='Turning Point')
        self.import_temp_tp_curve = self.temp.plot(pen=self.itp_pen)
        self.temp_drop_out = self.temp.plot(pen=self.do_pen, name='Drop Out')
        self.import_temp_drop_out_curve = self.temp.plot(pen=self.ido_pen)

        self.temp.setXRange(0, 1100000., padding=0)
        self.temp.setYRange(0, 255, padding=0)
        self.temp.showGrid(x=True, y=True, alpha=0.3)
        self.axis = TimeAxisItem(orientation='bottom')
        self.roc = pg.PlotWidget(title='RoC vs. Time Graph', axisItems={'bottom': self.axis})
        self.axis.setTickSpacing(100, 5155)
        self.roc.addLegend(size=(110, 0), offset=(480, 130))

        self.roc_curve = self.roc.plot(pen=self.pen, name='Rate of Change/Temperature')
        self.import_roc_curve = self.roc.plot(pen=self.ipen)

        self.roc_gas_curve = self.roc.plot(pen=self.gas_pen, name='Gas Level/Air Flow')
        self.import_roc_gas_curve = self.roc.plot(pen=self.igas_pen)

        self.roc_first_crack = self.roc.plot(pen=self.fc_pen, name='First Crack')
        self.import_roc_first_crack = self.roc.plot(pen=self.ifc_pen)

        self.roc_second_crack = self.roc.plot(pen=self.sc_pen, name='Second Crack')
        self.import_roc_second_crack = self.roc.plot(pen=self.isc_pen)

        self.roc_tp = self.roc.plot(pen=self.tp_pen, name='Turning Point')
        self.import_roc_tp_curve = self.roc.plot(pen=self.itp_pen)

        self.roc_drop_out = self.roc.plot(pen=self.do_pen, name='Drop Out')
        self.import_roc_drop_out_curve = self.roc.plot(pen=self.ido_pen)

        self.roc.setYRange(0, 0.31, padding=0)
        self.roc.setXRange(5000, 1100000, padding=0)

        self.roc.showGrid(x=True, y=True, alpha=0.3)
    def connect(self):
        self.arduino = SerialThread(9600, self, self.timer)

    def initUI(self):
        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit'), 'Terminate Application', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.quit)

        newWindowAction  = QtGui.QAction(QtGui.QIcon.fromTheme('new'), 'New Window', self)
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

        roc_pref_action = QtGui.QAction(QtGui.QIcon.fromTheme('somethingelse'), 'Change Preferences', self)
        # roc_pref_action.setShortcut('Ctrl+P')
        roc_pref_action.triggered.connect(self.rocPref)


        toolMenu.addAction(roc_pref_action)
        

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

    def showChildWindow(self):
            if (self.arduino.state == False):
                gc.collect()
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                start = time.time()
                splash = QtGui.QSplashScreen(QPixmap((os.path.expanduser("/~/Roastery/loading.png"))), QtCore.Qt.WindowStaysOnTopHint)
                splash.show()
                progressBar = QtGui.QProgressBar(splash)
                palette = QtGui.QPalette()
                palette.setColor(QtGui.QPalette.Highlight,QtGui.QColor(QtCore.Qt.red))

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



    def update(self):
        temp_time = time.time()

        line = self.arduino.readline()
        self.temp_temp.append(float(line))
        if(self.tempSmooth == "True"):
            try:
                self.temp_label.setText('        TEMP:' + str(round(float((self.temp_temp[-1] + self.temp_temp[-2] + self.temp_temp[-3]) / 3),2)))
                # print("This is self.count" + str(self.count))
            except:
                self.temp_label.setText('        TEMP:' + str(float(line)))
                self.count+=1
                pass
        else:
            self.temp_label.setText('        TEMP:' + str(float(line)))
            if(self.count <2):
                self.count += 1

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
            # print ("This is elasped time: " + str(time.time() - self.start_time) )

            try:
                if (self.first_crack_bool):
                    # print ("This is elasped time: " + str(self.minute_count*60 + self.second_count) )
                    # print("This is first crack time " + str( self.fcrack_time_s) )

                    dev_amount_s = (self.minute_count*60 + self.second_count) - self.fcrack_time_s
                    dev_percentage = (1-round(float((float(self.fcrack_time_s)/float((self.minute_count*60 + self.second_count)))),2))*100
                    self.dev_second_count +=1

                    if(self.dev_second_count == 60):
                        self.dev_minute_count +=1
                        self.dev_second_count =0

                    dev_amount_str = str(self.dev_minute_count) +":" + str(self.dev_second_count)
                    self.dev_label.setText("DEV: " + dev_amount_str +" | " +  str(dev_percentage) + "%")

                self.refresh_counter += 1

                if (self.refresh_counter == self.refresh_rate):
                    self.arduino.flushOutput()
                    self.arduino.flushInput()
                    self.refresh_counter = 0


                if(self.tp_bool == False):
                    if(len(self.roc_data) >10):
                        if(self.roc_data[-9]<0):
                            if(self.roc_data[-1] >0):
                                self.temp_tp_data[-1] = float(240)
                                self.roc_tp_data[-1] = float(0.3)
                                self.turn()
                                self.tp_bool = True

                if (self.count > 1):
                    try:

                        # print ("Time taken for a portion update(): " + str((time.time() - temp_time) % 60) + "s")
                        self.time_data.append(self.t.elapsed())
                        if (self.tempSmooth == "True"):
                            self.temp_data.append(
                                float((self.temp_temp[-1] + self.temp_temp[-2] + self.temp_temp[-3]) / 3))
                        else:
                            self.temp_data.append(float(line))

                        air_lvl = float(self.air_slider.value())

                        # self.temp_label.setText('        TEMP ' + str(float(line)))

                        self.air_data.append(air_lvl * 2.4)

                        self.global_count += 1

                        x_time = np.array(self.time_data)
                        y_temp = np.array(self.temp_data)
                        y_air = np.array(self.air_data)

                        self.temp_curve.setData(x=x_time, y=y_temp)
                        self.temp_air_curve.setData(x=x_time, y=y_air)
                        self.temp_first_crack.setData(x=x_time, y=np.array(self.temp_first_crack_data))
                        self.temp_second_crack_curve.setData(x=x_time, y=np.array(self.temp_second_crack_data))
                        self.temp_drop_out.setData(x=x_time, y=np.array(self.temp_drop_out_data))
                        self.temp_tp.setData(x=x_time, y=np.array(self.temp_tp_data))

                        self.temp_tp_data.append(float(0))
                        self.temp_first_crack_data.append((float(0)))
                        self.temp_second_crack_data.append((float(0)))
                        self.temp_drop_out_data.append(float(0))
                        self.count += 1
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        self.count += 1
                        pass


                if (len(self.temp_data)-3 > self.delta - 1):

                    if (self.rocMethod.__contains__('point')):  # Point Average
                        if (self.count > self.delta):
                            roc_temp = (self.temp_data[self.count] - self.temp_data[self.count - int(self.delta)]) / int(self.delta)
                        else:
                            roc_temp =0

                        self.roc_label.setText('ROC ' + str(round(roc_temp,2)))
                        self.roc_data.append(float(roc_temp))
                        self.roc_time_data.append(self.t.elapsed())
                        x_roc_time = np.array(self.roc_time_data)
                        y_roc_data = np.array(self.roc_data)
                        self.roc_curve.setData(x=x_roc_time, y=y_roc_data)
                        self.roc_first_crack.setData(x=x_roc_time, y=np.array(self.roc_first_crack_data))
                        self.roc_second_crack.setData(x=x_roc_time, y=np.array(self.roc_second_crack_data))
                        self.roc_drop_out.setData(x=x_roc_time, y=np.array(self.roc_drop_out_data))
                        self.roc_tp.setData(x=x_roc_time, y=np.array(self.roc_tp_data))
                        self.roc_gas_curve.setData(x=x_roc_time, y=np.array(self.gas_data))

                    if (self.rocMethod.__contains__('self')):  # Moving self Average
                        if (self.count > self.delta):
                            frame_tot = 0
                            for point in range(self.count-3 - int(self.delta+1), self.count-3):  #self.delta + 1 because it needs to go to zero
                                frame_tot += self.temp_data[point] - self.temp_data[point - 1]


                            roc_temp = frame_tot / self.delta
                        else:
                            roc_temp = 0
                        self.roc_label.setText('ROC ' + str(round(roc_temp,2))  )

                        self.roc_data.append(float(roc_temp))
                        self.roc_time_data.append(self.t.elapsed())
                        x_roc_time = np.array(self.roc_time_data)
                        y_roc_data = np.array(self.roc_data)
                        self.roc_curve.setData(x=x_roc_time, y=y_roc_data)
                        self.roc_first_crack.setData(x=x_roc_time, y=np.array(self.roc_first_crack_data))
                        self.roc_second_crack.setData(x=x_roc_time, y=np.array(self.roc_second_crack_data))
                        self.roc_drop_out.setData(x=x_roc_time, y=np.array(self.roc_drop_out_data))
                        self.roc_tp.setData(x=x_roc_time, y=np.array(self.roc_tp_data))
                        self.roc_gas_curve.setData(x=x_roc_time, y=np.array(self.gas_data))

                    self.roc_tp_data.append(float(0))
                    self.roc_first_crack_data.append((float(0)))
                    self.roc_second_crack_data.append((float(0)))
                    self.roc_drop_out_data.append(float(0))
                    self.gas_lvl = float(self.gas_slider.value())
                    self.gas_data.append(float((self.gas_lvl * 1.0) / 333.3333))

                # app.processEvents() /////////////////////////////////////MAY BE PROBLEMATIC



                if (len(self.temp_data) - 3< self.delta - 1):

                    self.roc_data.append(float(0))
                    self.roc_time_data.append(self.t.elapsed())
                    x_roc_time = np.array(self.roc_time_data)
                    y_roc_data = np.array(self.roc_data)

                    self.roc_curve.setData(x=x_roc_time, y=y_roc_data)
                    self.roc_first_crack.setData(x=x_roc_time, y=np.array(self.roc_first_crack_data))
                    self.roc_second_crack.setData(x=x_roc_time, y=np.array(self.roc_second_crack_data))
                    self.roc_drop_out.setData(x=x_roc_time, y=np.array(self.roc_drop_out_data))
                    self.roc_tp.setData(x=x_roc_time, y=np.array(self.roc_tp_data))
                    self.roc_gas_curve.setData(x=x_roc_time, y=np.array(self.gas_data))



                    self.roc_tp_data.append(float(0))
                    self.roc_first_crack_data.append((float(0)))
                    self.roc_second_crack_data.append((float(0)))
                    self.roc_drop_out_data.append(float(0))
                    self.gas_lvl = float(self.gas_slider.value())
                    self.gas_data.append(float((self.gas_lvl * 1.0) / 333.3333))


            except ():
                print "Unexpected error:", sys.exc_info()[0]
                pass



        # print ("Time taken for update(): " + str((time.time()-temp_time)% 60) + "s")


    def quit (self):
        self.close()

    def initPref(self):
        print'init Pref'

        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            pre_file = open('/home/Pref', 'r')

        elif sys.platform.startswith('darwin'):
            pre_file = open(os.path.expanduser("~/Roastery/Pref"), "r")

        line = pre_file.readline()

        while line != '':
            if (line.__contains__('sampling_interval')):
                val = line.split('=')
                self.sampling_interval = float(val[1])
            if (line.__contains__('rocMethod')):
                val = line.split('=')
                # print"This is val 1 " + val[1]
                self.rocMethod = str(val[1])
            if (line.__contains__('delta')):
                val = line.split('=')
                self.delta = float(val[1])
            if (line.__contains__('refresh_rate')):
                val = line.split('=')
                self.refresh_rate = float(val[1])
            if (line.__contains__('temp_smooth')):
                val = line.split('=')
                self.tempSmooth = str(val[1])
                # print("Temp smooth ::::" + str(val[1]) + "This is self.tempSmooth:: " + self.tempSmooth)
            line = pre_file.readline()

    def savePref(self):
        
        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            pref_file = open('/home/Pref', 'w')
            pref_file.write('sampling_interval =' + str(self.sampling_interval) + '\n')
            pref_file.write('rocMethod =' + str(self.rocMethod) + '\n')
            pref_file.write('delta =' + str(self.delta) + '\n')
            pref_file.write('refresh_rate =' + str(self.refresh_rate) + "\n")
            pref_file.write('temp_smooth=' + str(self.tempSmooth))
            pref_file.close()

        elif sys.platform.startswith('darwin'):
            pref_file =  open(os.path.expanduser("~/Roastery/Pref"), "w")
            pref_file.write('sampling_interval =' + str(self.sampling_interval) + '\n')
            pref_file.write('rocMethod =' + str(self.rocMethod) + '\n')
            pref_file.write('delta =' + str(self.delta) + '\n')
            pref_file.write('refresh_rate =' + str(self.refresh_rate)+"\n")
            pref_file.write('temp_smooth=' + str(self.tempSmooth))
            pref_file.close()


    def rocPref(self):
        roc_dialog = RocDialog(self,self.font)
        roc_dialog.setWindowTitle("Preference Dialog")
        roc_dialog.exec_()
        roc_dialog.show()
        roc_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.savePref()
        self.initPref()
        # self.timer.stop()
        # self.timer.start(self.sampling_interval)
        print'ROC PREF'

    def initBeans(self):
        with open(self.roastPreflocation, 'r') as f:
            line = f.readline()
            self.beans = line.split(',')
        self.setWindowTitle(str(self.beans[0]))
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

    def importAction(self):
        x = False
        rcount = 0
        ccount = 0
        fname = QtGui.QFileDialog.getExistingDirectory(self, 'Open file', '/home')
        tempFile = fname + '/Temp.csv'
        rocFile = fname + '/RoC.csv'
        # try:
        #   # self.setup_graph()
        #
        # except Exception:
        #     print("Boston we have a problem")
        #     print "Unexpected error:", sys.exc_info()[0]
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
                            rcount+=1
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



                        except Exception,e:
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
                    self.import_bool=True
                    self.setFocus()


        except Exception as e :
            print e
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You have not selected a roast data file')
            msgBox.setInformativeText('Please reopen import dialog and select correct file')
            msgBox.setWindowTitle("ERROR")
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()

            if ret == QtGui.QMessageBox.Ok:
                pass

    def addBean(self):
        bean_file = open(self.roastPreflocation, 'a')
        text, result = QtGui.QInputDialog.getText(self, "Add New Bean Dialog", "Please Enter New Bean Name")
        if result:
            bean_file.write(',' + text)
            bean_file.close()
        self.initBeans()

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
            if(not self.start_stop):
                self.current_temp = self.temp_label.text().split(":") 
                self.current_tbl.setItem(5, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
            self.current_tbl.setItem(5, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))
            self.timer.stop()
            export_dir = QtGui.QFileDialog.getExistingDirectory(self, 'Select Export Directory', '/home')
            self.setExportBean()
            self.directory = str(export_dir + "/" + self.directory)

            if not os.path.exists(self.directory):
                os.makedirs(self.directory)

            _tempFile = self.directory + '/Temp.csv'
            export_tempFile = open(_tempFile, 'w+')
            _rocFile = self.directory + '/RoC.csv'
            export_rocFile = open(_rocFile, 'w+')

            temp_writer = csv.writer(export_tempFile, dialect='excel')
            roc_writer = csv.writer(export_rocFile, dialect='excel')
            try:
                roc_writer.writerow(['Time', 'RoC', 'Gas', 'First' 'Crack Second', 'Crack Turning Point', 'Drop Out'])
                temp_writer.writerow(['Time', 'Temp', 'Air', 'First Crack', 'Second Crack', 'Turing Point', 'Drop Out'])

                for i in range(0, (len(self.temp_data) - 1)):
                    temp_writer.writerow(
                            [i, self.temp_data[i], self.air_data[i], self.temp_first_crack_data[i], self.temp_second_crack_data[i],
                             self.temp_tp_data[i], self.temp_drop_out_data[i]])

                for i in range(0, (len(self.roc_data) - 1)):
                    roc_writer.writerow([i, self.roc_data[i], self.gas_data[i], self.roc_first_crack_data[i], self.roc_second_crack_data[i],
                                         self.roc_tp_data[i], self.roc_drop_out_data[i]])
            except:
                print "Unexpected error:", sys.exc_info()[0]
                pass
            finally:
                try:


                    temp_writer.writerow(['Comments:'])
                    temp_writer.writerow(['', 'Time', 'Temp'])
                    temp_writer.writerow(['Roast Start', self.current_tbl.item(0, 0).text(), self.current_tbl.item(0, 1).text()])
                    temp_writer.writerow(['First Crack', self.current_tbl.item(1, 0).text(), self.current_tbl.item(1, 1).text()])
                    temp_writer.writerow(['Second Crack', self.current_tbl.item(2, 0).text(), self.current_tbl.item(2, 1).text()])
                    temp_writer.writerow(
                            ['Turning Point', self.current_tbl.item(3, 0).text(), self.current_tbl.item(3, 1).text()])
                    temp_writer.writerow(['Drop Out', self.current_tbl.item(4, 0).text(), self.current_tbl.item(4, 1).text()])
                    temp_writer.writerow(['Roast End', self.current_tbl.item(5, 0).text(), self.current_tbl.item(5, 1).text()])
                    temp_writer.writerow(['Development Time', str(self.dev_label.text()), ""])

                    roc_writer.writerow(['Comments:'])
                    roc_writer.writerow(['', 'Time', 'Temp'])
                    roc_writer.writerow(['Roast Start', self.current_tbl.item(0, 0).text(), self.current_tbl.item(0, 1).text()])
                    roc_writer.writerow(['First Crack', self.current_tbl.item(1, 0).text(), self.current_tbl.item(1, 1).text()])
                    roc_writer.writerow(['Second Crack', self.current_tbl.item(2, 0).text(), self.current_tbl.item(2, 1).text()])
                    roc_writer.writerow(['Turning Point', self.current_tbl.item(3, 0).text(), self.current_tbl.item(3, 1).text()])
                    roc_writer.writerow(['Drop Out', self.current_tbl.item(4, 0).text(), self.current_tbl.item(4, 1).text()])
                    roc_writer.writerow(['Roast End', self.current_tbl.item(5, 0).text(), self.current_tbl.item(5, 1).text()])
                    roc_writer.writerow(['Development Time', self.dev_label.text(), ""])
                    export_tempFile.close()
                    export_rocFile.close()
                    temp_exporter = pg.exporters.ImageExporter(self.temp.plotItem)
                    temp_exporter.export(self.directory + '/Temp.png')
                    roc_exporter = pg.exporters.ImageExporter(self.roc.plotItem)
                    roc_exporter.export(self.directory + '/RoC.png')
                    QPixmap.grabWidget(self).save(self.directory + '/screenshot.jpg', 'jpg')

                    

                    print("exported to: " + self.directory)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    pass

                finally:
                    self.timer.stop()
                    self.timer.disconnect(self.timer, QtCore.SIGNAL('timeout()'), self.update)
                    self.timer_thread.stop()
                    # self.timer_thread.disconnect(self.timer_thread, QtCore.SIGNAL('timeout()'), self.updateTime)
                    self.arduino.disconnect()
                    print'arduino port closed'
                    self.hide()
                    self.dock_widget.endRoast()


    def setExportBean(self):
        self.directory = self.beans[0] + '/' + self.directory

    def ss(self):
        global timer

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
                self.current_tbl.setItem(5, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))
                self.timer.stop()
                self.timer.disconnect(self.timer, QtCore.SIGNAL('timeout()'), self.update)
                self.timer_thread.stop()
                self.arduino.disconnect()
                self.setVisible(False)
                print'arduino port closed'
                # self.dock_widget.endRoast()



            elif reply == QtGui.QMessageBox.No:
                pass

    def fcrack(self):

        self.temp_first_crack_data[-1] = float(240)
        self.roc_first_crack_data[-1] = float(0.3)
        self.current_temp = self.temp_label.text().split(":") 
        self.current_tbl.setItem(1, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(1, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))
        self.first_crack_bool = True
        self.fcrack_time_s =  self.minute_count*60 + self.second_count

        print 'First Crack'

    def scrack(self):
        self.current_temp = self.temp_label.text().split(":")
        self.temp_second_crack_data[-1] = float(240)
        self.roc_second_crack_data[-1] = float(0.3)
        self.current_tbl.setItem(2, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(2, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))

        print 'Second Crack'

    def turn(self):
        self.current_temp = self.temp_label.text().split(":") 
        self.temp_tp_data[-1] = float(240)
        self.roc_tp_data[-1] = float(0.3)
        self.current_tbl.setItem(3, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(3, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))

        print 'Turning point'

    def drop(self):
        self.current_temp = self.temp_label.text().split(":") 
        self.temp_drop_out_data[-1] = float(240)
        self.roc_drop_out_data[-1] = float(0.3)
        self.current_tbl.setItem(4, 1, QtGui.QTableWidgetItem(str(float(self.current_temp[1]))))
        self.current_tbl.setItem(4, 0, QtGui.QTableWidgetItem(str(self.minute_count) + ":" + str(self.second_count)))
        self.first_crack_bool = False

        print"Drop Out"

    def gas(self, event):
        self.gas_slider.setFocus(True)
        b_font = QtGui.QFont()
        b_font.setBold(True)
        self.gas_slider_label.setFont(b_font)
        b_font.setBold(False)
        self.air_slider_label.setFont(b_font)

    def air(self):
        self.air_slider.setFocus(True)
        b_font = QtGui.QFont()
        b_font.setBold(True)
        self.air_slider_label.setFont(b_font)
        b_font.setBold(False)
        self.gas_slider_label.setFont(b_font)