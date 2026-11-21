[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/musegaming62/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/musegaming62/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

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

## Stories

36 stories in total (3 heroes + 33 in the grid), across the Americas, Europe, Asia-Pacific, the Middle East and Africa, and across conflict, diplomacy, economy, tech, science, health, sport, justice and climate.

Hero stories:

1. Russia's biggest strike of the year hits Kyiv — and spills into Poland
2. Markets sink as the AI trade unwinds (S&P 500 -3.7%, Nikkei -5.1%)
3. Hormuz on edge: blockade, burning tankers, record energy shock

The full numbered list, with a one-line summary, region, topic and source per story, is in `STORIES-20NOV.md`.
