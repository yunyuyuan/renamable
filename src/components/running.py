from PyQt5.Qt import *

from src.components.button import Button


class Runner(QThread):
    cursor = pyqtSignal(int)
    finish_args = pyqtSignal(str, str, str)
    abort = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lis = []
        self.backup = False
        self.aborted = False

        self.abort.connect(self.set_abort)

    def set_args(self, lis, backup):
        self.lis = lis
        self.backup = backup

    def set_abort(self):
        self.aborted = True

    def run(self):
        self.aborted = False
        # 检查重复
        lis = []
        for i in self.lis:
            if i.file_exist:
                self.finish_args.emit('warn', "文件已存在", f"文件(夹)<b>{i.output_name}</b>已经存在，无法执行!")
                return
            if i.output_name in lis:
                for file in lis:
                    file.set_same_name_warn(i.output_name)
                self.finish_args.emit('warn', "文件名重复", f"文件名<b>{i.output_name}</b>存在重复，无法执行!")
                return
            lis.append(i.output_name)
        # 执行
        cursor = 0
        for i in self.lis:
            if self.aborted:
                return
            error = i.do_rename(self.backup)
            if error:
                self.finish_args.emit('error', "重命名失败", f"文件<b>{i.input_name}</b>重命名失败!Error:{error}")
                return
            cursor += 1
            self.cursor.emit(cursor)
        self.finish_args.emit('success', "重命名成功", f"所有<b>{len(self.lis)}</b>个文件重命名成功!")


class Running(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.runner = Runner(self)
        self.progress = QProgressBar(self)
        self.progress.setEnabled(False)
        self.percentage_label = QLabel("0/0", self)
        self.abort_btn = Button("中断", self)
        self.abort_btn.setEnabled(False)

        self.runner.cursor.connect(self.change_cursor)
        self.runner.finished.connect(self.set_finished)

        layout = QHBoxLayout()
        layout.addWidget(self.progress)
        layout.addWidget(self.percentage_label)
        layout.addWidget(self.abort_btn)
        self.setLayout(layout)

    def run(self, lis, backup):
        self.progress.setMaximum(len(lis))
        self.progress.setEnabled(True)
        self.progress.setValue(0)
        self.percentage_label.setText(f"0/{len(lis)}")

        self.runner.set_args(lis, backup)
        self.runner.start()
        self.abort_btn.setEnabled(True)

    def change_cursor(self, cursor):
        self.progress.setValue(cursor)
        self.percentage_label.setText(f"{cursor}/{self.progress.maximum()}")

    def set_finished(self):
        self.progress.setValue(0)
        self.progress.setEnabled(False)
        self.percentage_label.setText("0/0")
        self.abort_btn.setEnabled(False)
