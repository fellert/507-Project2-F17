# coding=utf-8
# SI 507 F17 Project 2 - Objects
# Ethan Ellert
# September 30, 2017

import requests
import json
import unittest
import csv

print("\n*** *** PROJECT 2 *** ***\n")


def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


def sample_get_cache_itunes_data(search_term, media_term="all"):
    CACHE_FNAME = 'cache_file_name.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    baseurl = "https://itunes.apple.com/search"
    params = {}
    params["media"] = media_term
    params["term"] = search_term
    unique_ident = params_unique_combination(baseurl, params)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        CACHE_DICTION[unique_ident] = json.loads(requests.get(baseurl,
                                                 params=params).text)
        full_text = json.dumps(CACHE_DICTION)
        cache_file_ref = open(CACHE_FNAME, "w")
        cache_file_ref.write(full_text)
        cache_file_ref.close()
        return CACHE_DICTION[unique_ident]


# [PROBLEM 1] [250 POINTS]
print("\n***** PROBLEM 1 *****\n")


class Media(object):

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.title = self.dictionary["trackName"]
        self.author = self.dictionary["artistName"]
        self.itunes_URL = self.dictionary["trackViewUrl"]
        self.itunes_id = self.dictionary["trackId"]

    def __str__(self):
        return "%s by %s" % (self.title, self.author)  # "Song by Artist"

    def __repr__(self):
        return "ITUNES MEDIA: %s" % (self.itunes_id)  # ITUNES MEDIA: ID

    def __len__(self):
        return 0

    def __contains__(self, item):
        if str(item) in str(self.title):
            return True


# [PROBLEM 2] [400 POINTS]
print("\n***** PROBLEM 2 *****\n")


class Song(Media):

    def __init__(self, dictionary):
        Media.__init__(self, dictionary)  # inherits Media class
        self.album = self.dictionary["collectionName"]
        self.track_number = self.dictionary["trackNumber"]
        self.genre = self.dictionary["primaryGenreName"]

    def __len__(self):
        time = self.dictionary["trackTimeMillis"] // 1000  # ms to seconds
        return time


class Movie(Media):

    def __init__(self, dictionary):
        Media.__init__(self, dictionary)  # inherits Media class
        self.rating = self.dictionary["contentAdvisoryRating"]
        self.genre = self.dictionary["primaryGenreName"]
        if len(str(self.dictionary["longDescription"])) == 0:
            self.description = None  # if description does not exist
        else:
            self.description = dictionary["longDescription"]

    def __len__(self):
        if "trackTimeMillis" in self.dictionary:
            time = self.dictionary["trackTimeMillis"] // 1000 // 60
            return time
        else:
            return 0  # in case of KeyErrors becuase time does not exist

    def title_words_num():
        if self.description is None:
            return 0
        else:
            return len(self.description)


# [PROBLEM 3] [150 POINTS]
print("\n***** PROBLEM 3 *****\n")

media_samples = sample_get_cache_itunes_data("love")["results"]

song_samples = sample_get_cache_itunes_data("love", "music")["results"]

movie_samples = sample_get_cache_itunes_data("love", "movie")["results"]

# iterates through each list above and creates/stores respective objects
media_list = [Media(instance) for instance in media_samples]
song_list = [Song(instance) for instance in song_samples]
movie_list = [Movie(instance) for instance in movie_samples]


# [PROBLEM 4] [200 POINTS]
print("\n***** PROBLEM 4 *****\n")

# Each of the three CSV files contains 5 columns each:
# - title
# - artist
# - id
# - url (for the itunes url of that thing --
#   the url to view that track of media on iTunes)
# - length

media = open("media.csv", "w")
media.write("Title, Artist, ID, URL, Length\n")
for item in media_list:
    # include " " around title, which sometimes includes commas
    media.write('"{}", {}, {}, {}, {}\n'.format(item.title, item.author,
                                                item.itunes_id,
                                                item.itunes_URL,
                                                len(item)))
media.close()

songs = open("songs.csv", "w")
songs.write("Title, Artist, ID, URL, Length(seconds)\n")
for song in song_list:
    songs.write('"{}", {}, {}, {}, {}\n'.format(song.title, song.author,
                                                song.itunes_id,
                                                song.itunes_URL,
                                                len(song)))
songs.close()

movies = open("movies.csv", "w")
movies.write("Title, Artist, ID, URL, Length(minutes)\n")
for movie in movie_list:
    movies.write('"{}", {}, {}, {}, {}\n'.format(movie.title, movie.author,
                                                 movie.itunes_id,
                                                 movie.itunes_URL,
                                                 len(movie)))
movies.close()
