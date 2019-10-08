import os
import argparse
import logging
import time
import matplotlib.pyplot as plt
from collections import OrderedDict

logging.basicConfig(level=logging.DEBUG)


# to run in python 3
_description = 'Measure the relative frequencies of letters ' \
			   'in a text file'



def process(file_path, hist, skip, stats):

	"""Main processing method.
	"""

	# Basic sanity check: make sure that the file_argument points to an
	# existing text file.
	assert file_path.endswith('.txt'), 'invalid file extension'
	assert os.path.isfile(file_path), 'directory not found'

	# Open the input file (note that we are taking advantage of context
	# management, using a with statement).
	logging.info('opening input file "%s"', file_path)
	with open(file_path, "r") as myfile:
		string = myfile.read().lower()
	logging.info('file opened')

	# If 'skip' remove the preamble
	if skip:
		index = string.find('***')
		index = string.find('\n', index)
		string = string[index:]
	logging.debug('beginning of the string: {}...'.format(string[:100]))

	# Prepare a dictionary for the occurrences and initialize some
	# values
	alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
				'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
				'w', 'x', 'y', 'z']
	totchar = 0 # count of generic characters
	totletters = 0 # count of letters in the alphabet
	totlines = 0 # count of lines
	d = OrderedDict((char, 0) for char in alphabet)
	logging.debug('empty dictionary: {}'.format(d))

	# Count the occurrences for every letter and some other stuff
	logging.info("counting frequencies...")
	for c in string:
		totchar += 1
		if c in alphabet:
			totletters += 1
			d[c] += 1
		if c == '\n':
			totlines += 1
	logging.debug('letter count: {}'.format(totletters))
	logging.debug('count of the "a" letter: {}'.format(d['a']))

	# if 'stats' is true, print some stats
	if stats:
		print('### STATS ###')
		print('Number of generic characters: {}'.format(totchar))
		print('Number of alphabet letters: {}'.format(totletters))
		print('Number of lines: {}'.format(totlines))
		L = len(string.split()) # requires another loop
		print('Number of words: {}'.format(L))

	# show relative frequencies
	print('The relative frequencies are the following:')
	for key in d:
		d[key] /= totletters
		d[key] *= 100
		print(key, '{:.3f}%'.format(d[key]))
	logging.debug('sum of all the frequencies: '
				  '{}'.format(sum(d.values())))

	# plot histogram if required
	if hist:
		plt.ylabel('Frequencies (%)')
		plt.xlabel('Letter')
		plt.bar(d.keys(), d.values(), 1, color='g')
		plt.show()





if __name__ == '__main__':

	logging.info("start processing")
	start_time = time.time()

	# Inizialize parser and add arguments
	parser = argparse.ArgumentParser(description=_description)
	parser.add_argument('infile', help='Path to the input file')
	parser.add_argument('-hist', '--histogram', action="store_true",
						help='show a histogram for the '
							 'frequencies')
	parser.add_argument('--skip', action='store_true',
						help='skip the preamble and the license. The '
							 'script starts counting at the end of the '
							 '"***" string, which (in the plain text '
							 'format) is usually located at the end '
							 'of the preamble')
	parser.add_argument('--stats', action='store_true',
						help='print out some basic stats about the book')
	args = parser.parse_args()
	logging.debug('Args: {}'.format(args))

	# Run process
	process(args.infile, args.histogram, args.skip, args.stats)

	# Print elapsed time
	elapsed_time = time.time() - start_time
	logging.info('end of process. Total elapsed time: {:.3f}'
				 .format(elapsed_time))
