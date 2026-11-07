(() => {
  const announce = (message) => {
    const area = document.getElementById('announcement');
    if (!area) return;
    area.textContent = message;
    window.clearTimeout(announce.timer);
    announce.timer = window.setTimeout(() => { area.textContent = ''; }, 3500);
  };
  document.querySelectorAll('[data-copy-link]').forEach(button => button.addEventListener('click', async () => {
    const url = new URL(button.dataset.copyLink || location.pathname, location.origin).href;
    try {
      if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(url);
      else {
        const input = document.createElement('textarea'); input.value = url;
        input.style.position = 'fixed'; input.style.opacity = '0';
        document.body.append(input); input.select();
        const copied = document.execCommand('copy'); input.remove();
        if (!copied) throw new Error('Clipboard unavailable');
      }
      announce('Link copied. Ready to share.');
    } catch { announce('Select and copy the address from your browser to share this page.'); }
  }));
  let printStates = [];
  window.addEventListener('beforeprint', () => {
    printStates = [...document.querySelectorAll('details')].map(el => [el, el.open]);
    printStates.forEach(([el]) => el.open = true);
  });
  window.addEventListener('afterprint', () => printStates.forEach(([el, state]) => el.open = state));
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  const search = document.getElementById('search');
  if (!search) return;
  const grammar = document.getElementById('grammar');
  const tabs = [...document.querySelectorAll('[data-group-filter]')];
  const cards = [...document.querySelectorAll('[data-practice-card]')];
  let group = 'all';
  const normalize = text => text.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const update = () => {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    cards.forEach(card => {
      const match = (group === 'all' || card.dataset.group === group) &&
        (!grammar.value || JSON.parse(card.dataset.tags).includes(grammar.value)) &&
        words.every(word => normalize(card.dataset.search).includes(word));
      card.hidden = !match; if (match) visible++;
    });
    document.getElementById('result-count').textContent = `${visible} ${visible === 1 ? 'entry' : 'entries'}`;
    document.getElementById('empty').hidden = visible !== 0;
    tabs.forEach(tab => tab.setAttribute('aria-pressed', String(tab.dataset.groupFilter === group)));
  };
  tabs.forEach(tab => tab.addEventListener('click', () => { group = tab.dataset.groupFilter; update(); }));
  search.addEventListener('input', update); grammar.addEventListener('change', update);
  document.getElementById('reset').addEventListener('click', () => { search.value=''; grammar.value=''; group='all'; update(); search.focus(); });
  update();
})();
