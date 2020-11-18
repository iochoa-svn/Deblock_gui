
import time
import re
import socket
import queue as Queue
import _thread as thread
class TCIPCommandChannel:
    def __init__(self,RTDS_IP,RTDS_PORT):
        self.RTDS_IP=RTDS_IP

        self.RTDS_PORT=int(RTDS_PORT)
        print ("%s: ip:%s port:%d"%(time.ctime(),self.RTDS_IP,self.RTDS_PORT))
        self._socket=None
        self.index=0
        self.max_retries = 4
        try:
            #create an AF_INET, STREAM socket (TCP)
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._waitQueue = Queue.Queue()
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 0)
            self.sockTimeout = None
        except socket.error as msg:
            log_msg = "%s: Failed to create socket." \
                   " Error code:%s Error message :%s" \
                   %(time.ctime(),str(msg[0]),msg[1])
            print(log_msg)

            return
        self._socket.connect((self.RTDS_IP,self.RTDS_PORT))

    def get_RTDS_instance(self):
        '''
        Get RTDS instance object
        @param self: object of TestSteps
        '''
        return self.RTDS

    def send_command(self, command):
        """Send raw RTDS command
        @param command: Str: Command to be sent to RTDS
        """
        print("NoteMsg", "Sending RTDS command: {}".format(command))
        rtds = self.get_RTDS_instance(self)
        if not rtds:
            print("FailMsg", "No connection to RTDS, failed to send command:{}"
                        .format(command))
        else:
            self.sendRawCommand(command)



    def set_slider(self, slider_name, value, subsystem):
        """
        Set slider to @value position
        @param slider_name: Str: name of a slider to be set in RTDS
        @param value: Int/Float: value to be set to a slider
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'SetSlider "Subsystem #{} : CTLs : Inputs : {}" = {};'.format(
            subsystem, slider_name, value)
        self.send_command(self, command)

    def set_dial(self, dial_name, value, subsystem=1):
        """
        Set dial control to @value position
        @param dial_name: Str: name of a slider to be set in RTDS
        @param value: Int/Float: value to be set to a slider
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'SetDial "Subsystem #{} : CTLs : Inputs : {}" = {};'.format(
            subsystem, dial_name, value)
        self.send_command(self, command)



   
   

    def set_Slider_List(self, RTDS_Slider_List, Test_Values, subsys):
        """
        Set a list of slider with a list of predifined values.
        @RTDS_silder
        """
        for i in range(0, len(RTDS_Slider_List)):
            self.set_slider(self, RTDS_Slider_List[i], Test_Values[i], subsys[i])

    def set_SB_Slider_List(self, RTDS_Slider_List, Test_Values):
        """
        Set a list of slider with a list of predifined values.
        @RTDS_silder
        """
        for i in range(0, len(RTDS_Slider_List)):
            self.set_slider(self, RTDS_Slider_List[i], Test_Values[i], subsystem=2)

    def set_Slider_Listv2(self, RTDS_Slider_List, Test_Values):
        """
        Set a list of slider with a list of predifined values.
        @RTDS_silder
        """
        # Customise test values
        t_values = Test_Values[0:len(RTDS_Slider_List)]
        for i in range(0, len(RTDS_Slider_List)):
            self.set_slider(self, RTDS_Slider_List[i][0], t_values[i], subsystem=1)
    def sendRawCommand(self,Command, blocking=True):
        if not self._dummySession:
            self.sendTCP(Command, blocking)

    def sendTCP(self, Command, blocking=True):
        # print(Command)
        if not hasattr(self, '_channel'):
           print("WARNING: RTDS not connected, command ignored:'" \
                + Command + "'")
            return
        if not self._dummySession:
            self._channel.Send(Command, blocking)


def openConnection(self):
    """open connection
    @return: None
    """
    self.logger.println("%s: Opening socket on ip:%s port:%s" \
                        % (time.ctime(), self.RTDS_IP, self.RTDS_PORT))  # TODO: print
    self.logger.info("Opening socket on ip:{} port:{}".format(self.RTDS_IP,
                                                              self.RTDS_PORT))
    # In dummy session create RTDS channel only if REAL_RTDS_IN_DUMMY is set to True
    createChannel = False
    if self._dummySession:
        try:
            rtdsdummy = self.params["REAL_RTDS_IN_DUMMY"]
            if rtdsdummy.lower() == "true":
                createChannel = True
        except Exception as err:
            self.logger.info("Define and set Key REAL_RTDS_IN_DUMMY to \
                   TRUE in configuration to create RTDS channel in DUMMY mode")
    else:
        createChannel = True
    if createChannel:
        self._channel = TCIPCommandChannel(self.RTDS_IP, self.RTDS_PORT)