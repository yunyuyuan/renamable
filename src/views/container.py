import re
import time
from os import listdir
from os.path import dirname, basename, isfile, join

from PyQt5.Qt import *

from src.components.body_file_row import FileRow
from src.components.dialog import Dialog
from src.components.running import Running
from src.utils import set_css
from src.views.about import About


class Container(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("container")
        self.setWindowTitle("批量重命名工具")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.body_layout = QHBoxLayout()
        self.files_widget_list = []
        self.all_chosen = False
        self.can_run = False
        self.is_running = False
        self.back_up = False

        from src.views.menu import Menu
        self.menubar = Menu(self)
        self.frame_head = QFrame(self)
        self.frame_body = QFrame(self)
        self.dialog_about = About(self)
        self.running = Running(self)
        self.body_table = QTableWidget(0, 4, self.frame_body)

        self.input_regx = QLineEdit(self.frame_head)
        self.input_regx.setPlaceholderText("输入正则表达式")
        self.out_regx = QLineEdit(self.frame_head)

        self.out_regx.setPlaceholderText("输出")

        self.set_layout()
        self.connect()
        self.set_class()
        set_css(self, "assets/container.css")
        self.show()

    def set_layout(self):
        head_layout = QGridLayout()
        head_layout.addWidget(self.input_regx, 0, 0, 1, 3)
        mid = QLabel("→", self.frame_head)
        mid.setAlignment(Qt.AlignCenter)
        head_layout.addWidget(mid, 0, 3, 1, 2)
        head_layout.addWidget(self.out_regx, 0, 5, 1, 3)
        self.frame_head.setLayout(head_layout)

        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_table.verticalHeader().hide()
        self.body_table.setHorizontalHeaderLabels(["选择", "输入", "输出", "状态"])
        self.body_layout.addWidget(self.body_table, Qt.AlignCenter)
        self.frame_body.setLayout(self.body_layout)
        self.row_changed()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        menu_layout = QHBoxLayout()
        menu_layout.addWidget(self.menubar)
        layout.addLayout(menu_layout)
        layout.addWidget(self.frame_head)
        layout.addWidget(self.frame_body)
        layout.addWidget(self.running)
        self.setLayout(layout)

    def connect(self):
        self.input_regx.textChanged.connect(self.apply_regx)
        self.out_regx.textChanged.connect(self.apply_regx)
        self.running.runner.finished.connect(self.do_finish)
        self.running.runner.finish_args.connect(lambda *args: Dialog(*args))
        self.running.abort_btn.clicked.connect(lambda: self.running.runner.abort.emit())

    def set_class(self):
        self.frame_head.setProperty("class", "head")
        self.frame_body.setProperty("class", "body")
        self.running.setProperty("class", "running")

        self.input_regx.setProperty("class", "input")
        self.out_regx.setProperty("class", "output")

    def import_files(self):
        files_list, _ = QFileDialog.getOpenFileUrls(self, caption="选择文件", filter="All Files(*)")
        if len(files_list):
            self.apply_files(dirname(files_list[0].toLocalFile()), [basename(x.toLocalFile()) for x in files_list])

    def import_folder(self):
        folder = QFileDialog.getExistingDirectoryUrl(self, caption="选择文件夹")
        dir_path = folder.toLocalFile()
        if dir_path:
            self.apply_files(dir_path, [name for name in listdir(dir_path) if isfile(join(dir_path, name))])

    def apply_files(self, dir_path, name_list):
        start_row = self.body_table.rowCount()
        for idx in range(len(name_list)):
            name = name_list[idx]
            for i in self.files_widget_list:
                if i.dir_name == dir_path and i.base_name == name:
                    break
            else:
                file = FileRow(self.frame_body, self, dir_name=dir_path, base_name=name)
                self.body_table.setRowCount(self.body_table.rowCount()+1)
                file.set_layout(self.body_table, start_row)
                file.choose_change.connect(lambda b: self.choose_state_change())
                self.files_widget_list.append(file)
                start_row += 1
        self.apply_regx()
        self.choose_changed()
        self.row_changed()

    def apply_regx(self):
        input_, output_ = self.input_regx.text(), self.out_regx.text()
        time_stamp = time.strftime("--%Y-%m-%d %H-%M-%S重命名", time.localtime())
        for i in self.files_widget_list:
            try:
                i.update_regx(input_, output_, self.back_up, time_stamp)
            except re.error:
                break
        self.row_changed()

    # ------------ footer -------------

    def choose_state_change(self):
        all_chosen = True
        for i in self.files_widget_list:
            if not i.chosen:
                all_chosen = False
                break
        self.all_chosen = all_chosen
        self.choose_changed()

    def change_select_all(self):
        self.all_chosen = not self.all_chosen
        for i in self.files_widget_list:
            i.change_choose(self.all_chosen)
        self.choose_changed()

    def set_back_up(self, b):
        self.back_up = b
        self.apply_regx()

    def remove_file_row(self):
        if not self.can_run:
            return
        new_list = []
        for idx in range(len(self.files_widget_list)-1, -1, -1):
            file = self.files_widget_list[idx]
            if file.chosen:
                self.body_table.removeRow(idx)
                # self.body_table.setRowCount(self.body_table.rowCount()-1)
                file.setParent(None)
            else:
                new_list.append(file)
        self.files_widget_list = new_list
        self.all_chosen = False
        self.body_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.choose_changed()
        self.row_changed()

    def row_changed(self):
        self.body_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.body_table.setFixedWidth(self.body_table.horizontalHeader().length()+22)

    def choose_changed(self):
        self.menubar.action_choose_all.setText("取消全选" if self.all_chosen else "全选")
        self.menubar.action_choose_all.setEnabled(True if len(self.files_widget_list) else False)
        can_run = False
        for i in self.files_widget_list:
            if i.chosen:
                can_run = True
                break
        self.menubar.action_delete_chosen.setEnabled(True if can_run else False)
        self.menubar.action_do_it.setEnabled(True if can_run else False)
        self.can_run = can_run

    def do_operate(self):
        if self.is_running:
            return
        candidate = [x for x in self.files_widget_list if x.chosen]
        self.is_running = True
        self.running.run(candidate, self.back_up)

    def do_finish(self):
        self.is_running = False

    def closeEvent(self, e):
        e.accept()
        if self.is_running:
            self.running.runner.abort.emit()
        else:
            super().close()
