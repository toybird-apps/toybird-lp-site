(function () {
  'use strict';

  const body = document.body;
  if (!body) return;

  const appName = body.dataset.appName || 'unknown';
  const pageLanguage = body.dataset.pageLanguage || document.documentElement.lang || 'unknown';
  const sectionTimers = new Map();
  const ctaTimers = new Map();
  const viewedSections = new Set();
  const viewedCtas = new Set();
  const reachedScrollDepths = new Set();

  function compact(parameters) {
    return Object.fromEntries(
      Object.entries(parameters).filter(([, value]) => value !== undefined && value !== null && value !== '')
    );
  }

  function sendEvent(eventName, parameters) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', eventName, compact({
      app_name: appName,
      page_language: pageLanguage,
      ...parameters
    }));
  }

  function visibleLongEnough(entry, requiredRatio) {
    if (!entry.isIntersecting) return false;
    if (entry.intersectionRatio >= requiredRatio) return true;

    // Very tall sections can never reach a 30% IntersectionObserver ratio.
    // Treat half of the viewport as sufficient only for those sections.
    const elementHeight = entry.boundingClientRect.height;
    const viewportHeight = entry.rootBounds ? entry.rootBounds.height : window.innerHeight;
    const visibleHeight = entry.intersectionRect.height;
    return elementHeight > viewportHeight / requiredRatio && visibleHeight >= viewportHeight * 0.5;
  }

  function isCurrentlyVisible(element, requiredRatio) {
    const rect = element.getBoundingClientRect();
    const viewportWidth = document.documentElement.clientWidth;
    const viewportHeight = window.innerHeight;
    const visibleWidth = Math.max(0, Math.min(rect.right, viewportWidth) - Math.max(rect.left, 0));
    const visibleHeight = Math.max(0, Math.min(rect.bottom, viewportHeight) - Math.max(rect.top, 0));
    const elementArea = rect.width * rect.height;
    const visibleArea = visibleWidth * visibleHeight;
    const ratio = elementArea > 0 ? visibleArea / elementArea : 0;
    return ratio >= requiredRatio || (rect.height > viewportHeight / requiredRatio && visibleHeight >= viewportHeight * 0.5);
  }

  function observeWithDwellTime(elements, options) {
    if (!elements.length) return;

    if (!('IntersectionObserver' in window)) {
      let fallbackFrameRequested = false;
      const checkFallbackVisibility = () => {
        fallbackFrameRequested = false;
        elements.forEach((element) => {
          const eventId = options.getId(element);
          if (!eventId || options.viewed.has(eventId)) return;

          if (isCurrentlyVisible(element, options.ratio)) {
            if (!options.timers.has(element)) {
              options.timers.set(element, window.setTimeout(() => {
                options.timers.delete(element);
                if (options.viewed.has(eventId) || !isCurrentlyVisible(element, options.ratio)) return;
                options.viewed.add(eventId);
                options.onView(element);
              }, 500));
            }
          } else if (options.timers.has(element)) {
            window.clearTimeout(options.timers.get(element));
            options.timers.delete(element);
          }
        });
      };
      const requestFallbackCheck = () => {
        if (fallbackFrameRequested) return;
        fallbackFrameRequested = true;
        window.requestAnimationFrame(checkFallbackVisibility);
      };
      window.addEventListener('scroll', requestFallbackCheck, { passive: true });
      window.addEventListener('resize', requestFallbackCheck);
      requestFallbackCheck();
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const element = entry.target;
        const eventId = options.getId(element);
        if (!eventId || options.viewed.has(eventId)) return;

        if (visibleLongEnough(entry, options.ratio)) {
          if (!options.timers.has(element)) {
            options.timers.set(element, window.setTimeout(() => {
              options.timers.delete(element);
              if (options.viewed.has(eventId)) return;
              if (!isCurrentlyVisible(element, options.ratio)) return;
              options.viewed.add(eventId);
              options.onView(element);
              observer.unobserve(element);
            }, 500));
          }
        } else if (options.timers.has(element)) {
          window.clearTimeout(options.timers.get(element));
          options.timers.delete(element);
        }
      });
    }, { threshold: Array.from(new Set([0, 0.05, 0.1, 0.15, 0.2, 0.25, options.ratio, 0.5, 0.75, 1])).sort((a, b) => a - b) });

    elements.forEach((element) => observer.observe(element));
  }

  const sections = Array.from(document.querySelectorAll('[data-track-section]'));
  observeWithDwellTime(sections, {
    ratio: 0.3,
    timers: sectionTimers,
    viewed: viewedSections,
    getId: (section) => section.dataset.sectionId,
    onView: (section) => sendEvent('section_view', {
      section_id: section.dataset.sectionId,
      section_name: section.dataset.sectionName,
      section_order: Number(section.dataset.sectionOrder)
    })
  });

  function ctaParameters(link) {
    const rawDestination = link.getAttribute('href') || link.href;
    const analyticsUrl = link.dataset.analyticsUrl || (rawDestination.startsWith('#') ? rawDestination : link.href);
    return {
      cta_id: link.dataset.ctaId,
      cta_location: link.dataset.ctaLocation,
      store_platform: link.dataset.storePlatform,
      destination_url: analyticsUrl
    };
  }

  const ctas = Array.from(document.querySelectorAll('a[data-track-cta]'));
  observeWithDwellTime(ctas, {
    ratio: 0.5,
    timers: ctaTimers,
    viewed: viewedCtas,
    getId: (link) => link.dataset.ctaId,
    onView: (link) => sendEvent('cta_view', ctaParameters(link))
  });

  document.addEventListener('click', (event) => {
    const link = event.target instanceof Element ? event.target.closest('a[data-track-cta]') : null;
    if (!link) return;

    const parameters = {
      ...ctaParameters(link),
      transport_type: 'beacon',
      link_url: link.dataset.analyticsUrl || link.href,
      link_text: link.getAttribute('aria-label') || link.textContent.trim().replace(/\s+/g, ' '),
      page_location: window.location.href
    };

    sendEvent('cta_click', parameters);

    const legacyEvents = [
      link.dataset.legacyEvent,
      link.dataset.event,
      link.dataset.storeEvent,
      link.dataset.extraLegacyEvent
    ].filter((eventName, index, events) => eventName && events.indexOf(eventName) === index);

    legacyEvents.forEach((eventName) => sendEvent(eventName, parameters));
  });

  const scrollThresholds = [25, 50, 75, 90, 100];
  let scrollFrameRequested = false;

  function measureScrollDepth() {
    scrollFrameRequested = false;
    const pageHeight = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
    const viewportBottom = window.scrollY + window.innerHeight;
    const scrollPercent = pageHeight - viewportBottom <= 2
      ? 100
      : (pageHeight > 0 ? Math.min(100, Math.floor((viewportBottom / pageHeight) * 100)) : 100);

    scrollThresholds.forEach((threshold) => {
      if (scrollPercent >= threshold && !reachedScrollDepths.has(threshold)) {
        reachedScrollDepths.add(threshold);
        sendEvent('scroll_depth', { scroll_percent: threshold });
      }
    });
  }

  function requestScrollMeasurement() {
    if (scrollFrameRequested) return;
    scrollFrameRequested = true;
    window.requestAnimationFrame(measureScrollDepth);
  }

  window.addEventListener('scroll', requestScrollMeasurement, { passive: true });
  window.addEventListener('resize', requestScrollMeasurement);
  window.addEventListener('load', requestScrollMeasurement);
  requestScrollMeasurement();

  document.querySelectorAll('details[data-track-faq]').forEach((details) => {
    details.addEventListener('click', (event) => {
      if (event.target instanceof Element && event.target.closest('summary')) details.dataset.analyticsInteraction = 'true';
    });

    details.addEventListener('toggle', () => {
      const wasUserInteraction = details.dataset.analyticsInteraction === 'true';
      delete details.dataset.analyticsInteraction;
      if (!details.open || !wasUserInteraction) return;

      sendEvent('faq_open', {
        section_id: 'faq',
        faq_id: details.dataset.faqId,
        faq_question: details.querySelector('summary')?.textContent.trim()
      });
    });
  });

  document.addEventListener('toybird:os-select', (event) => {
    const osName = event.detail?.os_name;
    if (osName !== 'windows' && osName !== 'macos') return;
    sendEvent('os_select', { os_name: osName });
  });

  document.querySelectorAll('video[data-track-video]').forEach((video) => {
    let started = false;
    let completed = false;
    const progressReached = new Set();
    const videoId = video.dataset.videoId;

    video.addEventListener('play', () => {
      if (started) return;
      started = true;
      sendEvent('video_start', { video_id: videoId });
    });

    video.addEventListener('timeupdate', () => {
      if (!Number.isFinite(video.duration) || video.duration <= 0) return;
      const percent = (video.currentTime / video.duration) * 100;
      [25, 50, 75].forEach((threshold) => {
        if (percent >= threshold && !progressReached.has(threshold)) {
          progressReached.add(threshold);
          sendEvent('video_progress', { video_id: videoId, video_percent: threshold });
        }
      });
    });

    video.addEventListener('ended', () => {
      if (completed) return;
      completed = true;
      sendEvent('video_complete', { video_id: videoId, video_percent: 100 });
    });
  });
})();
