import hdf5_getters
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import glob

DB_DIR = "./MillionSongSubset"

def recommend(song, similarity_matrix, artist_terms, song_names, top_n=5):
    # Find the index of the given song in the artist_terms list
    song_index = song_names.index(song)

    # Get the similarity scores for the given song
    similarity_scores = similarity_matrix[song_index]

    # Sort the songs based on similarity scores (descending order)
    sorted_indices = similarity_scores.argsort()[::-1]

    # Exclude the input song from the recommended list and get the top N recommendations
    recommended_songs = [song_names[i] for i in sorted_indices if i != song_index][:top_n]

    return recommended_songs


artist_terms = []
song_names = []

# Iterate through the dataset files
for root, dirs, files in os.walk(DB_DIR):
    files = glob.glob(os.path.join(root, "*" + ".h5"))
    for file_path in files:
        # Open the HDF5 file
        with hdf5_getters.open_h5_file_read(file_path) as h5:

            # Extract artist terms
            artist_term_from_getter = hdf5_getters.get_artist_terms(h5)
            artist_terms_arr = [term.decode("utf-8").replace(" ", "") for term in artist_term_from_getter]
            artist_terms_as_str = " ".join(artist_terms_arr)
            artist_terms.append(artist_terms_as_str)
            song_names.append(hdf5_getters.get_title(h5).decode("utf-8"))

# Create vectors and calculate cosine similarity
cv = CountVectorizer(max_features=10000, stop_words="english")
vectors = cv.fit_transform(artist_terms).toarray()
similarity_matrix = cosine_similarity(vectors)

# Example: Recommend songs for "Heard 'Em Say"
recommended_songs = recommend("Heard 'Em Say", similarity_matrix, artist_terms, song_names)
print("Recommended songs:", recommended_songs)
