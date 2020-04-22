import  sys
import  json
import  pprint
from datetime import  datetime
from  API.Objects.Task import  Task

DATA_FILE_NAME = "data.json"




class DayPlanner:
    data = {
        "Tasks": [],
        "Phones": []
    }

    def __init__(self):
        # self.test_create_tasks()
        self.initObjectData()
        self.create_new_task("read book",False, datetime(2020, 5,20))
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
        elif firstarg == '-book':
            if (len(sys.argv) < 3): return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.out_phones()

    def out_tasks(self):
        print(*self.tasks, sep='\n')
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
        pprint.pprint(self.data)
        [print(task) for task in self.data["Tasks"]]

    def create_new_task(self, name, done, date):
        self.data["Tasks"].append(Task(name,done, date))
        self.updateJSON()

    def craete_new_phone(self):
        pass

    def test_create_tasks(self):
        t1 = Task("Buy clothes",True, datetime.now())
        t2 = Task("Update pip packages", False, datetime.now())
        self.data["Tasks"].append(t1)
        self.data["Tasks"].append(t2)


dayPlanner = DayPlanner()
# print(sys.argv[1])
