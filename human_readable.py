from json import load
from typing import Dict

JSON_FILE = "output_ol.json"

with open(JSON_FILE) as input_file:
    results: Dict[str, str] = load(input_file)

    l = []
    for result in results:
        if result["rating"]: l.append(f'{result["author"].ljust(25)} - {result["title"].ljust(40)}; {result["rating"]}\n')
    
    with open(f"hr_{JSON_FILE.removesuffix('.json')}.txt", "w") as human_readable_file:
        human_readable_file.writelines(l)