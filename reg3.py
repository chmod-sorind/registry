from _winreg import *

def get_guid_by_name(name):
    # Open the uninstaller key
    with OpenKey(HKEY_LOCAL_MACHINE, r'Software\Microsoft\Windows\CurrentVersion\Uninstall') as key:
        # We only care about subkeys of the installer key
        subkeys, _, _ = QueryInfoKey(key)
        for i in range(subkeys):
            subkey = EnumKey(key, i)
            # Since we're looking for uninstallers for MSI products,
            # the key name will always be the GUID. We assume that any
            # key starting with '{' and ending with '}' is a GUID, but
            # if not the name won't match.
            if subkey[0] != '{' or subkey[-1] != '}':
                 continue
            # Query the display name or other property of the key to
            # see if it's the one we want
            with OpenKey(key, subkey) as _subkey:
                if QueryValueEx(_subkey, 'DisplayName')[1] == name:
                    return subkey
                    return None

get_guid_by_name("EpsonNet Print")