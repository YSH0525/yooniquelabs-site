(() => {
  const controls = document.querySelector('.directory-controls');
  if (!controls) return;
  const cards = [...document.querySelectorAll('.app-card')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const search = document.querySelector('#app-search');
  const count = document.querySelector('.result-count');
  const empty = document.querySelector('.empty-results');
  let category = '전체';
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase('ko').replace(/\s+/g, '');
  const update = () => {
    const query = normalize(search.value);
    let visible = 0;
    cards.forEach(card => {
      const match = (category === '전체' || card.dataset.category === category) && normalize(card.dataset.search).includes(query);
      card.hidden = !match;
      if (match) visible++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    count.textContent = `${category} ${visible}개의 앱${search.value.trim() ? ' · 검색 결과' : ''}`;
    empty.hidden = visible !== 0;
  };
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
  search.addEventListener('input', update);
  document.querySelector('#reset-apps').addEventListener('click', () => { category = '전체'; search.value = ''; update(); search.focus(); });
  controls.hidden = false;
  count.hidden = false;
  update();
})();
