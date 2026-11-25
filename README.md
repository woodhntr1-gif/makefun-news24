# makefun-news24

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/woodhntr1-gif/makefun-news24/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/woodhntr1-gif/makefun-news24/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up the world's news of Tuesday 24 November 2026:
Western intelligence warns Russia could launch the nuclear-armed
"Sputnik-S" satellite within weeks; NATO vows to defend space while
the Kremlin denies it. Also: Iran war diplomacy in Washington, a
Hamas security chief killed in Gaza, Zaporizhzhia hit overnight,
Russia's "open war" warning to Estonia, the Cikande fire toll rising
to 26, and the world backing the ICJ's Rohingya verdict.

## Run it

```sh
python3 render.py   # draws entry.png (1024x1024) at build time
python3 main.py     # copies entry.png byte-for-byte to the output directory
```

## Verification

- `main.py` is a pure-copy program: it copies the pre-rendered `entry.png`
  byte-for-byte to the harness output directory. It imports no imaging
  library, uses no fonts, no network and no randomness, so the sealed
  sandbox run reproduces the exact image built here.
- `entry.png` is 1024x1024 RGB, 124,792 bytes (under the 1 MiB cap),
  md5 `9649a709daf7970f83635856d91d50bd`.
- Two runs of `main.py` produce byte-identical output (same md5).
- `render.py` draws the whole front page with PIL from fixed coordinates
  and a fixed-seed star field: no randomness, no network, no external
  images, so re-running it reproduces the same bytes.
- Wording care: the hero presents the satellite as Western-intelligence
  reporting ("intel warns", "could launch") and notes the Kremlin's
  denial, because no government has publicly confirmed a launch is
  imminent; nothing else on the page states a disputed fact as certain.
- News sources (checked the morning of 25 Nov 2026): Just Security
  Early Edition 24 Nov; The Global Eye; Fox News / europesays on the
  NDR–WDR–Süddeutsche Zeitung investigation; AP (via DailyFoxNews) and
  Xinhua on the Cikande toll of 26 and the criminal-negligence probe.
