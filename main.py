import json
import os
import server
import tools


def create_json(path, opt):
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(tools.cdumps(opt))
            return

    with open(path, 'r') as f:
        _j = json.loads(f.read())
        _keys = _j.keys()
        for key, value in zip(opt.keys(), opt.values()):
             if key not in _keys:
                 _j[key] = value
        with open(path, 'w') as f:
            f.write(tools.cdumps(_j))

def get_json(path, key, default):
    if not os.path.isfile(path):
        return default

    with open(path, 'r') as f:
        _j = json.load(f)
        return _j.get(key, default)

def create_optimize(opt):
    create_json('app-optimize.json', opt)

def get_optimize(key, default=None):
    return get_json("app-optimize.json", key, default)

def create_data(opt):
    create_json("app-data.json", opt)

def get_data(key, default=None):
    return get_json("app-data.json", key, default)


if __name__ == "__main__":
    create_optimize({
        "browser":"edge",
        "theme":"dark|light",
        "color":"rgb(204, 240, 230)",
        "f_lang":"python",
        "app_lang":"en",
        "port": 4000,
        "projects_meta_dir": ".projects",
        "projects_path": "{lang}_projects"
    })

    create_data({
        "languages": {
            "python": {
                "name": "Python",
                "ext": ".py",
                "single-comment": "# {line}",
                "multi-comments": "'''{lines}'''",
                "start_arguments": "py {file}",
                "run_argument": "py -m {project_name}",
                "project": {
                    "__init__.py": "import {project_name}",
                    "{project_name}.py": "print('Language created by script view automatically')"
                }
            },
            "node-javascript": {
                "name": "Node.js",
                "ext": ".js",
                "single-comment": "// {line}",
                "multi-comments": "/*{lines}*/",
                "start_arguments": "node {file}",
                "run_argument": "node {project_name}/{project_name}.js",
                "project": {
                    "{project_name}.js": ""
                }
            },
            "html-5": {
                "name": "Html 5",
                "ext": ".html",
                "multi-comments": "<!--{lines}-->",
                "start_arguments": "edge {file}",
                "run_argument": "{project_path}/index.html",
                "project": {
                    "index.html": ""
                }
            }
        }
    })

    server.eel._start_args["host"] = "localhost"
    server.eel._start_args["port"] = get_optimize("port", 4000)
    is_started, port = server.start(get_optimize('browser'))
    if is_started:
        print(f"Server started on 'http://localhost:{port}/index.html'")
    while is_started:
        server.eel.sleep(1)
