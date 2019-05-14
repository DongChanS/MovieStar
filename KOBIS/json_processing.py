

import json
from pprint import pprint
import os

print(os.getcwd())

def str_to_list(string):
    string = string.replace('[','')
    string = string.replace(']','')
    str_list = string.split(',')
    return [int(idx) for idx in str_list if idx]



with open('movies_result.json') as data_file:    
    movies = json.load(data_file)
    processed_movies = []
    for movie in movies:
        processed_movie = movie
        genres = processed_movie['fields'].get('genres')
        actors = processed_movie['fields'].get('actors')
        if genres:
            processed_movie['fields']['genres'] = str_to_list(genres)
        
        if actors:
            processed_movie['fields']['actors'] = str_to_list(actors)
        processed_movies.append(processed_movie)
        print(processed_movie)

with open('movies.json', 'w', encoding="utf-8") as fp:
    json.dump(processed_movies, fp, ensure_ascii=False, indent="\t")