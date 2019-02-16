# -*- coding: utf-8 -*-

import wx
import wx.lib.mixins.listctrl as listmix

from .editwindow import EditWindow, Subscene

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
                del self.data.scenes[oldText] # lo posso cancellare solo se non ci sono altre occorrenze sulla setlist!!


    def InitScene(self):
        sceneText = "New Scene" 

        subsceneText = "--"
        self.data.scenes[sceneText] = [{}]
        part = 0
        subscene = Subscene()
        self.data.scenes[sceneText][part][subsceneText] = subscene.InitSubscene()
        return sceneText
