from pathlib import Path
import os
import subprocess

import pandas as pd
import numpy as np

from collections import Counter
from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib
import pylab as pl
from IPython.core.display import display, HTML

import sklearn
import sklearn.model_selection
import sklearn.linear_model
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline

import spacy

import pyLDAvis
import pyLDAvis.gensim
    
import gensim
import logging

def main():
    data_dir = '/home/srivbane/eriks074/repos/sna-social-support/support_classification/data'
    output_data_dir = "/home/srivbane/shared/caringbridge/data/projects/sna-social-support/support_modeling"
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        
    gbs = pd.read_hdf(os.path.join(data_dir, 'tokenized_gb_1000000.h5'), key='gbs')
    dct = gensim.corpora.Dictionary(gbs.tokens)
    
    prev_size = len(dct)
    dct.filter_extremes(no_below=5, no_above=0.2)
    new_size = len(dct)
    print(f"Removed {prev_size - new_size} dictionary entries. New size: {new_size}")
    dct.save(os.path.join(output_data_dir, "lda/gb_30t_dict.pkl"))
    
    corpus = [dct.doc2bow(sentence) for sentence in tqdm(gbs.tokens, position=False) if len(sentence) > 2]
    lda = gensim.models.LdaMulticore(corpus, id2word=dct, num_topics=30, passes=10, chunksize=10000)
    
    lda.save(os.path.join(output_data_dir, 'lda/gb_1000000_lda_30t.model'))
    
    #prepared_data = pyLDAvis.gensim.prepare(lda, corpus, dct)
    #pyLDAvis.save_html(prepared_data, "lda_vis_100topic.html")

if __name__ == "__main__":
    main()
