from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1]
for route in ['apps/pdf-reader','guides/pdf-reader']:
    soup=BeautifulSoup((root/route/'index.html').read_text(encoding='utf-8'),'html.parser')
    assert len(soup.select('h1'))==1
    assert soup.select_one('meta[name=description]')['content']
    assert soup.select_one('link[rel=canonical]')['href']==f'https://yooniquelabs.kr/{route}/'
    for node in soup.select('[href],[src]'):
        url=urlsplit(node.get('href',node.get('src')))
        if url.scheme or url.netloc:continue
        target=root/url.path.lstrip('/') if url.path else root/route/'index.html'
        if target.is_dir():target=target/'index.html'
        assert target.exists(),str(target)
        if url.fragment:assert BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser').find(id=url.fragment)
for file,link in [('index.html','/apps/pdf-reader/'),('guides/index.html','/guides/pdf-reader/')]:
    assert link in (root/file).read_text(encoding='utf-8')
assert 'apps/pdf-reader/' in (root/'sitemap.xml').read_text(encoding='utf-8')
print('PASS PDF download and guide metadata, links, fragments and discovery')
