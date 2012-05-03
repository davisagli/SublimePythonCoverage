``SublimePythonCoverage`` is a plugin for Sublime Text 2
that can highlight lines of Python lacking test coverage,
based on the output of Ned Batchelder's
`coverage.py <http://nedbatchelder.com/code/coverage/>`_.

Installation
------------

1. Use git to check out ``SublimePythonCoverage``
   into your Sublime Text 2 ``Packages`` directory.

   On OS X::

     $ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
     $ git clone git://github.com/davisagli/SublimePythonCoverage.git

2. Install our dependency, ``coverage.py``::

     $ cd SublimePythonCoverage
     $ python setup.py install

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
`nose <http://readthedocs.org/docs/nose/en/latest/>`_ test runner,
SublimePythonCoverage also comes with a *build system*
to help produce coverage information.

Set your build system to ``Python Nose with Coverage``.

Now when you trigger a build in Sublime Text 2,
it will run ``nosetests --with-coverage`` to generate
coverage data, and then update the highlighted lines.

SublimePythonCoverage uses a simple heuristic
to guess the right ``nosetests`` script to run.
First it looks in all parent directories for ``bin/nosetests``.
If that fails, it tries to find nosetests in the PATH.

SublimePythonCoverage uses another heuristic
to guess what path to pass to nosetests.
If the directory of the current file is not a package,
(i.e., does not contain an ``__init__.py``),
it runs nosetests on the current file.
Otherwise, it looks in all parent directories for ``setup.py``,
and if it finds it it runs nosetests on that directory.
If not, it runs nosetests on the directory of the current file.
