import os
import glob
import hdf5_getters

DB_DIR = "./MillionSongSubset"
#print all records title, artist, and year
def find_song_artist(song, artist):
    for root, dirs, files in os.walk(DB_DIR):
        files = glob.glob(os.path.join(root, "*" + ".h5"))
        for f in files:
            h5 = hdf5_getters.open_h5_file_read(f)
            title = hdf5_getters.get_title(h5).decode("utf-8")
            a = hdf5_getters.get_artist_name(h5).decode("utf-8")
            if (str(song).lower() == str(title).lower()) and (str(artist).lower() == str(a).lower()):
                h5.close()
                return True
            else:
                h5.close()
            