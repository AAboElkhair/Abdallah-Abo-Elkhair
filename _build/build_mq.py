#!/usr/bin/env python3
"""Builds the A+ MQ product mini-site: aplus-mq/index.html (EN) and aplus-mq/ar/index.html (AR)."""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE = 'https://aaboelkhair.github.io/Abdallah-Abo-Elkhair/'
MAIL = 'a.aboalkhair99@gmail.com'
GA = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-0K38B1126B"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","G-0K38B1126B");</script>'
GSC = '<meta name="google-site-verification" content="oB1Y7vtP2tWkz8GH9cx0OZ_tzoRiDiCoBTRpXzOVgYY">'

ICONS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="b" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="10" height="18" rx="1"/><path d="M15 9h4v12h-4M8 7h4M8 11h4M8 15h4"/><circle cx="17.5" cy="5.5" r="2.5"/></symbol>
<symbol id="r" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/></symbol>
<symbol id="d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></symbol>
<symbol id="l" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 15h18M9 15v5M7 8h6v4H7z"/></symbol>
<symbol id="t" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19l7-7"/><rect x="12" y="4" width="8" height="7" rx="1.5"/></symbol>
<symbol id="e" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 16h6M13.5 13.5L16 16l-2.5 2.5"/></symbol>
<symbol id="s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><path d="M12 8v4l2.5 2"/></symbol>
<symbol id="q" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h10M4 18h7"/></symbol>
</defs></svg>'''

# Shared illustrative mockups (English UI, sample data only)
def tile(icon, name, live):
    return f'<div class="tl{"" if live else " soon"}"><b>{"In use" if live else "Soon"}</b><svg><use href="#{icon}"/></svg>{name}</div>'

def ribbon():
    t = ''.join([tile('b','Building Explorer',1), tile('r','Furnishing Report',1), tile('d','Equipment Datasheet',1),
                 tile('l','Room Layout Sheet',1), tile('t','Room Tags Auto Leader',1), tile('e','Sheet Export',1)])
    return ('<div class="card ribbon" dir="ltr" aria-hidden="true"><div class="tabs"><span class="f">File</span><span>Architecture</span><span>Systems</span><span>Annotate</span><span>View</span><span class="on">A+ MQ</span></div>'
            f'<div class="tools">{t}</div></div>')

SHOTS = {
 'explorer': '<div style="font-weight:700;margin-bottom:2px">Level 02 · 18 rooms</div><div class="bar"><i style="width:72%"></i></div><div class="li">Operating Room 01<em class="ok">Furnished</em></div><div class="li">Recovery Bay<em class="ms">3 missing</em></div><div class="li">Sterile Store<em class="ok">Furnished</em></div><div class="li">Isolation Room<em class="ms">5 missing</em></div>',
 'report': '<table class="tbl"><tr><th>Room</th><th>Furnished</th><th>Missing</th></tr><tr><td>Operating Room 01</td><td><em class="li ok" style="display:inline;padding:1px 8px;margin:0;border:0">Yes</em></td><td>0</td></tr><tr><td>Recovery Bay</td><td>Partly</td><td>3</td></tr><tr><td>Sterile Store</td><td><em class="li ok" style="display:inline;padding:1px 8px;margin:0;border:0">Yes</em></td><td>0</td></tr><tr><td>Isolation Room</td><td>Partly</td><td>5</td></tr><tr><td>Staff Lounge</td><td>No</td><td>9</td></tr></table>',
 'datasheet': '<div class="paper"><h6>Equipment Datasheet</h6><div class="sk m"></div><div class="two"><div><div class="sk s"></div><div class="sk"></div><div class="sk"></div></div><div><div class="sk s"></div><div class="sk"></div><div class="sk"></div></div></div><div class="sk s" style="margin-top:12px"></div><div class="sk m"></div></div>',
 'layout': '<svg viewBox="0 0 280 150" width="100%" height="150" role="img" aria-hidden="true"><rect x="6" y="6" width="268" height="138" rx="4" fill="var(--card)" stroke="var(--line)"/><rect x="26" y="20" width="150" height="84" fill="none" stroke="var(--ink)" stroke-width="2"/><path d="M26 82h0M96 104h30" stroke="var(--card)" stroke-width="4"/><path d="M96 104a30 30 0 0 1 30 0" fill="none" stroke="var(--mute)"/><rect x="40" y="32" width="36" height="24" fill="var(--blue-s)" stroke="var(--blue)"/><rect x="118" y="32" width="44" height="16" fill="var(--blue-s)" stroke="var(--blue)"/><rect x="140" y="64" width="22" height="22" rx="11" fill="var(--blue-s)" stroke="var(--blue)"/><rect x="190" y="20" width="72" height="84" fill="none" stroke="var(--line)"/><rect x="196" y="28" width="60" height="6" rx="3" fill="var(--line)"/><rect x="196" y="42" width="44" height="6" rx="3" fill="var(--line)"/><rect x="196" y="56" width="52" height="6" rx="3" fill="var(--line)"/><rect x="26" y="114" width="236" height="22" fill="none" stroke="var(--line)"/><rect x="34" y="122" width="70" height="6" rx="3" fill="var(--mute)" opacity=".5"/></svg>',
 'tags': '<svg viewBox="0 0 280 150" width="100%" height="150" role="img" aria-hidden="true"><rect x="14" y="14" width="120" height="70" fill="none" stroke="var(--ink)" stroke-width="2"/><rect x="134" y="14" width="132" height="70" fill="none" stroke="var(--ink)" stroke-width="2"/><rect x="14" y="84" width="252" height="52" fill="none" stroke="var(--ink)" stroke-width="2"/><path d="M60 52L48 118" stroke="var(--red)" stroke-width="1.5"/><path d="M200 50L214 118" stroke="var(--red)" stroke-width="1.5"/><path d="M110 112L150 120" stroke="var(--red)" stroke-width="1.5"/><g font-family="Manrope,sans-serif" font-size="11" font-weight="700" text-anchor="middle"><rect x="30" y="104" width="38" height="18" rx="3" fill="var(--card)" stroke="var(--red)"/><text x="49" y="117" fill="var(--ink)">101</text><rect x="196" y="104" width="38" height="18" rx="3" fill="var(--card)" stroke="var(--red)"/><text x="215" y="117" fill="var(--ink)">102</text><rect x="116" y="104" width="38" height="18" rx="3" fill="var(--card)" stroke="var(--red)"/><text x="135" y="117" fill="var(--ink)">103</text></g></svg>',
 'export': '<div class="li"><span class="cb on"></span>A-101 · Level 01 Plan<span class="exp"><u>DWG</u><u>PDF</u></span></div><div class="li"><span class="cb on"></span>A-102 · Level 02 Plan<span class="exp"><u>DWG</u><u>PDF</u></span></div><div class="li"><span class="cb on"></span>R-201 · Room Layout 201<span class="exp"><u>DWG</u><u>PDF</u></span></div><div class="li"><span class="cb"></span>R-202 · Room Layout 202<span class="exp"><u>DWG</u><u>PDF</u></span></div>',
}

L = {
'en': dict(
 lang='en', dir='ltr', rel='', home=BASE + 'aplus-mq/', other=BASE + 'aplus-mq/ar/', other_href='ar/', other_label='العربية', portfolio='../',
 title='A+ MQ: Revit Plugin for Medical Equipment Planners',
 desc='A+ MQ is a Revit plugin for medical equipment planners on hospital BIM projects: furnishing status, datasheets, layout sheets, room tags and sheet export. Launching soon.',
 nav=[('#tools','Tools'),('#roadmap','Roadmap'),('#licensing','Licensing'),('#faq','FAQ')], cta='Get early access', ctasub='Launching soon',
 kick='Revit plugin · Launching soon',
 h1='Stop repeating Revit work. <em>Plan the equipment.</em>',
 lede='A+ MQ adds a tab to Revit for medical equipment planners: furnishing status, datasheets, layout sheets, room tags and sheet export, built from daily work on large hospital projects.',
 see='See the tools', note='Six tools are in daily use and being tested. Release is coming soon.',
 pains_h='The repetitive work behind every hospital model', pains_s='These are the questions and tasks that eat a planner\'s week. A+ MQ is built around them.',
 pains=[('b','Which rooms are furnished?','A clear status for every room, level by level.'),('r','What is still missing?','Furnished rooms and missing items in one report.'),('d','Are datasheets up to date?','Datasheets generated straight from the equipment database.'),('l','Layout sheets and tags','A layout sheet for every room and tags with leaders, without drawing each one by hand.')],
 tools_h='Six tools in daily use', tools_s='Each tool does one repetitive job well. They are being tested on real planning work and will be released soon.',
 tools=[('explorer','Building Explorer','Room-by-room furnishing status across the whole building.'),('report','Furnishing Report','Furnished rooms and missing items, ready to review.'),('datasheet','Equipment Datasheet','Datasheets straight from the equipment database.'),('layout','Room Layout Sheet','A ready layout sheet for every room in one click.'),('tags','Room Tags Auto Leader','Room tags placed with automatic leaders.'),('export','Sheet Export','Sheets exported to CAD or PDF in one click, no hassle.')],
 inuse='In daily use',
 cav='Illustrative mockups with sample data. They show the idea of each tool and are not screenshots of the released plugin.',
 road_h='Ten more tools on the way', road_s='The roadmap follows what a planner actually needs on a hospital model.',
 road=[('Healthcare QA',['Item Code Guard']),('Planning',['Smart Placement','RDS Sync','RBR Schedule','Equipment BOQ']),('Coordination',['Utility Matrix','Medical Gas Map','Ceiling Load Map','Clearance Check']),('Sheets',['As-Built Tracker'])],
 ask='If one tool could save you the most time in medical equipment planning on Revit, which would it be? Tell us and it moves up the list.', askbtn='Tell us your pick',
 by_h='Built by a planner, for planners', by_p='A+ MQ grew out of the day-to-day work of Abdallah Abo-Elkhair, a Medical Equipment Planning Engineer. It started with Building Explorer and became a full Revit plugin.', by_a='About the author', 
 lic_h='Licensing for individuals, teams and companies', lic_s='Pricing is announced at launch. Teams and companies get a lower price per seat.',
 lic=[('Individual','For a single planner or BIM specialist.',['One user','Full toolset once released'],False),
      ('Team','For planning teams on shared projects.',['Several seats under one license','Lower price per seat','For shared projects'],True),
      ('Company','For firms and contractors rolling it out across projects.',['Many seats across projects','Lower price per seat','Talk to us about your needs'],False)],
 licbadge='Lower per seat', licprice='Pricing at launch', licbtn='Ask about this plan',
 faq_h='Questions', faq=[
  ('Who is A+ MQ for?','Medical equipment planners and BIM teams who plan equipment for hospitals in Revit.'),
  ('Is it available now?','Not yet. Six tools are in daily use and still being tested. Join the early-access list and you will hear first.'),
  ('Will there be team and company licenses?','Yes. Team and company licenses are planned with a lower price per seat. Get in touch to discuss your team.'),
  ('Can I suggest a tool?','Yes. The roadmap is shaped by planners\' feedback. Send your suggestion by email or LinkedIn.'),
  ('Is A+ MQ affiliated with Autodesk?','No. It is an independent product for use with Autodesk Revit.')],
 end_h='Be first to try A+ MQ', end_p='Join the early-access list, or tell us what your team needs.', end_b='Email us', end_b2='Message on LinkedIn',
 foot='A+ MQ is an independent product by Abdallah Abo-Elkhair.', foot_a='Autodesk and Revit are trademarks of Autodesk, Inc. A+ MQ is not affiliated with or endorsed by Autodesk.', copy='© 2026 A+ MQ. All rights reserved.', portlabel='Portfolio',
 mail_sub='A+ MQ early access', 
),
'ar': dict(
 lang='ar', dir='rtl', rel='../', home=BASE + 'aplus-mq/ar/', other=BASE + 'aplus-mq/', other_href='../', other_label='English', portfolio='../../ar/',
 title='A+ MQ: إضافة Revit لمخططي المعدات الطبية',
 desc='A+ MQ إضافة على Revit لمخططي المعدات الطبية في مشاريع المستشفيات: حالة الفرش، الداتا شيت، Layout Sheets، تاجات الغرف وتصدير الشيتات. تُطلق قريبًا.',
 nav=[('#tools','الأدوات'),('#roadmap','الخطة'),('#licensing','التراخيص'),('#faq','أسئلة')], cta='احجز وصولًا مبكرًا', ctasub='قريبًا',
 kick='إضافة Revit · تُطلق قريبًا',
 h1='كفاية شغل متكرر على Revit. <em>خطّط المعدات.</em>',
 lede='A+ MQ تضيف تبويبًا على Revit لمخططي المعدات الطبية: حالة الفرش، الداتا شيت، الـ Layout Sheets، تاجات الغرف وتصدير الشيتات. خرجت من الشغل اليومي في مشاريع المستشفيات الكبيرة.',
 see='شوف الأدوات', note='ست أدوات شغالة في الاستخدام اليومي وتحت الاختبار، والإطلاق قريب.',
 pains_h='الشغل المتكرر وراء كل موديل مستشفى', pains_s='دي الأسئلة والمهام اللي بتاكل أسبوع المخطط. A+ MQ مبنية حولها.',
 pains=[('b','أنهي غرف اتفرشت؟','حالة واضحة لكل غرفة، دور بدور.'),('r','إيه اللي لسه ناقص؟','الغرف المفروشة والعناصر الناقصة في تقرير واحد.'),('d','الداتا شيت متحدثة؟','داتا شيت بتتولد مباشرة من قاعدة بيانات المعدات.'),('l','Layout Sheets والتاجات','Layout Sheet لكل غرفة وتاجات بالـ leaders من غير رسم كل واحدة يدويًا.')],
 tools_h='ست أدوات في الاستخدام اليومي', tools_s='كل أداة بتخلص مهمة متكررة واحدة بإتقان. بتتجرب على شغل تخطيط حقيقي وهتنزل قريبًا.',
 tools=[('explorer','Building Explorer','حالة فرش كل غرفة في المبنى كله، غرفة غرفة.'),('report','Furnishing Report','الغرف المفروشة والعناصر الناقصة في تقرير جاهز للمراجعة.'),('datasheet','Equipment Datasheet','داتا شيت لكل جهاز مباشرة من قاعدة بيانات المعدات.'),('layout','Room Layout Sheet','شيت Layout جاهز لكل غرفة بضغطة زر.'),('tags','Room Tags Auto Leader','تاجات الغرف بالـ leaders أوتوماتيك.'),('export','Sheet Export','تصدير الشيتات CAD أو PDF بضغطة واحدة من غير تعقيدات.')],
 inuse='شغالة يوميًا',
 cav='رسومات توضيحية ببيانات تجريبية. بتوضح فكرة كل أداة، وليست لقطات شاشة من الإضافة بعد إطلاقها.',
 road_h='عشر أدوات أخرى في الطريق', road_s='الخطة بتمشي على اللي المخطط محتاجه فعلًا في موديل المستشفى.',
 road=[('Healthcare QA',['Item Code Guard']),('Planning',['Smart Placement','RDS Sync','RBR Schedule','Equipment BOQ']),('Coordination',['Utility Matrix','Medical Gas Map','Ceiling Load Map','Clearance Check']),('Sheets',['As-Built Tracker'])],
 ask='لو أداة واحدة توفر عليك أكبر وقت في تخطيط المعدات الطبية على Revit، تبقى إيه؟ قولنا وهتتقدم في القائمة.', askbtn='قولنا اختيارك',
 by_h='مبنية بإيد مخطط، لمخططين', by_p='A+ MQ خرجت من الشغل اليومي لعبدالله أبو الخير، مهندس تخطيط معدات طبية. بدأت بـ Building Explorer وبقت إضافة كاملة على Revit.', by_a='عن المؤلف',
 lic_h='تراخيص للأفراد والفرق والشركات', lic_s='الأسعار تُعلن عند الإطلاق. الفرق والشركات بسعر أقل للمقعد الواحد.',
 lic=[('فرد','لمخطط أو BIM specialist واحد.',['مستخدم واحد','الأدوات كاملة عند الإطلاق'],False),
      ('فريق','لفرق التخطيط على مشاريع مشتركة.',['عدة مقاعد في ترخيص واحد','سعر أقل للمقعد','لمشاريع مشتركة'],True),
      ('شركة','للشركات والمقاولين اللي هتطبقها على مشاريع كتير.',['مقاعد كتير على مشاريع متعددة','سعر أقل للمقعد','كلمنا نعرف احتياجك'],False)],
 licbadge='أقل للمقعد', licprice='السعر عند الإطلاق', licbtn='اسأل عن الباقة',
 faq_h='أسئلة', faq=[
  ('A+ MQ لمين؟','لمخططي المعدات الطبية وفرق BIM اللي بيخططوا معدات المستشفيات على Revit.'),
  ('هي متاحة دلوقتي؟','لسه. ست أدوات شغالة يوميًا وتحت الاختبار. سجّل في قائمة الوصول المبكر وهتعرف أول ناس.'),
  ('هل فيه تراخيص للفرق والشركات؟','أيوه. تراخيص الفرق والشركات مخططة بسعر أقل للمقعد. كلمنا لنناقش احتياج فريقك.'),
  ('أقدر أقترح أداة؟','أيوه. الخطة بتتشكل بآراء المخططين. ابعت اقتراحك على الإيميل أو LinkedIn.'),
  ('هل A+ MQ تابعة لـ Autodesk؟','لا. هي منتج مستقل بيشتغل مع Autodesk Revit.')],
 end_h='كن أول من يجرّب A+ MQ', end_p='سجّل في قائمة الوصول المبكر، أو قولنا فريقك محتاج إيه.', end_b='راسلنا بالإيميل', end_b2='رسالة على LinkedIn',
 foot='A+ MQ منتج مستقل من عبدالله أبو الخير.', foot_a='Autodesk وRevit علامتان تجاريتان لشركة Autodesk, Inc. وA+ MQ غير تابعة لها أو معتمدة منها.', copy='© 2026 A+ MQ. جميع الحقوق محفوظة.', portlabel='الموقع الشخصي',
 mail_sub='وصول مبكر A+ MQ',
)}

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def page(k):
    t = L[k]; r = t['rel']
    mail = f'mailto:{MAIL}?subject=' + t['mail_sub'].replace('+','%2B').replace(' ', '%20')
    jld = {"@context":"https://schema.org","@type":"SoftwareApplication","name":"A+ MQ","applicationCategory":"DesignApplication","description":t['desc'],"url":t['home'],"inLanguage":t['lang'],"creator":{"@type":"Person","name":"Abdallah Abo-Elkhair","url":BASE}}
    nav = ''.join(f'<a href="{h}">{esc(x)}</a>' for h,x in t['nav'])
    pains = ''.join(f'<div class="card pain"><svg><use href="#{i}"/></svg><b>{esc(a)}</b><span>{esc(b)}</span></div>' for i,a,b in t['pains'])
    tools = ''.join(f'<article class="card tc"><div class="shot" dir="ltr" aria-hidden="true">{SHOTS[s]}</div><div class="tx"><span class="tag">{t["inuse"]}</span><h3>{n}</h3><p>{esc(d)}</p></div></article>' for s,n,d in t['tools'])
    road = ''.join(f'<div class="card rd"><h3>{h}</h3><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>' for h,items in t['road'])
    lic = ''
    for name,forr,feats,hl in t['lic']:
        lic += (f'<div class="card lc{" hl" if hl else ""}">' + (f'<span class="badge">{t["licbadge"]}</span>' if hl else '') +
                f'<h3>{name}</h3><div class="for">{esc(forr)}</div><div class="pr">{t["licprice"]}</div><ul>' + ''.join(f'<li>{esc(f)}</li>' for f in feats) +
                f'</ul><div style="margin-top:auto;padding-top:18px"><a class="btn ghost" href="{mail}">{t["licbtn"]}</a></div></div>')
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in t['faq'])
    faqld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in t['faq']]}
    og = BASE + 'aplus-mq/assets/og.png'
    hreflang = f'<link rel="alternate" hreflang="en" href="{BASE}aplus-mq/"><link rel="alternate" hreflang="ar" href="{BASE}aplus-mq/ar/"><link rel="alternate" hreflang="x-default" href="{BASE}aplus-mq/">'
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}" dir="{t['dir']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t['title'])}</title><meta name="description" content="{esc(t['desc'])}"><meta name="color-scheme" content="light dark">
<link rel="canonical" href="{t['home']}">{hreflang}
<meta property="og:type" content="website"><meta property="og:site_name" content="A+ MQ"><meta property="og:title" content="{esc(t['title'])}"><meta property="og:description" content="{esc(t['desc'])}"><meta property="og:url" content="{t['home']}"><meta property="og:image" content="{og}"><meta property="og:locale" content="{'ar_AR' if k=='ar' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(t['title'])}"><meta name="twitter:description" content="{esc(t['desc'])}"><meta name="twitter:image" content="{og}">
<link rel="icon" href="{r}assets/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="{r}assets/favicon-32.png"><link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">{GSC}{GA}
<link rel="preload" href="{r}fonts/manrope-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/mq.css?v=1">
<script type="application/ld+json">{json.dumps(jld, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(faqld, ensure_ascii=False)}</script></head>
<body>{ICONS}
<header class="nav"><div class="wrap"><a class="logo" href="./" aria-label="A+ MQ"><picture><source media="(prefers-color-scheme: dark)" srcset="{r}assets/logo-horizontal-white.png"><img src="{r}assets/logo-horizontal.png" alt="A+ MQ" width="120" height="38"></picture></a><nav aria-label="Main">{nav}</nav><a class="lang" href="{t['other_href']}" hreflang="{'en' if k=='ar' else 'ar'}">{t['other_label']}</a><a class="btn" href="{mail}">{t['cta']}</a></div></header>
<main>
<div class="hero"><div class="wrap"><div><span class="kick"><i></i>{t['kick']}</span><h1>{t['h1']}</h1><p class="lede">{esc(t['lede'])}</p><div class="row"><a class="btn" href="{mail}">{t['cta']}</a><a class="btn ghost" href="#tools">{t['see']}</a></div><p class="note">{esc(t['note'])}</p></div>{ribbon()}</div></div>
<section class="sec"><div class="wrap"><h2>{esc(t['pains_h'])}</h2><p class="sub">{esc(t['pains_s'])}</p><div class="pains">{pains}</div></div></section>
<section class="sec" id="tools" style="padding-top:20px"><div class="wrap"><div class="eyebrow">{t['inuse']}</div><h2>{esc(t['tools_h'])}</h2><p class="sub">{esc(t['tools_s'])}</p><div class="grid3">{tools}</div><p class="cav">{esc(t['cav'])}</p></div></section>
<section class="sec" id="roadmap" style="padding-top:20px"><div class="wrap"><h2>{esc(t['road_h'])}</h2><p class="sub">{esc(t['road_s'])}</p><div class="road">{road}</div><div class="card ask"><p>{esc(t['ask'])}</p><a class="btn" href="{mail}">{t['askbtn']}</a></div></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap"><div class="card by"><div class="av"><img src="{r}assets/icon-128.png" alt="" width="40" height="40"></div><div><h2 style="font-size:24px;margin-bottom:8px">{esc(t['by_h'])}</h2><p>{esc(t['by_p'])} <a href="{t['portfolio']}">{t['by_a']}</a></p></div></div></div></section>
<section class="sec" id="licensing" style="padding-top:20px"><div class="wrap"><h2>{esc(t['lic_h'])}</h2><p class="sub">{esc(t['lic_s'])}</p><div class="lic">{lic}</div></div></section>
<section class="sec" id="faq" style="padding-top:20px"><div class="wrap"><h2>{t['faq_h']}</h2><div class="faq">{faq}</div></div></section>
<section style="padding-top:10px"><div class="wrap"><div class="cta"><h2>{esc(t['end_h'])}</h2><p>{esc(t['end_p'])}</p><div class="row" style="justify-content:center"><a class="btn" href="{mail}">{t['end_b']}</a><a class="btn ghost" href="https://linkedin.com/in/abo-elkhair" target="_blank" rel="noopener">{t['end_b2']}</a></div></div></div></section>
</main>
<footer><div class="wrap"><div class="fr"><strong style="color:var(--ink)">A+ MQ</strong><span><a href="{t['portfolio']}">{t['portlabel']}</a> · <a href="{t['other_href']}">{t['other_label']}</a></span></div><small>{esc(t['foot'])} {esc(t['foot_a'])}</small><small style="margin-top:8px">{esc(t['copy'])}</small></div></footer>
</body></html>'''

def main():
    for k, path in (('en', 'aplus-mq/index.html'), ('ar', 'aplus-mq/ar/index.html')):
        p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(page(k))
    print('built aplus-mq EN + AR')

if __name__ == '__main__':
    main()
