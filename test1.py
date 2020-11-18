import requests

NUM_RETRIES =10

RETRY_DELAY = 1.1

class session:

    def __init__(self,ip):
        self.ip = ip
        self.rsession = requests.Session()

    def setValue(self,s5path,s5type,s5value):
        reqstr = "http://" + self.ip + "/Logger/Command?Path=" + s5path + "&Type=" + s5type + "&value=" + str(s5value)
        r = self.rsession.put(reqstr)

    def getValue(self,s5path):
        reqstr = "http://" + self.ip + "/Logger/json?Class=0&Path=" + s5path
        r = self.rsession.get(reqstr)