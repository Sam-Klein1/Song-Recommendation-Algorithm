import os
import glob
import hdf5_getters
import print_all_songs
import find_song
import find_song_artist
import find_tags
import similarTags

DB_DIR = "./MillionSongSubset"

input_song = input("Enter a song: ")
input_artist = input("Enter artist: ")
#print_all_songs.print_all_songs()
if find_song.find_song(input_song):
    print("song found!")
if find_song_artist.find_song_artist(input_song, input_artist):
    tags = find_tags.find_tags(input_song, input_artist)
    similarTags.similarTags(input_song, input_artist, tags)


