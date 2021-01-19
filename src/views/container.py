import re

from PyQt5.Qt import *
from os import listdir
from os.path import dirname, basename, isfile, join

from src.components.body_file_row import FileRow
from src.components.button import Button
from src.utils import set_css, update_css


class Container(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("container")
        self.body_layout = QVBoxLayout()
        self.files_widget_list = []
        self.all_chosen = False
        self.can_run = False

        self.frame_head = QFrame(self)
        self.frame_body = QFrame(self)
        self.body_table = QTableWidget(0, 4, self.frame_body)
        self.frame_footer = QFrame(self)

        self.btn_choose_files = Button("批量选择文件", self.frame_head)
        self.btn_choose_folder = Button("导入整个文件夹", self.frame_head)

        self.input_regx = QLineEdit(self.frame_head)
        self.input_regx.setPlaceholderText("输入正则表达式")
        self.out_regx = QLineEdit(self.frame_head)

        self.out_regx.setPlaceholderText("输出")

        self.btn_change_select_all = Button("全选", self.frame_footer)
        self.btn_remove_row = Button("移除所选", self.frame_footer)
        self.btn_do_it = Button("执行操作", self.frame_footer)
        self.btn_remove_row.setCursor(Qt.ForbiddenCursor)
        self.btn_do_it.setCursor(Qt.ForbiddenCursor)

        self.set_layout()
        self.connect()
        self.set_class()
        set_css(self, "src/views/container.css")
        self.show()

    def set_layout(self):
        head_layout = QGridLayout()
        head_layout.addWidget(self.btn_choose_files, 0, 0, 1, 4)
        head_layout.addWidget(self.btn_choose_folder, 0, 4, 1, 4)
        head_layout.addWidget(self.input_regx, 1, 0, 1, 3)
        head_layout.addWidget(QLabel("→", self.frame_head), 1, 3, 1, 2)
        head_layout.addWidget(self.out_regx, 1, 5, 1, 3)
        self.frame_head.setLayout(head_layout)

        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_table.verticalHeader().hide()
        self.body_table.setHorizontalHeaderLabels(["选择", "输入", "输出", "状态"])
        self.body_layout.addWidget(self.body_table)
        self.frame_body.setLayout(self.body_layout)

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(self.btn_change_select_all, 1)
        footer_layout.addWidget(self.btn_remove_row, 1)
        footer_layout.addWidget(self.btn_do_it, 2)
        self.frame_footer.setLayout(footer_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.frame_head)
        layout.addWidget(self.frame_body)
        layout.addWidget(self.frame_footer)
        self.setLayout(layout)

    def connect(self):
        self.btn_choose_files.clicked.connect(self.import_files)
        self.btn_choose_folder.clicked.connect(self.import_folder)

        self.input_regx.textChanged.connect(self.apply_regx)
        self.out_regx.textChanged.connect(self.apply_regx)

        self.btn_change_select_all.clicked.connect(self.change_select_all)
        self.btn_remove_row.clicked.connect(self.remove_file_row)
        self.btn_do_it.clicked.connect(self.do_operate)

    def set_class(self):
        self.frame_head.setProperty("class", "head")
        self.frame_body.setProperty("class", "body")
        self.frame_footer.setProperty("class", "footer")

        self.btn_choose_files.setProperty("class", "choose-file")
        self.btn_choose_folder.setProperty("class", "choose-folder")

        self.input_regx.setProperty("class", "input")
        self.out_regx.setProperty("class", "output")

        self.btn_change_select_all.setProperty("class", "choose")
        self.btn_remove_row.setProperty("class", "remove")
        self.btn_do_it.setProperty("class", "do")

    def import_files(self):
        files_list, _ = QFileDialog.getOpenFileUrls(self, caption="选择文件", filter="All Files(*)")
        if len(files_list):
            self.apply_files(dirname(files_list[0].toLocalFile()), [basename(x.toLocalFile()) for x in files_list])

    def import_folder(self):
        folder = QFileDialog.getExistingDirectoryUrl(self, caption="选择文件夹")
        if folder:
            dir_path = folder.toLocalFile()
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
                file.update_regx(self.input_regx.text(), self.out_regx.text())
                file.choose_change.connect(lambda b: self.choose_state_change(file, b))
                self.files_widget_list.append(file)
                start_row += 1
        self.body_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def apply_regx(self):
        input_, output_ = self.input_regx.text(), self.out_regx.text()
        for i in self.files_widget_list:
            try:
                i.update_regx(input_, output_)
            except re.error:
                break

    # ------------ footer -------------

    def choose_state_change(self, widget, b):
        all_chosen = True
        for i in self.files_widget_list:
            if not i.chosen:
                all_chosen = False
                break
        self.all_chosen = all_chosen
        self.after_choose_state_change()

    def change_select_all(self):
        self.all_chosen = not self.all_chosen
        for i in self.files_widget_list:
            i.change_choose(self.all_chosen)
        self.after_choose_state_change()

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
        self.body_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.after_choose_state_change()

    def after_choose_state_change(self):
        self.btn_change_select_all.setText("全不选" if self.all_chosen else "全选")
        # self.btn_change_select_all.setProperty("active", "t" if self.all_chosen else "f")
        can_run = False
        for i in self.files_widget_list:
            if i.chosen:
                can_run = True
                break
        self.btn_remove_row.setProperty("available", "t" if can_run else "f")
        self.btn_remove_row.setEnabled(True if can_run else False)
        self.btn_remove_row.setCursor(Qt.PointingHandCursor if can_run else Qt.ForbiddenCursor)
        update_css(self.btn_remove_row)
        self.btn_do_it.setProperty("available", "t" if can_run else "f")
        self.btn_do_it.setEnabled(True if can_run else False)
        self.btn_do_it.setCursor(Qt.PointingHandCursor if can_run else Qt.ForbiddenCursor)
        update_css(self.btn_do_it)
        self.can_run = can_run

    def do_operate(self):
        candidate = [x for x in self.files_widget_list if x.chosen]
        # 检查重复
        lis = []
        for i in candidate:
            if i.output_name in lis:
                # TODO 文件重复
                return
            lis.append(i.output_name)
        for i in candidate:
            if i.chosen:
                i.do_rename()
