"""Wearable Mania を組み立てる。

    python scripts/build.py           # public/ を作り直す
    python scripts/build.py --serve   # http://localhost:8792 で確かめる

content/p/*.md(1記事1製品) + config/site.yaml → public/
「日本で使える？」の欄・仕様表・買うボタン・代わり・出典は front matter から作る。
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
CFG = yaml.safe_load((ROOT / "config" / "site.yaml").read_text(encoding="utf-8"))
SITE = CFG["site"]
PARTS = CFG["parts"]
PART = {p["slug"]: p for p in PARTS}
STATUS = CFG["status"]
BASE = SITE["base_url"].rstrip("/")
E = html.escape

JP_ROWS = [("giteki", "技適"), ("buy", "国内で買えるか"), ("app", "アプリ"),
           ("health", "健康の機能"), ("pay", "決済"), ("lang", "言語")]
MARK = {"ok": "○", "q": "△", "ng": "×", "none": "－"}
GITEKI_BADGE = {"ok": ("ok", "技適あり"), "q": ("q", "技適 未確認"), "none": ("none", "技適の対象外")}
STORES = [
    ("rakuten", "楽天で見る", "https://search.rakuten.co.jp/search/mall/{q}/"),
    ("amazon", "Amazon で見る", "https://www.amazon.co.jp/s?k={q}"),
    ("yahoo", "Yahoo!ショッピングで見る", "https://shopping.yahoo.co.jp/search?p={q}"),
]

# 線の絵(部位)。24x24
ICON = {
    "wrist": '<rect x="7" y="6" width="10" height="12" rx="3"/><path d="M9 6V2h6v4M9 18v4h6v-4M12 10v2.5l1.5 1"/>',
    "finger": '<circle cx="12" cy="14" r="6"/><path d="M9.5 6.5 12 3l2.5 3.5"/>',
    "face": '<circle cx="7" cy="13" r="3.5"/><circle cx="17" cy="13" r="3.5"/><path d="M10.5 13h3M3.5 13 2 9M20.5 13 22 9"/>',
    "ear": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Lexend:wght@700&display=swap" rel="stylesheet">')


def fail(msg: str) -> None:
    sys.stderr.reconfigure(encoding="utf-8")
    print(f"NG: {msg}", file=sys.stderr)
    sys.exit(1)


def load_posts() -> list[dict]:
    posts = []
    for f in sorted((ROOT / "content" / "p").glob("*.md")):
        txt = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
        if not m:
            fail(f"{f.name}: front matter がない")
        fm = yaml.safe_load(m.group(1))
        for k in ("title", "slug", "date", "part", "summary", "status", "jp", "sources"):
            if not fm.get(k):
                fail(f"{f.name}: {k} がない")
        if fm["part"] not in PART:
            fail(f"{f.name}: part {fm['part']} は site.yaml に無い")
        if fm["status"] not in STATUS:
            fail(f"{f.name}: status {fm['status']} は site.yaml に無い")
        for k in ("giteki", "buy", "app", "lang"):
            if k not in fm["jp"]:
                fail(f"{f.name}: jp.{k} がない")
        for k, _ in JP_ROWS:
            v = fm["jp"].get(k)
            if v and v.get("mark") not in MARK:
                fail(f"{f.name}: jp.{k}.mark は ok/q/ng/none のどれか")
        if fm["jp"]["giteki"]["mark"] == "ng":
            fail(f"{f.name}: 技適は ng にしない(見つからなければ q)")
        if re.search(r"[!！]", (fm["title"] + m.group(2)).replace("Yahoo!", "")):
            fail(f"{f.name}: 感嘆符を使っている")
        fm["date"] = str(fm["date"])
        fm["modified"] = str(fm.get("modified") or fm["date"])
        fm["body_html"] = markdown.markdown(m.group(2), extensions=["tables"])
        posts.append(fm)
    slugs = [p["slug"] for p in posts]
    if len(slugs) != len(set(slugs)):
        fail("slug が重なっている")
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def store_url(key: str, q: str) -> str:
    tpl = next(t for k, _, t in STORES if k == key)
    url = tpl.format(q=urllib.parse.quote(q))
    aff = (CFG.get("affiliate") or {}).get(key) or ""
    return aff.format(url=urllib.parse.quote(url, safe="")) if aff else url


def has_aff() -> bool:
    return any((CFG.get("affiliate") or {}).values())


def buy_buttons(q: str) -> str:
    rel = ' rel="sponsored noopener"' if has_aff() else ' rel="noopener"'
    return '<div class="buy">' + "".join(
        f'<a href="{E(store_url(k, q))}" target="_blank"{rel} data-store="{k}">{E(label)}</a>' for k, label, _ in STORES
    ) + "</div>"


def badges(p: dict) -> str:
    out = []
    g = p["jp"]["giteki"]["mark"]
    cls, label = GITEKI_BADGE[g]
    out.append(f'<span class="b {cls}">{label}</span>')
    if p["status"] == "japan":
        out.append('<span class="b buy">国内で買える</span>')
    else:
        out.append(f'<span class="b q">{E(STATUS[p["status"]])}</span>')
    return '<div class="badges">' + "".join(out) + "</div>"


def page(title: str, body: str, *, desc: str, path: str, og_image: str = "", jsonld: dict | None = None, og_type="website") -> str:
    url = BASE + path
    full = f"{SITE['title']} | {SITE['title_ja']}" if title == SITE["title"] else f"{title} | {SITE['title']}"
    ga = ""
    if SITE.get("analytics_id"):
        gid = SITE["analytics_id"]
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{gid}');"
              "document.addEventListener('click',e=>{const a=e.target.closest('[data-store]');if(a)gtag('event','buy_click',{store:a.dataset.store,page:location.pathname})});</script>")
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    og = f'<meta property="og:image" content="{E(og_image)}"><meta name="twitter:card" content="summary_large_image">' if og_image else '<meta name="twitter:card" content="summary">'
    year = dt.date.today().year
    years = f"{SITE['copyright_from']}" if year == SITE["copyright_from"] else f"{SITE['copyright_from']}–{year}"
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(full)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{E(url)}">
<meta property="og:title" content="{E(full)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{E(url)}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{E(SITE['title'])}">{og}
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" href="/feed.xml">
{FONTS}<link rel="stylesheet" href="/wear.css">{ga}{ld}</head><body>
{header(path)}
<main class="wrap">{body}</main>
<footer class="site"><div class="wrap">
<p><a href="/about/">このサイトの確かめ方</a><a href="/privacy/">プライバシーと広告</a><a href="https://gadgetterminal.com/">Gadget Terminal</a><a href="https://charge.gadgetterminal.com/">充電沼</a></p>
<p>© {years} {E(SITE['author'])}</p></div></footer>
</body></html>"""


def header(path: str) -> str:
    cur = path.strip("/").split("/")
    on = cur[1] if len(cur) > 1 and cur[0] == "part" else ("" if path == "/" else None)
    nav = f'<a class="{"on" if on == "" else ""}" href="/">ぜんぶ</a>' + "".join(
        f'<a class="{"on" if on == p["slug"] else ""}" href="/part/{p["slug"]}/">{E(p["name"])}' + (f'<small>{E(p["sub"])}</small>' if p["sub"] else "") + "</a>"
        for p in PARTS)
    band = ""
    if path == "/":
        icons = "".join(f'<a href="/part/{k}/"><svg viewBox="0 0 24 24">{v}</svg><b>{E(PART[k]["name"])}</b></a>' for k, v in ICON.items())
        band = (f'<div class="hero-band"><div><span class="hb-k">WEARABLE GADGETS ONLY</span>'
                f'<p class="hb-t">腕・指・顔・耳に<br>つけるガジェットだけ。</p></div><div class="hb-r">{icons}</div></div>')
    # トップだけ、ロゴと「ウェアラブルガジェット専門」を h1 にする(記事ページは記事の題名が h1)
    tag = "h1" if path == "/" else "div"
    return (f'<header class="site"><div class="wrap"><div class="hd"><{tag} class="brand"><a class="logo" href="/">{E(SITE["title"])}</a>'
            f' <span class="logo-ja">{E(SITE["title_ja"])}</span></{tag}><span class="tag">{E(SITE["tagline"])}</span></div>'
            f'{band}<nav class="parts">{nav}</nav></div></header>')


def card(p: dict) -> str:
    img = f'<img src="{E(p["thumbnail"])}" alt="{E(p.get("model") or p["title"])}" loading="lazy" referrerpolicy="no-referrer">' if p.get("thumbnail") else (
        f'<svg class="noimg" viewBox="0 0 24 24">{ICON[p["part"]]}</svg>' if p["part"] in ICON else "")
    return (f'<a class="card" href="/p/{p["slug"]}/"><div class="ph"><span class="part">{E(PART[p["part"]]["name"])}</span>{img}</div>'
            f'<div class="cb"><h3>{E(p["title"])}</h3><p class="d">{p["date"]}</p>{badges(p)}</div></a>')


def grid(posts: list[dict]) -> str:
    if not posts:
        return '<p class="empty">まだ記事がありません。</p>'
    return '<div class="grid">' + "".join(card(p) for p in posts) + "</div>"


def article(p: dict) -> str:
    part = PART[p["part"]]
    hero = ""
    if p.get("thumbnail"):
        hero = (f'<div class="hero"><img src="{E(p["thumbnail"])}" alt="{E(p.get("model") or p["title"])}" referrerpolicy="no-referrer"></div>'
                f'<div class="credit">画像: {E(p.get("thumbnail_credit", ""))}</div>')
    rows = "".join(
        f'<tr><td>{label}</td><td><span class="mk {p["jp"][k]["mark"]}">{MARK[p["jp"][k]["mark"]]}</span>{E(str(p["jp"][k]["text"]))}</td></tr>'
        for k, label in JP_ROWS if p["jp"].get(k))
    verdict = f'<div class="verdict">結論: {E(p["jp"]["verdict"])}</div>' if p["jp"].get("verdict") else ""
    jp = f'<div class="jp"><div class="jp-h">日本で使える？<span>{p["modified"]} 時点</span></div><table>{rows}</table>{verdict}</div>'
    specs = ""
    sp = list(p.get("specs") or [])
    if p.get("price"):
        sp.append(["価格", p["price"]])
    if sp:
        specs = '<h2>仕様</h2><table class="spec">' + "".join(f"<tr><th>{E(str(a))}</th><td>{E(str(b))}</td></tr>" for a, b in sp) + "</table>"
        specs += '<p class="note">メーカー公式と出典の記事にある数字だけを載せています。</p>'
    buy = ""
    if (p.get("stores") or {}).get("query"):
        buy = f'<h2>買えるところ</h2>{buy_buttons(p["stores"]["query"])}'
    alts = ""
    if p.get("alternatives"):
        alts = "<h2>日本で買える代わり</h2>" + "".join(
            f'<div class="alt"><b>{E(a["name"])}</b><p>{E(a.get("why", ""))}</p>' + (buy_buttons(a["query"]) if a.get("query") else "") + "</div>"
            for a in p["alternatives"])
    ad = '<p class="note">このページには広告(紹介リンク)を含みます。</p>' if (buy or alts) and has_aff() else ""
    if buy or alts:
        ad += '<p class="note">価格と在庫は掲載時点のものです。</p>'
    src = '<h2>出典</h2><ul class="src">' + "".join(
        f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["title"])}</a>({E(s.get("publisher", ""))})</li>' for s in p["sources"]) + "</ul>"
    return (f'<article><div class="crumb"><a href="/">ホーム</a> › <a href="/part/{part["slug"]}/">{E(part["name"])}</a></div>'
            f'<h1>{E(p["title"])}</h1><p class="meta">{p["date"]} 公開' + (f'・{p["modified"]} 更新' if p["modified"] != p["date"] else "") +
            f'</p>{hero}{jp}<div class="body">{p["body_html"]}</div>{specs}{buy}{alts}{ad}{src}</article>')


def write(path: str, text: str) -> None:
    f = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


def static_page(name: str, path: str) -> None:
    txt = (ROOT / "content" / "pages" / f"{name}.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    fm, body = yaml.safe_load(m.group(1)), m.group(2)
    ads = ("このサイトの買うボタンの一部は、もしもアフィリエイトを通じた紹介リンクです(楽天市場・Amazon・Yahoo!ショッピング)。リンクから買い物があると、運営者に紹介料が入ります。紹介料の有無で、載せる製品や書き方は変えていません。"
           if has_aff() else "今は広告を載せていません。買うボタンは、ふつうの検索ページへのリンクです。")
    ana = ("Google アナリティクス(GA4)で、ページの閲覧と買うボタンが押された回数を数えています。Cookie を使いますが、個人を特定する情報は集めていません。"
           if SITE.get("analytics_id") else "")
    body = body.replace("{{ads}}", ads).replace("{{analytics}}", ana).replace("{{author}}", SITE["author"]).replace("{{contact}}", SITE["contact_email"])
    write(path, page(fm["title"], f'<div class="page"><h1>{E(fm["title"])}</h1>{markdown.markdown(body, extensions=["tables"])}</div>', desc=fm["summary"], path=path))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true")
    a = ap.parse_args()

    posts = load_posts()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "assets" / "wear.css", OUT / "wear.css")
    shutil.copy(ROOT / "assets" / "favicon.svg", OUT / "favicon.svg")
    (OUT / "CNAME").write_text(urllib.parse.urlparse(BASE).netloc + "\n", encoding="utf-8")

    home = '<h2 class="sec">新着</h2>' + grid(posts)
    write("/", page(SITE["title"], home, desc=SITE["description"], path="/",
                    jsonld={"@context": "https://schema.org", "@type": "WebSite", "name": SITE["title"], "url": BASE + "/"}))
    for pt in PARTS:
        sub = [p for p in posts if p["part"] == pt["slug"]]
        name = pt["name"] + (f"({pt['sub']})" if pt["sub"] else "")
        body = f'<h2 class="sec">{E(name)}につけるガジェット</h2>' + grid(sub)
        write(f"/part/{pt['slug']}/", page(f"{name}のウェアラブル", body, desc=f"{name}につけるウェアラブルガジェットの新製品。技適と日本で使えない機能まで。", path=f"/part/{pt['slug']}/"))
    for p in posts:
        path = f"/p/{p['slug']}/"
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "datePublished": p["date"],
              "dateModified": p["modified"], "author": {"@type": "Organization", "name": SITE["author"]},
              "publisher": {"@type": "Organization", "name": SITE["title"]}, "mainEntityOfPage": BASE + path}
        if p.get("thumbnail"):
            ld["image"] = p["thumbnail"]
        write(path, page(p["title"], article(p), desc=p["summary"], path=path, og_image=p.get("thumbnail", ""), jsonld=ld, og_type="article"))
    static_page("about", "/about/")
    static_page("privacy", "/privacy/")
    write("/404.html", page("ページが見つかりません", '<div class="page"><h1>ページが見つかりません</h1><p><a href="/">トップへ戻る</a></p></div>', desc="", path="/404.html"))

    urls = ["/"] + [f"/part/{pt['slug']}/" for pt in PARTS] + [f"/p/{p['slug']}/" for p in posts] + ["/about/", "/privacy/"]
    mod = {f"/p/{p['slug']}/": p["modified"] for p in posts}
    sm = "".join(f"<url><loc>{BASE}{u}</loc>" + (f"<lastmod>{mod[u]}</lastmod>" if u in mod else "") + "</url>" for u in urls)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    items = "".join(
        f"<item><title>{E(p['title'])}</title><link>{BASE}/p/{p['slug']}/</link><guid>{BASE}/p/{p['slug']}/</guid>"
        f"<pubDate>{dt.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y 06:00:00 +0900')}</pubDate><description>{E(p['summary'])}</description></item>"
        for p in posts[:20])
    write("/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{E(SITE["title"])}</title><link>{BASE}/</link>'
                       f'<description>{E(SITE["description"])}</description><language>ja</language>{items}</channel></rss>')
    n = sum(1 for _ in OUT.rglob("*.html"))
    print(f"OK: 記事 {len(posts)} 本 / ページ {n} 枚 -> public/")

    if a.serve:
        import functools
        import http.server
        h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("http://localhost:8792")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8792), h).serve_forever()


if __name__ == "__main__":
    main()
