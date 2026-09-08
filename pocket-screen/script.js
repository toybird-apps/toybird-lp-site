const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

(function addSixColorsProof() {
  const existing = document.querySelector('.six-colors-proof');
  const launchProof = document.querySelector('.product-hunt-proof');
  if (existing || !launchProof) return;

  const style = document.createElement('style');
  style.textContent = `
    .six-colors-proof{
      margin-top:12px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:14px;
      width:min(100%,370px);
      min-height:78px;
      padding:11px 13px 11px 14px;
      background:rgba(255,255,255,.92);
      border:1px solid #dfe5ee;
      border-radius:14px;
      box-shadow:0 10px 26px rgba(35,54,88,.08);
      text-align:left;
      transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease;
    }
    .six-colors-proof:hover{
      transform:translateY(-2px);
      border-color:#b8c5d8;
      box-shadow:0 14px 32px rgba(35,54,88,.13);
    }
    .six-colors-proof:focus-visible{
      outline:3px solid rgba(22,113,255,.22);
      outline-offset:3px;
    }
    .six-colors-copy{
      display:flex;
      min-width:0;
      flex:1;
      flex-direction:column;
      line-height:1.25;
    }
    .six-colors-copy small{
      color:#6f7b8e;
      font-size:9px;
      font-weight:850;
      letter-spacing:.13em;
    }
    .six-colors-copy strong{
      margin-top:4px;
      color:#29364a;
      font-size:13px;
      font-weight:800;
    }
    .six-colors-copy q{
      margin-top:5px;
      color:#61708a;
      font-size:11px;
      font-style:normal;
      quotes:none;
    }
    .six-colors-arrow{
      flex:0 0 auto;
      color:#1671ff;
      font-size:18px;
      font-weight:800;
      line-height:1;
    }
    @media(max-width:900px){
      .six-colors-proof{margin-left:auto;margin-right:auto}
    }
    @media(prefers-reduced-motion:reduce){
      .six-colors-proof{transition:none}
    }
  `;
  document.head.appendChild(style);

  const language = (document.body.dataset.pageLanguage || document.documentElement.lang || 'en').toLowerCase();
  const isJapanese = language.startsWith('ja');

  const card = document.createElement('a');
  card.className = 'six-colors-proof';
  card.href = 'https://sixcolors.com/post/2026/09/app-report-ai-to-the-rescue-no-really/';
  card.target = '_blank';
  card.rel = 'noopener noreferrer';
  card.setAttribute('data-track-cta', '');
  card.dataset.ctaId = 'six_colors_feature';
  card.dataset.ctaLocation = 'hero';
  card.setAttribute(
    'aria-label',
    isJapanese
      ? 'Six ColorsのApp ReportでPocket Screenが紹介された記事を読む'
      : 'Read the Six Colors App Report featuring Pocket Screen'
  );

  const copy = document.createElement('span');
  copy.className = 'six-colors-copy';

  const label = document.createElement('small');
  label.textContent = 'SIX COLORS · APP REPORT';

  const headline = document.createElement('strong');
  headline.textContent = isJapanese
    ? 'Six Colors App Reportで紹介'
    : 'Featured in Six Colors’ App Report';

  const quote = document.createElement('q');
  quote.textContent = '“picture-in-picture feature, but for productivity.”';

  copy.append(label, headline, quote);

  const arrow = document.createElement('span');
  arrow.className = 'six-colors-arrow';
  arrow.setAttribute('aria-hidden', 'true');
  arrow.textContent = '↗';

  card.append(copy, arrow);
  launchProof.insertAdjacentElement('afterend', card);
})();
