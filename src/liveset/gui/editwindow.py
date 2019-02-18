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

        self.data = data
        self.sceneText = sceneText

       
        ## TextCtrls

        self.subsceneTextCtrl = wx.TextCtrl(self)      

        ## Buttons

        newSubsceneButton = wx.Button(self, label='New Subscene')
        delSubsceneButton = wx.Button(self, label='Del Subscene')
        closeButton = wx.Button(self, label='Close')

        ## Subscenes list box

        self.subscenesListbox = wx.ListBox(self, -1)

        ## zone (parts) number
        self.zones = 4

        self.partsCheckBox = []
        self.MidiInChSpinCtrls = []
        self.MidiChSpinCtrls = []
        self.PCSpinCtrls = []
        self.Bank00SpinCtrls = []
        self.Bank32SpinCtrls = []
#        self.LowerKeySpinCtrls = []
        self.LowerKeyComboBox = []
#        self.UpperKeySpinCtrls = []
        self.UpperKeyComboBox = []


        for i in range(0, self.zones):
            self.partsCheckBox.append(wx.CheckBox(self, label="Part "+str(i+1)+":", style = wx.ALIGN_RIGHT))

            self.MidiInChSpinCtrls.append(wx.SpinCtrl(self, value =str(i+1)))
            self.MidiInChSpinCtrls[i].SetRange(1, 16)

            self.MidiChSpinCtrls.append(wx.SpinCtrl(self, value =str(i+1)))
            self.MidiChSpinCtrls[i].SetRange(1, 16)

            self.PCSpinCtrls.append(wx.SpinCtrl(self, value ='0'))
            self.PCSpinCtrls[i].SetRange(1, 128)

            self.Bank00SpinCtrls.append(wx.SpinCtrl(self, value ='0'))
            self.Bank00SpinCtrls[i].SetRange(0, 127)

            self.Bank32SpinCtrls.append(wx.SpinCtrl(self, value ='0'))
            self.Bank32SpinCtrls[i].SetRange(0, 127)

#            self.LowerKeySpinCtrls.append(wx.SpinCtrl(self, value ='0'))  # sarebbe meglio un combobox o simile e un dict con i nomi nota mididings
#            self.LowerKeySpinCtrls[i].SetRange(0, 127)
            self.LowerKeyComboBox.append(wx.ComboBox(self, choices=noteList, style=wx.CB_READONLY))

#            self.UpperKeySpinCtrls.append(wx.SpinCtrl(self, value ='0'))
#            self.UpperKeySpinCtrls[i].SetRange(0, 127)
            self.UpperKeyComboBox.append(wx.ComboBox(self, choices=noteList, style=wx.CB_READONLY))


        PartText = wx.StaticText(self, label="Part")
        MidiInChText = wx.StaticText(self, label="MIDI In CH")        
        MidiChText = wx.StaticText(self, label="MIDI Out CH")
        PCText = wx.StaticText(self, label="Program Change")
        Bank00Text = wx.StaticText(self, label="Bank 00")
        Bank32Text = wx.StaticText(self, label="Bank 32")
        LowerKeyText = wx.StaticText(self, label="Lower Key")
        UpperKeyText = wx.StaticText(self, label="Upper Key")

        grid = wx.GridSizer(8, self.zones+1, 2, 2)
        grid.Add(PartText)
        grid.AddMany(self.partsCheckBox)
        grid.Add(MidiInChText)
        grid.AddMany(self.MidiInChSpinCtrls)
        grid.Add(MidiChText)
        grid.AddMany(self.MidiChSpinCtrls)
        grid.Add(PCText)
        grid.AddMany(self.PCSpinCtrls)
        grid.Add(Bank00Text)
        grid.AddMany(self.Bank00SpinCtrls)
        grid.Add(Bank32Text)
        grid.AddMany(self.Bank32SpinCtrls)
        grid.Add(LowerKeyText)
#        grid.AddMany(self.LowerKeySpinCtrls)
        grid.AddMany(self.LowerKeyComboBox)
        grid.Add(UpperKeyText)
#        grid.AddMany(self.UpperKeySpinCtrls)
        grid.AddMany(self.UpperKeyComboBox)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(newSubsceneButton, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(delSubsceneButton, 1, wx.EXPAND | wx.ALL, 5)

        staticBox2 = wx.StaticBox(self, label='Subscenes')
        vbox2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)
        vbox2.Add(hbox2, 0, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.subsceneTextCtrl, 0, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.subscenesListbox, 1, wx.EXPAND | wx.ALL, 5)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(grid, 0,  wx.ALL, 5)
        vbox3.Add(closeButton, 0, wx.ALL | wx.CENTER, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vbox2, 1,  wx.EXPAND | wx.ALL, 5)
        hbox.Add(vbox3, 0,  wx.EXPAND | wx.ALL, 5)

        ## Binding

        newSubsceneButton.Bind(wx.EVT_BUTTON, self.OnNewSubsceneButton)
        delSubsceneButton.Bind(wx.EVT_BUTTON, self.OnDelSubsceneButton)  
        self.subsceneTextCtrl.Bind(wx.EVT_TEXT, self.OnEditSubscene)
        self.subscenesListbox.Bind(wx.EVT_LISTBOX, self.OnSelectSubscene)
        closeButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)

        for part in range(0, self.zones):
            self.partsCheckBox[part].Bind(wx.EVT_CHECKBOX, lambda evt, temp=part: self.OnSelectPart(evt, temp))
            self.MidiInChSpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnMidiInSpinCtrl(evt, temp))
            self.MidiChSpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnMidiSpinCtrl(evt, temp))
            self.PCSpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnPCSpinCtrl(evt, temp))
            self.Bank00SpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnBank00SpinCtrl(evt, temp))
#            self.LowerKeySpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnLowerKeySpinCtrl(evt, temp))
            self.LowerKeyComboBox[part].Bind(wx.EVT_COMBOBOX, lambda evt, temp=part: self.OnLowerKeyComboBox(evt, temp))
#            self.UpperKeySpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnUpperKeySpinCtrl(evt, temp))
            self.UpperKeyComboBox[part].Bind(wx.EVT_COMBOBOX, lambda evt, temp=part: self.OnUpperKeyComboBox(evt, temp))
   
        self.SetSizer(hbox)
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
#                self.LowerKeySpinCtrls[part].SetValue(subscene[part]['Lower'])
                lowerNote = noteList[subscene[part]['Lower']]
                self.LowerKeyComboBox[part].SetValue(lowerNote)
#                self.UpperKeySpinCtrls[part].SetValue(subscene[part]['Upper'])
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

#    def OnLowerKeySpinCtrl(self, event, part):
#        sender = event.GetEventObject()
#        self.selectedSubscene[part]['Lower'] = sender.GetValue()
    def OnLowerKeyComboBox(self, event, part):
        sender = event.GetEventObject()
        noteNumber = mididings.util.note_number(str(sender.GetValue()))
        self.selectedSubscene[part]['Lower'] = noteNumber

#    def OnUpperKeySpinCtrl(self, event, part):
#        sender = event.GetEventObject()
#        self.selectedSubscene[part]['Upper'] = sender.GetValue()
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
#        self.LowerKeySpinCtrls[part].Enable()
        self.LowerKeyComboBox[part].Enable()
#        self.UpperKeySpinCtrls[part].Enable()
        self.UpperKeyComboBox[part].Enable()


    def DisablePart(self, part):
        self.MidiInChSpinCtrls[part].Disable()
        self.MidiChSpinCtrls[part].Disable()
        self.PCSpinCtrls[part].Disable()
        self.Bank00SpinCtrls[part].Disable()
        self.Bank32SpinCtrls[part].Disable() 
#        self.LowerKeySpinCtrls[part].Disable() 
        self.LowerKeyComboBox[part].Disable()
#        self.UpperKeySpinCtrls[part].Disable()
        self.UpperKeyComboBox[part].Disable() 

    def OnCloseButton(self, event):
        self.Close(True)        