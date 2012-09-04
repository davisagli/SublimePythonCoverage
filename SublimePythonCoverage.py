# bootstrap
import os
plugin_path = os.path.dirname(__file__)
if not os.path.exists(os.path.join(plugin_path, 'coverage')):
    # Fetch coverage.py
    print 'SublimePythonCoverage installing coverage.py.'

    from StringIO import StringIO
    import tarfile
    import urllib
    from hashlib import md5

    SOURCE = 'http://pypi.python.org/packages/source/c/coverage/coverage-3.5.2.tar.gz'
    MD5SUM = '28c43d41b13f8987ea14d7b1d4a4e3ec'

    payload = urllib.urlopen(SOURCE).read()
    if md5(payload).hexdigest() != MD5SUM:
        raise ImportError('Invalid checksum.')

    tar = tarfile.open(mode='r:gz', fileobj=StringIO(payload))
    for m in tar.getmembers():
        if not m.name.startswith('coverage-3.5.2/coverage/'):
            continue
        m.name = '/'.join(m.name.split('/')[2:])
        tar.extract(m, os.path.join(plugin_path, 'coverage'))

    print 'SublimePythonCoverage successfully installed coverage.py.'
# end bootstrap


import sublime
import sublime_plugin
from coverage import coverage
from coverage.files import FnmatchMatcher
PLUGIN_FILE = os.path.abspath(__file__)


def find(base, rel, access=os.R_OK):
    if not isinstance(rel, basestring):
        rel = os.path.join(*rel)
    while 1:
        path = os.path.join(base, rel)
        if os.access(path, access):
            return path
        baseprev = base
        base = os.path.dirname(base)
        if not base or base == baseprev:
            return


def find_cmd(base, cmd):
    return find(base, ('bin', cmd), os.X_OK)


def find_tests(fname):
    dirname = os.path.dirname(fname)
    init = os.path.join(dirname, '__init__.py')
    if not os.path.exists(init):
        # not a package; run tests for the file
        return fname

    setup = find(dirname, 'setup.py')
    if setup:
        # run tests for the whole distribution
        return os.path.dirname(setup)

    # run tests for the package
    return os.path.dirname(fname)


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

        # run analysis and find uncovered lines
        cov = coverage(data_file=cov_file)
        outlines = []
        omit_matcher = FnmatchMatcher(cov.omit)
        if not omit_matcher.match(fname):
            cov_dir = os.path.dirname(cov_file)
            os.chdir(cov_dir)
            relpath = os.path.relpath(fname, cov_dir)
            cov.load()
            f, s, excluded, missing, m = cov.analysis2(relpath)
            for line in missing:
                outlines.append(view.full_line(view.text_point(line - 1, 0)))

        # update highlighted regions
        view.erase_regions('SublimePythonCoverage')
        if outlines:
            view.add_regions('SublimePythonCoverage', outlines, 'comment',
                sublime.DRAW_EMPTY | sublime.DRAW_OUTLINED)


# manually import the module containing ST2's default build command,
# since it's in a module whose name is a Python keyword :-s
ExecCommand = __import__('exec').ExecCommand


class TestExecCommand(ExecCommand):
    """An generic extension of the default build system which shows coverage at the end."""

    runner = None

    def cmd(self, runner, testpath):
        NotImplemented

    def run(self, **kw):
        if 'cmd' not in kw:
            fname = self.window.active_view().file_name()

            # look for a virtualenv with nosetests, py.test etc
            runner = find_cmd(fname, self.runner)
            if runner is None:
                # no virtualenv; maybe there's a global one
                runner = self.runner

            testpath = find_tests(fname)
            if os.path.isdir(testpath):
                kw['working_dir'] = testpath
            else:
                kw['working_dir'] = os.path.dirname(testpath)

            kw['cmd'] = self.cmd(runner, testpath)

        super(TestExecCommand, self).run(**kw)

    def finish(self, proc):
        super(TestExecCommand, self).finish(proc)
        for view in self.window.views():
            view.run_command('show_python_coverage')


class NoseExecCommand(TestExecCommand):
    """An extension of the default build system using the Python Nose test
       runner to generate coverage information."""

    runner = 'nosetests'

    def cmd(self, runner, testpath):
        return [runner, '--with-coverage', testpath]


class PytestExecCommand(TestExecCommand):
    """An extension of the default build system using the py.test test
       runner to generate coverage information."""

    runner = 'py.test'

    def cmd(self, runner, testpath):
        return [runner]
