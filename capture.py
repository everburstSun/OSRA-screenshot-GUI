from window import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
import sys, os


class MyWindow(Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.new = Ui_Form()
        self.setupUi(self)
        self.prefix = 1000
        self.pushButton.clicked.connect(ShowFullScreenshot)
        self.plainTextEdit.setPlainText("1000")
        self.show()


class FullScreenshot(QtWidgets.QWidget):
    def __init__(self):
        super(FullScreenshot, self).__init__()
        self.start_x, self.start_y, self.end_x, self.end_y = 0, 0, 0, 0
        self.PNGpath = "/Users/simon/research/COPD/PNGs/"
        self.SDFpath = "/Users/simon/research/COPD/SDFs/"
        self.flag = False
        self.setCursor(Qt.CrossCursor)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("screenshot")
        desktop = QtWidgets.QDesktopWidget()
        r = desktop.screenGeometry(desktop.screenNumber())
        self.setGeometry(r)
        self.screen = QApplication.primaryScreen()
        self.pixmap = self.screen.grabWindow(0)

    def swap(self, p1, p2):
        return p2, p1

    def mouseMoveEvent(self, event):
        if self.flag:
            self.end_x, self.end_y = event.x(), event.y()
            self.update()

    def mousePressEvent(self, event):
        self.flag = True
        self.start_x, self.start_y = event.x(), event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False
        self.end_x, self.end_y = event.x(), event.y()
        if (self.start_x - self.end_x) * (self.start_y - self.end_y):
            if self.start_x > self.end_x:
                self.start_x, self.end_x = self.swap(self.start_x, self.end_x)
            if self.start_y > self.end_y:
                self.start_y, self.end_y = self.swap(self.start_y, self.end_y)
            subshot = self.screen.grabWindow(self.winId(),self.start_x, self.start_y,
                                                         (self.end_x - self.start_x),
                                                         (self.end_y - self.start_y))
            subshot.save(self.PNGpath + "%d.png" % myshow.prefix, "png")
            os.system("/usr/local/bin/osra %(png)s%(pref)d.png -f sdf -w %(sdf)s%(pref)d.sdf"
                                                          % {"png": self.PNGpath,
                                                             "pref": myshow.prefix,
                                                             "sdf": self.SDFpath})
            self.close()
            myshow.prefix += 1
            myshow.plainTextEdit.setPlainText(str(myshow.prefix))

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.start_x-1, self.start_y-1, abs(self.start_x - self.end_x)+2, abs(self.start_y - self.end_y)+2)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        painter.drawRect(rect)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


def ShowFullScreenshot():
    fullscreen.start_x, fullscreen.start_y, fullscreen.end_x, fullscreen.end_y = 0, 0, 0, 0
    fullscreen.update()
    myshow.prefix = int(myshow.plainTextEdit.toPlainText())
    fullscreen.screen = QApplication.primaryScreen()
    fullscreen.pixmap = fullscreen.screen.grabWindow(0)
    palette1 = QPalette()
    palette1.setBrush(fullscreen.backgroundRole(), QBrush(fullscreen.pixmap))
    fullscreen.setPalette(palette1)
    fullscreen.setAutoFillBackground(True)
    fullscreen.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()     # construct and show the window
    fullscreen = FullScreenshot()
    sys.exit(app.exec_())