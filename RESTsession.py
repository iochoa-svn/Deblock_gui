
import requests
import time


NUM_RETRIES = 3
RETRY_DELAY = 3

class s5openconnection:

    def __init__(self, ipaddress):
        print("You are just starting a connection to series 5, ip {}".format(ipaddress))
        self.ipaddress = ipaddress
        self.rqsession = requests.Session()
        self.checking = "not match"


    def getValueDic(self, ipaddress, s5path):
        """get value through REST API
        Reads a value through the REST api
        @param s5path: relative path of the value.
                       the root will be guessed from the session's ip
        @return: a tuple containing: t: type of the value
                                     v: the value itself
                                     s: time of the value in seconds
                                     m: milliseconds
        """

        reqstr = "http://" + ipaddress + "/Logger/json?Class=0&Path=" + s5path
        couldread = False
        try:
            r = self.rqsession.get(reqstr)
            print("REST Response:<{}>".format(r.content))  ###

            retrycount = NUM_RETRIES
            while retrycount > 0:
                if (r.content == b'{\r\n\"events\": [\r\n]}\r\n'):
                    # self.testInstance.Pause(RETRY_DELAY)
                    time.sleep(RETRY_DELAY)
                    r = self.rqsession.get(reqstr)
                    retrycount = retrycount - 1
                else:
                    retrycount = 0
            if (r.content == b'{\r\n\"events\": [\r\n]}\r\n'):
                raise Exception("Empty response after " + str(NUM_RETRIES) + " retries")
            else:
                couldread = True
        except Exception as err:
            msg = ": Failed to read {} ({})".format(reqstr, err)
            print(time.ctime() + msg)
            print(time.ctime() + ": Failed to read %s (%s)" % (reqstr, err))


        else:

            resp = r.json()
            t = resp['events'][0]['type']
            v = resp['events'][0]['value']
            s = resp['events'][0]['seconds']
            m = resp['events'][0]['ms']
            return (t, v, s, m)

    def setValueDic(self,s5path,s5type,s5value,mons5path=None):
        print(s5type)

        reqstr = "http://" + self.ipaddress + "/Logger/Command?Path=" + s5path + "&Type=" + s5type + "&value=" + s5value
        rr=self.rqsession.get(reqstr)
        print(self.ipaddress)
        print(rr.url)

        try:
            mon_value = self.getValue(mons5path)
            print("monId retrived value",mon_value[1])
            print(s5value)
            time.sleep(RETRY_DELAY)
            retrycount = NUM_RETRIES
            while retrycount > 0:
                if s5value=="False":
                    s5value_tr = '0'
                else :
                    s5value_tr = '1'
                if (mon_value[1] == s5value_tr):
                    print("after if ", s5value_tr)
                    self.checking = "match"
                    retrycount = retrycount -1
                else:
                    retrycount = 0

        except Exception as err:
            msg = ": Failed to write {} ({})".format(reqstr, err)
            print(time.ctime() + msg)
            print(time.ctime() + ": Failed to read %s (%s)" % (reqstr, err))
        else:

            return self.checking

    def setValue(self,s5path,s5type,s5value): # main method to set value
        setresult = self.setValueDic(s5path,s5type,s5value)
        return setresult



    def getValue(self, s5path): # main method to GET value
        t, v, s, m = self.getValueDic(self.ipaddress, s5path)
        return ([t, v])

    def getValueAndTime(self, s5path):
        t, v, s, m = self.getValueDic(self, s5path)
        time = int(s) + (int(m) / 1000)
        return ([v, time])

#
def main():
    openip = s5openconnection('SAL1P1CCP4')
    rvalue = openip.getValue("/P0237/SideA/Pole1/Cc/GlobalInterfaces/Cc-SysI/Cib2/Test/monIdIOTest")
    print(rvalue)


    set_path = "/P0237/SideA/Pole1/Cc/GlobalInterfaces/Cc-SysI/Cib2/Test/setPntIOTest"
    set_type = "bool"
    set_value="false"
    set_mon = "/P0237/SideA/Pole1/Cc/GlobalInterfaces/Cc-SysI/Cib2/Test/monIdIOTest"
    svalue = openip.setValue(set_path,set_type,set_value)
    print(svalue)


if __name__ == "__main__":
    main()
