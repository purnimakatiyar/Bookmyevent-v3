import json
from os import path

queries = None
prompts = None
menu = None
constants = None

path_current_directory = path.dirname(__file__)
 

filepath = path.join(path_current_directory , "../config.json")

with open(filepath, "r") as file:
    get_data = json.load(file)
    queries = get_data["queries"]
    menu = get_data["menu"]
    prompts = get_data["prompts"]
    constants = get_data["constants"]
