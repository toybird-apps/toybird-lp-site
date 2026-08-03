(function () {
  'use strict';

  const body = document.body;
  const articleId = body?.dataset.articleId || 'unknown';
  const articleTitle = body?.dataset.articleTitle || document.title;
  const fired = new Set();

  function send(name, params) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', name, {
      article_id: articleId,
      article_title: articleTitle,
      content_group: 'Toybird Labs Blog',
      page_language: body?.dataset.pageLanguage || 'ja',
      ...params
    });
  }

  send('article_start', { page_location: window.location.href });

  [30, 60, 120].forEach((seconds) => {
    window.setTimeout(() => {
      if (document.visibilityState !== 'visible') return;
      const key = `time_${seconds}`;
      if (fired.has(key)) return;
      fired.add(key);
      send('article_engaged_time', { engagement_seconds: seconds });
    }, seconds * 1000);
  });

  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      if (!target) return;
      const text = target.textContent.trim();
      try {
        await navigator.clipboard.writeText(text);
        const original = button.textContent;
        button.textContent = 'コピーしました';
        window.setTimeout(() => { button.textContent = original; }, 1400);
        send('prompt_copy', {
          prompt_id: button.dataset.promptId || button.dataset.copyTarget,
          prompt_label: button.dataset.promptLabel || ''
        });
      } catch (_) {
        button.textContent = 'コピーできませんでした';
      }
    });
  });

  document.querySelectorAll('a[data-product-link]').forEach((link) => {
    link.addEventListener('click', () => {
      send('product_link_click', {
        product_name: link.dataset.productName || 'Prompt Ready',
        link_location: link.dataset.linkLocation || 'article',
        destination_url: link.href,
        store_platform: link.dataset.storePlatform || ''
      });
    });
  });

  const end = document.querySelector('[data-article-end]');
  if (end && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      if (!fired.has('complete')) {
        fired.add('complete');
        send('article_complete', { completion_method: 'end_visible' });
      }
      observer.disconnect();
    }, { threshold: 0.25 });
    observer.observe(end);
  }
})();
