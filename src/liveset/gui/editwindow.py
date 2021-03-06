# -*- coding: utf-8 -*-

import wx

import mididings.util

noteList = []
for i in range(0, 128):
    noteList.append(mididings.util.note_name(i))

class Subscene():
    def InitPart(self):
        part = {}
        part["InCH"] = 1
        part["CH"] = 1
        part["PC"] = 1
        part["CC0"] = 0
        part["CC32"] = 0
        part["Lower"] = 0
        part["Upper"] = 127
        return part

    def InitSubscene(self):
        part = self.InitPart()
        subscene = [part]
        return subscene

class EditWindow(wx.Frame):
    def __init__(self, parent, data, sceneText):
        wx.Frame.__init__(self, None, title=sceneText)

        panel = wx.Panel(self)

        self.data = data
        self.sceneText = sceneText

       
        ## TextCtrls

        self.subsceneTextCtrl = wx.TextCtrl(panel)      

        ## Buttons

        newSubsceneButton = wx.Button(panel, label='New Subscene')
        delSubsceneButton = wx.Button(panel, label='Del Subscene')
        closeButton = wx.Button(panel, label='Close')

        ## Subscenes list box

        self.subscenesListbox = wx.ListBox(panel, -1)

        ## zone (parts) number
        self.zones = 4

        self.partsCheckBox = []
        self.MidiInChSpinCtrls = []
        self.MidiChSpinCtrls = []
        self.PCSpinCtrls = []
        self.Bank00SpinCtrls = []
        self.Bank32SpinCtrls = []
        self.LowerKeyComboBox = []
        self.UpperKeyComboBox = []


        for i in range(0, self.zones):
            self.partsCheckBox.append( \
                wx.CheckBox(panel, label="Part "+str(i+1)+":", style = wx.ALIGN_RIGHT))

            self.MidiInChSpinCtrls.append(wx.SpinCtrl(panel, value =str(i+1)))
            self.MidiInChSpinCtrls[i].SetRange(1, 16)
	    textSize = self.MidiInChSpinCtrls[i].GetTextExtent("999")
            textWidth = textSize[0]
            spinCtrlWidth = textWidth*2.5  # empiric value
            self.MidiInChSpinCtrls[i].SetMinSize((spinCtrlWidth, -1)) # -1 default


            self.MidiChSpinCtrls.append(wx.SpinCtrl(panel, value =str(i+1)))
            self.MidiChSpinCtrls[i].SetRange(1, 16)
            self.MidiChSpinCtrls[i].SetMinSize((spinCtrlWidth, -1))

            self.PCSpinCtrls.append(wx.SpinCtrl(panel, value ='0'))
            self.PCSpinCtrls[i].SetRange(1, 128)
            self.PCSpinCtrls[i].SetMinSize((spinCtrlWidth, -1))

            self.Bank00SpinCtrls.append(wx.SpinCtrl(panel, value ='0'))
            self.Bank00SpinCtrls[i].SetRange(0, 127)
            self.Bank00SpinCtrls[i].SetMinSize((spinCtrlWidth, -1))

            self.Bank32SpinCtrls.append(wx.SpinCtrl(panel, value ='0'))
            self.Bank32SpinCtrls[i].SetRange(0, 127)
            self.Bank32SpinCtrls[i].SetMinSize((spinCtrlWidth, -1))

            self.LowerKeyComboBox.append(wx.ComboBox(panel, choices=noteList, style=wx.CB_READONLY))

            self.UpperKeyComboBox.append(wx.ComboBox(panel, choices=noteList, style=wx.CB_READONLY))


        PartText = wx.StaticText(panel, label="Part")
        MidiInChText = wx.StaticText(panel, label="MIDI In CH")        
        MidiChText = wx.StaticText(panel, label="MIDI Out CH")
        PCText = wx.StaticText(panel, label="Program Change")
        Bank00Text = wx.StaticText(panel, label="Bank 00")
        Bank32Text = wx.StaticText(panel, label="Bank 32")
        LowerKeyText = wx.StaticText(panel, label="Lower Key")
        UpperKeyText = wx.StaticText(panel, label="Upper Key")

        grid = wx.FlexGridSizer(8, self.zones+1, 2, 2)
        grid.AddGrowableCol(0, 2)
        for i in range(1, self.zones+1):
            grid.AddGrowableCol(i, 1)

        grid.Add(PartText, 1, wx.EXPAND)
        for i in range(0, self.zones):     
            grid.Add(self.partsCheckBox[i], 0)
        grid.Add(MidiInChText, 1, wx.EXPAND)
        for i in range(0, self.zones):
            grid.Add(self.MidiInChSpinCtrls[i], 1, wx.EXPAND)
        grid.Add(MidiChText, 1, wx.EXPAND)
        for i in range(0, self.zones):
            grid.Add(self.MidiChSpinCtrls[i], 1, wx.EXPAND)
        grid.Add(PCText, 1, wx.EXPAND)
        for i in range(0, self.zones):
            grid.Add(self.PCSpinCtrls[i], 1, wx.EXPAND)
        grid.Add(Bank00Text, 1, wx.EXPAND)
        for i in range(0, self.zones):
            grid.Add(self.Bank00SpinCtrls[i], 1, wx.EXPAND)
        grid.Add(Bank32Text, 1, wx.EXPAND)
        for i in range(0, self.zones):
            grid.Add(self.Bank32SpinCtrls[i], 1, wx.EXPAND)
        grid.Add(LowerKeyText, 1, wx.EXPAND)
        for i in range(0, self.zones):
            grid.Add(self.LowerKeyComboBox[i], 1, wx.EXPAND)
        grid.Add(UpperKeyText, 1, wx.EXPAND)
        for i in range(0, self.zones):
            grid.Add(self.UpperKeyComboBox[i], 1, wx.EXPAND)


        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(newSubsceneButton, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(delSubsceneButton, 1, wx.EXPAND | wx.ALL, 5)

        staticBox2 = wx.StaticBox(panel, label='Subscenes')
        vbox2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)
        vbox2.Add(hbox2, 0, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.subsceneTextCtrl, 0, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.subscenesListbox, 1, wx.EXPAND | wx.ALL, 5)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(grid, 0,  wx.EXPAND | wx.ALL, 1)
        vbox3.Add(closeButton, 0, wx.ALL | wx.CENTER, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vbox2, 1,  wx.EXPAND | wx.ALL, 5)
        hbox.Add(vbox3, 1,  wx.EXPAND | wx.ALL, 5)

        ## Binding

        newSubsceneButton.Bind(wx.EVT_BUTTON, self.OnNewSubsceneButton)
        delSubsceneButton.Bind(wx.EVT_BUTTON, self.OnDelSubsceneButton)  
        self.subsceneTextCtrl.Bind(wx.EVT_TEXT, self.OnEditSubscene)
        self.subscenesListbox.Bind(wx.EVT_LISTBOX, self.OnSelectSubscene)
        closeButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)

        for part in range(0, self.zones):
            self.partsCheckBox[part].Bind(\
               wx.EVT_CHECKBOX, lambda evt, temp=part: self.OnSelectPart(evt, temp))
            self.MidiInChSpinCtrls[part].Bind(\
               wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnMidiInSpinCtrl(evt, temp))
            self.MidiChSpinCtrls[part].Bind(\
               wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnMidiSpinCtrl(evt, temp))
            self.PCSpinCtrls[part].Bind(\
               wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnPCSpinCtrl(evt, temp))
            self.Bank00SpinCtrls[part].Bind(\
               wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnBank00SpinCtrl(evt, temp))
            self.LowerKeyComboBox[part].Bind(\
               wx.EVT_COMBOBOX, lambda evt, temp=part: self.OnLowerKeyComboBox(evt, temp))
            self.UpperKeyComboBox[part].Bind(\
               wx.EVT_COMBOBOX, lambda evt, temp=part: self.OnUpperKeyComboBox(evt, temp))
   
        panel.SetSizer(hbox)
	sizer = wx.BoxSizer(wx.HORIZONTAL)
    	sizer.Add(panel, 1, wx.EXPAND)
    	self.SetSizerAndFit(sizer)

        self.OnLoad()


    def OnLoad(self):
        self.subscenesListbox.Clear()

        for subsceneSel in self.data.scenes[self.sceneText]:
            for subsceneText in subsceneSel:
                self.subscenesListbox.Append(subsceneText)

        self.subscenesListbox.Select(0)
        self.OnSelectSubscene(wx.EVT_LISTBOX)


    def OnEditSubscene(self, event):      
        subsceneSel = self.subscenesListbox.GetSelection()
        oldText = self.subscenesListbox.GetString(subsceneSel)
        newText = self.subsceneTextCtrl.GetValue()

        self.subscenesListbox.SetString(subsceneSel, newText)

        if oldText != newText:
            self.data.scenes[self.sceneText][subsceneSel][newText] = self.data.scenes[self.sceneText][subsceneSel][oldText]
            del self.data.scenes[self.sceneText][subsceneSel][oldText]


    def OnNewSubsceneButton(self, event):
        subsceneText = "--"
        subscene = Subscene()
        self.data.scenes[self.sceneText].append({subsceneText : subscene.InitSubscene()})  
        self.subscenesListbox.Append(subsceneText)
        subsceneCount = self.subscenesListbox.GetCount()
        self.subscenesListbox.Select(subsceneCount-1)
        self.OnSelectSubscene(wx.EVT_LISTBOX)


    def OnDelSubsceneButton(self, event):
        subsceneSel = self.subscenesListbox.GetSelection()
        subsceneText = self.subscenesListbox.GetString(subsceneSel)

        if subsceneSel != -1:
            self.subscenesListbox.Delete(subsceneSel)
            del self.data.scenes[self.sceneText][subsceneSel]
            try:
                self.subscenesListbox.Select(subsceneSel)
            except:
                self.subscenesListbox.Select(subsceneSel-1)
            self.OnSelectSubscene(wx.EVT_LISTBOX)  


    def OnSelectSubscene(self, event):
        subsceneSel = self.subscenesListbox.GetSelection()
        subsceneText = self.subscenesListbox.GetString(subsceneSel)

        self.subsceneTextCtrl.ChangeValue(subsceneText) 

        subscene = self.data.scenes[self.sceneText][subsceneSel][subsceneText]
        for part in range(0, len(subscene)):        
                self.partsCheckBox[part].SetValue(True)
                self.EnablePart(part) 
                self.MidiInChSpinCtrls[part].SetValue(subscene[part]['InCH'])
                self.MidiChSpinCtrls[part].SetValue(subscene[part]['CH'])
                self.PCSpinCtrls[part].SetValue(subscene[part]['PC'])
                self.Bank00SpinCtrls[part].SetValue(subscene[part]['CC0'])
                self.Bank32SpinCtrls[part].SetValue(subscene[part]['CC32'])
                lowerNote = noteList[subscene[part]['Lower']]
                self.LowerKeyComboBox[part].SetValue(lowerNote)
                upperNote = noteList[subscene[part]['Upper']]
                self.UpperKeyComboBox[part].SetValue(upperNote)

        for part in range(len(subscene), self.zones):
                self.partsCheckBox[part].SetValue(False)
                self.DisablePart(part)

        ## REMINDER: the following point to self.data.scenes...
        self.selectedSubscene = subscene

    def OnMidiInSpinCtrl(self, event, part):
        sender = event.GetEventObject()
        ## This is a pointer to self.data.scenes...
        self.selectedSubscene[part]['InCH'] = sender.GetValue()

    def OnMidiSpinCtrl(self, event, part):
        sender = event.GetEventObject()
        ## This is a pointer to self.data.scenes...
        self.selectedSubscene[part]['CH'] = sender.GetValue()

    def OnPCSpinCtrl(self, event, part):
        sender = event.GetEventObject()
        self.selectedSubscene[part]['PC'] = sender.GetValue()

    def OnBank00SpinCtrl(self, event, part):
        sender = event.GetEventObject()
        self.selectedSubscene[part]['CC0'] = sender.GetValue()

    def OnBank32SpinCtrl(self, event, part):
        sender = event.GetEventObject()
        self.selectedSubscene[part]['CC32'] = sender.GetValue()

    def OnLowerKeyComboBox(self, event, part):
        sender = event.GetEventObject()
        noteNumber = mididings.util.note_number(str(sender.GetValue()))
        self.selectedSubscene[part]['Lower'] = noteNumber

    def OnUpperKeyComboBox(self, event, part):
        sender = event.GetEventObject()
        noteNumber = mididings.util.note_number(str(sender.GetValue()))
        self.selectedSubscene[part]['Upper'] = noteNumber

    def OnSelectPart(self, event, part):
        sender = event.GetEventObject()
        isChecked = sender.GetValue()
        subscene = Subscene()
        if isChecked:
            self.EnablePart(part)
            ## if part number is equal to len(self.selectedSubscene), the part in sceneData doesn't exist yet           
            if part == len(self.selectedSubscene):
                self.selectedSubscene.append(subscene.InitPart())
        else:
            self.DisablePart(part)
            del self.selectedSubscene[part]

    def EnablePart(self, part):
        self.MidiInChSpinCtrls[part].Enable()
        self.MidiChSpinCtrls[part].Enable()
        self.PCSpinCtrls[part].Enable()
        self.Bank00SpinCtrls[part].Enable()
        self.Bank32SpinCtrls[part].Enable()
        self.LowerKeyComboBox[part].Enable()
        self.UpperKeyComboBox[part].Enable()


    def DisablePart(self, part):
        self.MidiInChSpinCtrls[part].Disable()
        self.MidiChSpinCtrls[part].Disable()
        self.PCSpinCtrls[part].Disable()
        self.Bank00SpinCtrls[part].Disable()
        self.Bank32SpinCtrls[part].Disable() 
        self.LowerKeyComboBox[part].Disable()
        self.UpperKeyComboBox[part].Disable() 

    def OnCloseButton(self, event):
        self.Close(True)        
