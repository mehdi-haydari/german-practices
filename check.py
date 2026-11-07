from pathlib import Path
from html.parser import HTMLParser
import json
import os
from urllib.parse import urlsplit,unquote
from html import unescape
ROOT=Path(__file__).resolve().parent;DIST=ROOT/'dist';data=json.loads((ROOT/'practices.json').read_text());BASE_PATH=os.environ.get('SITE_BASE_PATH','').rstrip('/')
assert len(data)==11
assert len({p['id'] for p in data})==len(data)
assert sum(p['original'] is not None for p in data)==10
assert sum(len(p['attempts']) for p in data)==7
class Page(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.lang=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')=='en'
        if 'id' in a: assert a['id'] not in self.ids,a['id'];self.ids.add(a['id'])
        for key in ['href','src']:
            if a.get(key):self.links.append(a[key])
for file in DIST.rglob('*.html'):
    html=file.read_text();page=Page();page.feed(html);assert page.lang,file
    for link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        local_path=unquote(u.path)
        if BASE_PATH and local_path.startswith(BASE_PATH):local_path=local_path[len(BASE_PATH):] or '/'
        target=DIST/local_path.lstrip('/') if local_path else file
        if u.path.endswith('/') or target.is_dir():target=target/'index.html'
        assert target.exists(),(file,link)
        if u.fragment:
            q=Page();q.feed(target.read_text());assert u.fragment in q.ids,(target,u.fragment)
index=(DIST/'index.html').read_text();assert f'{BASE_PATH}/lesson/9/' in index and 'Lessons we’ve practised' in index
lesson=(DIST/'lesson/9/index.html').read_text();assert f'{BASE_PATH}/practice/lesson-09-c2a/' in lesson and f'{BASE_PATH}/practice/lesson-09-opening/' in lesson
c2=DIST/'practice/lesson-09-c2a/index.html';html=unescape(c2.read_text())
assert 'Fragen A' in html and 'Fragen B' in html
for p in data:
    if p['group'] in ('A','B'):
        assert p['question'] in html
        if p['original'] is not None:assert p['original'] in html
        assert p['corrected'] in html
        for a in p['attempts']:assert a['answer'] in html
        legacy=(DIST/'practice'/p['id']/'index.html').read_text();assert f'#{p["ref"].split(" · ")[-1].lower().replace(".","-")}' in legacy
assert (DIST/'.nojekyll').exists()
print('Verified lesson → practice navigation, all 10 C2.a questions, original answers, corrections, follow-ups, and legacy question links.')
