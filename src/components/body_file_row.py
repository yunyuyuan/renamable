from PyQt5.Qt import *
from os.path import join
from re import sub

from src.utils import update_css, set_css


class FileRow(QFrame):
    choose_change = pyqtSignal(bool)

    def __init__(self, body, container, dir_name='', base_name=''):
        super().__init__(body)
        self.setProperty("class", "body-file-row")
        self.body, self.container = body, container
        self.dir_name, self.base_name = dir_name, base_name
        self.input_name = join(dir_name, base_name)
        self.output_name = join(dir_name, base_name)
        self.chosen = False

        layout = QHBoxLayout()
        self.choose_state_label = QPushButton(self)
        self.choose_state_label.setFixedSize(40, 40)
        self.choose_state_label.setCursor(Qt.PointingHandCursor)
        self.choose_state_label.setProperty("class", "choose")
        self.choose_state_label.clicked.connect(self.__change_choose)
        self.input_label = QLabel(self.input_name, self)
        self.input_label.setProperty("class", "input")
        self.output_label = QLabel(self.output_name, self)
        self.output_label.setProperty("class", "output")

        layout.addWidget(self.choose_state_label, 1, Qt.AlignCenter)
        layout.addWidget(self.input_label, 4, Qt.AlignCenter)
        layout.addWidget(self.output_label, 4, Qt.AlignCenter)
        self.setLayout(layout)
        set_css(self, 'src/components/body_file_row.css')

    def update_regx(self, input_, output_):
        self.output_name = join(self.dir_name, sub(input_, output_, self.base_name))
        self.output_label.setText(self.output_name)
        if self.input_name == self.output_name:
            self.setProperty("state", "not-change")

    def change_choose(self, b):
        self.chosen = b
        self.choose_state_label.setProperty("active", "t" if self.chosen else "f")
        update_css(self.choose_state_label)

    def __change_choose(self):
        self.chosen = not self.chosen
        self.choose_state_label.setProperty("active", "t" if self.chosen else "f")
        update_css(self.choose_state_label)
        self.choose_change.emit(self.chosen)
