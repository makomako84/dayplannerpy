import  sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from API.DayPlanner import DayPlanner
from datetime import  date, datetime

class TasksListItem(QListWidgetItem):
    def __init__(self,task, parent=None):
        super(TasksListItem, self).__init__(parent)
        self.task = task

class RightSideWidget(QWidget):
    def __init__(self, parent=None):
        super(RightSideWidget, self).__init__(parent)
        self.setFixedWidth(250)
        verticalLayout = QVBoxLayout()

        label = QLabel()
        label.setText("Right side")
        verticalLayout.addWidget(label)


        self.setLayout(verticalLayout)

class LeftSideWidget(QWidget):
    def __init__(self, parent=None):
        super(LeftSideWidget, self).__init__(parent)
        self.setMinimumWidth(450)
        self.setMaximumWidth(750)
        verticalLayout = QVBoxLayout()
        self.initUI(verticalLayout)
        self.setLayout(verticalLayout)

    def initUI(self, layout):
        label = QLabel()
        label.setText("Left side")
        layout.addWidget(label)

class DayTasksWidget(LeftSideWidget):
    def __init__(self,parent=None):
        super(DayTasksWidget, self).__init__(parent)
        self.set_selectedItem(None)

    def set_selectedItem(self, value):
        self.__selectedItem = value
    def get_selectedItem(self):
        return  self.__selectedItem

    def initUI(self, layout):

        headLabel  = QLabel()
        headLabel.setText("Today")
        headLabel.setAlignment(Qt.AlignLeft)

        self.tasksListWidget = QListWidget()

        self.updateItems()

        self.tasksListWidget.itemClicked.connect(self.itemClicked)
        self.tasksListWidget.show()

        layout.addWidget(headLabel)
        layout.addWidget(self.tasksListWidget)

    def itemClicked(self):
        sender = self.sender()
        print(sender)
        print(type(sender))
        # QListWidget.selectedItems()

        print(sender.selectedItems()[0])

    def updateItems(self):
        dp = DayPlanner();
        current_date_tasks = dp.get_tasks_filtered_by_date(date.today())
        self.tasksListWidget.clear()

        for task in current_date_tasks:
            task_time = task.datetime.strftime("%H:%M")
            self.tasksListWidget.addItem(f"{task_time} {task.name}")

class GUITabs(QTabWidget):
    def __init__(self, parent=None):
        super(GUITabs, self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "Day Tasks")
        self.addTab(self.tab2, "PhonesBook")
        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        self.setTabText(0, "DayTasks")

        tabLayout = QHBoxLayout()
        # tasksLayout = QVBoxLayout()

        leftSide = DayTasksWidget(self)
        rightSide = RightSideWidget(self)

        tabLayout.addWidget(leftSide)
        tabLayout.addWidget(rightSide)


        self.tab1.setLayout(tabLayout)

    def tab2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"), sex)
        layout.addRow("Date of Birth", QLineEdit())
        self.setTabText(1, "PhonesBook")
        self.tab2.setLayout(layout)

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
