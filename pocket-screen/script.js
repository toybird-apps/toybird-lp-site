const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

// Mac App Storeへの遷移を、通常の離脱クリックとは別にGA4イベントとして記録します。
document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href*="apps.apple.com"]');
  if (!link || typeof window.gtag !== 'function') return;

  window.gtag('event', 'app_store_click', {
    app_name: 'Pocket Screen',
    page_language: document.documentElement.lang || 'unknown',
    link_url: link.href,
    link_text: link.getAttribute('aria-label') || link.textContent.trim().replace(/\s+/g, ' '),
    page_location: window.location.href
  });
});
