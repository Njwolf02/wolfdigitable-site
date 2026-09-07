#!/usr/bin/env python3
"""Generate the favicon set and the Open Graph share image for wolfdigitable.com.

WHY: the site had NO favicon (both /favicon.ico and /favicon.svg returned 404) and NO og:image,
so it showed a generic globe in browser tabs and search results, and rendered as a bare URL when
shared on LinkedIn — which is the main channel a consultancy actually gets seen through.

Drawn with PIL rather than rasterised from SVG: no rasteriser is installed, and the mark is simple
geometry. Rendered at 8x and downsampled with LANCZOS so the 16px favicon stays clean.

Run: python3 make-assets.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
INK, ACCENT, PAPER = "#0f172a", "#d97706", "#ffffff"
SS = 8


def _font(size, bold=True):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mark(px):
    """Rounded ink square with an orange 'W' — the brand's own two colours, nothing invented."""
    s = px * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=INK)
    f = _font(int(s * 0.62))
    t = "W"
    box = d.textbbox((0, 0), t, font=f)
    d.text(((s - (box[2] - box[0])) / 2 - box[0], (s - (box[3] - box[1])) / 2 - box[1]),
           t, font=f, fill=ACCENT)
    return img.resize((px, px), Image.LANCZOS)


def og():
    """1200x630 share card. Text only — a real screenshot would date instantly."""
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 12, W, H], fill=ACCENT)          # accent rule
    d.text((80, 96), "WOLF", font=_font(56), fill="#ffffff")
    d.text((80 + d.textlength("WOLF ", font=_font(56)), 96), "DIGITABLE", font=_font(56), fill=ACCENT)
    line_f = _font(46)
    for i, line in enumerate(["Senior software engineering,", "on contract."]):
        d.text((80, 220 + i * 66), line, font=line_f, fill="#ffffff")
    small = _font(26, bold=False)
    d.text((80, 396), "Platform architecture · Database reliability · Data & analytics", font=small, fill="#cbd5e1")
    d.text((80, 440), "10+ years healthcare & regulated SaaS · Louisville, KY · Remote-friendly", font=small, fill="#94a3b8")
    return img


def main():
    (HERE / "assets").mkdir(exist_ok=True)
    for name, px in [("favicon-48.png", 48), ("favicon-96.png", 96),
                     ("favicon-192.png", 192), ("apple-touch-icon.png", 180)]:
        mark(px).save(HERE / name, "PNG", optimize=True)
        print(f"  {name} ({px}x{px})")
    mark(48).save(HERE / "favicon.ico", "ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  favicon.ico (16/32/48)")
    og().save(HERE / "assets" / "og-image.png", "PNG", optimize=True)
    print("  assets/og-image.png (1200x630)")


if __name__ == "__main__":
    main()
