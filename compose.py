#!/usr/bin/env python3
"""Compose the front page for news-image-20261120.

Draws one 1024x1024 newspaper front page summing up the world news of
Friday 20 November 2026. Every word on the page is rendered here by Pillow,
so the finished image carries no garbled AI text. The four editorial
illustrations in assets/ contain no text of their own.

Deterministic: no network, no clock, no randomness. Running this script
twice produces the same entry.png byte for byte (PNG encoder settings
are fixed below).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 22, 22)
RED = (178, 34, 34)
NAVY = (31, 58, 95)
GREY = (90, 86, 78)
RULE = (180, 172, 158)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_crop(img, tw, th):
    """Centre-crop an image to the target aspect ratio, then resize."""
    iw, ih = img.size
    target = tw / th
    current = iw / ih
    if current > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target)
        y0 = (ih - nh) // 2
        img = img.crop((0, y0, iw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=6):
    """Draw wrapped paragraph text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def headline(draw, x, y, text, fnt, width, fill=INK, leading=2):
    return para(draw, x, y, text, fnt, width, fill=fill, leading=leading)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    d.text((32, 18), "THE WORLD IN ONE DAY", font=font(SERIF, 56), fill=INK)
    d.text((32, 84), "A front page of Friday's world news",
           font=font(SERIF_REG, 20), fill=GREY)

    # ---- Date strip -----------------------------------------------------
    d.rectangle([0, 122, W, 158], fill=RED)
    d.text((32, 129), "FRIDAY  20  NOVEMBER  2026",
           font=font(SANS_BOLD, 24), fill=(255, 255, 255))
    d.text((700, 133), "WORLD  •  JUSTICE  •  MARKETS",
           font=font(SANS_BOLD, 15), fill=(255, 235, 220))

    # ---- Lead story: The Hague ------------------------------------------
    icj = fit_crop(Image.open(os.path.join(
        ASSETS, "media-generation-icj-courtroom-0-872217ba-1b2a-4cf1-8c2c-29c35e5d3877.webp"
    )).convert("RGB"), 596, 218)
    page.paste(icj, (32, 176))
    d.text((32, 402), "THE HAGUE", font=font(SANS_BOLD, 15), fill=RED)
    y = headline(d, 32, 422,
                 "Court rules Myanmar committed genocide against the Rohingya",
                 font(SERIF, 30), 596)
    y = para(d, 32, y + 4,
             "The International Court of Justice ruled 9\u20136 that Myanmar "
             "committed genocide in its 2017 campaign in Rakhine \u2014 the "
             "court's first such finding against a state. Refugees in "
             "Bangladesh cheered the verdict.",
             font(SANS, 17), 596, leading=4)

    # ---- Second story: Shenzhen -----------------------------------------
    summit = fit_crop(Image.open(os.path.join(
        ASSETS, "media-generation-shenzhen-summit-0-c49738fd-06a8-4365-afee-6e99953e84e8.webp"
    )).convert("RGB"), 336, 218)
    page.paste(summit, (656, 176))
    d.text((656, 402), "SHENZHEN", font=font(SANS_BOLD, 15), fill=RED)
    y2 = headline(d, 656, 422,
                  "Trump, Xi and Putin meet in a first three-way summit",
                  font(SERIF, 24), 336)
    y2 = para(d, 656, y2 + 4,
              "The three presidents issued a four-point peace declaration, "
              "discussing nuclear arms control, Iran and the war in Ukraine.",
              font(SANS, 16), 336, leading=4)

    d.line([32, 596, 992, 596], fill=RULE, width=2)

    # ---- Third story: the record IPO -------------------------------------
    ipo = fit_crop(Image.open(os.path.join(
        ASSETS, "media-generation-ipo-market-0-9dcfac99-5386-49a5-89d9-5201c43fff2e.webp"
    )).convert("RGB"), 468, 168)
    page.paste(ipo, (32, 610))
    d.text((32, 786), "NEW YORK", font=font(SANS_BOLD, 15), fill=RED)
    y3 = headline(d, 32, 806,
                  "Anthropic's record IPO: $83 a share, up 17% on debut",
                  font(SERIF, 24), 468)
    y3 = para(d, 32, y3 + 4,
              "The biggest listing on record, worth about $1.5 trillion. "
              "The S&P 500 fell 2% for a fifth straight loss.",
              font(SANS, 16), 468, leading=4)

    # ---- Fourth story: Riyadh -------------------------------------------
    riyadh = fit_crop(Image.open(os.path.join(
        ASSETS, "media-generation-riyadh-tower-0-d92bed86-e80e-495c-8127-bce97262dbd3.webp"
    )).convert("RGB"), 468, 168)
    page.paste(riyadh, (524, 610))
    d.text((524, 786), "RIYADH", font=font(SANS_BOLD, 15), fill=RED)
    y4 = headline(d, 524, 806,
                  "Houthi missile hits Riyadh's tallest tower",
                  font(SERIF, 24), 468)
    y4 = para(d, 524, y4 + 4,
              "Saudi authorities confirmed damage to a landmark building "
              "in the capital after the strike.",
              font(SANS, 16), 468, leading=4)

    d.line([32, 912, 992, 912], fill=RULE, width=2)

    # ---- Also today: briefs ----------------------------------------------
    d.text((32, 924), "ALSO TODAY", font=font(SANS_BOLD, 15), fill=RED)
    briefs = [
        "HORMUZ \u2014 Iran escalates tanker attacks in the Strait of Hormuz.",
        "GAZA \u2014 Four nations urge Israel to let aid into flood-hit Gaza.",
        "INDIA \u2014 Cyclone Akvan nears Odisha; schools closed.",
        "TAIWAN \u2014 Stocks fall 5,248 points over three trading days.",
        "WASHINGTON \u2014 Trump back from China; press conference today.",
    ]
    by = 958
    # Three briefs in the left column, two in the right. Each brief is
    # wrapped to its column width (measured: all five fit on one line at
    # 13px in a 468px column) so columns can never collide.
    brief_font = font(SANS, 13)
    left = briefs[:3]
    right = briefs[3:]
    yy = 948
    for b in left:
        lines = wrap(d, "\u2022  " + b, brief_font, 460)
        for line in lines:
            d.text((32, yy), line, font=brief_font, fill=INK)
            yy += 18
    yy = 948
    for b in right:
        lines = wrap(d, "\u2022  " + b, brief_font, 460)
        for line in lines:
            d.text((524, yy), line, font=brief_font, fill=INK)
            yy += 18

    # ---- Footer: date + sources, reinforcing which day this sums up -----
    d.text((32, 1006),
           "All stories reported on Friday 20 November 2026  \u2014  ICJ, Reuters, AP",
           font=font(SANS, 11), fill=GREY)

    page.save(os.path.join(HERE, "entry.png"), "PNG",
              optimize=True, compress_level=9)
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
