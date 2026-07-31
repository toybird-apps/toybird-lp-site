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

selectOS('windows', false);

const WINDOWS_STORE_URL = 'https://apps.microsoft.com/detail/9pd31c5s8v7p?hl=ja-JP&gl=JP';
const MAC_STORE_URL = 'https://apps.apple.com/jp/app/prompt-ready-ai%E4%BE%9D%E9%A0%BC%E6%96%87%E4%BD%9C%E6%88%90/id6779955570?mt=12';

function preferredDeviceOS() {
  const params = new URLSearchParams(window.location.search);
  const requested = params.get('os');
  if (requested === 'windows' || requested === 'macos') return requested;

  try {
    const saved = localStorage.getItem('promptReadySelectedOS');
    if (saved === 'windows' || saved === 'macos') return saved;
  } catch (_) {}

  const platform = `${navigator.userAgent || ''} ${navigator.platform || ''}`;
  if (/iPhone|iPad|iPod|Android|Mobile/i.test(platform)) return null;
  if (/Windows/i.test(platform)) return 'windows';
  if (/Macintosh|Mac OS X|MacIntel/i.test(platform)) return 'macos';
  return null;
}

function configureOSRecommendations() {
  const preferred = preferredDeviceOS();

  document.querySelectorAll('[data-os-cta]').forEach((link) => {
    link.classList.toggle('is-recommended', Boolean(preferred && link.dataset.osCta === preferred));
  });
}

configureOSRecommendations();

document.querySelectorAll('[data-app-info-link]').forEach((link) => {
  link.addEventListener('click', () => {
    selectOS('windows', false);
  });
});
