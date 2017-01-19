from pyqtgraph.Qt import QtGui, QtCore

class MultiWindows(QtGui.QMainWindow):

    def __init__(self):
        self.__windows = []

    def addwindow(self, window):
        self.__windows.append(window)

    def show(self):
        for current_child_window in self.__windows:
             current_child_window.exec_() # probably show will do the same tri