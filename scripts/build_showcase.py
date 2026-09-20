"""Build the static storefront; run from any working directory."""
from pathlib import Path
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
apps = json.loads((ROOT / 'data/apps.json').read_text(encoding='utf-8-sig'))
guides = json.loads((ROOT / 'data/guides.json').read_text(encoding='utf-8-sig'))
blogs = json.loads((ROOT / 'data/blog-posts.json').read_text(encoding='utf-8-sig'))
E = html.escape
groups = {'kokplus':'운동','kkalkkeum':'생활','foldnote':'기록','chosung5':'게임','yeogi-parking':'생활','clawking3d':'게임','rider-net':'기록','juyuhalkka':'생활','gyodae-hannun':'기록'}
blurbs = {'kokplus':'코트에서는 경기에만 집중하세요.','kkalkkeum':'함께 쓴 돈, 기분 좋게 나누세요.','foldnote':'펼친 화면에, 오늘을 기록하세요.','chosung5':'오늘의 다섯 문제, 머리를 깨우는 시간.','yeogi-parking':'차를 세운 곳, 말 한마디로 기록.','clawking3d':'손끝으로 조준하고, 인형을 모으세요.','rider-net':'매출 너머, 내 손에 남는 수익.','juyuhalkka':'조금 더 가서 넣으면 정말 이득일까요?','gyodae-hannun':'반복되는 근무표를 한눈에.'}
symbols = {'kokplus':'↗','kkalkkeum':'÷','foldnote':'▤','chosung5':'ㄱㄴ','yeogi-parking':'P','clawking3d':'✳','rider-net':'₩','juyuhalkka':'+','gyodae-hannun':'31'}
def play(a): return 'https://play.google.com/store/apps/details?id='+a['package']+'&hl=ko&gl=KR'
def shot(slug):
    for ext in ('png','jpg'):
        if (ROOT/f'assets/guides/{slug}.{ext}').exists(): return f'/assets/guides/{slug}.{ext}'
    return None
def picture(a, eager=False):
    src=shot(a['slug'])
    return f'<img src="{src}" alt="{E(a["name"])} 실제 앱 화면" loading="{"eager" if eager else "lazy"}" decoding="async">' if src else ''
nav='''<header><nav class="wrap nav" aria-label="주 메뉴"><a class="logo" href="/" aria-label="유니크랩스 홈"><span class="mark">y.</span>Yoonique<span class="logo-light">Labs</span></a><ul><li><a class="link" href="/#apps">앱 둘러보기</a></li><li><a class="link" href="/guides/">사용 가이드</a></li><li><a class="link" href="/#stories">블로그</a></li><li><a class="link" href="/#about">스튜디오</a></li></ul><a class="nav-contact" href="mailto:hello@yooniquelabs.kr">문의하기 <span aria-hidden="true">↗</span></a></nav></header>'''
home=(ROOT/'index.html').read_text(encoding='utf-8')
head=home[:home.index('<body')]
head=re.sub(r'<title>.*?</title>','<title>유니크랩스 | 일상을 편하게, 쉬는 시간을 즐겁게</title>',head)
head=re.sub(r'<meta property="og:title"[^>]*>', '<meta property="og:title" content="유니크랩스 | 일상을 편하게, 쉬는 시간을 즐겁게">',head)
head=re.sub(r'<meta property="og:description"[^>]*>', '<meta property="og:description" content="생활·기록·운동·게임. 유니크랩스의 9가지 Android 앱을 실제 화면과 함께 만나보세요.">',head)
head=re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="유니크랩스의 9가지 Android 앱을 만나보세요. 콕플러스, 교대한눈, 여기주차, 깔끔정산, 폴드8노트와 인형뽑기 게임 뽑기왕 3D의 실제 화면과 사용법, 설치 링크를 안내합니다.">',head)
if '/assets/showcase.css' not in head: head=head.replace('</head>','<link rel="stylesheet" href="/assets/showcase.css"><script src="/assets/showcase.js" defer></script>\n</head>')
footer=home[home.index('<footer>'):home.index('</footer>')+9]
cards=[]
for a in apps:
    slug=a['slug']; group=groups[slug]
    cards.append(f'''<article class="app-card tone-{slug}" data-category="{group}" data-search="{E(a['name']+' '+a['tag']+' '+a['summary'])}">
<div class="app-card-top"><span class="app-symbol" aria-hidden="true">{symbols[slug]}</span><span class="app-category">{E(a['tag'])}</span></div>
<h3><a href="/apps/{slug}/">{E(a['name'])}</a></h3><p class="app-promise">{blurbs[slug]}</p><p class="app-description">{E(a['summary'])}</p>
<div class="app-card-links"><a href="/apps/{slug}/" aria-label="{E(a['name'])} 자세히 보기">자세히 보기 <span aria-hidden="true">↗</span></a><a href="{E(play(a))}" aria-label="Google Play에서 {E(a['name'])} 설치">Google Play <span aria-hidden="true">↗</span></a></div></article>''')
guidecards=[]
for i,g in enumerate(guides):
    a=next(a for a in apps if a['slug']==g['app'])
    guidecards.append(f'<a class="guide-tile" href="/guides/{g["slug"]}/"><span class="guide-number">0{i+1}</span><div><span class="eyebrow">{E(a["name"])}</span><h3>{E(g["title"])}</h3></div><span aria-hidden="true">↗</span></a>')
bloglinks=''.join(f'<a href="{E(b["url"])}"><span>{E(b["app"])}</span><strong>{E(b["title"])}</strong><span aria-hidden="true">↗</span></a>' for b in blogs)
by={a['slug']:a for a in apps}
body=f'''<body class="showcase"><a class="skip-link" href="#main">본문 바로가기</a>{nav}
<main id="main">
<section class="showcase-hero"><div class="wrap hero-layout"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> SMALL APPS. EVERYDAY DIFFERENCE.</p><h1>일상을 편하게,<br>쉬는 시간을<br><span class="hero-highlight">즐겁게.</span></h1><p class="hero-description">주차한 곳을 기억하고, 함께 쓴 돈을 나누고,<br class="desktop-break"> 잠깐의 틈에는 인형뽑기 한 판.<br>당신의 하루에 쓸모 있는 앱을 만듭니다.</p><div class="hero-actions"><a class="btn btn-primary" href="#apps">나에게 맞는 앱 찾기 <span aria-hidden="true">↗</span></a><a class="quiet-link" href="#featured-game">게임 먼저 구경하기 <span aria-hidden="true">→</span></a></div><p class="hero-footnote">9개의 앱과 게임 <span>·</span> Google Play에서 만나보세요</p></div>
<div class="hero-stage"><div class="stage-label">MADE FOR YOUR EVERYDAY <span>✳</span></div><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><figure class="hero-phone phone-back">{picture(by['yeogi-parking'],True)}<figcaption>여기주차 <span>주차 기록</span></figcaption></figure><figure class="hero-phone phone-front">{picture(by['clawking3d'],True)}<figcaption>뽑기왕 3D <span>잠깐의 즐거움</span></figcaption></figure><span class="stage-sticker">작은 앱,<br>쓸모 있는 변화.</span><p class="stage-caption">Google Play에 공개된 실제 앱 화면</p></div></div></section>
<div class="category-strip"><div class="wrap"><span>EVERYDAY, A LITTLE BETTER.</span><p>생활을 가볍게 <b>↗</b> 기록을 차곡차곡 <b>↗</b> 함께하는 운동 <b>↗</b> 손안의 즐거움</p></div></div>
<section id="apps" class="apps-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">OUR APPS / 01</p><h2>지금 필요한 앱을 찾아보세요.</h2></div><p>복잡한 하루에, 간단한 도구 하나.<br>용도에 맞게 골라 시작하세요.</p></div>
<div class="directory-controls" hidden><div class="filter-buttons" role="group" aria-label="앱 카테고리">{''.join(f'<button type="button" data-filter="{g}" aria-pressed="{str(g=="전체").lower()}">{g}</button>' for g in ('전체','생활','기록','운동','게임'))}</div><label class="app-search"><span aria-hidden="true">⌕</span><input id="app-search" type="search" placeholder="앱 이름이나 기능 검색" aria-label="앱 이름이나 기능 검색"></label></div><p class="result-count" aria-live="polite" aria-atomic="true" hidden>전체 9개의 앱</p>
<div class="app-grid">{''.join(cards)}</div><div class="empty-results" hidden><h3>찾으시는 앱이 없어요.</h3><p>다른 검색어를 입력하거나 전체 앱을 확인해 보세요.</p><button class="btn btn-primary" type="button" id="reset-apps">전체 앱 보기</button></div></div></section>
<section id="featured-game" class="game-section"><div class="wrap game-layout"><div class="game-copy"><p class="eyebrow">PLAY A LITTLE / 02</p><h2>이번에는<br>잡을 수 있을 것 같은데?</h2><p class="game-name">뽑기왕 3D</p><p>집게를 움직이고, 흔들림을 읽고, 한 번 더 도전.<br>손끝으로 즐기는 작은 크레인 게임장을 만나보세요.</p><ul class="game-features"><li>물리 시뮬레이션</li><li>스윙샷 연습</li><li>인형 도감 수집</li></ul><div class="cta"><a class="btn btn-lime" href="{E(play(by['clawking3d']))}">Google Play에서 만나보기 ↗</a><a class="game-detail-link" href="/apps/clawking3d/">게임 소개 →</a></div><small>광고 포함 · 모바일 인형뽑기 게임</small></div><figure class="game-visual"><span class="game-star" aria-hidden="true">✳</span>{picture(by['clawking3d'])}<figcaption>뽑기왕 3D 실제 게임 화면</figcaption></figure></div></section>
<section id="guides"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">HOW TO / 03</p><h2>처음부터, 어렵지 않게.</h2></div><a class="quiet-link" href="/guides/">사용 가이드 전체 보기 ↗</a></div><div class="guide-grid">{''.join(guidecards)}</div></div></section>
<section id="stories" class="stories-section"><div class="wrap stories-layout"><div><p class="eyebrow">FROM THE STUDIO / 04</p><h2>이럴 때<br>이 앱을 써보세요.</h2><p>일상에서 마주치는 작은 고민과<br>앱을 활용하는 방법을 나눕니다.</p><a class="quiet-link" href="https://blog.naver.com/PostList.naver?blogId=cupidjjang&amp;categoryNo=10">네이버 블로그 ↗</a></div><div class="story-list">{bloglinks}</div></div></section>
<section id="about"><div class="wrap about-layout"><div class="about-mark" aria-hidden="true">y<span>.</span></div><div><p class="eyebrow">YOONIQUE LABS · BUSAN, KOREA</p><h2>작은 불편에서 시작합니다.</h2><p>유니크랩스는 부산에서 모바일 앱을 만드는 개발 스튜디오입니다. 동호회 운영부터 생활 기록, 짧게 즐기는 게임까지. 직접 기획하고 개발하며, 사용자의 이야기를 듣고 개선합니다.</p><a class="quiet-link" href="mailto:hello@yooniquelabs.kr">앱에 대한 의견 보내기 ↗</a></div></div></section>
<section id="contact" class="contact-section"><div class="wrap"><p class="eyebrow">LET’S MAKE THINGS BETTER</p><h2>당신의 이야기를 들려주세요.</h2><p>앱 이용 문의, 개선 의견, 제휴 제안을 기다립니다.</p><a class="contact-email" href="mailto:hello@yooniquelabs.kr">hello@yooniquelabs.kr <span aria-hidden="true">↗</span></a></div></section>
</main>{footer}</body></html>'''
(ROOT/'index.html').write_text(head+body,encoding='utf-8')
for a in apps:
    p=ROOT/f'apps/{a["slug"]}/index.html'
    text=p.read_text(encoding='utf-8')
    if '/assets/showcase.css' not in text: text=text.replace('</head>','<link rel="stylesheet" href="/assets/showcase.css"></head>')
    text=text.replace('<body>','<body class="app-detail">')
    text=re.sub(r'<header>.*?</header>',nav,text,flags=re.S)
    if 'feature-grid' not in text:
        text=re.sub(r'(<h2>[^<]+로 할 수 있는 일</h2>)(.*?)(</div></section>)',lambda m:m[1]+'<div class="feature-grid">'+re.sub(r'<h3>(.*?)</h3><p>(.*?)</p>',r'<article><h3>\1</h3><p>\2</p></article>',m[2],flags=re.S)+'</div>'+m[3],text,count=1,flags=re.S)
    text=re.sub(r'<figure class="detail-screenshot">.*?</figure>','',text,flags=re.S)
    if shot(a['slug']):
        fig=f'<figure class="detail-screenshot">{picture(a,True)}<figcaption>Google Play 공개 스크린샷 · 앱 버전에 따라 화면은 달라질 수 있습니다.</figcaption></figure>'
        text=text.replace('</div></div>\n<section>',fig+'</div></div>\n<section>',1)
    text=re.sub(r'<div class="detail-blog">.*?</div>','',text,flags=re.S)
    blog=next((b for b in blogs if b['app']==a['name']),None)
    if blog: text=text.replace('</main>',f'<div class="detail-blog wrap detail"><p class="eyebrow">개발사 블로그</p><a href="{blog["url"]}">{E(blog["title"])} ↗</a></div></main>')
    p.write_text(text,encoding='utf-8')
for p in (ROOT/'guides').rglob('index.html'):
    text=p.read_text(encoding='utf-8')
    if '/assets/showcase.css' not in text: text=text.replace('</head>','<link rel="stylesheet" href="/assets/showcase.css"></head>')
    text=re.sub(r'<header>.*?</header>',nav,text,flags=re.S)
    p.write_text(text,encoding='utf-8')
print('Built homepage and enhanced 9 app pages.')
