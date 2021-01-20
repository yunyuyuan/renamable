from os.path import join, normpath

from PyQt5.Qt import *


def set_css(widget: QWidget, filepath):
    with open(filepath, encoding='utf-8') as fp:
        widget.setStyleSheet(fp.read())


def update_css(widget: QWidget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


def parse_path(*args):
    return normpath(join(*args))
