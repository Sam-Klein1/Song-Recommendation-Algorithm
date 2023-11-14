import os
import glob
import hdf5_getters

DB_DIR = "./MillionSongSubset"
#print all records title, artist, and year
def find_tags(song, artist):
    for root, dirs, files in os.walk(DB_DIR):
        files = glob.glob(os.path.join(root, "*" + ".h5"))
        for f in files:
            h5 = hdf5_getters.open_h5_file_read(f)
            title = hdf5_getters.get_title(h5).decode("utf-8")
            yr = str(int(hdf5_getters.get_year(h5)))
            if yr=='0': yr='NO RELEASE DATE INFO'
            a = hdf5_getters.get_artist_name(h5).decode("utf-8")
            if (str(song).lower() == str(title).lower()) and (str(artist).lower() == str(a).lower()):
                tag = hdf5_getters.get_artist_mbtags(h5)
                t = []
                for x in tag:
                    t.append(x.decode("utf-8"))
                if t != [] : 
                    h5.close()
                    return t
                else:
                    print("No tags found!")
                    return t
            h5.close()