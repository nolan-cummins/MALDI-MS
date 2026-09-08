# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_v5RtrBtq.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDockWidget, QDoubleSpinBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QScrollBar,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

from .ui_utils import cameraFrameMouseTracking

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1543, 1095)
        self.actionSave_Directory = QAction(MainWindow)
        self.actionSave_Directory.setObjectName(u"actionSave_Directory")
        self.actionNano_Genie_M1920 = QAction(MainWindow)
        self.actionNano_Genie_M1920.setObjectName(u"actionNano_Genie_M1920")
        self.actionEZFlow_Push_1 = QAction(MainWindow)
        self.actionEZFlow_Push_1.setObjectName(u"actionEZFlow_Push_1")
        self.actionEZFlow_Push_2 = QAction(MainWindow)
        self.actionEZFlow_Push_2.setObjectName(u"actionEZFlow_Push_2")
        self.actionLoad_Scripts = QAction(MainWindow)
        self.actionLoad_Scripts.setObjectName(u"actionLoad_Scripts")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1543, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.stage_dockwidget = QDockWidget(MainWindow)
        self.stage_dockwidget.setObjectName(u"stage_dockwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stage_dockwidget.sizePolicy().hasHeightForWidth())
        self.stage_dockwidget.setSizePolicy(sizePolicy)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.gridLayout_7 = QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.scrollArea = QScrollArea(self.dockWidgetContents_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 807, 612))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stage_layout_parent = QVBoxLayout()
        self.stage_layout_parent.setObjectName(u"stage_layout_parent")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_6)

        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMaximumSize(QSize(16777215, 18))
        self.label_18.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.label_18)

        self.arduino_status = QCheckBox(self.scrollAreaWidgetContents)
        self.arduino_status.setObjectName(u"arduino_status")
        self.arduino_status.setMaximumSize(QSize(16777215, 18))
        self.arduino_status.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_16.addWidget(self.arduino_status)

        self.set_zero_btn = QPushButton(self.scrollAreaWidgetContents)
        self.set_zero_btn.setObjectName(u"set_zero_btn")

        self.horizontalLayout_16.addWidget(self.set_zero_btn)

        self.stop_btn = QPushButton(self.scrollAreaWidgetContents)
        self.stop_btn.setObjectName(u"stop_btn")

        self.horizontalLayout_16.addWidget(self.stop_btn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_5)


        self.stage_layout_parent.addLayout(self.horizontalLayout_16)

        self.line_6 = QFrame(self.scrollAreaWidgetContents)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.stage_layout_parent.addWidget(self.line_6)

        self.stage_layout = QVBoxLayout()
        self.stage_layout.setObjectName(u"stage_layout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_22 = QLabel(self.scrollAreaWidgetContents)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_22, 0, 6, 1, 1)

        self.x_accel_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.x_accel_newval_spbx.setObjectName(u"x_accel_newval_spbx")
        self.x_accel_newval_spbx.setReadOnly(False)

        self.gridLayout.addWidget(self.x_accel_newval_spbx, 4, 4, 1, 1)

        self.x_move_val_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.x_move_val_spbx.setObjectName(u"x_move_val_spbx")
        self.x_move_val_spbx.setReadOnly(False)

        self.gridLayout.addWidget(self.x_move_val_spbx, 2, 4, 1, 3)

        self.x_speed_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.x_speed_apply_btn.setObjectName(u"x_speed_apply_btn")

        self.gridLayout.addWidget(self.x_speed_apply_btn, 3, 3, 1, 1)

        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 0, 5, 1, 1)

        self.label_23 = QLabel(self.scrollAreaWidgetContents)
        self.label_23.setObjectName(u"label_23")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy1)
        self.label_23.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_23, 3, 2, 1, 1)

        self.x_accel_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.x_accel_currentval_spbx.setObjectName(u"x_accel_currentval_spbx")
        self.x_accel_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_accel_currentval_spbx.setReadOnly(True)
        self.x_accel_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.x_accel_currentval_spbx, 4, 6, 1, 1)

        self.x_speed_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.x_speed_currentval_spbx.setObjectName(u"x_speed_currentval_spbx")
        self.x_speed_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_speed_currentval_spbx.setReadOnly(True)
        self.x_speed_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.x_speed_currentval_spbx, 3, 6, 1, 1)

        self.x_speed_setpoint_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.x_speed_setpoint_spbx.setObjectName(u"x_speed_setpoint_spbx")
        self.x_speed_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_speed_setpoint_spbx.setReadOnly(True)
        self.x_speed_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.x_speed_setpoint_spbx, 3, 5, 1, 1)

        self.x_speed_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.x_speed_newval_spbx.setObjectName(u"x_speed_newval_spbx")
        self.x_speed_newval_spbx.setReadOnly(False)

        self.gridLayout.addWidget(self.x_speed_newval_spbx, 3, 4, 1, 1)

        self.x_moveto_btn = QPushButton(self.scrollAreaWidgetContents)
        self.x_moveto_btn.setObjectName(u"x_moveto_btn")

        self.gridLayout.addWidget(self.x_moveto_btn, 1, 3, 1, 1)

        self.x_moveto_currentval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.x_moveto_currentval_spbx.setObjectName(u"x_moveto_currentval_spbx")
        self.x_moveto_currentval_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.x_moveto_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_moveto_currentval_spbx.setReadOnly(True)
        self.x_moveto_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.x_moveto_currentval_spbx.setMaximum(100000.000000000000000)

        self.gridLayout.addWidget(self.x_moveto_currentval_spbx, 1, 6, 1, 1)

        self.x_move_btn = QPushButton(self.scrollAreaWidgetContents)
        self.x_move_btn.setObjectName(u"x_move_btn")

        self.gridLayout.addWidget(self.x_move_btn, 2, 3, 1, 1)

        self.x_accel_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.x_accel_apply_btn.setObjectName(u"x_accel_apply_btn")

        self.gridLayout.addWidget(self.x_accel_apply_btn, 4, 3, 1, 1)

        self.label_24 = QLabel(self.scrollAreaWidgetContents)
        self.label_24.setObjectName(u"label_24")
        sizePolicy1.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy1)
        self.label_24.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_24, 4, 2, 1, 1)

        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")
        sizePolicy1.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy1)
        self.label_21.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 1, 2, 2, 1)

        self.x_moveto_setpoint_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.x_moveto_setpoint_spbx.setObjectName(u"x_moveto_setpoint_spbx")
        self.x_moveto_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_moveto_setpoint_spbx.setReadOnly(True)
        self.x_moveto_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.x_moveto_setpoint_spbx.setMaximum(100000.000000000000000)
        self.x_moveto_setpoint_spbx.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.x_moveto_setpoint_spbx, 1, 5, 1, 1)

        self.x_accel_setpoint_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.x_accel_setpoint_spbx.setObjectName(u"x_accel_setpoint_spbx")
        self.x_accel_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_accel_setpoint_spbx.setReadOnly(True)
        self.x_accel_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.x_accel_setpoint_spbx, 4, 5, 1, 1)

        self.x_moveto_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.x_moveto_newval_spbx.setObjectName(u"x_moveto_newval_spbx")
        self.x_moveto_newval_spbx.setReadOnly(False)

        self.gridLayout.addWidget(self.x_moveto_newval_spbx, 1, 4, 1, 1)

        self.label_25 = QLabel(self.scrollAreaWidgetContents)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_25, 0, 4, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 5, 2, 1, 1)

        self.label_26 = QLabel(self.scrollAreaWidgetContents)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMaximumSize(QSize(20, 16777215))
        font = QFont()
        font.setPointSize(16)
        self.label_26.setFont(font)
        self.label_26.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_26, 0, 0, 6, 1)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 0, 1, 6, 1)

        self.x_stepsize_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.x_stepsize_apply_btn.setObjectName(u"x_stepsize_apply_btn")

        self.gridLayout.addWidget(self.x_stepsize_apply_btn, 5, 3, 1, 1)

        self.x_stepsize_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.x_stepsize_newval_spbx.setObjectName(u"x_stepsize_newval_spbx")
        self.x_stepsize_newval_spbx.setReadOnly(False)

        self.gridLayout.addWidget(self.x_stepsize_newval_spbx, 5, 4, 1, 1)

        self.x_stepsize_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.x_stepsize_currentval_spbx.setObjectName(u"x_stepsize_currentval_spbx")
        self.x_stepsize_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_stepsize_currentval_spbx.setReadOnly(True)
        self.x_stepsize_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.x_stepsize_currentval_spbx, 5, 5, 1, 2)


        self.stage_layout.addLayout(self.gridLayout)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.stage_layout.addWidget(self.line_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.y_accel_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.y_accel_apply_btn.setObjectName(u"y_accel_apply_btn")

        self.gridLayout_2.addWidget(self.y_accel_apply_btn, 4, 3, 1, 1)

        self.y_move_btn = QPushButton(self.scrollAreaWidgetContents)
        self.y_move_btn.setObjectName(u"y_move_btn")

        self.gridLayout_2.addWidget(self.y_move_btn, 2, 3, 1, 1)

        self.label_30 = QLabel(self.scrollAreaWidgetContents)
        self.label_30.setObjectName(u"label_30")
        sizePolicy1.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy1)
        self.label_30.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_30, 3, 2, 1, 1)

        self.y_speed_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.y_speed_newval_spbx.setObjectName(u"y_speed_newval_spbx")
        self.y_speed_newval_spbx.setReadOnly(False)

        self.gridLayout_2.addWidget(self.y_speed_newval_spbx, 3, 4, 1, 1)

        self.y_speed_setpoint_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.y_speed_setpoint_spbx.setObjectName(u"y_speed_setpoint_spbx")
        self.y_speed_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_speed_setpoint_spbx.setReadOnly(True)
        self.y_speed_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_2.addWidget(self.y_speed_setpoint_spbx, 3, 5, 1, 1)

        self.y_moveto_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.y_moveto_newval_spbx.setObjectName(u"y_moveto_newval_spbx")
        self.y_moveto_newval_spbx.setReadOnly(False)

        self.gridLayout_2.addWidget(self.y_moveto_newval_spbx, 1, 4, 1, 1)

        self.y_moveto_btn = QPushButton(self.scrollAreaWidgetContents)
        self.y_moveto_btn.setObjectName(u"y_moveto_btn")

        self.gridLayout_2.addWidget(self.y_moveto_btn, 1, 3, 1, 1)

        self.y_speed_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.y_speed_apply_btn.setObjectName(u"y_speed_apply_btn")

        self.gridLayout_2.addWidget(self.y_speed_apply_btn, 3, 3, 1, 1)

        self.y_moveto_setpoint_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.y_moveto_setpoint_spbx.setObjectName(u"y_moveto_setpoint_spbx")
        self.y_moveto_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_moveto_setpoint_spbx.setReadOnly(True)
        self.y_moveto_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.y_moveto_setpoint_spbx.setMaximum(100000.000000000000000)
        self.y_moveto_setpoint_spbx.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.y_moveto_setpoint_spbx, 1, 5, 1, 1)

        self.label_32 = QLabel(self.scrollAreaWidgetContents)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_32, 0, 5, 1, 1)

        self.y_accel_setpoint_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.y_accel_setpoint_spbx.setObjectName(u"y_accel_setpoint_spbx")
        self.y_accel_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_accel_setpoint_spbx.setReadOnly(True)
        self.y_accel_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_2.addWidget(self.y_accel_setpoint_spbx, 4, 5, 1, 1)

        self.label_29 = QLabel(self.scrollAreaWidgetContents)
        self.label_29.setObjectName(u"label_29")
        sizePolicy1.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy1)
        self.label_29.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_29, 4, 2, 1, 1)

        self.label_31 = QLabel(self.scrollAreaWidgetContents)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_31, 0, 4, 1, 1)

        self.y_speed_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.y_speed_currentval_spbx.setObjectName(u"y_speed_currentval_spbx")
        self.y_speed_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_speed_currentval_spbx.setReadOnly(True)
        self.y_speed_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_2.addWidget(self.y_speed_currentval_spbx, 3, 6, 1, 1)

        self.label_28 = QLabel(self.scrollAreaWidgetContents)
        self.label_28.setObjectName(u"label_28")
        sizePolicy1.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy1)
        self.label_28.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_28, 1, 2, 2, 1)

        self.y_accel_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.y_accel_currentval_spbx.setObjectName(u"y_accel_currentval_spbx")
        self.y_accel_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_accel_currentval_spbx.setReadOnly(True)
        self.y_accel_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_2.addWidget(self.y_accel_currentval_spbx, 4, 6, 1, 1)

        self.y_move_val_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.y_move_val_spbx.setObjectName(u"y_move_val_spbx")
        self.y_move_val_spbx.setReadOnly(False)

        self.gridLayout_2.addWidget(self.y_move_val_spbx, 2, 4, 1, 3)

        self.label_27 = QLabel(self.scrollAreaWidgetContents)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_27, 0, 6, 1, 1)

        self.y_accel_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.y_accel_newval_spbx.setObjectName(u"y_accel_newval_spbx")
        self.y_accel_newval_spbx.setReadOnly(False)

        self.gridLayout_2.addWidget(self.y_accel_newval_spbx, 4, 4, 1, 1)

        self.y_moveto_currentval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.y_moveto_currentval_spbx.setObjectName(u"y_moveto_currentval_spbx")
        self.y_moveto_currentval_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.y_moveto_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_moveto_currentval_spbx.setReadOnly(True)
        self.y_moveto_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.y_moveto_currentval_spbx.setMaximum(100000.000000000000000)

        self.gridLayout_2.addWidget(self.y_moveto_currentval_spbx, 1, 6, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 5, 2, 1, 1)

        self.label_33 = QLabel(self.scrollAreaWidgetContents)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMaximumSize(QSize(20, 16777215))
        self.label_33.setFont(font)
        self.label_33.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_33, 0, 0, 6, 1)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 0, 1, 6, 1)

        self.y_stepsize_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.y_stepsize_apply_btn.setObjectName(u"y_stepsize_apply_btn")

        self.gridLayout_2.addWidget(self.y_stepsize_apply_btn, 5, 3, 1, 1)

        self.y_stepsize_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.y_stepsize_newval_spbx.setObjectName(u"y_stepsize_newval_spbx")
        self.y_stepsize_newval_spbx.setReadOnly(False)

        self.gridLayout_2.addWidget(self.y_stepsize_newval_spbx, 5, 4, 1, 1)

        self.y_stepsize_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.y_stepsize_currentval_spbx.setObjectName(u"y_stepsize_currentval_spbx")
        self.y_stepsize_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_stepsize_currentval_spbx.setReadOnly(True)
        self.y_stepsize_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_2.addWidget(self.y_stepsize_currentval_spbx, 5, 5, 1, 2)


        self.stage_layout.addLayout(self.gridLayout_2)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.stage_layout.addWidget(self.line)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.z_speed_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.z_speed_apply_btn.setObjectName(u"z_speed_apply_btn")

        self.gridLayout_3.addWidget(self.z_speed_apply_btn, 3, 3, 1, 1)

        self.z_accel_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.z_accel_newval_spbx.setObjectName(u"z_accel_newval_spbx")
        self.z_accel_newval_spbx.setReadOnly(False)

        self.gridLayout_3.addWidget(self.z_accel_newval_spbx, 4, 4, 1, 1)

        self.z_speed_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.z_speed_newval_spbx.setObjectName(u"z_speed_newval_spbx")
        self.z_speed_newval_spbx.setReadOnly(False)

        self.gridLayout_3.addWidget(self.z_speed_newval_spbx, 3, 4, 1, 1)

        self.z_accel_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.z_accel_apply_btn.setObjectName(u"z_accel_apply_btn")

        self.gridLayout_3.addWidget(self.z_accel_apply_btn, 4, 3, 1, 1)

        self.label_38 = QLabel(self.scrollAreaWidgetContents)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_38.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_38, 0, 4, 1, 1)

        self.z_accel_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.z_accel_currentval_spbx.setObjectName(u"z_accel_currentval_spbx")
        self.z_accel_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_accel_currentval_spbx.setReadOnly(True)
        self.z_accel_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.z_accel_currentval_spbx, 4, 6, 1, 1)

        self.z_move_btn = QPushButton(self.scrollAreaWidgetContents)
        self.z_move_btn.setObjectName(u"z_move_btn")

        self.gridLayout_3.addWidget(self.z_move_btn, 2, 3, 1, 1)

        self.z_moveto_setpoint_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.z_moveto_setpoint_spbx.setObjectName(u"z_moveto_setpoint_spbx")
        self.z_moveto_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_moveto_setpoint_spbx.setReadOnly(True)
        self.z_moveto_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.z_moveto_setpoint_spbx.setMaximum(100000.000000000000000)
        self.z_moveto_setpoint_spbx.setValue(0.000000000000000)

        self.gridLayout_3.addWidget(self.z_moveto_setpoint_spbx, 1, 5, 1, 1)

        self.label_35 = QLabel(self.scrollAreaWidgetContents)
        self.label_35.setObjectName(u"label_35")
        sizePolicy1.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy1)
        self.label_35.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_35, 1, 2, 2, 1)

        self.z_moveto_btn = QPushButton(self.scrollAreaWidgetContents)
        self.z_moveto_btn.setObjectName(u"z_moveto_btn")

        self.gridLayout_3.addWidget(self.z_moveto_btn, 1, 3, 1, 1)

        self.label_34 = QLabel(self.scrollAreaWidgetContents)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_34, 0, 6, 1, 1)

        self.label_36 = QLabel(self.scrollAreaWidgetContents)
        self.label_36.setObjectName(u"label_36")
        sizePolicy1.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy1)
        self.label_36.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_36, 4, 2, 1, 1)

        self.z_accel_setpoint_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.z_accel_setpoint_spbx.setObjectName(u"z_accel_setpoint_spbx")
        self.z_accel_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_accel_setpoint_spbx.setReadOnly(True)
        self.z_accel_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.z_accel_setpoint_spbx, 4, 5, 1, 1)

        self.z_speed_setpoint_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.z_speed_setpoint_spbx.setObjectName(u"z_speed_setpoint_spbx")
        self.z_speed_setpoint_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_speed_setpoint_spbx.setReadOnly(True)
        self.z_speed_setpoint_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.z_speed_setpoint_spbx, 3, 5, 1, 1)

        self.z_moveto_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.z_moveto_newval_spbx.setObjectName(u"z_moveto_newval_spbx")
        self.z_moveto_newval_spbx.setReadOnly(False)

        self.gridLayout_3.addWidget(self.z_moveto_newval_spbx, 1, 4, 1, 1)

        self.label_39 = QLabel(self.scrollAreaWidgetContents)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_39.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_39, 0, 5, 1, 1)

        self.z_move_val_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.z_move_val_spbx.setObjectName(u"z_move_val_spbx")
        self.z_move_val_spbx.setReadOnly(False)

        self.gridLayout_3.addWidget(self.z_move_val_spbx, 2, 4, 1, 3)

        self.z_moveto_currentval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.z_moveto_currentval_spbx.setObjectName(u"z_moveto_currentval_spbx")
        self.z_moveto_currentval_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.z_moveto_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_moveto_currentval_spbx.setReadOnly(True)
        self.z_moveto_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.z_moveto_currentval_spbx.setMaximum(100000.000000000000000)

        self.gridLayout_3.addWidget(self.z_moveto_currentval_spbx, 1, 6, 1, 1)

        self.label_37 = QLabel(self.scrollAreaWidgetContents)
        self.label_37.setObjectName(u"label_37")
        sizePolicy1.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy1)
        self.label_37.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_37, 3, 2, 1, 1)

        self.z_speed_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.z_speed_currentval_spbx.setObjectName(u"z_speed_currentval_spbx")
        self.z_speed_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_speed_currentval_spbx.setReadOnly(True)
        self.z_speed_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.z_speed_currentval_spbx, 3, 6, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 5, 2, 1, 1)

        self.label_40 = QLabel(self.scrollAreaWidgetContents)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMaximumSize(QSize(20, 16777215))
        self.label_40.setFont(font)
        self.label_40.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_40.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_40, 0, 0, 6, 1)

        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line_5, 0, 1, 6, 1)

        self.z_stepsize_apply_btn = QPushButton(self.scrollAreaWidgetContents)
        self.z_stepsize_apply_btn.setObjectName(u"z_stepsize_apply_btn")

        self.gridLayout_3.addWidget(self.z_stepsize_apply_btn, 5, 3, 1, 1)

        self.z_stepsize_newval_spbx = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.z_stepsize_newval_spbx.setObjectName(u"z_stepsize_newval_spbx")
        self.z_stepsize_newval_spbx.setReadOnly(False)

        self.gridLayout_3.addWidget(self.z_stepsize_newval_spbx, 5, 4, 1, 1)

        self.z_stepsize_currentval_spbx = QSpinBox(self.scrollAreaWidgetContents)
        self.z_stepsize_currentval_spbx.setObjectName(u"z_stepsize_currentval_spbx")
        self.z_stepsize_currentval_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_stepsize_currentval_spbx.setReadOnly(True)
        self.z_stepsize_currentval_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.z_stepsize_currentval_spbx, 5, 5, 1, 2)


        self.stage_layout.addLayout(self.gridLayout_3)

        self.line_7 = QFrame(self.scrollAreaWidgetContents)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.stage_layout.addWidget(self.line_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.stage_layout.addItem(self.verticalSpacer_2)


        self.stage_layout_parent.addLayout(self.stage_layout)


        self.gridLayout_6.addLayout(self.stage_layout_parent, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_7.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.stage_dockwidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.stage_dockwidget)
        self.camera_dockwidget = QDockWidget(MainWindow)
        self.camera_dockwidget.setObjectName(u"camera_dockwidget")
        sizePolicy.setHeightForWidth(self.camera_dockwidget.sizePolicy().hasHeightForWidth())
        self.camera_dockwidget.setSizePolicy(sizePolicy)
        self.camera_dockwidget.setFloating(False)
        self.camera_dockwidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable|QDockWidget.DockWidgetFeature.DockWidgetFloatable|QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.gridLayout_4 = QGridLayout(self.dockWidgetContents_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.camera_frame = QFrame(self.dockWidgetContents_4)
        self.camera_frame.setObjectName(u"camera_frame")
        self.camera_frame.setMinimumSize(QSize(640, 400))
        self.camera_frame.setMaximumSize(QSize(1920, 1080))
        self.camera_frame.setFrameShape(QFrame.Shape.Box)
        self.camera_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.camera_frame)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.camera_label = cameraFrameMouseTracking(self.camera_frame)
        self.camera_label.setObjectName(u"camera_label")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.camera_label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.camera_frame, 0, 0, 1, 1)

        self.camera_dockwidget.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.camera_dockwidget)
        self.camera_controls_dockwidget = QDockWidget(MainWindow)
        self.camera_controls_dockwidget.setObjectName(u"camera_controls_dockwidget")
        sizePolicy.setHeightForWidth(self.camera_controls_dockwidget.sizePolicy().hasHeightForWidth())
        self.camera_controls_dockwidget.setSizePolicy(sizePolicy)
        self.dockWidgetContents_6 = QWidget()
        self.dockWidgetContents_6.setObjectName(u"dockWidgetContents_6")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_16 = QLabel(self.dockWidgetContents_6)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_16)

        self.camera_status = QCheckBox(self.dockWidgetContents_6)
        self.camera_status.setObjectName(u"camera_status")
        self.camera_status.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_12.addWidget(self.camera_status)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.camera_controls_layout = QVBoxLayout()
        self.camera_controls_layout.setObjectName(u"camera_controls_layout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.dockWidgetContents_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.label_2)

        self.exposure_scroll = QScrollBar(self.dockWidgetContents_6)
        self.exposure_scroll.setObjectName(u"exposure_scroll")
        self.exposure_scroll.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.exposure_scroll)

        self.exposure_box = QSpinBox(self.dockWidgetContents_6)
        self.exposure_box.setObjectName(u"exposure_box")
        self.exposure_box.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.exposure_box)


        self.camera_controls_layout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.dockWidgetContents_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.label_3)

        self.gain_scroll = QScrollBar(self.dockWidgetContents_6)
        self.gain_scroll.setObjectName(u"gain_scroll")
        self.gain_scroll.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.gain_scroll)

        self.gain_box = QSpinBox(self.dockWidgetContents_6)
        self.gain_box.setObjectName(u"gain_box")
        self.gain_box.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.gain_box)


        self.camera_controls_layout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.dockWidgetContents_6)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.width_scroll = QScrollBar(self.dockWidgetContents_6)
        self.width_scroll.setObjectName(u"width_scroll")
        self.width_scroll.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.width_scroll)

        self.width_box = QSpinBox(self.dockWidgetContents_6)
        self.width_box.setObjectName(u"width_box")
        self.width_box.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.width_box)


        self.camera_controls_layout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.dockWidgetContents_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.label_5)

        self.height_scroll = QScrollBar(self.dockWidgetContents_6)
        self.height_scroll.setObjectName(u"height_scroll")
        self.height_scroll.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.height_scroll)

        self.height_box = QSpinBox(self.dockWidgetContents_6)
        self.height_box.setObjectName(u"height_box")
        self.height_box.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.height_box)


        self.camera_controls_layout.addLayout(self.horizontalLayout_4)

        self.dynamic_range_cbbx = QComboBox(self.dockWidgetContents_6)
        self.dynamic_range_cbbx.addItem("")
        self.dynamic_range_cbbx.addItem("")
        self.dynamic_range_cbbx.setObjectName(u"dynamic_range_cbbx")
        self.dynamic_range_cbbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.camera_controls_layout.addWidget(self.dynamic_range_cbbx)


        self.verticalLayout_3.addLayout(self.camera_controls_layout)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.line_10 = QFrame(self.dockWidgetContents_6)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_10)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_17 = QLabel(self.dockWidgetContents_6)
        self.label_17.setObjectName(u"label_17")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_17)

        self.recording_layout = QVBoxLayout()
        self.recording_layout.setObjectName(u"recording_layout")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")

        self.recording_layout.addLayout(self.horizontalLayout_18)

        self.save_label = QLabel(self.dockWidgetContents_6)
        self.save_label.setObjectName(u"save_label")
        self.save_label.setEnabled(False)
        self.save_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.recording_layout.addWidget(self.save_label)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_19 = QLabel(self.dockWidgetContents_6)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(73, 16777215))

        self.horizontalLayout_11.addWidget(self.label_19)

        self.target_fps_scroll = QScrollBar(self.dockWidgetContents_6)
        self.target_fps_scroll.setObjectName(u"target_fps_scroll")
        self.target_fps_scroll.setMaximum(1000)
        self.target_fps_scroll.setSliderPosition(100)
        self.target_fps_scroll.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_11.addWidget(self.target_fps_scroll)

        self.target_fps_box = QSpinBox(self.dockWidgetContents_6)
        self.target_fps_box.setObjectName(u"target_fps_box")
        self.target_fps_box.setMaximumSize(QSize(100, 16777215))
        self.target_fps_box.setMinimum(1)
        self.target_fps_box.setMaximum(1000)
        self.target_fps_box.setValue(100)

        self.horizontalLayout_11.addWidget(self.target_fps_box)

        self.compress_btn = QCheckBox(self.dockWidgetContents_6)
        self.compress_btn.setObjectName(u"compress_btn")
        self.compress_btn.setMaximumSize(QSize(80, 20))

        self.horizontalLayout_11.addWidget(self.compress_btn)


        self.recording_layout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.record_button = QPushButton(self.dockWidgetContents_6)
        self.record_button.setObjectName(u"record_button")
        self.record_button.setCheckable(True)

        self.horizontalLayout_14.addWidget(self.record_button)

        self.screenshot_button = QPushButton(self.dockWidgetContents_6)
        self.screenshot_button.setObjectName(u"screenshot_button")
        self.screenshot_button.setCheckable(False)

        self.horizontalLayout_14.addWidget(self.screenshot_button)


        self.recording_layout.addLayout(self.horizontalLayout_14)


        self.verticalLayout_7.addLayout(self.recording_layout)


        self.verticalLayout.addLayout(self.verticalLayout_7)

        self.line_11 = QFrame(self.dockWidgetContents_6)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.Shape.HLine)
        self.line_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_11)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_11 = QLabel(self.dockWidgetContents_6)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_11)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.run_script_button = QPushButton(self.dockWidgetContents_6)
        self.run_script_button.setObjectName(u"run_script_button")
        self.run_script_button.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_15.addWidget(self.run_script_button)

        self.stop_script_button = QPushButton(self.dockWidgetContents_6)
        self.stop_script_button.setObjectName(u"stop_script_button")
        self.stop_script_button.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_15.addWidget(self.stop_script_button)

        self.script_combobox = QComboBox(self.dockWidgetContents_6)
        self.script_combobox.setObjectName(u"script_combobox")

        self.horizontalLayout_15.addWidget(self.script_combobox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 128, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.camera_controls_dockwidget.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.camera_controls_dockwidget)
        self.pump_dockwidget = QDockWidget(MainWindow)
        self.pump_dockwidget.setObjectName(u"pump_dockwidget")
        sizePolicy.setHeightForWidth(self.pump_dockwidget.sizePolicy().hasHeightForWidth())
        self.pump_dockwidget.setSizePolicy(sizePolicy)
        self.dockWidgetContents_7 = QWidget()
        self.dockWidgetContents_7.setObjectName(u"dockWidgetContents_7")
        self.verticalLayout_10 = QVBoxLayout(self.dockWidgetContents_7)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_2)

        self.label_6 = QLabel(self.dockWidgetContents_7)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.label_6)

        self.push1_status = QCheckBox(self.dockWidgetContents_7)
        self.push1_status.setObjectName(u"push1_status")

        self.horizontalLayout_17.addWidget(self.push1_status)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout_17)

        self.push1_layout = QVBoxLayout()
        self.push1_layout.setObjectName(u"push1_layout")
        self.push1_setpoint_scroll = QScrollBar(self.dockWidgetContents_7)
        self.push1_setpoint_scroll.setObjectName(u"push1_setpoint_scroll")
        self.push1_setpoint_scroll.setOrientation(Qt.Orientation.Horizontal)

        self.push1_layout.addWidget(self.push1_setpoint_scroll)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.dockWidgetContents_7)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(83, 16777215))

        self.horizontalLayout_5.addWidget(self.label_9)

        self.push1_setpoint_box = QSpinBox(self.dockWidgetContents_7)
        self.push1_setpoint_box.setObjectName(u"push1_setpoint_box")
        self.push1_setpoint_box.setMinimumSize(QSize(100, 0))
        self.push1_setpoint_box.setMaximumSize(QSize(100000, 16777215))

        self.horizontalLayout_5.addWidget(self.push1_setpoint_box)


        self.push1_layout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_10 = QLabel(self.dockWidgetContents_7)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(126, 16777215))

        self.horizontalLayout_7.addWidget(self.label_10)

        self.push1_pressure_label = QLabel(self.dockWidgetContents_7)
        self.push1_pressure_label.setObjectName(u"push1_pressure_label")
        self.push1_pressure_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.push1_pressure_label)


        self.push1_layout.addLayout(self.horizontalLayout_7)

        self.push1_apply_button = QPushButton(self.dockWidgetContents_7)
        self.push1_apply_button.setObjectName(u"push1_apply_button")
        self.push1_apply_button.setCheckable(False)

        self.push1_layout.addWidget(self.push1_apply_button)

        self.push1_zero_button = QPushButton(self.dockWidgetContents_7)
        self.push1_zero_button.setObjectName(u"push1_zero_button")

        self.push1_layout.addWidget(self.push1_zero_button)


        self.verticalLayout_6.addLayout(self.push1_layout)


        self.horizontalLayout_8.addLayout(self.verticalLayout_6)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_3)

        self.label_12 = QLabel(self.dockWidgetContents_7)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.label_12)

        self.push2_status = QCheckBox(self.dockWidgetContents_7)
        self.push2_status.setObjectName(u"push2_status")

        self.horizontalLayout_13.addWidget(self.push2_status)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_13)

        self.push2_layout = QVBoxLayout()
        self.push2_layout.setObjectName(u"push2_layout")
        self.push2_setpoint_scroll = QScrollBar(self.dockWidgetContents_7)
        self.push2_setpoint_scroll.setObjectName(u"push2_setpoint_scroll")
        self.push2_setpoint_scroll.setOrientation(Qt.Orientation.Horizontal)

        self.push2_layout.addWidget(self.push2_setpoint_scroll)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_13 = QLabel(self.dockWidgetContents_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(83, 16777215))

        self.horizontalLayout_9.addWidget(self.label_13)

        self.push2_setpoint_box = QSpinBox(self.dockWidgetContents_7)
        self.push2_setpoint_box.setObjectName(u"push2_setpoint_box")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.push2_setpoint_box.sizePolicy().hasHeightForWidth())
        self.push2_setpoint_box.setSizePolicy(sizePolicy2)
        self.push2_setpoint_box.setMinimumSize(QSize(100, 0))
        self.push2_setpoint_box.setMaximumSize(QSize(10000, 16777215))

        self.horizontalLayout_9.addWidget(self.push2_setpoint_box)


        self.push2_layout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_14 = QLabel(self.dockWidgetContents_7)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(126, 16777215))

        self.horizontalLayout_10.addWidget(self.label_14)

        self.push2_pressure_label = QLabel(self.dockWidgetContents_7)
        self.push2_pressure_label.setObjectName(u"push2_pressure_label")
        self.push2_pressure_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.push2_pressure_label)


        self.push2_layout.addLayout(self.horizontalLayout_10)

        self.push2_apply_button = QPushButton(self.dockWidgetContents_7)
        self.push2_apply_button.setObjectName(u"push2_apply_button")
        self.push2_apply_button.setCheckable(False)

        self.push2_layout.addWidget(self.push2_apply_button)

        self.push2_zero_button = QPushButton(self.dockWidgetContents_7)
        self.push2_zero_button.setObjectName(u"push2_zero_button")

        self.push2_layout.addWidget(self.push2_zero_button)


        self.verticalLayout_8.addLayout(self.push2_layout)


        self.horizontalLayout_8.addLayout(self.verticalLayout_8)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.horizontalLayout_8.addLayout(self.verticalLayout_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.verticalLayout_10.addLayout(self.verticalLayout_4)

        self.verticalSpacer_3 = QSpacerItem(20, 118, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_3)

        self.pump_dockwidget.setWidget(self.dockWidgetContents_7)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.pump_dockwidget)
        self.yolo_controls_dockwidget = QDockWidget(MainWindow)
        self.yolo_controls_dockwidget.setObjectName(u"yolo_controls_dockwidget")
        sizePolicy.setHeightForWidth(self.yolo_controls_dockwidget.sizePolicy().hasHeightForWidth())
        self.yolo_controls_dockwidget.setSizePolicy(sizePolicy)
        self.yolo_controls_dockwidget.setFloating(False)
        self.yolo_controls_dockwidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable|QDockWidget.DockWidgetFeature.DockWidgetFloatable|QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.dockWidgetContents_8 = QWidget()
        self.dockWidgetContents_8.setObjectName(u"dockWidgetContents_8")
        self.verticalLayout_9 = QVBoxLayout(self.dockWidgetContents_8)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.camera_controls_layout_2 = QVBoxLayout()
        self.camera_controls_layout_2.setObjectName(u"camera_controls_layout_2")
        self.label_43 = QLabel(self.dockWidgetContents_8)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_43.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.camera_controls_layout_2.addWidget(self.label_43)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_44 = QLabel(self.dockWidgetContents_8)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_19.addWidget(self.label_44)

        self.confidence_scrollbar = QScrollBar(self.dockWidgetContents_8)
        self.confidence_scrollbar.setObjectName(u"confidence_scrollbar")
        self.confidence_scrollbar.setMaximum(100)
        self.confidence_scrollbar.setSliderPosition(75)
        self.confidence_scrollbar.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_19.addWidget(self.confidence_scrollbar)

        self.confidence_spbx = QSpinBox(self.dockWidgetContents_8)
        self.confidence_spbx.setObjectName(u"confidence_spbx")
        self.confidence_spbx.setMaximumSize(QSize(100, 16777215))
        self.confidence_spbx.setMaximum(100)
        self.confidence_spbx.setValue(75)

        self.horizontalLayout_19.addWidget(self.confidence_spbx)


        self.camera_controls_layout_2.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_45 = QLabel(self.dockWidgetContents_8)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_21.addWidget(self.label_45)

        self.max_detections_scrollbar = QScrollBar(self.dockWidgetContents_8)
        self.max_detections_scrollbar.setObjectName(u"max_detections_scrollbar")
        self.max_detections_scrollbar.setMaximum(10)
        self.max_detections_scrollbar.setSliderPosition(10)
        self.max_detections_scrollbar.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_21.addWidget(self.max_detections_scrollbar)

        self.max_detections_spbx = QSpinBox(self.dockWidgetContents_8)
        self.max_detections_spbx.setObjectName(u"max_detections_spbx")
        self.max_detections_spbx.setMaximumSize(QSize(100, 16777215))
        self.max_detections_spbx.setMinimum(1)
        self.max_detections_spbx.setMaximum(10)
        self.max_detections_spbx.setValue(10)

        self.horizontalLayout_21.addWidget(self.max_detections_spbx)


        self.camera_controls_layout_2.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.run_model_btn = QPushButton(self.dockWidgetContents_8)
        self.run_model_btn.setObjectName(u"run_model_btn")
        self.run_model_btn.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_22.addWidget(self.run_model_btn)

        self.stop_model_btn = QPushButton(self.dockWidgetContents_8)
        self.stop_model_btn.setObjectName(u"stop_model_btn")
        self.stop_model_btn.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_22.addWidget(self.stop_model_btn)

        self.model_combobox = QComboBox(self.dockWidgetContents_8)
        self.model_combobox.setObjectName(u"model_combobox")

        self.horizontalLayout_22.addWidget(self.model_combobox)

        self.feedframes_chkbox = QCheckBox(self.dockWidgetContents_8)
        self.feedframes_chkbox.setObjectName(u"feedframes_chkbox")
        self.feedframes_chkbox.setMaximumSize(QSize(100, 16777215))
        self.feedframes_chkbox.setChecked(True)
        self.feedframes_chkbox.setTristate(False)

        self.horizontalLayout_22.addWidget(self.feedframes_chkbox)

        self.fit_ellipse_chbx = QCheckBox(self.dockWidgetContents_8)
        self.fit_ellipse_chbx.setObjectName(u"fit_ellipse_chbx")
        self.fit_ellipse_chbx.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_22.addWidget(self.fit_ellipse_chbx)

        self.ema_chckbx = QCheckBox(self.dockWidgetContents_8)
        self.ema_chckbx.setObjectName(u"ema_chckbx")
        self.ema_chckbx.setMaximumSize(QSize(50, 16777215))
        self.ema_chckbx.setChecked(False)
        self.ema_chckbx.setTristate(False)

        self.horizontalLayout_22.addWidget(self.ema_chckbx)


        self.camera_controls_layout_2.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_51 = QLabel(self.dockWidgetContents_8)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_28.addWidget(self.label_51)

        self.volume_spbx = QDoubleSpinBox(self.dockWidgetContents_8)
        self.volume_spbx.setObjectName(u"volume_spbx")
        self.volume_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.volume_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.volume_spbx.setReadOnly(True)
        self.volume_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.volume_spbx.setMaximum(100000.000000000000000)

        self.horizontalLayout_28.addWidget(self.volume_spbx)


        self.camera_controls_layout_2.addLayout(self.horizontalLayout_28)

        self.line_9 = QFrame(self.dockWidgetContents_8)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.camera_controls_layout_2.addWidget(self.line_9)

        self.label_50 = QLabel(self.dockWidgetContents_8)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.camera_controls_layout_2.addWidget(self.label_50)

        self.tabWidget = QTabWidget(self.dockWidgetContents_8)
        self.tabWidget.setObjectName(u"tabWidget")
        self.model_timings = QWidget()
        self.model_timings.setObjectName(u"model_timings")
        self.verticalLayout_11 = QVBoxLayout(self.model_timings)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_47 = QLabel(self.model_timings)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_25.addWidget(self.label_47)

        self.pre_processing_spbx = QDoubleSpinBox(self.model_timings)
        self.pre_processing_spbx.setObjectName(u"pre_processing_spbx")
        self.pre_processing_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pre_processing_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pre_processing_spbx.setReadOnly(True)
        self.pre_processing_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pre_processing_spbx.setMaximum(100000.000000000000000)

        self.horizontalLayout_25.addWidget(self.pre_processing_spbx)


        self.verticalLayout_11.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_46 = QLabel(self.model_timings)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_26.addWidget(self.label_46)

        self.inference_spbx = QDoubleSpinBox(self.model_timings)
        self.inference_spbx.setObjectName(u"inference_spbx")
        self.inference_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.inference_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inference_spbx.setReadOnly(True)
        self.inference_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.inference_spbx.setMaximum(100000.000000000000000)

        self.horizontalLayout_26.addWidget(self.inference_spbx)


        self.verticalLayout_11.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_48 = QLabel(self.model_timings)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_24.addWidget(self.label_48)

        self.total_delay_ms_spbx = QDoubleSpinBox(self.model_timings)
        self.total_delay_ms_spbx.setObjectName(u"total_delay_ms_spbx")
        self.total_delay_ms_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.total_delay_ms_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_delay_ms_spbx.setReadOnly(True)
        self.total_delay_ms_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.total_delay_ms_spbx.setMaximum(100000.000000000000000)

        self.horizontalLayout_24.addWidget(self.total_delay_ms_spbx)


        self.verticalLayout_11.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_49 = QLabel(self.model_timings)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_23.addWidget(self.label_49)

        self.total_delay_frames_spbx = QSpinBox(self.model_timings)
        self.total_delay_frames_spbx.setObjectName(u"total_delay_frames_spbx")
        self.total_delay_frames_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_delay_frames_spbx.setReadOnly(True)
        self.total_delay_frames_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.horizontalLayout_23.addWidget(self.total_delay_frames_spbx)


        self.verticalLayout_11.addLayout(self.horizontalLayout_23)

        self.tabWidget.addTab(self.model_timings, "")
        self.filter_timings = QWidget()
        self.filter_timings.setObjectName(u"filter_timings")
        self.verticalLayout_13 = QVBoxLayout(self.filter_timings)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.label_57 = QLabel(self.filter_timings)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_34.addWidget(self.label_57)

        self.filters_total_delay_ms_spbx = QDoubleSpinBox(self.filter_timings)
        self.filters_total_delay_ms_spbx.setObjectName(u"filters_total_delay_ms_spbx")
        self.filters_total_delay_ms_spbx.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.filters_total_delay_ms_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filters_total_delay_ms_spbx.setReadOnly(True)
        self.filters_total_delay_ms_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.filters_total_delay_ms_spbx.setMaximum(100000.000000000000000)

        self.horizontalLayout_34.addWidget(self.filters_total_delay_ms_spbx)


        self.verticalLayout_13.addLayout(self.horizontalLayout_34)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_55 = QLabel(self.filter_timings)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_32.addWidget(self.label_55)

        self.filters_total_delay_frames_spbx = QSpinBox(self.filter_timings)
        self.filters_total_delay_frames_spbx.setObjectName(u"filters_total_delay_frames_spbx")
        self.filters_total_delay_frames_spbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filters_total_delay_frames_spbx.setReadOnly(True)
        self.filters_total_delay_frames_spbx.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.horizontalLayout_32.addWidget(self.filters_total_delay_frames_spbx)


        self.verticalLayout_13.addLayout(self.horizontalLayout_32)

        self.tabWidget.addTab(self.filter_timings, "")

        self.camera_controls_layout_2.addWidget(self.tabWidget)

        self.line_8 = QFrame(self.dockWidgetContents_8)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.camera_controls_layout_2.addWidget(self.line_8)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_7)

        self.label_41 = QLabel(self.dockWidgetContents_8)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_41.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_27.addWidget(self.label_41)

        self.clahe_checkbox = QCheckBox(self.dockWidgetContents_8)
        self.clahe_checkbox.setObjectName(u"clahe_checkbox")

        self.horizontalLayout_27.addWidget(self.clahe_checkbox)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_8)


        self.camera_controls_layout_2.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_15 = QLabel(self.dockWidgetContents_8)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_6.addWidget(self.label_15)

        self.clip_limit_scrollbar = QScrollBar(self.dockWidgetContents_8)
        self.clip_limit_scrollbar.setObjectName(u"clip_limit_scrollbar")
        self.clip_limit_scrollbar.setMinimum(2)
        self.clip_limit_scrollbar.setMaximum(10)
        self.clip_limit_scrollbar.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.clip_limit_scrollbar)

        self.clip_limit_spbx = QSpinBox(self.dockWidgetContents_8)
        self.clip_limit_spbx.setObjectName(u"clip_limit_spbx")
        self.clip_limit_spbx.setMaximumSize(QSize(100, 16777215))
        self.clip_limit_spbx.setMinimum(2)
        self.clip_limit_spbx.setMaximum(10)

        self.horizontalLayout_6.addWidget(self.clip_limit_spbx)


        self.camera_controls_layout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_42 = QLabel(self.dockWidgetContents_8)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_20.addWidget(self.label_42)

        self.tile_grid_scrollbar = QScrollBar(self.dockWidgetContents_8)
        self.tile_grid_scrollbar.setObjectName(u"tile_grid_scrollbar")
        self.tile_grid_scrollbar.setMinimum(2)
        self.tile_grid_scrollbar.setMaximum(32)
        self.tile_grid_scrollbar.setSliderPosition(8)
        self.tile_grid_scrollbar.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_20.addWidget(self.tile_grid_scrollbar)

        self.tile_grid_spbx = QSpinBox(self.dockWidgetContents_8)
        self.tile_grid_spbx.setObjectName(u"tile_grid_spbx")
        self.tile_grid_spbx.setMaximumSize(QSize(100, 16777215))
        self.tile_grid_spbx.setMinimum(2)
        self.tile_grid_spbx.setMaximum(32)
        self.tile_grid_spbx.setValue(8)

        self.horizontalLayout_20.addWidget(self.tile_grid_spbx)


        self.camera_controls_layout_2.addLayout(self.horizontalLayout_20)


        self.verticalLayout_12.addLayout(self.camera_controls_layout_2)


        self.verticalLayout_9.addLayout(self.verticalLayout_12)

        self.verticalSpacer_4 = QSpacerItem(20, 128, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_4)

        self.yolo_controls_dockwidget.setWidget(self.dockWidgetContents_8)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.yolo_controls_dockwidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionSave_Directory)
        self.menuFile.addAction(self.actionLoad_Scripts)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave_Directory.setText(QCoreApplication.translate("MainWindow", u"Save Directory", None))
        self.actionNano_Genie_M1920.setText(QCoreApplication.translate("MainWindow", u"Nano Genie M1920", None))
        self.actionEZFlow_Push_1.setText(QCoreApplication.translate("MainWindow", u"EZFlow Push 1", None))
        self.actionEZFlow_Push_2.setText(QCoreApplication.translate("MainWindow", u"EZFlow Push 2", None))
        self.actionLoad_Scripts.setText(QCoreApplication.translate("MainWindow", u"Load Scripts", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.stage_dockwidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Stage Controls", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Arduino", None))
        self.arduino_status.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.set_zero_btn.setText(QCoreApplication.translate("MainWindow", u"Set Zero", None))
        self.stop_btn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Current Value", None))
        self.x_speed_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Setpoint", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Speed (um/s)", None))
        self.x_moveto_btn.setText(QCoreApplication.translate("MainWindow", u"Move To", None))
        self.x_move_btn.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.x_accel_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Acceleration (um/s\u00b2)", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Position (um)", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"New Value", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Step Size (um)", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.x_stepsize_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.y_accel_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.y_move_btn.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Speed (um/s)", None))
        self.y_moveto_btn.setText(QCoreApplication.translate("MainWindow", u"Move To", None))
        self.y_speed_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Setpoint", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Acceleration (um/s\u00b2)", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"New Value", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Position (um)", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Current Value", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Step Size (um)", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.y_stepsize_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.z_speed_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.z_accel_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"New Value", None))
        self.z_move_btn.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Position (um)", None))
        self.z_moveto_btn.setText(QCoreApplication.translate("MainWindow", u"Move To", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Current Value", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Acceleration (um/s\u00b2)", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Setpoint", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Speed (um/s)", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Step Size (um)", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.z_stepsize_apply_btn.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.camera_dockwidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Camera Feed", None))
        self.camera_label.setText(QCoreApplication.translate("MainWindow", u"Empty", None))
        self.camera_controls_dockwidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Camera Controls", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"a2A1920-160umBAS", None))
        self.camera_status.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Exposure", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Gain", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Width", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Height", None))
        self.dynamic_range_cbbx.setItemText(0, QCoreApplication.translate("MainWindow", u"12-Bit Monochromatic (101 fps, 1920x1200)", None))
        self.dynamic_range_cbbx.setItemText(1, QCoreApplication.translate("MainWindow", u"8-Bit Monochromatic (152 fps, 1920x1200)", None))

        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Recording", None))
        self.save_label.setText(QCoreApplication.translate("MainWindow", u"/save_directory/script.*", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Target FPS", None))
        self.compress_btn.setText(QCoreApplication.translate("MainWindow", u"Compress", None))
        self.record_button.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.screenshot_button.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Scripts", None))
        self.run_script_button.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stop_script_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.script_combobox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"/load_directory/foo.json", None))
        self.pump_dockwidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pump Controls", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Push 1", None))
        self.push1_status.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Setpoint (mBar)", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Current Pressure (mBar)", None))
        self.push1_pressure_label.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.push1_apply_button.setText(QCoreApplication.translate("MainWindow", u"Apply Pressure", None))
        self.push1_zero_button.setText(QCoreApplication.translate("MainWindow", u"Zero", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Push 2", None))
        self.push2_status.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Setpoint (mBar)", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Current Pressure (mBar)", None))
        self.push2_pressure_label.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.push2_apply_button.setText(QCoreApplication.translate("MainWindow", u"Apply Pressure", None))
        self.push2_zero_button.setText(QCoreApplication.translate("MainWindow", u"Zero", None))
        self.yolo_controls_dockwidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Vision Controls", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"YOLO Droplet Segmentation Model", None))
#if QT_CONFIG(tooltip)
        self.label_44.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Confidence (%)", None))
#if QT_CONFIG(tooltip)
        self.label_45.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Max Detections", None))
        self.run_model_btn.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stop_model_btn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.model_combobox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"/model_dir/model.pt", None))
#if QT_CONFIG(tooltip)
        self.feedframes_chkbox.setToolTip(QCoreApplication.translate("MainWindow", u"Feed model frames to process. If unchecked, model thread will run, but will not inference.", None))
#endif // QT_CONFIG(tooltip)
        self.feedframes_chkbox.setText(QCoreApplication.translate("MainWindow", u"Feed Frames", None))
        self.fit_ellipse_chbx.setText(QCoreApplication.translate("MainWindow", u"Fit Elipse", None))
#if QT_CONFIG(tooltip)
        self.ema_chckbx.setToolTip(QCoreApplication.translate("MainWindow", u"Apply an Exponential Moving Average to the model output for smoothing", None))
#endif // QT_CONFIG(tooltip)
        self.ema_chckbx.setText(QCoreApplication.translate("MainWindow", u"EMA", None))
#if QT_CONFIG(tooltip)
        self.label_51.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Volume (pL)", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Timings", None))
#if QT_CONFIG(tooltip)
        self.label_47.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Pre-processing (ms)", None))
#if QT_CONFIG(tooltip)
        self.label_46.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Inference (ms)", None))
#if QT_CONFIG(tooltip)
        self.label_48.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Total Delay (ms)", None))
#if QT_CONFIG(tooltip)
        self.label_49.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Total Delay (frames)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.model_timings), QCoreApplication.translate("MainWindow", u"Model", None))
#if QT_CONFIG(tooltip)
        self.label_57.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Total Delay (ms)", None))
#if QT_CONFIG(tooltip)
        self.label_55.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Total Delay (frames)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filter_timings), QCoreApplication.translate("MainWindow", u"Filters", None))
#if QT_CONFIG(tooltip)
        self.label_41.setToolTip(QCoreApplication.translate("MainWindow", u"Adaptive histogram equalization algorithm: auto-applied to bit-shift 12-bit down to 8-bit, optional for YOLO input", None))
#endif // QT_CONFIG(tooltip)
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Contrast Limited Adaptive Histogram Equalization (CLAHE)", None))
        self.clahe_checkbox.setText("")
#if QT_CONFIG(tooltip)
        self.label_15.setToolTip(QCoreApplication.translate("MainWindow", u"Sets the threshold for contrast limiting. Higher values increase contrast but also amplify background noise. A value of 2.0 to 4.0 is typically used to enhance subtle gradients in the spray plume without creating \"grainy\" artifacts in the dark regions", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Clip Limit", None))
#if QT_CONFIG(tooltip)
        self.label_42.setToolTip(QCoreApplication.translate("MainWindow", u"Defines the number of local regions (tiles) the image is divided into for equalization. Specified as (Rows, Cols), e.g., 8x8. Smaller tiles allow for more localized detail enhancement (good for small features), while larger tiles provide a smoother, more global contrast adjustment.", None))
#endif // QT_CONFIG(tooltip)
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Tile Grid Size", None))
    # retranslateUi

