import json

MSG_TYPE_DATA = 0x00 #Data Transfer
MSG_TYPE_ACK = 0x01
MSG_TYPE_DATA_ACK = MSG_TYPE_DATA | MSG_TYPE_ACK
MSG_TYPE_FILE = 0x02  #File Transfer (Download)
MSG_TYPE_DIR_LIST = 0x04  #List Directory
MSG_TYPE_RENAME = 0x08 #Rename
MSG_TYPE_DELETE = 0x10 #Delete
MSG_TYPE_ERROR = 0x20  #Error

class Datagram:
    def __init__(self, mtype: int, msg: str, sz: int = 0, filename: str = ''):
        self.mtype = mtype
        self.msg = msg
        self.sz = len(self.msg)
        self.filename = filename

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        return Datagram(**json.loads(json_str))

    def to_bytes(self):
        if self.mtype == MSG_TYPE_FILE:
            header = json.dumps({'mtype': self.mtype, 'filename': self.filename, 'sz': self.sz}).encode('utf-8')
            return header + b'\0' + self.msg.encode('utf-8')
        else:
            return json.dumps(self.__dict__).encode('utf-8')

    @staticmethod
    def from_bytes(json_bytes):
        if b'\0' in json_bytes:
            parts = json_bytes.split(b'\0', 1)
            header = json.loads(parts[0].decode('utf-8'))
            if 'filename' in header:
                msg = parts[1].decode('utf-8') if len(parts) > 1 else ''
                return Datagram(header['mtype'], msg, header['sz'], header['filename'])
            else:
                msg = parts[1].decode('utf-8') if len(parts) > 1 else ''
                return Datagram(header['mtype'], msg, header['sz'])
        else:
            header = json.loads(json_bytes.decode('utf-8'))
            return Datagram(**header)
