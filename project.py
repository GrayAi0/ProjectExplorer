import json
import os
import main
import tools


def GetLangInfo(lang):
    langinfo = main.get_data("languages", {}).get(lang, {})
    return langinfo

def create_projects_meta_file(project_name, project_description, project_language, project_path):
    projects_meta_dir = main.get_optimize('projects_meta_dir', '.projects')
    project_meta_file = os.path.join(projects_meta_dir, f"{project_name}.json")
    if not os.path.isdir(projects_meta_dir):
        os.mkdir(projects_meta_dir)

    if os.path.isfile(project_meta_file):
       return False

    with open(project_meta_file, 'w') as f:
        f.write(tools.cdumps({
            "project_path":project_path,
            "project_name":project_name,
            "project_description":project_description,
            "project_language":project_language,
        }))
    return True


def create_dirs(*paths):
    for path in paths:
        print(path)
        path = path.replace('\\', '/')
        if path.find('/') > -1:
            fullpath = './'
            for path in path.split('/'):
                fullpath += f'{path}/'
                if not os.path.isdir(fullpath):
                    os.mkdir(fullpath)
        else:
            if not os.path.isdir(path):
                os.mkdir(path)


def create_main_files(project_path, project_name, language_info):
    project_files = language_info.get('project', {})
    for key, value in zip(project_files.keys(), project_files.values()):
        with open(f"{project_path}/{key.replace('{project_name}', project_name)}", 'w') as f:
            value = value.replace('{project_name}', project_name)
            f.write(add_comment(language_info, "this file created by script view", "", "you can run this project from application", ""))
            f.write(value)

def add_comment(language_info, *lines):
    single_commant = language_info.get("single-comment")
    multi_commant = language_info.get("multi-comment")
    if single_commant == None and multi_commant == None:
        return ""

    if len(lines) > 1:
        if multi_commant:
            _lines = '\n'
            for line in lines:
                _lines += f"{line}\n"
            return multi_commant.replace("{lines}", _lines, 1)
        elif single_commant:
            _lines = ''
            for line in lines:
                _lines += f"{single_commant.replace('{line}', line)}\n"
            return _lines
    else:
        if single_commant:
            _lines = ''
            for line in lines:
                _lines += f"{single_commant.replace('{line}', line)}\n"
            return _lines
    return ""

def add_project_to_path(project_name, project_description, project_language):
    project_language_info = main.get_data('languages', {}).get(project_language, project_language)
    projects_path = main.get_optimize('projects_path', '{lang}_projects').replace('{lang}', project_language, 1)
    project_path = f"{projects_path}/{project_name.replace(' ', '_')}"
    create_dirs(project_path)
    create_main_files(project_path, project_name, project_language_info)
    return create_projects_meta_file(project_name, project_description, project_language, project_path)


def GetAllProjects():
    projects_meta_dir = main.get_optimize('projects_meta_dir', '.projects')
    if not os.path.isdir(projects_meta_dir):
        return []

    projects_files = [f for f in os.listdir(projects_meta_dir) if f.endswith('.json')]
    projects = []
    for fn in projects_files:
        file = os.path.join(projects_meta_dir, fn)
        if not os.path.isfile(file):
            continue

        with open(file, 'r') as f:
            _json = json.load(f)
            _json['is_runnable'] = main.get_data("languages", {}).get(_json['project_language'], {}).get('run_argument', None) != None
            _json['is_startable'] = main.get_data("languages", {}).get(_json['project_language'], {}).get('start_arguments', None) != None
            if _json.get('is_startable'):
                _json["start_files"] = [f for f in [_f for _, _, f in os.walk(_json.get("project_path")) for _f in f] if f.endswith(GetLangInfo(_json.get("project_language")).get('ext', ''))]
            projects.append(_json)

    return projects

