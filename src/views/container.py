from PyQt5.Qt import *

from src.components.button import Button


class Container(QWidget):
    def __init__(self):
        super().__init__()

        self.frame_head = QFrame(self)
        self.frame_body = QFrame(self)
        self.frame_footer = QFrame(self)

        self.btn_choose_files = Button("批量选择文件", self.frame_head)
        self.btn_choose_folder = Button("导入整个文件夹", self.frame_head)

        self.input_regx = QLineEdit(self.frame_head)
        self.input_regx.setPlaceholderText("输入正则表达式")
        self.do_it = Button("执行操作", self.frame_head)

        self.change_hide_filter_file = Button("隐藏已排除的文件", self.frame_footer)
        self.change_select_all = Button("全选", self.frame_footer)

        layout = QVBoxLayout()
        layout.addWidget(self.frame_head)
        layout.addWidget(self.frame_body)
        layout.addWidget(self.frame_footer)
        self.setLayout(layout)
