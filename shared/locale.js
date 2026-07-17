(function () {
  const STORAGE_KEY = 'toybird_language';
  const pageLanguage = document.documentElement.lang || 'unknown';

  document.querySelectorAll('[data-language-switch]').forEach((link) => {
    link.addEventListener('click', () => {
      const language = link.getAttribute('data-language-switch');
      try { localStorage.setItem(STORAGE_KEY, language); } catch (_) {}
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'language_switch', {
          language_from: pageLanguage,
          language_to: language,
          page_path: window.location.pathname
        });
      }
    });
  });

  try {
    const autoLanguage = sessionStorage.getItem('toybird_auto_language');
    if (autoLanguage) {
      sessionStorage.removeItem('toybird_auto_language');
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'language_auto_selected', {
          page_language: autoLanguage,
          page_path: window.location.pathname
        });
      }
    }
  } catch (_) {}
})();
