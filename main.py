from src.views.container import Container

if __name__ == '__main__':
    from sys import argv, exit
    from PyQt5.Qt import QApplication
    app = QApplication(argv)
    obj = Container()
    exit(app.exec_())
