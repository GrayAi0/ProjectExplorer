import json
import os
import threading


def GetListOfDir(dir):
    for path, folders, _files in os.walk(dir):
        for file in _files:
            yield os.path.join(path, file)

def ForgetThread(func, args=[]):
    threading.Thread(target=func, args=args).start()


def GetFullPath(_for):
    return str(os.path.abspath(_for))


def getPath(_for):
    pa = GetFullPath(_for)

    if pa.find(' ') > -1:
        pa = f'"{pa}"'

    lpa = '\\'.join(pa.split('\\')[:-1])

    return lpa

def IsEmptyOrSpaces(s):
    if s == '':
        return True
    for _s in s:
        if _s != ' ':
            return False

    return True

def cdumps(_j):
    return json.dumps(_j, sort_keys=True, indent=4, separators=(', \n', ': '), ensure_ascii=False)
