``SublimePythonCoverage`` is a plugin for Sublime Text 2
that can highlight lines of Python lacking test coverage,
based on the output of Ned Batchelder's
`coverage.py <http://nedbatchelder.com/code/coverage/>`_.

Installation
------------

Set up
`Sublime Package Control <http://wbond.net/sublime_packages/package_control>`_
if you don't have it yet.

Go to Tools > Command Palette.
Type ``Package Control: Install Package`` and hit enter.
Type ``Python Coverage`` and hit enter.
It may take a bit to install as it needs to fetch its dependency, coverage.py.

Usage
-----

Highlighting lines missing coverage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you open a .py file,
SublimePythonCoverage tries to find coverage information
and highlight all uncovered lines with an outline.

It does this by looking in all parent directories
until it finds a ``.coverage`` file as produced by ``coverage.py``.
Obviously, it only works if that file exists
and contains coverage information for the .py file you opened.

You can force a reload of the coverage information
and redraw of the outlines
by running the ``show_python_coverage`` command,
bound to super+shift+c by default.

Running tests with coverage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you run your tests using the
`nose <http://readthedocs.org/docs/nose/en/latest/>`_ or
`pytest <http://pytest.org/>`_ test runners,
SublimePythonCoverage also comes with matching *build systems*
to help produce coverage information.

Set your build system to either ``Python Nose with Coverage``
or ``Python pytest with Coverage``.

Now when you trigger a build in Sublime Text 2,
it will run ``nosetests --with-coverage`` or ``py.test`` to generate
coverage data, and then update the highlighted lines.  In the
latter case, your `setup.cfg` or `pytest.ini` is expected to
provide the options necessary to test your package and generate
coverage information.

SublimePythonCoverage uses a simple heuristic
to guess the right ``nosetests``/``py.test`` script to run.
First it looks in all parent directories for ``bin/nosetests``/``bin/py.test``.
If that fails, it tries to find ``nosetests``/``py.test`` in the PATH.

SublimePythonCoverage uses another heuristic
to guess what path to pass to ``nosetests``.
If the directory of the current file is not a package,
(i.e., does not contain an ``__init__.py``),
it runs ``nosetests`` on the current file.  This does not work for ``py.test``.

Otherwise, it looks in all parent directories for ``setup.py``,
and if it finds it it starts the test runner on that directory.
If not, it runs the tests on the directory of the current file.
