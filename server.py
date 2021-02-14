import json
import os
import shutil

import eel

import console
import main
import project
import tools

@eel.expose
def GetProjects():
    return project.GetAllProjects()

@eel.expose
def GetAvailableLanguages():
    languages_data = main.get_data("languages", {})
    languages = {}
    for key, value in zip(languages_data.keys(), languages_data.values()):
        languages[key] = {
            'key':key,
            'name':value.get('name', key),
            'ext': value.get('ext', False),
        }
    return languages

@eel.expose
def CreateProject(name, description, lang):
    if tools.IsEmptyOrSpaces(name):
        return "Project name required"
    elif tools.IsEmptyOrSpaces(lang):
        return "Chose language first"

    return "Project created" if project.add_project_to_path(name, description, lang) else "Project is already exists"

@eel.expose
def CreateConsole(proj_name, is_start, file=None):
    proj_path = os.path.join(main.get_optimize('projects_meta_dir'), f"{proj_name}.json")
    if not os.path.isfile(proj_path):
        print("Project not exists")
        return False
    with open(proj_path, 'r') as f:
        project_info = json.load(f)
        langinfo = project.GetLangInfo(project_info.get("project_language", ""))
        if is_start:
            start_arg = langinfo.get('start_arguments', '')
            if start_arg == '':
                print("start_arguments is empty")
                return False
            start_arg = start_arg.replace('{project_path}', project_info.get('project_path', "")).replace("{project_name}", project_info.get('project_name', "")).replace('file', file)
        else:

            start_arg = str(langinfo.get('run_argument', ''))
            if start_arg == '':
                print("run_argument is empty")
                return False
            start_arg = start_arg\
                .replace('{project_path}', project_info.get('project_path', ""))\
                .replace("{project_name}", project_info.get('project_name', ""))

        _console = console.Console(project_info, f"cd /d {tools.getPath(project_info.get('project_path'))} && {start_arg}")

    return _console.cid

@eel.expose
def DestroyConsole(cid):
    _console = console.running_console.get(cid, {}).get('class', False)
    if _console:
        if _console.is_running:
            _console.force_stop()
        console.running_console.pop(cid)


@eel.expose
def GetConsole(cid):
    _console = console.running_console.get(cid, {})
    return _console

@eel.expose
def ExecuteConsole(cid):
    _console = console.running_console.get(cid, {}).get('class', False)
    if _console:
        _console.exec()
        return True
    else:
        return False

@eel.expose
def StopConsole(cid):
    _console = console.running_console.get(cid, {}).get('class', False)

    if _console:
        _console.force_stop()
        return True
    else:
        return False
@eel.expose
def GetConsoleStatus(cid):
    _console = console.running_console.get(cid, {}).get('class', False)

    if _console:
        return _console.is_running
    else:
        return None


@eel.expose
def GetOutput(cid):
    _console = console.running_console.get(cid, {}).get('class', False)
    lastoutput = console.running_console.get(cid, {}).get('lastoutput', '')

    if _console:
        output = _console.output()
        if output == lastoutput:
            return [False, output.replace('\n', '<br>')]
        console.running_console[cid]['lastoutput'] = output
        return [True, output.replace('\n', '<br>')]
    else:
        return None

@eel.expose
def OpenProject(proj_name):
    proj_path = os.path.join(main.get_optimize('projects_meta_dir'), f"{proj_name}.json")
    if not os.path.isfile(proj_path):
        return False
    with open(proj_path, 'r') as f:
        proj = json.load(f)
        f_editor = proj.get('f_editor', 'code')
        proj_path = proj.get('project_path', False)
        if not proj_path:
            return False
        tools.ForgetThread(os.system, args=[f"{f_editor} {proj_path}"])

    return True


@eel.expose
def OpenFolder(proj_name):
    proj_path = os.path.join(main.get_optimize('projects_meta_dir'), f"{proj_name}.json")
    if not os.path.isfile(proj_path):
        return False
    with open(proj_path, 'r') as f:
        proj = json.load(f)
        proj_path = proj.get('project_path', False)
        if not proj_path:
            return False
        tools.ForgetThread(os.system, args=[f"explorer {os.path.abspath(proj_path)}"])

    return True


@eel.expose
def DeleteProject(proj_name):
    proj_meta_path = os.path.join(main.get_optimize('projects_meta_dir'), f"{proj_name}.json")
    if not os.path.isfile(proj_meta_path):
        return False

    with open(proj_meta_path, 'r') as f:
        proj = json.load(f)
        proj_path = proj.get('project_path', False)
        if not proj_path:
            return False

        proj_path = tools.GetFullPath(proj_path)
        if not proj_path:
            return False

    os.remove(proj_meta_path)
    shutil.rmtree(proj_path)
    if not os.path.isfile(proj_meta_path) and not os.path.isdir(proj_path):
        return True
    else:
        return False



@eel.expose
def IsDarkMode():
    return True if main.get_optimize('theme', 'dark') == 'dark' else False

@eel.expose
def GetAllScriptsFromProject(proj_name):
    proj_meta_path = os.path.join(main.get_optimize('projects_meta_dir'), f"{proj_name}.json")
    if not os.path.isfile(proj_meta_path):
        return False

    with open(proj_meta_path, 'r') as f:
        proj = json.load(f)
        proj_path = proj.get('project_path', False)
        if not proj_path:
            return proj_path

        files = []
        project_name = proj_path.replace('\\', '/').split('/')[-1]
        for index, file in enumerate(tools.GetListOfDir(proj_path)):
            file = file.replace('\\', '/')
            splited = file.split('/')
            _file = None
            for nindex, name in enumerate(splited):
                if name == project_name:
                    short_path = '/'.join(splited[nindex-1:-1])
                    with open(file, 'r', encoding='utf8') as f:
                        try:
                            text = f.read()
                        except:
                            text = "cannot read this file"
                        _file = {
                            'file': file,
                            'short': f'<font color=gray size=3px>{short_path}/</font>{file.split("/")[-1]}',
                            'index': index,
                            'lang': os.path.splitext(file)[1].split('.')[-1],
                            'oldtext':text,
                            'text': text
                        }
            if _file == None:
                with open(file, 'r', encoding='utf8') as f:
                    try:
                        text = f.read()
                    except :
                        text = "cannot read this file"
                    _file = {
                        'file': file,
                        'short': f'<font color=gray size=3px>/</font>{file.split("/")[-1]}',
                        'index': index,
                        'oldtext': text,
                        'lang': os.path.splitext(file)[1].split('.')[-1],
                        'text': text
                    }

            files.append(_file)
        return files


@eel.expose
def saveFile(file, newtext):
    if os.path.isfile(file):
        with open(file, 'w', encoding='utf8') as f:
            f.write(newtext)

def start(browser:str = '', block:bool = False) -> (bool, int):
    eel.init('web')
    eel._start_args['mode'] = browser
    eel.start('index.html', block=block)
    return True, eel._start_args['port']