"""Manual installation of coverage package."""

from StringIO import StringIO
import sys
import tarfile
import urllib
from hashlib import md5

SOURCE = 'http://pypi.python.org/packages/source/c/coverage/coverage-3.5.1.tar.gz'
MD5SUM = '410d4c8155a4dab222f2bc51212d4a24'

if __name__ == '__main__':
	if len(sys.argv) != 2 or sys.argv[1] != 'install':
		print 'Usage: setup.py install'
		sys.exit()

	payload = urllib.urlopen(SOURCE).read()
	if md5(payload).hexdigest() != MD5SUM:
		raise ValueError('Invalid checksum.')

	tar = tarfile.open(mode='r:gz', fileobj=StringIO(payload))
	for m in tar.getmembers():
		if not m.name.startswith('coverage-3.5.1/coverage/'):
			continue
		m.name = '/'.join(m.name.split('/')[2:])
		tar.extract(m, 'coverage')

	print 'coverage successfully installed.'
