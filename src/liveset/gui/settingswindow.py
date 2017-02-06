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

        self.nextSceneCCSpinCtrl = wx.SpinCtrl(panel, value ='0')
        self.nextSceneCCSpinCtrl.SetRange(0, 127)
        self.nextSubsceneCCSpinCtrl = wx.SpinCtrl(panel, value ='0')
        self.nextSubsceneCCSpinCtrl.SetRange(0, 127)

        applyButton = wx.Button(panel, wx.ID_APPLY)
        closeButton = wx.Button(panel, wx.ID_CLOSE)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(midiInPortText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox1.Add(self.midiInPortComboBox, 1,  wx.EXPAND |wx.ALL, 5)
        hbox2.Add(midiOutPortText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox2.Add(self.midiOutPortComboBox, 1,  wx.EXPAND |wx.ALL, 5)
        hbox3.Add(nextSceneCCText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox3.Add(self.nextSceneCCSpinCtrl, 1, wx.EXPAND |wx.ALL, 5)
        hbox4.Add(nextSubsceneCCText, 1,  wx.EXPAND |wx.ALL, 5)
        hbox4.Add(self.nextSubsceneCCSpinCtrl, 1, wx.EXPAND |wx.ALL, 5)       


        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(applyButton, 1, wx.EXPAND | wx.ALL , 10)
        hbox5.Add(closeButton, 1, wx.EXPAND | wx.ALL , 10)   

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, 0, wx.EXPAND |wx.ALL, 5) 
        vbox.Add(hbox2, 0, wx.EXPAND |wx.ALL, 5)
        vbox.Add(hbox3, 0, wx.EXPAND |wx.ALL, 5)
        vbox.Add(hbox4, 0, wx.EXPAND |wx.ALL, 5)    
        vbox.Add(hbox5, 0, wx.EXPAND | wx.ALL, 5)

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
                "nextSubsceneCC":0}

        self.midiInPortComboBox.SetValue(self.options["midiInPort"])  
        self.midiOutPortComboBox.SetValue(self.options["midiOutPort"])
        self.nextSceneCCSpinCtrl.SetValue(self.options["nextSceneCC"])
        self.nextSubsceneCCSpinCtrl.SetValue(self.options["nextSubsceneCC"])                         

        

    def OnApplyButton(self, event):
        self.options["midiInPort"] = self.midiInPortComboBox.GetValue() 
        self.options["midiOutPort"] = self.midiOutPortComboBox.GetValue()
        self.options["nextSceneCC"] = self.nextSceneCCSpinCtrl.GetValue()        
        self.options["nextSubsceneCC"] = self.nextSubsceneCCSpinCtrl.GetValue()
  
        with open(settings_file, 'w') as outFile:
            json.dump(self.options, outFile, sort_keys = True, indent = 4, ensure_ascii = False)


    def OnCloseButton(self, event):
        self.Close(True)
                 