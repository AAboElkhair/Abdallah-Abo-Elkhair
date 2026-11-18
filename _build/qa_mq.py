import os,sys
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'));O=sys.argv[1]
os.makedirs(O,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch()
    for lang,path in (('en','aplus-mq/index.html'),('ar','aplus-mq/ar/index.html')):
        for w in (390,1280):
            for cs in ('light','dark'):
                c=b.new_context(viewport={'width':w,'height':900},color_scheme=cs);pg=c.new_page();pg.goto('file://'+R+'/'+path);pg.wait_for_timeout(400)
                sw=pg.evaluate('document.documentElement.scrollWidth');
                over=pg.evaluate('''()=>[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1&&!e.closest('.tabs,.shot')&&r.width>0}).map(e=>e.className||e.tagName).slice(0,5)''')
                vis=pg.evaluate("[...document.querySelectorAll('.lg-l,.lg-d')].filter(e=>e.offsetParent).map(e=>e.className)")
                print(lang,w,cs,'scrollW',sw,'overflow',over,'logo',vis)
                pg.screenshot(path=f'{O}/{lang}-{w}-{cs}.png',full_page=True);c.close()
    b.close()
