import  sys
import  json
import  pprint
from datetime import  datetime
from API.Objects.Task import Task
import  os

print(__file__)
DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), 'data.json')




class DayPlanner:
    data = {
        "Tasks": [],
        "Phones": []
    }

    def __init__(self):
        # self.test_create_tasks()
        self.initObjectData()
        self.shell_main_menu()

        # self.updateJSON()

        # self.shell_main_menu()
    def shell_main_menu(self):
        if(len(sys.argv) <2): return

        firstarg = sys.argv[1]

        if firstarg == '-calend':
            if(len(sys.argv) < 3) : return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.out_tasks()
            elif secondarg == 'add':
                self.shell_create_task()
        elif firstarg == '-book':
            if (len(sys.argv) < 3): return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.out_phones()

    def shell_create_task(self):
        ui = {}
        ui["name"] = input("Enter task name: ")
        ui["date"] = input("enter date in form: YYYY-M-D H:M ")
        ui["done"] = True if input("Is task done? y/n ") else False
        self.add_new_task(ui)

    def out_tasks(self):
        [print(task.__str__()+"\n") for task in self.data["Tasks"]]
    def out_phones(self):
        print(*self.phones, sep='\n')

    def readJSON(self):
        with open(DATA_FILE_NAME, "r") as read_file:
            return json.load(read_file)

    def updateJSON(self):
        jsondata = {
            "Tasks" : [task.encodeJSON() for task in self.data["Tasks"]],
            "Phones" : []
        }
        with open(DATA_FILE_NAME, "w") as write_file:
            json.dump(jsondata, write_file, indent=4)

    def initObjectData(self):
        nonobjectdata = self.readJSON()
        for task in nonobjectdata["Tasks"]:
            self.data["Tasks"].append(Task.decodeJSON(task))
        # pprint.pprint(self.data)
        # [print(task) for task in self.data["Tasks"]]

    def add_new_task(self,dict):
        self.data["Tasks"].append(Task.decodeJSON(dict))
        self.updateJSON()

    def create_new_task(self, name, done, date):
        self.data["Tasks"].append(Task(name, done, date))
        self.updateJSON()

    def craete_new_phone(self):
        pass

    def test_create_tasks(self):
        t1 = Task("Buy clothes", True, datetime.now())
        t2 = Task("Update pip packages", False, datetime.now())
        self.data["Tasks"].append(t1)
        self.data["Tasks"].append(t2)


dayPlanner = DayPlanner()
# print(sys.argv[1])
