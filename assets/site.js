(function(){
var rt=document.documentElement,tg=document.getElementById('tg');
if(tg)tg.onclick=function(){var n=rt.dataset.theme==='dark'?'light':'dark';rt.dataset.theme=n;try{localStorage.setItem('theme',n)}catch(e){}};
var pb=document.getElementById('prog');
addEventListener('scroll',function(){var h=document.documentElement;pb.style.transform='scaleX('+(h.scrollTop/((h.scrollHeight-h.clientHeight)||1))+')'},{passive:true});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
var ARTICLES=[
{title:"How Visual Learning Transforms My Work in Medical Equipment Planning",url:"https://www.linkedin.com/pulse/how-visual-learning-transforms-my-work-medical-abdallah-abo-elkhair-zvcnf/"},
{title:"Navigating Healthcare Project Delivery Phases",url:"https://www.linkedin.com/pulse/navigating-healthcare-project-delivery-phases-from-abo-elkhair-dbiuf/"},
{title:"Transforming Medical Equipment Planning with BIM",url:"https://www.linkedin.com/pulse/transforming-medical-equipment-planning-bim-abdallah-abo-elkhair-gz9cf/"},
{title:"Featured LinkedIn post",date:"May 2024",url:"https://www.linkedin.com/feed/update/urn:li:activity:7196852681393467392/",label:"View post on LinkedIn"}
]; /* {title,date,summary,url,label,body:["paragraph",...]} */
var L=document.getElementById('artList');
if(L){var n=+L.dataset.limit||ARTICLES.length;ARTICLES.slice(0,n).forEach(function(a){var c=document.createElement('article');c.className='card';
var h=document.createElement('h3');h.textContent=a.title;c.append(h);
var t=[a.date,a.summary].filter(Boolean).join(' · ');if(t){var m=document.createElement('p');m.textContent=t;c.append(m)}
if(a.body){var d=document.createElement('details'),s=document.createElement('summary');s.textContent='Read article';d.append(s);a.body.forEach(function(x){var p=document.createElement('p');p.textContent=x;d.append(p)});c.append(d)}
if(a.url){var k=document.createElement('a');k.className='btn dk';k.href=a.url;k.target='_blank';k.rel='noopener';k.style.marginTop='16px';k.textContent=(a.label||'Read on LinkedIn')+' \u2192';c.append(k)}
L.append(c)})}
var T=document.getElementById('toast'),seen=false;
try{seen=sessionStorage.getItem('t')==='1'}catch(e){}
if(T&&!seen)setTimeout(function(){T.classList.add('on')},4000);
function closeT(){T.classList.remove('on');try{sessionStorage.setItem('t','1')}catch(e){}}
var tx=document.getElementById('tx'),tc=document.getElementById('tc');if(tx)tx.onclick=closeT;if(tc)tc.onclick=closeT;
})();