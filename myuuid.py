import uuid
import os

class Uuid(object):

    def __init__(self):
        self._path = './json/.uuid'
        self._file_uuid = ""
        self._pc_uuid = ""

    def write_pc_uuid_to_file(self):
        with open(self._path, 'w') as f:
            f.write(self._pc_uuid)

    def get_file_uuid(self):
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                mac = f.read()
                if len(mac) < 3:
                    self.get_pc_uuid()
                    self.write_pc_uuid_to_file()
                    return self._pc_uuid
                else:
                    return mac
        else:
            self.get_pc_uuid()
            self.write_pc_uuid_to_file()
            return self._pc_uuid

    def get_pc_uuid(self):
        self._pc_uuid = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return self._pc_uuid


def authour():
    u =Uuid()
    file_uuid = u.get_file_uuid()
    pc_uuid = u.get_pc_uuid()

    if file_uuid == pc_uuid:
        return True
    else:
        return False

if __name__ == "__main__":
    print(authour())

