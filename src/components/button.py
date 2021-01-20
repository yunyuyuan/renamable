from PyQt5.Qt import *

from src.utils import set_css


class Button(QPushButton):
    def __init__(self, text, parent):
        super().__init__(parent=parent, text=text)
        self.setProperty("class", "button")
        set_css(self, 'assets/button.css')
        self.setCursor(Qt.PointingHandCursor)
