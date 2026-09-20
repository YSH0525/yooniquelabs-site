"""Check crawlable pages, local links, metadata, and release invariants."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
from bs4 import BeautifulSoup

root=Path(__file__).resolve().parents[1]
pages=[root/'index.html', *sorted((root/'apps').rglob('index.html')), *sorted((root/'guides').rglob('index.html'))]
titles=set()
for path in pages:
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    assert len(soup.select('h1'))==1, f'H1: {path}'
    title=soup.title.get_text()
    assert title not in titles, f'Duplicate title: {path}'
    titles.add(title)
    assert soup.select_one('meta[name=description]')['content'], path
    canonical=soup.select_one('link[rel=canonical]')['href']
    rel=path.relative_to(root).as_posix().removesuffix('index.html')
    assert canonical=='https://yooniquelabs.kr/'+rel, (path,canonical)
    for schema in soup.select('script[type="application/ld+json"]'): json.loads(schema.string)
    for element in soup.select('[href], [src]'):
        value=element.get('href',element.get('src'))
        url=urlparse(value)
        if url.scheme or url.netloc: continue
        target=root/unquote(url.path.lstrip('/')) if url.path.startswith('/') else path.parent/unquote(url.path)
        if not url.path: target=path
        if target.is_dir(): target=target/'index.html'
        assert target.exists(), f'Broken link: {path}: {value}'
        if url.fragment:
            target_soup=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            assert target_soup.find(id=url.fragment), f'Broken fragment: {path}: {value}'
home=BeautifulSoup((root/'index.html').read_text(encoding='utf-8'),'html.parser')
assert len(home.select('.app-card'))==9
assert not home.select('.app-card[hidden]'), 'No-JS app discovery must remain visible'
assert len(home.select('.story-list a'))==6
assert len(home.select('.guide-tile'))==6
assert home.select_one('meta[name="naver-site-verification"]')
assert (root/'CNAME').read_text().strip()=='yooniquelabs.kr'
assert (root/'app-ads.txt').exists()
print(f'PASS: {len(pages)} pages; titles, H1, canonical, JSON-LD, local links, fragments, 9 apps, 6 guides and 6 blog links.')
