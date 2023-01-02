from Interface import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer,QTime,QDate
from PyQt5.uic import loadUiType
import AIMain
import sys
from Task import MainIntFaceFun
import os
import signal

class MainThread(QThread):

    def __init__(self):
        super(MainThread,self).__init__()


    def run(self):
        AIMain.Program_Main()  


startExe=MainThread()


class Gui_Start(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.gui = Ui_MainWindow()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.gui.setupUi(self)
        self.gui.StartButton.clicked.connect(self.startTask)
        self.gui.ExitButton.clicked.connect(self.Clos)

    def Clos(self):
        self.close()
        os.kill(os.getppid(), signal.SIGTERM)


    def startTask(self):

        self.gui.label1 = QtGui.QMovie("Earth.gif")
        self.gui.EarthGIF.setMovie(self.gui.label1)
        self.gui.label1.start()

        self.gui.label2 = QtGui.QMovie("GIF1Label.gif")
        self.gui.TimeGIF.setMovie(self.gui.label2)
        self.gui.label2.start()

        self.gui.label3 = QtGui.QMovie("GIF1Label.gif")
        self.gui.DateGIF.setMovie(self.gui.label3)
        self.gui.label3.start()

        self.gui.label4 = QtGui.QMovie("GIF1Label.gif")
        self.gui.DayGIF.setMovie(self.gui.label4)
        self.gui.label4.start()

        self.gui.label5 = QtGui.QMovie("Iron_Template_1.gif")
        self.gui.AIImageGIF.setMovie(self.gui.label5)
        self.gui.label5.start()

        self.gui.label6 = QtGui.QMovie("Jarvis_Gui (1).gif")
        self.gui.RoundGIF.setMovie(self.gui.label6)
        self.gui.label6.start()

        self.gui.label7 = QtGui.QMovie("exa.gif")
        self.gui.CommandLineDetails.setMovie(self.gui.label7)
        self.gui.label7.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTimeLive)
        timer.start(999)

        startExe.start()


    def showTimeLive(self):
        
        t_ime=QTime.currentTime()
        time=t_ime.toString()
        d_ate=QDate.currentDate()
        date =d_ate.toString()
        temp=str(MainIntFaceFun())
        

        self.gui.TimeTextBrowser.setText(time)
        self.gui.DateTextBrowser.setText(date)
        self.gui.DateTextBrowser_2.setText(temp+" Kelvin")

        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.gui.TimeTextBrowser.setFont(font)
        self.gui.TimeTextBrowser.setAlignment(QtCore.Qt.AlignCenter)

        font1 = QtGui.QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.gui.DateTextBrowser.setFont(font1)
        self.gui.DateTextBrowser.setAlignment(QtCore.Qt.AlignCenter)

        font2 = QtGui.QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        self.gui.DateTextBrowser_2.setFont(font2)
        self.gui.DateTextBrowser_2.setAlignment(QtCore.Qt.AlignCenter)




GuiApp = QApplication(sys.argv)
jarvis_gui = Gui_Start()
jarvis_gui.showMaximized()
exit(GuiApp.exec_())


