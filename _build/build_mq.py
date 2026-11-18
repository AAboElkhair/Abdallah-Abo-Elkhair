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
<symbol id="g" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/></symbol>
<symbol id="p" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></symbol>
<symbol id="y" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 7a8 8 0 0 0-14-2L4 7"/><path d="M4 3v4h4"/><path d="M4 17a8 8 0 0 0 14 2l2-2"/><path d="M20 21v-4h-4"/></symbol>
<symbol id="k" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M3 14h18M9 9v11"/></symbol>
<symbol id="o" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h6M9 18h3"/></symbol>
<symbol id="u" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L5 14h6l-1 8 8-12h-6z"/></symbol>
<symbol id="m" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><path d="M12 7v6M9 10h6"/></symbol>
<symbol id="c" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h18"/><path d="M12 4v9M8.5 10L12 13.5 15.5 10"/><rect x="7" y="16" width="10" height="5" rx="1"/></symbol>
<symbol id="x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="8" height="8" rx="1"/><path d="M4 4h4M4 4v4M20 4h-4M20 4v4M4 20h4M4 20v-4M20 20h-4M20 20v-4" stroke-dasharray="2 2"/></symbol>
<symbol id="a" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21V4M5 4h11l-2 4 2 4H5"/></symbol>
<symbol id="z" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 3L4 14h7l-1 7 9-11h-7z"/></symbol>
<symbol id="v" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/></symbol>
<symbol id="h" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-8-4.5-8-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5C20 15.5 12 20 12 20z"/><path d="M12 10v5M9.5 12.5h5"/></symbol>
<symbol id="w1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></symbol>
<symbol id="w2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 13.5a7 7 0 0 1 4 6.5"/></symbol>
<symbol id="w3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14"/><path d="M10 21v-5h4v5M12 8v4M10 10h4"/></symbol>
<symbol id="w4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/></symbol>
<symbol id="ck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
<symbol id="ar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
</defs></svg>'''

# Illustrative mockups (English UI, sample data only)
SHOTS = {
 'explorer': '<div style="font-weight:700;margin-bottom:2px">Level 02 · 18 rooms</div><div class="bar"><i style="width:72%"></i></div><div class="li">Operating Room 01<em class="ok">Furnished</em></div><div class="li">Recovery Bay<em class="ms">3 missing</em></div><div class="li">Sterile Store<em class="ok">Furnished</em></div><div class="li">Isolation Room<em class="ms">5 missing</em></div>',
 'report': '<table class="tbl"><tr><th>Room</th><th>Furnished</th><th>Missing</th></tr><tr><td>Operating Room 01</td><td><em class="li ok" style="display:inline;padding:1px 8px;margin:0;border:0">Yes</em></td><td>0</td></tr><tr><td>Recovery Bay</td><td>Partly</td><td>3</td></tr><tr><td>Sterile Store</td><td><em class="li ok" style="display:inline;padding:1px 8px;margin:0;border:0">Yes</em></td><td>0</td></tr><tr><td>Isolation Room</td><td>Partly</td><td>5</td></tr><tr><td>Staff Lounge</td><td>No</td><td>9</td></tr></table>',
 'datasheet': '<div class="paper"><h6>Equipment Datasheet</h6><div class="sk m"></div><div class="two"><div><div class="sk s"></div><div class="sk"></div><div class="sk"></div></div><div><div class="sk s"></div><div class="sk"></div><div class="sk"></div></div></div><div class="sk s" style="margin-top:12px"></div><div class="sk m"></div></div>',
 'layout': '<svg viewBox="0 0 280 150" width="100%" height="150" role="img" aria-hidden="true"><rect x="6" y="6" width="268" height="138" rx="4" fill="var(--card)" stroke="var(--line)"/><rect x="26" y="20" width="150" height="84" fill="none" stroke="var(--ink)" stroke-width="2"/><path d="M26 82h0M96 104h30" stroke="var(--card)" stroke-width="4"/><path d="M96 104a30 30 0 0 1 30 0" fill="none" stroke="var(--mute)"/><rect x="40" y="32" width="36" height="24" fill="var(--blue-s)" stroke="var(--blue)"/><rect x="118" y="32" width="44" height="16" fill="var(--blue-s)" stroke="var(--blue)"/><rect x="140" y="64" width="22" height="22" rx="11" fill="var(--blue-s)" stroke="var(--blue)"/><rect x="190" y="20" width="72" height="84" fill="none" stroke="var(--line)"/><rect x="196" y="28" width="60" height="6" rx="3" fill="var(--line)"/><rect x="196" y="42" width="44" height="6" rx="3" fill="var(--line)"/><rect x="196" y="56" width="52" height="6" rx="3" fill="var(--line)"/><rect x="26" y="114" width="236" height="22" fill="none" stroke="var(--line)"/><rect x="34" y="122" width="70" height="6" rx="3" fill="var(--mute)" opacity=".5"/></svg>',
 'tags': '<svg viewBox="0 0 280 150" width="100%" height="150" role="img" aria-hidden="true"><rect x="14" y="14" width="120" height="70" fill="none" stroke="var(--ink)" stroke-width="2"/><rect x="134" y="14" width="132" height="70" fill="none" stroke="var(--ink)" stroke-width="2"/><rect x="14" y="84" width="252" height="52" fill="none" stroke="var(--ink)" stroke-width="2"/><path d="M60 52L48 118" stroke="var(--red)" stroke-width="1.5"/><path d="M200 50L214 118" stroke="var(--red)" stroke-width="1.5"/><path d="M110 112L150 120" stroke="var(--red)" stroke-width="1.5"/><g font-family="Manrope,sans-serif" font-size="11" font-weight="700" text-anchor="middle"><rect x="30" y="104" width="38" height="18" rx="3" fill="var(--card)" stroke="var(--red)"/><text x="49" y="117" fill="var(--ink)">101</text><rect x="196" y="104" width="38" height="18" rx="3" fill="var(--card)" stroke="var(--red)"/><text x="215" y="117" fill="var(--ink)">102</text><rect x="116" y="104" width="38" height="18" rx="3" fill="var(--card)" stroke="var(--red)"/><text x="135" y="117" fill="var(--ink)">103</text></g></svg>',
 'export': '<div class="li"><span class="cb on"></span>A-101 · Level 01 Plan<span class="exp"><u>DWG</u><u>PDF</u></span></div><div class="li"><span class="cb on"></span>A-102 · Level 02 Plan<span class="exp"><u>DWG</u><u>PDF</u></span></div><div class="li"><span class="cb on"></span>R-201 · Room Layout 201<span class="exp"><u>DWG</u><u>PDF</u></span></div><div class="li"><span class="cb"></span>R-202 · Room Layout 202<span class="exp"><u>DWG</u><u>PDF</u></span></div>',
}

def ribbon(more):
    tl = lambda i, n: f'<div class="tl"><svg><use href="#{i}"/></svg>{n}</div>'
    t = (tl('b','Building Explorer') + tl('l','Room Layout Sheet') + tl('y','RDS Sync') +
         tl('u','Utility Matrix') + tl('x','Clearance Check') + f'<div class="tl more"><b>+11</b>{more}</div>')
    return ('<div class="card ribbon" dir="ltr" aria-hidden="true"><div class="tabs"><span class="f">File</span><span>Architecture</span><span>Systems</span><span>Annotate</span><span>View</span><span class="on">A+ MQ</span></div>'
            f'<div class="tools">{t}</div></div>')

# (icon, name, category key, EN description, AR description)
TOOLS = [
 ('b','Building Explorer','ex','See the furnishing status of every room across the building, level by level, in one panel.','حالة فرش كل غرفة في المبنى كله، دور بدور، في شاشة واحدة.'),
 ('r','Furnishing Report','ex','Furnished rooms and missing items in one clear report, ready to review and share.','الغرف المفروشة والعناصر الناقصة في تقرير واحد واضح، جاهز للمراجعة والإرسال.'),
 ('d','Equipment Datasheet','ex','Generate equipment datasheets straight from the equipment database, always up to date.','داتا شيت لكل جهاز مباشرة من قاعدة بيانات المعدات، ومتحدثة دايمًا.'),
 ('l','Room Layout Sheet','sh','A ready layout sheet for every room in one click, views and titles included.','Layout Sheet جاهز لكل غرفة بضغطة واحدة، بالـ views والعناوين.'),
 ('t','Room Tags Auto Leader','sh','Place room tags with clean automatic leaders, without dragging each one by hand.','تاجات الغرف بـ leaders أوتوماتيك ونظيفة، من غير ما تسحب كل واحدة بإيدك.'),
 ('e','Sheet Export','sh','Export sheets to CAD or PDF in one click, named and organized.','تصدير الشيتات CAD أو PDF بضغطة واحدة، بأسماء مرتبة.'),
 ('a','As-Built Tracker','sh','Track equipment changes through construction and keep as-built sheets in step with the site.','متابعة تغييرات المعدات أثناء التنفيذ، وشيتات الـ As-Built ماشية مع الموقع.'),
 ('p','Smart Placement','pl','Place equipment in rooms faster and more consistently across similar room types.','وضع المعدات في الغرف أسرع وبشكل موحد في الغرف المتشابهة.'),
 ('y','RDS Sync','pl','Keep room data sheets and the Revit model in sync, so equipment lists match on both sides.','الـ Room Data Sheets والموديل متزامنين، وقوائم المعدات متطابقة في الاتنين.'),
 ('k','RBR Schedule','pl','Room-by-room equipment schedules built from the model, ready for the client.','جداول RBR غرفة غرفة من الموديل مباشرة، جاهزة للعميل.'),
 ('o','Equipment BOQ','pl','Equipment quantities and BOQ pulled from the model for costing and procurement.','كميات المعدات والـ BOQ من الموديل للتسعير والتوريد.'),
 ('u','Utility Matrix','co','Equipment utility needs, such as power, water and data, gathered in one matrix for MEP.','احتياجات المعدات من كهرباء ومياه وداتا في جدول واحد لفريق الـ MEP.'),
 ('m','Medical Gas Map','co','Medical gas requirements mapped room by room for clear coordination with MEP.','احتياجات الغازات الطبية غرفة غرفة، لتنسيق واضح مع الـ MEP.'),
 ('c','Ceiling Load Map','co','Ceiling-mounted equipment mapped with its loads for structural coordination.','المعدات المعلقة في السقف بأحمالها، للتنسيق مع الإنشائي.'),
 ('x','Clearance Check','co','Check equipment service and access clearances before they become site problems.','مراجعة مسافات الخدمة والوصول حوالين المعدات قبل ما تبقى مشكلة في الموقع.'),
 ('g','Item Code Guard','qa','Catch missing, duplicate or wrong equipment item codes before they reach schedules.','اكتشاف أكواد المعدات الناقصة أو المكررة أو الغلط قبل ما توصل للجداول.'),
]

L = {
'en': dict(
 lang='en', dir='ltr', rel='', home=BASE + 'aplus-mq/', other_href='ar/', other_label='العربية', portfolio='../',
 title='A+ MQ: Revit Plugin for Medical Equipment Planners',
 desc='A+ MQ puts 16 Revit tools for medical equipment planners in one tab: furnishing status, datasheets, layout sheets, schedules, BOQ, utilities and QA. Launching soon.',
 nav=[('#tools','Tools'),('#how','How it works'),('#licensing','Licensing'),('#faq','FAQ')],
 demo='Request a demo', demo_sub='A+ MQ demo request', demo_body='Name:\nCompany:\nTeam size:\nPreferred time for a demo:\n',
 cta='Get early access', mail_sub='A+ MQ early access', see='Explore the 16 tools',
 kick='Revit plugin for medical equipment planning · Launching soon',
 h1='Medical equipment planning in Revit, <em>done faster.</em>',
 lede='A+ MQ puts 16 tools in one Revit tab: furnishing status, datasheets, layout sheets, schedules, BOQ, utilities, medical gases and QA checks. Less clicking, cleaner deliverables, and more time for the planning decisions that matter.',
 trust=['Built by a medical equipment planner','16 tools in one Revit tab','Team and company licenses'],
 more='more tools',
 out_h='Deliver hospital projects faster, and better', out_s='Repetitive Revit work slows every healthcare project down. A+ MQ automates it, so your team spends its time on planning, not on clicking.',
 out=[('z','Faster delivery','Tasks that take hours of manual work run in a click, so packages reach the client sooner.'),
      ('g','Fewer errors','Automatic checks catch missing items, wrong codes and clearance issues before the client or the site does.'),
      ('v','Consistent deliverables','Every sheet, tag, schedule and datasheet follows the same standard, on every project and every team member.'),
      ('h','Better healthcare projects','More time for clinical planning means better-equipped rooms, smoother coordination and safer hospitals.')],
 ba_h='From manual work to one click', ba_s='The same planning tasks, without the repetition.', ba_l='Without A+ MQ', ba_r='With A+ MQ',
 ba=[('Furnishing status','Checking rooms one by one in views and schedules','A building-wide status in one panel'),
     ('Datasheets','Copying equipment data into documents by hand','Generated straight from the equipment database'),
     ('Layout sheets','Setting up every room sheet view by view','A layout sheet for every room in one click'),
     ('RDS and schedules','Keeping spreadsheets and the model aligned manually','RDS, RBR schedules and BOQ synced with the model'),
     ('MEP coordination','Rebuilding utility and gas lists for every issue','Utility matrix and medical gas map from the model'),
     ('QA and export','Manual reviews, then exporting sheets one by one','Codes and clearances checked, sheets exported in one click')],
 tools_h='16 tools. One tab. Every stage of planning.', tools_s='From the first room survey to as-built sheets, A+ MQ covers the repetitive work of medical equipment planning in Revit.',
 cats=[('all','All tools'),('ex','Explore and report'),('sh','Sheets and documentation'),('pl','Planning'),('co','Coordination'),('qa','Healthcare QA')],
 show_h='See it in action', show_s='A look at how some of the tools present your model data.',
 shows=[('explorer','Building Explorer'),('report','Furnishing Report'),('datasheet','Equipment Datasheet'),('layout','Room Layout Sheet'),('tags','Room Tags Auto Leader'),('export','Sheet Export')],
 cav='Illustrative mockups with sample data, showing the idea of each tool.',
 how_h='Up and running in three steps', how=[('Open your hospital model','A+ MQ adds its own tab to the Revit ribbon, next to the tools you already use.'),('Pick a tool','Run reports, sheets, schedules, coordination maps and checks in a click.'),('Deliver with confidence','Send consistent, checked outputs to the client, the design team and the site.')],
 who_h='Made for the people who equip hospitals', who=[('w1','Medical equipment planners','Spend less time on Revit chores and more on planning.'),('w2','Healthcare BIM teams','Standard outputs across every model and every team member.'),('w3','Hospital design firms','Faster equipment packages and smoother MEP coordination.'),('w4','Contractors and suppliers','Clear schedules, BOQ and as-built records for delivery and handover.')],
 by_h='Built by a planner, for planners', by_p='A+ MQ grew out of the day-to-day work of Abdallah Abo-Elkhair, a Medical Equipment Planning Engineer on large hospital projects. Every tool solves a task planners repeat on every project.', by_a='About the author',
 lic_h='Licensing for individuals, teams and companies', lic_s='Pricing is announced at launch. The bigger your team, the lower the price per seat.',
 lic=[('Individual','For a single planner or BIM specialist.',['One user','All 16 tools'],False,'cta'),
      ('Team','For planning teams on shared projects.',['Several seats under one license','All 16 tools','Lower price per seat'],True,'demo'),
      ('Company','For firms rolling it out across projects.',['Seats for the whole company','All 16 tools','Lowest price per seat'],False,'demo')],
 licbadge='Best for teams', licprice='Pricing at launch',
 faq_h='Questions', faq=[
  ('Who is A+ MQ for?','Medical equipment planners, healthcare BIM teams, hospital design firms and contractors who plan equipment in Revit.'),
  ('Can I see a demo?','Yes. Send a demo request with your team size and we will walk you through the tools and how they fit your workflow.'),
  ('When can I buy it?','A+ MQ is launching soon. Join early access or request a demo and you will be the first to know, with launch pricing.'),
  ('Are there team and company licenses?','Yes. Team and company licenses cost less per seat. Get in touch to discuss your team size.'),
  ('Can I suggest a tool?','Yes. A+ MQ is shaped by planners. Send your idea by email or LinkedIn.'),
  ('Is A+ MQ affiliated with Autodesk?','No. It is an independent product for use with Autodesk Revit.')],
 form=dict(h='Book your A+ MQ demo', p='Tell us a little about your team and we will get back to you by email to set a time.',
   name='Full name', email='Work email', company='Company', role='Your role', roles=['Medical equipment planner','BIM manager or coordinator','Architect or hospital designer','Contractor or equipment supplier','Other'],
   size='Team size', sizes=['Just me','2 to 5','6 to 20','More than 20'], country='Country', msg='What would you like to see? (optional)',
   send='Request my demo', sending='Sending...', ok_h='Thank you, your request is in.', ok_p='We will email you shortly to arrange your demo.',
   err='Something went wrong. Please try again, or email us directly:', note='We use your details only to arrange your demo.', choose='Select', subject='New A+ MQ demo request'),
 end_h='Ready to plan faster?', end_p='Book a demo for your team or join early access. Team and company licenses get a lower price per seat.', end_b2='Message on LinkedIn',
 foot='A+ MQ is an independent product by Abdallah Abo-Elkhair.', foot_a='Autodesk and Revit are trademarks of Autodesk, Inc. A+ MQ is not affiliated with or endorsed by Autodesk.', copy='© 2026 A+ MQ. All rights reserved.', portlabel='Portfolio',
),
'ar': dict(
 lang='ar', dir='rtl', rel='../', home=BASE + 'aplus-mq/ar/', other_href='../', other_label='English', portfolio='../../ar/',
 title='A+ MQ: إضافة Revit لمخططي المعدات الطبية',
 desc='A+ MQ بتجمع 16 أداة على Revit لمخططي المعدات الطبية في تبويب واحد: حالة الفرش، الداتا شيت، الشيتات، الجداول، الـ BOQ، الخدمات والـ QA. تُطلق قريبًا.',
 nav=[('#tools','الأدوات'),('#how','إزاي بتشتغل'),('#licensing','التراخيص'),('#faq','أسئلة')],
 demo='اطلب ديمو', demo_sub='طلب ديمو A+ MQ', demo_body='الاسم:\nالشركة:\nعدد الفريق:\nالوقت المناسب للديمو:\n',
 cta='احجز وصولًا مبكرًا', mail_sub='وصول مبكر A+ MQ', see='اكتشف الـ 16 أداة',
 kick='إضافة Revit لتخطيط المعدات الطبية · تُطلق قريبًا',
 h1='تخطيط المعدات الطبية على Revit، <em>أسرع بكتير.</em>',
 lede='A+ MQ بتجمعلك 16 أداة في تبويب واحد على Revit: حالة الفرش، الداتا شيت، الـ Layout Sheets، الجداول، الـ BOQ، الخدمات، الغازات الطبية ومراجعات الجودة. ضغطات أقل، مخرجات أنضف، ووقت أكتر لقرارات التخطيط المهمة.',
 trust=['مبنية بإيد مخطط معدات طبية','16 أداة في تبويب واحد','تراخيص للفرق والشركات'],
 more='more tools',
 out_h='سلّم مشاريع المستشفيات أسرع، وبجودة أعلى', out_s='الشغل المتكرر على Revit بيأخر أي مشروع صحي. A+ MQ بتعمله أوتوماتيك، عشان فريقك يركز في التخطيط مش في الضغط على الماوس.',
 out=[('z','تسليم أسرع','مهام بتاخد ساعات شغل يدوي بتخلص بضغطة، والباكدجات توصل للعميل بدري.'),
      ('g','أخطاء أقل','مراجعات أوتوماتيك بتكشف العناصر الناقصة والأكواد الغلط ومشاكل المسافات قبل العميل أو الموقع.'),
      ('v','مخرجات موحدة','كل شيت وتاج وجدول وداتا شيت بنفس الستاندرد، في كل مشروع ومع كل عضو في الفريق.'),
      ('h','مشاريع صحية أفضل','وقت أكتر للتخطيط الإكلينيكي يعني غرف مجهزة أحسن، تنسيق أسهل، ومستشفيات أأمن.')],
 ba_h='من الشغل اليدوي لضغطة واحدة', ba_s='نفس مهام التخطيط، من غير التكرار.', ba_l='من غير A+ MQ', ba_r='مع A+ MQ',
 ba=[('حالة الفرش','مراجعة الغرف واحدة واحدة في الـ views والجداول','حالة المبنى كله في شاشة واحدة'),
     ('الداتا شيت','نقل بيانات المعدات للمستندات يدويًا','بتتولد مباشرة من قاعدة بيانات المعدات'),
     ('Layout Sheets','تجهيز شيت كل غرفة view بـ view','Layout Sheet لكل غرفة بضغطة واحدة'),
     ('الـ RDS والجداول','مطابقة الإكسيل مع الموديل بالإيد','RDS وجداول RBR والـ BOQ متزامنين مع الموديل'),
     ('تنسيق الـ MEP','إعادة عمل قوائم الخدمات والغازات مع كل تعديل','Utility Matrix وخريطة غازات طبية من الموديل'),
     ('المراجعة والتصدير','مراجعة يدوية وتصدير الشيتات واحد واحد','الأكواد والمسافات متراجعة والتصدير بضغطة')],
 tools_h='16 أداة. تبويب واحد. كل مراحل التخطيط.', tools_s='A+ MQ بتغطي الشغل المتكرر في تخطيط المعدات الطبية على Revit، من أول حصر الغرف لحد شيتات الـ As-Built.',
 cats=[('all','كل الأدوات'),('ex','الاستكشاف والتقارير'),('sh','الشيتات والتوثيق'),('pl','التخطيط'),('co','التنسيق'),('qa','جودة المشاريع الصحية')],
 show_h='شوفها وهي شغالة', show_s='نظرة على طريقة عرض بعض الأدوات لبيانات الموديل.',
 shows=[('explorer','Building Explorer'),('report','Furnishing Report'),('datasheet','Equipment Datasheet'),('layout','Room Layout Sheet'),('tags','Room Tags Auto Leader'),('export','Sheet Export')],
 cav='رسومات توضيحية ببيانات تجريبية بتوضح فكرة كل أداة.',
 how_h='تبدأ في تلات خطوات', how=[('افتح موديل المستشفى','A+ MQ بتضيف تبويبها الخاص على شريط Revit جنب الأدوات اللي بتستخدمها.'),('اختار الأداة','تقارير، شيتات، جداول، خرايط تنسيق ومراجعات بضغطة واحدة.'),('سلّم وانت مطمن','مخرجات موحدة ومتراجعة للعميل وفريق التصميم والموقع.')],
 who_h='معمولة للناس اللي بتجهز المستشفيات', who=[('w1','مخططي المعدات الطبية','وقت أقل في شغل Revit الروتيني، ووقت أكتر للتخطيط.'),('w2','فرق BIM الصحية','مخرجات بستاندرد واحد في كل موديل ومع كل الفريق.'),('w3','مكاتب تصميم المستشفيات','باكدجات معدات أسرع وتنسيق MEP أسهل.'),('w4','المقاولين والموردين','جداول وBOQ وسجلات As-Built واضحة للتوريد والتسليم.')],
 by_h='مبنية بإيد مخطط، لمخططين', by_p='A+ MQ خرجت من الشغل اليومي لعبدالله أبو الخير، مهندس تخطيط معدات طبية في مشاريع مستشفيات كبيرة. كل أداة بتحل مهمة المخطط بيكررها في كل مشروع.', by_a='عن المؤلف',
 lic_h='تراخيص للأفراد والفرق والشركات', lic_s='الأسعار تُعلن عند الإطلاق. كل ما الفريق يكبر، سعر المقعد يقل.',
 lic=[('فرد','لمخطط أو BIM specialist واحد.',['مستخدم واحد','الـ 16 أداة كاملة'],False,'cta'),
      ('فريق','لفرق التخطيط على مشاريع مشتركة.',['عدة مقاعد في ترخيص واحد','الـ 16 أداة كاملة','سعر أقل للمقعد'],True,'demo'),
      ('شركة','للشركات اللي هتطبقها على مشاريع كتير.',['مقاعد للشركة كلها','الـ 16 أداة كاملة','أقل سعر للمقعد'],False,'demo')],
 licbadge='الأنسب للفرق', licprice='السعر عند الإطلاق',
 faq_h='أسئلة', faq=[
  ('A+ MQ لمين؟','لمخططي المعدات الطبية وفرق BIM الصحية ومكاتب تصميم المستشفيات والمقاولين اللي بيخططوا المعدات على Revit.'),
  ('أقدر أشوف ديمو؟','أيوه. ابعت طلب ديمو واكتب عدد فريقك، وهنعرّفك على الأدوات وإزاي تمشي مع طريقة شغلك.'),
  ('أقدر أشتريها إمتى؟','A+ MQ هتنزل قريب. احجز وصول مبكر أو اطلب ديمو وهتعرف أول واحد، بأسعار الإطلاق.'),
  ('فيه تراخيص للفرق والشركات؟','أيوه. تراخيص الفرق والشركات سعر المقعد فيها أقل. كلمنا عشان نتكلم عن حجم فريقك.'),
  ('أقدر أقترح أداة؟','أيوه. A+ MQ بتتشكل بآراء المخططين. ابعت فكرتك على الإيميل أو LinkedIn.'),
  ('هل A+ MQ تابعة لـ Autodesk؟','لا. هي منتج مستقل بيشتغل مع Autodesk Revit.')],
 form=dict(h='احجز ديمو A+ MQ', p='قولنا شوية عن فريقك، وهنرد عليك بالإيميل عشان نحدد معاد.',
   name='الاسم بالكامل', email='إيميل الشغل', company='الشركة', role='وظيفتك', roles=['مخطط معدات طبية','مدير أو منسق BIM','معماري أو مصمم مستشفيات','مقاول أو مورد معدات','أخرى'],
   size='حجم الفريق', sizes=['أنا بس','من 2 لـ 5','من 6 لـ 20','أكتر من 20'], country='الدولة', msg='حابب تشوف إيه في الديمو؟ (اختياري)',
   send='احجز الديمو', sending='جاري الإرسال...', ok_h='شكرًا، طلبك وصل.', ok_p='هنبعتلك إيميل قريب عشان نحدد معاد الديمو.',
   err='حصلت مشكلة. جرّب تاني، أو ابعتلنا إيميل مباشرة:', note='بياناتك بتستخدم بس لترتيب الديمو.', choose='اختار', subject='طلب ديمو جديد A+ MQ'),
 end_h='جاهز تخطط أسرع؟', end_p='احجز ديمو لفريقك أو سجّل في الوصول المبكر. تراخيص الفرق والشركات بسعر أقل للمقعد.', end_b2='رسالة على LinkedIn',
 foot='A+ MQ منتج مستقل من عبدالله أبو الخير.', foot_a='Autodesk و Revit علامتان تجاريتان لشركة Autodesk, Inc. و A+ MQ غير تابعة لها أو معتمدة منها.', copy='© 2026 A+ MQ. جميع الحقوق محفوظة.', portlabel='الموقع الشخصي',
)}

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

FILTER_JS = '''<script>document.querySelectorAll('.chips button').forEach(function(b){b.addEventListener('click',function(){var c=b.dataset.c;document.querySelectorAll('.chips button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});document.querySelectorAll('.tg .tool').forEach(function(t){t.hidden=!(c==='all'||t.dataset.c===c)})})});var fm=document.getElementById('demo-form');if(fm){fm.addEventListener('submit',function(e){if(!window.fetch)return;e.preventDefault();var b=fm.querySelector('button[type=submit]'),lbl=b.textContent,er=fm.querySelector('.ferr');er.hidden=true;b.disabled=true;b.textContent=b.dataset.sending;var d={};new FormData(fm).forEach(function(v,k){d[k]=v});fetch(fm.dataset.ajax,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json().then(function(j){if(!r.ok||String(j.success)==='false')throw 0})}).then(function(){fm.hidden=true;var ok=document.getElementById('demo-ok');ok.hidden=false;ok.scrollIntoView({block:'center'})}).catch(function(){er.hidden=false;b.disabled=false;b.textContent=lbl})})};var st=document.querySelector('.sticky');addEventListener('scroll',function(){st.classList.toggle('on',scrollY>560)},{passive:true})</script>'''

def page(k):
    from urllib.parse import quote
    t = L[k]; r = t['rel']; ar = k == 'ar'
    demo_mail = 'mailto:' + MAIL + '?subject=' + quote(t['demo_sub']) + '&body=' + quote(t['demo_body'])
    demo = '#demo'
    f = t['form']
    opts = lambda xs: f'<option value="" disabled selected>{f["choose"]}</option>' + ''.join(f'<option>{esc(x)}</option>' for x in xs)
    form = (f'<form class="card df" id="demo-form" action="https://formsubmit.co/{MAIL}" method="POST" data-ajax="https://formsubmit.co/ajax/{MAIL}">'
      f'<input type="hidden" name="_subject" value="{esc(f["subject"])}"><input type="hidden" name="_template" value="table"><input type="hidden" name="_next" value="{t["home"]}#demo"><input type="hidden" name="Page" value="{t["lang"].upper()}">'
      f'<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
      f'<label>{f["name"]}<input name="Name" required autocomplete="name"></label>'
      f'<label>{f["email"]}<input type="email" name="email" required autocomplete="email" dir="ltr"></label>'
      f'<label>{f["company"]}<input name="Company" required autocomplete="organization"></label>'
      f'<label>{f["country"]}<input name="Country" autocomplete="country-name"></label>'
      f'<label>{f["role"]}<select name="Role" required>{opts(f["roles"])}</select></label>'
      f'<label>{f["size"]}<select name="Team size" required>{opts(f["sizes"])}</select></label>'
      f'<label class="wide">{f["msg"]}<textarea name="Message" rows="3"></textarea></label>'
      f'<div class="wide fa"><button class="btn lg" type="submit" data-sending="{esc(f["sending"])}">{f["send"]}</button><small>{esc(f["note"])}</small></div>'
      f'<p class="wide ferr" hidden>{esc(f["err"])} <a href="{demo_mail}">{MAIL}</a></p></form>'
      f'<div class="card dok" id="demo-ok" hidden><svg><use href="#ck"/></svg><h3>{esc(f["ok_h"])}</h3><p>{esc(f["ok_p"])}</p></div>')
    mail = 'mailto:' + MAIL + '?subject=' + quote(t['mail_sub'])
    arrow = '<svg class="ic"><use href="#ar"/></svg>'
    jld = {"@context":"https://schema.org","@type":"SoftwareApplication","name":"A+ MQ","applicationCategory":"DesignApplication","operatingSystem":"Windows","description":t['desc'],"url":t['home'],"inLanguage":t['lang'],"creator":{"@type":"Person","name":"Abdallah Abo-Elkhair","url":BASE}}
    nav = ''.join(f'<a href="{h}">{esc(x)}</a>' for h,x in t['nav'])
    trust = ''.join(f'<li><svg><use href="#ck"/></svg>{esc(x)}</li>' for x in t['trust'])
    out = ''.join(f'<div class="card oc"><span class="oi"><svg><use href="#{i}"/></svg></span><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for i,a,b in t['out'])
    ba = ''.join(f'<div class="br"><b>{esc(a)}</b><span class="bl">{esc(x)}</span><span class="bg"><svg><use href="#ck"/></svg>{esc(y)}</span></div>' for a,x,y in t['ba'])
    catname = dict(t['cats'])
    chips = ''.join(f'<button type="button" data-c="{c}" aria-pressed="{"true" if c=="all" else "false"}">{esc(n)}</button>' for c,n in t['cats'])
    tools = ''.join(f'<article class="card tool" data-c="{c}"><span class="ti"><svg><use href="#{i}"/></svg></span><div><span class="tcat">{esc(catname[c])}</span><h3 dir="ltr">{n}</h3><p>{esc(da if ar else de)}</p></div></article>' for i,n,c,de,da in TOOLS)
    shows = ''.join(f'<figure class="card sh"><div class="shot" dir="ltr" aria-hidden="true">{SHOTS[s]}</div><figcaption dir="ltr">{n}</figcaption></figure>' for s,n in t['shows'])
    how = ''.join(f'<div class="hw"><span class="hn">{i+1}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for i,(a,b) in enumerate(t['how']))
    who = ''.join(f'<div class="card wc"><svg><use href="#{i}"/></svg><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for i,a,b in t['who'])
    lic = ''
    for name,forr,feats,hl,btn in t['lic']:
        href, label = (demo, t['demo']) if btn == 'demo' else (mail, t['cta'])
        lic += (f'<div class="card lc{" hl" if hl else ""}">' + (f'<span class="badge">{t["licbadge"]}</span>' if hl else '') +
                f'<h3>{name}</h3><div class="for">{esc(forr)}</div><div class="pr">{t["licprice"]}</div><ul>' + ''.join(f'<li>{esc(f)}</li>' for f in feats) +
                f'</ul><div style="margin-top:auto;padding-top:18px"><a class="btn{"" if hl else " ghost"} full" href="{href}">{label}</a></div></div>')
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in t['faq'])
    faqld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in t['faq']]}
    og = BASE + 'aplus-mq/assets/og.png'
    hreflang = f'<link rel="alternate" hreflang="en" href="{BASE}aplus-mq/"><link rel="alternate" hreflang="ar" href="{BASE}aplus-mq/ar/"><link rel="alternate" hreflang="x-default" href="{BASE}aplus-mq/">'
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}" dir="{t['dir']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t['title'])}</title><meta name="description" content="{esc(t['desc'])}"><meta name="color-scheme" content="light dark">
<link rel="canonical" href="{t['home']}">{hreflang}
<meta property="og:type" content="website"><meta property="og:site_name" content="A+ MQ"><meta property="og:title" content="{esc(t['title'])}"><meta property="og:description" content="{esc(t['desc'])}"><meta property="og:url" content="{t['home']}"><meta property="og:image" content="{og}"><meta property="og:locale" content="{'ar_AR' if ar else 'en_US'}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(t['title'])}"><meta name="twitter:description" content="{esc(t['desc'])}"><meta name="twitter:image" content="{og}">
<link rel="icon" href="{r}assets/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="{r}assets/favicon-32.png"><link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">{GSC}{GA}
<link rel="preload" href="{r}fonts/manrope-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/mq.css?v=15">
<script type="application/ld+json">{json.dumps(jld, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(faqld, ensure_ascii=False)}</script></head>
<body>{ICONS}
<header class="nav"><div class="wrap"><a class="logo" href="./" aria-label="A+ MQ"><picture><source media="(prefers-color-scheme: dark)" srcset="{r}assets/logo-horizontal-white.png"><img src="{r}assets/logo-horizontal.png" alt="A+ MQ" width="120" height="38"></picture></a><nav aria-label="Main">{nav}</nav><a class="lang" href="{t['other_href']}" hreflang="{'en' if ar else 'ar'}">{t['other_label']}</a><a class="btn" href="{demo}">{t['demo']}</a></div></header>
<main>
<div class="hero"><div class="wrap"><div><span class="kick"><i></i>{t['kick']}</span><h1>{t['h1']}</h1><p class="lede">{esc(t['lede'])}</p><div class="row"><a class="btn lg" href="{demo}">{t['demo']} {arrow}</a><a class="btn ghost lg" href="{mail}">{t['cta']}</a></div><ul class="trust">{trust}</ul></div>{ribbon(t['more'])}</div></div>
<section class="sec"><div class="wrap"><h2>{esc(t['out_h'])}</h2><p class="sub">{esc(t['out_s'])}</p><div class="outs">{out}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>{esc(t['ba_h'])}</h2><p class="sub">{esc(t['ba_s'])}</p><div class="card ba"><div class="br hd"><b></b><span class="bl">{t['ba_l']}</span><span class="bg">{t['ba_r']}</span></div>{ba}</div></div></section>
<section class="sec" id="tools"><div class="wrap"><h2>{esc(t['tools_h'])}</h2><p class="sub">{esc(t['tools_s'])}</p><div class="chips" role="group">{chips}</div><div class="tg">{tools}</div><div class="mid"><a class="btn lg" href="{demo}">{t['demo']} {arrow}</a></div></div></section>
<section class="sec alt"><div class="wrap"><h2>{esc(t['show_h'])}</h2><p class="sub">{esc(t['show_s'])}</p><div class="shows">{shows}</div><p class="cav">{esc(t['cav'])}</p></div></section>
<section class="sec" id="how"><div class="wrap"><h2>{esc(t['how_h'])}</h2><div class="how">{how}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>{esc(t['who_h'])}</h2><div class="who">{who}</div><div class="card by"><div class="av"><img src="{r}assets/icon-128.png" alt="" width="40" height="40"></div><div><h3>{esc(t['by_h'])}</h3><p>{esc(t['by_p'])} <a href="{t['portfolio']}">{t['by_a']}</a></p></div></div></div></section>
<section class="sec" id="licensing"><div class="wrap"><h2>{esc(t['lic_h'])}</h2><p class="sub">{esc(t['lic_s'])}</p><div class="lic">{lic}</div></div></section>
<section class="sec alt" id="faq"><div class="wrap"><h2>{t['faq_h']}</h2><div class="faq">{faq}</div></div></section>
<section class="sec" id="demo"><div class="wrap"><div class="cta dcta"><div class="dl"><h2>{esc(t['end_h'])}</h2><p>{esc(t['end_p'])}</p><h3>{esc(f['h'])}</h3><p class="dp">{esc(f['p'])}</p><p class="li2"><a href="{mail}">{t['cta']}</a> · <a href="https://linkedin.com/in/abo-elkhair" target="_blank" rel="noopener">{t['end_b2']}</a></p></div><div class="dr">{form}</div></div></div></section>
</main>
<footer><div class="wrap"><div class="fr"><strong style="color:var(--ink)">A+ MQ</strong><span><a href="{t['portfolio']}">{t['portlabel']}</a> · <a href="{t['other_href']}">{t['other_label']}</a></span></div><small>{esc(t['foot'])} {esc(t['foot_a'])}</small><small style="margin-top:8px">{esc(t['copy'])}</small></div></footer>
<div class="sticky"><a class="btn" href="{demo}">{t['demo']}</a><a class="btn ghost" href="{mail}">{t['cta']}</a></div>
{FILTER_JS}
</body></html>'''

def main():
    for k, path in (('en', 'aplus-mq/index.html'), ('ar', 'aplus-mq/ar/index.html')):
        p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(page(k))
    print('built aplus-mq EN + AR')

if __name__ == '__main__':
    main()
