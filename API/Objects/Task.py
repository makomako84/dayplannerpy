from API.Utils.timeutils import  deserialize_datetime, serialize_datetime


class Task:

    def __init__(self, uuid,name,done, datetime, *, description=None):
        self.uuid = uuid
        self.name = name
        self.done = done
        self.datetime = datetime
        self.description = description
    @staticmethod
    def decodeJSON(jsondata):
        newTask = Task(uuid=jsondata["uuid"],name=jsondata["name"], done=jsondata["done"], datetime=deserialize_datetime(jsondata["date"]))
        if "description" in jsondata:
            newTask.description = jsondata["description"]
        return newTask

    def encodeJSON(self):
        return {
            "uuid":self.uuid,
            "name":self.name,
            "description": self.description,
            "done": self.done,
            "date": serialize_datetime(self.datetime)
        }

    def __eq__(self, other):
        assert isinstance(other, Task), "other is not instance of Task"
        return  self.uuid == other.uuid

    def __ne__(self, other):
        assert isinstance(other, Task), "other is not instance of Task"
        return self.uuid != other.uuid

    def __str__(self):
        return f"{self.uuid}, {self.name}, {self.done}, {self.description}, {self.datetime}"

