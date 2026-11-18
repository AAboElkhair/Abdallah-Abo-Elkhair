#!/usr/bin/env python3
"""Renders aplus-mq/assets/og.png (1200x630)."""
import os
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
html=f'''<html><head><style>
@font-face{{font-family:M;font-weight:700;src:url(file://{R}/aplus-mq/fonts/manrope-latin-700-normal.woff2)}}
@font-face{{font-family:M;font-weight:600;src:url(file://{R}/aplus-mq/fonts/manrope-latin-600-normal.woff2)}}
body{{margin:0;width:1200px;height:630px;background:#f3f5fa;font-family:M;color:#0f1630;position:relative;overflow:hidden;
background-image:linear-gradient(rgba(47,85,224,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(47,85,224,.07) 1px,transparent 1px);background-size:40px 40px}}
img{{position:absolute;left:80px;top:70px;height:120px}}
h1{{position:absolute;left:80px;top:250px;margin:0;width:900px;font-size:84px;line-height:1.05;letter-spacing:-2px}}
h1 em{{font-style:normal;color:#2f55e0}}
.b{{position:absolute;left:80px;bottom:70px;background:#2f55e0;color:#fff;font-weight:700;font-size:30px;padding:14px 30px;border-radius:99px}}
</style></head><body><img src="file://{R}/aplus-mq/assets/logo-horizontal.png"><h1>Revit tools for <em>medical equipment</em> planners</h1><div class="b">Launching soon</div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1200,'height':630}); tmp=os.path.join(R,'aplus-mq/assets/_og.html'); open(tmp,'w').write(html); pg.goto('file://'+tmp); pg.wait_for_timeout(600); os.remove(tmp)
    pg.screenshot(path=os.path.join(R,'aplus-mq/assets/og.png')); b.close()
