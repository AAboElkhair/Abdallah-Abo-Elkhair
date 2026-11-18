#!/usr/bin/env python3
"""Render an HTML snippet/file to a WebP image with Playwright (used for covers and infographics).

    from render import html_to_webp
    html_to_webp(html_string, "images/my-infographic.webp", width=1200, height=None)

height=None renders the full page height. All fonts come from _build/fonts (no network needed).
Use the CSS variables and the @font-face block in FONT_CSS so images match the site (navy and gold).
"""
import sys, tempfile, os
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"

FONT_CSS = f"""
@font-face{{font-family:'Cormorant';font-weight:600;src:url('file://{FONTS}/cormorant-garamond-latin-600-normal.woff2')}}
@font-face{{font-family:'Cormorant';font-weight:700;src:url('file://{FONTS}/cormorant-garamond-latin-700-normal.woff2')}}
@font-face{{font-family:'Manrope';font-weight:500;src:url('file://{FONTS}/manrope-latin-500-normal.woff2')}}
@font-face{{font-family:'Manrope';font-weight:600;src:url('file://{FONTS}/manrope-latin-600-normal.woff2')}}
@font-face{{font-family:'Manrope';font-weight:700;src:url('file://{FONTS}/manrope-latin-700-normal.woff2')}}
@font-face{{font-family:'AmiriAr';font-weight:700;src:url('file://{FONTS}/amiri-arabic-700-normal.woff2')}}
@font-face{{font-family:'CairoAr';font-weight:400;src:url('file://{FONTS}/cairo-arabic-400-normal.woff2')}}
@font-face{{font-family:'CairoAr';font-weight:600;src:url('file://{FONTS}/cairo-arabic-600-normal.woff2')}}
:root{{--navy:#0B1626;--navy2:#13243B;--gold:#D8B56B;--gold2:#C9A24D;--ink:#EEEADF;--muted:#99A8BA;--paper:#F4F5F8;--line:#1D2E44}}
*{{box-sizing:border-box;margin:0;padding:0}}
"""

def html_to_webp(body_html, out_path, width=1200, height=None, quality=88, extra_css=""):
    from playwright.sync_api import sync_playwright
    page = f"<!doctype html><meta charset='utf-8'><style>{FONT_CSS}{extra_css}</style><body>{body_html}</body>"
    tmp = Path(tempfile.mkdtemp()) / "r.html"; tmp.write_text(page, encoding="utf-8")
    png = tmp.with_suffix(".png")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": width, "height": height or 800}, device_scale_factor=1)
        pg.goto(f"file://{tmp}"); pg.wait_for_timeout(400)
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(png), full_page=height is None, clip=None if height is None else {"x":0,"y":0,"width":width,"height":height})
        b.close()
    Image.open(png).convert("RGB").save(out_path, "WEBP", quality=quality, method=6)
    return out_path
