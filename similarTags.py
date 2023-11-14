import os
import glob
import hdf5_getters

DB_DIR = "./MillionSongSubset"
#print all records title, artist, and year
def similarTags(song, artist, tags):
    if tags == []: return
    for root, dirs, files in os.walk(DB_DIR):
        files = glob.glob(os.path.join(root, "*" + ".h5"))
        for f in files:
            h5 = hdf5_getters.open_h5_file_read(f)
            title = hdf5_getters.get_title(h5).decode("utf-8")
            yr = str(int(hdf5_getters.get_year(h5)))
            if yr=='0': yr='NO RELEASE DATE INFO'
            a = hdf5_getters.get_artist_name(h5).decode("utf-8")
            tag = hdf5_getters.get_artist_mbtags(h5)
            t = []
            for x in tag:
                t.append(x.decode("utf-8"))
            found = False
            if (str(song).lower() != str(title).lower()) and (str(artist).lower() != str(a).lower()):
                count = 0
                length = len(tags)
                if length < 4:
                    for y in tags:
                        for z in t:
                            if z == y :
                                count = count + 1
                                if count == length:
                                    print(f"{title} by {a}, {yr}\n")
                                    found = True
                                    break
                        if found == True : break
                else:
                    for y in tags:
                        for z in t:
                            if z == y :
                                count = count + 1
                                if count == 3:
                                    print(f"{title} by {a}, {yr}\n")
                                    found = True
                                    break
                        if found == True : break
            h5.close()