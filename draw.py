#!/usr/bin/env python3
"""Draw the news-image-01 entry image (1024x1024 PNG) with PIL.

A one-page editorial front page: six flat pictogram panels, each with a
short factual label, summing up the world's news of Friday 13 November
2026. Every story was first reported on 13 November 2026 (BBC / Al
Jazeera and other wire reporting, checked 14 November 2026 WIB):

  1. Ukraine peace talks - Zelensky meets US envoys Witkoff and Kushner;
     Europe promised a seat at the next round.
  2. Drone hits Russian warship - Ukrainian drone strike on the corvette
     Naro-Fominsk in the Gulf of Finland, detected by Finland.
  3. Nvidia CEO resigns - Jensen Huang resigns; CFO Colette Kress named
     interim CEO. (Share moves that day were volatile; no % is claimed.)
  4. Microsoft 365 outage - mail and Teams down worldwide.
  5. Tanker hit by mine - LNG tanker reported struck by a naval mine in
     the Strait of Hormuz; Iran says it struck a US radar site in Bahrain.
  6. Kane breaks England record - England beat Croatia to reach the
     Nations League quarter-finals; Harry Kane's 126th cap, a record.

Deterministic: fixed geometry, fixed fonts, no randomness, no time,
no network. Run:  python3 draw.py   (writes entry.png next to itself)
"""

import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"

BG = (244, 239, 230)
NAVY = (22, 40, 63)
GOLD = (232, 185, 59)
RED = (192, 57, 43)
INK = (28, 39, 51)
GREY = (90, 100, 112)
PANEL = (255, 255, 255)
BORDER = (216, 210, 196)


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def panel_base(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=PANEL,
                           outline=BORDER, width=2)
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 12], fill=accent)


def panel_text(draw, x, y, w, h, kicker, accent, headline, sub, pic_cy):
    f_kick = font(BOLD, 21)
    f_head = font(BOLD, 33)
    f_sub = font(REG, 19)
    draw.text((x + w / 2, y + 34), kicker, font=f_kick, fill=accent,
              anchor="ma")
    lines = wrap(draw, headline, f_head, w - 36)
    ly = y + 232
    for ln in lines:
        draw.text((x + w / 2, ly), ln, font=f_head, fill=INK, anchor="ma")
        ly += 40
    draw.text((x + w / 2, y + h - 40), sub, font=f_sub, fill=GREY,
              anchor="ma")
    return pic_cy


# --- pictograms (drawn in a zone centred at (cx, cy)) ---------------------

def pic_talks(draw, cx, cy):
    # two overlapping speech bubbles
    draw.rounded_rectangle([cx - 78, cy - 58, cx + 2, cy + 8], radius=16,
                           fill=(47, 127, 193))
    draw.polygon([(cx - 66, cy + 8), (cx - 46, cy + 8), (cx - 70, cy + 30)],
                 fill=(47, 127, 193))
    draw.rounded_rectangle([cx - 2, cy - 28, cx + 78, cy + 38], radius=16,
                           fill=(245, 197, 24))
    draw.polygon([(cx + 52, cy + 38), (cx + 32, cy + 38), (cx + 60, cy + 60)],
                 fill=(245, 197, 24))
    for dx in (-52, -28, -4):
        draw.ellipse([cx + dx - 6, cy - 36, cx + dx + 6, cy - 24],
                     fill=(255, 255, 255))
    for dx in (22, 38, 54):
        draw.ellipse([cx + dx - 4, cy + 2, cx + dx + 4, cy + 10],
                     fill=(90, 70, 10))


def pic_warship(draw, cx, cy):
    # hull
    draw.polygon([(cx - 95, cy + 8), (cx + 95, cy + 8), (cx + 72, cy + 48),
                  (cx - 72, cy + 48)], fill=(74, 90, 106))
    draw.rectangle([cx - 48, cy - 28, cx + 18, cy + 8], fill=(74, 90, 106))
    draw.rectangle([cx - 30, cy - 46, cx - 2, cy - 28], fill=(74, 90, 106))
    draw.line([cx - 16, cy - 78, cx - 16, cy - 46], fill=(74, 90, 106),
              width=5)
    draw.polygon([(cx - 16, cy - 78), (cx + 8, cy - 70), (cx - 16, cy - 62)],
                 fill=RED)
    for wx in (-38, -14, 6):
        draw.rectangle([cx + wx, cy - 18, cx + wx + 12, cy - 6],
                       fill=(255, 255, 255))
    # waves
    for wy, ww in ((cy + 58, 190), (cy + 70, 160)):
        draw.arc([cx - ww // 2, wy, cx + ww // 2, wy + 22], 0, 180,
                 fill=(47, 127, 193), width=4)
    # drone
    dx, dy = cx + 62, cy - 62
    draw.ellipse([dx - 22, dy - 6, dx + 22, dy + 6], fill=(40, 44, 52))
    draw.ellipse([dx - 34, dy - 10, dx - 18, dy - 2], fill=(120, 128, 136))
    draw.ellipse([dx + 18, dy - 10, dx + 34, dy - 2], fill=(120, 128, 136))
    draw.line([dx, dy + 6, dx, dy + 16], fill=(40, 44, 52), width=3)
    starburst(draw, cx + 34, cy - 6, 26, 12, 8, (245, 130, 32))
    starburst(draw, cx + 34, cy - 6, 12, 6, 8, (255, 220, 60))


def pic_chip(draw, cx, cy):
    # pins
    for i in range(4):
        px = cx - 66 + i * 30
        draw.rectangle([px, cy - 62, px + 12, cy - 34], fill=(120, 128, 136))
        draw.rectangle([px, cy + 34, px + 12, cy + 62], fill=(120, 128, 136))
    for i in range(3):
        py = cy - 44 + i * 34
        draw.rectangle([cx - 92, py, cx - 64, py + 12], fill=(120, 128, 136))
        draw.rectangle([cx + 64, py, cx + 92, py + 12], fill=(120, 128, 136))
    draw.rounded_rectangle([cx - 64, cy - 34, cx + 64, cy + 34], radius=10,
                           fill=(106, 168, 79))
    draw.text((cx, cy), "NVDA", font=font(BOLD, 30), fill=(255, 255, 255),
              anchor="mm")
    # red down arrow
    ax = cx + 96
    draw.polygon([(ax - 14, cy - 52), (ax + 14, cy - 52), (ax + 14, cy + 8),
                  (ax + 30, cy + 8), (ax, cy + 48), (ax - 30, cy + 8),
                  (ax - 14, cy + 8)], fill=(192, 57, 43))


def pic_cloud(draw, cx, cy):
    draw.ellipse([cx - 78, cy - 22, cx - 8, cy + 48], fill=(31, 122, 194))
    draw.ellipse([cx - 34, cy - 52, cx + 44, cy + 48], fill=(31, 122, 194))
    draw.ellipse([cx + 8, cy - 22, cx + 78, cy + 48], fill=(31, 122, 194))
    draw.rectangle([cx - 78, cy + 4, cx + 78, cy + 48], fill=(31, 122, 194))
    draw.text((cx - 4, cy + 6), "365", font=font(BOLD, 34),
              fill=(255, 255, 255), anchor="mm")
    # red X badge
    bx, by = cx + 78, cy - 48
    draw.ellipse([bx - 24, by - 24, bx + 24, by + 24], fill=(192, 57, 43))
    draw.line([bx - 11, by - 11, bx + 11, by + 11], fill=(255, 255, 255),
              width=6)
    draw.line([bx + 11, by - 11, bx - 11, by + 11], fill=(255, 255, 255),
              width=6)


def pic_tanker(draw, cx, cy):
    # naval mine
    mx, my = cx - 82, cy - 6
    draw.ellipse([mx - 20, my - 20, mx + 20, my + 20], fill=(40, 44, 52))
    for k in range(8):
        a = math.pi * k / 4
        draw.line([mx + 18 * math.cos(a), my + 18 * math.sin(a),
                   mx + 30 * math.cos(a), my + 30 * math.sin(a)],
                  fill=(40, 44, 52), width=5)
    starburst(draw, mx + 26, my - 16, 24, 11, 8, (245, 130, 32))
    starburst(draw, mx + 26, my - 16, 11, 5, 8, (255, 220, 60))
    # hull + containers
    draw.polygon([(cx - 62, cy + 2), (cx + 98, cy + 2), (cx + 74, cy + 46),
                  (cx - 62, cy + 46)], fill=(38, 56, 76))
    draw.rectangle([cx - 40, cy - 26, cx + 6, cy + 2], fill=(74, 90, 106))
    draw.rectangle([cx + 10, cy - 26, cx + 30, cy + 2], fill=(192, 57, 43))
    draw.rectangle([cx + 34, cy - 40, cx + 78, cy + 2], fill=(38, 56, 76))
    for wy in (cy - 26, cy - 14):
        draw.rectangle([cx + 42, wy, cx + 70, wy + 5], fill=(255, 255, 255))
    for wy, ww in ((cy + 56, 190), (cy + 68, 160)):
        draw.arc([cx - ww // 2, wy, cx + ww // 2, wy + 22], 0, 180,
                 fill=(47, 127, 193), width=4)


def pic_ball(draw, cx, cy):
    draw.ellipse([cx - 56, cy - 56, cx + 56, cy + 56], outline=INK, width=5)
    pts = []
    for i in range(5):
        a = -math.pi / 2 + 2 * math.pi * i / 5
        pts.append((cx + 22 * math.cos(a), cy + 22 * math.sin(a)))
    draw.polygon(pts, fill=INK)
    for k in range(5):
        a = -math.pi / 2 + 2 * math.pi * k / 5 + math.pi / 5
        sx, sy = cx + 43 * math.cos(a), cy + 43 * math.sin(a)
        draw.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=INK)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.text((W / 2, 44), "FRIDAY 13 NOVEMBER 2026", font=font(BOLD, 60),
           fill=(255, 255, 255), anchor="ma")
    tracked(d, W / 2, 112, "THE WORLD IN ONE DAY", font(BOLD, 27), GOLD, 8)
    d.rectangle([0, 150, W, 156], fill=RED)

    # grid: 3 x 2 panels
    margin, gap = 24, 12
    pw = (W - 2 * margin - 2 * gap) // 3
    ph = (1000 - 168 - gap) // 2
    panels = [
        # (col, row, accent, kicker, headline, sub, pictogram)
        (0, 0, (47, 127, 193), "DIPLOMACY", "UKRAINE PEACE TALKS",
         "Europe joins the next round", pic_talks),
        (1, 0, (74, 90, 106), "WAR AT SEA", "DRONE HITS RUSSIAN WARSHIP",
         "Gulf of Finland", pic_warship),
        (2, 0, (106, 168, 79), "TECH", "NVIDIA CEO RESIGNS",
         "Kress named interim CEO", pic_chip),
        (0, 1, (31, 122, 194), "TECH", "MICROSOFT 365 OUTAGE",
         "Mail & Teams down worldwide", pic_cloud),
        (1, 1, (20, 88, 107), "GULF", "TANKER HIT BY MINE",
         "Iran hits US radar in Bahrain", pic_tanker),
        (2, 1, (30, 125, 70), "SPORT", "KANE BREAKS ENGLAND RECORD",
         "126 caps \u00b7 beat Croatia", pic_ball),
    ]
    for col, row, accent, kicker, headline, sub, pic in panels:
        x = margin + col * (pw + gap)
        y = 168 + row * (ph + gap)
        panel_base(d, x, y, pw, ph, accent)
        pic(d, x + pw / 2, y + 128 if pic is pic_ball else y + 138)
        if pic is pic_ball:
            # big cap number between the ball and the headline
            d.text((x + pw / 2, y + 34), kicker, font=font(BOLD, 21),
                   fill=accent, anchor="ma")
            d.text((x + pw / 2, y + 192), "126", font=font(BOLD, 40),
                   fill=INK, anchor="ma")
            lines = wrap(d, headline, font(BOLD, 33), pw - 36)
            ly = y + 240
            for ln in lines:
                d.text((x + pw / 2, ly), ln, font=font(BOLD, 33), fill=INK,
                       anchor="ma")
                ly += 38
            d.text((x + pw / 2, y + ph - 40), sub, font=font(REG, 19),
                   fill=GREY, anchor="ma")
        else:
            panel_text(d, x, y, pw, ph, kicker, accent, headline, sub,
                       y + 138)

    d.text((W / 2, 1004),
           "Sources: BBC & Al Jazeera  \u00b7  All events reported 13 November 2026",
           font=font(REG, 16), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
