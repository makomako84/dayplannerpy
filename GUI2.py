import  sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QPushButton, QAction, qApp
from PyQt5.QtGui import QIcon
from API.DayPlanner import DayPlanner
from datetime import  date, datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.resize(640,480)
        self.center()
        self.setWindowTitle('Day Planner Py by Galimsky')

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        outAction = QAction('Out calend', self)
        outAction.setStatusTip('Out calend tasks data')
        outAction.triggered.connect(self.out_tasks)

        outFilteredAction = QAction('Out filtered', self)
        outFilteredAction.setStatusTip('Out today task')
        outFilteredAction.triggered.connect(self.out_filtered)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        commandsMenu = menubar.addMenu('&Commands')
        commandsMenu.addAction(outAction)
        commandsMenu.addAction(outFilteredAction)

        # button_out = QPushButton('Out calend', self)
        # button_out.resize(button_out.sizeHint())


        self.show()

    def out_tasks(self):
        dp = DayPlanner()
        for task in  dp.get_tasks():
            print(task.__str__())
    def out_filtered(self):
        dp = DayPlanner()
        currentdate = date.today()
        for task in dp.get_tasks_filtered_by_date(currentdate):
            print(task.__str__())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
