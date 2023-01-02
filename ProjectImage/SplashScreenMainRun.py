import sys
import platform
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from splash_screen import Ui_MainWindow


counter=0

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)
        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter) 
        if counter>100:
            self.timer.stop()
            self.close()
            import os 
            os.system('python Start.py')
        counter += 1

        

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=SplashScreen()
    sys.exit(app.exec_())
   

          

