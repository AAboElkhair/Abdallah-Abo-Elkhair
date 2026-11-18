#!/usr/bin/env python3
"""Build the articles section: article pages (EN + AR), listing pages, RSS feeds and sitemap entries.

Run from anywhere:   python3 _build/build_articles.py [--root /path/to/repo]

Source files (Markdown with a small header) live in _content/articles/:
    <slug>.md       English version
    <slug>.ar.md    Arabic version (optional)
Header fields:  title, date (YYYY-MM-DD), description, tags (comma separated),
                linkedin (original LinkedIn URL, optional), image (optional), updated (optional)
Legacy LinkedIn-only cards live in _content/legacy-links.json and disappear automatically
when an article lists the same URL in its `linkedin` field.
Folders starting with "_" are not published by GitHub Pages.
"""
import argparse, html, json, re, sys
from datetime import date, datetime
from email.utils import format_datetime
from pathlib import Path
import markdown

SITE = "https://aaboelkhair.github.io/Abdallah-Abo-Elkhair"
PERSON_ID = SITE + "/#person"
MONTHS_EN = ["January","February","March","April","May","June","July","August","September","October","November","December"]
MONTHS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]

L = {
 "en": dict(lang="en", dir="ltr", locale="en_US", name="Abdallah Abo-Elkhair", job="Medical Equipment Planning Engineer",
   home="Home", articles="Articles", min="min read", share="Share", copy="Copy link", copied="Link copied",
   on_linkedin="Originally published on LinkedIn", read_li="Read the original on LinkedIn", read="Read article", read_more="Read article",
   more="More articles", about="About the author", bio="4+ years across 15 healthcare projects in Saudi Arabia, Egypt and Australia, from concept design through IFC, Shop Drawings and As-Built (LOD 500).",
   cta_h="Planning a hospital or clinic?", cta_p="Tell me about the project and I'll reply with how I can help.", cta_b="Work with me",
   list_title="Articles on Medical Equipment Planning | Abdallah Abo-Elkhair", back="All articles", updated="Updated",
   lang_label="عربي", lang_hl="ar", rss="RSS feed", on_li_btn="Read on LinkedIn"),
 "ar": dict(lang="ar", dir="rtl", locale="ar_AR", name="عبدالله أبو الخير", job="مهندس تخطيط معدات طبية",
   home="الرئيسية", articles="المقالات", min="دقيقة قراءة", share="شارك", copy="انسخ الرابط", copied="تم نسخ الرابط",
   on_linkedin="نُشر أصلا على LinkedIn", read_li="اقرأ النسخة الأصلية على LinkedIn", read="اقرأ المقال", read_more="اقرأ المقال",
   more="مقالات أخرى", about="عن الكاتب", bio="أكثر من 4 سنوات عبر 15 مشروع رعاية صحية في السعودية ومصر وأستراليا، من التصميم المفاهيمي حتى IFC وShop Drawings وAs-Built (LOD 500).",
   cta_h="تخطط لمستشفى أو عيادة؟", cta_p="أخبرني عن المشروع وسأرد عليك بكيف أستطيع المساعدة.", cta_b="تعاون معي",
   list_title="مقالات عن تخطيط المعدات الطبية | عبدالله أبو الخير", back="كل المقالات", updated="آخر تحديث",
   lang_label="English", lang_hl="en", rss="خلاصة RSS", on_li_btn="اقرأ على LinkedIn"),
}

def esc(s): return html.escape(s, quote=True)

def fmt_date(d, lg):
    return f"{d.day} {(MONTHS_AR if lg=='ar' else MONTHS_EN)[d.month-1]} {d.year}"

def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    if not m: sys.exit(f"{path}: missing --- header ---")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1); meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    for req in ("title", "date"):
        if not meta.get(req): sys.exit(f"{path}: header needs '{req}'")
    meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d").date()
    if meta.get("updated"): meta["updated"] = datetime.strptime(meta["updated"], "%Y-%m-%d").date()
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    body = m.group(2).strip()
    html_body = markdown.markdown(body, extensions=["extra", "sane_lists"])
    html_body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', html_body)
    html_body = html_body.replace("<img ", '<img loading="lazy" ')
    html_body = html_body.replace("<table>", '<div class="tscroll"><table>').replace("</table>", "</table></div>")
    text = re.sub(r"<[^>]+>", " ", html_body); text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    if not meta.get("description"):
        d = text[:160].rsplit(" ", 1)[0]; meta["description"] = d + ("…" if len(text) > 160 else "")
    words = len(text.split())
    meta["minutes"] = max(1, round(words / (180 if path.name.endswith(".ar.md") else 220)))
    meta["html"], meta["text"] = html_body, text
    return meta

def load_articles(root):
    cdir = root / "_content" / "articles"; items = {}
    for p in sorted(cdir.glob("*.md")):
        if p.name.endswith(".ar.md"): slug, lg = p.name[:-6], "ar"
        else: slug, lg = p.name[:-3], "en"
        items.setdefault(slug, {})[lg] = parse(p)
    return items

class Chunks:
    """Reuse head/header/footer from the existing listing page so every page stays identical."""
    def __init__(self, root, lg):
        sub = "articles/index.html" if lg == "en" else "ar/articles/index.html"
        txt = (root / sub).read_text(encoding="utf-8"); self.txt = txt
        lines = txt.split("\n")
        self.gtag = re.search(r'<meta name="google-site-verification"[^>]*><script async[^>]*></script><script>.*?</script>', lines[1], re.S).group(0)
        self.icons, self.fonts, self.theme = lines[5], lines[6], lines[7]
        self.css = re.search(r'<link rel="stylesheet" href="[^"]*styles\.css[^"]*">', lines[8]).group(0)
        i, j = txt.index("<body>"), txt.index("</header><main>") + len("</header><main>")
        self.header = txt[i:j]
        k = txt.index("</main><footer>"); self.footer = txt[k:]
        self.lg = lg
    def deeper(self, s):
        # one directory deeper than the listing page
        return re.sub(r'(href|src)="((?:\.\./)+)', lambda m: f'{m.group(1)}="../{m.group(2)}', s)

def abs_url(lg, slug=None):
    base = SITE + ("/articles/" if lg == "en" else "/ar/articles/")
    return base + (slug + "/" if slug else "")

def head(ch, lg, title, desc, canon, hreflangs, og_type, image, ld, extra=""):
    T = L[lg]; img = image or SITE + "/images/og-image.jpg"
    alt = "".join(f'<link rel="alternate" hreflang="{h}" href="{u}">' for h, u in hreflangs)
    out = ['<!DOCTYPE html>', f'<html lang="{lg}" dir="{T["dir"]}" data-theme="light"><head><meta charset="utf-8">{ch.gtag}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">']
    out.append(f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canon}">{alt}<meta name="theme-color" content="#0D2237"><meta name="author" content="{esc(T["name"])}">')
    out.append(f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(T["name"])}"><meta property="og:locale" content="{T["locale"]}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(T["name"])}">{extra}')
    out.append(f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{img}">')
    out.append(ch.deeper(ch.icons)); out.append(ch.fonts); out.append(ch.theme)
    feed = abs_url(lg).replace("/articles/", "/feed.xml")
    out.append(f'{ch.deeper(ch.css)}<link rel="alternate" type="application/rss+xml" title="{esc(T["name"])}" href="{feed}"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>')
    return "\n".join(out)

def person_ld(lg):
    return {"@type": "Person", "@id": PERSON_ID, "name": "Abdallah Abo-Elkhair", "jobTitle": "Medical Equipment Planning Engineer",
            "url": SITE + "/", "sameAs": ["https://linkedin.com/in/abo-elkhair"]}

def set_lang_link(header, lg, target_href, hreflang, label):
    return re.sub(r'<a class="lang"[^>]*>.*?</a>', f'<a class="lang" href="{target_href}" hreflang="{hreflang}" lang="{hreflang}">{label}</a>', header, count=1, flags=re.S)

def card(a, lg, slug=None, legacy=None):
    T = L[lg]
    if legacy:
        meta = " · ".join(x for x in [legacy.get("date")] if x)
        return (f'<article class="card"><div>' + (f'<span class="amt">{esc(meta)}</span>' if meta else '') +
                f'<h3>{esc(legacy["title"])}</h3></div><a class="btn dk" href="{esc(legacy["url"])}" target="_blank" rel="noopener" style="margin-top:16px">{T["on_li_btn"]} &rarr;</a></article>')
    d = fmt_date(a["date"], lg)
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in a["tags"][:3])
    return (f'<article class="card"><div><span class="amt">{d} · {a["minutes"]} {T["min"]}</span>'
            f'<h3><a href="{slug}/">{esc(a["title"])}</a></h3><p>{esc(a["description"])}</p></div>'
            f'<div class="amr">{tags}<a class="btn dk" href="{slug}/">{T["read"]} &rarr;</a></div></article>')

def build_listing(root, lg, items, legacy):
    path = root / ("articles/index.html" if lg == "en" else "ar/articles/index.html")
    txt = path.read_text(encoding="utf-8")
    cards = []
    native = sorted(((s, v[lg]) for s, v in items.items() if lg in v), key=lambda x: x[1]["date"], reverse=True)
    covered = {a.get("linkedin", "").rstrip("/") for s, v in items.items() for a in v.values() if a.get("linkedin")}
    for s, a in native: cards.append(card(a, lg, slug=s))
    for l in legacy:
        if l["url"].rstrip("/") not in covered: cards.append(card(None, lg, legacy=l))
    block = '<!--ART-LIST--><div class="grid art" id="artGrid">' + "".join(cards) + '</div><!--/ART-LIST-->'
    if "<!--ART-LIST-->" in txt: txt = re.sub(r"<!--ART-LIST-->.*?<!--/ART-LIST-->", lambda m: block, txt, flags=re.S)
    else: txt = txt.replace('<div class="grid art" id="artList"></div>', block)
    path.write_text(txt, encoding="utf-8")

def build_article(root, lg, slug, a, items, ch):
    T = L[lg]; other = "ar" if lg == "en" else "en"
    canon = abs_url(lg, slug)
    both = other in items[slug]
    hl = [("en", abs_url("en", slug)), ("ar", abs_url("ar", slug)), ("x-default", abs_url("en", slug))] if both else [(lg, canon)]
    lang_href = ("../../ar/articles/" if lg == "en" else "../../../articles/") + (slug + "/" if both else "")
    img = SITE + "/" + a["image"] if a.get("image") else None
    iso = a["date"].isoformat(); mod = (a.get("updated") or a["date"]).isoformat()
    ld = {"@context": "https://schema.org", "@graph": [
        person_ld(lg),
        {"@type": "Article", "headline": a["title"], "description": a["description"], "datePublished": iso, "dateModified": mod,
         "inLanguage": lg, "mainEntityOfPage": canon, "image": img or SITE + "/images/og-image.jpg",
         "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID}, "keywords": ", ".join(a["tags"]) or None},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": T["home"], "item": SITE + ("/" if lg == "en" else "/ar/")},
            {"@type": "ListItem", "position": 2, "name": T["articles"], "item": abs_url(lg)},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": canon}]}]}
    ld["@graph"][1] = {k: v for k, v in ld["@graph"][1].items() if v}
    extra = f'<meta property="article:published_time" content="{iso}"><meta property="article:modified_time" content="{mod}">' + "".join(f'<meta property="article:tag" content="{esc(t)}">' for t in a["tags"])
    page = head(ch, lg, f'{a["title"]} | {T["name"]}', a["description"], canon, hl, "article", img, ld, extra)
    header = set_lang_link(ch.deeper(ch.header), lg, lang_href, T["lang_hl"], T["lang_label"])
    d = fmt_date(a["date"], lg)
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in a["tags"])
    up = f' · {T["updated"]} {fmt_date(a["updated"], lg)}' if a.get("updated") and a["updated"] != a["date"] else ""
    share_url = canon; enc = html.escape(re.sub(r"[^A-Za-z0-9_.~-]", lambda m: "".join(f"%{b:02X}" for b in m.group(0).encode()), share_url))
    wa = "https://api.whatsapp.com/send?text=" + re.sub(r"[^A-Za-z0-9_.~-]", lambda m: "".join(f"%{b:02X}" for b in m.group(0).encode()), a["title"] + " " + share_url)
    li = f"https://www.linkedin.com/sharing/share-offsite/?url={enc}"
    orig = (f'<p class="orig"><a href="{esc(a["linkedin"])}" target="_blank" rel="noopener">{T["read_li"]} &rarr;</a></p>') if a.get("linkedin") else ""
    others = sorted(((s, v[lg]) for s, v in items.items() if lg in v and s != slug), key=lambda x: x[1]["date"], reverse=True)[:2]
    more = ""
    if others:
        more = f'<section class="more"><h2>{T["more"]}</h2><div class="grid art">' + "".join(card(o, lg, slug="../" + s) for s, o in others) + '</div></section>'
    body = f'''
<div class="ph"><div class="wrap"><div class="crumbs"><a href="../../">{T["home"]}</a><span>/</span><a href="../">{T["articles"]}</a></div><h1>{esc(a["title"])}</h1><p class="postmeta">{d} · {a["minutes"]} {T["min"]}{up}</p><div class="tags">{tags}</div></div></div>
<section id="post"><div class="wrap"><article class="post">
<div class="prose">{a["html"]}</div>
{orig}
<div class="share" data-copied="{T["copied"]}"><span>{T["share"]}</span><a class="btn dk" href="{li}" target="_blank" rel="noopener">LinkedIn</a><a class="btn dk" href="{wa}" target="_blank" rel="noopener">WhatsApp</a><button class="btn dk" type="button" data-copy="{canon}">{T["copy"]}</button></div>
<aside class="author"><b>{T["about"]}</b><h3>{esc(T["name"])}</h3><p class="role">{T["job"]}</p><p>{T["bio"]}</p></aside>
</article>{more}
<div class="band"><div><h3>{T["cta_h"]}</h3><p>{T["cta_p"]}</p></div><a class="btn gold" href="../../#contact">{T["cta_b"]} <svg class="ic" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
</div></section>
'''
    foot = ch.deeper(ch.footer)
    foot = foot.replace("</body></html>", COPY_JS + "</body></html>")
    out = root / ("articles" if lg == "en" else "ar/articles") / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page + "\n" + header + body + foot, encoding="utf-8")

COPY_JS = ('<script>document.querySelectorAll("[data-copy]").forEach(function(b){b.addEventListener("click",function(){var u=b.getAttribute("data-copy"),o=b.textContent,m=b.parentNode.getAttribute("data-copied");'
           'function ok(){b.textContent=m;setTimeout(function(){b.textContent=o},1800)}'
           'if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(u).then(ok,function(){})}else{var t=document.createElement("textarea");t.value=u;document.body.appendChild(t);t.select();try{document.execCommand("copy");ok()}catch(e){}t.remove()}})})</script>')

def build_feed(root, lg, items):
    T = L[lg]
    arts = sorted(((s, v[lg]) for s, v in items.items() if lg in v), key=lambda x: x[1]["date"], reverse=True)
    base = abs_url(lg)
    feed_path = root / ("feed.xml" if lg == "en" else "ar/feed.xml")
    rows = []
    for s, a in arts:
        dt = datetime(a["date"].year, a["date"].month, a["date"].day, 9, 0)
        rows.append(f'<item><title>{esc(a["title"])}</title><link>{abs_url(lg, s)}</link><guid isPermaLink="true">{abs_url(lg, s)}</guid>'
                    f'<pubDate>{format_datetime(dt.replace(tzinfo=__import__("datetime").timezone.utc))}</pubDate><description>{esc(a["description"])}</description>'
                    + "".join(f"<category>{esc(t)}</category>" for t in a["tags"]) + f'<content:encoded><![CDATA[{a["html"].replace("]]>", "]]&gt;")}]]></content:encoded></item>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
           f'<title>{esc(T["list_title"].split(" | ")[0])} | {esc(T["name"])}</title><link>{base}</link><description>{esc(T["list_title"])}</description><language>{lg}</language>'
           f'<atom:link href="{SITE}{"/feed.xml" if lg == "en" else "/ar/feed.xml"}" rel="self" type="application/rss+xml"/>' + "".join(rows) + '</channel></rss>\n')
    feed_path.parent.mkdir(parents=True, exist_ok=True); feed_path.write_text(xml, encoding="utf-8")

def update_sitemap(root, items):
    p = root / "sitemap.xml"; txt = p.read_text(encoding="utf-8")
    txt = re.sub(r"<url><loc>[^<]*/articles/[^/<]+/</loc>.*?</url>\n?", "", txt)
    add = ""
    for slug, v in sorted(items.items()):
        for lg, a in v.items():
            add += f'<url><loc>{abs_url(lg, slug)}</loc><lastmod>{(a.get("updated") or a["date"]).isoformat()}</lastmod></url>\n'
    txt = txt.replace("</urlset>", add + "</urlset>")
    p.write_text(txt, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent)); a = ap.parse_args()
    root = Path(a.root); items = load_articles(root)
    lp = root / "_content" / "legacy-links.json"; legacy = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else []
    for lg in ("en", "ar"):
        ch = Chunks(root, lg)
        for slug, v in items.items():
            if lg in v: build_article(root, lg, slug, v[lg], items, ch)
        build_listing(root, lg, items, legacy); build_feed(root, lg, items)
    update_sitemap(root, items)
    print(f"built {sum(len(v) for v in items.values())} article page(s), {len(items)} article(s)")

if __name__ == "__main__": main()
