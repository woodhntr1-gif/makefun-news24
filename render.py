#!/usr/bin/env python3
"""Render the news-image-20261124 front page (1024x1024 PNG) at build time.

Draws a newspaper front page summing up Tuesday 24 November 2026:
hero = Western intelligence warning that Russia could launch the
nuclear-armed "Sputnik-S" satellite within weeks, with NATO's vow to
defend space and the Kremlin's denial; six story cards below; a
one-liner ticker at the foot. Deterministic: fixed coordinates, a
fixed-seed star field, no randomness, no network, no external images.
Run: python3 render.py -> entry.png
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent

PAPER = (244, 239, 228)
INK = (24, 24, 24)
RED = (178, 34, 28)
NAVY = (16, 36, 64)
SKY = (10, 18, 38)
STAR = (235, 238, 245)
EARTH_BLUE = (38, 84, 150)
EARTH_LIGHT = (90, 140, 205)
GOLD = (212, 164, 62)
GREY = (110, 108, 100)
CARD_BG = (255, 255, 255)
CARD_LINE = (158, 155, 145)
TICKER_BG = (16, 36, 64)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_hero(d, x0, y0, w, h):
    """Night sky over Earth: stars, orbit rings around the satellite."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    rng = random.Random(20261124)
    for _ in range(110):
        sx = x0 + rng.randint(4, w - 4)
        sy = y0 + rng.randint(4, h - 130)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=STAR)
    # Earth arc at the bottom of the hero
    d.ellipse([x0 - 220, y0 + h - 130, x0 + w + 220, y0 + h + 620],
              fill=EARTH_BLUE)
    d.ellipse([x0 - 180, y0 + h - 150, x0 + w + 180, y0 + h + 560],
              outline=EARTH_LIGHT, width=4)
    for cx, cy, cw, ch in [(180, 400, 150, 16), (560, 430, 190, 14),
                           (820, 405, 120, 12)]:
        d.ellipse([x0 + cx, y0 + cy, x0 + cx + cw, y0 + cy + ch],
                  fill=(200, 220, 240))
    # satellite, right side
    bx, by = x0 + 700, y0 + 150
    # orbit rings centred on the satellite: they stay clear of the
    # headline and subhead on the left (old full-width ellipse crossed
    # the masthead and the headline, so it is gone)
    cx, cy = bx + 60, by + 25
    d.ellipse([cx - 240, cy - 105, cx + 240, cy + 105],
              outline=(120, 140, 190), width=2)
    d.ellipse([cx - 222, cy - 90, cx + 222, cy + 90],
              outline=(120, 140, 190), width=1)
    # red warning glow behind the satellite
    d.ellipse([bx - 70, by - 70, bx + 230, by + 90], outline=RED, width=3)
    d.ellipse([bx - 46, by - 46, bx + 206, by + 66], outline=RED, width=1)
    # solar panels
    d.rectangle([bx - 130, by + 8, bx - 8, by + 42], fill=(30, 60, 110),
                outline=(140, 170, 220), width=2)
    d.rectangle([bx + 128, by + 8, bx + 250, by + 42], fill=(30, 60, 110),
                outline=(140, 170, 220), width=2)
    for gx in range(bx - 130, bx - 8, 20):
        d.line([gx, by + 8, gx, by + 42], fill=(140, 170, 220), width=1)
    for gx in range(bx + 128, bx + 250, 20):
        d.line([gx, by + 8, gx, by + 42], fill=(140, 170, 220), width=1)
    # body
    d.rectangle([bx, by, bx + 120, by + 50], fill=(200, 200, 205),
                outline=(120, 120, 125), width=2)
    d.rectangle([bx + 8, by + 8, bx + 112, by + 20], fill=GOLD)
    # dish
    d.ellipse([bx + 40, by - 34, bx + 80, by + 6], outline=(220, 220, 225),
              width=3)
    d.line([bx + 60, by, bx + 60, by + 12], fill=(220, 220, 225), width=3)
    # nuclear warhead cone on top
    d.polygon([(bx + 30, by), (bx + 90, by), (bx + 60, by - 58)],
              fill=RED, outline=(255, 120, 100))


def card(d, x, y, w, h, kicker, headline, body, head_size=22):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_LINE, width=1)
    d.rectangle([x, y, x + w, y + 4], fill=RED)
    yy = y + 14
    d.text((x + 12, yy), kicker, font=font(F_SANS_B, 13), fill=RED)
    yy += 22
    yy = block(d, x + 12, yy, wrap(d, headline, font(F_SERIF_B, head_size),
                                   w - 24), font(F_SERIF_B, head_size), INK,
               head_size + 4)
    yy += 4
    # body: largest size that still fits in four lines, so no card ever
    # ends mid-sentence
    for size in (16, 15, 14):
        lines = wrap(d, body, font(F_SANS, size), w - 24)
        if len(lines) <= 4:
            break
    block(d, x + 12, yy, lines[:4], font(F_SANS, size), (60, 60, 60),
          size + 5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 64], fill=NAVY)
    d.text((28, 14), "THE WORLD IN ONE IMAGE",
           font=font(F_SERIF_B, 26), fill=(255, 255, 255))
    d.text((1024 - 28 - d.textlength("TUESDAY 24 NOVEMBER 2026",
                                     font=font(F_SANS_B, 18)), 20),
           "TUESDAY 24 NOVEMBER 2026", font=font(F_SANS_B, 18),
           fill=(200, 210, 230))
    d.rectangle([0, 64, W, 68], fill=RED)

    # hero
    draw_hero(d, 0, 68, W, 420)
    # the Earth arc spills past the hero: restore paper below it
    d.rectangle([0, 488, W, 952], fill=PAPER)
    d.text((28, 92), "INTEL WARNS", font=font(F_SANS_B, 20), fill=GOLD)
    y = block(d, 28, 122,
              wrap(d, "NUCLEAR SATELLITE IN ORBIT?",
                   font(F_SERIF_B, 46), 620),
              font(F_SERIF_B, 46), (255, 255, 255), 52)
    y += 6
    block(d, 28, y,
          wrap(d, "Russia could launch 'Sputnik-S' within weeks, "
                  "Western intelligence says — NATO vows to defend "
                  "space; Kremlin denies it.",
               font(F_SANS, 19), 520),
          font(F_SANS, 19), (215, 222, 235), 25)

    # grid: 3 columns x 2 rows
    gx, gy = 28, 508
    cw, ch, gap = 304, 202, 16
    cards = [
        ("IRAN", "Qatar talks as war fears grow",
         "Vance and Rubio met Qatar's PM; Netanyahu urges strikes. "
         "Iran vows to confront the blockade. Qatar mediated the "
         "stalled talks."),
        ("GAZA", "Hamas security chief killed",
         "Israeli strikes kill Hamas security chief Naeem Abu Nahel "
         "and six others, two of them police. A day earlier, three "
         "more died, including a UNRWA worker."),
        ("UKRAINE", "Zaporizhzhia hit overnight",
         "A Russian attack kills 2 and wounds 40, including four "
         "children. Governor Semikin says an apartment building was "
         "struck overnight."),
        ("ESTONIA", "Russia warns of 'open war'",
         "Moscow says Estonia's moves are on the verge of triggering "
         "open war, after Tallinn closed its land border. Estonia is "
         "a NATO and EU member."),
        ("CIKANDE", "Fire toll rises to 26",
         "Police open a criminal-negligence probe; 19 witnesses "
         "questioned. 16 identified, 10 need DNA; 8–28 still missing. "
         "Most victims were found on the second floor."),
        ("MYANMAR", "World backs Rohingya verdict",
         "Fourteen countries recognise the ICJ genocide ruling. The "
         "UK sanctions five senior Myanmar generals. The ruling found "
         "genocide against the Rohingya in 2017."),
    ]
    for i, (kick, head, body) in enumerate(cards):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        card(d, cx, cy, cw, ch, kick, head, body)

    # ticker
    d.rectangle([0, 952, W, H], fill=TICKER_BG)
    ticker = ("NEPAL 5.6 QUAKE  •  OREGON & VIRGINIA SUE SPACEX OVER GROK "
              "IMAGES  •  SOLOMON ISLANDS ENDS CHINA PACT  •  SEOUL OFFERS "
              "$375,000 TO CATCH AI CHEATS  •  CHINA OPENS TIANGONG TO "
              "PAKISTANI ASTRONAUT  •  CAR BOMB DESTROYS BUILDINGS IN "
              "VILLAVICENCIO")
    block(d, 28, 962, wrap(d, ticker, font(F_SANS_B, 15), W - 56),
          font(F_SANS_B, 15), (225, 230, 240), 20)

    out = HERE / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
