/* Shared LP / Labs award motion: 32 CSS px/s, Product Hunt centered immediately, then a seamless loop. */
(() => {
  document.querySelectorAll('.ps-awards').forEach(band => {
    const viewport = band.querySelector('.ps-awards-viewport');
    const track = band.querySelector('.ps-awards-track');
    const group = band.querySelector('.ps-awards-group');
    const button = band.querySelector('.ps-awards-toggle');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    let x = 0, cycle = 0, manual = false, hover = false, visible = false, last = 0;
    let keyboardFocus = false;
    document.addEventListener('keydown', e => { if (e.key === 'Tab') keyboardFocus = true; });
    document.addEventListener('pointerdown', () => { keyboardFocus = false; }, true);
    const ja = document.documentElement.lang.startsWith('ja');
    function centeredStart() {
      const ph = group.querySelector('.ps-ph') || group.firstElementChild;
      const center = ph.getBoundingClientRect().left - group.getBoundingClientRect().left + ph.getBoundingClientRect().width / 2;
      const offset = viewport.clientWidth / 2 - center;
      return ((offset % cycle) + cycle) % cycle - cycle;
    }
    function measure() {
      track.querySelectorAll('.ps-awards-clone').forEach(el => el.remove());
      cycle = group.getBoundingClientRect().width;
      if (!cycle) return;
      for (let i = 0; i < Math.ceil(viewport.clientWidth / cycle) + 1; i++) {
        const clone = group.cloneNode(true);
        clone.classList.add('ps-awards-clone'); clone.setAttribute('aria-hidden','true');
        clone.querySelectorAll('a').forEach(a => a.tabIndex = -1);
        track.append(clone);
      }
      x = centeredStart();
      if (!manual) track.style.transform = `translateX(${x}px)`;
      last = 0;
    }
    function setManual(value) {
      manual = value;
      band.classList.toggle('is-manual', value);
      band.classList.toggle('is-animated', !value);
      if (value) { track.style.transform = 'none'; viewport.scrollLeft = 0; }
      else { x = centeredStart(); viewport.scrollLeft = 0; track.style.transform = `translateX(${x}px)`; }
      button.textContent = value ? (ja ? '自動スクロールを再開' : 'Resume scrolling') : (ja ? '停止して手動で見る' : 'Pause / browse');
      button.setAttribute('aria-pressed', String(value));
      last = 0;
    }
    measure();
    band.classList.add('is-animated');
    track.style.transform = `translateX(${x}px)`;
    button.hidden = false;
    document.documentElement.classList.remove('ps-awards-pending');
    button.addEventListener('click', () => setManual(!manual));
    viewport.addEventListener('mouseenter', () => { hover = true; });
    viewport.addEventListener('mouseleave', () => { hover = false; last = 0; });
    viewport.addEventListener('pointerdown', e => { if(e.pointerType !== 'mouse' && !manual) { e.preventDefault(); setManual(true); } });
    viewport.addEventListener('focusin', () => { if(keyboardFocus && !manual) setManual(true); });
    reduced.addEventListener('change', () => { if(reduced.matches) setManual(true); });
    if (reduced.matches) setManual(true);
    const resize = new ResizeObserver(measure);
    resize.observe(viewport);
    resize.observe(group);
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; last = 0; }).observe(viewport);
    document.addEventListener('visibilitychange', () => { last = 0; });
    function frame(t) {
      if (!manual && !hover && visible && !document.hidden) {
        if(last) x -= Math.min(t-last,100)/1000*32;
        if(x <= -cycle) x += cycle;
        track.style.transform = `translateX(${x}px)`;
        last = t;
      } else last = 0;
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  });
})();
