import os
import threading
from time import sleep
import psutil
import subprocess

running_console = {'0': {}}


def CreateConsole(project_info, obj):
    _max = max(running_console)
    cid = (int(_max) if str(_max).isdigit() else 0) + 1
    running_console[str(cid)] = {
        "project": project_info,
        "class": obj,
        "lastoutput": ""
    }
    return cid

class Console:
    def __init__(self, project_info, arguments):
        self.cid = CreateConsole(project_info, self)
        self.exec_arguments = arguments
        self.is_running = False
        self.Thread = None
        self.stdout = ""
        self.process = None
    def read_sync(self, read, is_error = False):
        while self.is_running:
            line = read.readline() # 1kb
            if not line:
                continue
            line = line.decode('utf8').replace('<', '&lt;')
            line = line.replace('>', '&gt;')
            if is_error:
                self.stdout += f"<font color=red>{line}</font>"
            else:
                self.stdout += f"{line}"

    def _exec_sync(self):
        process = subprocess.Popen(self.exec_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.process = process
        threading.Thread(target=self.read_sync, args=(process.stderr, True)).start()
        threading.Thread(target=self.read_sync, args=(process.stdout,)).start()
        process.wait()
        self.do_stopstaff()
    def exec(self):
        self.stdout = ""
        if self.is_running:
            return
        self.Thread = threading.Thread(target=self._exec_sync)
        self.Thread.start()
        self.is_running = True

    def output(self):
        return self.stdout

    def do_stopstaff(self):
        self.is_running = False
        self.stdout += f"\n\nProcess finished with exit code {self.process.returncode or 'unknown'}"

    def force_stop(self):
        if not self.is_running:
            return
        pid = self.process.pid
        for process in psutil.process_iter():
            if process.pid == pid:
                while self.is_running:
                    try:
                        process.kill()
                    except :
                        pass