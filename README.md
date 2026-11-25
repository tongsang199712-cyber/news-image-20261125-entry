# news-image-20261125-entry

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/tongsang199712-cyber/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/tongsang199712-cyber/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image summing up the world's news of **Wednesday 25 November 2026** — drawn
entirely in code, no photographs. Lead story: the CIA and ODNI cyber breach of
their open-source intelligence system, first reported by the NYT and confirmed
by CNN. Also inside: Huawei convicted in the US on 10 of 12 counts, Zelenskiy
confirming Ukraine hit Russian ships in the Gulf of Finland and off Libya,
the WHO evacuating its Ebola hospital in DR Congo, a Houthi drone hitting
Riyadh's tallest tower — plus Giuliani's Medal of Freedom, the Dow topping
50,000, the Colombia hostage siege and England levelling the T20 series.

## Run it

```sh
python3 main.py   # writes entry.png to /output (or $MAKEFUN_OUTPUT_DIR)
```

`main.py` draws the image deterministically with the Python standard library
only — a small built-in 5x7 bitmap font, a tiny raster canvas and a hand-rolled
PNG encoder. Same code, same bytes, every run; no network, no fonts on disk.

## The files

- `main.py`: the program (Python 3, standard library only).
- `entry.png`: the image as drawn by `main.py` (1024×1024, about 21 KB).
- `LICENSE`: MIT.

## Sources

Wire and press reports of 25 November 2026 (NYT, CNN, Reuters, AP, WHO).
The Huawei verdict was delivered late on 24 November US time and reported
worldwide on the 25th; every other headline story was first reported on
25 November itself. Built early on the 25th (UTC), so the image covers the
stories reported by then — a later run may rebuild with the full day's news
before the deadline.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dd7e8ra1&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
