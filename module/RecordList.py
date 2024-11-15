import uuid

from module.Record import Record

class RecordList:
    def __init__(self):
        self.list = {}

    def add(self, record: Record):
        # 创建记录的唯一标识符
        uid = str(uuid.uuid1())
        self.list[uid] = record
        return uid
    
    def findByUid(self, uid: str) -> Record:
        record = self.list.get(uid)
        return record
    
    def removeById(self, uid: str):
        return self.list.pop(uid)
    
    def length(self):
        return len(self.list)
    
    def __iter__(self):
        return iter(self.list.values())
    
    def __str__(self):
        s = ''
        for uid in self.list:
            s += "UID('" + uid + "'): " + self.list[uid].__str__() + "\n"
        return s