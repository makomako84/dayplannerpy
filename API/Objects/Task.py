from API.Utils.timeutils import  deserializeDate, serializeDate
from  datetime import  datetime


class Task:
    name = None
    date = None
    description = None
    done = False

    def __init__(self, name,done, date):
        self.name = name
        self.done = done
        self.date = date
    @staticmethod
    def decodeJSON(jsondata):
        newTask = Task(name=jsondata["name"], done=jsondata["done"], date=deserializeDate(jsondata["date"]))
        newTask.description = jsondata["description"]
        return newTask

    def encodeJSON(self):
        return {
            "name":self.name,
            "description": self.description,
            "done": self.done,
            "date": serializeDate(self.date)
        }

    def __str__(self):
        return f"{self.name}, {self.done}, {self.description}, {self.date}"

