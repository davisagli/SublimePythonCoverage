"""Helper to run nosetests appropriately for a given file.

If the file is in a Python package, nosetests is run for the package.
Otherwise it is run for the file.

Usage: python nose_runner.py file_under_test
"""
import os
from subprocess import Popen
import sys
from utils import find_cmd, find_tests


if __name__ == '__main__':
    fname = sys.argv[1]
    dirname = os.path.dirname(fname)

    # look for a virtualenv with nosetests
    nose = find_cmd(fname, 'nosetests')
    if nose is None:
        nose = find_cmd(__file__, 'nosetests')
    if nose is None:
        print 'Could not find nose.'
        sys.exit()

    testpath = find_tests(fname)
    if os.path.isdir(testpath):
        os.chdir(testpath)
    else:
        os.chdir(os.path.dirname(testpath))
    p = Popen([nose, '--with-coverage', testpath])
    sys.exit(p.wait())
