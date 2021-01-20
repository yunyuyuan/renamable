from PyQt5.Qt import *

from src.components.button import Button
from src.utils import set_css


class Dialog(QDialog):
    def __init__(self, type_='success', title='', text=''):
        super().__init__()
        self.setObjectName("dialog")
        self.setFixedWidth(300)
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setWindowTitle(title)

        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap(f'assets/{type_}.png').scaled(50, 50, Qt.KeepAspectRatio))
        self.icon_label.setProperty("class", "icon")
        self.text_label = QLabel(text, self)
        self.text_label.setWordWrap(True)
        self.text_label.setProperty("class", "text")

        self.ok_button = Button("知道了", self)
        self.ok_button.clicked.connect(self.close)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.icon_label, 1)
        layout1.addWidget(self.text_label, 4)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
        set_css(self, 'assets/dialog.css')
        self.exec()

