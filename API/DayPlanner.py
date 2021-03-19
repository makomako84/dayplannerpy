import  sys
import  json
import  pprint
import  os
from typing import List
import uuid
from datetime import  datetime
from datetime import  date
from API.Objects.Task import Task


#py path
DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), 'data.json')

#build path
# DATA_FILE_NAME = os.path.join(os.path.dirname(sys.executable), 'data.json')


class DayPlanner:


    __data = {
        "Tasks": [],
        "Phones": []
    }

    def __init__(self):
        # self.test_create_tasks()
        # self.__initObjectData()
        # print("init object data")
        # nonlocal  DATA_FILE_NAME
        # DATA_FILE_NAME = os.path.join(os.path.dirname(sys.executable), 'data.json')
        print(sys.executable)
        self.__initObjectData()
        # self.updateJSON()
        # self.shell_main_menu()

    def __initObjectData(self):
        # print(DATA_FILE_NAME)
        nonobjectdata = self.readJSON()
        tasks = []
        for task in nonobjectdata["Tasks"]:
            tasks.append(Task.decodeJSON(task))
        self.__data["Tasks"] = tasks


    # tasks functions
    def get_tasks(self):
        return [task.__str__() for task in self.__data["Tasks"]]
        
    def get_tasks_filtered_by_date(self, date) -> List[Task]:
        return list(filter((lambda x: x.datetime.date() == date),self.__data["Tasks"]))

    def add_new_task(self,dict):
        dict["uuid"] = str(uuid.uuid1())
        self.__data["Tasks"].append(Task.decodeJSON(dict))
        self.updateJSON()
    def save_task(self, task:Task):
        if task in self.__data["Tasks"]:
            self.__data["Tasks"][self.__data["Tasks"].index(task)] = task
            self.updateJSON()
            print("There is such task")
        else:
            self.__data["Tasks"].append(task)
            self.updateJSON()

    def get_temp_task(self, dt:datetime):
        return  Task(str(uuid.uuid1()),"",False, dt)

    def find_task_by_uuid_str(self, uuidvalue:str) -> Task:
        searchfunc = lambda x: x.uuid.find(uuidvalue)!=-1
        return list(filter(searchfunc, self.__data["Tasks"]))[0]
    def find_task_by_name(self, searchvalue:str):
        searchfunc = lambda x: x.name.find(searchvalue) != -1
        return list(filter(searchfunc, self.__data["Tasks"]))

    def delete_task_byuuid(self, uuid:str):
        self.__data["Tasks"].remove(self.find_task_by_uuid_str(uuid))
        self.updateJSON()

    def delete_task(self, foundtask: Task):
        self.__data["Tasks"].remove(foundtask)
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
        self.updateJSON()
