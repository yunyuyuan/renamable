from PyQt5.Qt import *
from os.path import exists
from os import rename, mkdir
from shutil import copy2
from re import sub

from src.utils import update_css, set_css, parse_path


class FileRow(QFrame):
    choose_change = pyqtSignal(bool)

    def __init__(self, body, container, dir_name='', base_name=''):
        super().__init__(body)
        self.setProperty("class", "body-file-row")
        self.body, self.container = body, container
        self.dir_name, self.base_name = dir_name, base_name
        self.input_name = parse_path(dir_name, base_name)
        self.output_name = parse_path(dir_name, base_name)
        self.chosen = False
        self.file_exist = False
        self.back_up_dir = ''

        self.choose_state_box = QCheckBox(self)
        self.choose_state_box.setFixedSize(20, 20)
        self.choose_state_box.setCursor(Qt.PointingHandCursor)
        self.choose_state_box.setProperty("class", "choose")
        self.choose_state_box.clicked.connect(self.__change_choose)
        self.input_label = QLabel(sub('([/\\\\])([^/\\\\]+)$', '\\1<a style="color: red">\\2</a>', self.input_name), self)
        self.input_label.setProperty("class", "input")
        self.output_label = QLabel(self.output_name, self)
        self.output_label.setProperty("class", "output")
        self.status_label = QLabel(self)
        self.status_label.setFixedSize(15, 15)
        self.status_label.setProperty("class", "status")

        set_css(self, 'assets/body_file_row.css')

    def set_layout(self, table: QTableWidget, row):
        idx = 0
        for widget in [self.choose_state_box, self.input_label, self.output_label, self.status_label]:
            parent1 = QWidget()
            layout1 = QHBoxLayout(parent1)
            layout1.addWidget(widget)
            layout1.setAlignment(Qt.AlignCenter)
            layout1.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(row, idx, parent1)
            idx += 1

    def update_regx(self, input_, output_, backup, time_stamp):
        self.output_label.setProperty("same", "f")
        update_css(self.output_label)
        self.back_up_dir = sub('[/\\\\]$', '', self.dir_name) + time_stamp
        self.output_name = parse_path(self.dir_name if not backup else self.back_up_dir, sub(input_, output_, self.base_name))
        if backup:
            self.output_label.setText(sub('([/\\\\])([^/\\\\]+)([/\\\\])([^/\\\\]+)$',
                                          '\\1<a style="color: blue">\\2</a>\\3<a style="color: red">\\4</a>', self.output_name))
        else:
            self.output_label.setText(sub('([/\\\\])([^/\\\\]+)$', '\\1<a style="color: red">\\2</a>', self.output_name))
        self.file_exist = False
        if self.input_name == self.output_name:
            self.status_label.setProperty("status", "warn")
            self.status_label.setToolTip("未改变")
        elif exists(self.output_name):
            self.status_label.setProperty("status", "exist")
            self.status_label.setToolTip("已存在!")
            self.file_exist = True
        else:
            self.status_label.setProperty("status", "fine")
            self.status_label.setToolTip("已改变")
        update_css(self.status_label)

    def change_choose(self, b):
        self.chosen = b
        self.choose_state_box.setChecked(b)
        update_css(self.choose_state_box)

    def __change_choose(self):
        self.chosen = self.choose_state_box.checkState()
        self.choose_change.emit(self.chosen)

    def do_rename(self, back_up):
        if self.input_name == self.output_name:
            return None
        try:
            if back_up:
                if not exists(self.back_up_dir):
                    mkdir(self.back_up_dir)
                copy2(self.input_name, self.output_name)
            else:
                rename(self.input_name, self.output_name)
            return None
        except BaseException as e:
            return str(e)

    def set_same_name_warn(self, name):
        self.output_label.setProperty("same", "t" if name == self.output_name else "f")
        update_css(self.output_label)
