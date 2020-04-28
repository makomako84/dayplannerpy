import  sys
from datetime import  date
from pydispatch import dispatcher


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from API.DayPlanner import DayPlanner
from API.Objects.Task import  Task
from GUI.widgets import TabWidget, LeftSideWidget, RightSideWidget

TASK_PICKED = 'task-picked'

class TasksListItem(QListWidgetItem):
    def __init__(self,uuid, parent=None):
        super(TasksListItem, self).__init__(parent)
        self.uuid = uuid

class PickedTaskWidget(RightSideWidget):
    def __init__(self, parent=None):
        super(PickedTaskWidget, self).__init__(parent)
        self.hide()

    def initUI(self, layout : QFormLayout):
        namelabel = QLabel("Name: ")
        self.nameedit = QLineEdit()

        datetimelabel = QLabel("Date: ")
        self.datetimeedit = QDateTimeEdit()

        descriptionlabel = QLabel("Description: ")
        self.descriptionedit = QTextEdit()

        isdonelabel = QLabel("Is task done: ")
        self.isdoneedit = QCheckBox()

        self.cancelbutton = QPushButton("Cancel")
        self.cancelbutton.clicked.connect(lambda: self.hide())
        self.applybutton = QPushButton("Save")

        buttonslayout = QHBoxLayout()

        layout.addRow(namelabel, self.nameedit)
        layout.addRow(datetimelabel, self.datetimeedit)
        layout.addRow(descriptionlabel, self.descriptionedit)
        layout.addRow(isdonelabel, self.isdoneedit)
        buttonslayout.addWidget(self.cancelbutton)
        buttonslayout.addWidget(self.applybutton)
        layout.addRow(buttonslayout)


    def updateItem(self, task:Task):
        self.nameedit.setText(task.name)
        self.datetimeedit.setDateTime(task.datetime)
        self.descriptionedit.setText(task.description)
        self.isdoneedit.setCheckState(task.done)
        self.show()


    def apply_button_clicked(self):
        pass
    def cancel_button_clicked(self):
        self.hide()

class DayTasksListWidget(LeftSideWidget):
    def __init__(self,parent=None):
        super(DayTasksListWidget, self).__init__(parent)
        self.__selectedtask  = None
        self.tasksListWidget.setSelectionMode(QAbstractItemView.ContiguousSelection)

    @property
    def selectedtask(self):
        return self.__selectedtask

    @selectedtask.setter
    def selectedtask(self, value):
        self.__selectedtask = value
        dispatcher.send(signal=TASK_PICKED, sender=self)

    def initUI(self, layout):

        headLabel  = QLabel()
        headLabel.setText("Today")
        headLabel.setAlignment(Qt.AlignLeft)

        self.tasksListWidget = QListWidget()

        self.updateItems()

        self.tasksListWidget.itemClicked.connect(self.taskClicked)
        self.tasksListWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.tasksListWidget.show()

        layout.addWidget(headLabel)
        layout.addWidget(self.tasksListWidget)

    def selectionChanged(self):
        if len(self.tasksListWidget.selectedItems()) == 0:
            self.selectedtask = None

    def taskClicked(self):
        sender = self.sender()
        dp = DayPlanner()
        self.selectedtask = dp.find_task_by_uuid_str(sender.selectedItems()[0].uuid)


    def updateItems(self):
        dp = DayPlanner()
        current_date_tasks = dp.get_tasks_filtered_by_date(date.today())
        self.tasksListWidget.clear()

        for task in current_date_tasks:
            task_time = task.datetime.strftime("%H:%M")
            newItem = TasksListItem(task.uuid)
            newItem.setText(f"{task_time} {task.name}")
            self.tasksListWidget.addItem(newItem)

class DayTasksWidget(TabWidget):
    def __init__(self,parent=None):
        super(DayTasksWidget, self).__init__(parent)

    def initUI(self,layout):
        self.leftside = DayTasksListWidget()
        self.rightside = PickedTaskWidget()
        layout.addWidget(self.leftside)
        layout.addWidget(self.rightside)

        dispatcher.connect(self.task_picked_handler, signal=TASK_PICKED, sender=dispatcher.Any)

    def task_picked_handler(self,sender):
        if(sender.selectedtask != None):
            self.rightside.updateItem(sender.selectedtask)
        else:
            self.rightside.hide()