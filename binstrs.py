#!/usr/bin/python
# (c) 2014 Anmol Sarma <me@anmolsarma.in>
# Script to recusrsively find string attributes/values in libs directory 
# Usage: binstrs.py <directory path> <attribute> <value>
# Example: binstrs.py ./src GCC: 4.7.3

from sys import argv
from os import path, walk
from string import printable

def getStrs(filename, min_len = 10):
	with open(filename, 'rb') as open_file:
		string_buffer = ''
		for read_byte in open_file.read():
			if read_byte in printable:
				string_buffer += read_byte
				continue
			if len(string_buffer) >= min_len:
				yield string_buffer
			string_buffer = ''

def matchStrs(attr, value, strings):
	for instance in strings:
		if attr in instance:
			if value not in instance:
				print '\tMismatch found: ' + instance
				return False	
			return True

def parseDirectory(directory_path, attr, value):
	num_parse = 0
	num_mismatch = 0
	num_notfound = 0
	for root, dirnames, filenames in walk(directory_path):
		for filename in filenames:
			if filename.endswith(('.a', '.lib', '.dll')):
				print 'Parsing ' + path.join(root, filename)
				num_parse += 1
				result = matchStrs(attr, value, getStrs(path.join(root, filename)))
				if result == None:
					print '\t '' + attr + '' instance not found'
					num_notfound += 1
				if result == False:
					num_mismatch += 1
	
	print '========= SUMMARY ========='
	print 'In directory ' + directory_path				
	print '\t' + str(num_parse) + ' files parsed'
	print '\t' + str(num_mismatch) + ' mismatches found'
	print '\t' + str(num_notfound) + ' files without instance of ' + attr
	
parseDirectory(argv[1], argv[2], argv[3])


	
