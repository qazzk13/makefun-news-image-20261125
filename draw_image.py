"""Draw the 25 November 2026 world-news image (1024x1024 JPEG).

Layout: a masthead naming the day, four illustrated panels for the
day's four biggest stories, and a footer strip with four more items.
All drawing is done with Pillow primitives and DejaVu fonts, so the
output is fully deterministic: the same script run twice writes the
same bytes (fixed JPEG quality, no timestamps, no randomness).

Stories (all first reported on Wednesday 25 November 2026):
- China investigates Politburo member and Shanghai party chief
  Chen Jining (AP; Japan Times calls it the biggest shakeup in
  decades).
- China's Shenzhou-24 space flight launches with the first Pakistani
  national on board (Japan Times; Arab News).
- A US jury convicts China's Huawei of conspiracy to steal trade
  secrets and bank fraud (AP).
- Gunmen take 25 hostages at a supermarket in Cartagena, Colombia,
  after a failed armoured-car raid (AP; Manila Times; SCMP).
Footer: Trump awards Giuliani the Medal of Freedom; Trump pardons
the Thanksgiving turkeys Freedom and Feathers; Shein to pay $100M to
settle FTC allegations; a Russian strike kills two in Ukraine's
Odesa region.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.jpg"
JPEG_QUALITY = 90

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (13, 27, 62)
WHITE = (255, 255, 255)
INK = (18, 22, 32)
GOLD = (212, 160, 23)
RED = (178, 34, 34)
BLUE = (24, 90, 160)
TEAL = (0, 120, 120)
ORANGE = (214, 110, 0)
PURPLE = (96, 52, 148)
PANEL_BG = (245, 246, 248)
FOOTER_BG = (232, 234, 238)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width, returning a list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_skyline(d, x0, y0, x1, y1):
    """Shanghai skyline with the Pearl Tower and a magnifier."""
    d.rectangle([x0, y0, x1, y1], fill=(24, 34, 64))
    for sx, sy in [(x0 + 36, y0 + 26), (x0 + 150, y0 + 52), (x1 - 70, y0 + 30),
                   (x0 + 84, y1 - 120), (x1 - 150, y0 + 70)]:
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=WHITE)
    base = y1 - 8
    # Skyscrapers.
    for bx, bw, bh in [(x0 + 26, 62, 96), (x0 + 102, 52, 128),
                       (x1 - 150, 58, 110), (x1 - 78, 50, 82)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(52, 68, 104))
        for wy in range(base - bh + 12, base - 14, 22):
            for wx in range(bx + 10, bx + bw - 12, 18):
                d.rectangle([wx, wy, wx + 8, wy + 10], fill=(255, 214, 90))
    # Oriental Pearl Tower: mast, two spheres, base.
    cx = (x0 + x1) // 2
    d.line([cx, y0 + 16, cx, base], fill=(230, 120, 160), width=6)
    d.ellipse([cx - 30, y0 + 74, cx + 30, y0 + 134], fill=(214, 74, 130),
              outline=WHITE, width=2)
    d.ellipse([cx - 20, base - 74, cx + 20, base - 34], fill=(214, 74, 130),
              outline=WHITE, width=2)
    d.polygon([(cx - 44, base), (cx + 44, base), (cx + 18, base - 36),
               (cx - 18, base - 36)], fill=(120, 130, 150))
    # Magnifier over the tower: an investigation.
    mx, my, mr = x1 - 118, y0 + 66, 44
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=GOLD, width=7)
    d.line([mx + 30, my + 30, mx + 62, my + 62], fill=GOLD, width=10)


def draw_rocket(d, x0, y0, x1, y1):
    """A Shenzhou rocket lifting off under a starry sky."""
    d.rectangle([x0, y0, x1, y1], fill=(8, 14, 40))
    for sx, sy in [(x0 + 44, y0 + 30), (x0 + 170, y0 + 60), (x1 - 56, y0 + 44),
                   (x0 + 90, y0 + 110), (x1 - 130, y0 + 96), (x0 + 250, y0 + 24)]:
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=WHITE)
    cx = (x0 + x1) // 2
    top, bot = y0 + 14, y1 - 52
    # Body and nose cone.
    d.rectangle([cx - 30, top + 34, cx + 30, bot], fill=(238, 238, 240))
    d.polygon([(cx - 30, top + 34), (cx + 30, top + 34), (cx, top)],
              fill=RED)
    d.rectangle([cx - 30, top + 72, cx + 30, top + 92], fill=RED)
    d.text((cx, top + 52), "SZ-24", font=font(FONT_BOLD, 20),
           fill=(30, 30, 40), anchor="mm")
    # Side boosters.
    for sgn in (-1, 1):
        bx = cx + sgn * 46
        d.rectangle([bx - 13, top + 78, bx + 13, bot], fill=(210, 214, 220))
        d.polygon([(bx - 13, top + 78), (bx + 13, top + 78), (bx, top + 56)],
                  fill=RED)
    # Flame and smoke.
    d.polygon([(cx - 26, bot), (cx + 26, bot), (cx, bot + 36)], fill=ORANGE)
    d.polygon([(cx - 13, bot), (cx + 13, bot), (cx, bot + 24)],
              fill=(255, 214, 90))
    for ex, ey, er in [(cx - 92, bot + 20, 30), (cx + 92, bot + 20, 30),
                       (cx - 140, bot + 30, 22), (cx + 140, bot + 30, 22)]:
        d.ellipse([ex - er, ey - er // 2, ex + er, ey + er // 2],
                  fill=(200, 206, 216))


def draw_court_phone(d, x0, y0, x1, y1):
    """Scales of justice over a smartphone, for the Huawei verdict."""
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 218))
    cx = (x0 + x1) // 2
    # Smartphone body at the base.
    d.rounded_rectangle([cx - 58, y1 - 108, cx + 58, y1 - 10], radius=12,
                        fill=(30, 34, 44), outline=(90, 84, 76), width=3)
    d.rectangle([cx - 46, y1 - 94, cx + 46, y1 - 30], fill=(70, 120, 180))
    d.ellipse([cx - 6, y1 - 26, cx + 6, y1 - 14], fill=(200, 200, 210))
    # Scales: post, beam and two pans.
    post_top = y0 + 34
    d.rectangle([cx - 5, post_top, cx + 5, y1 - 104], fill=(120, 96, 30))
    d.rectangle([cx - 150, post_top - 6, cx + 150, post_top + 6],
                fill=(120, 96, 30))
    d.ellipse([cx - 14, post_top - 26, cx + 14, post_top + 2],
              fill=GOLD, outline=(120, 96, 30), width=2)
    for sgn in (-1, 1):
        px = cx + sgn * 138
        d.line([px, post_top + 6, px - 34, y0 + 96], fill=(120, 96, 30),
               width=3)
        d.line([px, post_top + 6, px + 34, y0 + 96], fill=(120, 96, 30),
               width=3)
        d.pieslice([px - 52, y0 + 84, px + 52, y0 + 128], 0, 180,
                   fill=GOLD, outline=(120, 96, 30), width=2)
    # A red verdict stamp in the top-left corner, clear of the phone.
    d.rounded_rectangle([x0 + 14, y0 + 12, x0 + 148, y0 + 52], radius=6,
                        outline=RED, width=3)
    d.text((x0 + 81, y0 + 32), "GUILTY", font=font(FONT_BOLD, 25),
           fill=RED, anchor="mm")


def draw_storefront(d, x0, y0, x1, y1):
    """A supermarket front sealed with police tape, in Cartagena."""
    d.rectangle([x0, y0, x1, y1], fill=(250, 226, 170))
    d.rectangle([x0, y0, x1, y0 + 64], fill=(36, 110, 76))
    cx = (x0 + x1) // 2
    d.text((cx, y0 + 32), "SUPERMERCADO", font=font(FONT_BOLD, 30),
           fill=WHITE, anchor="mm")
    # Shop windows and door.
    for wx in (x0 + 36, x1 - 136):
        d.rectangle([wx, y0 + 84, wx + 100, y1 - 44], fill=(170, 205, 225),
                    outline=(90, 84, 76), width=3)
        d.line([wx, y0 + 128, wx + 100, y0 + 128], fill=(90, 84, 76),
               width=3)
    d.rectangle([cx - 34, y0 + 84, cx + 34, y1 - 10], fill=(120, 90, 60),
                outline=(90, 84, 76), width=3)
    d.ellipse([cx + 14, (y0 + y1) // 2 + 16, cx + 24, (y0 + y1) // 2 + 26],
              fill=GOLD)
    # Police tape across the front, two crossing bands; the word
    # follows each band's slope so it sits inside the yellow.
    for yy, flip in ((y1 - 92, 1), (y1 - 52, -1)):
        d.polygon([(x0, yy), (x1, yy + 26 * flip), (x1, yy + 26 * flip + 24),
                   (x0, yy + 24)], fill=(255, 205, 0))
        for tx in range(x0 + 30, x1 - 90, 118):
            ty = yy + 12 + flip * 26 * (tx - x0) // (x1 - x0)
            d.text((tx, ty), "POLICIA", font=font(FONT_BOLD, 17),
                   fill=(30, 30, 30), anchor="lm")


PANELS = [
    {
        "tag": "CHINA  ·  POLITICS",
        "color": RED,
        "title": "SHANGHAI CHIEF PROBED",
        "body": ("China investigates Shanghai party chief "
                 "Chen Jining, a Politburo member, in the biggest "
                 "party shakeup in decades."),
        "scene": draw_skyline,
    },
    {
        "tag": "SPACE  ·  CHINA",
        "color": BLUE,
        "title": "SHENZHOU-24 LIFTS OFF",
        "body": ("China's Shenzhou-24 space flight launches with "
                 "the first Pakistani national on board."),
        "scene": draw_rocket,
    },
    {
        "tag": "TECH  ·  US COURTS",
        "color": PURPLE,
        "title": "HUAWEI CONVICTED",
        "body": ("A US jury convicts China's Huawei of conspiracy "
                 "to steal trade secrets and bank fraud."),
        "scene": draw_court_phone,
    },
    {
        "tag": "COLOMBIA  ·  CARTAGENA",
        "color": TEAL,
        "title": "HOSTAGES IN A STORE",
        "body": ("Gunmen take 25 hostages at a Cartagena "
                 "supermarket after a failed armoured-car raid."),
        "scene": draw_storefront,
    },
]

FOOTER_ITEMS = [
    "Trump gives Giuliani the Medal of Freedom",
    "Trump pardons turkeys Freedom & Feathers",
    "Shein to pay $100M to settle FTC case",
    "Russian strike kills 2 in Odesa region",
]


def draw_panel(d, box, panel):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=14, fill=PANEL_BG,
                        outline=(200, 205, 212), width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 46], radius=14,
                        fill=panel["color"])
    d.rectangle([x0, y0 + 32, x1, y0 + 46], fill=panel["color"])
    d.text((x0 + 18, y0 + 23), panel["tag"], font=font(FONT_BOLD, 21),
           fill=WHITE, anchor="lm")
    scene_box = (x0 + 12, y0 + 58, x1 - 12, y0 + 238)
    panel["scene"](d, *scene_box)
    d.text((x0 + 18, y0 + 256), panel["title"],
           font=font(FONT_BOLD, 29), fill=INK)
    lines = wrap(d, panel["body"], font(FONT_REG, 21), x1 - x0 - 36)
    y = y0 + 292
    for line in lines:
        d.text((x0 + 18, y), line, font=font(FONT_REG, 21), fill=(48, 52, 64))
        y += 27


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    # Masthead.
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 134], fill=GOLD)
    d.text((24, 38), "WEDNESDAY 25 NOVEMBER 2026",
           font=font(FONT_BOLD, 38), fill=WHITE)
    d.text((24, 92), "WORLD NEWS IN ONE IMAGE",
           font=font(FONT_BOLD, 26), fill=(255, 214, 90))
    d.text((W - 24, 34), "make.fun", font=font(FONT_BOLD, 30),
           fill=(150, 170, 210), anchor="ra")
    d.text((W - 24, 92), "DAILY NEWS IMAGE", font=font(FONT_BOLD, 20),
           fill=(150, 170, 210), anchor="ra")
    # Four panels, 2 x 2.
    gx, gy, gap = 16, 150, 12
    pw = (W - 2 * gx - gap) // 2
    ph = 368
    for i, panel in enumerate(PANELS):
        col, row = i % 2, i // 2
        box = (gx + col * (pw + gap), gy + row * (ph + gap),
               gx + col * (pw + gap) + pw, gy + row * (ph + gap) + ph)
        draw_panel(d, box, panel)
    # Footer strip.
    fy0 = gy + 2 * ph + gap + 12
    d.rectangle([0, fy0, W, H], fill=FOOTER_BG)
    d.text((24, fy0 + 12), "ALSO TODAY",
           font=font(FONT_BOLD, 22), fill=NAVY)
    lines = ["•  " + item for item in FOOTER_ITEMS]
    y = fy0 + 44
    for i in range(0, 4, 2):
        d.text((24, y), lines[i], font=font(FONT_REG, 21), fill=INK)
        d.text((W // 2 + 8, y), lines[i + 1], font=font(FONT_REG, 21),
               fill=INK)
        y += 30
    img.save(OUT, "JPEG", quality=JPEG_QUALITY, optimize=True)
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
