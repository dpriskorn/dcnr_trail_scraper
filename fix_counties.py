#read the trails2.json into Trail objects
import json

from dcnr_scraper import console
from trail import Trail

trails = []
with open("trails2.jsonl", "r") as file:
    for line in file.readlines():
        #print(line)
        data = json.loads(line)
        trail = Trail(**data)
        trails.append(trail)
print(len(trails))
with open("trails3.jsonl", "w") as file:
    for trail in trails:
        trail.parse_counties()
        trail.generate_url()
        file.write(f"{trail.json()}\n")
        #console.print(trail)
        #exit()