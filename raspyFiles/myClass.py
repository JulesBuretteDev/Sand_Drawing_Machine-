
class Value:

    def __init__(self,name:str,id:int,val:str):
        self.name = name
        self.id = id
        self.val = val

    def __str__(self) -> str:
        return f"{self.name}: {self.val} : id : {self.id}\n"

class Values:

    def __init__(self,values : list[Value] = []) -> None:
        self.values = values

    def addVal(self, values):
        self.values.append(values)

    def __str__(self) -> str:
        res = ""
        for val in self.values:
            res += val.__str__()
        return f"{res}"

class Arduino:
    def __init__(self,port, baud_rate:int = 9600) -> None:
        self.com_port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.com_port, self.baud_rate, timeout = 1)


    def find_port(self):
        ports = ['/dev/ttyACM{}'.format(i) for i in range(1, 10)]
        for port in ports:
            try:
                arduino = serial.Serial(port, 9600, timeout=1)
                arduino.close()
                return port
            except:
                pass
        print("did not find any available port")
        return None
    
    def __str__(self) -> str:
        return f"port: {self.com_port}"
