import _winreg
import sys
import os
import time
import datetime
import logging

start_time = time.time()

AppData = os.environ["APPDATA"]
log = (AppData + '\\' + 'BroadSignLogs\\BroadSignUninstaller.log')
logging.basicConfig(level=logging.DEBUG, filename=log, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('=' * 220)

try:
    arg = sys.argv[0]
    arg1 = sys.argv[1]
    if arg1 == 'bsa':
        arg1 = 'BroadSign Administrator'
    elif arg1 == 'bsp':
        arg1 = 'BroadSign Player'
    elif arg1 == 'bses':
        arg1 = "BroadSign Edge Server"
except IndexError:
    pass

def get_uninstallString(matchValue):
    regHive = _winreg.HKEY_LOCAL_MACHINE
    regKey = r'Software\Microsoft\Windows\CurrentVersion\Uninstall'
    regRights = _winreg.KEY_READ
    regOpen = _winreg.OpenKey
    regClose = _winreg.CloseKey
    subKey = regOpen(regHive, regKey, regRights)

    for x in xrange(0, _winreg.QueryInfoKey(subKey)[0] -1):
        subKey2 =  _winreg.EnumKey(subKey, x)
        if "{" not in subKey2:
           continue
        subKey3 = regOpen(regHive, regKey + '\\' + subKey2, regRights)
        for y in range(0, _winreg.QueryInfoKey(subKey3)[1]):
            name, value, key_type = _winreg.EnumValue(subKey3, y)
            if name == "DisplayVersion":
                displayVersion = value
            if "DisplayName" not in name:
                continue
            if value == matchValue:
                return subKey2, displayVersion
        regClose(subKey3)
    regClose(subKey)

def kill_process(process):
    if process == 'BroadSign Player':
        os.system('taskkill /f /im bspsh.exe')
        os.system('taskkill /f /im bsp.exe')
    elif process == 'BroadSign Administrator':
        os.system('taskkill /f /im bsa.exe')
    elif process == 'BroadSign Edge Server':
        os.system('taskkill /f /im bses.exe')


try:
    prodCode, version = get_uninstallString(arg1)
    prodName = arg1.replace (" ", "_")
    logLocation = (AppData + '\\' + 'BroadSignLogs\\' + prodName + '\\')
    timeStamp = '{:%Y-%b-%d_%H.%M.%S}'.format(datetime.datetime.now())
    logFile = logLocation + prodName + "_" + version + "_" + timeStamp + ".log"
    if not os.path.exists(logLocation):
        os.makedirs(logLocation)
    uninstallString = "msiexec.exe /x " + prodCode + " /qn /L*V " + logFile
    kill_process(arg1)
    os.system(uninstallString)
    print arg1, version, "was successfully uninstalled. Uninstall log " + logFile + " was created."
    logging.info(arg1 + " " + version + " was successfully uninstalled. Uninstall log " + logFile + " was created.")
except NameError:
    print "Use " + arg + " with on of the following arguments.\n bsa for BroadSign Administrator\n bsp for BroadSign Player\n bses for BroadSign Edge Server."
    logging.info("Use " + arg + " with arguments.")
except TypeError:
    print "Cannot find", arg1, "on this machine"
    logging.info("Cannot find " + arg1 + " on this machine")
print("--- %s milliseconds ---" %(time.time() - start_time))
logging.info("--- %s milliseconds ---" %(time.time() - start_time))
logging.info('=' * 220 + '\n')