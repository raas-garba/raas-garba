#! /usr/bin/env python
"Check symlinks to songs"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2018-2019, Paresh Adhia"

from typing import Iterable, Dict, Optional, Sequence
from pathlib import Path
from os.path import relpath, commonpath
import logging
import sys
import re

def main(paths: Sequence[Path], libpath: Path) -> int:
	"script entry-point"
	lib = {p.name: p for p in libpath.resolve().rglob('*.rst') if p.name != 'index.rst'}

	missing = linked = 0
	for e in new_entries(paths):
		b = lib.get(e.name, None)
		if b:
			e.symlink_to(rel_link(e, b))
			linked += 1
		else:
			missing += 1
			logging.error(f"'{e.name}' in '{e.parent}' not found")
	print(f"Entries linked={linked}, missing={missing}")

	return 1 if missing > 0 else 0

def new_entries(paths: Sequence[Path]) -> Iterable[Path]:
	all_toc = (i for p in paths for i in p.resolve().rglob('index.rst'))
	toc_lines = ((t, l) for t in all_toc for l in t.read_text().split('\n'))
	all_entries = filter(None, (entry(t.parent, l) for t, l in toc_lines))
	only_new = filter(lambda e: not e.exists(), all_entries)

	return only_new

def entry(dirpath: Path, line: str) -> Optional[str]:
	m = re.fullmatch(r'\s*.*<(.*\.rst)>', line)
	if m:
		return dirpath / m.group(1)
	m = re.fullmatch(r'\s*(.*\.rst)', line)
	if m:
		return dirpath / m.group(1)

def rel_link(link: Path, base: Path):
	c = commonpath([base, link])
	up = len(link.relative_to(c).parts)-1

	return Path('/'.join(['..'] * up)) / base.relative_to(c)

def getargs():
	import argparse

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('paths', nargs='*', default=[Path.cwd()], type=Path, help='directories to fix')
	parser.add_argument('--libpath', default=(Path(sys.argv[0]).parent / 'lib'), type=Path, help='library path')

	return parser.parse_args()

if __name__ == '__main__':
	sys.exit(main(**getargs().__dict__))
