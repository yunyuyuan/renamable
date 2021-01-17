from PyQt5.Qt import *


class FileRow(QFrame):
    def __init__(self, body, container):
        super().__init__(body)
        self.body, self.container = body, container

        self.choose_state = QLabel(self)

    def update_regx(self, input_, output_):
        pass
