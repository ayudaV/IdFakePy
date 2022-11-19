import pandas as pd
import os
import argparse


# create a argparser
def prepareArgParser():
	arg_parser = argparse.ArgumentParser(description='A fake news classifier training system')
	arg_parser.add_argument('input_dir', help='path to the folder containing texts to be reduced.')
	arg_parser.add_argument('-o','--output', help='output file', default='texts.csv')
	return arg_parser


# parses arguments from argparser
def parseArgs(arg_parser):
	args = arg_parser.parse_args()
	input_dir = args.input_dir
	output_file = args.output
	return (input_dir, output_file)

def extract_to_csv(input_dir, output_file):
    df = pd.DataFrame(columns=['tag', 'text'])
    for filename in os.listdir(input_dir + '/real'):
        text = open(input_dir + '/real/' + filename).read()
        df.loc[len(df)] = ['REAL', text]
        
    for filename in os.listdir(input_dir + '/fake'):
        text = open(input_dir + '/fake/' + filename).read()
        df.loc[len(df)] = ['FAKE', text]
        
    df.to_csv(output_file,index=False)

def main():
    input_dir, output_file = parseArgs(prepareArgParser())
    extract_to_csv(input_dir, output_file)

if __name__ == '__main__':
	main()
	