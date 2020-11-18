import RESTsession

class settingpanels(RESTsession.s5openconnection):
    def __init__(self,side, lane, pole):
        side1 = "SA"
        pole1 = "P1"
        if side =="SideB": side1 = "SB"
        if pole == "Pole2": pole1 = "P2"

        self.cabinet = side1 + lane + pole1 + "CCP4"
        print(self.cabinet)
        super().__init__(self.cabinet)

        self.side = side
        self.pole = pole

    def setInput29(self):
        path = "/P0237/" + self.side + "/"+ self.pole + "/Cc/GlobalInterfaces/Cc-SysI/Cib3/Comms/In/Input29"
        type = "int"
        value = "2"
        super().setValue(path,type,value)

    def IOtestMode(self):
        pathcc =  "/P0237/" +self.side+ "/" +self.pole+ "/Cc/GlobalInterfaces/Cc-SysI/Cib2/Test/setPntIOTest"
        pathcp1 = "/P0237/" +self.side+ "/" +self.pole+ "/Cp1/GlobalInterfaces/Cp-SysI/Cib2/Test/setPntIOTest"
        pathcp2 = "/P0237/" +self.side+ "/" +self.pole+ "/Cp2/GlobalInterfaces/Cp-SysI/Cib2/Test/setPntIOTest"
        type = "bool"
        value = "True"
        super().setValue(pathcc,type,value)
        super().setValue(pathcp1,type,value)
        super().setValue(pathcp2, type, value)

    def setBShealthy(self):
        cp1path3 = "/P0237/" + self.side + "/" + self.pole + "/Cp1/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO3Out"
        cp1path4 = "/P0237/" + self.side + "/" + self.pole + "/Cp1/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO4Out"
        cp1path5 = "/P0237/" + self.side + "/" + self.pole + "/Cp1/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO5Out"
        cp1path7 = "/P0237/" + self.side + "/" + self.pole + "/Cp1/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO7Out"
        ##
        path3 = "/P0237/" + self.side + "/" + self.pole + "/Cp2/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO3Out"
        path4 = "/P0237/" + self.side + "/" + self.pole + "/Cp2/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO4Out"
        path5 = "/P0237/" + self.side + "/" + self.pole + "/Cp2/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO5Out"
        path7 = "/P0237/" + self.side + "/" + self.pole + "/Cp2/GlobalInterfaces/Cp-SysI/Cib2/GPIO/setPntGPIO7Out"
        type = "Bool"
        value = "True"
        super().setValue(path3,type,value)
        super().setValue(path4, type, value)
        super().setValue(path5, type, value)
        super().setValue(path7, type, value)
        super().setValue(cp1path3, type, value)
        super().setValue(cp1path4, type, value)
        super().setValue(cp1path5, type, value)
        super().setValue(cp1path7, type, value)
    def Laneavailable(self):
        lpath = "/P0237/" +self.side+ "/" + "pole" + "/Cc/GlobalInterfaces/Cc-SysI/Cib2/GPIO/setPntGPIO7Out"
        type = "bool"
        value = "TRUE"
        super().setValue(lpath,type,value)
    def Laneunavailable(self):
        lpath = "/P0237/" + self.side + "/" + "pole" + "/Cc/GlobalInterfaces/Cc-SysI/Cib2/GPIO/setPntGPIO7Out"
        type = "bool"
        value = "False"
        super().setValue(lpath, type, value)
    def Deblock(self):
        bpath = "/P0237/" +self.side+ "/" +self.pole+ "/Cc/Software/PhC/BitFields/setPntBitField2"
        type = "int"
        value = "801"
    def Block(self):
        bpath = "/P0237/" +self.side+ "/" +self.pole+ "/Cc/Software/PhC/BitFields/setPntBitField2"
        type = "int"
        value = "0"
def main():
    panel = settingpanels("SideA","L1","Pole1")
    print(panel.cabinet)
    panel.IOtestMode()
    panel.setInput29()
    panel.setBShealthy()
    panel.Laneavailable()
    while(1):
        


if __name__ == "__main__":
    main()





