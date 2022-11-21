import argparse
import os
import joblib
from sklearn.pipeline import Pipeline

def prepareArgParser():
    arg_parser = argparse.ArgumentParser(description='A fake news classifier training system')
    arg_parser.add_argument('input_file', help='trained model saved in a pkl file', default='idfake_model.pkl')
    arg_parser.add_argument('texts_dir', help='path containing texts to predicting', default='test')
    return arg_parser


# parses arguments from argparser
def parseArgs(arg_parser):
    args = arg_parser.parse_args()
    input_file = args.input_file
    texts_dir = args.texts_dir

    return (input_file, texts_dir)


def predict_txt(model: Pipeline, texts):
    return model.predict(texts)

def main():
    input_file, texts_dir = parseArgs(prepareArgParser())
    model = joblib.load(input_file)
    texts = []
    for filename in os.listdir(texts_dir):
        text = open(texts_dir + '/' + filename).read()
        texts.append(text)
        
    print(predict_txt(model, texts))

if __name__ == '__main__':
	main()
	