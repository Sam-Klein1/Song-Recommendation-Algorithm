import hdf5_getters

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=10000, stop_words="english")

from sklearn.metrics.pairwise import cosine_similarity

import os
import glob

DB_DIR = "./MillionSongSubset"


def recommend(song):
    #TODO Implement recommendation based on similarity

artist_terms = []

for root, dirs, files in os.walk(DB_DIR):
    files = glob.glob(os.path.join(root, "*" + ".h5"))
    for f in files:
        h5 = hdf5_getters.open_h5_file_read(f)
        artist_term_from_getter = hdf5_getters.get_artist_terms(h5)
        artist_terms_arr = []
        for artist_term in artist_term_from_getter:
            artist_terms_arr.append(artist_term.decode("utf-8").replace(" ", ""))
        artist_terms.append(" ".join(artist_terms_arr))
        h5.close()

vectors = cv.fit_transform(artist_terms).toarray()
similarity = cosine_similarity(vectors)

print(similarity)
