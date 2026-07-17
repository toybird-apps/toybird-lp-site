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
  const previousOS = osTabs.find((tab) => tab.getAttribute('aria-selected') === 'true')?.dataset.os;
  const selectionChanged = previousOS !== os;

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

  if (remember && selectionChanged) {
    document.dispatchEvent(new CustomEvent('toybird:os-select', { detail: { os_name: os } }));
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
