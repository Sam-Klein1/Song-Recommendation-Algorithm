import os
import glob
import hdf5_getters
import print_all_songs
import find_song

DB_DIR = "./MillionSongSubset"

input_song = input("Enter a song: ")
# print_all_songs.print_all_songs()
if find_song.find_song(input_song):
    print("song found!")



