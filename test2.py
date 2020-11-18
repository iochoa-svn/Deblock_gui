
import requests
import time


NUM_RETRIES = 5
RETRY_DELAY = 1

class s5openconnection:

    def _init__(self,ipaddress):
        print("You are just starting a connection to series 5, ip {}".format(ipaddress))
        self.ipaddress = ipaddress
        self.rqsession = requests.Session()


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
        couldRead = False
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
                couldRead = True
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


    def getValue(self,s5path):
        t, v, s, m = self.getValueDic(s5path)
        return (v)


    def getValueAndTime(self, s5path):
        t, v, s, m = self.getValueDic(s5path)
        time = int(s) + (int(m) / 1000)
        return (v, time)

openip = s5openconnection('UKL1CCP1')



openip.getValue(path)