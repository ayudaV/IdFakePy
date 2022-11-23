#Codigo adaptado do projeto FakeNilc, autoria de Rafael Monteiro
import os
import argparse
import re

# create a argparser
def prepareArgParser():
	arg_parser = argparse.ArgumentParser(description='A fake news classifier training system')
	arg_parser.add_argument('input_dir', help='path to the folder containing texts to be reduced.')
	arg_parser.add_argument('-o','--output', help='output folder', default='reduced_texts')
	arg_parser.add_argument('-t','--truncate', help='truncates text instead of waiting for end of sentence.', action='store_true')
	arg_parser.add_argument('-v','--verbose', help='output verbosity.', action='store_true')
	return arg_parser

# parses arguments from argparser
def parseArgs(arg_parser):
	args = arg_parser.parse_args()
	news_dir = args.input_dir
	output_dir = args.output
	truncate = args.truncate
	verbose = args.verbose
	return (news_dir, output_dir, truncate, verbose)

def wordcount(string):

	count = 0
	#split string into multiple sentences
	for sentence in re.split('([,\.\n])', string):
		#checks each word in the sentence
		for word in sentence.strip().split():
			# this regex skips punctuations, as I don't consider it words.
			if(re.match('([,\.\n])',word)):
				continue
			# sums 1 to the word count
			count += 1
	return count

def reducestr_truncate(str, limit):
	result = []
	count = 0
	#splits the text into sentences
	for word in str.split():
		result += word + " "
		if(re.match('([,\.\n])',word)):
			continue
		# counts words in each sentence
		count += 1
		
		# if the number of words is bigger than the limit 
		if count > limit:
			break

	return ''.join(result)

def reducestr(str, limit):
	result = []
	count = 0
	#splits the text into sentences
	for sentence in re.split('([\.\n])', str):
		# counts words in each sentence
		for word in sentence.strip().split():
			# this regex skips punctuations, as I don't consider it words.
			if(re.match('([,\.\n])',word)):
				continue
			count += 1
			# result += word + " "
		# if the 
		if count > limit:
			break
		result += sentence
	return ''.join(result)

def reduce(text1,text2, truncate = False):

	# counting number of words in texts
	c1 = wordcount(text1)
	c2 = wordcount(text2)

	# reduces the bigger text in size
	if(c1 > c2):
		text1 = reducestr_truncate(text1,c2) if truncate else reducestr(text1, c2)	
	else:
		text2 = reducestr_truncate(text2,c1) if truncate else reducestr(text2, c1)

	return(text1,text2)

def main():
	news_dir, output_dir, truncate, verbose = parseArgs(prepareArgParser())

	# creating dir for storing reduced texts
	os.makedirs(output_dir, exist_ok=True)
	output_dir += '/'
	os.makedirs(output_dir + 'real', exist_ok=True)
	os.makedirs(output_dir + 'fake', exist_ok=True)
	

	#fetching files
	filenames = []
	for real, fake in zip(os.listdir(news_dir + '/true'),os.listdir(news_dir + '/fake')):
		#appends a tuple with a true and a fake file filename
		filenames.append((news_dir + '/true/' + real, news_dir + '/fake/' + fake))

	# reducing files lenght
	for pair in filenames:

		real_filename = pair[0]
		fake_filename = pair[1]
		real_name = real_filename.split('/')[-1]
		fake_name = fake_filename.split('/')[-1]

		#opening files
		with open(pair[0], encoding='utf8') as real:
			with open(pair[1], encoding='utf8') as fake:

				#read both files and reduce the lenght of the biggest
				result = reduce(real.read(),fake.read(), truncate)

				#saves result
				with open(output_dir + 'real/' + real_name,'w', encoding='utf8') as f:
					print(result[0],file=f)
				with open(output_dir + 'fake/' + fake_name,'w', encoding='utf8') as f:
					print(result[1],file=f)


if __name__ == '__main__':
	main()
	