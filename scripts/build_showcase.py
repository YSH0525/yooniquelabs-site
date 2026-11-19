"""Build the static storefront; run from any working directory.

Inputs : data/apps.json (app facts), data/store.json (grouping, chips, order),
         data/guides.json, data/blog-posts.json, assets/icons, assets/shots.
Outputs: index.html, apps/<slug>/index.html (created when missing, enhanced
         otherwise), shared navigation on guides and Windows pages, sitemap.xml.
"""
from pathlib import Path
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://yooniquelabs.kr'
load = lambda name: json.loads((ROOT / 'data' / name).read_text(encoding='utf-8-sig'))
apps, guides, blogs, store = load('apps.json'), load('guides.json'), load('blog-posts.json'), load('store.json')
E = html.escape
by = {a['slug']: a for a in apps}
meta = store['apps']
ordered = [by[s] for s in store['order']]
assert set(by) == set(meta) == set(store['order']), 'apps.json and store.json must list the same slugs'
N = len(apps)

TITLE = '유니크랩스 | 일상을 편하게, 쉬는 시간을 즐겁게'
DESC = (f'유니크랩스가 만든 Android 앱과 게임 {N}가지, Windows 프로그램 2가지를 만나보세요. 배드민턴 대진표 콕플러스, '
        '더치페이 깔끔정산, 파티게임 찔러봐 해적, 3D 인형뽑기, 에어 오목·장기의 실제 화면과 사용법, 설치 링크를 안내합니다.')
OG_DESC = f'생활·기록·운동·학습·게임. 유니크랩스의 Android 앱 {N}가지와 Windows 프로그램을 실제 화면과 함께 만나보세요.'
FONT = '<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">'
MARK = ('<svg class="mark" viewBox="0 0 120 120" aria-hidden="true"><defs><linearGradient id="yl-a" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#6366F1"/><stop offset="1" stop-color="#22D3EE"/></linearGradient><linearGradient id="yl-b" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#A78BFA"/><stop offset="1" stop-color="#22D3EE"/></linearGradient></defs>'
        '<path d="M60 8 105 34v52L60 112 15 86V34Z" fill="none" stroke="url(#yl-a)" stroke-width="5" stroke-linejoin="round"/>'
        '<path d="M32 42 60 64 88 42M60 64v24" fill="none" stroke="url(#yl-b)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
        '<g fill="#22D3EE"><circle cx="32" cy="42" r="5"/><circle cx="88" cy="42" r="5"/><circle cx="60" cy="88" r="5"/></g></svg>')
FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'><rect width='120' height='120' rx='26' fill='%23070A14'/>"
           "<path d='M60 14 100 37v46L60 106 20 83V37Z' fill='none' stroke='%236366F1' stroke-width='5'/>"
           "<path d='M36 44 60 64 84 44M60 64v22' fill='none' stroke='%2322D3EE' stroke-width='9' stroke-linecap='round'/></svg>")
NAV = ('<header class="site-header"><nav class="wrap nav" aria-label="주 메뉴"><a class="logo" href="/" aria-label="유니크랩스 홈">' + MARK +
       '<span>Yoonique<span class="logo-light">Labs</span></span></a><ul>'
       '<li><a class="link" href="/#apps">앱</a></li><li><a class="link" href="/#play">게임</a></li>'
       '<li><a class="link" href="/#windows">Windows</a></li><li><a class="link" href="/guides/">사용 가이드</a></li>'
       '<li><a class="link" href="/#about">스튜디오</a></li></ul>'
       '<a class="nav-contact" href="mailto:hello@yooniquelabs.kr">문의하기</a></nav></header>')
ARROW = '<span class="arr" aria-hidden="true">→</span>'


def play(a):
    return 'https://play.google.com/store/apps/details?id=' + a['package'] + '&hl=ko&gl=KR'


def icon(slug, size=56, lazy=True):
    return (f'<img class="app-icon" src="/assets/icons/{slug}.webp" width="{size}" height="{size}" alt="" '
            f'loading="{"lazy" if lazy else "eager"}" decoding="async">')


def shot(slug, n=1, lazy=True, alt=None):
    alt = alt if alt is not None else f'{by[slug]["name"]} 실제 앱 화면'
    return (f'<img src="/assets/shots/{slug}-{n}.webp" alt="{E(alt)}" height="640" '
            f'loading="{"lazy" if lazy else "eager"}" decoding="async">')


def phone(slug, n=1, lazy=True, extra=''):
    return f'<figure class="phone {extra}">{shot(slug, n, lazy)}<figcaption>{E(by[slug]["name"])}</figcaption></figure>'


def app_pill(slug):
    return f'<a class="app-pill" href="/apps/{slug}/">{icon(slug, 40)}<b>{E(by[slug]["name"])}</b></a>'


def collection(eyebrow, title, body, facts, slugs, shots, flip=False):
    return (f'<article class="collection{" flip" if flip else ""} reveal"><div class="collection-copy"><p class="eyebrow">{eyebrow}</p><h3>{title}</h3>'
            f'<p class="collection-body">{body}</p><ul class="facts">{"".join(f"<li>{f}</li>" for f in facts)}</ul>'
            f'<div class="pill-row">{"".join(app_pill(s) for s in slugs)}</div></div>'
            f'<div class="collection-shots">{"".join(phone(s, n) for s, n in shots)}</div></article>')


# ---------- homepage ----------
marquee_a = ordered[:11]
marquee_b = ordered[11:]


def marquee(row, cls):
    HID = ' aria-hidden="true" tabindex="-1"'
    cell = lambda a, hidden: (f'<a class="mq-item" href="/apps/{a["slug"]}/"{HID if hidden else ""}>'
                              f'{icon(a["slug"], 52, False)}<span>{E(a["name"])}</span></a>')
    return (f'<div class="marquee {cls}"><div class="marquee-track">{"".join(cell(a, False) for a in row)}'
            f'{"".join(cell(a, True) for a in row)}</div></div>')


cards = []
for a in ordered:
    slug, m = a['slug'], meta[a['slug']]
    chips = ''.join(f'<li>{E(c)}</li>' for c in m['chips'])
    cards.append(
        f'<article class="app-card" data-category="{m["group"]}" data-search="{E(a["name"] + " " + a["tag"] + " " + a["summary"] + " " + " ".join(a["keywords"]))}">'
        f'<div class="app-card-top">{icon(slug, 64)}<div><span class="app-category">{E(a["tag"])}</span>'
        f'<h3><a href="/apps/{slug}/">{E(a["name"])}</a></h3></div></div>'
        f'<p class="app-promise">{E(m["blurb"])}</p><p class="app-description">{E(a["summary"])}</p><ul class="chips">{chips}</ul>'
        f'<div class="app-card-links"><a href="/apps/{slug}/" aria-label="{E(a["name"])} 자세히 보기">자세히 보기 {ARROW}</a>'
        f'<a class="store" href="{E(play(a))}" aria-label="Google Play에서 {E(a["name"])} 설치">Google Play</a></div></article>')

groups = ['전체', '게임', '생활', '기록', '운동', '학습']
counts = {g: sum(1 for s in meta if meta[s]['group'] == g) for g in groups[1:]}
filters = ''.join(
    f'<button type="button" data-filter="{g}" aria-pressed="{str(g == "전체").lower()}">{g}<span>{N if g == "전체" else counts[g]}</span></button>'
    for g in groups)

guide_rows = [('/guides/' + g['slug'] + '/', by[g['app']]['name'], g['title']) for g in guides]
guide_rows += [('/guides/pdf-reader/', '유니크 PDF Reader', 'PDF Reader 설치부터 편집·주석, 양식 저장까지'),
               ('/guides/unique-excel/', '유니크 엑셀', '엑셀 설치와 문서 편집·저장 방법')]
guidecards = ''.join(
    f'<a class="guide-tile" href="{u}"><span class="guide-number">{i + 1:02d}</span><div><span class="guide-app">{E(n)}</span><h3>{E(t)}</h3></div>{ARROW}</a>'
    for i, (u, n, t) in enumerate(guide_rows))
bloglinks = ''.join(f'<a href="{E(b["url"])}"><span>{E(b["app"])}</span><strong>{E(b["title"])}</strong>{ARROW}</a>' for b in blogs)

schema_org = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Yoonique Labs', 'alternateName': '유니크랩스',
              'url': BASE + '/', 'email': 'hello@yooniquelabs.kr',
              'sameAs': ['https://play.google.com/store/apps/developer?id=Yoonique+Labs']}
schema_list = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': '유니크랩스 앱', 'numberOfItems': N,
               'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': a['name'], 'url': f'{BASE}/apps/{a["slug"]}/'}
                                   for i, a in enumerate(ordered)]}
head = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="naver-site-verification" content="eac97a459ae9db908eb381f09f69323f45a9b508" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#070A14">
<title>{TITLE}</title>
<meta name="description" content="{E(DESC)}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{E(OG_DESC)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<link rel="icon" href="{FAVICON}">
<link rel="canonical" href="{BASE}/">
<meta property="og:url" content="{BASE}/">
{FONT}
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/showcase.css"><script src="/assets/showcase.js" defer></script>
<script type="application/ld+json">{json.dumps(schema_org, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(schema_list, ensure_ascii=False)}</script>
</head>
'''
footer = '''<footer class="site-footer"><div class="wrap"><div class="footer-top"><a class="logo" href="/" aria-label="유니크랩스 홈">''' + MARK + '''<span>Yoonique<span class="logo-light">Labs</span></span></a>
<nav aria-label="바닥글 메뉴"><a href="/#apps">전체 앱</a><a href="/#play">게임</a><a href="/#windows">Windows</a><a href="/guides/">사용 가이드</a><a href="https://play.google.com/store/apps/developer?id=Yoonique+Labs">Google Play 개발자 페이지</a></nav></div>
<div class="biz">
<p><strong>상호</strong> 유니크랩스 (Yoonique Labs)</p>
<p><strong>대표자</strong> 윤상호 (SANGHO YOON)</p>
<p><strong>사업자등록번호</strong> 770-11-03155</p>
<p><strong>D-U-N-S® Number</strong> 696493065</p>
<p><strong>주소</strong> 부산광역시 수영구 호암로29번길 50, 103동 2503호 (48263)</p>
<p><strong>이메일</strong> hello@yooniquelabs.kr</p>
</div>
<div class="legal"><span>© 2026 Yoonique Labs. All rights reserved.</span><a href="/privacy.html">개인정보처리방침</a></div></div></footer>'''

play_section = ''.join([
    collection('PARTY · 술자리 · MT · 가족 모임', '폰 하나면,<br>모임이 게임판.',
               '칼을 꽂고, 이빨을 누르고, 얼음을 두드리고. 어릴 적 그 장난감 세 가지를 3D로 옮겼습니다. 방장이 QR을 띄우면 친구들은 앱을 설치하지 않고 브라우저로 바로 들어옵니다.',
               ['<b>QR 찍고 바로 입장</b> 친구는 앱 설치 없이 참가', '<b>폰 하나로도</b> 가운데 두고 돌려가며 한 판', '<b>벌칙 카드</b> 랜덤 미션·고정 벌칙과 오늘의 기록'],
               ['stabpirate', 'crocteeth', 'penguinice'], [('stabpirate', 1), ('crocteeth', 1), ('penguinice', 1)]),
    collection('CLAW · 3D 인형뽑기', '이번에는<br>잡을 수 있을 것 같은데?',
               '집게가 인형을 감싸 쥐고, 흔들리고, 아깝게 미끄러지는 순간까지 물리 엔진으로 움직입니다. 세 가지 게임, 세 가지 손맛.',
               ['<b>뽑기왕 3D</b> 스테이지 30개, 10회 확정 보장', '<b>크레인 드림즈</b> 테마 기계 8대, 인형 261종', '<b>뽑아봐 인형</b> 놓칠수록 세지는 파워 집게'],
               ['clawking3d', 'cranedreams', 'clawdoll'], [('clawking3d', 1), ('cranedreams', 1), ('clawdoll', 1)], flip=True),
    collection('AIR · 오프라인 보드게임', '비행기 모드에서도,<br>한 판.',
               '서버도 로그인도 없습니다. 데이터가 닿지 않는 기내와 지하철에서도 AI와 겨루고, 옆 사람 폰과는 블루투스로 직접 연결합니다.',
               ['<b>AI 19단계</b> 18급부터 초단까지, 내 급수에 맞춰', '<b>블루투스 대전</b> 인터넷 없이 폰 2대로', '<b>폰 하나로 둘이서</b> 폴드와 태블릿의 넓은 화면 지원'],
               ['omok', 'janggi', 'chosung5'], [('omok', 1), ('janggi', 1), ('omok', 2)]),
])
tools_section = ''.join([
    collection('BADMINTON · 동호회 운영', '코트에서는<br>경기에만 집중하세요.',
               '참가자를 고르면 복식 대진표가 완성되고, 회비와 회원, 대회 접수와 코트별 진행까지 한곳에서 관리합니다. 소모임이라면 로그인 없는 퀵대진표로 가볍게.',
               ['<b>대진표 자동 생성</b> 남복·여복·혼복과 순위표', '<b>회비 관리</b> 입금·미납과 수입·지출 장부', '<b>PC 웹 지원</b> 앱과 같은 계정으로 이용'],
               ['kokplus', 'quickbracket'], [('kokplus', 1), ('kokplus', 2), ('quickbracket', 1)]),
    collection('LEARN · 아이부터 어른까지', '하루 한 걸음,<br>아는 즐거움.',
               '아기의 첫 낱말부터 상식 퀴즈, 한국사 개념까지. 잠깐 열어도 하나는 배우고 닫도록 만들었습니다.',
               ['<b>쑥쑥 낱말카드</b> 12가지 주제 192장, 광고 없음', '<b>상식 한 스푼</b> 900문항, 광고·결제 없음', '<b>한걸음 한국사</b> 개념 73개와 문제 162개'],
               ['ssukssuk', 'sangsik', 'history-study'], [('ssukssuk', 1), ('sangsik', 1), ('history-study', 1)], flip=True),
    collection('EVERYDAY · 일과 생활', '복잡한 하루에,<br>간단한 도구 하나.',
               '교대근무표, 회식 정산, 주차 위치, 배달 순수익. 매번 헷갈리던 일을 한 화면으로 정리합니다. 대부분 회원가입 없이 바로 시작하고, 기록은 내 기기에 남습니다.',
               ['<b>교대한눈</b> 반복 패턴으로 근무표를 한 번에', '<b>깔끔정산</b> 1차·2차 참석자가 달라도 N빵', '<b>여기주차</b> 층수와 기둥 번호를 음성·사진으로'],
               ['gyodae-hannun', 'kkalkkeum', 'yeogi-parking', 'rider-net', 'juyuhalkka', 'foldnote'],
               [('kkalkkeum', 1), ('yeogi-parking', 1), ('gyodae-hannun', 1)]),
])

body = f'''<body class="showcase"><a class="skip-link" href="#main">본문 바로가기</a>{NAV}
<main id="main">
<section class="hero-dark"><div class="wrap hero-grid"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span>SOFTWARE STUDIO · BUSAN, KOREA</p>
<h1>일상을 편하게,<br>쉬는 시간을 <em>즐겁게.</em></h1>
<p class="hero-lede">대진표를 짜고, 회식비를 나누고, 주차한 곳을 기억하고. 모임에서는 폰 하나로 해적룰렛 한 판. 유니크랩스는 하루에 쓸모 있는 앱과 게임을 만듭니다.</p>
<div class="hero-actions"><a class="btn btn-glow" href="#apps">앱 {N}개 전체 보기 {ARROW}</a><a class="btn btn-line" href="#play">게임 먼저 구경하기</a></div>
<dl class="hero-stats"><div><dt>Android 앱·게임</dt><dd>{N}</dd></div><div><dt>Windows 프로그램</dt><dd>2</dd></div><div><dt>사용 가이드</dt><dd>{len(guide_rows)}</dd></div></dl></div>
<div class="hero-phones" aria-label="Google Play에 공개된 실제 앱 화면">{phone('kokplus', 1, False, 'p1')}{phone('stabpirate', 1, False, 'p2')}{phone('cranedreams', 1, False, 'p3')}</div></div>
<div class="marquee-band" aria-label="유니크랩스의 앱과 게임">{marquee(marquee_a, 'to-left')}{marquee(marquee_b, 'to-right')}</div></section>

<section id="play" class="play-section"><div class="wrap"><div class="section-heading on-dark"><div><p class="eyebrow">PLAY / 01</p><h2>같이 놀 때도, 혼자 쉴 때도.</h2></div><p>파티게임 3종, 인형뽑기 3종, 인터넷 없이 두는 오목과 장기.<br>모두 Google Play에서 만나보세요.</p></div>{play_section}</div></section>

<section id="tools" class="tools-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">TOOLS / 02</p><h2>작은 불편을 덜어 주는 도구.</h2></div><p>동호회 운영부터 배움, 일과 생활 기록까지.<br>필요한 기능만 담아 가볍게 만들었습니다.</p></div>{tools_section}</div></section>

<section id="apps" class="apps-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">ALL APPS / 03</p><h2>지금 필요한 앱을 찾아보세요.</h2></div><p>유니크랩스가 Google Play에 공개한 앱 {N}가지.<br>분류를 고르거나 이름·기능으로 검색하세요.</p></div>
<div class="directory-controls" hidden><div class="filter-buttons" role="group" aria-label="앱 분류">{filters}</div><label class="app-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="app-search" type="search" placeholder="앱 이름이나 기능 검색" aria-label="앱 이름이나 기능 검색"></label></div><p class="result-count" aria-live="polite" aria-atomic="true" hidden>전체 {N}개의 앱</p>
<div class="app-grid">{''.join(cards)}</div><div class="empty-results" hidden><h3>찾으시는 앱이 없어요.</h3><p>다른 검색어를 입력하거나 전체 앱을 확인해 보세요.</p><button class="btn btn-primary" type="button" id="reset-apps">전체 앱 보기</button></div></div></section>

<section id="windows" class="windows-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">FOR WINDOWS / 04</p><h2>PC에서 쓰는 유니크 시리즈.</h2></div><p>설치 파일을 내려받아 바로 사용하세요.<br>문서는 내 컴퓨터에서 처리합니다.</p></div>
<div class="win-grid"><article class="win-card reveal"><div class="win-copy"><p class="eyebrow">PDF · WINDOWS 10/11</p><h3>유니크 PDF Reader</h3><p>PDF를 읽고, 필요한 내용을 고치고, 주석을 달고, 양식을 채우세요. PDF를 서버에 업로드하지 않습니다.</p><ul class="chips"><li>읽기·편집</li><li>주석</li><li>양식 입력</li></ul><div class="cta"><a class="btn btn-primary" href="/apps/pdf-reader/">Windows 다운로드 {ARROW}</a><a class="btn btn-ghost" href="/guides/pdf-reader/">설치·사용 방법</a></div></div><figure class="win-shot"><img src="/assets/pdf-reader/screen.png" alt="유니크 PDF Reader 실행 화면" loading="lazy" decoding="async"></figure></article>
<article class="win-card reveal"><div class="win-copy"><p class="eyebrow">SPREADSHEET · WINDOWS</p><h3>유니크 엑셀</h3><p>XLSX·XLSM·CSV 문서 편집부터 수식 계산, 차트와 피벗까지. 익숙한 표 계산을 가볍게 시작하세요.</p><ul class="chips"><li>XLSX·CSV</li><li>수식</li><li>차트·피벗</li></ul><div class="cta"><a class="btn btn-primary" href="/apps/unique-excel/">Windows 다운로드 {ARROW}</a><a class="btn btn-ghost" href="/guides/unique-excel/">설치·사용 방법</a></div></div><figure class="win-shot"><img src="/assets/unique-excel/screen.png" alt="유니크 엑셀 실행 화면" loading="lazy" decoding="async"></figure></article></div></div></section>

<section id="guides" class="guides-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">HOW TO / 05</p><h2>처음부터, 어렵지 않게.</h2></div><a class="quiet-link" href="/guides/">사용 가이드 전체 보기 {ARROW}</a></div><div class="guide-grid">{guidecards}</div></div></section>

<section id="stories" class="stories-section"><div class="wrap stories-layout"><div><p class="eyebrow">FROM THE STUDIO / 06</p><h2>이럴 때<br>이 앱을 써보세요.</h2><p>일상에서 마주치는 작은 고민과<br>앱을 활용하는 방법을 나눕니다.</p><a class="quiet-link" href="https://blog.naver.com/PostList.naver?blogId=cupidjjang&amp;categoryNo=10">네이버 블로그 {ARROW}</a></div><div class="story-list">{bloglinks}</div></div></section>

<section id="about" class="about-section"><div class="wrap about-layout"><div><p class="eyebrow">YOONIQUE LABS · BUSAN, KOREA</p><h2>작은 불편에서<br>시작합니다.</h2><p class="about-lede">유니크랩스는 부산에서 앱과 게임을 만드는 소프트웨어 스튜디오입니다. 동호회 운영부터 생활 기록, 모임에서 즐기는 게임까지. 직접 기획하고 개발하며, 사용자의 이야기를 듣고 개선합니다.</p><a class="quiet-link" href="mailto:hello@yooniquelabs.kr">앱에 대한 의견 보내기 {ARROW}</a></div>
<ol class="principles"><li><span>01</span><div><h3>가볍게 시작합니다</h3><p>많은 앱이 회원가입 없이 열자마자 바로 쓸 수 있습니다.</p></div></li><li><span>02</span><div><h3>기록은 내 기기에</h3><p>메모와 정산, 근무표와 문서는 가능한 한 기기 안에 둡니다.</p></div></li><li><span>03</span><div><h3>있는 그대로 안내합니다</h3><p>하지 않는 기능과 광고 포함 여부를 앱 소개에 그대로 적습니다.</p></div></li></ol></div></section>

<section id="contact" class="contact-section"><div class="wrap"><p class="eyebrow">LET’S MAKE THINGS BETTER</p><h2>당신의 이야기를 들려주세요.</h2><p>앱 이용 문의, 개선 의견, 제휴 제안을 기다립니다.</p><a class="contact-email" href="mailto:hello@yooniquelabs.kr">hello@yooniquelabs.kr {ARROW}</a></div></section>
</main>{footer}</body></html>'''
(ROOT / 'index.html').write_text(head + body, encoding='utf-8')

# ---------- app detail pages ----------
DETAIL_FOOT = ('<footer><div class="wrap"><p>유니크랩스 · Yoonique Labs</p><p>앱 이용 문의: <a href="mailto:hello@yooniquelabs.kr">hello@yooniquelabs.kr</a></p>'
               '<div class="legal"><a href="/">공식 홈페이지</a>{privacy}<a href="/privacy.html">웹사이트 개인정보처리방침</a></div></div></footer>')


def new_detail(a):
    url = f'{BASE}/apps/{a["slug"]}/'
    schema = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': a['title'], 'url': url, 'description': a['summary'], 'inLanguage': 'ko-KR',
              'about': {'@type': 'SoftwareApplication', 'name': a['name'], 'operatingSystem': 'Android', 'url': play(a), 'description': a['summary']},
              'publisher': {'@type': 'Organization', 'name': 'Yoonique Labs', 'url': BASE + '/'}}
    features = ''.join(f'<h3>{E(h)}</h3><p>{E(p)}</p>' for h, p in a['features'])
    steps = ''.join(f'<li>{E(s)}</li>' for s in a['steps'])
    faq = ''.join(f'<h3>{E(q)}</h3><p>{E(ans)}</p>' for q, ans in a['faq'])
    extra = f'<a class="btn btn-ghost" href="{E(a["extra"])}">{E(a["extraLabel"])}</a>' if a.get('extra') else ''
    privacy = a.get('privacy')
    plink = f'<p><a href="{E(privacy)}">이 앱의 개인정보처리방침</a></p>' if privacy else ''
    pfoot = f'<a href="{E(privacy)}">앱 개인정보처리방침</a>' if privacy else ''
    return f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(a['title'])} | 유니크랩스</title>
<meta name="description" content="{E(a['summary'])}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{E(a['title'])}"><meta property="og:description" content="{E(a['summary'])}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:locale" content="ko_KR">
<link rel="stylesheet" href="/assets/site.css"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body><header></header>
<main><div class="wrap breadcrumb"><a href="/">홈</a> / <a href="/#apps">앱</a> / {E(a['name'])}</div>
<div class="hero"><div class="wrap detail"><p class="eyebrow">{E(a['tag'])}</p><h1>{E(a['title'])}</h1><p class="lede">{E(a['summary'])}</p><div class="cta"><a class="btn btn-primary" href="{E(play(a))}">Google Play에서 설치</a>{extra}</div></div></div>
<section><div class="wrap detail"><h2>{E(a['name'])}로 할 수 있는 일</h2>{features}</div></section>
<section><div class="wrap detail"><h2>이렇게 시작하세요</h2><ol>{steps}</ol></div></section>
<section><div class="wrap detail"><h2>자주 묻는 질문</h2>{faq}<p class="note">{E(a['notes'])}</p>{plink}<div class="cta"><a class="btn btn-primary" href="{E(play(a))}">Google Play에서 {E(a['name'])} 보기</a></div></div></section>
<section><div class="wrap detail"><h2>유니크랩스의 다른 앱</h2><div class="related"></div></div></section></main>
{DETAIL_FOOT.format(privacy=pfoot)}</body></html>'''


def strip_block(text, name):
    return re.sub(rf'<!--{name}-->.*?<!--/{name}-->', '', text, flags=re.S)


def ensure_head(text):
    if 'pretendard' not in text:
        text = text.replace('<link rel="stylesheet" href="/assets/site.css">', FONT + '<link rel="stylesheet" href="/assets/site.css">', 1)
    if '/assets/showcase.css' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="/assets/showcase.css"></head>', 1)
    if 'rel="icon"' not in text:
        text = text.replace('</head>', f'<link rel="icon" href="{FAVICON}"></head>', 1)
    return re.sub(r'<header[^>]*>.*?</header>', lambda m: NAV, text, count=1, flags=re.S)


created = 0
for a in apps:
    slug, m = a['slug'], meta[a['slug']]
    p = ROOT / f'apps/{slug}/index.html'
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(new_detail(a), encoding='utf-8')
        created += 1
    text = ensure_head(p.read_text(encoding='utf-8'))
    text = re.sub(r'<body[^>]*>', '<body class="app-detail">', text, count=1)
    if 'feature-grid' not in text:
        text = re.sub(r'(<h2>[^<]+로 할 수 있는 일</h2>)(.*?)(</div></section>)',
                      lambda mm: mm[1] + '<div class="feature-grid">' + re.sub(r'<h3>(.*?)</h3><p>(.*?)</p>', r'<article><h3>\1</h3><p>\2</p></article>', mm[2], flags=re.S) + '</div>' + mm[3],
                      text, count=1, flags=re.S)
    text = re.sub(r'<figure class="detail-screenshot">.*?</figure>', '', text, flags=re.S)
    for block in ('detail-id', 'detail-gallery'):
        text = strip_block(text, block)
    ident = (f'<!--detail-id--><div class="detail-id">{icon(slug, 88, False)}<ul class="chips">'
             f'{"".join(f"<li>{E(c)}</li>" for c in m["chips"])}</ul></div><!--/detail-id-->')
    text = text.replace('<div class="hero"><div class="wrap detail"><p class="eyebrow">', '<div class="hero"><div class="wrap detail">' + ident + '<p class="eyebrow">', 1)
    y, mo, d = m['updated'].split('-')
    gallery = (f'<!--detail-gallery--><div class="detail-gallery"><div class="gallery-strip" tabindex="0" aria-label="{E(a["name"])} 스크린샷">'
               f'{"".join(shot(slug, i + 1, i > 1, a["name"] + " 실제 앱 화면 " + str(i + 1)) for i in range(m["shots"]))}</div>'
               f'<p class="gallery-note">Google Play 공개 스크린샷 · 최근 업데이트 {y}년 {int(mo)}월 {int(d)}일 · 앱 버전에 따라 화면은 달라질 수 있습니다.</p></div><!--/detail-gallery-->')
    text = text.replace('</div></div>\n<section>', gallery + '</div></div>\n<section>', 1)
    related = ''.join(f'<a href="/apps/{o["slug"]}/">{icon(o["slug"], 28)}{E(o["name"])}</a>' for o in ordered if o['slug'] != slug)
    text = re.sub(r'<div class="related">.*?</div>', lambda mm: f'<div class="related">{related}</div>', text, count=1, flags=re.S)
    text = re.sub(r'<div class="detail-blog[^"]*">.*?</div>', '', text, flags=re.S)
    blog = next((b for b in blogs if b['app'] == a['name']), None)
    if blog:
        text = text.replace('</main>', f'<div class="detail-blog wrap detail"><p class="eyebrow">개발사 블로그</p><a href="{blog["url"]}">{E(blog["title"])} →</a></div></main>')
    p.write_text(text, encoding='utf-8')

# ---------- shared chrome on guides and Windows pages ----------
others = list((ROOT / 'guides').rglob('index.html')) + [ROOT / 'apps/pdf-reader/index.html', ROOT / 'apps/unique-excel/index.html']
for p in others:
    if p.exists():
        p.write_text(ensure_head(p.read_text(encoding='utf-8')), encoding='utf-8')

# ---------- sitemap ----------
sm = ROOT / 'sitemap.xml'
text = sm.read_text(encoding='utf-8')
for a in apps:
    url = f'{BASE}/apps/{a["slug"]}/'
    if url not in text:
        text = text.replace('</urlset>', f'<url><loc>{url}</loc><lastmod>{meta[a["slug"]]["updated"]}</lastmod></url>\n</urlset>')
sm.write_text(text, encoding='utf-8')
print(f'Built homepage with {N} apps; created {created} new app pages; refreshed {len(apps)} detail pages and {len(others)} shared pages.')
