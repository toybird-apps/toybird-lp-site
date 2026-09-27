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
    .product-hunt-proof .appboard-badge{
      width:274px;
      min-height:0;
      flex:0 0 274px;
    }
    .product-hunt-proof .appboard-badge img{
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
    .runway-radar-proof{
      margin-top:7px;
      display:inline-flex;
      align-items:flex-start;
      gap:7px;
      max-width:100%;
      padding:0;
      background:transparent;
      border:0;
      box-shadow:none;
      text-align:left;
      color:#778398;
    }
    .runway-radar-proof:hover .runway-radar-copy strong{text-decoration:underline}
    .runway-radar-proof:focus-visible{
      outline:3px solid rgba(22,113,255,.16);
      outline-offset:4px;
    }
    .runway-radar-copy{
      display:flex;
      min-width:0;
      flex-direction:column;
      line-height:1.35;
    }
    .runway-radar-copy strong{
      color:#53637c;
      font-size:11px;
      font-weight:750;
    }
    .runway-radar-copy span{
      margin-top:2px;
      color:#8792a5;
      font-size:10px;
      font-weight:500;
    }
    .runway-radar-arrow{
      flex:0 0 auto;
      margin-top:0;
      color:#8792a5;
      font-size:12px;
      font-weight:700;
      line-height:1.2;
    }
    @media(max-width:900px){
      .six-colors-proof,.runway-radar-proof{margin-left:auto;margin-right:auto}
    }
    @media(max-width:600px){
      .product-hunt-proof .appboard-badge{flex-basis:274px}
    }
  `;
  document.head.appendChild(style);

  const language = (document.body.dataset.pageLanguage || document.documentElement.lang || 'en').toLowerCase();
  const isJapanese = language.startsWith('ja');

  let sixColorsLink = document.querySelector('.six-colors-proof');
  if (!sixColorsLink) {
    sixColorsLink = document.createElement('a');
    sixColorsLink.className = 'six-colors-proof';
    sixColorsLink.href = 'https://sixcolors.com/post/2026/09/app-report-ai-to-the-rescue-no-really/';
    sixColorsLink.target = '_blank';
    sixColorsLink.rel = 'noopener noreferrer';
    sixColorsLink.setAttribute('data-track-cta', '');
    sixColorsLink.dataset.ctaId = 'six_colors_feature';
    sixColorsLink.dataset.ctaLocation = 'hero';
    sixColorsLink.setAttribute(
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

    sixColorsLink.append(copy, arrow);
    launchProof.insertAdjacentElement('afterend', sixColorsLink);
  }

  if (document.querySelector('.runway-radar-proof')) return;

  const runwayLink = document.createElement('a');
  runwayLink.className = 'runway-radar-proof';
  runwayLink.href = 'https://launchfree.io/listings/pocket-screen.html';
  runwayLink.target = '_blank';
  runwayLink.rel = 'noopener noreferrer';
  runwayLink.setAttribute('data-track-cta', '');
  runwayLink.dataset.ctaId = 'runway_radar_feature';
  runwayLink.dataset.ctaLocation = 'hero';
  runwayLink.setAttribute(
    'aria-label',
    isJapanese
      ? 'The Runway RadarでPocket Screenが411件の公開週で2位になった掲載ページを見る'
      : 'View Pocket Screen on The Runway after placing #2 in a 411-launch week'
  );

  const runwayCopy = document.createElement('span');
  runwayCopy.className = 'runway-radar-copy';

  const runwayHeadline = document.createElement('strong');
  runwayHeadline.textContent = 'The Runway Radar — #2 Weekly Launch';

  const runwayDetail = document.createElement('span');
  runwayDetail.textContent = '#2 in a 411-launch week';

  runwayCopy.append(runwayHeadline, runwayDetail);

  const runwayArrow = document.createElement('span');
  runwayArrow.className = 'runway-radar-arrow';
  runwayArrow.setAttribute('aria-hidden', 'true');
  runwayArrow.textContent = '↗';

  runwayLink.append(runwayCopy, runwayArrow);
  sixColorsLink.insertAdjacentElement('afterend', runwayLink);

  const smolTextLink = document.createElement('a');
  smolTextLink.className = 'runway-radar-proof smol-startup-proof';
  smolTextLink.href = 'https://smolstartup.com/projects/pocket-screen';
  smolTextLink.target = '_blank';
  smolTextLink.rel = 'noopener noreferrer';
  smolTextLink.setAttribute('data-track-cta', '');
  smolTextLink.dataset.ctaId = 'smol_startup_feature';
  smolTextLink.dataset.ctaLocation = 'hero';
  smolTextLink.setAttribute(
    'aria-label',
    isJapanese
      ? 'Smol StartupでPocket ScreenがProject of the Day 3位になった掲載ページを見る'
      : 'View Pocket Screen on Smol Startup after placing #3 Project of the Day'
  );

  const smolCopy = document.createElement('span');
  smolCopy.className = 'runway-radar-copy';

  const smolHeadline = document.createElement('strong');
  smolHeadline.textContent = 'Smol Startup — #3 Project of the Day';
  smolCopy.append(smolHeadline);

  const smolArrow = document.createElement('span');
  smolArrow.className = 'runway-radar-arrow';
  smolArrow.setAttribute('aria-hidden', 'true');
  smolArrow.textContent = '↗';

  smolTextLink.append(smolCopy, smolArrow);
  runwayLink.insertAdjacentElement('afterend', smolTextLink);
})();
