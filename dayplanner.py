import  sys
import  json
import  pprint
from datetime import  datetime
from API.Objects.Task import Task
import  os

# private
DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), 'data.json')



class DayPlanner:


    __data = {
        "Tasks": [],
        "Phones": []
    }

    def __init__(self):
        # self.test_create_tasks()
        self.__initObjectData()
        self.shell_main_menu()
        # self.updateJSON()
        # self.shell_main_menu()

    def __initObjectData(self):
        nonobjectdata = self.readJSON()
        for task in nonobjectdata["Tasks"]:
            self.__data["Tasks"].append(Task.decodeJSON(task))

    def shell_main_menu(self):
        if(len(sys.argv) <2): return

        firstarg = sys.argv[1]

        if firstarg == '-calend':
            if(len(sys.argv) < 3) : return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.out_tasks()
            elif secondarg == 'add':
                self.shell_add_task()
            elif secondarg == 'find':
                self.shell_find_task()
            elif secondarg == 'del':
                self.shell_del_task()
        elif firstarg == '-book':
            if (len(sys.argv) < 3): return
            secondarg = sys.argv[2]
            if secondarg == 'out':
                self.out_phones()

    def shell_add_task(self):
        ui = {}
        ui["name"] = input("Enter task name: ")
        ui["date"] = input("enter date in form: YYYY-M-D H:M ")
        ui["done"] = True if input("Is task done? y/n ") else False
        self.add_new_task(ui)

    def shell_find_task(self):
        ui={}
        ui["name"] = input("Enter part of task name: ")

        searchfunc = lambda x: x.name.find(ui["name"])!=-1
        res = list(filter(searchfunc, self.__data["Tasks"]))
        [print(x) for x in res]
        return  res

    def shell_del_task(self):
        res = self.shell_find_task()
        if len(res) > 1:
            print("Create more Accureate request")
        else:
            delaquired = True if input("Delete? (y)") == "y" else False
            if(delaquired):
                self.__data["Tasks"]  = list(filter((lambda task: res[0]!=task),self.__data["Tasks"]))
                self.updateJSON()


    # tasks functions
    def out_tasks(self):
        [print(task.__str__()+"\n") for task in self.__data["Tasks"]]
    def add_new_task(self,dict):
        self.__data["Tasks"].append(Task.decodeJSON(dict))
        self.updateJSON()

    def out_phones(self):
        print(*self.phones, sep='\n')


    # work with JSON
    def readJSON(self):
        with open(DATA_FILE_NAME, "r") as read_file:
            return json.load(read_file)
    def updateJSON(self):
        jsondata = {
            "Tasks" : [task.encodeJSON() for task in self.__data["Tasks"]],
            "Phones" : []
        }
        with open(DATA_FILE_NAME, "w") as write_file:
            json.dump(jsondata, write_file, indent=4)



    def test_create_new_task(self, name, done, date):
        self.__data["Tasks"].append(Task(name, done, date))
        self.updateJSON()

    def test_craete_new_phone(self):
        pass

    def test_create_tasks(self):
        t1 = Task("Buy clothes", True, datetime.now())
        t2 = Task("Update pip packages", False, datetime.now())
        self.__data["Tasks"].append(t1)
        self.__data["Tasks"].append(t2)


dayPlanner = DayPlanner()
# dayPlanner.shell_del_task()
# print(sys.argv[1])
