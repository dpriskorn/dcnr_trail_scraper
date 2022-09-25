# DCNR trail scraper

This was a quick project to get the data out in a form that enables me to easily upload it to Wikidata using OpenRefine.
I'll need to reconcile all the counties and names of the trails.

In the end this harvested 630 hiking trails.

See trails.jsonl for the result.

## What I learned from this project
* async programming is nice, but I found it too complicated for a small project like this
* it took only an hour for 800 requests
* the time of development was low compared to the gain and perhaps the code can be reused
* OpenRefine does NOT support jsonl so CSV would have been a better choice for output format