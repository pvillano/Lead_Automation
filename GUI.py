# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI1.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost! lmao
from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
import UnifiedRun
import RobotControl
import _thread
from time import sleep

MODES = {"Filters": 1, "Test Kits": 0, "Soil Samples": 2}


class SampleDisplay(object):
    def __init__(self, disp):
        self.disp = disp

    def create_initial(self):
        xPos = 10
        yPos = 10
        ret = {}
        for i in range(1, 31):
            ret[i] = {
                "selected": False,
                "tested": False,
                "valid": True,
                "x": xPos,
                "y": yPos,
            }
            xPos += 30
            if xPos > 70:
                xPos = 10
                yPos += 30
        return ret

    def paintSample(self, sample, p, f, number):
        cX = sample["x"]
        cY = sample["y"]
        if not sample["selected"]:
            p.setPen(QtGui.QPen(QtCore.Qt.lightGray, 2))
        else:
            if sample["tested"]:
                if sample["valid"]:
                    p.setPen(QtGui.QPen(QtCore.Qt.green, 2))
                else:
                    p.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            else:
                p.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        p.drawEllipse(cY, cX, 20, 20)
        p.drawText(cY, cX, 20, 20, QtCore.Qt.AlignCenter, str(number))


class SampleDisplayBag(SampleDisplay):
    """
    individual sample display
    """

    def __init__(self, disp):
        super(SampleDisplayBag, self).__init__(disp)

    def create_initial(self):
        xPos = 10
        yPos = 10
        ret = {}
        for i in range(1, 9):
            ret[i] = {
                "selected": False,
                "tested": False,
                "valid": True,
                "x": xPos,
                "y": yPos,
            }
            yPos += 37.5
        return ret

    def paintSample(self, sample, p, f, number):
        cX = sample["x"]
        cY = sample["y"]
        if not sample["selected"]:
            p.setPen(QtGui.QPen(QtCore.Qt.lightGray, 2))
        else:
            if sample["tested"]:
                if sample["valid"]:
                    p.setPen(QtGui.QPen(QtCore.Qt.green, 2))
                else:
                    p.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            else:
                p.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        p.drawRect(cY, cX, 27.5, 80)
        p.drawText(cY, cX, 27.5, 80, QtCore.Qt.AlignCenter, str(number))


class TrayDisplay(QtWidgets.QWidget):
    """
    shows multiple samples
    """

    def __init__(self, parent):
        super(TrayDisplay, self).__init__(parent)
        self.samples = {}
        self.sampleType = SampleDisplay(self)
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
            self.sampleType.paintSample(self.samples[sample], p, f, sample)

    def setSampleType(self, t):
        if not self.locked:
            if 0 == t:
                self.sampleType = SampleDisplayBag(self)
            elif 1 == t:
                self.sampleType = SampleDisplay(self)
            self.populateSamples()

    def populateSamples(self):
        self.samples = self.sampleType.create_initial()
        self.update()

    def lockPositions(self):
        self.locked = True

    def unlockPositions(self):
        self.locked = False

    def enablePositions(self, number):
        if not self.locked:
            for sample in self.samples:
                if sample <= number:
                    self.samples[sample]["selected"] = True
                else:
                    self.samples[sample]["selected"] = False
            self.update()

    def testResults(self, sample, passed):
        if sample not in self.samples.keys():
            sample = sample % 8
            if sample == 0:
                sample = 8
        self.samples[sample]["tested"] = True
        self.samples[sample]["valid"] = passed
        self.update()

    def reset(self, number):
        self.populateSamples()
        self.enablePositions(number)


class GantryDisplay(QtWidgets.QFrame):
    """
    unused current position of sensor
    """

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
        center = QtCore.QRect(self.x - 3, self.y - 3, self.x + 3, self.y + 3)
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
        self.x = 390 - int(y) // 2
        self.y = 174 - int(x) * 2
        self.trueX = x
        self.trueY = y
        print(f"x={self.trueX:d},y={self.trueY:d}")
        self.update()


class dummySignal(QtCore.QObject):
    nextTray = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(dummySignal, self).__init__()


class Ui_MainWindow(object):
    """
    procedurally generated, layout of tray_display_widgets
    """

    def __init__(self):
        self.id_paste_box: Optional[QtWidgets.QPlainTextEdit] = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(706, 475)
        self.centraltray_display_widget = QtWidgets.QWidget(MainWindow)
        self.centraltray_display_widget.setObjectName("centraltray_display_widget")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centraltray_display_widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 281, 201))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.begin_run_button = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.begin_run_button.setAlignment(QtCore.Qt.AlignCenter)
        self.begin_run_button.setObjectName("begin_run_button")
        self.verticalLayout_2.addWidget(self.begin_run_button)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        # axle mode
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        # axle mode combo box
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)

        # Samples
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)

        # sample number
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)

        # checkbox
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.checkBox)

        # continuous mode
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)

        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.verticalLayout_2.addLayout(self.formLayout)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.start_or_next_tray_butt = QtWidgets.QPushButton(
            self.verticalLayoutWidget_2
        )
        self.start_or_next_tray_butt.setObjectName("start_or_next_tray_butt")
        self.horizontalLayout.addWidget(self.start_or_next_tray_butt)

        self.reset_or_end_run_butt = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.reset_or_end_run_butt.setObjectName("reset_or_end_run_butt")
        self.horizontalLayout.addWidget(self.reset_or_end_run_butt)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tray_display_widget = TrayDisplay(self.centraltray_display_widget)
        self.tray_display_widget.setGeometry(QtCore.QRect(330, 20, 311, 101))
        self.tray_display_widget.setObjectName("tray_display_widget")

        self.id_paste_label = QtWidgets.QLabel(self.centraltray_display_widget)
        self.id_paste_label.setObjectName("id_paste_label")
        self.id_paste_label.setGeometry(QtCore.QRect(330, 121 + 40, 311, 20))

        self.id_paste_box = QtWidgets.QPlainTextEdit(self.centraltray_display_widget)
        self.id_paste_box.setGeometry(QtCore.QRect(330, 121 + 20 + 40, 311, 200))
        self.id_paste_box.setObjectName("id_paste_box")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centraltray_display_widget)
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

        self.home_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.home_button.setObjectName("home_button")
        self.horizontalLayout_2.addWidget(self.home_button)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centraltray_display_widget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 706, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.spinBox.valueChanged["int"].connect(self.sampleNumberChanged)
        self.comboBox.currentTextChanged["QString"].connect(self.sampleTypeChanged)
        self.lineEdit.textEdited["QString"].connect(self.sampleNameChanged)
        self.reset_or_end_run_butt.clicked.connect(self.reset)
        self.start_or_next_tray_butt.clicked.connect(self.start)
        self.home_button.clicked.connect(self.sendHome)
        self.checkBox.stateChanged.connect(self.setContMode)
        self.run = None
        self.continuousMode = False
        self.reset()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.dSignal = dummySignal()
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.begin_run_button.setText(_translate("MainWindow", "Begin Run"))
        self.label.setText(_translate("MainWindow", "AXLE Mode"))
        # self.comboBox.setItemText(0, _translate("MainWindow", "Test Kits"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Filters"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Test Kits"))
        # self.comboBox.setItemText(2, _translate("MainWindow", "Soil Samples"))
        self.label_2.setText(_translate("MainWindow", "Samples"))
        self.label_3.setText(_translate("MainWindow", "Run Name"))
        self.lineEdit.setText(_translate("MainWindow", "Filters1"))
        self.start_or_next_tray_butt.setText(_translate("MainWindow", "Start"))
        self.reset_or_end_run_butt.setText(_translate("MainWindow", "Reset"))
        self.label_4.setText(_translate("MainWindow", "Gantry Control"))
        self.label_6.setText(_translate("MainWindow", "Continuous Mode"))
        self.id_paste_label.setText(_translate("MainWindow", "Paste IDs Here"))
        self.home_button.setText(_translate("MainWindow", "Home"))

    def setContMode(self, i):
        if 2 == i:
            self.spinBox.setEnabled(False)
            self.continuousMode = True
            self.tray_display_widget.enablePositions(99)
        elif 0 == i:
            self.spinBox.setEnabled(True)
            self.continuousMode = False
            self.tray_display_widget.enablePositions(self.number)
        else:
            print("Error, invalid i = " + str(i))
        self.centraltray_display_widget.update()

    def sampleNumberChanged(self, i):
        self.number = i
        self.tray_display_widget.enablePositions(self.number)

    def sampleNameChanged(self, s):
        self.name = s

    def sampleTypeChanged(self, s):
        self.type = MODES[s]
        self.tray_display_widget.setSampleType(self.type)
        if not self.continuousMode:
            self.tray_display_widget.enablePositions(self.number)
        else:
            self.tray_display_widget.enablePositions(99)

    def reset(self):
        self.number = 1
        self.tray_display_widget.enablePositions(self.number)
        self.name = "Filters1"
        self.comboBox.setCurrentIndex(0)
        self.type = MODES[self.comboBox.currentText()]
        self.lineEdit.setText("Filters1")
        self.spinBox.setValue(1)

    def sendHome(self):
        self.lockButtons()
        self.centraltray_display_widget.update()
        try:
            _thread.start_new_thread(self.sendHomeThread, ())
        except Exception as e:
            print(e)

    def sendHomeThread(self):
        """
        print("Homing!")
        """
        if self.run is None:
            tempRobot = RobotControl.robotControl()
            tempRobot.home()
            tempRobot.close()
        else:
            self.run.robot.home()
        self.unLockButtons()
        self.centraltray_display_widget.update()

    def start(self):
        """
        where it all happens

        """
        print(self.type)
        print(self.number)
        print(self.name)
        self.setRunningButtons()
        self.checkBox.setEnabled(False)
        self.tray_display_widget.lockPositions()
        self.centraltray_display_widget.update()
        """
        try:
            _thread.start_new_thread(self.dummyRun, (3,))
        except Exception as e:
            print(e)
        """
        if self.run is None:
            self.run = UnifiedRun.unifiedRun(self)
            # connect to qt5 signals
            self.dSignal.nextTray.connect(self.run.cont)
            # self.run.robot.gant.positionChanged.connect(self.displayPosition)
            self.run.sampleStatusOK.connect(self.tray_display_widget.testResults)
            self.run.batchDone.connect(
                self.fullReEnable
            )  # unifiedrun will call this later
            self.run.trayDoneTime.connect(self.reEnable)
            self.run.pop_id.connect(self.pop_id)
        try:
            if not self.continuousMode:
                _thread.start_new_thread(
                    self.run.runBatch, (self.type, self.number, self.name)
                )
            else:
                _thread.start_new_thread(self.run.runBatch, (self.type, -1, self.name))
        except Exception as e:
            print(e)

    def pop_id(self):
        raw_id_str = self.id_paste_box.toPlainText()
        split_str = raw_id_str.split("\n", 1)  # "a b c" --> ["a", "b c"]
        if len(split_str) > 1:
            targetLabel, rest = split_str
        else:
            targetLabel, rest = raw_id_str, ""
        self.id_paste_box.setPlainText(rest)

    def setRunningButtons(self):
        self.start_or_next_tray_butt.setText("Next Tray")
        self.reset_or_end_run_butt.setText("End Run")
        self.lockButtons()

    def lockButtons(self):
        self.start_or_next_tray_butt.setEnabled(False)
        self.reset_or_end_run_butt.setEnabled(False)
        self.home_button.setEnabled(False)

    def unLockButtons(self):
        self.start_or_next_tray_butt.setEnabled(True)
        self.reset_or_end_run_butt.setEnabled(True)
        self.home_button.setEnabled(True)

    def dummyRun(self, number):
        valid = True
        for n in range(number):
            sleep(1)
            self.tray_display_widget.testResults(n + 1, valid)
            valid = not valid
            print(n, valid)
        sleep(1)
        self.fullReEnable()

    def reEnable(self, time):
        print("Re-enabling buttons, tray took " + str(time) + "s")
        self.start_or_next_tray_butt.disconnect()
        self.start_or_next_tray_butt.clicked.connect(self.nextTraySend)
        self.reset_or_end_run_butt.disconnect()
        self.reset_or_end_run_butt.clicked.connect(self.endContRun)
        self.tray_display_widget.unlockPositions()
        self.unLockButtons()
        self.centraltray_display_widget.update()

    def fullReEnable(self):
        self.start_or_next_tray_butt.setText("Start")
        self.reset_or_end_run_butt.setText("Reset")
        self.tray_display_widget.unlockPositions()
        if not self.continuousMode:
            self.tray_display_widget.reset(self.number)
        else:
            self.tray_display_widget.reset(99)
        self.checkBox.setEnabled(True)
        self.unLockButtons()
        self.centraltray_display_widget.update()

    def endContRun(self):
        self.start_or_next_tray_butt.disconnect()
        self.start_or_next_tray_butt.clicked.connect(self.start)
        self.reset_or_end_run_butt.disconnect()
        self.reset_or_end_run_butt.clicked.connect(self.reset)
        self.dSignal.nextTray.emit(False)
        self.fullReEnable()
        self.unLockButtons()
        self.centraltray_display_widget.update()

    def nextTraySend(self):
        self.lockButtons()
        if not self.continuousMode:
            self.tray_display_widget.reset(self.number)
        else:
            self.tray_display_widget.reset(99)
        self.dSignal.nextTray.emit(True)

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
