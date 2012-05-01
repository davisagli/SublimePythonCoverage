import os


def find(base, rel, access=os.R_OK):
    if not isinstance(rel, basestring):
        rel = os.path.join(*rel)
    while 1:
        path = os.path.join(base, rel)
        if os.access(path, access):
            return path
        base = os.path.dirname(base)
        if not base or base == '/':
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
