import spacy
import pandas as pd
from azureml.core import Workspace
from azureml.core import Model
import re
import warnings
from src.pa_logging import logger

warnings.filterwarnings('ignore')

class spacy_mof:
    def __init__(self,spacy_model_name):
        ws = Workspace.from_config()              
        self.model_path = Model.get_model_path(spacy_model_name,_workspace = ws)        

    def predict(self,data_path,description_column_name):
        if description_column_name == "":
            description_column_name = "Description"
        logger.info("Loading data...")
        if data_path.endswith('csv'):
            df_source = pd.read_csv(data_path)
        else:
            df_source = pd.read_excel(data_path)
        assert description_column_name in df_source.columns, logger.info(f'Column not found: There is no \'{description_column_name}\' column in the data. Please check the column name')
        logger.info('Loading Model...')  
        nlp = spacy.load(self.model_path)
        df = df_source[[description_column_name]].dropna().drop_duplicates()
        logger.info('Predicting results...')
        df.loc[:,'cleaned_text'] = df[description_column_name].apply(lambda x: re.sub("^[\d]+\.","",x)).str.replace(".",' ').str.replace("("," ").str.replace(")"," ").str.replace(","," ").str.replace("->"," ").str.replace("/"," ")
        df_result = pd.DataFrame(columns=['First','Second',"Third"])
        texts = df['cleaned_text'].tolist()
        y_pred = list()
        docs = list(nlp.pipe(texts))     

        for index,doc in enumerate(docs):
            y_pred.append(sorted(doc.cats, key=doc.cats.get, reverse=True)[:3])        
            
        logger.info("Saving result...")
        df_result[description_column_name] = df[description_column_name]
        df_result['First'] = [i[0] for i in y_pred]
        df_result['Second'] = [i[1] for i in y_pred]
        df_result['Third'] = [i[2] for i in y_pred]
        df_source.merge(df_result, how = 'left', on = description_column_name).to_csv('results/'+data_path.split('/')[-1].split('.')[0] +'-results.csv')
        logger.info("Done!")
        logger.info("Task Completed!")
        