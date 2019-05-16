

import json
from pprint import pprint
import os

print(os.getcwd())

def str_to_list(string):
    string = string.replace('[','')
    string = string.replace(']','')
    str_list = string.split(',')
    return [int(idx) for idx in str_list if idx]


def get_clean_actor(filename):
    
    with open(filename) as data_file:    
        actors = json.load(data_file)
        clean_actors = []
        
        for actor in actors:
            actor['fields']['filmography'] = actor['fields']['filmogaphy']
            if type(actor['fields']['filmogaphy']) != type("ABC"):
                actor['fields']['filmography'] = ''
            actor['fields'].pop('filmogaphy')

            clean_actors.append(actor)            
    
    with open("clean_"+filename, 'w', encoding="utf-8") as fp:
        json.dump(clean_actors, fp, ensure_ascii=False, indent="\t")
        
get_clean_actor('actor_진짜마지막.json')