import os
import glob
import hdf5_getters

DB_DIR = "./MillionSongSubset"

for root, dirs, files in os.walk(DB_DIR):
    files = glob.glob(os.path.join(root, "*" + ".h5"))
    for f in files:
        h5 = hdf5_getters.open_h5_file_read(f)
        title = hdf5_getters.get_title(h5)
        print(title)
        h5.close()
