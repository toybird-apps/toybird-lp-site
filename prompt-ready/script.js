const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

const osTabs = Array.from(document.querySelectorAll('.os-tab'));
const osPanels = Array.from(document.querySelectorAll('.os-detail[data-panel]'));

function selectOS(os, remember = true) {
  osTabs.forEach((tab) => {
    const selected = tab.dataset.os === os;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
  });

  osPanels.forEach((panel) => {
    panel.hidden = panel.dataset.panel !== os;
  });

  if (remember) {
    try { localStorage.setItem('promptReadySelectedOS', os); } catch (_) {}
  }
}

function detectOS() {
  const params = new URLSearchParams(window.location.search);
  const requested = params.get('os');
  if (requested === 'windows' || requested === 'macos') return requested;

  try {
    const saved = localStorage.getItem('promptReadySelectedOS');
    if (saved === 'windows' || saved === 'macos') return saved;
  } catch (_) {}

  const platform = `${navigator.userAgent || ''} ${navigator.platform || ''}`;
  if (/Windows/i.test(platform)) return 'windows';
  if (/Macintosh|Mac OS X|MacIntel/i.test(platform)) return 'macos';
  return 'windows';
}

osTabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectOS(tab.dataset.os));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    const direction = event.key === 'ArrowRight' ? 1 : -1;
    const next = osTabs[(index + direction + osTabs.length) % osTabs.length];
    selectOS(next.dataset.os);
    next.focus();
  });
});

selectOS(detectOS(), false);

document.addEventListener('click', (event) => {
  const link = event.target.closest('a.store-link');
  if (!link || typeof window.gtag !== 'function') return;

  const eventName = link.dataset.event || 'store_click';
  const parameters = {
    app_name: 'Prompt Ready',
    page_language: document.documentElement.lang || 'unknown',
    store_platform: link.dataset.platform || 'unknown',
    link_url: link.href,
    link_text: link.getAttribute('aria-label') || link.textContent.trim().replace(/\s+/g, ' '),
    page_location: window.location.href
  };

  window.gtag('event', eventName, parameters);
  window.gtag('event', 'store_click', parameters);
});
