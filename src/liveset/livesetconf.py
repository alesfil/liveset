# -*- coding: utf-8 -*-

import os

home = os.getenv("HOME")
prog_name = "liveset" 

xdg_config_home = os.path.join(home,".config") 
xdg_data_home = os.path.join(home,".local","share")
xdg_cache_home =  os.path.join(home,".cache")

config_dir = os.path.join(xdg_config_home, prog_name )
data_dir = os.path.join(xdg_data_home, prog_name)
cache_dir = os.path.join(xdg_cache_home, prog_name)

if not os.path.exists(config_dir):
    os.makedirs(config_dir)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

settings_file = os.path.join(config_dir, "settings.json")
switchmode_file = os.path.join(cache_dir,"switchMode")
usbswitchlock_file = os.path.join(cache_dir,"usbswitchLock")
scenes_file = os.path.join(data_dir, "scenes.json")
