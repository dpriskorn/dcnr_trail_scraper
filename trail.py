from typing import List

from pydantic import BaseModel


class Trail(BaseModel):
    label: str
    trail_id: int
    difficulty: str
    length: float
    description = "hiking trail in Pennsylvania"
    counties: List[str]
    website: str
    counties_string: str = ""
    pa_trails_url: str = ""

    @property
    def trail_url(self):
        return f"https://trails.dcnr.pa.gov/trails/trail/trailview?trailkey={self.trail_id}"

    def write_to_file(self):
        #console.print("Writing to file")
        with open("trails.jsonl", "a") as file:
            file.write(f"{self.dict()}\n")

    def parse_counties(self):
        counties = []
        for county in self.counties:
            counties.append(f"{county.strip(',')} County")
        self.counties_string = ";".join(counties)

    def generate_url(self):
        self.pa_trails_url = self.trail_url