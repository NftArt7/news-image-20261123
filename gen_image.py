#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page (build time only).

Writes entry.png next to this file. main.py is what the grader runs: it
only copies the finished image, standard library only, no network.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (28, 68, 120)
TEAL = (16, 96, 92)
GREY = (90, 88, 80)
LIGHT = (232, 226, 210)
DARK = (24, 30, 44)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=4):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 17)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 24


def headline(draw, x, y, text, fnt, width, fill=INK, leading=2):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def rule(draw, x, y, w, color=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def panel(draw, x, y, w, h, fill=(255, 255, 255)):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill,
                           outline=(200, 192, 172), width=2)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 148], fill=DARK)
d.text((32, 18), "THE WORLD IN ONE DAY", font=font(SERIF, 58), fill=(247, 243, 232))
d.text((32, 92), "MONDAY  23  NOVEMBER  2026", font=font(SANS_B, 30), fill=(232, 176, 62))
d.text((700, 96), "SIX STORIES  •  ONE DAY", font=font(SANS_B, 19), fill=(200, 205, 215))
rule(d, 0, 148, W, color=RED, width=6)

# ---- lead story: Merkury ----
panel(d, 24, 168, 976, 268)
# drawn scene on the right: night sea, capsizing corvette, explosion, drones
sx, sy, sw, sh = 640, 184, 344, 236
d.rectangle([sx, sy, sx + sw, sy + sh], fill=(18, 38, 66))
for i in range(5):  # stars
    d.ellipse([sx + 20 + i * 62, sy + 14 + (i % 2) * 18, sx + 24 + i * 62, sy + 18 + (i % 2) * 18],
              fill=(220, 225, 240))
# explosion glow, low over the hull
d.ellipse([sx + 130, sy + 78, sx + 250, sy + 168], fill=(255, 140, 40))
d.ellipse([sx + 155, sy + 96, sx + 225, sy + 150], fill=(255, 210, 90))
# ship hull, listing hard to starboard
d.polygon([(sx + 30, sy + 158), (sx + 265, sy + 140), (sx + 290, sy + 158),
           (sx + 110, sy + 184)], fill=(120, 128, 140))
d.polygon([(sx + 150, sy + 140), (sx + 178, sy + 96), (sx + 192, sy + 136)],
          fill=(90, 98, 110))  # mast, tilted
d.rectangle([sx + 198, sy + 116, sx + 206, sy + 138], fill=(90, 98, 110))
# smoke drifting up-left, clear of the blast
for cx, cy, r in [(sx + 268, sy + 42, 20), (sx + 300, sy + 26, 15), (sx + 232, sy + 26, 13)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 72, 80))
# sea waves
for wy in (sy + 185, sy + 205, sy + 222):
    for wx in range(sx + 8, sx + sw - 20, 34):
        d.arc([wx, wy, wx + 30, wy + 16], 180, 360, fill=(120, 170, 210), width=3)
# two sea drones with wakes
for dx in (sx + 40, sx + 270):
    d.rounded_rectangle([dx, sy + 168, dx + 34, sy + 178], radius=4, fill=(230, 230, 230))
    d.line([(dx - 22, sy + 173), (dx, sy + 173)], fill=(200, 210, 225), width=2)
d.text((sx + 10, sy + 8), "BENGHAZI, LIBYA", font=font(SANS_B, 15), fill=(200, 210, 225))

y = 186
y = kicker(d, 48, y, "Libya  •  Ukraine war  —  lead story")
y = headline(d, 48, y + 2, "Ukraine sinks Russian warship off Libya", font(SERIF, 40), 560)
y = para(d, 48, y + 8,
         "President Zelenskyy says seven sea drones sank the corvette Merkury at Benghazi and hit the cargo ship MV Angara. A Ka-27 helicopter was destroyed with the corvette.",
         font(SANS, 21), 560, leading=6)

# ---- row 2: COP31 + NATO ----
panel(d, 24, 436, 480, 210)
y = 452
y = kicker(d, 46, y, "Climate  •  Antalya, Turkey")
y = headline(d, 46, y + 2, "COP31 ends with no deal", font(SERIF, 30), 436)
# small sun-and-globe mark
d.ellipse([46, y + 6, 86, y + 46], fill=(232, 176, 62))
d.ellipse([52, y + 12, 80, y + 40], fill=(240, 200, 90))
para(d, 100, y + 4,
     "The EU rejects the final draft; talks run the longest in COP history, with no agreement on fossil fuels.",
     font(SANS, 19), 382, leading=5)

panel(d, 520, 436, 480, 210)
y = 452
y = kicker(d, 542, y, "Europe  •  NATO", color=BLUE)
y = headline(d, 542, y + 2, "NATO meets over Poland missiles", font(SERIF, 30), 436)
# shield mark
d.polygon([(542, y + 8), (566, y + 2), (590, y + 8), (590, y + 34), (566, y + 52), (542, y + 34)],
          fill=BLUE)
d.text((558, y + 14), "N", font=font(SANS_B, 24), fill=(255, 255, 255))
para(d, 606, y + 4,
     "The North Atlantic Council gathers in Brussels after Russian missiles crossed into Poland on Friday.",
     font(SANS, 19), 372, leading=5)

# ---- row 3: three stories ----
def third(x, kick, color, title, body, mark):
    panel(d, x, 662, 312, 228)
    y = 678
    y = kicker(d, x + 22, y, kick, color=color)
    y = headline(d, x + 22, y + 2, title, font(SERIF, 25), 268)
    mark(x + 22, y + 2)
    para(d, x + 22, y + 52, body, font(SANS, 17), 268, leading=5)


def mark_chart(x, y):
    pts = [(x, y + 34), (x + 22, y + 26), (x + 44, y + 30), (x + 66, y + 12),
           (x + 88, y + 18), (x + 110, y + 2)]
    d.line(pts, fill=RED, width=4)
    d.line([(x, y + 44), (x + 120, y + 44)], fill=GREY, width=2)


def mark_flame(x, y):
    d.polygon([(x + 14, y + 44), (x, y + 20), (x + 10, y + 8), (x + 22, y + 18),
               (x + 30, y), (x + 34, y + 22), (x + 28, y + 44)], fill=(230, 90, 30))


def mark_road(x, y):
    d.polygon([(x, y + 44), (x + 18, y), (x + 34, y), (x + 52, y + 44)], fill=(90, 88, 80))
    for i, yy in enumerate((y + 6, y + 18, y + 30)):
        d.line([(x + 26, yy), (x + 26, yy + 7)], fill=(232, 176, 62), width=3)


third(24, "Markets  •  Asia", RED, "Asian chip stocks slide",
      "Kospi −3.3% after falling over 5% in the day, as AI stocks slide.",
      mark_chart)
third(356, "Indonesia", TEAL, "24 dead in factory fire",
      "A blaze at a candy factory in Banten leaves 24 dead; dozens still missing.",
      mark_flame)
third(688, "Caucasus", BLUE, "Trump Route launches",
      "Pashinyan and Trump announce TRIPP, linking Azerbaijan to Nakhchivan.",
      mark_road)

# ---- ticker ----
d.rectangle([0, 902, W, 962], fill=DARK)
d.text((32, 920), "ALSO ON 23 NOVEMBER:", font=font(SANS_B, 19), fill=(232, 176, 62))
para(d, 300, 922, "Dymer toll rises to 11  •  Iran vows “all tools” against the US blockade",
     font(SANS, 18), 700, fill=(240, 240, 235), leading=0)

# ---- footer ----
d.text((32, 976), "All stories first reported on 23 November 2026.  Sources: Reuters, AP, CNN, Korea JoongAng Daily, RIA Novosti.",
       font=font(SANS, 16), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
