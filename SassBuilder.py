import sublime, sublime_plugin

import codecs
import json
import os
import stat
import re
import sys

from functools import partial
from threading import Thread
from subprocess import PIPE, Popen


SASS_EXTENSIONS = ('.scss', '.sass')


def which(executable):
    for path in os.environ['PATH'].split(os.pathsep):
        path = path.strip('"')

        fpath = os.path.join(path, executable)

        if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
            return fpath

    if os.name == 'nt' and not executable.endswith('.exe'):
        return which('{0}.exe'.format(executable))

    return None


def which_syspath(executable):
    for path in sys.path:
        fpath = os.path.join(path, executable)

        if os.path.isfile(fpath):
            if not os.access(fpath, os.X_OK):
                mode = os.stat(fpath).st_mode
                os.chmod(fpath, mode | stat.S_IEXEC)

            return fpath

    if os.name == 'nt' and not executable.endswith('.exe'):
        return which_syspath('{0}.exe'.format(executable))

    return executable


def path_info(path):
    root = os.path.dirname(path)
    name = os.path.splitext(os.path.basename(path))[0]
    extn = os.path.splitext(path)[1]

    return {'root': root, 'name': name, 'extn': extn, 'path': path}


def find_files(pattern, path):
    pattern = re.compile(pattern)
    found = []
    path = os.path.realpath(path)

    for root, dirnames, files in os.walk(path):
        for fname in files:
            if fname.endswith(SASS_EXTENSIONS):
                with codecs.open(os.path.join(root, fname), 'r', "utf-8") as f:
                    if any(pattern.search(line) for line in f):
                        found.append(os.path.join(root, fname))
                        break

    return found


def grep_files(pattern, path):
    path = os.path.realpath(path)
    grep = '''grep -E "{0}" * -lr'''.format(pattern)

    proc = Popen(grep, shell=True, cwd=path, stdout=PIPE, stderr=PIPE)

    out, err = proc.communicate()

    if err:
        print(err)
        sublime.error_message('SassBuilder: Hit \'ctrl+`\' to see errors.')

    if not out:
        return None

    out = out.decode('utf8')
    found = []
    for f in out.split():
        if f.endswith(SASS_EXTENSIONS):
            found.append(os.path.join(path, f))

    return found


def get_partial_files(info, project_path):
    pattern = '''@import.*{0}'''.format(info['name'][1:])

    if which('grep'):
        return grep_files(pattern, project_path)

    return find_files(pattern, project_path)


def get_files(info, project_path):
    if info['name'].startswith('_'):
        return get_partial_files(info, project_path)
    return [info['path']]


def load_settings(project_path):
    try:
        with open(os.sep.join([project_path, '.sassbuilder-config.json']), 'r') as f:
            data = f.read()
        return json.loads(data)
    except:
        return None


def defaultFlags(compiler):
    if compiler.endswith('sass'):
        return ['--stop-on-error', '--trace']
    elif compiler.endswith('sassc'):
        return []
    else:
        sublime.error_message("{0} is not a valid compiler option".format(compiler))


def toFlags(options):
    flags = []
    for key, value in options.items():
        if value is True:
            flags.append('--{0}'.format(key))
        elif value is not False:
            flags.append('--{0}={1}'.format(key, value))

    return flags


def compile_sass(files, settings):
    compiled_files = []
    for f in files:
        info = path_info(f)
        input = info['path']

        srcPath = os.path.join(info['root'], settings['output_path'])
        outputName = '.'.join([info['name'], 'css'])

        output = os.path.join(srcPath, outputName)

        compiler = which_syspath(settings.get('compiler', 'sass'))

        flags = defaultFlags(compiler) + toFlags(settings['options'])

        command = '{compiler} {flags} {input} {output}'.format(
                compiler=compiler, flags=' '.join(flags), input=input, output=output)
        print(command)

        sass = Popen(command, shell=True, cwd=info['root'], stdout=PIPE, stderr=PIPE)

        out, err = sass.communicate()
        if out:
            compiled_files.append(outputName)

        if err:
            print(err)
            sublime.error_message('SassBuilder: Hit \'ctrl+`\' to see errors.')
            return

    print('{0} has been compiled.'.format(', '.join(compiled_files)))


class SassBuilderCommand(sublime_plugin.EventListener):

    def on_post_save(self, view):
        info = path_info(view.file_name())
        settings = load_settings(info['root'])

        if not settings:
            return None

        if info['extn'] in SASS_EXTENSIONS:
            print('SassBuilder started.')
            files = get_files(info, settings['project_path'])

            #t = Thread(target=compile_sass, args=(files, settings))
            #t.start()
            compile_sass(files, settings)
