from PyQt5.Qt import *

from src.utils import set_css
from src.views.container import Container


class Menu(QMenuBar):
    def __init__(self, container: Container):
        super().__init__(container)
        self.container = container
        self.tab_file = QMenu('文件', self)
        self.tab_edit = QMenu('操作', self)
        self.tab_about = QAction('关于', self)
        self.action_choose_all = QAction('全选', self)
        self.action_delete_chosen = QAction('删除所选', self)
        self.action_do_it = QAction('执行所选', self)

        self.bind_action()
        self.set_element()
        set_css(self, 'assets/menu.css')

    def bind_action(self):
        action_add_file = QAction('导入文件', self)
        action_add_file.triggered.connect(self.container.import_files)
        self.tab_file.addAction(action_add_file)
        action_add_folder = QAction('导入文件夹', self)
        action_add_folder.triggered.connect(self.container.import_folder)
        self.tab_file.addAction(action_add_folder)

        self.action_choose_all.triggered.connect(self.container.change_select_all)
        self.action_delete_chosen.triggered.connect(self.container.remove_file_row)
        self.action_do_it.triggered.connect(self.container.do_operate)
        action_back_up = QAction('备份文件夹', self)
        action_back_up.setCheckable(True)
        action_back_up.setChecked(False)
        action_back_up.triggered.connect(self.container.set_back_up)
        self.tab_edit.addAction(self.action_choose_all)
        self.tab_edit.addAction(action_back_up)
        self.tab_edit.addAction(self.action_delete_chosen)
        self.tab_edit.addAction(self.action_do_it)

        # self.tab_about.triggered.connect(lambda: self.container.dialog_about.exec())
        self.tab_about.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/yunyuyuan/renamable")))

    def set_element(self):
        self.action_choose_all.setEnabled(False)
        self.action_delete_chosen.setEnabled(False)
        self.action_do_it.setEnabled(False)
        self.addMenu(self.tab_file)
        self.addMenu(self.tab_edit)
        self.addAction(self.tab_about)
