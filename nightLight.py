# -*- coding: utf-8 -*-

"""
Toggle nightlight and change color temperature in Ubuntu 18.10.
"""

from albertv0 import *
from shutil import which
import subprocess
import json

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Nightlight Ubuntu 18.10"
__version__ = "1.2"
__trigger__ = "night "
__author__ = "David Britt"
__dependencies__ = []
iconPath = ":python_module"

if not which('gsettings'):
    raise Exception("`gsettings` is not in $PATH")

def handleQuery(query):
    results = []
    if query.isTriggered:

        stripped = query.string.strip()
        nightLightStatus = subprocess.check_output(gsettings_status('get')).decode('utf-8').strip()        
        color_status = subprocess.check_output(gsettings_color('get')).decode('utf-8').strip()

        results.append(Item(
            id=__prettyname__,
            icon=iconPath,
            text="Night Light: {}".format("ON" if json.loads(nightLightStatus) else "OFF"),
            subtext="night <1000 - 9000> To change color temperature.",
            actions=[
                ProcAction("Turn {}".format("OFF" if json.loads(nightLightStatus) else "ON"), 
                    gsettings_status('set', 'false' if json.loads(nightLightStatus) else 'true'))
            ]
        ))

        if stripped.isdigit() and 1000 <= int(stripped) <= 9000:
            results.append(Item(
                id=__prettyname__,
                icon=iconPath,
                text="Change color temperature to: {}".format(stripped),
                subtext="Current: {}".format(color_status.strip().split()[1]),
                actions=[ProcAction("Change temperature to: {}".format(stripped), gsettings_color('set', stripped))]
            ))               

    return results

# get set needs to be string; {'get', 'set'} for the following two functions.
def gsettings_status(getset, toggle=None):
    gsettings = ['gsettings', getset, 'org.gnome.settings-daemon.plugins.color', 'night-light-enabled']
    if toggle is not None:
        gsettings.append(toggle)
    return gsettings

def gsettings_color(getset, color_temp=None):
    gsettings = ['gsettings', getset, 'org.gnome.settings-daemon.plugins.color', 'night-light-temperature']
    if color_temp is not None:
        gsettings.append(color_temp)
    return gsettings
