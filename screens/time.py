##############################################
# time.py
#
# TimeScreen Module for microwave project
# date: 3/3/22
# author: hdonahue
##############################################

from importlib.metadata import PackagePath
import logging
from PySide6 import QtWidgets, QtCore, QtGui

logging.basicConfig(level=logging.DEBUG, format="%(filename)s[%(levelname)s]:%(lineno)s - %(message)s")


##################################
# Class: TimeScreen
# 
# Desc: Microwave Idle screen showing
#       time and date.
##################################
class TimeScreen(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setup_ui()
    
    ############################
    #         Members          #
    ############################

    """
    override: mouseReleaseEvent
    brief: click handler.
    TODO: This could probably be moved to parent and track idle state
    """
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        logging.debug("Pressed")
        self.screen_pressed.emit()

    """
    method: setup_ui
    brief: configure the UI and intialize timers and business logic members
    """
    def setup_ui(self):
        # self.setAutoFillBackground(True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True) # This is necessary to enable styled background for custom widget - https://stackoverflow.com/questions/57778434/set-background-colour-for-a-custom-qwidget
        self.setStyleSheet(open("style/time.css", 'r').read())
        
        # Screen widgets
        self.label_time = QtWidgets.QLabel(self.current_time, objectName="label_time")
        self.label_date = QtWidgets.QLabel(self.current_date, objectName="label_date")
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_date.setAlignment(QtCore.Qt.AlignCenter)
        # Bind time and date members to label text
        self.time_changed.connect(self.label_time.setText)
        self.date_changed.connect(self.label_date.setText)
        # Set layout and add widgets
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addSpacing(200) # Add spacing between top and time
        self.layout.addWidget(self.label_time)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.label_date)
        self.layout.addStretch()
        


    ############################
    #         Signals          #
    ############################

    time_changed = QtCore.Signal(str)   # Emit on set_time
    screen_pressed = QtCore.Signal()    # 
    date_changed = QtCore.Signal(str)

    ############################
    #          Slots           #
    ############################

    """
    slot: set_time
    update current time and notify watchers
    """
    @QtCore.Slot(str)
    def set_time(self, current_time: str):
        self.current_time = current_time
        self.time_changed.emit(self.current_time)
        logging.debug("time changed")

    """
    slot: set_date
    brief: update current date and notify watchers
    """
    @QtCore.Slot(str)
    def set_date(self, current_date: str):
        self.current_date = current_date
        self.date_changed.emit(self.current_date)
        logging.debug("date changed")


    ##########################
    #     Private Members    #
    ##########################

    current_time: str="12:00"
    current_date: str="Sun Jan 1"