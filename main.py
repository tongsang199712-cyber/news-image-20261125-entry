#!/usr/bin/env python3
"""news-image-20261125: draw one image summing up Wednesday 25 November 2026's
world news and write it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).

Pure Python 3 standard library only: no Pillow, no fonts on disk, no network.
A small 5x7 bitmap font (written out below), a tiny raster canvas, and a
hand-rolled PNG encoder produce the 1024x1024 image deterministically: the
same code writes the same bytes on every run.

Stories, all first reported on 25 November 2026 (or late 24 Nov US time,
reported worldwide on the 25th) from NYT / CNN / Reuters / AP / WHO wires:
  1. CIA and ODNI hit by a cyber breach of their unclassified open-source
     intelligence system; no classified data affected (NYT first, CNN/WSJ).
  2. A Brooklyn jury convicts Huawei on 10 of 12 counts: trade-secret theft,
     bank fraud and sanctions violations over its Iran business; acquitted
     of racketeering; sentencing Sept 2027 (Reuters/CNN).
  3. Zelenskiy confirms Ukraine's drones hit a Russian cargo ship in the
     Gulf of Finland and a warship off Libya; NATO to send early-warning
     jets to Poland (Reuters).
  4. WHO evacuates staff from an Ebola hospital in Ituri, DR Congo, after
     three days sheltering from fighting; 5,775 dead of 11,762 cases (WHO).
  5. A Houthi drone hits Riyadh's tallest tower; 11 wounded, Saudi civil
     defence says (Reuters).
  6. Also today: Trump gives Rudy Giuliani the Medal of Freedom; the Dow
     closes above 50,000; gunmen hold 25 hostages at a Colombia
     supermarket; England beat Australia by 8 wickets to level the T20
     series.
"""
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 230)   # warm newsprint cream
PANEL = (255, 255, 255)
INK = (27, 42, 65)       # deep navy ink
NAVY = (22, 35, 61)
RED = (179, 39, 30)
GOLD = (201, 162, 39)
GOLD_LT = (232, 197, 92)
BLUE = (46, 94, 140)
TEAL = (31, 122, 109)
GREY = (96, 104, 112)
LINE = (214, 208, 194)
STRIP = (233, 229, 218)
GREEN = (46, 125, 50)

# 5x7 bitmap font, all caps. Each glyph is 7 rows of 5 "0"/"1" characters,
# leftmost character is the leftmost pixel.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "01110", "00000", "01110", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
}


class Canvas:
    """A plain RGB pixel buffer with a few filled-shape helpers."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def hline(self, x, y, w, c):
        self.fill_rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.fill_rect(x, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) <= r else 0
            self.fill_rect(cx - dx, yy, 2 * dx + 1, 1, c)

    def ring(self, cx, cy, r, t, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 <= d2 <= r * r:
                    self.set(xx, yy, c)

    def tri(self, x0, y0, x1, y1, x2, y2, c):
        # Filled triangle by scanline interpolation.
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        if ay == cy:
            return
        for y in range(ay, cy + 1):
            if y < by:
                t1 = (y - ay) / (by - ay) if by != ay else 0.0
                xa = ax + (bx - ax) * t1
            else:
                t2 = (y - by) / (cy - by) if cy != by else 0.0
                xa = bx + (cx - bx) * t2
            t3 = (y - ay) / (cy - ay)
            xb = ax + (cx - ax) * t3
            lo, hi = sorted([int(xa), int(xb)])
            self.fill_rect(lo, y, hi - lo + 1, 1, c)


def png_bytes(cv):
    """Encode the canvas as a PNG (filter 0 rows, zlib level 9)."""
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    data = zlib.compress(bytes(raw), 9)

    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload +
                struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", data) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- text

def text_w(s, scale):
    return len(s) * 6 * scale


def draw_text(cv, x, y, s, scale, color):
    """Draw uppercase text; characters outside the font render blank."""
    cx = x
    for ch in s.upper():
        rows = FONT.get(ch)
        if rows:
            for r, row in enumerate(rows):
                for col, bit in enumerate(row):
                    if bit == "1":
                        cv.fill_rect(cx + col * scale, y + r * scale,
                                     scale, scale, color)
        cx += 6 * scale
    return cx


def draw_text_c(cv, cx, y, s, scale, color):
    draw_text(cv, cx - text_w(s, scale) // 2, y, s, scale, color)


def wrap(s, scale, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(cv, x, y, s, scale, color, max_w, lh):
    for ln in wrap(s, scale, max_w):
        draw_text(cv, x, y, ln, scale, color)
        y += lh
    return y


# ---------------------------------------------------------------- icons
# Each icon is drawn in a small box (x, y, w, h) with simple flat shapes.

def icon_laptop(cv, x, y, w, h):
    # Laptop with a warning triangle: the breached spy-agency system.
    cv.fill_rect(x + 18, y + 22, w - 36, h - 62, NAVY)
    cv.fill_rect(x + 26, y + 30, w - 52, h - 78, (176, 216, 230))
    cv.fill_rect(x + 8, y + h - 34, w - 16, 10, INK)
    cv.fill_rect(x + w // 2 - 14, y + h - 24, 28, 5, GREY)
    cx, cy = x + w // 2, y + h // 2 - 8
    cv.tri(cx, cy - 34, cx - 32, cy + 22, cx + 32, cy + 22, GOLD)
    cv.tri(cx, cy - 26, cx - 25, cy + 17, cx + 25, cy + 17, INK)
    cv.fill_rect(cx - 3, cy - 14, 6, 18, GOLD_LT)
    cv.fill_rect(cx - 3, cy + 8, 6, 6, GOLD_LT)


def icon_chip(cv, x, y, w, h):
    # Microchip: the Huawei trial. All pins stay inside the icon box
    # (x..x+w) so they never touch the story text beside it.
    cv.fill_rect(x + 34, y + 34, w - 68, h - 68, INK)
    cv.fill_rect(x + 48, y + 48, w - 96, h - 96, BLUE)
    cv.fill_rect(x + 62, y + 62, w - 124, h - 124, GOLD_LT)
    for i in range(3):
        px = x + 40 + i * 28
        cv.fill_rect(px, y + 14, 8, 20, INK)
        cv.fill_rect(px, y + h - 34, 8, 20, INK)
        py = y + 40 + i * 28
        cv.fill_rect(x + 14, py, 20, 8, INK)
        cv.fill_rect(x + w - 34, py, 20, 8, INK)


def icon_ship(cv, x, y, w, h):
    # Cargo ship on waves with a small jet above: the Gulf of Finland /
    # Libya strikes and NATO's response.
    cv.fill_rect(x + 38, y + 30, 6, 62, INK)
    cv.tri(x + 44, y + 30, x + 44, y + 44, x + 64, y + 37, RED)
    cv.fill_rect(x + 28, y + 72, 24, 20, RED)
    cv.fill_rect(x + 56, y + 72, 24, 20, GOLD_LT)
    cv.fill_rect(x + 14, y + 92, w - 28, 24, NAVY)
    cv.tri(x + w - 14, y + 92, x + w - 14, y + 116, x + w - 38, y + 116,
           NAVY)
    cv.fill_rect(x + 22, y + 100, w - 44, 6, GOLD_LT)
    for i in range(3):
        cv.fill_rect(x + 14 + i * 38, y + 128, 28, 5, BLUE)
    cv.fill_rect(x + w - 42, y + 20, 24, 6, GREY)
    cv.tri(x + w - 18, y + 20, x + w - 18, y + 26, x + w - 10, y + 23,
           GREY)


def icon_cross(cv, x, y, w, h):
    # Medical cross in a ring: the Ebola evacuation in Congo.
    cx, cy = x + w // 2, y + h // 2
    cv.ring(cx, cy, 62, 6, TEAL)
    cv.fill_rect(cx - 14, cy - 42, 28, 84, RED)
    cv.fill_rect(cx - 42, cy - 14, 84, 28, RED)


def icon_tower(cv, x, y, w, h):
    # A tall tower with a drone above it: the Riyadh strike.
    cv.fill_rect(x + w // 2 - 22, y + 34, 44, h - 64, NAVY)
    cv.tri(x + w // 2 - 22, y + 34, x + w // 2 + 22, y + 34,
           x + w // 2, y + 12, NAVY)
    for i in range(4):
        cv.fill_rect(x + w // 2 - 14, y + 48 + i * 22, 28, 10, GOLD_LT)
    cv.fill_rect(x + w // 2 - 34, y + h - 30, 68, 8, INK)
    dx, dy = x + w - 34, y + 22
    cv.fill_rect(dx - 3, dy - 3, 7, 7, RED)
    cv.fill_rect(dx - 16, dy - 12, 12, 4, INK)
    cv.fill_rect(dx + 4, dy - 12, 12, 4, INK)
    cv.fill_rect(dx - 16, dy + 8, 12, 4, INK)
    cv.fill_rect(dx + 4, dy + 8, 12, 4, INK)


# ---------------------------------------------------------------- layout

def story_panel(cv, x, y, w, h, tag, color, headline, body, icon):
    cv.fill_rect(x, y, w, h, PANEL)
    cv.fill_rect(x, y, w, 4, color)
    cv.fill_rect(x, y, 4, h, color)
    cv.fill_rect(x, y, w, 34, color)
    draw_text(cv, x + 14, y + 8, tag, 2, (255, 255, 255))
    icon(cv, x + 8, y + 42, 118, h - 52)
    tx = x + 134
    tw = w - 148
    hy = y + 48
    for ln in wrap(headline, 3, tw):
        draw_text(cv, tx, hy, ln, 3, INK)
        hy += 26
    para(cv, tx, hy + 6, body, 2, (52, 60, 70), tw, 18)


def strip_item(cv, x, y, w, tag, color, text):
    cv.fill_rect(x, y, 10, 10, color)
    draw_text(cv, x + 18, y - 3, tag, 2, color)
    para(cv, x, y + 20, text, 2, INK, w, 18)


def main():
    cv = Canvas(W, H, PAPER)
    cv.fill_rect(0, 0, W, 6, NAVY)
    cv.fill_rect(0, H - 6, W, 6, NAVY)
    cv.fill_rect(0, 0, 6, H, NAVY)
    cv.fill_rect(W - 6, 0, 6, H, NAVY)

    # Masthead.
    cv.fill_rect(6, 6, W - 12, 112, NAVY)
    draw_text_c(cv, W // 2, 24, "THE WORLD IN ONE DAY", 5, (255, 255, 255))
    cv.fill_rect(212, 70, W - 424, 3, GOLD)
    draw_text_c(cv, W // 2, 82, "WEDNESDAY 25 NOVEMBER 2026", 3, GOLD_LT)

    # Lead story: the CIA / ODNI breach.
    lx, ly, lw, lh = 14, 126, W - 28, 262
    cv.fill_rect(lx, ly, lw, lh, PANEL)
    cv.fill_rect(lx, ly, 8, lh, RED)
    cv.fill_rect(lx, ly, lw, 4, RED)
    icon_laptop(cv, lx + 14, ly + 40, 210, 200)
    tx = lx + 244
    draw_text(cv, tx, ly + 18, "WASHINGTON - CYBER ATTACK", 2, RED)
    draw_text(cv, tx, ly + 50, "US SPY AGENCIES HACKED", 5, INK)
    para(cv, tx, ly + 122,
         "CIA AND ODNI BREACH HITS OPEN-SOURCE INTEL SYSTEM; "
         "NO CLASSIFIED DATA AFFECTED, US OFFICIALS SAY. "
         "EARLY SIGNS POINT TO CHINA, SOURCES SAY.",
         3, (52, 60, 70), lw - 258, 27)

    # Four stories in a 2x2 grid.
    gy, gh = 396, 200
    gw = (W - 28 - 12) // 2
    story_panel(cv, 14, gy, gw, gh, "CHINA - US COURT", RED,
                "HUAWEI GUILTY OF TRADE-SECRET THEFT",
                "US JURY CONVICTS THE CHINESE GIANT ON 10 OF 12 "
                "COUNTS; CLEARED OF RACKETEERING. SENTENCE DUE "
                "SEPT 2027.", icon_chip)
    story_panel(cv, 14 + gw + 12, gy, gw, gh, "UKRAINE - WAR AT SEA", NAVY,
                "KYIV CONFIRMS IT HIT RUSSIAN SHIPS",
                "DRONES STRUCK A CARGO SHIP IN THE GULF OF "
                "FINLAND AND A WARSHIP OFF LIBYA. NATO TO SEND "
                "EARLY-WARNING JETS TO POLAND.", icon_ship)
    story_panel(cv, 14, gy + gh + 12, gw, gh, "CONGO - EBOLA", TEAL,
                "WHO FLEES EBOLA HOSPITAL IN CONGO",
                "STAFF LEAVE AFTER 3 DAYS SHELTERING FROM "
                "FIGHTING IN ITURI. 5,775 DEAD OF 11,762 CASES "
                "SO FAR.", icon_cross)
    story_panel(cv, 14 + gw + 12, gy + gh + 12, gw, gh,
                "MIDDLE EAST - RIYADH", GOLD,
                "HOUTHI DRONE HITS RIYADH TOWER",
                "11 WOUNDED IN A STRIKE ON THE CAPITAL'S "
                "TALLEST TOWER, SAUDI CIVIL DEFENCE SAYS.",
                icon_tower)

    # Also today.
    sy = 820
    cv.fill_rect(14, sy, W - 28, 128, STRIP)
    cv.fill_rect(14, sy, W - 28, 4, INK)
    draw_text(cv, 28, sy + 14, "ALSO TODAY", 2, INK)
    cv.hline(150, sy + 22, W - 178, LINE)
    col_w = (W - 28 - 3 * 24 - 28) // 4
    items = [
        ("MEDAL", RED, "TRUMP AWARDS RUDY GIULIANI THE MEDAL OF FREEDOM."),
        ("MARKETS", GREEN, "DOW CLOSES ABOVE 50,000 FOR THE FIRST TIME."),
        ("COLOMBIA", BLUE, "GUNMEN HOLD 25 HOSTAGES AT A SUPERMARKET."),
        ("SPORT", TEAL, "ENGLAND BEAT AUSTRALIA BY 8 WICKETS TO LEVEL THE T20 SERIES."),
    ]
    for i, (tag, color, text) in enumerate(items):
        strip_item(cv, 28 + i * (col_w + 24), sy + 44, col_w, tag, color, text)

    # Footer.
    draw_text_c(cv, W // 2, 968, "SOURCES: NYT, CNN, REUTERS, AP, WHO - 25 NOV 2026",
                2, GREY)
    draw_text_c(cv, W // 2, 990, "DRAWN IN CODE - NO PHOTOGRAPHS", 2, GREY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(png_bytes(cv))


if __name__ == "__main__":
    main()
