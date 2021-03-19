import sys
from datetime import  date

from PyQt5.QtWidgets import \
    (QTabWidget, QMainWindow, QAction,
    QDesktopWidget,QApplication)
print(sys.executable)
from API.DayPlanner import DayPlanner

from GUI.daytasks import DayTasksWidget
from GUI.widgets import TabWidget



class GUITabs(QTabWidget):
    def __init__(self, parent=None):
        super(GUITabs, self).__init__(parent)
        self.tab1 = DayTasksWidget()
        self.tab2 = TabWidget()

        self.addTab(self.tab1, "Day Tasks")
        self.addTab(self.tab2, "PhonesBook")


    # def tab2UI(self):
        # layout = QFormLayout()
        # sex = QHBoxLayout()
        # sex.addWidget(QRadioButton("Male"))
        # sex.addWidget(QRadioButton("Female"))
        # layout.addRow(QLabel("Sex"), sex)
        # layout.addRow("Date of Birth", QLineEdit())
        # self.setTabText(1, "PhonesBook")
        # self.tab2.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.center()
        self.setWindowTitle('Day Planner Py by Galimsky')
        self.guitabs = GUITabs(self)
        self.setCentralWidget(self.guitabs)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        outAction = QAction('Out calend', self)
        outAction.setStatusTip('Out calend tasks data')
        outAction.triggered.connect(self.out_tasks)

        dayAnalyseAction = QAction('Day analyse', self)
        dayAnalyseAction.setStatusTip('Get picked date tasks accomplishment')
        dayAnalyseAction.triggered.connect(self.out_analyse)

        outFilteredAction = QAction('Out filtered', self)
        outFilteredAction.setStatusTip('Out today task')
        outFilteredAction.triggered.connect(self.out_filtered)

        openDayTasksAction = QAction('DayTasks', self)
        openDayTasksAction.setStatusTip('Open today todo tasks')
        openDayTasksAction.triggered.connect(lambda : self.guitabs.setCurrentIndex(0))

        openPhonesBookAction = QAction('PhonesBook', self)
        openPhonesBookAction.setStatusTip('Open phonebook')
        openPhonesBookAction.triggered.connect(lambda : self.guitabs.setCurrentIndex(1))


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        commandsMenu = menubar.addMenu('&Commands')
        commandsMenu.addAction(outAction)
        commandsMenu.addAction(outFilteredAction)
        commandsMenu.addAction(dayAnalyseAction)

        appMenu = menubar.addMenu('&Application')
        appMenu.addAction(openDayTasksAction)
        appMenu.addAction(openPhonesBookAction)


        # guiTabs = GUITabsWidget()
        #
        # self.setCentralWidget(guiTabs)

        self.show()

    def _on_radio_button_clicked(self, button):
        print(button)
        self.label.setText('Current: ' + button.text())


    def out_tasks(self):
        dayPlanner = DayPlanner()
        for task in  dayPlanner.get_tasks():            
            print(task.__str__())

    def out_filtered(self):
        dayPlanner = DayPlanner()
        currentdate = date.today()
        for task in dayPlanner.get_tasks_filtered_by_date(currentdate):
            print(task.__str__())

    def out_analyse(self):
        dayPlanner = DayPlanner()
        currentdate = date.today()
        todayTasks = dayPlanner.get_tasks_filtered_by_date(currentdate)
        doneTasks = list(filter(lambda task: task.done == True, todayTasks))
        print("number of donet tasks today: {} / {}".format(len(doneTasks), len(todayTasks)))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
