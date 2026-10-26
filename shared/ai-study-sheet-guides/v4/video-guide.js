(() => {
  const guide = document.querySelector('.study-video-guide');
  if (!guide) return;
  const video = guide.querySelector('video');
  const buttons = [...guide.querySelectorAll('[data-guide-seek]')];
  const error = guide.querySelector('.guide-error');
  const updateCurrent = () => {
    let current = buttons[0];
    buttons.forEach((button) => {
      if (Number(button.dataset.guideSeek) <= video.currentTime + 0.1) current = button;
    });
    buttons.forEach((button) => {
      if (button === current) button.setAttribute('aria-current', 'true');
      else button.removeAttribute('aria-current');
    });
  };
  buttons.forEach((button) => button.addEventListener('click', () => {
    const start = Number(button.dataset.guideSeek);
    if (video.readyState < 1) {
      video.addEventListener('loadedmetadata', () => { video.currentTime = start; }, { once: true });
    } else {
      video.currentTime = start;
    }
    // Invoke play during the click gesture so mobile browsers can play with sound.
    const playback = video.play();
    if (playback) playback.catch(() => { error.hidden = false; });
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (window.matchMedia('(max-width: 760px)').matches) {
      video.scrollIntoView({ behavior: reduceMotion ? 'instant' : 'smooth', block: 'center' });
    }
  }));
  video.addEventListener('timeupdate', updateCurrent);
  video.addEventListener('loadedmetadata', updateCurrent);
  video.addEventListener('playing', () => { error.hidden = true; });
  video.addEventListener('error', () => { error.hidden = false; });
  updateCurrent();
})();
