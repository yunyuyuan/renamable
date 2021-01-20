from PyQt5.Qt import *

from src.utils import set_css


class About(QDialog):
    def __init__(self, container):
        super().__init__(container)
        self.setObjectName("about")
        self.setWindowTitle("关于")
        self.container = container

        self.title_label = QLabel("一个批量重命名工具，仅此而已", self)
        self.url_to_git_label = QLabel("", self)

        self.set_layout()
        set_css(self, 'src/views/about.css')
        self.hide()

    def set_layout(self):
        pass
