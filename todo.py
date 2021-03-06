# TODO.PY
# ------------------------------------------------------------------------
# This is a small utility that helps you find 'TODO'ed lines in the source
# files of a given directory.
# License: Why would I need one? I mean it's such a small program...
# Copy as you wish, modify as you wish.
# Author: Zoltan Szatmary

import os
import sys

SOURCE_FILE_EXTENSIONS = ['.asm', '.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx']

# Just to be able to determine if the string ends with one of the endings.
def ends_with(string, xs):
	for x in xs:
		if string.endswith(x):
			return True
	return False

def get_source_files(path):
	files = []
	for root, ds, fs in os.walk(path):
		for f in fs:
			if ends_with(f, SOURCE_FILE_EXTENSIONS):
				files.append(os.path.join(root, f))
		for d in ds:
			files += get_source_files(os.path.join(root, d))
	return files

def get_todos(path):
	files = get_source_files(path)
	todos = []
	for fname in files:
		f = open(fname, 'r')
		ts = []
		for index, line in enumerate(f, start=1):
			line = line.strip()
			if 'TODO' in line.upper():
				ts.append((index, line))
		if len(ts) > 0:
			todos.append((fname, ts))
		f.close()
	return todos

def print_todos(todos):
	print('TODOs found in "{}"'.format(path))
	for name, ts in todos:
		print('\t' + name)
		for i, t in ts:
			print('\t\tLine {}: {}'.format(i, t))

def write_todos(todos):
	f = open('analysis.csv', 'w')
	f.write('file;line;todo\n')
	for name, ts in todos:
		for i, t in ts:
			f.write('{};{};{}\n'.format(name, i, t))
	f.close()

if __name__ == '__main__':
	path = ''
	if len(sys.argv) == 1:
		path = os.getcwd()
		todos = get_todos(path)
		print_todos(todos)
		write_todos(todos)
	else:
		for i in range(1, len(sys.argv)):
			path = str(sys.argv[i])
			todos = get_todos(path)
			print_todos(todos)
			write_todos(todos)
