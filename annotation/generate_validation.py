import pandas as pd
import numpy as np

df = pd.read_json('reviews_Electronics_sample.json',lines=True)
df = df.sample(1000, random_state=np.random.RandomState(40))
df = df[['reviewerID','summary','reviewText']]
df = df.set_index('reviewerID')
df.to_csv('validation.csv')