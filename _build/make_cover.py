#!/usr/bin/env python3
"""Make a 1200x630 article cover in the site's navy and gold style.

python3 _build/make_cover.py --out images/cover-my-article.webp --title "Article title" --kicker "Healthcare BIM" [--lang ar] [--motif plan|cube|chart|cross|grid]
Use --lang ar for the Arabic cover (Arabic title, right-to-left).
"""
import argparse, html, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import html_to_webp

MOTIFS = {
 "plan": '<svg viewBox="0 0 400 300" fill="none" stroke="#D8B56B" stroke-width="2.2"><rect x="30" y="30" width="340" height="240" opacity=".5"/><path d="M30 130h150M180 30v240M180 190h190M290 30v160" opacity=".7"/><circle cx="105" cy="80" r="26" opacity=".9"/><rect x="215" y="60" width="50" height="34" opacity=".9"/><path d="M60 210h90M60 230h60" opacity=".6"/></svg>',
 "cube": '<svg viewBox="0 0 400 300" fill="none" stroke="#D8B56B" stroke-width="2.2"><path d="M200 40l130 75v130L200 290 70 245V115z" opacity=".8"/><path d="M200 165l130-50M200 165v125M200 165L70 115" opacity=".8"/><path d="M135 78l130 75M265 78L135 153" opacity=".35"/></svg>',
 "chart": '<svg viewBox="0 0 400 300" fill="none" stroke="#D8B56B" stroke-width="2.2"><path d="M40 260V40M40 260h320" opacity=".6"/><rect x="80" y="170" width="44" height="90" opacity=".8"/><rect x="150" y="120" width="44" height="140" opacity=".8"/><rect x="220" y="150" width="44" height="110" opacity=".8"/><rect x="290" y="70" width="44" height="190" opacity=".9"/><path d="M70 150l70-45 70 25 90-85" opacity=".9"/></svg>',
 "cross": '<svg viewBox="0 0 400 300" fill="none" stroke="#D8B56B" stroke-width="2.2"><circle cx="200" cy="150" r="115" opacity=".5"/><circle cx="200" cy="150" r="78" opacity=".35"/><path d="M200 95v110M145 150h110" stroke-width="5" opacity=".95"/></svg>',
 "grid": '<svg viewBox="0 0 400 300" fill="none" stroke="#D8B56B" stroke-width="2"><path d="M40 60h320M40 120h320M40 180h320M40 240h320M80 30v250M160 30v250M240 30v250M320 30v250" opacity=".35"/><rect x="160" y="120" width="80" height="60" opacity=".95" stroke-width="3"/><circle cx="320" cy="60" r="8" fill="#D8B56B"/><circle cx="80" cy="240" r="8" fill="#D8B56B"/></svg>',
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True); ap.add_argument("--title", required=True); ap.add_argument("--kicker", default="")
    ap.add_argument("--lang", default="en"); ap.add_argument("--motif", default="plan"); a = ap.parse_args()
    ar = a.lang == "ar"; t = html.escape(a.title); k = html.escape(a.kicker)
    size = 64 if len(a.title) < 60 else 54 if len(a.title) < 85 else 46
    css = f"""
body{{width:1200px;height:630px;background:radial-gradient(900px 520px at {'15%' if ar else '88%'} 12%,#d8b56b26,transparent 60%),linear-gradient(135deg,#0B1626,#13243B);color:#EEEADF;position:relative;overflow:hidden;direction:{'rtl' if ar else 'ltr'}}}
.frame{{position:absolute;inset:26px;border:1px solid #d8b56b55;border-radius:6px}}
.motif{{position:absolute;{'left' if ar else 'right'}:60px;bottom:70px;width:400px;opacity:.95}}
.k{{position:absolute;top:70px;{'right' if ar else 'left'}:80px;font:600 18px {'CairoAr' if ar else 'Manrope'};letter-spacing:{'0' if ar else '.22em'};text-transform:uppercase;color:#D8B56B}}
.k:after{{content:"";display:inline-block;width:56px;height:1px;background:#D8B56B;vertical-align:middle;margin-{'right' if ar else 'left'}:16px}}
h1{{position:absolute;top:150px;{'right' if ar else 'left'}:80px;width:{650 if True else 900}px;font:{'700' if ar else '600'} {size + (0 if not ar else -4)}px/1.14 {'AmiriAr' if ar else 'Cormorant'},Georgia,serif;letter-spacing:-.01em;color:#fff}}
.by{{position:absolute;bottom:62px;{'right' if ar else 'left'}:80px;font:600 20px {'CairoAr' if ar else 'Manrope'};color:#99A8BA;letter-spacing:{'0' if ar else '.04em'}}}.by b{{color:#D8B56B;font-weight:600}}
"""
    by = "عبدالله أبو الخير" if ar else "Abdallah Abo-Elkhair"
    body = f'<div class="frame"></div><div class="k">{k}</div><h1>{t}</h1><div class="motif">{MOTIFS.get(a.motif, MOTIFS["plan"])}</div><div class="by"><b>{by}</b> &nbsp;·&nbsp; {"مهندس تخطيط معدات طبية" if ar else "Medical Equipment Planning"}</div>'
    html_to_webp(body, a.out, width=1200, height=630, extra_css=css)
    print("wrote", a.out)

if __name__ == "__main__": main()
