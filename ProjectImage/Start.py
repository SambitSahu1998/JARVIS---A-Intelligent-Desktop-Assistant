import sys
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QProcess, QTextCodec
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QPlainTextEdit

class ProcessOutputReader(QProcess):
    produce_output = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setProcessChannelMode(QProcess.MergedChannels)
        codec = QTextCodec.codecForLocale()
        self._decoder_stdout = codec.makeDecoder()
        self.readyReadStandardOutput.connect(self._ready_read_standard_output)
        
    @pyqtSlot()
    def _ready_read_standard_output(self):
        raw_bytes = self.readAllStandardOutput()
        text = self._decoder_stdout.toUnicode(raw_bytes)
        self.produce_output.emit(text)

class MyConsole(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(460,440)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.setFont(font)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: transparent;\n"
        "color: rgb(0, 170, 255);\n"
        "border-radius:none;")
        self.setMaximumBlockCount(10000)
        self._cursor_output = self.textCursor()
        self.setWindowFlag(Qt.FramelessWindowHint)


    @pyqtSlot(str)
    def append_output(self, text):
        self._cursor_output.insertText(text)
        self.scroll_to_last_line()

    def scroll_to_last_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else
                            QTextCursor.StartOfLine)
        self.setTextCursor(cursor)


    def mousePressEvent(self, event):
        self.oldPosition=event.globalPos()

    def mouseMoveEvent(self, event):
        delta=QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x()+delta.x(),self.y()+delta.y())
        self.oldPosition=event.globalPos()
        
        


GuiApp = QApplication(sys.argv)
reader = ProcessOutputReader()
console = MyConsole()
reader.produce_output.connect(console.append_output)
reader.start('python', ['-u', 'MainInterface.py'])  
console.show()
exit(GuiApp.exec_())                              

