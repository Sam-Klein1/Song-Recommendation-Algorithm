import hdf5_getters
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import glob

DB_DIR = "./MillionSongSubset"

def recommend(input_song_name, similarity_matrix, song_name_to_index, song_indices, artist_terms, num_recommendations=5):
    # Get the index of the input song
    input_song_index = song_name_to_index.get(input_song_name.lower())
    if input_song_index is None:
        print(f"Song '{input_song_name}' not found.")
        return []

    # Get similarity scores for the input song
    input_song_similarity_scores = similarity_matrix[input_song_index]

    # Get indices of songs with highest similarity scores
    recommended_song_indices = input_song_similarity_scores.argsort()[-num_recommendations-1:-1][::-1]

    # Get the actual song names and artist terms from the indices
    recommended_songs_info = [(song_indices[idx], artist_terms[idx]) for idx in recommended_song_indices]

    return recommended_songs_info

# Load artist terms and create a mapping from song names to indices
artist_terms = []
song_name_to_index = {}
song_indices = []

# Iterate through the dataset files
for root, dirs, files in os.walk(DB_DIR):
    files = glob.glob(os.path.join(root, "*" + ".h5"))
    for idx, file_path in enumerate(files):
        # Open the HDF5 file
        with hdf5_getters.open_h5_file_read(file_path) as h5:
            # Extract artist terms
            artist_term_from_getter = hdf5_getters.get_artist_terms(h5)
            artist_terms_arr = [term.decode("utf-8").replace(" ", "") for term in artist_term_from_getter]
            artist_terms.append(" ".join(artist_terms_arr))

            # Extract song name
            song_name = hdf5_getters.get_title(h5).decode("utf-8")

            # Populate the mapping and list
            song_name_to_index[song_name.lower()] = idx
            song_indices.append(song_name)

# Create vectors and calculate cosine similarity
cv = CountVectorizer(max_features=10000, stop_words="english")
vectors = cv.fit_transform(artist_terms).toarray()
similarity_matrix = cosine_similarity(vectors)

# Example: Recommend songs similar to the input song
input_song_name = "Heard 'Em Say"  # Provide the name in lowercase
recommendations = recommend(input_song_name, similarity_matrix, song_name_to_index, song_indices, artist_terms)

# Print recommendations with artist terms
if recommendations:
    print(f"Recommendations for {input_song_name}:")
    for song_name, artist_terms in recommendations:
        print(f"Song: {song_name}, Artist Terms: {artist_terms}")
else:
    print(f"Song '{input_song_name}' not found.")
