#! /usr/bin/env python
"Check symlinks to songs"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2018-2019, Paresh Adhia"

from typing import Iterable, Dict
from pathlib import Path
from os.path import relpath, commonpath
import logging
import sys

def main():
	"script entry-point"
	import argparse

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('paths', nargs='*', default=[Path.cwd()], type=Path, help='directories to fix')
	parser.add_argument('--libpath', default=None, type=Path, help='library path')
	args = parser.parse_args()

	if not args.libpath:
		args.libpath = Path(sys.argv[0]).parent / 'lib'

	lib = {p.name: p for p in args.libpath.resolve().rglob('*.rst') if p.name != 'index.rst'}

	for p in args.paths:
		for i in p.rglob('index.rst'):
			fix_dir(i.parent.resolve(), lib)

def fix_dir(dir_path: Path, lib: Dict[str, Path]) -> None:
	print(dir_path)

	for p in dir_path.glob('*'):
		if p.is_symlink() and not p.exists():
			p.unlink()
			print(f"  -{p}")

	for l in read_entries(dir_path / 'index.rst'):
		ln = dir_path / l

		if ln.exists():
			continue

		if ln.name in lib:
			base = rel_link(ln, lib[ln.name])
			ln.symlink_to(base)
			print(f"  +{ln} -> {base}")
		else:
			logging.error('%s cannot be found', str(l))

def read_entries(fname: Path) -> Iterable[str]:
	import re

	with open(fname) as f:
		for line in f.read().split('\n'):
			m = re.fullmatch(r'\s*.*<(.*\.rst)>', line)
			if m:
				yield m.group(1)
			m = re.fullmatch(r'\s*(.*\.rst)', line)
			if m:
				yield m.group(1)

def rel_link(link: Path, base: Path):
	c = commonpath([base, link])
	up = len(link.relative_to(c).parts)-1

	return Path('/'.join(['..'] * up)) / base.relative_to(c)

if __name__ == '__main__':
	sys.exit(main())
