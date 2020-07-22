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

import sklearn
import sklearn.model_selection
import sklearn.linear_model
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline

def main():
    data_dir = '/home/srivbane/eriks074/repos/sna-social-support/support_classification/data'
    output_data_dir = "/home/lana/shared/caringbridge/data/projects/sna-social-support/support_modeling"
    
    metadata_dir = "/home/lana/shared/caringbridge/data/projects/sna-social-support/user_metadata"
    author_to_site = os.path.join(metadata_dir, "interaction_metadata.h5")
    df = pd.read_hdf(author_to_site)
    
    author_type_dir = "/home/lana/shared/caringbridge/data/projects/sna-social-support/author_type"
    support_m_dir = "/home/lana/shared/caringbridge/data/projects/sna-social-support/support_modeling"
    site_patient_proportions_filepath = os.path.join(author_type_dir, 'site_patient_proportions.df')
    site_author_type_df = pd.read_feather(site_patient_proportions_filepath)
    
    # load the list of valid users. how to regenerate valid_user_ids.txt to include ALL users?
    data_selection_working_dir = "/home/lana/shared/caringbridge/data/projects/sna-social-support/data_selection"
    valid_user_ids = set()
    with open(os.path.join(data_selection_working_dir, "supportive_valid_user_ids.txt"), 'r') as infile:
        for line in infile:
            user_id = line.strip()
            if user_id == "":
                continue
            else:
                valid_user_ids.add(int(user_id))
    
    ints = df[(df.user_id.isin(valid_user_ids)) & (df.int_type != "journal") & (~df.is_self_interaction) & (df.is_nontrivial)]
    guestbooks = ints[ints.int_type == 'guestbook']
    site_to_type = {x: y for x, y in zip(site_author_type_df.site_id, site_author_type_df.site_author_type)}
    include = site_to_type.keys()
    limited = guestbooks[guestbooks.site_id.isin(include)]
    
    # add the guestbook text directly
    import sqlite3
    try:
        gb_db_filepath = "/home/lana/shared/caringbridge/data/projects/caringbridge_core/updated_guestbook.sqlite"
        guestbook_db = sqlite3.connect(
            gb_db_filepath,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        guestbook_db.row_factory = sqlite3.Row

        body_texts = []
        for user_id, site_id, created_at in tqdm(zip(limited.user_id, limited.site_id, limited.created_at), total=len(limited), position=False):
            cursor = guestbook_db.execute("""
                        SELECT *
                            FROM guestbook 
                            WHERE user_id = ? AND site_id = ? AND created_at = ?
                        """, (user_id,site_id,created_at))
            result = cursor.fetchall()
            #assert len(result) == 1
            result = result[0]
            body = result['body']
            body_texts.append(body)
    finally:
        guestbook_db.close()
    assert len(body_texts) == len(limited)
    limited['body_text'] = body_texts
    
    limited.to_hdf('with_text_for_classify.h5', key='limited')
    

if __name__ == "__main__":
    main()
