from PyQt5.Qt import *
from os import listdir
from os.path import dirname, basename

from src.components.button import Button


class Container(QWidget):
    def __init__(self):
        super().__init__()
        self.body_layout = QVBoxLayout()

        self.frame_head = QFrame(self)
        self.frame_body = QFrame(self)
        self.frame_footer = QFrame(self)

        self.btn_choose_files = Button("批量选择文件", self.frame_head)
        self.btn_choose_folder = Button("导入整个文件夹", self.frame_head)

        self.input_regx = QLineEdit(self.frame_head)
        self.input_regx.setPlaceholderText("输入正则表达式")
        self.out_regx = QLineEdit(self.frame_head)
        self.out_regx.setPlaceholderText("输出")

        self.change_select_all = Button("全选", self.frame_footer)
        self.do_it = Button("执行操作", self.frame_footer)

        self.set_layout()
        self.connect()
        self.show()

    def set_layout(self):
        head_layout = QGridLayout()
        head_layout.addWidget(self.btn_choose_files, 0, 0, 1, 4)
        head_layout.addWidget(self.btn_choose_folder, 0, 4, 1, 4)
        head_layout.addWidget(self.input_regx, 1, 0, 1, 3)
        head_layout.addWidget(QLabel("→", self.frame_head), 1, 3, 1, 2)
        head_layout.addWidget(self.out_regx, 1, 5, 1, 3)
        self.frame_head.setLayout(head_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.frame_head)
        layout.addWidget(self.frame_body)
        layout.addWidget(self.frame_footer)
        self.setLayout(layout)

    def connect(self):
        self.btn_choose_files.clicked.connect(self.import_files)
        self.btn_choose_folder.clicked.connect(self.import_folder)

    def import_files(self):
        files_list, _ = QFileDialog.getOpenFileUrls(self, caption="选择文件", filter="All Files(*)")
        if len(files_list):
            self.apply_files(dirname(files_list[0].toLocalFile()), [basename(x.toLocalFile()) for x in files_list])

    def import_folder(self):
        folder = QFileDialog.getExistingDirectoryUrl(self, caption="选择文件夹")
        dir_path = folder.toLocalFile()
        self.apply_files(dir_path, listdir(dir_path))

    def apply_files(self, dir_path, name_list):
        pass
