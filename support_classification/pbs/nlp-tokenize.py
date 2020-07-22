from pathlib import Path
import os
import subprocess

import pandas as pd
import numpy as np

from collections import Counter
from tqdm import tqdm

import spacy

def main():
    nlp = spacy.load('en_core_web_lg')

    output_data_dir = "/home/lana/shared/caringbridge/data/projects/sna-social-support/support_modeling"
    gbs = pd.read_hdf('with_text_for_classify.h5')

    tokens = []
    for doc in tqdm(nlp.pipe([x if x != None else "" for x in gbs.body_text], batch_size=25000, n_threads=16), total=len(gbs), position=False):
        tokens.append([token.text for token in doc])
    gbs['tokens'] = tokens
    
    gbs['tokens'] = gbs['tokens'].map(list)
    gbs['body_text'] = gbs['body_text'].map(str)
    gbs['int_type'] = gbs['int_type'].map(str)
    gbs['journal_oid'] = gbs['journal_oid'].map(str)
    
    gbs.to_hdf(os.path.join(output_data_dir, 'tokenized_for_bf.h5'), key='gbs')

if __name__ == "__main__":
    main()
