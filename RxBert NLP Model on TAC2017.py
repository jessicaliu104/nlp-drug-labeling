import re, os
import pickle
import pandas as pd
from tqdm import tqdm
import random
from collections import defaultdict
import numpy as np
import spacy
from spacy import displacy

import warnings
warnings.simplefilter("ignore")

# import xml.etree.ElementTree as ET
import spacy_transformers

## data load:
train_data = pickle.load(open('TAC_TRAIN_FIXED_2022.pik','rb'))
test_data  = pickle.load(open('TAC_TEST_FIXED_2022.pik','rb'))

# model
cur_model = 'tac2017_train_ep200_rxbert_fortesting'
nlp = spacy.load(cur_model)
result=[]
ent_pool = pd.DataFrame(None, columns=['Doc_ID', 'Term','Start','End','Type','Category'])
for doc_id, data in tqdm(enumerate(test_data)):
    doc = data[0]
    label = data[1]['entities']
    
    
    doc_ents = nlp(nlp.make_doc(doc))
    
    for ent in doc_ents.ents:
        term, start, ttype, end = ent.text, ent.start_char, ent.label_, ent.end_char
        curr = {'Doc_ID':doc_id, 'Term':term, 'Start':start, 'End':end, 'Type':ttype, 'Category':'PRED'}
        
        ent_pool = pd.concat((ent_pool, pd.DataFrame([curr])))
    
    for gt in label: # ground truth: the target for training or validating the model with a labeled dataset
        start, end, ttype = gt
        term = doc[start:end]
        curr = {'Doc_ID':doc_id, 'Term':term, 'Start':start, 'End':end, 'Type':ttype, 'Category':'TRUE'}
        
        ent_pool = pd.concat((ent_pool, pd.DataFrame([curr])))
ent_pool = ent_pool.sort_values(['Doc_ID','Start','Term']).reset_index(drop=True)
ent_pool['sid'] = [str(d['Doc_ID'])+'|'+str(d['Start']) for ind, d in ent_pool.iterrows()]

count=defaultdict(int)
for sid in ent_pool['sid'].unique():
    tmp_df = ent_pool.loc[ent_pool['sid']==sid,:]
    if tmp_df.shape[0]==1:
        count[tmp_df['Category'].values[0]]+=1
        if tmp_df['Category'].values[0]=='PRED':
            ent_pool.loc[tmp_df.index,'Result']='FP'
        else:
            ent_pool.loc[tmp_df.index,'Result']='FN'
    else:
        count['TP'] +=1
        ent_pool.loc[tmp_df.index,'Result']='TP'

ent_pool.groupby(['Type','Category','Result'])['Term'].count().to_csv('TAC2017_testing_result_Table.csv')
