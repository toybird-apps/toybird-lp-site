from pathlib import Path
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from urllib.parse import urlparse,unquote
import json,re,hashlib,shutil,argparse,xml.etree.ElementTree as ET
from PIL import Image
BASE='https://lp.toybird.com'
GROUPS=['Prompt Ready','AI赤シート','Pocket Screen','Pointer Cue']
ASSETS='blog/editorial-assets/blog108'
SLUGS={'Prompt Ready':'prompt-ready','AI赤シート':'ai-memorize-sheet','Pocket Screen':'pocket-screen','Pointer Cue':'pointer-cue'}
MD=MarkdownIt('commonmark',{'html':False,'breaks':True}).enable('table')
def esc(x):
 import html
 return html.escape(str(x),quote=True)
def fragment(s):return BeautifulSoup(s,'html.parser')
def text(el):return el.get_text(' ',strip=True) if el else ''
def put(parent,html):
 for n in list(fragment(html).contents):parent.append(n)
def file_from_url(u):
 p=unquote(urlparse(u).path).lstrip('/')
 return p+'index.html' if p.endswith('/') else p

def normalize_tables(md):
 out=[];fence=False;new=True
 for line in md.splitlines():
  if line.startswith('```'):fence=not fence
  row=not fence and line.lstrip().startswith('|') and line.rstrip().endswith('|')
  out.append(line)
  if row and new:out.append('|'+'|'.join('---' for _ in line.strip().strip('|').split('|'))+'|')
  new=not row
 return '\n'.join(out)

def load_drafts(root):
 result={}
 for f in sorted((root/'.editorial-108').glob('*.txt')):
  lang='ja' if f.stem.startswith('ja-') else f.stem
  for slug,body in re.findall(r'^@@ ([^\n]+)\n(.*?)(?=^@@ |\Z)',f.read_text(),re.M|re.S):
   path=('' if lang=='ja' else lang+'/')+'blog/'+slug.strip()+'/index.html'
   if path in result:raise ValueError('Duplicate '+path)
   body=body.strip()
   if lang=='zh-tw':
    for a,b in [('其他服务','其他服務'),('假設讲義','假設講義'),('判断依據','判斷依據'),('让介面','讓介面')]:body=body.replace(a,b)
   title=re.match(r'^# (.+)\n',body).group(1)
   result[path]={'title':title,'md':body.split('\n',1)[1].strip(),'lang':lang}
 return result

def derive_registry(root):
 urls=[x.text for x in BeautifulSoup((root/'sitemap.xml').read_text(),'xml').find_all('loc') if '/blog/' in x.text]
 assert len(urls)==108
 rows=[]
 for url in urls:
  p=file_from_url(url);parts=p.split('/');lang='ja' if parts[0]=='blog' else parts[0]
  typ='index' if len(parts)==(2 if lang=='ja' else 3) else 'article';slug=parts[-2]
  group='一覧' if typ=='index' else ('Prompt Ready' if slug.startswith('chatgpt-') else 'Pocket Screen' if slug.startswith('mac-') else 'Pointer Cue' if slug.startswith('screen') else 'AI赤シート')
  s=BeautifulSoup((root/p).read_text(),'html.parser');about={}
  for script in s.select('script[type="application/ld+json"]'):
   j=json.loads(script.string or script.text)
   for x in j.get('@graph',[j]):
    if x.get('@type') in ('Article','BlogPosting'):about=x.get('about',{})
  rows.append({'path':p,'url':url,'language':lang,'page_type':typ,'group':group,'product':about.get('name',group),'cta':about.get('url',BASE+'/'),'related':[]})
 langs=['ja','en','de','fr','es','it','pt-br','ko','zh-cn','zh-tw']
 rows.sort(key=lambda r:(langs.index(r['language']),r['page_type']=='index',r['path']))
 for n,r in enumerate(rows,1):
  r['id']=f'B{n:03}'
  peers=[x for x in rows if x['language']==r['language'] and x['group']==r['group'] and x['url']!=r['url'] and x['page_type']=='article']
  peers.sort(key=lambda x:(0 if x['path'].endswith('chatgpt-prompt-work-tips/index.html') else 1,x['path']))
  old=BeautifulSoup((root/r['path']).read_text(),'html.parser')
  selected=[a['href'] for a in old.select('#related a[href]') if a['href'] in [x['url'] for x in peers]]
  selected += [x['url'] for x in peers if x['url'] not in selected]
  r['related']=selected[:3]
 counts={g:sum(r['group']==g for r in rows) for g in GROUPS}
 assert counts=={'Prompt Ready':39,'AI赤シート':36,'Pocket Screen':12,'Pointer Cue':11},counts
 return rows

def selected_media(md):
 # New media in this release: verified supplied home crop. Version-specific clips are held.
 md=re.sub(r'(\{\{MEDIA:[^}]+\}\})',r'\n\n\1\n\n',md)
 blocks=[b for b in md.split('\n\n') if b.strip()]
 for i,b in enumerate(blocks):
  key=re.fullmatch(r'\{\{MEDIA:([^}]+)\}\}',b.strip())
  if not key or key.group(1) in ['PR-EN-HOME','PS-CURRENT','AS-LEARN','AS-LIB','AS-QUIZ','AS-METHOD']:continue
  blocks[i]=''
  if i+1>=len(blocks):continue
  t=blocks[i+1]
  if key.group(1)=='PC-RANGE':
   if t.startswith(('この静止画','提供された製品デモ')):blocks[i+1]=''
   continue
  if key.group(1).startswith('PR-'):
   t=t.replace('The screenshot shows where to prepare a request; it does not show this CSV case being executed.','')
   starts=("Der Screenshot","Die Abbildung zeigt","L’image","L'image montre","L'illustration montre","La imagen muestra","L'immagine mostra","La schermata mostra","A imagem mostra","이미지는","화면은 영어")
   if t.startswith(starts):
    m=re.match(r'^.*?[.。]\s*',t,re.S)
    if m:t=t[m.end():]
   blocks[i+1]=t
 return '\n\n'.join(b for b in blocks if b.strip())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--config',required=True);ap.add_argument('--date',required=True);args=ap.parse_args()
 root=Path(args.root).resolve();cfg=Path(args.config).resolve();date=args.date
 registry=derive_registry(root);ui=json.loads((cfg/'i18n.json').read_text())
 scope={r['path']:r for r in registry};byurl={r['url']:r for r in registry};drafts=load_drafts(root)
 assert len(drafts)==90 and all(p in scope for p in drafts)
 meta={};orig={};published={}
 hashes={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file() and '.git' not in f.parts}
 for p,r in scope.items():
  s=BeautifulSoup((root/p).read_text(),'html.parser');orig[p]=s;t=text(s.h1);lead=text(s.select_one('.article-deck'))
  if p in drafts:t=drafts[p]['title'];lead=text(fragment(MD.render(normalize_tables(drafts[p]['md']))).find('p'))
  meta[r['url']]={'title':t,'description':lead}
  el=s.find('meta',property='article:published_time');published[p]=el.get('content','') if el else ''
 ad=root/ASSETS;ad.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(cfg/'media/pr-en-home.webp',ad/'pr-en-home.webp')
 media={'PR-EN-HOME':('pr-en-home.webp','en','Prompt Ready'),'PR-JA-HOME':('pr-en-home.webp','en','Prompt Ready'),'AS-LEARN':('/ai-memorize-sheet/assets/learning-screen.webp','ja','AI Study Sheet'),'AS-LIB':('/ai-memorize-sheet/assets/library.webp','ja','AI Study Sheet'),'AS-QUIZ':('/ai-memorize-sheet/assets/quiz-screen.webp','ja','AI Study Sheet'),'AS-METHOD':('/ai-memorize-sheet/assets/quiz-methods.webp','ja','AI Study Sheet'),'PS-CURRENT':('/pocket-screen/assets/word-pdf-real-screen.png',None,'Pocket Screen')}
 def fig(key,r):
  name,lang,product=media[key];u=ui[r['language']];path=name.lstrip('/') if name.startswith('/') else ASSETS+'/'+name
  im=Image.open(root/path);w,h=im.size
  tag=' · '+u['english'] if lang=='en' else ' · '+u['japanese'] if lang=='ja' else ''
  caption=product+tag+' — '+u['provided']
  return f'<figure class="b108-figure"><a href="/{path}" target="_blank" rel="noopener" aria-label="{esc(u["expand"])}"><img src="/{path}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{esc(product+tag)}"></a><figcaption>{esc(caption)} <a href="/{path}" target="_blank" rel="noopener">{esc(u["expand"])}</a></figcaption></figure>'
 def related(r):
  u=ui[r['language']];links=[x for x in r['related'] if x in meta and byurl[x]['language']==r['language'] and x!=r['url']]
  if r['path'].endswith('chatgpt-prompt-work-tips/index.html'):links=[x['url'] for x in registry if x['language']==r['language'] and x['group']=='Prompt Ready' and x['url']!=r['url']]
  links=list(dict.fromkeys(links))
  if not links:return ''
  cards=''.join(f'<a class="b108-card" href="{esc(x)}"><strong>{esc(meta[x]["title"])}</strong><span>{esc(meta[x]["description"])}</span></a>' for x in links)
  return f'<section class="b108-related"><h2>{esc(u["next"])}</h2><div class="b108-cards">{cards}</div></section>'
 def quiz(r):
  u=ui[r['language']];items=''.join(f'<div class="b108-question"><p><b>Q{i}.</b> {esc(q)}</p><details><summary>{esc(u["answer"])}</summary><p>{esc(a)}</p></details></div>' for i,(q,a) in enumerate(u['water'],1))
  return f'<div class="b108-exercise"><p class="b108-label">{esc(u["exercise"])}</p><p>{esc(u["sample"])}</p>{items}</div>'
 def demo(r):
  u=ui[r['language']];inputs=''.join(f'<label class="b108-toggle"><span>{esc(u[k])}</span><input type="checkbox" checked data-name="{esc(u[k])}"></label>' for k in ['immediate','weekly'])
  return f'<div class="b108-demo" data-on="{esc(u["on"])}" data-off="{esc(u["off"])}"><p class="b108-label">{esc(u["exercise"])}</p><p>{esc(u["sample"])}</p>{inputs}<button type="button" class="b108-reset">{esc(u["reset"])}</button><output aria-live="polite"></output></div>'
 def mset(s,attr,key,val):
  if not val:return
  e=s.find('meta',attrs={attr:key})
  if e is None:e=s.new_tag('meta',attrs={attr:key});s.head.append(e)
  e['content']=val
 def setup(s,r):
  u=ui[r['language']];s.body['class']=list(dict.fromkeys(s.body.get('class',[])+['blog108']))
  for e in s.select('script[src]'):
   if e['src'].split('?')[0].endswith('/editorial.js'):e.decompose()
  for e in s.select('link[rel=stylesheet]'):
   if e.get('href','').split('?')[0].endswith('/editorial.css'):e.decompose()
  s.head.append(s.new_tag('link',attrs={'rel':'stylesheet','href':'/'+ASSETS+'/blog108.css'}));s.body.append(s.new_tag('script',attrs={'src':'/'+ASSETS+'/blog108.js','defer':''}))
  s.body['data-language']=r['language'];s.body['data-group']=r['group']
  for k in ['copy','copied','failed']:s.body['data-'+k]=u[k]
  for e in s.select('.skip-link'):e.string=u['toc']
 for p,r in scope.items():
  if r['page_type']!='article':continue
  s=orig[p];a=s.select_one('article.article-content');assert a is not None,p
  u=ui[r['language']];m=meta[r['url']];t=m['title'];lead=m['description'];setup(s,r)
  if p in drafts:
   body=MD.render(normalize_tables(selected_media(drafts[p]['md'])))
   body=re.sub(r'<p>\{\{MEDIA:([^}]+)\}\}</p>',lambda m:fig(m.group(1),r),body)
   body=body.replace('<p>{{QUIZ:WATER-3}}</p>',quiz(r)).replace('<p>{{DEMO:NOTIFICATIONS}}</p>',demo(r)).replace('<p>{{RELATED-INLINE}}</p>',related(r))
   a.clear();put(a,body)
  else:
   for e in a.select('.article-toc,.table-scroll-hint'):e.decompose()
   if p.endswith('chatgpt-prompt-work-tips/index.html'):
    h=[h for h in a.find_all('h2') if 'Prompt Ready' in text(h)];put(h[-1].parent if h else a,fig('PR-JA-HOME',r))
  if p.endswith('/screen-sharing-show-where-to-look/index.html') and not a.select_one('.b108-demo'):
   table=a.find('table')
   if table:table.insert_after(fragment(demo(r)))
  if r['group']=='Pocket Screen' and 'mac-view-reference' in p and not a.select_one('.b108-figure'):
   a.find_all('h2')[2].insert_after(fragment(fig('PS-CURRENT',r)))
  if not a.select_one('.b108-related'):put(a,related(r))
  support='https://labs.toybird.com/apps/'+SLUGS[r['group']]+'/support.html';note=' · '+u['english'] if '/en/' in r['cta'] and r['language']!='en' else ''
  put(a,f'<aside class="b108-product"><p class="b108-label">{esc(r["product"] or r["group"])}</p><a class="b108-product-link" href="{esc(r["cta"])}" data-blog-product="{esc(r["group"])}">{esc(u["product"]+note)}</a><a href="{esc(support)}">{esc(u["official"])}</a></aside><p class="b108-byline">{esc(u["written"])}</p>')
  heads=a.find_all('h2');seen=set(x['id'] for x in s.select('[id]') if x not in heads);toc=[]
  for i,h in enumerate(heads,1):
   hid=h.get('id') or f'guide-{i}'
   while hid in seen:hid+='-content'
   h['id']=hid;seen.add(hid);toc.append((hid,text(h)))
  nav=s.new_tag('nav',attrs={'class':'b108-toc','aria-label':u['toc']});put(nav,f'<b>{esc(u["toc"])}</b><ol>'+''.join(f'<li><a href="#{esc(k)}">{esc(v)}</a></li>' for k,v in toc)+'</ol>')
  first=a.find('p',recursive=False)
  if first:first.insert_after(nav)
  else:a.insert(0,nav)
  for i,tbl in enumerate(a.find_all('table'),1):
   assert tbl.find('thead'),p
   for th in tbl.find_all('th'):th['scope']='col'
   tbl.wrap(s.new_tag('div',attrs={'class':'b108-table','role':'region','tabindex':'0','aria-label':u['exercise']+' '+str(i)}))
  for pre in a.find_all('pre'):pre['tabindex']='0'
  s.h1.string=t;s.title.string=t+' | Toybird Labs Blog'
  deck=s.select_one('.article-deck')
  if deck:deck.string=lead
  for attr,key,val in [('name','description',lead),('property','og:title',t),('property','og:description',lead),('name','twitter:title',t),('name','twitter:description',lead),('property','article:modified_time',date)]:mset(s,attr,key,val)
  hero=s.select_one('.hero-image')
  if hero:hero.decompose()
  bc=s.select('.breadcrumbs li')
  if bc:bc[-1].string=t
  times=s.select('.byline time')
  if times:
   times[0].string=u['published']+': '+times[0].get('datetime','')[:10]
   if len(times)>1:times[1]['datetime']=date;times[1].string=u['updated']+': '+date
  bl=s.select_one('.byline')
  if bl:
   for e in bl.find_all('span'):e.decompose()
   cjk=r['language'] in ('ja','ko','zh-cn','zh-tw');length=len(a.get_text()) if cjk else len(a.get_text(' ').split());estimate=max(2,round(length/(500 if cjk else 200)))
   put(bl,f'<span>{estimate} {esc(u["minutes"])}</span>')
  for ld in s.select('script[type="application/ld+json"]'):
   data=json.loads(ld.string or ld.text);graph=[x for x in data.get('@graph',[data]) if x.get('@type')!='FAQPage']
   for x in graph:
    if x.get('@type') in ('Article','BlogPosting'):x['headline']=t;x['description']=lead;x['dateModified']=date
    if x.get('@type')=='BreadcrumbList' and x.get('itemListElement'):x['itemListElement'][-1]['name']=t
   if '@graph' in data:data['@graph']=graph
   else:data=graph[0] if graph else {}
   ld.string=json.dumps(data,ensure_ascii=False,separators=(',',':'))
  (root/p).write_text(str(s)+'\n')
 for p,r in scope.items():
  if r['page_type']!='index':continue
  s=orig[p];u=ui[r['language']];setup(s,r);entries=[x for x in registry if x['page_type']=='article' and x['language']==r['language']]
  hero=s.select_one('.hub-hero');mainel=s.find('main');intro=hero.select_one('div p') if hero else None
  if intro:intro.string=u['intro']
  elif hero:put(hero,f'<p>{esc(u["intro"])}</p>')
  if hero:put(hero,f'<p class="b108-index-count">{len(entries)} {esc(u["count"])}</p>')
  for e in list(mainel.select('section.cluster')):e.decompose()
  nav=s.new_tag('nav',attrs={'class':'b108-purpose','aria-label':u['pick']});put(nav,f'<b>{esc(u["pick"])}</b>')
  for gi,g in enumerate(GROUPS):
   chosen=[x for x in entries if x['group']==g]
   if not chosen:continue
   gid='topic-'+SLUGS[g];put(nav,f'<a href="#{gid}">{esc(u["groups"][gi])}</a>')
   sec=f'<section class="cluster" id="{gid}"><div class="cluster-head"><div><p>{esc(chosen[0]["product"] or g)}</p><h2>{esc(u["groups"][gi])}</h2><p>{esc(u["groupdesc"][gi])}</p></div></div><div class="hub-grid">'
   chosen.sort(key=lambda x:(0 if x['path'].endswith('chatgpt-prompt-work-tips/index.html') else 1,x['id']))
   for x in chosen:
    mm=meta[x['url']];sec+=f'<a class="hub-card" href="{esc(x["url"])}"><span>{esc(u["groups"][gi])}</span><h3>{esc(mm["title"])}</h3><p>{esc(mm["description"])}</p></a>'
   put(mainel,sec+'</div></section>')
  if hero:hero.insert_after(nav)
  else:mainel.insert(0,nav)
  mset(s,'name','description',u['intro']);mset(s,'property','og:description',u['intro'])
  for ld in s.select('script[type="application/ld+json"]'):
   data=json.loads(ld.string or ld.text)
   for x in data.get('@graph',[data]):
    if x.get('@type')=='ItemList':x['itemListElement']=[{'@type':'ListItem','position':i,'url':a['url'],'name':meta[a['url']]['title']} for i,a in enumerate(entries,1)]
    if x.get('@type')=='Blog':x['description']=u['intro'];x['dateModified']=date
   ld.string=json.dumps(data,ensure_ascii=False,separators=(',',':'))
  (root/p).write_text(str(s)+'\n')
 sm=root/'sitemap.xml';tree=ET.parse(sm);ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'};count=0
 for row in tree.getroot():
  loc=row.find('s:loc',ns)
  if loc is not None and loc.text in byurl:
   lm=row.find('s:lastmod',ns)
   if lm is None:lm=ET.SubElement(row,'{'+ns['s']+'}lastmod')
   lm.text=date;count+=1
 assert count==108
 ET.register_namespace('',ns['s']);tree.write(sm,encoding='utf-8',xml_declaration=True)
 shutil.copyfile(cfg/'blog108.css',ad/'blog108.css');shutil.copyfile(cfg/'blog108.js',ad/'blog108.js')
 issues=[];pages=[]
 for p,r in scope.items():
  content=(root/p).read_text();s=BeautifulSoup(content,'html.parser');can=s.select('link[rel=canonical]')
  if '{{' in content:issues.append([p,'unresolved token'])
  if len(can)!=1 or can[0]['href']!=r['url']:issues.append([p,'canonical'])
  rob=s.find('meta',attrs={'name':'robots'})
  if rob and 'noindex' in rob['content']:issues.append([p,'noindex'])
  ids=[x['id'] for x in s.select('[id]')]
  if len(ids)!=len(set(ids)):issues.append([p,'duplicate id'])
  for e in s.select('[href],[src]'):
   v=e.get('href',e.get('src',''))
   if v.startswith('#') and v[1:] not in ids:issues.append([p,'anchor',v])
   elif v.startswith('/') or v.startswith(BASE+'/'):
    path=file_from_url(v)
    if path and not (root/path).exists():issues.append([p,'missing file',v])
  if r['page_type']=='article':
   cur=s.find('meta',property='article:published_time')
   if (cur.get('content','') if cur else '')!=published[p]:issues.append([p,'publication date'])
   if 'G-MTD9Z8S7QG' not in content or 'article_id:' not in content:issues.append([p,'analytics'])
  else:
   actual={a['href'] for a in s.select('a.hub-card')};expect={a['url'] for a in registry if a['page_type']=='article' and a['language']==r['language']}
   if actual!=expect:issues.append([p,'index membership'])
  pages.append({'id':r['id'],'path':p,'url':r['url'],'language':r['language'],'type':r['page_type'],'sha256':hashlib.sha256(content.encode()).hexdigest(),'figures':len(s.select('.b108-figure')),'tables':len(s.find_all('table'))})
 changed=[]
 for f in root.rglob('*'):
  if not f.is_file() or '.git' in f.parts:continue
  rel=str(f.relative_to(root));h=hashlib.sha256(f.read_bytes()).hexdigest()
  if h!=hashes.get(rel):
   changed.append(rel)
   if rel not in scope and rel!='sitemap.xml' and not rel.startswith(ASSETS+'/'):issues.append([rel,'outside scope'])
 if issues:raise RuntimeError(json.dumps(issues,ensure_ascii=False))
 report={'date':date,'scope_count':108,'article_count':98,'index_count':10,'new_manuscripts':90,'retained_japanese_cases':8,'product_lp_changed':False,'issues':issues,'changed_files':sorted(changed),'pages':pages}
 (cfg/'qa-static.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));(cfg/'registry-generated.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k not in ['pages','changed_files']},ensure_ascii=False));print('changed_files',len(changed))
if __name__=='__main__':main()
