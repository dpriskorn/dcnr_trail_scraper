import logging
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from requests import Session

logger = logging.getLogger(__name__)

class Difficulty(Enum):
    UNKNOWN = "Unknown"



class Trail(BaseModel):
    label: str
    trail_id: int
    difficulty: Difficulty
    length: float
    description = "hiking trail in Pennsylvania"
    county: str


class MissingInformationError(BaseException):
    pass


class DcnrScraper(BaseModel):
    trails: List[Trail] = []

    def start(self):
        session = Session()
        for i in range(0, 10):
            url = f"https://trails.dcnr.pa.gov/trails/trail/trailview?trailkey={i}"
            response = session.get(url)
            if response.status_code == 200:
                print("got 200")
                soup = BeautifulSoup(response.text)
                h1 = soup.select_one("h1")
                if h1:
                    label = h1.text
                    print(label)
                else:
                    raise MissingInformationError("no h1")
                difficulty_span = soup.select_one("#difficulty")
                if difficulty_span:
                    difficulty = difficulty_span.text
                    print(difficulty)
                else:
                    raise MissingInformationError("no difficulty")
                length_span = soup.select_one("#length")
                if length_span:
                    length = length_span.text
                    print(length)
                else:
                    raise MissingInformationError("no length")
                county_wrapper_span = soup.select_one("#county-wrapper")
                if county_wrapper_span:
                    county = county_wrapper_span.text
                    print(county)
                else:
                    raise MissingInformationError("no county-wrapper")
                trail = Trail(
                    label=label,
                    trail_id=i,
                    difficulty=Difficulty(difficulty),
                    length=length,
                    county=county
                )
                self.trails.append(trail)
                print(trail.dict())
            else:
                pass
                # print(f"got {response.status_code}")
