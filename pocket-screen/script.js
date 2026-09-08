const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

(function refreshHeroProofs() {
  const launchProof = document.querySelector('.product-hunt-proof');
  if (!launchProof) return;

  const style = document.createElement('style');
  style.textContent = `
    .product-hunt-proof .smol-startup-badge{
      width:274px;
      min-height:0;
      flex:0 0 274px;
    }
    .product-hunt-proof .smol-startup-badge img{
      display:block;
      width:274px;
      height:auto;
      max-height:none;
    }
    .six-colors-proof{
      margin-top:16px;
      display:inline-flex;
      align-items:flex-start;
      gap:8px;
      max-width:100%;
      padding:0;
      background:transparent;
      border:0;
      border-radius:0;
      box-shadow:none;
      text-align:left;
      color:#29364a;
    }
    .six-colors-proof:hover .six-colors-copy strong{text-decoration:underline}
    .six-colors-proof:focus-visible{
      outline:3px solid rgba(22,113,255,.22);
      outline-offset:5px;
    }
    .six-colors-copy{
      display:flex;
      min-width:0;
      flex-direction:column;
      line-height:1.35;
    }
    .six-colors-copy strong{
      color:#29364a;
      font-size:13px;
      font-weight:800;
    }
    .six-colors-copy q{
      margin-top:3px;
      color:#61708a;
      font-size:11px;
      font-style:normal;
      quotes:none;
    }
    .six-colors-arrow{
      flex:0 0 auto;
      margin-top:1px;
      color:#1671ff;
      font-size:14px;
      font-weight:800;
      line-height:1.2;
    }
    @media(max-width:900px){
      .six-colors-proof{margin-left:auto;margin-right:auto}
    }
    @media(max-width:600px){
      .product-hunt-proof .smol-startup-badge{flex-basis:274px}
    }
  `;
  document.head.appendChild(style);

  const smolBadge = launchProof.querySelector('.smol-startup-badge');
  const smolImage = smolBadge && smolBadge.querySelector('img');
  if (smolBadge && smolImage) {
    smolBadge.href = 'https://smolstartup.com/projects/pocket-screen';
    smolBadge.title = 'Smol Startup Top 3 Daily Winner';
    smolImage.src = 'https://smolstartup.com/smolstartup/images/badges/top3-light.svg';
    smolImage.alt = 'Smol Startup Top 3 Daily Winner';
  }

  if (document.querySelector('.six-colors-proof')) return;

  const language = (document.body.dataset.pageLanguage || document.documentElement.lang || 'en').toLowerCase();
  const isJapanese = language.startsWith('ja');

  const link = document.createElement('a');
  link.className = 'six-colors-proof';
  link.href = 'https://sixcolors.com/post/2026/09/app-report-ai-to-the-rescue-no-really/';
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.setAttribute('data-track-cta', '');
  link.dataset.ctaId = 'six_colors_feature';
  link.dataset.ctaLocation = 'hero';
  link.setAttribute(
    'aria-label',
    isJapanese
      ? 'Six ColorsのApp ReportでPocket Screenが紹介された記事を読む'
      : 'Read the Six Colors App Report featuring Pocket Screen'
  );

  const copy = document.createElement('span');
  copy.className = 'six-colors-copy';

  const headline = document.createElement('strong');
  headline.textContent = isJapanese
    ? 'Six Colors App Reportで紹介'
    : 'Featured in Six Colors’ App Report';

  const quote = document.createElement('q');
  quote.textContent = '“picture-in-picture feature, but for productivity.”';

  copy.append(headline, quote);

  const arrow = document.createElement('span');
  arrow.className = 'six-colors-arrow';
  arrow.setAttribute('aria-hidden', 'true');
  arrow.textContent = '↗';

  link.append(copy, arrow);
  launchProof.insertAdjacentElement('afterend', link);
})();
