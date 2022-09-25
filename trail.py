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

    def trail_url(self):
        return f"https://trails.dcnr.pa.gov/trails/trail/trailview?trailkey={self.trail_id}"

    def write_to_file(self):
        #console.print("Writing to file")
        with open("trails.jsonl", "a") as file:
            file.write(f"{self.dict()}\n")
