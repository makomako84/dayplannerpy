from typing import Dict
import typing


class Phone:
    uuid: str
    phone: str
    name: str

    def __init__(self, uuid: str, phone: str, name: str):
        self.uuid = uuid
        self.phone = phone
        self.name = name
    
    @staticmethod
    def decodeJSON(jsondata: typing.Dict[str, str, str]):
        return Phone(uuid=jsondata["uuid"], phone=jsondata["phone"], name=jsondata["name"])

    def encodeJSON(self):
        return {
            "uuid":self.uuid,
            "phone":self.phone,
            "name":self.name
        }
    
    def __eq__(self,other):
        assert isinstance(other, Phone), "other is not instance of Phone"
        return self.uuid == other.uuid
    
    def __ne__(self,other):
        if other == None: return True
        assert isinstance(other, Phone), "other is not instance of Phone"
        return self.uuid != other.uuid

    def __str__(self):
        return  self.name