

import json
from pprint import pprint
import os

print(os.getcwd())

def str_to_list(string):
    string = string.replace('[','')
    string = string.replace(']','')
    str_list = string.split(',')
    return [int(idx) for idx in str_list if idx]


def get_clean_json(filename):
    
    with open(filename) as data_file:    
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
            
            duration = processed_movie['fields'].get('duration')
            if duration:
                processed_movie['fields']['duration'] = int(duration.split('.')[0])
                
            
            print(processed_movie)
    
    with open("clean_"+filename, 'w', encoding="utf-8") as fp:
        json.dump(processed_movies, fp, ensure_ascii=False, indent="\t")
        
get_clean_json('movie_진짜마지막.json')