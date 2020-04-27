import  sys
from datetime import  date, datetime
from pydispatch import dispatcher


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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

    def initUI(self, layout):
        self.label = QLabel()
        self.label.setText("")
        layout.addWidget(self.label)

    def updateItem(self, task):
        self.label.setText(task.__str__())

class DayTasksListWidget(LeftSideWidget):
    def __init__(self,parent=None):
        super(DayTasksListWidget, self).__init__(parent)
        self.set_selectedItem(None)

    def set_selectedItem(self, value):
        self.__selectedItem = value
        dispatcher.send(signal=TASK_PICKED, sender=self)
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
        dp = DayPlanner()
        foundTask = dp.find_task_by_uuid_str(sender.selectedItems()[0].uuid)
        self.set_selectedItem(foundTask)


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
        self.rightside.updateItem(sender.get_selectedItem())