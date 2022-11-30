"""Convert textcat annotation from JSONL to spaCy v3 .spacy format."""
import argparse
import re
from pathlib import Path

import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from spacy.tokens import DocBin


class convert_data:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.src_dir = str(Path().resolve().parents[2])

    def load_data(self,fileName: str,feature_c: str,label_c: str):
        """Load data from csv file to pdf and clean

        Args:
            fileName (str): input file name
            feature_c (str): feature column name
            label_c (str): label column name
        Returns:
            train (DataFrame): training dataframe
            test (DataFrame): testing dataframe
            labels_dict (Dict): dictionary of labels
        """
        df = pd.read_csv(self.src_dir +"/data/"+ fileName,encoding = 'utf-8').dropna(subset=[feature_c])
        print(df.columns)
        df['cleaned_text'] = df[feature_c].apply(lambda x: re.sub("^[\d]+\.","",x)).str.replace(".",' ').str.replace("("," ").str.replace(")"," ").str.replace(","," ").str.replace("->"," ")
        labels = df[label_c].unique().tolist()
        labels_dict = {i:0.0 for i in labels}
        df['tuples'] = df.apply(lambda row: (row['cleaned_text'],row[label_c]), axis=1)
        train, test = train_test_split(df['tuples'], test_size = 0.1, random_state = 0)
        train = train.tolist()
        test = test.tolist()        
        return train,test,labels_dict

    def get_cats(self,label: str,labels_dict: dict):
        """This will take a label and a dictionary and return a dictionary for spacy.Doc.doc.cats

        Args:
            label (str): label of current text
            labels_dict (dict): default labels dict to create label

        Returns:
            temp_dict: dictionary label for current text
        """
        temp_dict = labels_dict.copy()
        temp_dict[label] = 1.0
        return temp_dict

    def make_docs(self,data,labels_dict):
        """
        this will take a list of texts and labels and transform them in spacy documents
        
        texts: List(str)
        labels: List(labels)
        
        returns: List(spacy.Doc.doc)
        """

        # nlp.pipe([texts]) is way faster than running nlp(text) for each text
        # as_tuples allows us to pass in a tuple, the first one is treated as text
        # the second one will get returned as it is.
        docs = []
        for doc, label in self.nlp.pipe(data, as_tuples=True):
            temp_dict = self.get_cats(label,labels_dict)
            for key,value in temp_dict.items():
                doc.cats[key] = value        

            docs.append(doc)
        return docs

    def process_data(self,fileName: str,feature_c: str,label_c: str,destination: str):
        """

        Args:
            fileName (str): input filename
            feature_c (str): feature column name
            label_c (str): label column name
        """
        train,test,labels_dict = self.load_data(fileName,feature_c,label_c)
        train_docs = self.make_docs(train,labels_dict)
        val_docs = self.make_docs(test,labels_dict)
        destinations = ['textcat_multilabel']

        doc_bin = DocBin(docs=train_docs)       
        doc_bin.to_disk(self.src_dir+"/"+destination+"/corpus/train.spacy")

        doc_bin = DocBin(docs=val_docs)  
        doc_bin.to_disk(self.src_dir+"/"+destination+"/corpus/dev.spacy")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_name", help="Name of input file file")
    parser.add_argument("-i", "--feature_c", help="Name of feature columns")
    parser.add_argument("-l", "--label_c", help="Name of label columns")
    parser.add_argument("-d", "--destination", help="Folder containing the model")
    
    options = parser.parse_args()

    c = convert_data()
    c.process_data(options.file_name,options.feature_c,options.label_c,options.destination)
