# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI1.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
#import UnifiedRun
#import RobotControl
import _thread
from time import sleep

MODES = {"Filters": 1, "Test Kits": 0, "Soil Samples": 2}

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
        #p.drawLine(QtCore.QPoint(self.x, r.top()), QtCore.QPoint(self.x, r.bottom()))
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
        self.horizontalLine = QtCore.QLine(QtCore.QPoint(self.x, self.r.top()), QtCore.QPoint(self.x, self.r.bottom()))
        self.update()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(706, 475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 241, 155))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
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
        self.frame = GantryDisplay(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
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

    def sampleNumberChanged(self, i):
        self.number = i

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
        self.frame.updatePos(float(x), float(y))
        self.centralwidget.repaint()

    def start(self):
        print(self.type)
        print(self.number)
        print(self.name)
        self.pushButton.setText("Running...")
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.centralwidget.repaint()
        sleep(2)
        self.displayPosition(10,10)
        sleep(2)
        self.displayPosition(50,50)
        self.reEnable()
        '''
        if self.run is None:
            self.run = UnifiedRun.unifiedRun()
            self.run.robot.gant.positionChanged.connect(self.displayPosition)
            self.run.batchDone.connect(self.reEnable)
        try:
            _thread.start_new_thread(self.run.runBatch, (self.type, self.number, self.name))
        except Exception as e:
            print(e)'''

    def reEnable(self):
        print("Re-enabling buttons")
        self.pushButton.setText("Start")
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.centralwidget.repaint()

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

