from API.Utils.timeutils import  deserializeDate, serializeDate


class Task:

    def __init__(self, name,done, datetime, *, description=None):
        self.name = name
        self.done = done
        self.datetime = datetime
        self.description = description
    @staticmethod
    def decodeJSON(jsondata):
        newTask = Task(name=jsondata["name"], done=jsondata["done"], datetime=deserializeDate(jsondata["date"]))
        if "description" in jsondata:
            newTask.description = jsondata["description"]
        return newTask

    def encodeJSON(self):
        return {
            "name":self.name,
            "description": self.description,
            "done": self.done,
            "date": serializeDate(self.datetime)
        }

    def __eq__(self, other):
        assert isinstance(other, Task), "other is not instance of Task"
        return  self.name == other.name

    def __ne__(self, other):
        assert isinstance(other, Task), "other is not instance of Task"
        return self.name != other.name

    def __str__(self):
        return f"{self.name}, {self.done}, {self.description}, {self.datetime}"

