from subprocess import Popen, PIPE
import os
import sublime, sublime_plugin
import sys
from SublimePythonCoverage.utils import find, find_cmd


PLUGIN_FILE = os.path.abspath(__file__)


class SublimePythonCoverageListener(sublime_plugin.EventListener):
    """Event listener to highlight uncovered lines when a Python file is loaded."""

    def on_load(self, view):
        if 'source.python' not in view.scope_name(0):
            return

        view.run_command('show_python_coverage')


class ShowPythonCoverageCommand(sublime_plugin.TextCommand):
    """Highlight uncovered lines in the current file based on a previous coverage run."""

    def run(self, edit):
        view = self.view
        fname = view.file_name()
        if not fname:
            return

        cov_file = find(fname, '.coverage')
        if not cov_file:
            print 'Could not find .coverage file.'
            return

        python = find_cmd(PLUGIN_FILE, 'python')
        reader = find(PLUGIN_FILE, ('SublimePythonCoverage', 'read_coverage.py'))
        p = Popen([python, reader, cov_file, fname], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(None)
        print stdout, stderr

        outlines = []
        for line in stdout.splitlines():
            line = int(line)
            outlines.append(view.full_line(view.text_point(line - 1, 0)))
        view.erase_regions('SublimePythonCoverage')
        view.add_regions('SublimePythonCoverage', outlines, 'comment', 
            sublime.DRAW_EMPTY | sublime.DRAW_OUTLINED)


# manually import the module containing ST2's default build command,
# since it's in a module whose name is a Python keyword :-s
ExecCommand = __import__('exec').ExecCommand
class NoseExecCommand(ExecCommand):
    """An extension of the default build system which shows coverage at the end.

    Used by the Python Nose build system.
    """

    def finish(self, proc):
        super(NoseExecCommand, self).finish(proc)
        for view in self.window.views():
            view.run_command('show_python_coverage')


# TODO:
# - move read_coverage inline if possible
#   - coverage egg embedded or installed via helper script
# - refactor nose_runner to be part of NoseExecCommand
# - instructions on installation
# - documentation
