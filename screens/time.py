##############################################
# time.py
#
# TimeScreen Module for microwave project
# date: 3/3/22
# author: hdonahue
##############################################

from importlib.metadata import PackagePath
import os
from PySide6 import QtWidgets, QtCore, QtGui

class TimeScreen(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setup_ui()
    
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        print("Pressed")
        self.screen_pressed.emit()

    def setup_ui(self):
        # self.setAutoFillBackground(True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True) # This is necessary to enable styled background for custom widget - https://stackoverflow.com/questions/57778434/set-background-colour-for-a-custom-qwidget
        self.setStyleSheet(open("style/time.css", 'r').read())
        
        # Screen widgets
        label_time = QtWidgets.QLabel(self.current_time, objectName="label_time")
        label_date = QtWidgets.QLabel(self.current_date, objectName="label_date")

        self.time_changed.connect(label_time.setText)
        self.date_changed.connect(label_date.setText)
        label_time.setAlignment(QtCore.Qt.AlignCenter)
        label_date.setAlignment(QtCore.Qt.AlignCenter)
        # Set layout and add widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.addSpacing(200) # Add spacing between top and time
        layout.addWidget(label_time)
        layout.setSpacing(0)
        layout.addWidget(label_date)
        layout.addStretch()
        
        self.show() #TODO: is this necessary?

    time_changed = QtCore.Signal(str)
    screen_pressed = QtCore.Signal()

    @QtCore.Slot(str)
    def set_time(self, current_time: str):
        self.current_time = current_time
        self.time_changed.emit(self.current_time)
        print("time changed")

    date_changed = QtCore.Signal(str)

    @QtCore.Slot(str)
    def set_date(self, current_date: str):
        self.current_date = current_date
        self.date_changed.emit(self.current_date)
        print("date changed")


    ##########################
    #     Class Variables    #
    ##########################

    current_time: str="12:00"
    current_date: str="Sun Jan 1"