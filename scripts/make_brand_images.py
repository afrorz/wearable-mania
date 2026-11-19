"""Gemini で作った W・M のマーク(assets/brand/wm-mark-gemini.jpg)から、サイトで使う画像を作る。

    python scripts/make_brand_images.py

作る物(assets/ の中):
- logo-mark.png        ヘッダーのマーク(背景は透明)
- favicon-32/48/192.png, favicon.ico, apple-touch-icon.png
- ogp-1200x630.png     SNS で共有したときの画像(Chrome で HTML を撮る。名前の文字は Lexend)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "assets"
SRC = A / "brand" / "wm-mark-gemini.jpg"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def transparent_mark() -> Image.Image:
    """白地を透明にする。インクの濃さ(白からの離れ具合)を不透明度にし、色は白を抜いて戻す。"""
    im = SRC.convert("RGB") if False else Image.open(SRC).convert("RGB")
    w, h = im.size
    src = im.load()
    out = Image.new("RGBA", (w, h))
    px = out.load()
    FULL = 228  # これ以上白から離れていれば不透明(文字の黒も緑も min が 20 前後)
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            d = 255 - min(r, g, b)
            if d < 10:
                px[x, y] = (0, 0, 0, 0)
                continue
            a = min(1.0, d / FULL)
            px[x, y] = tuple(max(0, min(255, round(255 - (255 - c) / a))) for c in (r, g, b)) + (round(a * 255),)
    box = out.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    return out.crop(box)


def on_square(mark: Image.Image, size: int, pad: float, bg=(255, 255, 255, 255)) -> Image.Image:
    sq = Image.new("RGBA", (size, size), bg)
    inner = round(size * (1 - 2 * pad))
    m = mark.copy()
    m.thumbnail((inner, inner), Image.LANCZOS)
    sq.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return sq


def main() -> None:
    mark = transparent_mark()
    print("mark", mark.size)
    m = mark.copy()
    m.thumbnail((10_000, 160), Image.LANCZOS)  # 高さ160px(画面では32〜40px で出す)
    m.save(A / "logo-mark.png", optimize=True)
    mark.save(A / "brand" / "wm-mark.png", optimize=True)  # 原寸の透明版(ほかで使う用)

    for s in (32, 48, 192):
        on_square(mark, s, 0.06 if s < 100 else 0.12).save(A / f"favicon-{s}.png", optimize=True)
    on_square(mark, 180, 0.14).convert("RGB").save(A / "apple-touch-icon.png", optimize=True)
    on_square(mark, 256, 0.06).save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    html = A / "brand" / "_ogp.html"
    html.write_text(f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@700&family=Noto+Sans+JP:wght@700&display=swap" rel="stylesheet">
<style>html,body{{margin:0;width:1200px;height:630px;background:#fff;overflow:hidden}}
.c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px}}
img{{width:430px}}.t{{font:700 76px Lexend;letter-spacing:-.02em;color:#16181d}}
.s{{font:700 30px "Noto Sans JP";color:#0f7d70;letter-spacing:.08em;margin-top:-18px}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:22px;background:#16181d}}</style></head>
<body><div class="c"><img src="../brand/wm-mark.png"><div class="t">Wearable Mania</div><div class="s">ウェアラブルガジェット専門</div></div><div class="bar"></div></body></html>""",
                    encoding="utf-8")
    if not CHROME.exists():
        sys.exit("Chrome が見つからないので OGP は作れない")
    subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                    "--virtual-time-budget=8000", f"--screenshot={A / 'ogp-1200x630.png'}", html.as_uri()],
                   check=True, capture_output=True)
    html.unlink()
    print("OK")


if __name__ == "__main__":
    main()
