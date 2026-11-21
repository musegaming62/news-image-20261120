#!/usr/bin/env python3
"""Draw the news-image-20261120 front page: a dense newspaper poster.

Reads the story list from STORIES-20NOV.md (same directory) and draws
entry.png (1024x1024): a navy masthead naming Friday 20 November 2026,
three hero cards for the day's biggest stories, and a numbered grid of
the remaining 33 stories, plus a date-check footer. Run with:

    python3 build_poster.py

Requires Pillow and the DejaVu fonts (system packages).
"""

import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
STORIES_FILE = os.path.join(HERE, "STORIES-20NOV.md")
OUTPUT_FILE = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 24

NAVY = (15, 42, 74)
NAVY_DARK = (10, 31, 56)
GOLD = (201, 162, 39)
GOLD_DARK = (176, 141, 28)
PAPER = (247, 243, 232)
CARD = (255, 255, 255)
CARD_TINT = (245, 239, 224)
INK = (17, 17, 17)
MUTED = (92, 92, 92)
LINE = (216, 210, 192)
HERO1_TEXT = (247, 243, 232)
HERO1_DECK = (214, 222, 235)
HERO1_TAG = (226, 188, 74)

FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def parse_stories(path):
    """Parse STORIES-20NOV.md into {number: dict} entries."""
    stories = {}
    current = None
    with open(path, "r", encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    for line in lines:
        match = re.match(r"^###\s+(\d+)\.\s+(.*)$", line)
        if match:
            number = int(match.group(1))
            current = {
                "number": number,
                "headline": match.group(2).strip(),
                "summary": "",
                "region": "",
                "topic": "",
                "source": "",
            }
            stories[number] = current
            continue
        if current is None:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- Region:"):
            rest = stripped[len("- Region:"):].strip()
            parts = [p.strip() for p in rest.split("|")]
            # The first part is the region value (the "Region:" label
            # was stripped above); the rest carry their own labels.
            if parts:
                current["region"] = parts[0]
            for part in parts[1:]:
                if part.startswith("Topic:"):
                    current["topic"] = part[len("Topic:"):].strip()
                elif part.startswith("Source:"):
                    current["source"] = part[len("Source:"):].strip()
            continue
        if not current["summary"]:
            current["summary"] = stripped
    return stories


def wrap_text(draw, text, font_obj, max_width, max_lines=None):
    """Wrap text to max_width; returns a list of lines (truncated if needed)."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font_obj) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
            if max_lines is not None and len(lines) >= max_lines:
                break
    if current and (max_lines is None or len(lines) < max_lines):
        lines.append(current)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
    # Ellipsis if the last line still overflows (very long single word).
    if lines and draw.textlength(lines[-1], font=font_obj) > max_width:
        line = lines[-1]
        while line and draw.textlength(line + "...", font=font_obj) > max_width:
            line = line[:-1]
        lines[-1] = line + "..."
    return lines


def fit_one_line(draw, text, font_obj, max_width):
    """Shorten text with an ellipsis so it fits on one line."""
    if draw.textlength(text, font=font_obj) <= max_width:
        return text
    while text and draw.textlength(text + "...", font=font_obj) > max_width:
        text = text[:-1]
    return text + "..."


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 108], fill=NAVY)
    draw.rectangle([0, 108, W, 112], fill=GOLD)
    draw.rectangle([0, 112, W, 113], fill=NAVY_DARK)
    title_font = font(FONT_SERIF_BOLD, 56)
    date_font = font(FONT_SANS_BOLD, 23)
    draw.text((W // 2, 44), "THE WORLD TODAY", font=title_font,
              fill=PAPER, anchor="mm")
    draw.text((W // 2, 90), "FRIDAY  20  NOVEMBER  2026", font=date_font,
              fill=GOLD, anchor="mm")


def draw_hero1(draw, story):
    x0, y0, x1, y1 = MARGIN, 122, W - MARGIN, 288
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    draw.rectangle([x0, y0, x1, y0 + 4], fill=GOLD)
    tag_font = font(FONT_SANS_BOLD, 13)
    head_font = font(FONT_SERIF_BOLD, 31)
    deck_font = font(FONT_SANS, 15)
    src_font = font(FONT_SANS, 11)
    tag = "No. 1  —  {}  •  {}".format(story["region"].upper(),
                                       story["topic"].upper())
    draw.text((x0 + 18, y0 + 22), tag, font=tag_font, fill=HERO1_TAG)
    src = "Source: " + story["source"]
    draw.text((x1 - 18, y0 + 22), src, font=src_font, fill=HERO1_TAG,
              anchor="ra")
    head_lines = wrap_text(draw, story["headline"], head_font, x1 - x0 - 36,
                           max_lines=2)
    y = y0 + 46
    for line in head_lines:
        draw.text((x0 + 18, y), line, font=head_font, fill=HERO1_TEXT)
        y += 36
    deck_lines = wrap_text(draw, story["summary"], deck_font, x1 - x0 - 36,
                           max_lines=2)
    for line in deck_lines:
        draw.text((x0 + 18, y + 2), line, font=deck_font, fill=HERO1_DECK)
        y += 19


def draw_hero_card(draw, story, x0, y0, x1, y1, tinted):
    bg = CARD_TINT if tinted else CARD
    draw.rectangle([x0, y0, x1, y1], fill=bg)
    draw.rectangle([x0, y0, x1, y0 + 4], fill=GOLD)
    draw.rectangle([x0, y0, x0 + 1, y1], fill=LINE)
    draw.rectangle([x1 - 1, y0, x1, y1], fill=LINE)
    draw.rectangle([x0, y1 - 1, x1, y1], fill=LINE)
    tag_font = font(FONT_SANS_BOLD, 12)
    head_font = font(FONT_SERIF_BOLD, 24)
    deck_font = font(FONT_SANS, 12)
    src_font = font(FONT_SANS, 10)
    tag = "No. {}  —  {}  •  {}".format(story["number"],
                                        story["region"].upper(),
                                        story["topic"].upper())
    draw.text((x0 + 14, y0 + 16), tag, font=tag_font, fill=NAVY)
    src = "Source: " + story["source"]
    draw.text((x1 - 14, y0 + 16), src, font=src_font, fill=MUTED,
              anchor="ra")
    head_lines = wrap_text(draw, story["headline"], head_font, x1 - x0 - 28,
                           max_lines=2)
    y = y0 + 40
    for line in head_lines:
        draw.text((x0 + 14, y), line, font=head_font, fill=NAVY)
        y += 28
    deck_lines = wrap_text(draw, story["summary"], deck_font, x1 - x0 - 28,
                           max_lines=3)
    for line in deck_lines:
        draw.text((x0 + 14, y + 2), line, font=deck_font, fill=INK)
        y += 15


def draw_section_header(draw, y, text):
    hdr_font = font(FONT_SANS_BOLD, 15)
    tw = draw.textlength(text, font=hdr_font)
    cx = W // 2
    left_end = cx - tw / 2 - 14
    right_start = cx + tw / 2 + 14
    draw.rectangle([MARGIN, y + 9, left_end, y + 11], fill=GOLD)
    draw.rectangle([right_start, y + 9, W - MARGIN, y + 11], fill=GOLD)
    draw.text((cx, y + 10), text, font=hdr_font, fill=NAVY, anchor="mm")


def draw_grid(draw, stories):
    cols = 3
    rows = 11
    gap = 12
    col_w = (W - 2 * MARGIN - (cols - 1) * gap) // cols
    top = 492
    row_h = 44
    num_font = font(FONT_SANS_BOLD, 13)
    head_font = font(FONT_SANS_BOLD, 12)
    tag_font = font(FONT_SANS, 9)
    for idx in range(rows * cols):
        number = 4 + idx
        story = stories[number]
        col = idx % cols
        row = idx // cols
        x0 = MARGIN + col * (col_w + gap)
        y0 = top + row * row_h
        # Vertical dividers between columns.
        if col > 0:
            draw.line([x0 - gap // 2, top, x0 - gap // 2,
                       top + rows * row_h], fill=LINE, width=1)
        # Number badge.
        num_text = "{:02d}".format(number)
        draw.text((x0, y0 + 5), num_text, font=num_font, fill=GOLD_DARK)
        num_w = draw.textlength(num_text, font=num_font)
        text_x = x0 + num_w + 6
        text_w = x0 + col_w - text_x
        head_lines = wrap_text(draw, story["headline"], head_font, text_w,
                               max_lines=2)
        y = y0 + 4
        for line in head_lines:
            draw.text((text_x, y), line, font=head_font, fill=INK)
            y += 15
        tag = "{}  •  {}  —  {}".format(story["region"].upper(),
                                        story["topic"].upper(),
                                        story["source"])
        tag = fit_one_line(draw, tag, tag_font, text_w)
        draw.text((text_x, y + 1), tag, font=tag_font, fill=MUTED)
        # Horizontal rule under the row (not after the last row).
        if row < rows - 1:
            draw.line([MARGIN, y0 + row_h - 6, W - MARGIN, y0 + row_h - 6],
                      fill=LINE, width=1)


def draw_footer(draw):
    y = 984
    draw.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=GOLD)
    check_font = font(FONT_SANS_BOLD, 12)
    sub_font = font(FONT_SANS, 10)
    check = ("DATE CHECK — Every event on this page happened, or was first "
             "reported, on Friday 20 November 2026.")
    draw.text((W // 2, y + 14), check, font=check_font, fill=NAVY,
              anchor="mm")
    draw.text((W // 2, y + 30), "36 stories  •  Sources on file  •  THE WORLD TODAY",
              font=sub_font, fill=MUTED, anchor="mm")


def main():
    stories = parse_stories(STORIES_FILE)
    missing = [n for n in range(1, 37) if n not in stories]
    if missing:
        print("error: missing stories: {}".format(missing), file=sys.stderr)
        return 1
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero1(draw, stories[1])
    mid = (W - MARGIN) // 2
    draw_hero_card(draw, stories[2], MARGIN, 298, mid - 6, 448, tinted=False)
    draw_hero_card(draw, stories[3], mid + 6, 298, W - MARGIN, 448,
                   tinted=True)
    draw_section_header(draw, 458, "THE DAY IN 33 MORE STORIES")
    draw_grid(draw, stories)
    draw_footer(draw)
    img.save(OUTPUT_FILE, format="PNG", optimize=True)
    size = os.path.getsize(OUTPUT_FILE)
    print("wrote {} ({}x{}, {} bytes)".format(OUTPUT_FILE, W, H, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
