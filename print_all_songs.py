import os
import glob
import hdf5_getters

DB_DIR = "./MillionSongSubset"
#print all records title, artist, and year
def print_all_songs():
    for root, dirs, files in os.walk(DB_DIR):
        files = glob.glob(os.path.join(root, "*" + ".h5"))
        for f in files:
            h5 = hdf5_getters.open_h5_file_read(f)
            title = hdf5_getters.get_title(h5).decode("utf-8")
            yr = str(int(hdf5_getters.get_year(h5)))
            if yr=='0': yr='NO RELEASE DATE INFO'
            artist = hdf5_getters.get_artist_name(h5).decode("utf-8")
            tag = hdf5_getters.get_artist_mbtags(h5)
            t = []
            for x in tag:
                t.append(x.decode("utf-8"))
            if t != [] : print(f"{title} by {artist}, {yr}\nTags: {t}\n")
            h5.close()