import  sys
from datetime import  date
from pydispatch import dispatcher


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from API.DayPlanner import DayPlanner
from GUI.widgets import TabWidget, LeftSideWidget, RightSideWidget

TASK_PICKED = 'task-picked'

class TasksListItem(QListWidgetItem):
    def __init__(self,uuid, parent=None):
        super(TasksListItem, self).__init__(parent)
        self.uuid = uuid

class PickedTaskWidget(RightSideWidget):
    def __init__(self, parent=None):
        super(PickedTaskWidget, self).__init__(parent)
        self.pickedTaskText = None

    def initUI(self, layout : QFormLayout):
        self.nameedit = QLabel("Name: ")
        self.dateedit = QLabel("Date: ")
        self.descriptionedit = QLabel("Description: ")
        self.isdoneedit = QCheckBox("Is task done")
        self.applybutton = QPushButton("Save")

        layout.addRow(self.nameedit, QLineEdit())
        layout.addRow(self.dateedit, QDateTimeEdit())
        layout.addRow(self.descriptionedit, QTextEdit())
        layout.addRow(self.isdoneedit)
        layout.addRow(self.applybutton)

    def updateItem(self, task):
        # self.label.setText(task.__str__())
        pass

class DayTasksListWidget(LeftSideWidget):
    def __init__(self,parent=None):
        super(DayTasksListWidget, self).__init__(parent)
        self.__selectedtask  = None

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
        self.tasksListWidget.show()

        layout.addWidget(headLabel)
        layout.addWidget(self.tasksListWidget)

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
        self.rightside.updateItem(sender.selectedtask)