#!/usr/bin/env python3
"""Render Saturday 21 November 2026 as a one-page newspaper front.

The page carries five lead stories with a short summary each, a
two-column digest of twenty more stories, and a closing line of three
extras. All wording comes from the competition brief's verified facts.

Usage: python3 draw.py  — writes entry.png next to this script.
The picture is 1024 by 1024 pixels and stays under 1 MiB.
"""

import hashlib
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "entry.png")

SIDE = 1024
EDGE = 40

SHEET = (247, 243, 234)
INK = (24, 24, 24)
BODY_INK = (52, 52, 52)
MUTED = (90, 88, 80)
NAVY = (20, 38, 74)
ACCENT = (178, 34, 34)
GUIDE = (150, 148, 138)
FOOT = (232, 228, 218)
WHITE = (255, 255, 255)

DEJAVU = "/usr/share/fonts/truetype/dejavu"
BOLD_PATH = os.path.join(DEJAVU, "DejaVuSans-Bold.ttf")
PLAIN_PATH = os.path.join(DEJAVU, "DejaVuSans.ttf")


def typeface(bold, size):
    path = BOLD_PATH if bold else PLAIN_PATH
    return ImageFont.truetype(path, size)


def fit_lines(canvas, text, face, width):
    """Wrap text to the given pixel width, word by word."""
    out = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if canvas.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


LEAD_STORIES = [
    ("ANTALYA", (107, 33, 168),
     "COP31 talks run into overtime with no deal",
     "Negotiators work through Saturday after the draft deal dropped "
     "all mention of fossil fuels. The EU says it is 'a good deal "
     "or no deal'."),
    ("RIYADH", (15, 118, 110),
     "Saudi defences down three Houthi missiles over Riyadh",
     "Air defences intercepted three ballistic missiles early on "
     "Saturday, the second attack on the capital in three days. "
     "No one was hurt."),
    ("KRYVYI RIH", (31, 58, 95),
     "Russian strike kills a boy of seven and a paramedic",
     "Two ballistic missiles hit near a restaurant in Zelenskyy's "
     "home city on Friday evening; 58 were hurt. Kyiv was attacked "
     "again early on Saturday."),
    ("JUN\u00cdN", (185, 28, 28),
     "6.7-magnitude quake shakes central Peru",
     "The tremor struck the Andean region of Jun\u00edn on Friday "
     "evening and was felt in Lima, sending residents into the "
     "streets. No deaths were reported."),
    ("MARKETS", (22, 101, 52),
     "Stocks sink worldwide as AI doubts spread",
     "The S&P 500 fell 3.7% into correction and the Nasdaq lost "
     "5.3%, wiping out its gains for the year. Japan's Nikkei "
     "fell 5.1%."),
]

DIGEST_LEFT = [
    ("HORMUZ", (15, 118, 110), "Two tankers hit near the strait"),
    ("SINALOA", (185, 28, 28), "Cartel boss 'El Chapo Isidro' seized; 11 dead"),
    ("BAYELSA", (31, 58, 95), "Boat to a funeral capsizes; 24 dead"),
    ("GENEVA", (107, 33, 168), "'Killer robot' talks end with two-year plan"),
    ("BRAZIL", (22, 101, 52), "Wolbachia mosquitoes cut dengue by 69%"),
    ("USA", (20, 38, 74), "FBI probes hack of its NCIC crime database"),
    ("BASRA", (185, 28, 28), "Power station fire kills 4, injures 30"),
    ("WASHINGTON", (20, 38, 74), "Trump vows 10% cap on card interest"),
    ("MISSOURI", (22, 101, 52), "Bayer's $7.25bn Roundup deal approved"),
    ("EUROPE", (107, 33, 168), "Youth protests continue after walkouts"),
]

DIGEST_RIGHT = [
    ("FLORIDA", (15, 118, 110), "Storms bring historic flooding"),
    ("TIRANA", (185, 28, 28), "Thunberg joins march demanding PM resign"),
    ("KYIV", (31, 58, 95), "UK defence chief backs Ukraine in Kyiv"),
    ("LONDON", (107, 33, 168), "Princess Catherine on life after cancer"),
    ("VIRGINIA", (22, 101, 52), "Child is state's first measles death"),
    ("SAN FRANCISCO", (15, 118, 110), "City braces for massive tides"),
    ("LOS ANGELES", (185, 28, 28), "Man guilty of starting Palisades fire"),
    ("BARCELONA", (22, 101, 52), "Cancer pill shrank tumours in 6 in 10"),
    ("OTTAWA", (31, 58, 95), "Taiwan warns Canada over China risks"),
    ("INDONESIA", (107, 33, 168), "Massive forest fires burn on"),
]

CLOSING = (
    "ALSO TODAY:  State funeral for Mlambo-Ngcuka  \u00b7  "
    "Mets sign Ewing for $95m  \u00b7  Endurance swim in the Strait of Hormuz"
)


def lead_block(canvas, top, tag, colour, headline, summary, width, last):
    """Draw one lead story; return the y where the next block starts."""
    tag_face = typeface(True, 20)
    head_face = typeface(True, 27)
    body_face = typeface(False, 20)
    canvas.rectangle([EDGE, top + 3, EDGE + 11, top + 14], fill=colour)
    canvas.text((EDGE + 19, top), tag, font=tag_face, fill=colour, anchor="la")
    y = top + 26
    head_width = canvas.textlength(headline, font=head_face)
    assert head_width <= width, "headline overflows: " + headline
    canvas.text((EDGE, y), headline, font=head_face, fill=INK, anchor="la")
    y += 33
    lines = fit_lines(canvas, summary, body_face, width)
    assert len(lines) <= 2, "summary overflows: " + summary
    for line in lines:
        canvas.text((EDGE, y), line, font=body_face, fill=BODY_INK, anchor="la")
        y += 22
    y += 6
    if not last:
        canvas.line([EDGE, y, SIDE - EDGE, y], fill=GUIDE, width=1)
        y += 6
    return y


def digest(canvas, top):
    """Draw the two-column digest; return the y below it."""
    head_face = typeface(True, 21)
    canvas.text((EDGE, top), "THE DAY IN BRIEF", font=head_face,
                fill=ACCENT, anchor="la")
    y = top + 28
    tag_face = typeface(True, 15)
    item_face = typeface(False, 15)
    span = (SIDE - 2 * EDGE - 24) // 2
    for x0, items in ((EDGE, DIGEST_LEFT),
                      (EDGE + span + 24, DIGEST_RIGHT)):
        row = y
        for tag, colour, head in items:
            label = tag + " \u2014 "
            label_w = canvas.textlength(label, font=tag_face)
            canvas.text((x0, row), label, font=tag_face, fill=colour, anchor="la")
            canvas.text((x0 + label_w, row), head, font=item_face,
                        fill=INK, anchor="la")
            row += 20
    return y + 10 * 20


def render():
    page = Image.new("RGB", (SIDE, SIDE), SHEET)
    canvas = ImageDraw.Draw(page)
    width = SIDE - 2 * EDGE

    canvas.rectangle([0, 0, SIDE, 96], fill=NAVY)
    masthead = typeface(True, 52)
    canvas.text((SIDE / 2, 24), "THE WORLD IN ONE DAY", font=masthead,
                fill=WHITE, anchor="ma")

    canvas.rectangle([0, 96, SIDE, 101], fill=ACCENT)
    day_face = typeface(True, 36)
    canvas.text((SIDE / 2, 110), "Saturday 21 November 2026", font=day_face,
                fill=NAVY, anchor="ma")
    count_face = typeface(False, 18)
    canvas.text((SIDE / 2, 148), "28 stories  \u00b7  7 regions",
                font=count_face, fill=MUTED, anchor="ma")
    canvas.line([EDGE, 178, SIDE - EDGE, 178], fill=GUIDE, width=2)

    y = 188
    for index, (tag, colour, headline, summary) in enumerate(LEAD_STORIES):
        y = lead_block(canvas, y, tag, colour, headline, summary,
                       width, index == len(LEAD_STORIES) - 1)

    y = digest(canvas, y)

    foot_top = y + 4
    canvas.rectangle([0, foot_top, SIDE, SIDE], fill=FOOT)
    canvas.line([0, foot_top, SIDE, foot_top], fill=NAVY, width=3)
    foot_face = typeface(False, 14)
    assert canvas.textlength(CLOSING, font=foot_face) <= width, \
        "closing line overflows"
    canvas.text((EDGE, foot_top + 8), CLOSING, font=foot_face,
                fill=INK, anchor="la")
    return page


def main():
    page = render()
    page.save(TARGET, format="PNG", optimize=True)
    size = os.path.getsize(TARGET)
    with open(TARGET, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("wrote %s %dx%d %d bytes" % (TARGET, page.size[0], page.size[1], size))
    print("sha256 " + digest)


if __name__ == "__main__":
    main()
