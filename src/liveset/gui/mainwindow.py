# -*- coding: utf-8 -*-

import wx
import os.path
import threading
import subprocess
import time
import sys

import mididings.engine

##from .editpage import PageSongEdit
from .setlistpage import PageSetlist
from .settingswindow import SettingsWindow
from liveset.livesetconf import *
#import liveset.dings.livesetdings as livesetdings
from liveset.utils.files import *

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        filemenu = wx.Menu()
        settingsmenu = wx.Menu()
        helpmenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN)
        menuSave = filemenu.Append(wx.ID_SAVE)
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS)
        menuQuit = filemenu.Append(wx.ID_EXIT)
        menuOptions = settingsmenu.Append(wx.ID_PROPERTIES, '&Settings', 'Configuration of the program')
        menuAbout = helpmenu.Append(wx.ID_ABOUT, '&About', 'Information about the program')
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        menubar.Append(settingsmenu, '&Settings')
        menubar.Append(helpmenu, '&Help')
        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        openButton = wx.Button(self.toolbar, wx.ID_OPEN)
        saveButton = wx.Button(self.toolbar, wx.ID_SAVE)
        saveAsButton = wx.Button(self.toolbar, wx.ID_SAVEAS)
        startSessionButton = wx.Button(self.toolbar, label='Start Session')
        self.toolbar.AddControl(openButton)
        self.toolbar.AddControl(saveButton)
        self.toolbar.AddControl(saveAsButton)
        self.toolbar.AddControl(startSessionButton)
        self.toolbar.Realize()

        panel = wx.Panel(self, -1)

##        nb = wx.Notebook(panel)

        ## data ##
        self.filePath = scenes_file
        self.data = Data()  # definito in files.py ... magari mettere qui la classe...

##        self.pageEdit = PageSongEdit(nb, self.data)
##        self.pageSetlist = PageSetlist(nb, self.data)
        self.pageSetlist = PageSetlist(panel, self.data)
##        nb.AddPage(self.pageSetlist, "Setlist")
##        nb.AddPage(self.pageEdit, "Scenes edit")

## Buttons

        box = wx.BoxSizer(wx.HORIZONTAL)
##        box.Add(nb, 2, wx.EXPAND)
        box.Add(self.pageSetlist, 2, wx.EXPAND)
        panel.SetSizer(box)

## Binding

        self.Bind(wx.EVT_MENU, self.OnOptions, menuOptions)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnQuit, menuQuit)
        self.Bind(wx.EVT_BUTTON, self.OnOpen, openButton)
        self.Bind(wx.EVT_BUTTON, self.OnSave, saveButton)
        self.Bind(wx.EVT_BUTTON, self.OnSaveAs, saveAsButton)
        self.Bind(wx.EVT_BUTTON, self.OnStartSession, startSessionButton)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
##        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged, nb)

        self.Show()
        self.Maximize(True)
        self.filename = filename

        self.Reload()

        if not(os.path.isfile(settings_file)):
            self.OnOptions(wx.EVT_MENU)

##    def OnPageChanged(self, event):
##        self.pageSetlist.data.scenesName = self.pageEdit.data.scenes.keys()
##        self.pageSetlist.data.scenesName.sort()
##        self.pageSetlist.Reload()

    def Reload(self):
        self.data.Open(self.filePath)
##        self.pageEdit.data = self.data
        self.pageSetlist.data = self.data
##        self.pageEdit.Reload()
        self.pageSetlist.Reload()

    def OnStartSession_ORIGINAL(self, event):
        try:
            self.p_livedings.terminate()
        except:
            pass

        if not mididings.engine.active():
            self.mididings_thread = threading.Thread(target = livesetdings.Run, args=([self.filePath])) 
            self.mididings_thread.daemon = True
            self.mididings_thread.start()

         # subprocess.Popen can call process in background
        self.p_livedings = subprocess.Popen(["livedings","-T"])

        time.sleep(3)

         # maximize livedings window
#         subprocess.Popen(["wmctrl","-r","livedings","-b","add,fullscreen"])
        subprocess.Popen(["wmctrl","-r","livedings","-b","add,maximized_vert,maximized_horz"])  

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

            # maximize livedings window ## METTERE UN'OPZIONE SU SETTINGS
#            subprocess.Popen(["wmctrl","-r","livedings","-b","add,fullscreen"])
            subprocess.Popen(["wmctrl","-r","livedings","-b","add,maximized_vert,maximized_horz"])
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
        #self.data.Save(scenes_file)


    def OnSaveAs(self, event):
        wildcard = "Project files (*.json)|*.json"
        dialog = wx.FileDialog(None, "Save As", data_dir, "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.filePath = dialog.GetPath()
        dialog.Destroy()
        self.data.project["Scenes"] = self.pageSetlist.data.scenes
        self.data.project["Setlist"] = self.pageSetlist.data.setlist
        self.data.Save(self.filePath)
        #self.data.Save(scenes_file)

    def OnAbout(self, event):
        string = '''LiveSet - Setlist Programmer
Copyright (C) 2016-2019 Alessandro Filippo'''

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
        #if mididings.engine.active():   ### questo non servirà più
        #    mididings.engine.quit()
        #    time.sleep(0.5)
        try:
            self.p_livedings.terminate()
            self.p_livesetdings.terminate()
        except:
            pass   

        time.sleep(0.5)       
        sys.exit(0)
