# -*- coding: utf-8 -*-

import wx
import wx.lib.mixins.listctrl as listmix

class AutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class PageSetlist(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)

        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.data = data

        ## All songs listbox
        self.allSongsListbox = wx.ListBox(self, -1)

        self.data = data
        
        self.allSongsLabel = wx.StaticText(self, label="")
        self.allSongsLabel.SetFont(font)

#        ## Set list listbox

#        self.setListBox = wx.ListBox(self, -1)
        ## Setlist listctrl 
        self.setListCtrl = AutoWidthListCtrl(self) 
        self.setListCtrl.InsertColumn(0,'Pos.')
        self.setListCtrl.InsertColumn(1,'Scene')

        self.setListLabel = wx.StaticText(self, label="")
        self.setListLabel.SetFont(font)

        ## Buttons

        insertButton = wx.Button(self, label='Insert -->')
        upButton = wx.Button(self, label='Song Up')
        downButton = wx.Button(self, label='Song Down')
        deleteButton = wx.Button(self, label='Song Delete')

        ## Boxes
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)       
        hbox1.Add(insertButton, 0, wx.ALL, 5)

        staticBox1 = wx.StaticBox(self, label='Scenes')
        vbox1 = wx.StaticBoxSizer(staticBox1, wx.VERTICAL)
        vbox1.Add(hbox1, 0, wx.EXPAND |wx.ALL, 5)
        vbox1.Add(self.allSongsLabel, 0, wx.ALL, 5)
        vbox1.Add(self.allSongsListbox, 1,  wx.EXPAND |  wx.ALL, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(upButton, 1, wx.ALL, 5)
        hbox2.Add(downButton, 1,  wx.ALL, 5)
        hbox2.Add(deleteButton, 1,  wx.ALL, 5)

        staticBox2 = wx.StaticBox(self, label='Setlist')
        vbox2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)
        vbox2.Add(hbox2, 0, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.setListLabel, 0, wx.ALL, 5)
#        vbox2.Add(self.setListBox, 1, wx.EXPAND | wx.ALL, 5)
        vbox2.Add(self.setListCtrl, 1, wx.EXPAND | wx.ALL, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vbox1, 1, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND)


        insertButton.Bind(wx.EVT_BUTTON, self.OnInsert)
        upButton.Bind(wx.EVT_BUTTON, self.OnUp)
        downButton.Bind(wx.EVT_BUTTON, self.OnDown)
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDelete)
#        self.setListBox.Bind(wx.EVT_LISTBOX, self.OnSelectSetList)
        self.setListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectSetList)
        self.allSongsListbox.Bind(wx.EVT_LISTBOX, self.OnSelectAllSongsList)

        self.SetSizer(hbox)


    def Reload(self):
        self.allSongsListbox.Set(self.data.scenesName)
        self.setListLabel.SetLabel("")
        # define a list for setlist (dict are not sorted)
        try:
            self.setlist = [None]*len(self.data.setlist)          
            for pos in self.data.setlist:
                self.setlist[int(pos)-1] = self.data.setlist[pos] 
        except:
            self.setlist = []

#        self.setListBox.Set([])  
#        for song in self.setlist:
#            if song in self.data.scenesName:
#                self.setListBox.Append(song)
##
        self.setListCtrl.DeleteAllItems()
        for index, song in enumerate(self.setlist):
            if song in self.data.scenesName:
                self.setListCtrl.Append([str(index+1), song])
##

    def OnSelectAllSongsList(self, event):
         sel = self.allSongsListbox.GetSelection()
         self.allSongsLabel.SetLabel(self.allSongsListbox.GetString(sel))  

    def OnSelectSetList(self, event):
#        sel = self.setListBox.GetSelection()
        sel = self.setListCtrl.GetFirstSelected()
        item = self.setListCtrl.GetItem(sel, 1)
        text = item.GetText()
#        self.setListLabel.SetLabel(self.setListBox.GetString(sel))
        self.setListLabel.SetLabel(text)

    def OnInsert(self, event):
        sel1 = self.allSongsListbox.GetSelection()

#        if sel1 != -1: 
#            text = self.allSongsListbox.GetString(sel1)
#            sel2 = self.setListBox.GetSelection()
#            if sel2 != -1: 
#                self.setListBox.Insert(text, sel2)
#            else:
#                self.setListBox.Append(text)

##
        if sel1 != -1: 
            scene = self.allSongsListbox.GetString(sel1)
            sel2 = self.setListCtrl.GetFirstSelected()
            if sel2 != -1:
                index = self.setListCtrl.InsertStringItem(sel2, str(sel2+1))
                self.setListCtrl.SetStringItem(index, 1, scene)
            else:
                self.setListCtrl.Append([str(self.setListCtrl.GetItemCount()), scene])

            setlistLen = self.setListCtrl.GetItemCount()
            for index in range(setlistLen):
                self.setListCtrl.SetStringItem(index, 0, str(index+1))

        self.RefreshData()



    def OnUp(self, event):
#        sel = self.setListBox.GetSelection()
#        if sel > 0:
#            text = self.setListBox.GetString(sel)
#            self.setListBox.Insert(text, sel-1)
#            self.setListBox.Delete(sel+1)
#            self.setListBox.Select(sel-1)

##
        sel = self.setListCtrl.GetFirstSelected()
        setlistLen = self.setListCtrl.GetItemCount()
        if sel > 0:
            item = self.setListCtrl.GetItem(sel, 1)
            text = item.GetText()
            index = self.setListCtrl.InsertStringItem(sel-1, str(sel))
            self.setListCtrl.SetStringItem(index, 1, text)
            self.setListCtrl.DeleteItem(sel+1)

            for index in range(setlistLen):
                self.setListCtrl.SetStringItem(index, 0, str(index+1))
            self.setListCtrl.Select(sel-1)  
##
        self.RefreshData()


    def OnDown(self, event):
#        sel = self.setListBox.GetSelection()
#        lbMaxIdx = self.setListBox.GetCount()-1
#        if sel != -1 and sel < lbMaxIdx:
#            text = self.setListBox.GetString(sel)
#            self.setListBox.Insert(text, sel+2)
#            self.setListBox.Delete(sel)
#            self.setListBox.Select(sel+1)

##
        sel = self.setListCtrl.GetFirstSelected()
        setlistLen = self.setListCtrl.GetItemCount()
        if sel != -1 and sel <  setlistLen-1:
            item = self.setListCtrl.GetItem(sel, 1)
            text = item.GetText()
            index = self.setListCtrl.InsertStringItem(sel+2, str(sel))
            self.setListCtrl.SetStringItem(index, 1, text)
            self.setListCtrl.DeleteItem(sel) 
    
            for index in range(setlistLen):
                self.setListCtrl.SetStringItem(index, 0, str(index+1))
            self.setListCtrl.Select(sel+1) 
##
        self.RefreshData()

    def OnDelete(self, event):
#        sel = self.setListBox.GetSelection()
#        if sel != -1:
#            self.setListBox.Delete(sel)
#            try:
#                self.setListBox.Select(sel)
#            except:
#                self.setListBox.Select(sel-1)

##
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
##
        self.RefreshData()

    def RefreshData(self):
#        self.setlist = self.setListBox.GetStrings()
                
#        self.data.setlist = {}
#        for pos,song in enumerate(self.setlist):
#            self.data.setlist[str(pos+1)] = song  
## 
        self.data.setlist = {}
        setlistLen = self.setListCtrl.GetItemCount() 
        for index in range(setlistLen):
            itemPos = self.setListCtrl.GetItem(index, 0)
            textPos = itemPos.GetText()
            itemScene = self.setListCtrl.GetItem(index, 1)
            textScene = itemScene.GetText()
            self.data.setlist[textPos] = textScene 

