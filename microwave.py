############################################
# Project: Microwave
#
# Microwave project demonstrates a dynamic
# UI through a microwave application that
# adjusts it's top level widgets according 
# most use. 
#
# Desc: Main entry point
# Date: 3/3/2022
# Author: hdonahue
############################################

from datetime import datetime
import sys
import logging
from PySide6 import QtWidgets, QtCore, QtGui
from screens.time import TimeScreen

logging.basicConfig(level=logging.DEBUG, format="%(filename)s[%(levelname)s]:%(lineno)s - %(message)s")

DEFAULT_QUICK_PICK = ["Clock", "Timer", "Recipe"]
UPDATE_TIME_INTERVAL: int = 1000
USER_IDLE_INTERVAL: int = 10000
SCREEN_INDEX_IDLE = 0 # Time Screen
SCREEN_INDEX_MAIN = 1 # Main Screen



##################################
# Class: Microwave
# 
# Desc: Application root widget
#       and business logic.
##################################
class Microwave(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.start_time_update()

    ############################
    #         Members          #
    ############################

    """
    method: setup_ui
    brief: configure the UI and intialize timers and business logic members
    """
    def setup_ui(self):        
        # Widgets
        self.screen_time = TimeScreen(self)
        self.next_screen = QtWidgets.QWidget(self)
        # Timers
        self.timer_update_time = QtCore.QTimer(self)
        self.timer_idle = QtCore.QTimer(self)
        # Configure StackWidget (inherited)
        self.setGeometry(100,100,480,640)
        self.addWidget(self.screen_time)
        self.addWidget(self.next_screen)
        # Connect Signals/Slots
        self.screen_time.screen_pressed.connect(self.user_wake)
        # Initialize time
        self.screen_time.set_time(self.get_time())
        self.screen_time.set_date(self.get_date())
    
    """
    method: mousePressEvent (override)
    brief: trigger singleshot idle timer on press events to kick go_idle
    """
    def mousePressEvent(self, event):
        if(self.timer_idle.isActive()):
            self.timer_idle.stop()
        self.timer_idle.singleShot(USER_IDLE_INTERVAL, self.go_idle)
        logging.debug("Wake")

    """
    method: get_time
    brief: return the current time in specified string format
    """
    def get_time(self):
        f = "%I:%M"
        if(self.settings_time_format == "24"):
            f = "%I:%M" #TODO: Change this to correct format
        elif(self.settings_time_format == "12"):
            pass
        else:
            self.settings_time_format = "12" # Default to 12
        return datetime.now().strftime(f)

    """
    method: get_date
    brief: return the current date in specified string format
    """
    def get_date(self):
        f = "%a %b %d"
        return datetime.now().strftime(f)

    """
    method: start_time_update
    brief: start the continous timer for updating the current time and date
    """
    def start_time_update(self):
        self.timer_update_time.setInterval(UPDATE_TIME_INTERVAL)
        self.timer_update_time.setSingleShot(False)
        self.timer_update_time.timeout.connect(self.update_datetime)
        self.timer_update_time.start()

    ############################
    #      Member Slots        #
    ############################
    
    """
    slot: user_wake
    brief: move from Idle screen to 
    """
    @QtCore.Slot()
    def user_wake(self):
        self.setCurrentIndex(SCREEN_INDEX_MAIN)
        logging.info("User Wake")

    """
    slot: update_datetime
    brief: Update time & date members and refresh time screen 
    """
    @QtCore.Slot()            
    def update_datetime(self):
        self.current_time = self.get_time()
        self.current_date = self.get_date()
        self.screen_time.set_time(self.current_time)
        self.screen_time.set_date(self.current_date)
  
    """
    slot: go_idle
    brief: return to idle screen (time screen)
    """
    @QtCore.Slot()
    def go_idle(self):
        self.setCurrentIndex(SCREEN_INDEX_IDLE)
        logging.info("Going Idle")


    ############################
    #      Private Members     #
    ############################
    quick_pick_widgets = DEFAULT_QUICK_PICK # List of options for quick pick
    settings_time_format = "12"             # Time format stored in settings TODO: move this to a settings class
    current_time: str="12:00"               # Current Time string
    current_date: str="Sun Jan 1"           # Current Date string




if __name__ == "__main__":
    app = QtWidgets.QApplication()
    micro = Microwave()
    micro.show()
    sys.exit(app.exec())