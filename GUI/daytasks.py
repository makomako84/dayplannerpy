import  sys
from datetime import  date, datetime
from pydispatch import dispatcher


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from API.DayPlanner import DayPlanner
from API.Objects.Task import  Task
from GUI.widgets import TabWidget, LeftSideWidget, RightSideWidget

TASK_PICKED = 'task-picked'
DATE_PICKED = 'date-picked'

class TasksListItem(QListWidgetItem):
    def __init__(self,uuid, parent=None):
        super(TasksListItem, self).__init__(parent)
        self.uuid = uuid

class PickedTaskWidget(RightSideWidget):
    def __init__(self, parent=None):
        super(PickedTaskWidget, self).__init__(parent)
        self.__datachanged = False
        self.__editedtask = None
        self.hide()

    @property
    def editedtask(self):
        return self.__editedtask
    @editedtask.setter
    def editedtask(self,value):
        self.__editedtask = value

    def raisedatachanged(self):
        self.__datachanged = True
        self.editedtask.name = self.nameedit.text()
        self.editedtask.datetime = self.datetimeedit.dateTime().toPyDateTime()
        self.editedtask.description = self.descriptionedit.toPlainText()
        self.editedtask.done = True if self.isdoneedit.checkState()==2 else False
        print(self.editedtask.__str__())

    def initUI(self, layout : QFormLayout):
        namelabel = QLabel("Name: ")
        self.nameedit = QLineEdit()


        datetimelabel = QLabel("Date: ")
        self.datetimeedit = QDateTimeEdit()

        descriptionlabel = QLabel("Description: ")
        self.descriptionedit = QTextEdit()

        isdonelabel = QLabel("Is task done: ")
        self.isdoneedit = QCheckBox()
        self.isdoneedit.setTristate(on=False)

        self.cancelbutton = QPushButton("Cancel")
        self.cancelbutton.clicked.connect(self.hide)

        self.deletebutton = QPushButton("Delete")
        self.deletebutton.clicked.connect(self.deletetask_button_clicked)

        self.applybutton = QPushButton("Save")
        self.applybutton.clicked.connect(self.apply_button_clicked)



        buttonslayout = QHBoxLayout()

        layout.addRow(namelabel, self.nameedit)
        layout.addRow(datetimelabel, self.datetimeedit)
        layout.addRow(descriptionlabel, self.descriptionedit)
        layout.addRow(isdonelabel, self.isdoneedit)
        buttonslayout.addWidget(self.cancelbutton)
        buttonslayout.addWidget(self.deletebutton)
        buttonslayout.addWidget(self.applybutton)
        layout.addRow(buttonslayout)


    def updateItem(self, task:Task):
        self.editedtask = task

        self.nameedit.setText(task.name)
        self.datetimeedit.setDateTime(task.datetime)
        self.descriptionedit.setText(task.description)
        self.isdoneedit.setChecked(task.done)


        self.nameedit.textChanged.connect(self.raisedatachanged)
        self.datetimeedit.dateTimeChanged.connect(self.raisedatachanged)
        self.descriptionedit.textChanged.connect(self.raisedatachanged)
        self.isdoneedit.stateChanged.connect(self.raisedatachanged)

        self.show()

    def hide(self):
        try:
            self.nameedit.textChanged.disconnect()
            self.datetimeedit.dateTimeChanged.disconnect()
            self.descriptionedit.textChanged.disconnect()
            self.isdoneedit.stateChanged.disconnect()
            self.__datachanged = False
        except TypeError:
            print("not connected")
        super().hide()


    # this method is responds for saving data in RightWidget dayTask
    def apply_button_clicked(self):
        if self.__datachanged:
            print("SAVING DATA")
            self.__datachanged = False
            dp = DayPlanner()
            dp.save_task(self.editedtask)
            dispatcher.send(signal=DATE_PICKED, sender=self)


    def deletetask_button_clicked(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Are you sure?")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msg.buttonClicked.connect(self.deletetask_confirmed)

        retval = msg.exec_()
        if retval == QMessageBox.Ok:
            self.deletetask_confirmed()

    def deletetask_confirmed(self):
        dp = DayPlanner()
        dp.delete_task_byuuid(self.editedtask.uuid)
        dispatcher.send(signal=DATE_PICKED, sender=self)
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

        # headLabel  = QLabel()
        # headLabel.setText("Today")
        # headLabel.setAlignment(Qt.AlignLeft)

        self.tasksListWidget = QListWidget()


        self.tasksListWidget.itemClicked.connect(self.taskClicked)
        self.tasksListWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.tasksListWidget.show()

        # layout.addWidget(headLabel)
        layout.addWidget(self.tasksListWidget)

    def selectionChanged(self):
        if len(self.tasksListWidget.selectedItems()) == 0:
            self.selectedtask = None

    def taskClicked(self):
        sender = self.sender()
        dp = DayPlanner()
        self.selectedtask = dp.find_task_by_uuid_str(sender.selectedItems()[0].uuid)


    def updateItems(self, dt: date):
        dp = DayPlanner()
        current_date_tasks = dp.get_tasks_filtered_by_date(dt)
        self.tasksListWidget.clear()

        for task in current_date_tasks:
            task_time = task.datetime.strftime("%H:%M")
            newItem = TasksListItem(task.uuid)
            newItem.setText(f"{task_time} {task.name}")
            self.tasksListWidget.addItem(newItem)

# this is layout top class
class DayTasksWidget(TabWidget):
    def __init__(self,parent=None):
        super(DayTasksWidget, self).__init__(parent)
        self.dateedit.setDate(date.today())
        self.newtaskbutton.clicked.connect(self.create_task_handler)


    def initUI(self,layout):
        self.leftside = DayTasksListWidget()
        self.rightside = PickedTaskWidget()
        layout.addWidget(self.leftside)
        layout.addWidget(self.rightside)


        dispatcher.connect(self.task_picked_handler, signal=TASK_PICKED, sender=dispatcher.Any)
        dispatcher.connect(self.date_picked_handler, signal=DATE_PICKED, sender=dispatcher.Any)

    def initHeader(self, headerlayout:QHBoxLayout):
        datelabel = QLabel("Current date: ")
        self.dateedit = QDateEdit()
        self.dateedit.setMaximumWidth(150)
        self.newtaskbutton = QPushButton("Create new task")
        headerlayout.addWidget(datelabel)
        headerlayout.addWidget(self.dateedit)
        headerlayout.addWidget(self.newtaskbutton)
        self.dateedit.dateChanged.connect(self.date_picked_handler)

    def create_task_handler(self):
        dp = DayPlanner()
        temptask = dp.get_temp_task(self.dateedit.dateTime().toPyDateTime())
        self.rightside.hide()
        self.rightside.updateItem(temptask)

    def task_picked_handler(self,sender):
        if(sender.selectedtask != None):
            self.rightside.hide()
            self.rightside.updateItem(sender.selectedtask)
        else:
            self.rightside.hide()

    def date_picked_handler(self, sender):
        self.leftside.updateItems(self.dateedit.dateTime().toPyDateTime().date())