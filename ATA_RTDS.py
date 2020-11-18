from time import sleep
import ConRTDS

class ata_rtds(self,RTDS_IP,RTDS_PORT):



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
        self.logmsg("NoteMsg", "Sending RTDS command: {}".format(command))
        rtds = get_RTDS_instance(self)
        if not rtds:
            self.logmsg("FailMsg", "No connection to RTDS, failed to send command:{}"
                        .format(command))
        else:
            rtds.sendRawCommand(command)


    def press_button(self, btn_name, subsystem=1):
        """
        Press RTDS button
        @param btn_name: Str: Name of RTDS button to be pressed
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'PushButton "Subsystem #{} : CTLs : Inputs : {}";'.format(
            subsystem, btn_name)
        send_command(self, command)


    def release_button(self, btn_name, subsystem=1):
        """
        Press RTDS button
        @param btn_name: Str: Name of RTDS button to be pressed
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'ReleaseButton "Subsystem #{} : CTLs : Inputs : {}";'.format(
            subsystem, btn_name)
        send_command(self, command)


    def set_on_switch(self, sw_name, subsystem=1):
        """
        Set on switch
        @param sw_name: Str: name of a switch to be set in RTDS
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'SetSwitch "Subsystem #{} : CTLs : Inputs : {}" = 1;'.format(
            subsystem, sw_name)
        send_command(self, command)


    def set_off_switch(self, sw_name, subsystem=1):
        """
        Set off switch
        @param sw_name: Str: name of a switch to be set in RTDS
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'SetSwitch "Subsystem #{} : CTLs : Inputs : {}" = 0;'.format(
            subsystem, sw_name)
        send_command(self, command)


    def set_slider(self, slider_name, value, subsystem):
        """
        Set slider to @value position
        @param slider_name: Str: name of a slider to be set in RTDS
        @param value: Int/Float: value to be set to a slider
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'SetSlider "Subsystem #{} : CTLs : Inputs : {}" = {};'.format(
            subsystem, slider_name, value)
        send_command(self, command)


    def set_dial(self, dial_name, value, subsystem=1):
        """
        Set dial control to @value position
        @param dial_name: Str: name of a slider to be set in RTDS
        @param value: Int/Float: value to be set to a slider
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'SetDial "Subsystem #{} : CTLs : Inputs : {}" = {};'.format(
            subsystem, dial_name, value)
        send_command(self, command)


    def unlock_plot(self, plot_name):
        """
        Unlock named plot for recording
        @param plot_name: Str: name of a plot to be unlocked in RTDS
        """
        self.logmsg('NoteMsg', 'RTDS: Unlock plot {}'.format(plot_name))
        command = 'PlotChangeLockState "{}" = 0;'.format(plot_name)
        send_command(self, command)


    def lock_plot(self, plot_name):
        """
        Lock named plot and exclude it from recording
        @param plot_name: Str: name of a plot to be unlocked in RTDS
        """
        self.logmsg('NoteMsg', 'RTDS: Lock plot {}'.format(plot_name))
        command = 'PlotChangeLockState "{}" = 1;'.format(plot_name)
        send_command(self, command)


    def set_plot_seconds(self, finish_time, plot_precision, pre_trigger):
        """
        Set plots update parameters.
        @param finish_time: Int: Duration of update plots i.e. duration of all
        unlocked plots recording time in seconds
        @param plot_precision: Precision of plots recording points:[1, 2, 4, 8,
         16, 32, 64, 128] and custom.
        @param pre_trigger: Some trigger to write point, TBD
        """
        self.logmsg('NoteMsg', 'RTDS: Set plots update parameters: Finish time={}s,\
        Precision={}points, Pre Trigger={}%'.format(
            finish_time, plot_precision, pre_trigger))
        command = 'SetPlotSeconds {},{},{};'.format(finish_time, plot_precision, pre_trigger)
        send_command(self, command)


    def update_plots(self):
        """
        Update all unlocked plots
        """
        self.logmsg('NoteMsg', 'RTDS: Update plots')
        command = 'UpdatePlots;'
        send_command(self, command)


    def save_plot_comtrade(self, plot_name, save_path, year=1991,
                           min_point=0, max_point=65535):
        """
        Save plot as comtrade file
        @param plot_name: Str:  Plot name to be stored as comtrade files
        @param save_path: Str:  Path to save comtrade files
        @param year: Int: Year standart, 1991 or 1999
        @param min_point: Int: Min point of data from what to start a file
        @param max_point: Int: Max point of data to what ends a file
        """
        self.logmsg('NoteMsg', 'RTDS: Save plot {} as comtrade file to {}'
                    .format(plot_name, save_path))
        if year not in [1991, 1999]:
            year = 1991
        command = 'ComtradePlotSave "{0}","{1}\{0}.cfg",YEAR,{},MIN,{},MAX,{};'.format(
            plot_name, save_path, year, min_point, max_point)
        send_command(self, command)


    def save_plot_jpeg(self, plot_name, save_path, compression=75, units='inches'):
        """
        Save plot as comtrade file
        @param plot_name: Str:  Plot name to be stored as comtrade files
        @param save_path: Str:  Path to save comtrade files
        @param compress: Int: Level of jpeg compression 0..100%
        @param units: Str: The units in which height and width are given.
               Can be inches, px, cm or mm
        """
        self.logmsg('NoteMsg', 'RTDS: Save plot {} as jpeg file to {}'
                    .format(plot_name, save_path))
        command = 'SavePlotToJpeg "{0}","{1}\{0}.jpg", COMPRESSION,{}, UNITS,{};'.format(
            plot_name, save_path, compression, units)
        send_command(self, command)


    # ----------------- PROJECT SPECIFIC FUNCTIONS ---------------------

    def ctrl_MCBA(self, command):
        '''
        Control master circuit breaker of SA
        '''
        self.logmsg('NoteMsg', 'RTDS: {} MCCA'.format(command))
        if command is 'Close':
            press_button(self, "CMCBP1A", subsystem=2)
            release_button(self, "CMCBP1A", subsystem=2)
        elif command is 'Open':
            press_button(self, "OMCBP1A", subsystem=2)
            release_button(self, "OMCBP1A", subsystem=2)
        else:
            self.logmsg('NoteMsg', 'RTDS: Wrong command {} for MCCA'
                        .format(command))


    def ctrl_MCBB(self, command):
        '''
        Control master circuit breaker of SB
        '''
        self.logmsg('NoteMsg', 'RTDS: {} MCCB'.format(command))
        if command is 'Close':
            press_button(self, "CMCBP1B", subsystem=2)
            release_button(self, "CMCBP1B", subsystem=2)
        elif command is 'Open':
            press_button(self, "OMCBP1B", subsystem=2)
            release_button(self, "OMCBP1B", subsystem=2)
        else:
            self.logmsg('NoteMsg', 'RTDS: Wrong command {} for MCCA'
                        .format(command))


    def ctrl_TAPMODE1A(self, manual=True):
        """
        Control tap changer mode of SA Pole1
        @param manual: Bool: Tap changer in manual mode, otherwise in auto mode
        """
        if manual:
            self.logmsg('NoteMsg', 'RTDS: Set TAPMODE1A to Manual mode')
            set_on_switch(self, "TAPMODE1A", subsystem=2)
        else:
            self.logmsg('NoteMsg', 'RTDS: Set TAPMODE1A to Auto mode')
            set_off_switch(self, "TAPMODE1A", subsystem=2)


    def ctrl_TAPMODE1B(self, manual=True):
        """
        Control tap changer mode of SB Pole1
        @param manual: Bool: Tap changer in manual mode, otherwise in auto mode
        """
        if manual:
            self.logmsg('NoteMsg', 'RTDS: Set TAPMODE1B to Manual mode')
            set_on_switch(self, "TAPMODE1B", subsystem=2)
        else:
            self.logmsg('NoteMsg', 'RTDS: Set TAPMODE1B to Auto mode')
            set_off_switch(self, "TAPMODE1B", subsystem=2)


    def tap_up_1A(self, tap_change_delay=6):
        """
        Send tap up command by pressing TAPUP1A button of RTDS
        @param tap_change_delay: Delay in seconds after sending tap up command,
        if no delay quick commands are not accepted by RTDS
        """
        self.logmsg('NoteMsg', 'RTDS: Tap-up TAPUP1A')
        press_button(self, "TAPUP1A", subsystem=2)
        sleep(0.5)
        release_button(self, "TAPUP1A", subsystem=2)
        sleep(tap_change_delay)


    def tap_down_1A(self, tap_change_delay=6):
        """
        Send tap down command by pressing TAPDN1A button of RTDS
        @param tap_change_delay: Delay in seconds after sending tap up command,
        if no delay quick commands are not accepted by RTDS

        """
        self.logmsg('NoteMsg', 'RTDS: Tap-down TAPUP1A')
        press_button(self, "TAPDN1A", subsystem=2)
        sleep(0.5)
        release_button(self, "TAPDN1A", subsystem=2)
        sleep(tap_change_delay)


    def tap_up_1B(self, tap_change_delay=6):
        """
        Send tap up command by pressing TAPUP1B button of RTDS
        """
        self.logmsg('NoteMsg', 'RTDS: Tap-up TAPUP1B')
        press_button(self, "TAPUP1B", subsystem=2)
        sleep(0.5)
        release_button(self, "TAPUP1B", subsystem=2)
        sleep(tap_change_delay)


    def tap_down_1B(self, tap_change_delay=6):
        """
        Send tap down command by pressing TAPDN1B button of RTDS
        """
        self.logmsg('NoteMsg', 'RTDS: Tap-down TAPDN1B')
        press_button(self, "TAPDN1B", subsystem=2)
        sleep(0.5)
        release_button(self, "TAPDN1B", subsystem=2)
        sleep(tap_change_delay)


    def set_SA_AC_voltage(self, ac_voltage):
        """
        Set AC voltage slider for SA
        @param ac_voltage: Float: Relative AC voltage in PU. 1.0PU=315kV
        """
        self.logmsg('NoteMsg', 'RTDS: Set AC voltage for SA to {}pu'
                    .format(ac_voltage))
        set_slider(self, "SAAdjust", ac_voltage, subsystem=1)


    def set_SB_AC_voltage(self, ac_voltage):
        """
        Set AC voltage slider for SB
        @param ac_voltage: Float: Relative AC voltage in PU. 1.0PU=315kV
        """
        self.logmsg('NoteMsg', 'RTDS: Set AC voltage for SB to {}pu'
                    .format(ac_voltage))
        set_slider(self, "SBAdjust", ac_voltage, subsystem=2)


    def set_Slider_List(self, RTDS_Slider_List, Test_Values, subsys):
        """
        Set a list of slider with a list of predifined values.
        @RTDS_silder
        """
        for i in range(0, len(RTDS_Slider_List)):
            set_slider(self, RTDS_Slider_List[i], Test_Values[i], subsys[i])


    def set_SB_Slider_List(self, RTDS_Slider_List, Test_Values):
        """
        Set a list of slider with a list of predifined values.
        @RTDS_silder
        """
        for i in range(0, len(RTDS_Slider_List)):
            set_slider(self, RTDS_Slider_List[i], Test_Values[i], subsystem=2)


    def set_Slider_Listv2(self, RTDS_Slider_List, Test_Values):
        """
        Set a list of slider with a list of predifined values.
        @RTDS_silder
        """
        # Customise test values
        t_values = Test_Values[0:len(RTDS_Slider_List)]
        for i in range(0, len(RTDS_Slider_List)):
            set_slider(self, RTDS_Slider_List[i][0], t_values[i], subsystem=1)