(function () {
  const STORAGE_KEY = 'toybird_language';
  const pageLanguage = document.documentElement.lang || 'unknown';
  const appName = document.body?.dataset.appName || 'unknown';

  document.querySelectorAll('[data-language-switch]').forEach((link) => {
    link.addEventListener('click', () => {
      const language = link.getAttribute('data-language-switch');
      try { localStorage.setItem(STORAGE_KEY, language); } catch (_) {}
      const parameters = {
        app_name: appName,
        page_language: pageLanguage,
        target_language: language,
        language_from: pageLanguage,
        language_to: language,
        page_path: window.location.pathname,
        transport_type: 'beacon'
      };
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'language_switch', parameters);
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
