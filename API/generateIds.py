"""
This is temporary script for adding uniq ids into each Task data
"""

import  json
import uuid
import os

DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), 'data.json')

def generate_ids(collection):

    def generate_id(item):
        while True:
            newId = str(uuid.uuid1())
            existring_ids = [i["uuid"] for i in collection if "uuid" in i]
            if newId in existring_ids:
                continue
            else:
                return newId

    for item in collection:
        if "uuid" in item:
            pass
        else:
            item["uuid"] = generate_id(item)

    return collection




def readJSON():
    with open(DATA_FILE_NAME, "r") as read_file:
        return json.load(read_file)

nonobjectdata = readJSON()
[print(task) for task in nonobjectdata["Tasks"]]

nonobjectdata["Tasks"] =  generate_ids(nonobjectdata["Tasks"])


def updateJSON():
    jsondata = {
        "Tasks": [task for task in nonobjectdata["Tasks"]],
        "Phones": []
    }
    with open(DATA_FILE_NAME, "w") as write_file:
        json.dump(jsondata, write_file, indent=4)

# updateJSON()