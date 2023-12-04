import hdf5_getters
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import glob

DB_DIR = "./MillionSongSubset"

def recommend(song, similarity_matrix, song_names, artist_terms, top_n=10):
    # Find the index of the given song in the artist_terms list
    song_index = song_names.index(song)

    # Get the similarity scores for the given song
    similarity_scores = similarity_matrix[song_index]

    # Sort the songs based on similarity scores (descending order)
    sorted_indices = similarity_scores.argsort()[::-1]

    # Exclude the input song from the recommended list and get the top N recommendations
    recommended_songs = [song_names[i] for i in sorted_indices if i != song_index][:top_n]
    recommended_scores = [similarity_scores[i] for i in sorted_indices if i != song_index][:top_n]
    recommended_artist_terms = [artist_terms[i] for i in sorted_indices if i != song_index][:top_n]

    return recommended_songs, recommended_scores, recommended_artist_terms

artist_terms = []
song_names = []

# Iterate through the dataset files
for root, dirs, files in os.walk(DB_DIR):
    files = glob.glob(os.path.join(root, "*" + ".h5"))
    for file_path in files:
        # Open the HDF5 file
        with hdf5_getters.open_h5_file_read(file_path) as h5:
            print("opened file.")

            # Extract artist terms
            artist_term_from_getter = hdf5_getters.get_artist_terms(h5)
            artist_terms_arr = [term.decode("utf-8").replace(" ", "") for term in artist_term_from_getter]
            artist_terms_as_str = " ".join(artist_terms_arr)
            artist_terms.append(artist_terms_as_str)
            song_names.append(hdf5_getters.get_title(h5).decode("utf-8"))

            print("processed file.")

# Create vectors and calculate cosine similarity
print("creating vectors...")
cv = CountVectorizer(max_features=10000, stop_words="english")
vectors = cv.fit_transform(artist_terms).toarray()

print("calculating similarity matrix...")
similarity_matrix = cosine_similarity(vectors)

# Prompt user for input song from the database
input_song = str(input("\n=======================\nsong to get recommendations for: "))
print("=======================\n")

while True:
    recommended_songs, recommended_scores, recommended_artist_terms = recommend(input_song, similarity_matrix, song_names, artist_terms)
    print(f"Recommendations for: {input_song}")
    for i, (song, score, terms) in enumerate(zip(recommended_songs, recommended_scores, recommended_artist_terms)):
        print(f"{i+1}. {song} \n(Similarity Score: {score:.4f}) \nArtist Terms: {terms}")

    # Prompt user for the input song from the database
    input_song = str(input("\n=======================\nsong to get recommendations for: "))
    print("=======================\n")
