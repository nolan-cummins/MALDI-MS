# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_v1aZXloL.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollBar,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1188, 559)
        self.actionSave_Directory = QAction(MainWindow)
        self.actionSave_Directory.setObjectName(u"actionSave_Directory")
        self.actionNano_Genie_M1920 = QAction(MainWindow)
        self.actionNano_Genie_M1920.setObjectName(u"actionNano_Genie_M1920")
        self.actionEZFlow_Push_1 = QAction(MainWindow)
        self.actionEZFlow_Push_1.setObjectName(u"actionEZFlow_Push_1")
        self.actionEZFlow_Push_2 = QAction(MainWindow)
        self.actionEZFlow_Push_2.setObjectName(u"actionEZFlow_Push_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_15 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(640, 400))
        self.frame.setMaximumSize(QSize(640, 400))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(300, 200, 55, 16))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_15.addWidget(self.frame)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        font = QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_6.addWidget(self.checkBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.horizontalScrollBar_5 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_5.setObjectName(u"horizontalScrollBar_5")
        self.horizontalScrollBar_5.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.horizontalScrollBar_5)

        self.spinBox_5 = QSpinBox(self.centralwidget)
        self.spinBox_5.setObjectName(u"spinBox_5")

        self.horizontalLayout_5.addWidget(self.spinBox_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_7.addWidget(self.label_10)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_11)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCheckable(True)

        self.verticalLayout_2.addWidget(self.pushButton)


        self.horizontalLayout_8.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_3)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.label_12)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_13.addWidget(self.checkBox_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_9.addWidget(self.label_13)

        self.horizontalScrollBar_6 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_6.setObjectName(u"horizontalScrollBar_6")
        self.horizontalScrollBar_6.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_9.addWidget(self.horizontalScrollBar_6)

        self.spinBox_6 = QSpinBox(self.centralwidget)
        self.spinBox_6.setObjectName(u"spinBox_6")

        self.horizontalLayout_9.addWidget(self.spinBox_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_10.addWidget(self.label_14)

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.label_15)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setCheckable(True)

        self.verticalLayout_3.addWidget(self.pushButton_2)


        self.horizontalLayout_8.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.gridLayout.addLayout(self.verticalLayout_4, 2, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_8)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_16)

        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_12.addWidget(self.checkBox_3)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalScrollBar = QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        self.horizontalScrollBar.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalScrollBar)

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.horizontalScrollBar_2 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_2.setObjectName(u"horizontalScrollBar_2")
        self.horizontalScrollBar_2.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.horizontalScrollBar_2)

        self.spinBox_2 = QSpinBox(self.centralwidget)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.horizontalLayout_2.addWidget(self.spinBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalScrollBar_3 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_3.setObjectName(u"horizontalScrollBar_3")
        self.horizontalScrollBar_3.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.horizontalScrollBar_3)

        self.spinBox_3 = QSpinBox(self.centralwidget)
        self.spinBox_3.setObjectName(u"spinBox_3")

        self.horizontalLayout_3.addWidget(self.spinBox_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.horizontalScrollBar_4 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_4.setObjectName(u"horizontalScrollBar_4")
        self.horizontalScrollBar_4.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.horizontalScrollBar_4)

        self.spinBox_4 = QSpinBox(self.centralwidget)
        self.spinBox_4.setObjectName(u"spinBox_4")

        self.horizontalLayout_4.addWidget(self.spinBox_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_5.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_17)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_18)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_18.addWidget(self.lineEdit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_11.addWidget(self.label_19)

        self.horizontalScrollBar_7 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_7.setObjectName(u"horizontalScrollBar_7")
        self.horizontalScrollBar_7.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_11.addWidget(self.horizontalScrollBar_7)

        self.spinBox_7 = QSpinBox(self.centralwidget)
        self.spinBox_7.setObjectName(u"spinBox_7")

        self.horizontalLayout_11.addWidget(self.spinBox_7)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setCheckable(True)

        self.horizontalLayout_14.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setCheckable(True)

        self.horizontalLayout_14.addWidget(self.pushButton_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.gridLayout.addLayout(self.verticalLayout_7, 3, 0, 1, 1)


        self.horizontalLayout_15.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1188, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuDevices = QMenu(self.menubar)
        self.menuDevices.setObjectName(u"menuDevices")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDevices.menuAction())
        self.menuFile.addAction(self.actionSave_Directory)
        self.menuDevices.addAction(self.actionNano_Genie_M1920)
        self.menuDevices.addAction(self.actionEZFlow_Push_1)
        self.menuDevices.addAction(self.actionEZFlow_Push_2)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave_Directory.setText(QCoreApplication.translate("MainWindow", u"Save Directory", None))
        self.actionNano_Genie_M1920.setText(QCoreApplication.translate("MainWindow", u"Nano Genie M1920", None))
        self.actionEZFlow_Push_1.setText(QCoreApplication.translate("MainWindow", u"EZFlow Push 1", None))
        self.actionEZFlow_Push_2.setText(QCoreApplication.translate("MainWindow", u"EZFlow Push 2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Frame", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Pumps", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Push 1", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Setpoint (mBar)", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Current Pressure (mBar)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Apply Pressure", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Push 2", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Setpoint (mBar)", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Current Pressure (mBar)", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Apply Pressure", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Camera Controls", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Genie Nano M1920", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Exposure", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Gain", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Width", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Recording", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Save Location", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"/save_directory/foo.mp4", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Target FPS", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Record", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuDevices.setTitle(QCoreApplication.translate("MainWindow", u"Devices", None))
    # retranslateUi

