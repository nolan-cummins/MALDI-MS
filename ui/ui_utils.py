# capture mouse motions
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal

class cameraFrameMouseTracking(QLabel):
    coords = Signal(tuple)
    clicked = Signal()
    wheelScrolled = Signal(int)
    
    mousePressed = Signal(tuple)
    mouseMoved = Signal(tuple)
    mouseReleased = Signal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setFocus()
            self.mousePressed.emit((event.pos().x(), event.pos().y()))
            #print((event.pos().x(), event.pos().y()))
            self.clicked.emit()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        self.coords.emit((x, y))
        self.mouseMoved.emit((x, y))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseReleased.emit((event.pos().x(), event.pos().y()))
            event.accept()
        else:
            super().mouseReleaseEvent(event)