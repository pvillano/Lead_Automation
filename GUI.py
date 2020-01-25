# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI1.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import UnifiedRun
import RobotControl
import _thread
from time import sleep

MODES = {"Filters": 1, "Test Kits": 0, "Soil Samples": 2}

class TrayDisplay(QtWidgets.QWidget):
    def __init__(self, parent):
        super(TrayDisplay, self).__init__(parent)
        self.samples = {}
        self.populateSamples()
        self.unlockPositions()

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        r = event.rect()
        p.fillRect(r, QtGui.QBrush(QtCore.Qt.lightGray))
        p.setBrush(QtGui.QBrush(QtCore.Qt.darkGray, QtCore.Qt.SolidPattern))
        f = p.font()
        f.setBold(True)
        p.setFont(f)
        for sample in self.samples:
            cX = self.samples[sample]['x']
            cY = self.samples[sample]['y']
            if not self.samples[sample]['selected']:
                p.setPen(QtGui.QPen(QtCore.Qt.lightGray, 2))
            else:
                if self.samples[sample]['tested']:
                    if self.samples[sample]['valid']:
                        p.setPen(QtGui.QPen(QtCore.Qt.green, 2))
                    else:
                        p.setPen(QtGui.QPen(QtCore.Qt.red, 2))
                else:
                    p.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            p.drawEllipse(cY, cX, 20, 20)
            p.drawText(cY, cX, 20, 20, QtCore.Qt.AlignCenter, str(sample))


    def populateSamples(self):
        xPos = 10
        yPos = 10
        for i in range(1,31):
            self.samples[i] = {'selected':False, 'tested':False, 'valid':True, 'x':xPos, 'y':yPos}
            xPos += 30
            if xPos > 70:
                xPos = 10
                yPos += 30
        self.update()

    def lockPositions(self):
        self.locked = True

    def unlockPositions(self):
        self.locked = False

    def enablePositions(self, number):
        if not self.locked:
            for sample in self.samples:
                if sample <= number:
                    self.samples[sample]['selected'] = True
                else:
                    self.samples[sample]['selected'] = False
            self.update()

    def testResults(self, sample, passed):
        self.samples[sample]['tested'] = True
        self.samples[sample]['valid'] = passed
        self.update()

    def reset(self, number):
        self.populateSamples()
        self.enablePositions(number)


class GantryDisplay(QtWidgets.QFrame):
    def __init__(self, parent):
        super(GantryDisplay, self).__init__(parent)
        self.setGeometry(QtCore.QRect(270, 20, 391, 175))
        self.r = self.frameRect()
        print(self.r)
        self.updatePos(0, 0)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        r = event.rect()
        p.fillRect(r, QtGui.QBrush(QtCore.Qt.lightGray))
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(3)
        p.setPen(pen)
        center = QtCore.QRect(self.x-3,self.y-3, self.x+3, self.y+3)
        p.drawLine(self.horizontalLine)
        p.drawLine(QtCore.QPoint(self.x, r.top()), QtCore.QPoint(self.x, r.bottom()))
        p.drawLine(QtCore.QPoint(r.left(), self.y), QtCore.QPoint(r.right(), self.y))
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(5)
        p.setPen(pen)
        p.drawPoint(QtCore.QPoint(self.x, self.y))
        pen = QtGui.QPen(QtCore.Qt.yellow)
        pen.setWidth(4)
        p.setPen(pen)
        p.drawPoint(QtCore.QPoint(self.x, self.y))

    def updatePos(self, x, y):
        self.x = 390-int(y)/2
        self.y = 174-int(x)*2
        self.trueX = x
        self.trueY = y
        print("x=%d,y=%d" %(self.trueX, self.trueY))
        self.update()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(706, 475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 281, 201))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.widget = TrayDisplay(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(330, 20, 311, 101))
        self.widget.setObjectName("widget")
        self.widget.enablePositions(1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 230, 281, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 706, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        self.spinBox.valueChanged['int'].connect(self.sampleNumberChanged)
        self.comboBox.currentTextChanged['QString'].connect(self.sampleTypeChanged)
        self.lineEdit.textEdited['QString'].connect(self.sampleNameChanged)
        self.pushButton_2.clicked.connect(self.reset)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_4.clicked.connect(self.sendHome)
        self.run = None
        self.reset()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "Begin Run"))
        self.label.setText(_translate("MainWindow", "AXLE Mode"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Filters"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Test Kits"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Soil Samples"))
        self.label_2.setText(_translate("MainWindow", "Samples"))
        self.label_3.setText(_translate("MainWindow", "Run Name"))
        self.lineEdit.setText(_translate("MainWindow", "Filters1"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.setText(_translate("MainWindow", "Reset"))
        self.label_4.setText(_translate("MainWindow", "Gantry Control"))
        self.pushButton_4.setText(_translate("MainWindow", "Home"))

    def sampleNumberChanged(self, i):
        self.number = i
        self.widget.enablePositions(self.number)

    def sampleNameChanged(self, s):
        self.name = s

    def sampleTypeChanged(self, s):
        self.type = MODES[s]

    def reset(self):
        self.type = MODES["Filters"]
        self.number = 1
        self.name = "Filters1"
        self.comboBox.setCurrentIndex(0)
        self.lineEdit.setText("Filters1")
        self.spinBox.setValue(1)

    def displayPosition(self, x, y):
        self.frame.updatePos(float(x), float(ys))
        self.centralwidget.repaint()

    def sendHome(self):
        self.lockButtons()
        self.centralwidget.update()
        try:
            _thread.start_new_thread(self.sendHomeThread, (,))
        except Exception as e:
            print(e)
        self.unLockButtons()
        self.centralwidget.update()

    def sendHomeThread(self):
        if self.run is None:
            tempRobot = RobotControl.robotControl()
            tempRobot.home()
            tempRobot.close()
        else:
            self.run.robot.home()

    def start(self):
        print(self.type)
        print(self.number)
        print(self.name)
        self.pushButton.setText("Running...")
        self.lockButtons()
        self.widget.lockPositions()
        self.centralwidget.update()
        '''
        try:
            _thread.start_new_thread(self.dummyRun, (3,))
        except Exception as e:
            print(e)
        '''
        if self.run is None:
            self.run = UnifiedRun.unifiedRun()
            #self.run.robot.gant.positionChanged.connect(self.displayPosition)
            self.run.sampleStatusOK.connect(self.widget.testResults)
            self.run.batchDone.connect(self.reEnable)
        try:
            _thread.start_new_thread(self.run.runBatch, (self.type, self.number, self.name))
        except Exception as e:
            print(e)

    def lockButtons(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)

    def unLockButtons(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def dummyRun(self, number):
        valid = True
        for n in range(number):
            sleep(1)
            self.widget.testResults(n+1, valid)
            valid = not valid
            print(n, valid)
        sleep(1)
        self.reEnable()

    def reEnable(self):
        print("Re-enabling buttons")
        self.pushButton.setText("Start")
        self.unLockButtons()
        self.widget.unlockPositions()
        self.widget.reset(self.number)
        self.centralwidget.update()

    def closeEvent(self, event):
        if self.run is not None:
            self.run.close()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

