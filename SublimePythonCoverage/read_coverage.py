"""Helper to run coverage analysis and list uncovered lines.

Usage: python read_coverage.py coverage_file file_under_test
"""

import os
import sys
from coverage import coverage


if __name__ == '__main__':
    cov_file, fname = sys.argv[1:]
    cov = coverage(data_file=cov_file)
    cov_dir = os.path.dirname(cov_file)
    os.chdir(cov_dir)
    relpath = os.path.relpath(fname, cov_dir)
    cov.load()
    f, s, excluded, missing, m = cov.analysis2(relpath)
    for m in missing:
        print m
