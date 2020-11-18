#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
 @copyright: (c) ALSTOM Grid a GE Company / Power Electronic Systems Stafford.
 This File and any Information or Descriptive Matter set out herein are the
 Confidential and Copyright Property of ALSTOM Power Electronic Systems
 and must not be Disclosed, Loaned, Copied or Used for
 Manufacturing, Tendering or for any other purpose without their written
 permission.

 @note:   Automatically Generated Test Script
 @author: Ismael Ochoa GE-PES
 @since:  11-09-2017, code prepared for FIL porject
-------------------------------------------------------------------------------
"""

import RTDS_functionsv3
import Proj_Settings
import time
import sqlite3
import RESTsession as rts
from collections import OrderedDict


class TestClass(rts):



    def __init__(self, ip, parent=None):
        super(TestClass, self).__init__(self, parent, ip)

        # Get sesssion to Side A
        self.session_SA = self.rqsession
        #self.session_SB = self.getSession('B')

        self.date_now = time.strftime("%Y-%m-%d-%H-%M-%S")

    def verify_TABLE(self, Side, Pole, Rack, CIB, Path, sess_t, tol, *Test_vector_selected, **MonID_group):
        # MonID_group = OrderedDict(MonID_group)
        Apex_value = [0] * len(MonID_group)

        j = 0
        Slider_label = []
        Apex_data_point = []
        SLD_signal_name = []
        for k, v in MonID_group.items():
            print('NoteMsg', k)
            Apex_path = Path + str(k)
            Slider_label.append(v[1])
            Apex_data_point.append(v[0])
            SLD_signal_name.append(v[2])
            # print('NoteMsg',Apex_path)
            # print('NoteMsg',sess_t)

            Apex_value[j] = float(sess_t.getValue(Apex_path))

            j += 1

        # Report.generate_report(self,tol,*Apex_value,*Test_vector_selected, **MonID_group
        col_width = 17
        col_width2 = 11
        col_width3 = 6
        File_name = "C:\\Users\\212536861\\Desktop\\Alstom_grid\\testScripts_FIL\\TestScripts2019\\{}.txt".format(
            str(self.date_now))
        # next lin eis for lab only
        # File_name = "C:\\Users\\lg760442sd\\Desktop\\Alstom_grid\\ATE\\testScripts_FIL_ReplicaMBS\\TestCases\\HARDWARE_INTEGRATION\\{}.txt".format(str(self.date_now))
        File_r = open(File_name, "a+")
        File_r.write("**********************\n")
        # File_r.write("Test----{}---{}--{}-------------\n".format(path,CP,CIB))
        File_r.write(
            '*******Testing : ' + 'Side: ' + Side + '/' + ' Pole(Link):' + Pole + '/' + ' Rack : ' + Rack + ' / ' + 'CIB :' + str(
                CIB) + '---\n')
        File_r.write("**********************\n")
        File_r.close()

        File_r = open(File_name, "a+")
        l1 = 'Value in | {} | {} | {} | {} | {} | {} | {} |'.format('RTDS slider'.ljust(len('RTDS slider')),
                                                                    'Apex data point'.ljust(len('Apex data point')),
                                                                    'SLD Signal Name'.ljust(len('SLD Signal Name') + 3),
                                                                    'Testing Value (TV)'.ljust(
                                                                        len('Testing Value (TV)')),
                                                                    'Reading Apex value(RV)'.ljust(
                                                                        len('Reading Apex value(RV)')),
                                                                    'P/F '.ljust(len('P/F')),
                                                                    'error% (TV-RV)/TV%'.ljust(
                                                                        len('error% (TV-RV)/TV%')))
        File_r.write(l1 + "\n")
        print('NoteMsg', l1)
        l2 = 'Value in | {} | {} | {} | {} | {} | {} | {} |'.format('---------'.ljust(len('RTDS slider')),
                                                                    '---------'.ljust(len('Apex data point')),
                                                                    '---------'.ljust(len('SLD Signal Name') + 3),
                                                                    '-----------'.ljust(len('Testing Value [TV]')),
                                                                    '-----------'.ljust(len('Reading Apex value[RV]')),
                                                                    '----'.ljust(len('P/F')),
                                                                    '----'.ljust(len('error% (TV-RV)/TV%')))
        File_r.write(l2 + "\n")
        print('NoteMsg', l2)
        for m in range(0, len(Apex_value)):
            # compare values
            a = abs(Test_vector_selected[m])
            b = abs(Apex_value[m])
            e = (a - b) / a * 100

            if (abs(a) + tol * abs(a)) >= abs(b) >= (abs(a) - tol * abs(a)):
                STATUS = "PASS"

            else:
                STATUS = "FAIL"

            e = round(e, 4)
            l3 = 'Value in | {} | {} | {} | {} | {} | {} | {} |' \
                .format(str(Slider_label[m]).ljust(len('RTDS slider')),
                        Apex_data_point[m].ljust(len('Apex data point')),
                        str(SLD_signal_name[m]).ljust(len('SLD Signal Name') + 3),
                        str(Test_vector_selected[m]).ljust(len('Testing Value [TV]')),
                        str(Apex_value[m]).ljust(len('Reading Apex value[RV]')),
                        STATUS.ljust(len('P/F')),
                        str(e).ljust(len('error% (TV-RV)/TV%')))
            File_r.write(l3 + "\n")
            print('NoteMsg', l3)

            # File_r.close()

    def get_RTDS_instance(self):

        # Get RTDS instance object
        # @param self: object of TestSteps

        return RTDS

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
            rtds.sendRawCommand(command)

    def set_slider(self, slider_name, value, subsystem):
        """
        Set slider to @value position
        @param slider_name: Str: name of a slider to be set in RTDS
        @param value: Int/Float: value to be set to a slider
        @param subsystem: Int: Subsystem of RTDS
        """
        command = 'SetSlider "Subsystem #{} : CTLs : Inputs : {}" = {};'.format(
            subsystem, slider_name, value)
        self.send_command(command)

    def set_Slider_List(self, RTDS_Slider_List, Test_Values, subsys):
        """
        Set a list of slider with a list of predifined values.
        @RTDS_silder
        """
        for i in range(0, len(RTDS_Slider_List)):
            self.set_slider(RTDS_Slider_List[i], Test_Values[i], subsys[i])

    def readDB(self, DBtable, CIBn, Side):
        # Change this path
        # conn = sqlite3.connect('C:\\Users\\212536861\\Desktop\\Alstom_grid\\testScripts_LCP\\site-packages\\LCP_SIGNALSV7.db')
        # next lije is for lab only
        # conn = sqlite3.connect('C:\\Users\\lg760442sd\\Desktop\\Alstom_grid\\ATE\\testScripts_FIL_ReplicaMBS\\TestCases\\HARDWARE_INTEGRATION\\FIL_V2.db')

        conn = sqlite3.connect(
            'C:\\Users\\212536861\\Desktop\\Alstom_grid\\testScripts_FIL\\TestScripts2019\\FIL_V2.db')

        # conn = sqlite3.connect('C:\\Users\\lg760442sd\\Documents\\LCP_SIGNALSV7.db')
        cur = conn.cursor()
        comm = 'SELECT SLIDER_TABLE.SIGNAL_LONG_NAME,SLIDER_TABLE.GTA,SLIDER_TABLE.CHANNEL\
        ,{r}.CIB,{r}.ADC,{r}.IO_LABEL,{r}.SUBSYSTEM FROM SLIDER_TABLE JOIN {r} ON SLIDER_TABLE.SLIDER_ID \
        = {r}.SLIDER_ID WHERE {r}.CIB={n}'.format(r=DBtable, n=CIBn)
        cur.execute(comm)
        cc_a = cur.fetchall()
        monID_group = {}
        Test_slider = []
        Test_monId = []
        Test_signal_name = []
        Test_ADC = []
        Subsystem_Vector = []
        for t in cc_a:
            if Side == 'A':
                GTA = "GA{:>01}".format(t[1])
            elif Side == 'B':
                GTA = "GB{:>01}".format(t[1])
            CHANNEL = "CH{:>02}".format(t[2])
            ADC = "{:>02}".format(t[4])
            SUBSYSTEM = t[6]
            if GTA == "G00":
                continue
            else:
                slider = GTA + CHANNEL
                monId = "monIdADC" + ADC
                signal_name = t[0]
                # print(" {} : {} : {} : {} ".format(slider, monId, signal_name.ljust(20), ADC))

            # Test_slider.append(slider)
            # Test_monId.append(monId)
            # Test_signal_name.append(signal_name)
            # Test_ADC.append(ADC)
            # Subsystem_Vector.append(SUBSYSTEM)
            monID_group[monId] = monId, slider, signal_name, None, SUBSYSTEM

        conn.close()

        return monID_group

    def TestVectors(self, length, option):
        if option == 0:
            Test_Vector = [0] * length

        elif option == 1:
            Test_Vector = [1] * length

        elif option == 2:
            Test_Vector = [5] * length
        elif option == 3:
            Test_Vector = [10] * length
        elif option == 4:
            Test_Vector = [-1] * length
        elif option == 5:
            Test_Vector = [-5] * length
        elif option == 6:
            Test_Vector = [-10] * length
        elif option == 7:
            Master_TF1 = []
            for i in range(0, 16):
                t = round(1 + 0.1 * i, 1)
                Master_TF1.append(t)
            Test_Vector = Master_TF1
        elif option == 8:
            Master_TF1 = []
            for i in range(0, 16):
                t = round(1 + 0.1 * i, 1)
                Master_TF1.append(t)

            Master_TF1N = [i * (-1) for i in Master_TF1]
            Test_Vector = Master_TF1N
        return Test_Vector

    def setAllSlider2Zero(self, Side):
        g = range(1, 6)
        c = range(1, 13)
        all_sld = []
        for n in g:
            GTA = "G{}{:>01}".format(Side, n)
            for t in c:
                CHANNEL = "CH{:>02}".format(t)
                sld = GTA + CHANNEL
                all_sld.append(sld)
        sub1 = [1] * len(all_sld)
        # sub2 =[2]*len(all_sld)
        Test_Vector = self.TestVectors(len(all_sld), 0)
        RTDS_functionsv3.set_Slider_List(self, all_sld, Test_Vector, sub1)
        # RTDS_functionsv3.set_Slider_List(self,all_sld, Test_Vector,sub2)

    def TestSubRack(self, Side, Pole, Rack, CIB, Test_Case, wating_time, tolerance):

        Test_slider_label = []

        Path = self.Path_Selector(Side, Pole, Rack, CIB)  # Path selector
        DBtable = Proj_Settings.DBtable(self, Side, Pole, Rack)  # Table from DB

        MonID_group = self.readDB(DBtable, CIB, Side)
        # monID_group [monId][x] :  (monId, slider, signal_name, Value)
        vec_len = len(MonID_group)
        for key, value in MonID_group.items():
            Test_slider_label.append(value[1])

        Test_Vector_selected = self.TestVectors(vec_len, Test_Case)
        sub1 = [1] * len(Test_Vector_selected)
        RTDS_functionsv3.set_Slider_List(self, Test_slider_label, Test_Vector_selected, sub1)
        time.sleep(wating_time)
        # -----Apex---
        if Side == 'A':
            session_side = self.session_SA
        elif Side == 'B':
            session_side = self.session_SB

        print('NoteMsg', '**********************************************************************')
        print('NoteMsg',
                    '*******Testing : ' + 'Side: ' + Side + '/' + ' Pole(Link):' + Pole + '/' + ' Rack : ' + Rack + '*******')
        print('NoteMsg', '**********************************************************************')
        self.verify_TABLE(Side, Pole, Rack, CIB, Path, session_side, tolerance, *Test_Vector_selected, **MonID_group)
        print('NoteMsg', '**********************************************************************')

    def Path_Selector(self, Side, Pole, Rack, CIB):

        SA_Path, SB_Path = Proj_Settings.setPaths(self)

        if Side == 'A':
            if Rack == 'C':
                path = SA_Path['SA_C'][0]
                print(path)
                if int(CIB) == 2:
                    path = SA_Path['SA_C'][1]

                elif int(CIB) == 3:
                    path = SA_Path['SA_C'][2]
            elif Rack == 'M1':
                path = SA_Path['SA_M1'][0]
                if int(CIB) == 2:
                    path = SA_Path['SA_M1'][1]
                elif int(CIB) == 3:
                    path = SA_Path['SA_M1'][2]
            elif Rack == 'M2':
                path = SA_Path['SA_M2'][0]
                if int(CIB) == 2:
                    path = SA_Path['SA_M2'][1]
                elif int(CIB) == 3:
                    path = SA_Path['SA_M2'][2]
        elif Side == 'B':
            if Rack == 'C':
                path = SB_Path['SB_C'][0]
                print(path)
                if int(CIB) == 2:
                    path = SB_Path['SB_C'][1]

                elif int(CIB) == 3:
                    path = SB_Path['SB_C'][2]
            elif Rack == 'M1':
                path = SB_Path['SB_M1'][0]
                if int(CIB) == 2:
                    path = SB_Path['SB_M1'][1]
                elif int(CIB) == 3:
                    path = SB_Path['SB_M1'][2]
            elif Rack == 'M2':
                path = SB_Path['SB_M2'][0]
                if int(CIB) == 2:
                    path = SB_Path['SB_M2'][1]
                elif int(CIB) == 3:
                    path = SB_Path['SB_M2'][2]
        return path

def testFunction(hostname,side,pole,RackType,CIB):
    # Close MCBs
    mysession = TestClass(hostname)

    wating_time = 8
    tolerance = 0.01

    # ---Resetting to 0 RTDS------#
    mysession.setAllSlider2Zero('A')
    #self.setAllSlider2Zero('B')
    time.sleep(wating_time)
    # ---WHat is going to be tested----
    '''
    # Enter:
    TestSubRack(Side,Pole/Link, Subrack, Subsystem, Test_case, waiting time, tolerance)
    Side : 'A' or 'B'
    Pole/Link : 'P1'
    SubRack = 'C' 'M1 or 'M2'
    '''
    mysession.TestSubRack(side, pole, RackType, CIB, 7, wating_time, tolerance)

testFunction('UKL1CCP1','A','P1','C',1)
testFunction('ASL1CCP1','B','P1','C',1)

    # mysession.TestSubRack('A','P1','C', 2,7,wating_time,tolerance)
    # mysession.TestSubRack('A','P1','C', 3,7,wating_time,tolerance)
    # mysession.TestSubRack('A','P1','M1', 1,7,wating_time,tolerance)
    # mysession.TestSubRack('A','P1','M1', 2,7,wating_time,tolerance)
    # mysession.TestSubRack('A','P1','M1', 3,7,wating_time,tolerance)
    # mysession.TestSubRack('A','P1','M2', 1,7,wating_time,tolerance)
    # mysession.TestSubRack('A','P1','M2', 2,7,wating_time,tolerance)
    # mysession.TestSubRack('A','P1','M2', 3,7,wating_time,tolerance)
    # #
    #mysession.TestSubRack('B', 'P1', 'C', 1, 7, wating_time, tolerance)
    # mysession.TestSubRack('B','P1','C', 2,7,wating_time,tolerance)
    # mysession.TestSubRack('B','P1','M1', 1,7,wating_time,tolerance)
    # mysession.TestSubRack('B','P1','M1', 2,7,wating_time,tolerance)
    # mysession.TestSubRack('B','P1','M1', 3,7,wating_time,tolerance)
    # mysession.TestSubRack('B','P1','C', 3,7,wating_time,tolerance)
    # mysession.TestSubRack('B','P1','M2', 1,7,wating_time,tolerance)
    # mysession.TestSubRack('B','P1','M2', 2,7,wating_time,tolerance)
    # mysession.TestSubRack('B','P1','M2', 3,7,wating_time,tolerance)



