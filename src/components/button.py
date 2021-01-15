from PyQt5.Qt import *


class Button(QPushButton):
    def __init__(self, text, parent):
        super().__init__(parent=parent, text=text)
        self.setProperty("class", "button")
