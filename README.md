# Saturday 21 November 2026 — in one picture

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Notodirdjo/news-image-21-nov/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Notodirdjo/news-image-21-nov/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image that sums up Saturday 21 November 2026's world news, drawn
as a newspaper front page. This is an entry for the make.fun
competition [news-image-20261121](https://make.fun/bounty/news-image-20261121).

## What the picture shows

28 stories from 7 regions, every one checked against reporting from
21 November 2026. The five lead stories:

- **Antalya** — COP31 talks run into overtime with no deal, the draft
  still silent on fossil fuels.
- **Riyadh** — Saudi defences down three Houthi missiles over the
  capital, the second attack in three days.
- **Kryvyi Rih** — a Russian strike kills a seven-year-old boy and a
  paramedic; 58 are hurt, and Kyiv is hit again.
- **Junín** — a 6.7-magnitude quake shakes central Peru, felt in Lima.
- **Markets** — stocks sink worldwide as AI doubts spread: the S&P 500
  falls 3.7% into correction, the Nasdaq 5.3%.

Then "THE DAY IN BRIEF": tankers hit near the Strait of Hormuz,
Mexico's capture of cartel boss 'El Chapo Isidro', a boat capsizing in
Nigeria, UN talks on 'killer robots', a dengue breakthrough in Brazil,
the FBI's NCIC hack probe, a deadly power station fire in Basra,
Trump's 10% credit card cap vow, Bayer's $7.25bn Roundup settlement,
youth protests across Europe, and ten more — plus an "ALSO TODAY" line.

## How it works

`draw.py` renders `entry.png` (1024x1024) with Pillow from the verified
facts in the brief — real text, no AI-generated imagery. `main.py`
(Python 3.13, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` and checks the copy byte for byte.
It needs no network and writes identical bytes on every run.

```sh
python3 draw.py        # render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
