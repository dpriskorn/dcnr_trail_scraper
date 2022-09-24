import logging
from enum import Enum
from typing import List

from rich.console import Console
from bs4 import BeautifulSoup
from pydantic import BaseModel
from requests import Session

logger = logging.getLogger(__name__)
console = Console()


# class Difficulty(Enum):
#     UNKNOWN = "Unknown"


class Trail(BaseModel):
    label: str
    trail_id: int
    difficulty: str
    length: float
    description = "hiking trail in Pennsylvania"
    counties: List[str]
    website: str

    @property
    def trail_url(self):
        return f"https://trails.dcnr.pa.gov/trails/trail/trailview?trailkey={i}"


class MissingInformationError(BaseException):
    pass


class DcnrScraper(BaseModel):
    trails: List[Trail] = []

    def start(self):
        session = Session()
        for i in range(0, 1000):
            url = f"https://trails.dcnr.pa.gov/trails/trail/trailview?trailkey={i}"
            response = session.get(url)
            if response.status_code == 200:
                # print("got 200")
                soup = BeautifulSoup(response.text)
                h1 = soup.select_one("h1")
                if h1:
                    label = h1.text
                    # print(label)
                else:
                    raise MissingInformationError("no h1")
                difficulty_span = soup.select_one("#difficulty")
                if difficulty_span:
                    difficulty = difficulty_span.text
                    # print(difficulty)
                else:
                    raise MissingInformationError("no difficulty")
                length_span = soup.select_one("#length")
                if length_span:
                    length = float(length_span.text.replace(" Miles", ""))
                    # print(length)
                else:
                    raise MissingInformationError("no length")
                div_county = soup.select_one("#county-wrapper")
                if div_county:
                    counties = []
                    county_wrapper_spans = div_county.select(".county-wrapper")
                    if len(county_wrapper_spans):
                        for county in county_wrapper_spans:
                            counties.append(county.text)
                        #console.print(counties)
                else:
                    raise MissingInformationError("no county-wrapper")
                link = soup.select_one("a.trail-site-link")
                if link:
                    website = link["href"]
                else:
                    raise MissingInformationError(f"no link, see {url}")
                trail = Trail(
                    label=label,
                    trail_id=i,
                    difficulty=difficulty,
                    length=length,
                    counties=counties,
                    website=website
                )
                self.trails.append(trail)
                console.print(trail.dict())
            else:
                pass
                # print(f"got {response.status_code}")

    def write_trails_to_jsonl_file(self):
        console.print("Writing to file")
        with open("trails.jsonl", "w") as file:
            for trail in self.trails:
                file.write(f"{trail.dict()}\n")