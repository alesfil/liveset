# -*- coding: utf-8 -*-

import wx
import wx.lib.mixins.listctrl as listmix

import os.path
import threading
import subprocess
import time
import sys

import mididings.engine
import mididings.util

from .editwindow import EditWindow, Subscene
from .settingswindow import SettingsWindow
from liveset.livesetconf import *
import json
import liveset.files as files

sign = lambda x : 1 if x>0 else -1 if x <0 else 0

class AutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class PageSetlist(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)

        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.data = data

        ## Setlist listctrl 
        self.setListCtrl = AutoWidthListCtrl(self) 
        self.setListCtrl.InsertColumn(0,'Pos.')
        self.setListCtrl.InsertColumn(1,'Active')
        self.setListCtrl.InsertColumn(2,'Scene')

        self.sceneTextCtrl = wx.TextCtrl(self) 
        self.sceneTextCtrl.SetFont(font)

        ## Buttons

        upButton = wx.Button(self, label='Scene Up')
        downButton = wx.Button(self, label='Scene Down')
        newButton = wx.Button(self, label='New Scene')
        deleteButton = wx.Button(self, label='Delete Scene')
        editButton = wx.Button(self, label='Edit Scene')
        activeButton = wx.Button(self, label='Activate Scene')


        ## Boxes
      
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.sceneTextCtrl, 0, wx.EXPAND | wx.ALL, 5)
        vbox1.Add(self.setListCtrl, 1, wx.EXPAND | wx.ALL, 5)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(upButton, 1, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(newButton, 1,  wx.EXPAND | wx.ALL, 5)
        vbox2.Add(editButton, 1,  wx.EXPAND | wx.ALL, 5)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(downButton, 1, wx.EXPAND | wx.ALL, 5)
        vbox3.Add(deleteButton, 1, wx.EXPAND | wx.ALL, 5)
        vbox3.Add(activeButton, 1, wx.EXPAND | wx.ALL, 5)
 

        staticBox = wx.StaticBox(self, label='Setlist')
        hbox2 = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        hbox2.Add(vbox1, 4, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(vbox2, 1, wx.ALL, 5)
        hbox2.Add(vbox3, 1, wx.ALL, 5)


        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(hbox2, 1, wx.EXPAND)

        upButton.Bind(wx.EVT_BUTTON, self.OnUp)
        downButton.Bind(wx.EVT_BUTTON, self.OnDown)
        newButton.Bind(wx.EVT_BUTTON, self.OnNew)
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDelete)
        editButton.Bind(wx.EVT_BUTTON, self.OnEdit)
        activeButton.Bind(wx.EVT_BUTTON, self.OnActivate)

        self.setListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectSetList)
        self.sceneTextCtrl.Bind(wx.EVT_TEXT, self.OnRenameScene)

        self.SetSizer(hbox)


    def Reload(self):
        ## ChangeValue in order to not raise EVT_TEXT in TextCtrl ##
        self.sceneTextCtrl.ChangeValue("")

        # define a list for setlist (dict are not sorted)
        try:
            self.setlist = [None]*len(self.data.setlist)
            for key in self.data.setlist:
                self.setlist[abs(int(key))-1] = [self.data.setlist[key], sign(int(key))]
        except:
            self.setlist = []

        self.setListCtrl.DeleteAllItems()
        for index, scene in enumerate(self.setlist):
            if scene[0] in self.data.scenesName:
                # if scene is active if 1, not active if -1
                if scene[1] == 1:    
                    self.setListCtrl.Append([str(index+1), "Yes", scene[0]])
                else:
                    self.setListCtrl.Append([str(index+1), "No", scene[0]])


    def RefreshData(self):
        self.data.setlist = {}
        setlistLen = self.setListCtrl.GetItemCount() 
        for index in range(setlistLen):
            itemPos = self.setListCtrl.GetItem(index, 0)
            textPos = itemPos.GetText()
            itemScene = self.setListCtrl.GetItem(index, 2)
            textScene = itemScene.GetText()
            itemActive = self.setListCtrl.GetItem(index, 1)
            textActive = itemActive.GetText()
            if textActive == "Yes":
                self.data.setlist[textPos] = textScene
            else:
                self.data.setlist["-"+textPos] = textScene   


    def OnSelectSetList(self, event):
        sel = self.setListCtrl.GetFirstSelected()
        item = self.setListCtrl.GetItem(sel, 2)
        text = item.GetText()
        self.sceneTextCtrl.SetValue(text)


    def OnUp(self, event):
        sel = self.setListCtrl.GetFirstSelected()
        setlistLen = self.setListCtrl.GetItemCount()
        if sel > 0:
            item = self.setListCtrl.GetItem(sel, 2)
            activeItem = self.setListCtrl.GetItem(sel, 1)
            text = item.GetText()
            activeText = activeItem.GetText()
            index = self.setListCtrl.InsertStringItem(sel-1, str(sel)) 
            self.setListCtrl.SetStringItem(index, 2, text)
            self.setListCtrl.SetStringItem(index, 1, activeText)
            self.setListCtrl.DeleteItem(sel+1)

            for index in range(setlistLen):
                self.setListCtrl.SetStringItem(index, 0, str(index+1))
            self.setListCtrl.Select(sel-1)  

        self.RefreshData()


    def OnDown(self, event):
        sel = self.setListCtrl.GetFirstSelected()
        setlistLen = self.setListCtrl.GetItemCount()
        if sel != -1 and sel <  setlistLen-1:
            item = self.setListCtrl.GetItem(sel, 2)
            activeItem = self.setListCtrl.GetItem(sel, 1)
            text = item.GetText()
            activeText = activeItem.GetText()
            index = self.setListCtrl.InsertStringItem(sel+2, str(sel))
            self.setListCtrl.SetStringItem(index, 2, text)
            self.setListCtrl.SetStringItem(index, 1, activeText)
            self.setListCtrl.DeleteItem(sel) 
    
            for index in range(setlistLen):
                self.setListCtrl.SetStringItem(index, 0, str(index+1))
            self.setListCtrl.Select(sel+1) 

        self.RefreshData()


    def OnNew(self, event):
        sceneText = self.InitScene()
        sel = self.setListCtrl.GetFirstSelected()
        activeText = "Yes"   

        if sel != -1:
            index = self.setListCtrl.InsertStringItem(sel, str(sel+1))
            self.setListCtrl.SetStringItem(index, 1, activeText)
            self.setListCtrl.SetStringItem(index, 2, sceneText)

        else:
            self.setListCtrl.Append([str(self.setListCtrl.GetItemCount()), activeText, sceneText])

        setlistLen = self.setListCtrl.GetItemCount()
        for index in range(setlistLen):
            self.setListCtrl.SetStringItem(index, 0, str(index+1))

        self.RefreshData()


    def OnDelete(self, event):
        sel = self.setListCtrl.GetFirstSelected()
        if sel!= -1:
            self.setListCtrl.DeleteItem(sel)

            setlistLen = self.setListCtrl.GetItemCount() 
            for index in range(setlistLen):
                self.setListCtrl.SetStringItem(index, 0, str(index+1))

            if sel < setlistLen:
                self.setListCtrl.Select(sel)
            elif (sel == setlistLen) and setlistLen > 0:
                self.setListCtrl.Select(sel-1)

        self.RefreshData()
          

    def OnEdit(self, event):
        sel = self.setListCtrl.GetFirstSelected()
        if sel != -1:
            itemScene = self.setListCtrl.GetItem(sel, 2)
            textScene = itemScene.GetText()

            editWindow = EditWindow(self, self.data, textScene)
            editWindow.Show()

            displaySize = wx.GetDisplaySize()
            if displaySize[0] <= 1024: # Maximize only for small screens       
                editWindow.Maximize(True)


    def OnActivate(self, event):
        sel = self.setListCtrl.GetFirstSelected()
        if sel != -1:
            activeItem = self.setListCtrl.GetItem(sel, 1)
            activeText = activeItem.GetText()
            if activeText == "Yes":
                self.setListCtrl.SetStringItem(sel, 1, "No")
            else:
                self.setListCtrl.SetStringItem(sel, 1, "Yes")

        self.RefreshData()

    def OnRenameScene(self, event):
        sel = self.setListCtrl.GetFirstSelected()
        if sel != -1:
            item = self.setListCtrl.GetItem(sel, 2)
            oldText = item.GetText()
            newText = self.sceneTextCtrl.GetValue()

            self.setListCtrl.SetStringItem(sel, 2, newText)

            if oldText != newText:
                self.data.scenes[newText] = self.data.scenes[oldText]

            self.RefreshData()

            setlistLen = self.setListCtrl.GetItemCount()
            occurrency = 0
            for i in range(0, setlistLen):
                item = self.setListCtrl.GetItem(i, 2)
                text = item.GetText()
                if text == oldText:
                    occurrency = occurrency + 1

            if occurrency == 0:
            # old scene can be deleted only if no other occurency are present on setlist
                del self.data.scenes[oldText] 


    def InitScene(self):
        sceneText = "New Scene" 

        subsceneText = "--"
        self.data.scenes[sceneText] = [{}]
        part = 0
        subscene = Subscene()
        self.data.scenes[sceneText][part][subsceneText] = subscene.InitSubscene()
        return sceneText

###########################

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        panel = wx.Panel(self, -1)

        self.toolbar1 = wx.ToolBar(panel)
        self.toolbar2 = wx.ToolBar(panel)
        openButton = wx.Button(self.toolbar1, wx.ID_OPEN)
        saveButton = wx.Button(self.toolbar1, wx.ID_SAVE)
        saveAsButton = wx.Button(self.toolbar1, wx.ID_SAVEAS)
        startSessionButton = wx.Button(self.toolbar1, label='Start Session')
        settingsButton = wx.Button(self.toolbar2, label='Settings')
        aboutButton = wx.Button(self.toolbar2, wx.ID_ABOUT, label='About')
        self.toolbar1.AddControl(openButton)
        self.toolbar1.AddControl(saveButton)
        self.toolbar1.AddControl(saveAsButton)
        self.toolbar1.AddControl(startSessionButton)
        self.toolbar1.Realize()
        self.toolbar2.AddControl(settingsButton)
        self.toolbar2.AddControl(aboutButton)
        self.toolbar2.Realize()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.toolbar1, 0)
        hbox.AddStretchSpacer(1)
        hbox.Add(self.toolbar2, 0)


        ## data ##
        self.filePath = scenes_file
        self.data = files.Data()

        self.pageSetlist = PageSetlist(panel, self.data)

        ## Sizers ##

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(hbox, 0, wx.EXPAND)
        box.Add(self.pageSetlist, 1, wx.EXPAND)


        ## Binding

        self.Bind(wx.EVT_BUTTON, self.OnOpen, openButton)
        self.Bind(wx.EVT_BUTTON, self.OnSave, saveButton)
        self.Bind(wx.EVT_BUTTON, self.OnSaveAs, saveAsButton)
        self.Bind(wx.EVT_BUTTON, self.OnStartSession, startSessionButton)
        self.Bind(wx.EVT_BUTTON, self.OnOptions, settingsButton)
        self.Bind(wx.EVT_BUTTON, self.OnAbout, aboutButton)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

 
        panel.SetSizer(box)

	sizer = wx.BoxSizer(wx.HORIZONTAL)
    	sizer.Add(panel, 1, wx.EXPAND)
    	self.SetSizerAndFit(sizer)
        self.Show()

        displaySize = wx.GetDisplaySize()
        if displaySize[0] <= 1024: # Maximize only for small screens       
            self.Maximize(True) 

        self.filename = filename


        self.Reload()

        if not(os.path.isfile(settings_file)):
            self.OnOptions(wx.EVT_MENU)

    def Reload(self):
        self.data.Open(self.filePath)
        self.pageSetlist.data = self.data
        self.pageSetlist.Reload()


    def OnStartSession(self, event):
        try:
            self.p_livedings.terminate()
            self.p_livesetdings.terminate()
        except:
            pass

        if len(self.data.setlist) > 1: # mididings doesn't work with 1 scene
            # subprocess.Popen can call process in background
            self.p_livesetdings = subprocess.Popen(["livesetdings", self.filePath])
            self.p_livedings = subprocess.Popen(["livedings","-T", "-F", "Sans 24 bold", "-n", self.filename])

            time.sleep(3)

            # maximize livedings window
            try:
                with open(settings_file) as data_file:
                    self.options = json.load(data_file)
            except:
                self.options = {}  
                self.options["livedingsView"] = "Maximized"

            if self.options["livedingsView"] == "Fullscreen":
                try:
                    subprocess.Popen(["wmctrl","-r","livedings","-b","add,fullscreen"])
                except:
                    pass
            elif self.options["livedingsView"] == "Maximized":
                try:
                    subprocess.Popen(["wmctrl","-r","livedings","-b","add,maximized_vert,maximized_horz"])
                except:
                    pass
        else:
            print("There is only one scene. Please add more scenes")  

    def OnOpen(self, event):
        wildcard = "Project files (*.json)|*.json"
        dialog = wx.FileDialog(None, "Open", data_dir, "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filePath = dialog.GetPath()
            self.filename = dialog.GetFilename()
        dialog.Destroy()
        self.Reload()
        self.SetTitle(self.filename)


    def OnSave(self, event):
        self.data.project["Scenes"] = self.pageSetlist.data.scenes
        self.data.project["Setlist"] = self.pageSetlist.data.setlist
        self.data.Save(self.filePath)


    def OnSaveAs(self, event):
        wildcard = "Project files (*.json)|*.json"
        dialog = wx.FileDialog(None, "Save As", data_dir, "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.filePath = dialog.GetPath()
        dialog.Destroy()

        if self.filePath[-5] != '.json': # extracted string
            self.filePath = self.filePath + '.json'

        self.data.project["Scenes"] = self.pageSetlist.data.scenes
        self.data.project["Setlist"] = self.pageSetlist.data.setlist
        self.data.Save(self.filePath)


    def OnAbout(self, event):
        string = '''LiveSet - Setlist Programmer
Version 0.8.0
Copyright (C) 2016-2019 Alessandro Filippo
License: GPL-2+'''

        dialog = wx.MessageDialog(self, string, 'About', wx.OK | wx.ALIGN_CENTRE)
        dialog.ShowModal()
        dialog.Destroy()

    def OnOptions(self, event):
        settingsWindow = SettingsWindow()
	settingsWindow.Show()

    def OnQuit(self, event):
        # send a EVT_CLOSE, calling OnClose()
        self.Close(True)

    def OnClose(self, event):
        try:
            self.p_livedings.terminate()
            self.p_livesetdings.terminate()
        except:
            pass   

        time.sleep(0.5)       
        sys.exit(0)
