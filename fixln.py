#! /usr/bin/env python
"Check symlinks to songs"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2018, Paresh Adhia"

from pathlib import Path
import logging

libs = []

def main():
	"script entry-point"
	import argparse

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('path', nargs='*', default=[Path.cwd()], type=Path, help='directories to fix')
	parser.add_argument('--libpath', default=(Path.home() / 'raas-garba' / 'lib'), type=Path, help='library path')
	args = parser.parse_args()

	libs.extend((args.libpath / p) for p in ['આરતી', 'ગરબા', 'રાસ', 'શ્લોક', 'bollywood'])

	for p in args.path:
		for i in p.rglob('index.rst'):
			fix_dir(i.parent)

def fix_dir(dir_path: Path) -> None:
	print(dir_path)

	for p in dir_path.glob('*'):
		if p.is_symlink() and not p.exists():
			p.unlink()
			print(f"  -{p}")

	for l in read_entries(dir_path / 'index.rst'):
		ln = dir_path / l

		if ln.exists():
			continue

		f = next((lib / l for lib in libs if (lib / l).exists()), None)
		if f:
			from os.path import relpath
			rp = Path(relpath(f, dir_path))
			ln.symlink_to(rp)
			print(f"  +{ln} -> {rp}")
		else:
			logging.error('%s cannot be found', str(l))

def read_entries(fname: Path):
	import re

	with open(fname) as f:
		for line in f.read().split('\n'):
			m = re.fullmatch(r'\s*.*<(.*\.rst)>', line)
			if m:
				yield m.group(1)
			m = re.fullmatch(r'\s*(.*\.rst)', line)
			if m:
				yield m.group(1)

if __name__ == '__main__':
	import sys
	sys.exit(main())
