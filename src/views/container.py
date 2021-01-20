import re
from os import listdir
from os.path import dirname, basename, isfile, join

from PyQt5.Qt import *

from src.components.body_file_row import FileRow
from src.utils import set_css
from src.views.about import About


class Container(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("container")
        self.setWindowTitle("批量重命名工具")
        self.body_layout = QVBoxLayout()
        self.files_widget_list = []
        self.all_chosen = False
        self.can_run = False

        from src.views.menu import Menu
        self.menubar = Menu(self)
        self.frame_head = QFrame(self)
        self.frame_body = QFrame(self)
        self.dialog_about = About(self)
        self.body_table = QTableWidget(0, 4, self.frame_body)

        self.input_regx = QLineEdit(self.frame_head)
        self.input_regx.setPlaceholderText("输入正则表达式")
        self.out_regx = QLineEdit(self.frame_head)

        self.out_regx.setPlaceholderText("输出")

        self.set_layout()
        self.connect()
        self.set_class()
        set_css(self, "src/views/container.css")
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
        self.body_layout.addWidget(self.body_table)
        self.frame_body.setLayout(self.body_layout)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        menu_layout = QHBoxLayout()
        menu_layout.addWidget(self.menubar)
        layout.addLayout(menu_layout)
        layout.addWidget(self.frame_head)
        layout.addWidget(self.frame_body)
        self.setLayout(layout)

    def connect(self):
        self.input_regx.textChanged.connect(self.apply_regx)
        self.out_regx.textChanged.connect(self.apply_regx)

    def set_class(self):
        self.frame_head.setProperty("class", "head")
        self.frame_body.setProperty("class", "body")

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
                file.update_regx(self.input_regx.text(), self.out_regx.text())
                file.choose_change.connect(lambda b: self.choose_state_change())
                self.files_widget_list.append(file)
                start_row += 1
        self.body_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.file_changed()

    def apply_regx(self):
        input_, output_ = self.input_regx.text(), self.out_regx.text()
        for i in self.files_widget_list:
            try:
                i.update_regx(input_, output_)
            except re.error:
                break

    # ------------ footer -------------

    def choose_state_change(self):
        all_chosen = True
        for i in self.files_widget_list:
            if not i.chosen:
                all_chosen = False
                break
        self.all_chosen = all_chosen
        self.file_changed()

    def change_select_all(self):
        self.all_chosen = not self.all_chosen
        for i in self.files_widget_list:
            i.change_choose(self.all_chosen)
        self.file_changed()

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
        self.file_changed()

    def file_changed(self):
        self.menubar.action_choose_all.setText("全不选" if self.all_chosen else "全选")
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
        candidate = [x for x in self.files_widget_list if x.chosen]
        # 检查重复
        lis = []
        error_files = []
        for i in candidate:
            if i.file_exist:
                QMessageBox.warning(None, "文件已存在", f"文件(夹){i.output_name}已经存在，无法执行!", QMessageBox.Yes, QMessageBox.Yes)
                return
            if i.output_name in lis:
                for file in candidate:
                    file.set_same_name_warn(i.output_name)
                QMessageBox.warning(None, "文件名重复", f"文件名{i.output_name}存在重复，无法执行!", QMessageBox.Yes, QMessageBox.Yes)
                return
            lis.append(i.output_name)
        for i in candidate:
            if not i.do_rename():
                error_files.append(i.input_name)
        QMessageBox.critical(None, "重命名失败", f"以下文件{error_files}重命名失败!", QMessageBox.Yes, QMessageBox.Yes)
