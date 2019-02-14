# -*- coding: utf-8 -*-

import wx
##import wx.lib.scrolledpanel

##class PageSongEdit(wx.lib.scrolledpanel.ScrolledPanel):
class EditWindow(wx.Frame):
    def __init__(self, parent, data, sceneText):
        wx.Frame.__init__(self, None, title=sceneText)
##        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent)
##        self.SetupScrolling()

        self.data = data
        self.sceneText = sceneText

        ## Scenes listbox
##        self.scenesListbox = wx.ListBox(self, -1)
       
        ## TextCtrls

##        self.sceneTextCtrl = wx.TextCtrl(self)  
        self.subsceneTextCtrl = wx.TextCtrl(self)      

        ## Buttons

##        newSceneButton = wx.Button(self, label='New Scene')
        newSubsceneButton = wx.Button(self, label='New Subscene')
##        delSceneButton = wx.Button(self, label='Del Scene')
        delSubsceneButton = wx.Button(self, label='Del Subscene')
        closeButton = wx.Button(self, label='Close')

        ## Subscenes list box

        self.subscenesListbox = wx.ListBox(self, -1)

        ## zone (parts) number
        self.zones = 4

        self.partsCheckBox = []
        self.MidiChSpinCtrls = []
        self.PCSpinCtrls = []
        self.Bank00SpinCtrls = []
        self.Bank32SpinCtrls = []


        for i in range(0, self.zones):
            self.partsCheckBox.append(wx.CheckBox(self, label="Part "+str(i+1)+":", style = wx.ALIGN_RIGHT))

            self.MidiChSpinCtrls.append(wx.SpinCtrl(self, value =str(i+1)))
            self.MidiChSpinCtrls[i].SetRange(1, 16)

            self.PCSpinCtrls.append(wx.SpinCtrl(self, value ='0'))
            self.PCSpinCtrls[i].SetRange(1, 128)

            self.Bank00SpinCtrls.append(wx.SpinCtrl(self, value ='0'))
            self.Bank00SpinCtrls[i].SetRange(0, 127)

            self.Bank32SpinCtrls.append(wx.SpinCtrl(self, value ='0'))
            self.Bank32SpinCtrls[i].SetRange(0, 127)


        PartText = wx.StaticText(self, label="Part")        
        MidiChText = wx.StaticText(self, label="MIDI CH")
        PCText = wx.StaticText(self, label="Program Change")
        Bank00Text = wx.StaticText(self, label="Bank 00")
        Bank32Text = wx.StaticText(self, label="Bank 32")

        Labels = [PartText, MidiChText, PCText, Bank00Text, Bank32Text]

        grid = wx.GridSizer(17, 5, 2, 2)
  
        grid.AddMany(Labels)
        for i in range(0, self.zones):
            grid.AddMany([self.partsCheckBox[i], self.MidiChSpinCtrls[i], self.PCSpinCtrls[i], self.Bank00SpinCtrls[i], self.Bank32SpinCtrls[i]])

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
##        hbox1.Add(newSceneButton, 1, wx.EXPAND | wx.ALL, 5)
##        hbox1.Add(delSceneButton, 1, wx.EXPAND | wx.ALL, 5)

##        staticBox1 = wx.StaticBox(self, label='Scenes')
##        vbox1 = wx.StaticBoxSizer(staticBox1, wx.VERTICAL)
##        vbox1.Add(hbox1, 0, wx.EXPAND | wx.ALL, 5)
##        vbox1.Add(self.sceneTextCtrl, 0, wx.EXPAND | wx.ALL, 5)
##        vbox1.Add(self.scenesListbox, 1, wx.EXPAND | wx.ALL, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(newSubsceneButton, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(delSubsceneButton, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(closeButton, 1, wx.EXPAND | wx.ALL, 5)

        staticBox2 = wx.StaticBox(self, label='Subscenes')
        vbox2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)
        vbox2.Add(hbox2, 0, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.subsceneTextCtrl, 0, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.subscenesListbox, 1, wx.EXPAND | wx.ALL, 5)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(grid, 1,  wx.ALL, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
##        hbox.Add(vbox1, 1,  wx.EXPAND | wx.ALL, 5)
        hbox.Add(vbox2, 1,  wx.EXPAND | wx.ALL, 5)
        hbox.Add(vbox3, 0,  wx.EXPAND | wx.ALL, 5)

        ## Binding

##        newSceneButton.Bind(wx.EVT_BUTTON, self.OnNewSceneButton) 
        newSubsceneButton.Bind(wx.EVT_BUTTON, self.OnNewSubsceneButton)
##        delSceneButton.Bind(wx.EVT_BUTTON, self.OnDelSceneButton) 
        delSubsceneButton.Bind(wx.EVT_BUTTON, self.OnDelSubsceneButton)  
##        self.sceneTextCtrl.Bind(wx.EVT_TEXT, self.OnEditScene)
        self.subsceneTextCtrl.Bind(wx.EVT_TEXT, self.OnEditSubscene)
##        self.scenesListbox.Bind(wx.EVT_LISTBOX, self.OnSelectScene)
        self.subscenesListbox.Bind(wx.EVT_LISTBOX, self.OnSelectSubscene)
        closeButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)

        for part in range(0, self.zones):
            self.partsCheckBox[part].Bind(wx.EVT_CHECKBOX, lambda evt, temp=part: self.OnSelectPart(evt, temp))
            self.MidiChSpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnMidiSpinCtrl(evt, temp))
            self.PCSpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnPCSpinCtrl(evt, temp))
            self.Bank00SpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnBank00SpinCtrl(evt, temp))
            self.Bank32SpinCtrls[part].Bind(wx.EVT_SPINCTRL, lambda evt, temp=part: self.OnBank32SpinCtrl(evt, temp))
   
        self.SetSizer(hbox)
        self.OnLoad()


    def OnLoad(self):
        self.subscenesListbox.Clear()
##        sceneSel = self.scenesListbox.GetSelection()
##       sceneText = self.scenesListbox.GetString(sceneSel)

##        ## ChangeValue in order to not raise EVT_TEXT in TextCtrl ##
##        self.sceneTextCtrl.ChangeValue(self.sceneText)

        for subsceneSel in self.data.scenes[self.sceneText]:
            for subsceneText in subsceneSel:
                self.subscenesListbox.Append(subsceneText)

        self.subscenesListbox.Select(0)
        self.OnSelectSubscene(wx.EVT_LISTBOX)

#    def Reload(self):
#        self.scenesListbox.Set(self.data.scenesName)
#        if len(self.data.scenesName) == 0:
#            self.scenesListbox.Append(self.InitScene())     
#        self.scenesListbox.Select(0)        
#        self.OnSelectScene(wx.EVT_LISTBOX)

#    def OnEditScene(self, event):
#        sceneSel = self.scenesListbox.GetSelection()
#        oldText = self.scenesListbox.GetString(sceneSel)
#        newText = self.sceneTextCtrl.GetValue()

#        self.scenesListbox.SetString(sceneSel, newText)

#        if oldText != newText:
#            self.data.scenes[newText] = self.data.scenes[oldText]
#            del self.data.scenes[oldText]


    def OnEditSubscene(self, event):
        #sceneSel = self.scenesListbox.GetSelection()
        #sceneText = self.scenesListbox.GetString(sceneSel)
        
        subsceneSel = self.subscenesListbox.GetSelection()
        oldText = self.subscenesListbox.GetString(subsceneSel)
        newText = self.subsceneTextCtrl.GetValue()

        self.subscenesListbox.SetString(subsceneSel, newText)

        if oldText != newText:
            self.data.scenes[self.sceneText][subsceneSel][newText] = self.data.scenes[self.sceneText][subsceneSel][oldText]
            del self.data.scenes[self.sceneText][subsceneSel][oldText]
#### ANCHE QUI RAGIONARE SULLE OCCORRENZE COME SU SETLISTPAGE ##


    def InitPart(self):
        part = {}
        part["CH"] = 1
        part["PC"] = 1
        part["CC0"] = 0
        part["CC32"] = 0
        return part

    def InitSubscene(self):
        part = self.InitPart()
        subscene = [part]
        return subscene

#    def InitScene(self):
#        sceneText = "New Scene"
#        subsceneText = "--"
#        self.data.scenes[sceneText] = [{}]
#        part = 0
#        self.data.scenes[sceneText][part][subsceneText] = self.InitSubscene()
#        return sceneText

#    def OnNewSceneButton(self, event):
#        sceneText = self.InitScene()

#        ## New scene added at the end of the listbox
#        self.scenesListbox.Append(sceneText)
#        subsceneCount = self.scenesListbox.GetCount()
#        self.scenesListbox.Select(subsceneCount-1)
#        self.OnSelectScene(wx.EVT_LISTBOX)


    def OnNewSubsceneButton(self, event):
        ##sceneSel = self.scenesListbox.GetSelection()
        ##sceneText = self.scenesListbox.GetString(sceneSel)
        subsceneText = "--"
        self.data.scenes[self.sceneText].append({subsceneText : self.InitSubscene()})  
        self.subscenesListbox.Append(subsceneText)
        subsceneCount = self.subscenesListbox.GetCount()
        self.subscenesListbox.Select(subsceneCount-1)
        self.OnSelectSubscene(wx.EVT_LISTBOX)


#    def OnDelSceneButton(self, event):
#        sceneSel = self.scenesListbox.GetSelection()
#        sceneText = self.scenesListbox.GetString(sceneSel)
#        if sceneSel != -1:
#            self.scenesListbox.Delete(sceneSel)
#            del self.data.scenes[sceneText]
#            try:
#                self.scenesListbox.Select(sceneSel)
#            except:
#                self.scenesListbox.Select(sceneSel-1)
#            self.OnSelectScene(wx.EVT_LISTBOX)


    def OnDelSubsceneButton(self, event):
        ##sceneSel = self.scenesListbox.GetSelection()
        ##sceneText = self.scenesListbox.GetString(sceneSel)
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

        ##sceneSel = self.scenesListbox.GetSelection()
        ##sceneText = self.scenesListbox.GetString(sceneSel)
        self.subsceneTextCtrl.ChangeValue(subsceneText) 

        subscene = self.data.scenes[self.sceneText][subsceneSel][subsceneText]
        for part in range(0, len(subscene)):        
                self.partsCheckBox[part].SetValue(True)
                self.EnablePart(part) 
                self.MidiChSpinCtrls[part].SetValue(subscene[part]['CH'])
                self.PCSpinCtrls[part].SetValue(subscene[part]['PC'])
                self.Bank00SpinCtrls[part].SetValue(subscene[part]['CC0'])
                self.Bank32SpinCtrls[part].SetValue(subscene[part]['CC32'])

        for part in range(len(subscene), self.zones):
                self.partsCheckBox[part].SetValue(False)
                self.DisablePart(part)

        ## REMINDER: the following point to self.data.scenes...
        self.selectedSubscene = subscene


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

    def OnSelectPart(self, event, part):
        sender = event.GetEventObject()
        isChecked = sender.GetValue()
        if isChecked:
            self.EnablePart(part)
            ## if part number is equal to len(self.selectedSubscene), the part in sceneData doesn't exist yet           
            if part == len(self.selectedSubscene):
                self.selectedSubscene.append(self.InitPart())
        else:
            self.DisablePart(part)
            del self.selectedSubscene[part]

    def EnablePart(self, part):
        self.MidiChSpinCtrls[part].Enable()
        self.PCSpinCtrls[part].Enable()
        self.Bank00SpinCtrls[part].Enable()
        self.Bank32SpinCtrls[part].Enable()


    def DisablePart(self, part):
        self.MidiChSpinCtrls[part].Disable()
        self.PCSpinCtrls[part].Disable()
        self.Bank00SpinCtrls[part].Disable()
        self.Bank32SpinCtrls[part].Disable()  

    def OnCloseButton(self, event):
        self.Close(True)        