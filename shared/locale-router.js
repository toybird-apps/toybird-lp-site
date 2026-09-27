(function () {
  const STORAGE_KEY = 'toybird_language';
  const ROUTES = {
    ja: '/ai-memorize-sheet/',
    en: '/en/ai-memorize-sheet/',
    ko: '/ko/ai-memorize-sheet/',
    'zh-CN': '/zh-cn/ai-memorize-sheet/'
  };

  function normalizeLanguage(value) {
    if (!value) return null;
    const language = String(value).toLowerCase();
    if (language === 'ja' || language.startsWith('ja-')) return 'ja';
    if (language === 'ko' || language.startsWith('ko-')) return 'ko';
    if (language === 'zh-cn' || language === 'zh-hans' || language.startsWith('zh-') || language === 'zh') return 'zh-CN';
    if (language === 'en' || language.startsWith('en-')) return 'en';
    return null;
  }

  function currentLanguage(pathname) {
    if (/^\/en\/ai-memorize-sheet(?:\/|\/index\.html)?$/.test(pathname)) return 'en';
    if (/^\/ko\/ai-memorize-sheet(?:\/|\/index\.html)?$/.test(pathname)) return 'ko';
    if (/^\/zh-cn\/ai-memorize-sheet(?:\/|\/index\.html)?$/.test(pathname)) return 'zh-CN';
    if (/^\/ai-memorize-sheet(?:\/|\/index\.html)?$/.test(pathname)) return 'ja';
    return null;
  }

  try {
    const current = currentLanguage(location.pathname);
    if (!current) return;

    const ua = navigator.userAgent || '';
    if (/bot|crawl|spider|slurp|bingpreview/i.test(ua)) return;

    const params = new URLSearchParams(location.search);
    if (params.has('lang')) return;

    let saved = null;
    try { saved = normalizeLanguage(localStorage.getItem(STORAGE_KEY)); } catch (_) {}

    const browserLanguage = normalizeLanguage(
      (navigator.languages && navigator.languages[0]) || navigator.language || 'en'
    ) || 'en';

    const target = saved || browserLanguage;
    if (!ROUTES[target] || target === current) return;

    if (!saved) {
      try { sessionStorage.setItem('toybird_auto_language', target); } catch (_) {}
    }

    location.replace(ROUTES[target] + location.search + location.hash);
  } catch (_) {}
})();