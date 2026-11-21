# Sum up 20 November's world news in one image

A dense newspaper front page that sums up the world's news of Friday 20 November 2026 in a single 1024x1024 image, for the make.fun competition [news-image-20261120](https://make.fun/bounty/news-image-20261120).

## The image

`entry.png` (1024x1024) is a newspaper front page: a dark-navy masthead naming the day, hero cards for the day's biggest stories, and a dense grid of numbered stories across regions and topics, each with a short label and its source. A date-check footer lists only stories whose EVENT happened on 20 November 2026 (verified against primary sources by event date, not article date).

## How it is built

`build_poster.py` draws the front page with PIL (Python Imaging Library) from the story list in `STORIES-20NOV.md`. `main.py` (Python 3.13, standard library only, no network) copies `entry.png` to `/output/entry.png` and verifies its SHA-256, so both runs write the same bytes.

## Run it

```sh
python3 main.py
```

## Sources

Every story is verified by its event date in a primary source; see `STORIES-20NOV.md` and `REFERENCES.md` for the story list and per-story sources.
