(() => {
  const items = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window)) {
    items.forEach((item) => item.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        currentObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -35px 0px' });

  items.forEach((item) => observer.observe(item));
})();

// App Storeへの遷移を、通常の離脱クリックとは別にGA4イベントとして記録します。
(() => {
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href*="apps.apple.com"]');
    if (!link || typeof window.gtag !== 'function') return;

    window.gtag('event', 'app_store_click', {
      app_name: 'AI暗記シート',
      link_url: link.href,
      link_text: link.textContent.trim().replace(/\s+/g, ' '),
      page_location: window.location.href
    });
  });
})();
