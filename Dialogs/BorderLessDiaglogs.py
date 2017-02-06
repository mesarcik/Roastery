from pyqtgraph.Qt import QtGui, QtCore

class BorderLessDiaglogs(QtGui.QDialog):
    def __init__(self,window,gas_or_air,parent):
        super(BorderLessDiaglogs, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)


        self.window= window
        self.gas_or_air =gas_or_air
        #set font size
        self.font = QtGui.QFont()
        self.font.setPointSize(16)
        #set placeholder text and resize
        self.text = QtGui.QLineEdit("", self)
        self.text.setFont(self.font)
        self.text.setPlaceholderText("Enter Level")
        self.text.setMinimumSize(120,20)


        #ensure user can only enter doubles
        regexp = QtCore.QRegExp('^0*(?:[1-9][0-9]?|100)$') # regex expression from 0 - 100
        self.validator = QtGui.QRegExpValidator(regexp)
        self.text.setValidator(self.validator)
        self.resize(self.text.width(), self.text.height())


        # Connecting key events to functions
        self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self), QtCore.SIGNAL('activated()'),
                     self.Exit)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self), QtCore.SIGNAL('activated()'),
                     self.Return)
        self.installEventFilter(self)


        self.setFocus()
        self.show()

    def Exit(self):
        print"exit triggerd"
        self.close()

    def Return(self):
        print"returned"
        if (self.gas_or_air == "gas"):
            self.window.gas_slider.setValue(int(self.text.text()))
        else:
            self.window.air_slider.setValue(int(self.text.text()))
        self.close()

    # Gives focus to textedit when key is pressed
    def keyPressEvent(self, evt):
        self.text.setFocus()
        self.text.keyPressEvent(evt)

    def showEvent(self, event):
        if (self.gas_or_air == "gas"):
            point = self.window.gas_slider_label.rect().topLeft()
            global_point = self.window.gas_slider_label.mapToGlobal(point)
            self.move(global_point - QtCore.QPoint(self.width()-120,self.height() +30))
        else:
            point = self.window.air_slider_label.rect().topLeft()
            global_point = self.window.air_slider_label.mapToGlobal(point)
            self.move(global_point - QtCore.QPoint(self.width()-100, self.height()+30))
        super(BorderLessDiaglogs, self).showEvent(event)

    def eventFilter(self, object, event):
        try:
            if event.type() == QtCore.QEvent.WindowActivate or self.text.hasFocus():
                # print "widget window has gained focus"
                pass
            elif event.type() == QtCore.QEvent.WindowDeactivate or self.text.hasFocus():
                # print "widget window has lost focus"
                pass
            elif event.type() == QtCore.QEvent.FocusIn or self.text.hasFocus():
                # print "widget has gained keyboard focus"
                pass
            elif event.type() == QtCore.QEvent.FocusOut or self.text.hasFocus():
                # print "widget has lost keyboard focus"
                pass
                self.close()
        except:
            pass
        return super(BorderLessDiaglogs, self).eventFilter(object, event)

