import pandas as pd
import numpy as np
import joblib
import argparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

# create a argparser
def prepareArgParser():
	arg_parser = argparse.ArgumentParser(description='A fake news classifier training system')
	arg_parser.add_argument('input_file', help='csv file to train the ai.', default='texts.csv')
	arg_parser.add_argument('-o','--output', help='train ai model file', default='idFake_model.pkl')
	return arg_parser


# parses arguments from argparser
def parseArgs(arg_parser):
	args = arg_parser.parse_args()
	input_file = args.input_file
	output_file = args.output
	return (input_file, output_file)

def fit_ai(csv_filename, output_file):
    df = pd.read_csv(csv_filename)
    df.head()
    df['fake'] = df['tag'].apply(lambda x: 1 if x =='FAKE' else 0)


    X_train, X_test, y_train, y_test = train_test_split(df.text, df.fake, test_size=0.2)


    v = CountVectorizer()

    X_train_cv = v.fit_transform(X_train.values)

    clf = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('nb', MultinomialNB())
    ])
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print(classification_report(y_test, y_pred))
    joblib.dump(clf, output_file)
    
def main():
    input_file, output_file = parseArgs(prepareArgParser())
    fit_ai(input_file, output_file)

if __name__ == '__main__':
	main()
	