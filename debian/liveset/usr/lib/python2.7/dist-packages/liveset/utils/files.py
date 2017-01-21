# -*- coding: utf-8 -*-

import json
from liveset.livesetconf import *

class Data():
    def __init__(self):
        self.project = {}
        self.project["Scenes"] = {}
        self.project["Setlist"] = {}
        self.scenes = self.project["Scenes"]
        self.setlist = self.project["Setlist"]

    def Open(self, filePath):
        try:
            with open(filePath) as dataFile:
                self.project = json.load(dataFile)
            self.scenes = self.project["Scenes"]
            self.setlist = self.project["Setlist"]
            self.scenesName = self.scenes.keys()
            self.scenesName.sort()
        except:
            self.scenesName = []

    def Save(self, filePath):     
        with open(filePath, 'w') as outFile:
            json.dump(self.project, outFile, sort_keys = True, indent = 4, ensure_ascii = False)        