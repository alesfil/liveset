# -*- coding: utf-8 -*-

import wx
import json
import os
import time
import usb.core, usb.util
from liveset.livesetconf import *

import subprocess

class SettingsWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Configuration")

        panel = wx.Panel(self)

        midiInPortText = wx.StaticText(panel, label="MIDI In Port")
        self.midiInPortComboBox = wx.ComboBox(panel)
        self.midiInPortComboBox.SetItems(self.midiPorts('in'))

        midiOutPortText = wx.StaticText(panel, label="MIDI Out Port")
        self.midiOutPortComboBox = wx.ComboBox(panel)
        self.midiOutPortComboBox.SetItems(self.midiPorts('out'))

        nextSceneCCText = wx.StaticText(panel, label="Switch Scene MIDI CC")
        nextSubsceneCCText = wx.StaticText(panel, label="Switch Subscene MIDI CC")
        nextSubsceneUSBStaticBox = wx.StaticBox(panel, label="Switch Subscene USB Switch")

        idVendorUSBText = wx.StaticText(panel, label="USB Switch idVendor")
        idProductUSBText = wx.StaticText(panel, label="USB Switch idProduct")
        dataIndexUSBText = wx.StaticText(panel, label="USB Switch data index")
        dataValueUSBText = wx.StaticText(panel, label="USB Switch data Value")
        self.idVendorUSBTextCtrl = wx.TextCtrl(panel)
        self.idProductUSBTextCtrl = wx.TextCtrl(panel)
        self.dataIndexUSBTextCtrl = wx.TextCtrl(panel)
        self.dataValueUSBTextCtrl = wx.TextCtrl(panel)   
        self.idVendorUSBTextCtrl.Disable()
        self.idProductUSBTextCtrl.Disable()
        self.dataIndexUSBTextCtrl.Disable()
        self.dataValueUSBTextCtrl.Disable()
        self.nextSceneCCSpinCtrl = wx.SpinCtrl(panel, value ='0')
        self.nextSceneCCSpinCtrl.SetRange(0, 127)
        self.nextSubsceneCCSpinCtrl = wx.SpinCtrl(panel, value ='0')
        self.nextSubsceneCCSpinCtrl.SetRange(0, 127)

        findButton = wx.Button(panel, label='Find USB device')
        learnButton = wx.Button(panel, label='USB switch learn')
        applyButton = wx.Button(panel, wx.ID_APPLY)
        closeButton = wx.Button(panel, wx.ID_CLOSE)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        hbox8 = wx.BoxSizer(wx.HORIZONTAL)
        hbox9 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(midiInPortText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox1.Add(self.midiInPortComboBox, 1,  wx.EXPAND |wx.ALL, 5)
        hbox2.Add(midiOutPortText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox2.Add(self.midiOutPortComboBox, 1,  wx.EXPAND |wx.ALL, 5)
        hbox3.Add(nextSceneCCText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox3.Add(self.nextSceneCCSpinCtrl, 1, wx.EXPAND |wx.ALL, 5)
        hbox4.Add(nextSubsceneCCText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox4.Add(self.nextSubsceneCCSpinCtrl, 1, wx.EXPAND |wx.ALL, 5)

        hbox5.Add(idVendorUSBText, 1, wx.EXPAND |wx.ALL, 5)
        hbox5.Add(self.idVendorUSBTextCtrl, 1, wx.EXPAND |wx.ALL, 5)
        hbox6.Add(idProductUSBText, 1,wx.EXPAND | wx.ALL, 5)
        hbox6.Add(self.idProductUSBTextCtrl, 1, wx.EXPAND |wx.ALL, 5)
        hbox7.Add(dataIndexUSBText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox7.Add(self.dataIndexUSBTextCtrl, 1,  wx.EXPAND |wx.ALL, 5)
        hbox8.Add(dataValueUSBText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox8.Add(self.dataValueUSBTextCtrl, 1,  wx.EXPAND |wx.ALL, 5)
        hbox9.Add(findButton, 1, wx.EXPAND |wx.ALL, 5) 
        hbox9.Add(learnButton, 1, wx.EXPAND |wx.ALL, 5)         

        staticBoxSizer = wx.StaticBoxSizer(nextSubsceneUSBStaticBox, wx.VERTICAL)
        staticBoxSizer.Add(hbox5, 0, wx.EXPAND |wx.ALL, 5) 
        staticBoxSizer.Add(hbox6, 0, wx.EXPAND |wx.ALL, 5)
        staticBoxSizer.Add(hbox7, 0, wx.EXPAND | wx.ALL, 5)
        staticBoxSizer.Add(hbox8, 0, wx.EXPAND |wx.ALL, 5)
        staticBoxSizer.Add(hbox9, 0, wx.EXPAND | wx.ALL, 5) 

        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        hbox10.Add(applyButton, 1, wx.EXPAND | wx.ALL , 10)
        hbox10.Add(closeButton, 1, wx.EXPAND | wx.ALL , 10)   

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, 0, wx.EXPAND |wx.ALL, 5) 
        vbox.Add(hbox2, 0, wx.EXPAND |wx.ALL, 5)
        vbox.Add(hbox3, 0, wx.EXPAND |wx.ALL, 5)
        vbox.Add(hbox4, 0, wx.EXPAND |wx.ALL, 5)    
        vbox.Add(staticBoxSizer, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox10, 0, wx.EXPAND | wx.ALL, 5)


        findButton.Bind(wx.EVT_BUTTON, self.OnFindButton)
        learnButton.Bind(wx.EVT_BUTTON, self.OnLearnButton)
        applyButton.Bind(wx.EVT_BUTTON, self.OnApplyButton)
        closeButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)

        self.Init()
        panel.SetSizer(vbox)
	sizer = wx.BoxSizer(wx.HORIZONTAL)
    	sizer.Add(panel)
    	self.SetSizerAndFit(sizer)


    def midiPorts(self, inout):
        ## MIDI out ports (alsa sequencer)
        if inout == 'in':
            string = subprocess.check_output(['aconnect', '-i'])
        if inout == 'out':
            string = subprocess.check_output(['aconnect', '-o'])

        string = string.split('\n')

        ports = []
        for index, line in enumerate(string):
            if 'client' in line:
                client = line.split("'")[1::2]
                for i in range(index+1, len(string)-1):
                    if not ('client' in string[i]):
                        port = string[i].split("'")[1::2]
                        ports.append(client[0].strip()+':'+port[0].strip())
                    else:
                        break
        return ports
            

    def Init(self):
        try:
            with open(settings_file) as data_file:
                self.options = json.load(data_file)
        except:
            self.options = {"midiInPort":"",
                "midiOutPort":"",
                "nextSceneCC":0,
                "nextSubsceneCC":0,
                "idVendor":"",
                "idProduct":"",
                "dataIndexUSB":"",
                "dataValueUSB":""}

        self.midiInPortComboBox.SetValue(self.options["midiInPort"])  
        self.midiOutPortComboBox.SetValue(self.options["midiOutPort"])
        self.nextSceneCCSpinCtrl.SetValue(self.options["nextSceneCC"])
        self.nextSubsceneCCSpinCtrl.SetValue(self.options["nextSubsceneCC"])
        self.idVendorUSBTextCtrl.SetValue(self.options["idVendor"])
        self.idProductUSBTextCtrl.SetValue(self.options["idProduct"])
        self.dataIndexUSBTextCtrl.SetValue(self.options["dataIndexUSB"])
        self.dataValueUSBTextCtrl.SetValue(self.options["dataValueUSB"])                           

    def OnFindButton(self, event):
        string = "Unplug or leave unplugged the usb device and click OK"
        dialog1 = wx.MessageDialog(self, string, 'Step 1', wx.OK)
        dialog1.ShowModal()
        dialog1.Destroy()

        time.sleep(0.5)
        dev = usb.core.find(find_all=True)
        listA = []  
        for cfg in dev:
            listA.append((hex(cfg.idVendor), hex(cfg.idProduct)))
        string = "Plug the usb device and click OK"
        dialog2 = wx.MessageDialog(self, string, 'Step 2', wx.OK)
        dialog2.ShowModal()
        dialog2.Destroy()

        time.sleep(0.5)        
        dev = usb.core.find(find_all=True)        
        listB = []
        for cfg in dev:
            listB.append((hex(cfg.idVendor), hex(cfg.idProduct)))
        devicelist = list(set(listB) - set(listA))

        if len(devicelist) == 1:
            device = devicelist[0]
            ## int( str, 16) converts from string to hexadecimal
            idVendor = int(device[0], 16)
            idProduct = int(device[1], 16)
            dev = usb.core.find(idVendor = idVendor, idProduct = idProduct )
            if dev is None:
                self.DeviceNotFound()
            string = 'Device found:\n'+ device[0] +' ' + device[1]
            dialog3 =  wx.MessageDialog(self, string, 'Step 3', wx.OK)
            dialog3.ShowModal()
            dialog3.Destroy()
            self.idVendorUSBTextCtrl.SetValue(device[0])
            self.idProductUSBTextCtrl.SetValue(device[1])
        else:
            self.DeviceNotFound()
            self.idVendorUSBTextCtrl.SetValue('')
            self.idProductUSBTextCtrl.SetValue('')

    def DeviceNotFound(self):
        string = 'Device not found'
        dialog =  wx.MessageDialog(self, string, 'ERROR', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()   

    def OnLearnButton(self, event):
        idVendor = int(self.idVendorUSBTextCtrl.GetValue(), 16)
        idProduct = int(self.idProductUSBTextCtrl.GetValue(), 16)       
        dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        if dev is None:
            self.DeviceNotFound() 
        else:
            string = "Click OK and then press the USB switch"
            dialog1 = wx.MessageDialog(self, string, 'Learn', wx.OK)
            dialog1.ShowModal()
            dialog1.Destroy() 

            # first endpoint
            interface = 0
            endpoint = dev[0][(0,0)][0]
            if dev.is_kernel_driver_active(interface) is True:
                dev.detach_kernel_driver(interface)
                usb.util.claim_interface(dev, interface)
            i = 0
            data1 = None
            data2 = None

            while i < 2 :
                time.sleep(0.3)
                try:
                    data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
                    if data1 == None:
                        data1 = data
                        i += 1
                    else:
                        data2 = data
                        i += 1
                except usb.core.USBError as e:
                    data = None
                    if e.args == ('Operation timed out',):
                        continue
            usb.util.release_interface(dev, interface)
            dev.attach_kernel_driver(interface)

            valuelist = list(set(data1)-set(data2))                
            value = valuelist[0]
            for x, y in enumerate(data1):
                if value == y:
                    index = x
            string = 'USB switch configured\n'+\
                     'USB data index: '+ str(index) +'\n'+\
                     'USB data value: '+ str(value)
            dialog2 = wx.MessageDialog(self, string, 'Learn', wx.OK) 
            dialog2.ShowModal()
            dialog2.Destroy()
            self.dataIndexUSBTextCtrl.SetValue(str(index))
            self.dataValueUSBTextCtrl.SetValue(str(value))            

    def OnApplyButton(self, event):
        self.options["midiInPort"] = self.midiInPortComboBox.GetValue() 
        self.options["midiOutPort"] = self.midiOutPortComboBox.GetValue()
        self.options["nextSceneCC"] = self.nextSceneCCSpinCtrl.GetValue()        
        self.options["nextSubsceneCC"] = self.nextSubsceneCCSpinCtrl.GetValue()
        self.options["idVendor"] = self.idVendorUSBTextCtrl.GetValue()
        self.options["idProduct"] = self.idProductUSBTextCtrl.GetValue()
        self.options["dataIndexUSB"] = self.dataIndexUSBTextCtrl.GetValue()
        self.options["dataValueUSB"] = self.dataValueUSBTextCtrl.GetValue()

  
        with open(settings_file, 'w') as outFile:
            json.dump(self.options, outFile, sort_keys = True, indent = 4, ensure_ascii = False)


    def OnCloseButton(self, event):
        self.Close(True)
                 