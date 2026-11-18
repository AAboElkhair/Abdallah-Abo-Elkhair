import re,os,json,sys
from urllib.parse import urlparse,unquote
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
files=[os.path.join(dp,f) for dp,_,fs in os.walk(R) for f in fs if f.endswith('.html') and '.git' not in dp and '_build' not in dp]
bad=0
for f in files:
    s=open(f,encoding='utf-8').read(); d=os.path.dirname(f)
    for m in re.finditer(r'(?:href|src)="([^"#]*)(#[^"]*)?"',s):
        u=m.group(1)
        if not u or re.match(r'(https?:|mailto:|tel:|data:|javascript:)',u):
            if u.startswith('https://aaboelkhair.github.io/Abdallah-Abo-Elkhair/'):
                t=os.path.join(R,u.split('Abdallah-Abo-Elkhair/',1)[1])
            else: continue
        else: t=os.path.normpath(os.path.join(d,unquote(u.split('?')[0])))
        if os.path.isdir(t): t=os.path.join(t,'index.html')
        if not os.path.exists(t): print('MISSING',os.path.relpath(f,R),u);bad+=1
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: json.loads(j)
        except Exception as e: print('BADJSON',f,e);bad+=1
    if 'aplus-mq' in f or f.endswith(('/index.html')) and f.count('/')<=len(R.split('/'))+1:
        for k in ('G-0K38B1126B','google-site-verification'):
            if k not in s: print('NO',k,os.path.relpath(f,R));bad+=1
for a,b in (('aplus-mq/index.html','aplus-mq/ar/index.html'),):
    for f in (a,b):
        s=open(os.path.join(R,f),encoding='utf-8').read()
        print(f,'hreflang',sorted(re.findall(r'hreflang="([^"]+)" href',s)))
print('files',len(files),'problems',bad)
