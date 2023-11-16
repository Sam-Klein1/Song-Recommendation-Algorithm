import os
import glob
import hdf5_getters

DB_DIR = "./MillionSongSubset"

def print_all_metadata():
    for root, dirs, files in os.walk(DB_DIR):
        files = glob.glob(os.path.join(root, "*" + ".h5"))
        for f in files:
            h5 = hdf5_getters.open_h5_file_read(f)
            for getter_name in dir(hdf5_getters):
                if callable(getattr(hdf5_getters, getter_name)) and not getter_name.startswith("__"):
                    try:
                        result = getattr(hdf5_getters, getter_name)(h5)
                        print(f"{getter_name}: {result}\n")
                    except Exception as e:
                        print(f"Error in {getter_name}: {e}")
            h5.close()

print_all_metadata()
