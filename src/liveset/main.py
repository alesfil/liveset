# -*- coding: utf-8 -*-

import os
import wx
from gui.mainwindow import MainWindow
from liveset.livesetconf import *

if not os.path.exists(config_dir):
    os.mkdir(config_dir)

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

def main():
    app = wx.App(False)
    window = MainWindow(None, title='LiveSet')
    app.MainLoop()
