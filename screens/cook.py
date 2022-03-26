##############################################
# cook.py
#
# CookScreen Module for microwave project
# date: 3/6/22
# author: hdonahue
##############################################

import logging
from PySide6 import QtWidgets, QtCore, QtGui

logging.basicConfig(level=logging.DEBUG, format="%(filename)s[%(levelname)s]:%(lineno)s - %(message)s")

STATE_IDLE = 0
STATE_ENTER_TIME = 1
STATE_COOKING = 2

##################################
# Class: CookScreen
# 
# Desc: Microwave main screen showing
#       keypad and quick selects.
##################################
class CookScreen(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.state = STATE_IDLE
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
        self.setStyleSheet(open("style/cook.css", 'r').read())
        
        # Screen widgets
        self.label_cook_time = QtWidgets.QLabel(self, objectName="cook_time")
        self.label_cook_time.setAlignment(QtCore.Qt.AlignCenter)

        self.keypad = Keypad(self)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label_cook_time)
        self.layout.addStretch(0)
        self.layout.addWidget(self.keypad)

        self.keypad.key_pressed.connect(self.screen_pressed)
        self.keypad.key_pressed.connect(self.handle_keypad_press)
        
    """
    method: handleKeyPress
    brief: handle keypad presses and update UI
    """
    @QtCore.Slot(str)
    def handle_keypad_press(self, key: str):
        if(type(key) is not str):
            logging.error("%s is not an accepted type" % str(key))
            return
        if(self.state is STATE_IDLE):
            self.state = STATE_ENTER_TIME
            if(key != "start" and key != "stop"):
                self.label_cook_time.setText("00:0" + key)
                self.label_cook_time.setVisible(True)
        elif(self.state is STATE_ENTER_TIME):
            if(key.isdecimal() and 
                (int(key) >= 0 and int(key) < 10) ):

                old_cook_time = self.label_cook_time.text()
                cook_time = old_cook_time[1] + old_cook_time[3] + ':' + old_cook_time[4] + key
                self.label_cook_time.setText(cook_time)
            elif(key == "start"):
                self.state = STATE_COOKING
                self.cook_time_changed.emit(self.label_cook_time.text())
            elif(key == "stop"):
                self.state = STATE_IDLE
                self.label_cook_time.setVisible(False)



    ############################
    #         Signals          #
    ############################
    screen_pressed = QtCore.Signal()    
    cook_time_changed = QtCore.Signal(str)

    ############################
    #          Slots           #
    ############################

    ##########################
    #     Private Members    #
    ##########################



##################################
# Class: Keypad
# 
# Desc: Keypad interface for setting
#       cook time, clock and timers.
#
#    1 | 2 | 3
#   -----------
#    4 | 5 | 6
#   -----------
#    7 | 8 | 9
#   -----------
#    C | 0 | S
###################################
class Keypad(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setup_ui()

    """
    method: setup_ui
    brief: declare and init child widgets
    """
    def setup_ui(self):
        # Declare child keys
        self.button_0 = QtWidgets.QPushButton("0", self)
        self.button_1 = QtWidgets.QPushButton("1", self)
        self.button_2 = QtWidgets.QPushButton("2", self)
        self.button_3 = QtWidgets.QPushButton("3", self)
        self.button_4 = QtWidgets.QPushButton("4", self)
        self.button_5 = QtWidgets.QPushButton("5", self)
        self.button_6 = QtWidgets.QPushButton("6", self)
        self.button_7 = QtWidgets.QPushButton("7", self)
        self.button_8 = QtWidgets.QPushButton("8", self)
        self.button_9 = QtWidgets.QPushButton("9", self)
        self.button_stop = QtWidgets.QPushButton("Clear", self)
        self.button_start = QtWidgets.QPushButton("Start", self)
        # Set layout and add keys
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.button_0, 3, 1)
        self.layout.addWidget(self.button_1, 0, 0)
        self.layout.addWidget(self.button_2, 0, 1)
        self.layout.addWidget(self.button_3, 0, 2)
        self.layout.addWidget(self.button_4, 1, 0)
        self.layout.addWidget(self.button_5, 1, 1)
        self.layout.addWidget(self.button_6, 1, 2)
        self.layout.addWidget(self.button_7, 2, 0)
        self.layout.addWidget(self.button_8, 2, 1)
        self.layout.addWidget(self.button_9, 2, 2)
        self.layout.addWidget(self.button_stop, 3, 0)
        self.layout.addWidget(self.button_start, 3, 2)
        self.layout.setSpacing(25)
        logging.debug("keypad created")
        #connect signals
        self.keypad_map = QtCore.QSignalMapper(self)
        self.set_keypad_mappings()
        

    """
    method: set_keypad_mappings
    brief: map key signals
    """
    def set_keypad_mappings(self):
        
        # QtCore.QObject.connect(self.keypad_map, QtCore.SIGNAL("mappedInt()"), self, QtCore.SLOT("handle_key_press()"))
        self.keypad_map.mappedString.connect(self.handle_key_press)

        self.button_0.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_0, "0")
        
        self.button_1.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_1, "1")
        
        self.button_2.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_2, "2")
        
        self.button_3.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_3, "3")
        
        self.button_4.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_4, "4")
        
        self.button_5.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_5, "5")
        
        self.button_6.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_6, "6")
        
        self.button_7.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_7, "7")
        
        self.button_8.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_8, "8")
        
        self.button_9.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_9, "9")
        
        self.button_start.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_start, "start")
        
        self.button_stop.clicked.connect(self.keypad_map.map)
        self.keypad_map.setMapping(self.button_stop, "stop")
        

    ############################
    #         Signals          #
    ############################
    key_pressed = QtCore.Signal(str)

    @QtCore.Slot(str)
    def handle_key_press(self, key):
        logging.info("button pressed %s" % str(key))
        self.key_pressed.emit(str(key))


