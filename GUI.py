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
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 670, 161))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButton_8 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_8.setObjectName("radioButton_8")
        self.gridLayout_2.addWidget(self.radioButton_8, 2, 6, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_2.addWidget(self.radioButton_3, 2, 0, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_2.addWidget(self.radioButton_5, 2, 2, 1, 1)
        self.radioButton_6 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout_2.addWidget(self.radioButton_6, 2, 3, 1, 1)
        self.radioButton_9 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_9.setObjectName("radioButton_9")
        self.gridLayout_2.addWidget(self.radioButton_9, 2, 9, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_2.addWidget(self.radioButton, 0, 0, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_2.addWidget(self.radioButton_4, 2, 1, 1, 1)
        self.radioButton_7 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_7.setObjectName("radioButton_7")
        self.gridLayout_2.addWidget(self.radioButton_7, 2, 4, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_2.addWidget(self.radioButton_2, 1, 0, 1, 1)
        self.radioButton_10 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_10.setObjectName("radioButton_10")
        self.gridLayout_2.addWidget(self.radioButton_10, 2, 8, 1, 1)
        self.radioButton_11 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_11.setObjectName("radioButton_11")
        self.gridLayout_2.addWidget(self.radioButton_11, 2, 7, 1, 1)
        self.radioButton_12 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_12.setObjectName("radioButton_12")
        self.gridLayout_2.addWidget(self.radioButton_12, 2, 5, 1, 1)
        self.radioButton_13 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_13.setObjectName("radioButton_13")
        self.gridLayout_2.addWidget(self.radioButton_13, 1, 1, 1, 1)
        self.radioButton_14 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_14.setObjectName("radioButton_14")
        self.gridLayout_2.addWidget(self.radioButton_14, 1, 2, 1, 1)
        self.radioButton_15 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_15.setObjectName("radioButton_15")
        self.gridLayout_2.addWidget(self.radioButton_15, 1, 3, 1, 1)
        self.radioButton_16 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_16.setObjectName("radioButton_16")
        self.gridLayout_2.addWidget(self.radioButton_16, 1, 4, 1, 1)
        self.radioButton_17 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_17.setObjectName("radioButton_17")
        self.gridLayout_2.addWidget(self.radioButton_17, 1, 5, 1, 1)
        self.radioButton_18 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_18.setObjectName("radioButton_18")
        self.gridLayout_2.addWidget(self.radioButton_18, 1, 6, 1, 1)
        self.radioButton_19 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_19.setObjectName("radioButton_19")
        self.gridLayout_2.addWidget(self.radioButton_19, 1, 7, 1, 1)
        self.radioButton_20 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_20.setObjectName("radioButton_20")
        self.gridLayout_2.addWidget(self.radioButton_20, 1, 8, 1, 1)
        self.radioButton_21 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_21.setObjectName("radioButton_21")
        self.gridLayout_2.addWidget(self.radioButton_21, 1, 9, 1, 1)
        self.radioButton_22 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_22.setObjectName("radioButton_22")
        self.gridLayout_2.addWidget(self.radioButton_22, 0, 9, 1, 1)
        self.radioButton_23 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_23.setObjectName("radioButton_23")
        self.gridLayout_2.addWidget(self.radioButton_23, 0, 8, 1, 1)
        self.radioButton_24 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_24.setObjectName("radioButton_24")
        self.gridLayout_2.addWidget(self.radioButton_24, 0, 7, 1, 1)
        self.radioButton_25 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_25.setObjectName("radioButton_25")
        self.gridLayout_2.addWidget(self.radioButton_25, 0, 6, 1, 1)
        self.radioButton_26 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_26.setObjectName("radioButton_26")
        self.gridLayout_2.addWidget(self.radioButton_26, 0, 5, 1, 1)
        self.radioButton_27 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_27.setObjectName("radioButton_27")
        self.gridLayout_2.addWidget(self.radioButton_27, 0, 4, 1, 1)
        self.radioButton_28 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_28.setObjectName("radioButton_28")
        self.gridLayout_2.addWidget(self.radioButton_28, 0, 3, 1, 1)
        self.radioButton_29 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_29.setObjectName("radioButton_29")
        self.gridLayout_2.addWidget(self.radioButton_29, 0, 2, 1, 1)
        self.radioButton_30 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_30.setObjectName("radioButton_30")
        self.gridLayout_2.addWidget(self.radioButton_30, 0, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
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

