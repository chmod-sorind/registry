import _winreg

def getMDACversion():

    # Open the key and return the handle object.
    hKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                          "Software\\Microsoft\\DataAccess")

    # Read the value.
    result = _winreg.QueryValueEx(hKey, "FullInstallVer")

    # Close the handle object.
    _winreg.CloseKey(hKey)

    # Return only the value from the resulting tuple (value, type_as_int).
    return result[0]


print getMDACversion()