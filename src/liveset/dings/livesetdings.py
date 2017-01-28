#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mididings import *
from mididings.extra.osc import OSCInterface
import mididings.engine as engine
from liveset.livesetconf import *
from liveset.utils.files import *

import json
import time

def Run(filePath):

    hook(OSCInterface(56418, 56419))

    with open(settings_file) as data_file:
        settings = json.load(data_file)
    midiOutPort = settings["midiOutPort"]
    midiInPort = settings["midiInPort"]
    sceneswitchCC = settings["nextSceneCC"]
    subsceneswitchCC = settings["nextSubsceneCC"]  

    config(
       in_ports = [('in',str(midiInPort))], 
       out_ports = [('out',str(midiOutPort))],
	start_delay=0.5
    )

    # default values
    out_port = 'out'

    scenes_dict = {}


    data = Data()
    data.Open(filePath)


    for scene in data.scenes:
        subscenes = []
        for subscene in data.scenes[scene]:
            for key in subscene:
                patch = []             
                for part in subscene[key]:
		    patch.append([
    		        Ctrl(out_port, part["CH"], 0, part["CC0"]),
		        Ctrl(out_port, part["CH"], 32, part["CC32"]), 
	    	        Program(out_port, part["CH"], part["PC"])
		        ])
                if key != "--":
                    subscenes.append(Scene(str(key), Pass(), patch))
        ## if subscenes is empty, add a Scene
        if not subscenes:
            scenes_dict[str(scene)] = Scene(str(scene), Pass(), patch)
        else:
            scenes_dict[str(scene)] = SceneGroup(str(scene), subscenes)


    # Controller for subscene switch
    control = [CtrlFilter(sceneswitchCC) >> CtrlValueFilter(127) >> SceneSwitch(offset=1),
		CtrlFilter(subsceneswitchCC) >> CtrlValueFilter(127) >> SubSceneSwitch(offset=1)]
    pre = ~CtrlFilter(sceneswitchCC) >> ~CtrlFilter(subsceneswitchCC)

    # scenes ordered according setlist
    scenes = {}

    for pos in data.setlist:
        scenes[int(pos)] = scenes_dict[data.setlist[pos]]

    run(
        scenes = scenes,
        control = control,
        pre = pre
    )


def switchModed():
    time.sleep(1)
    last_switchMode = None
    while engine.active():
        scenes = engine.scenes()
        currentScene = engine.current_scene()
        currentSubscene = engine.current_subscene()
        subsceneLen = len(scenes[currentScene][1])
        if currentSubscene <= subsceneLen - 1:
            switchMode = "switchsubscene"
        else:
            switchMode = "switchscene"
  
        if switchMode != last_switchMode: 
            with open(switchmode_file, 'w') as switchModeFile:
                switchModeFile.write(switchMode)
            last_switchMode = switchMode
        time.sleep(0.5) 