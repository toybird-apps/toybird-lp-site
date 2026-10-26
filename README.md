# Toybird Labs portfolio and landing pages

Public site: https://lp.toybird.com/  
Repository: `toybird-apps/toybird-lp-site`  
Publishing branch: `main` (GitHub Pages)

## Published content

- `index.html`: English portfolio homepage, indexed and canonical at the domain root.
- `ai-memorize-sheet/`: Japanese AI Study Sheet LP. English, Korean, and Simplified Chinese versions are under `en/`, `ko/`, and `zh-cn/`.
- `pocket-screen/`, `prompt-ready/`, `pointer-cue/`: Japanese LPs, with English versions under `en/`.
- `koesub/`: Japanese KoeSub LP.
- `blog/`: Japanese articles; translated article collections are under their language directories.
- Other product-language URLs can be intentional redirects to a supported language. Do not count them as independently translated product pages.
- `shared/`: shared locale code, styles, badges, and versioned media assets.
- `sitemap.xml`: canonical, indexable content. Redirects, verification files, and noindex legacy media previews are excluded.

Product specifications, support pages, and privacy policies live at https://labs.toybird.com/ in the separate `toybird-apps-site` repository.

## Editing and release checks

- Preserve the current layout, fonts, established URLs, language choices, and analytics events.
- Lead with the user’s task and product value; keep detailed operation and troubleshooting on the support pages.
- Verify that an app version is publicly released before promoting its features.
- Update text, social metadata, JSON-LD, screenshots, related articles, and sitemap dates together when they are affected.
- Keep original article publication dates; change modification dates only for relevant edits.
- Check internal links, image paths, language targets, JSON-LD, desktop/mobile layout, and store destinations.
- Commit the reviewed update to `main`, then verify the actual GitHub Pages deployment.

Historical `UPDATE_NOTES` and versioned asset folders describe earlier releases. Existing one-off workflows must be reviewed before rerunning; they may contain old copy.

## Analytics and privacy

Google Analytics measurement ID: `G-MTD9Z8S7QG`. See `GA4_SETUP_NOTES.md` for event notes. Website privacy information is at https://labs.toybird.com/privacy/#websites.

## Pointer Cue distribution

The current macOS product is distributed through the Mac App Store. The existing Windows edition remains available through Microsoft Store, with different features and no ongoing new-feature development. Do not reintroduce retired direct binary downloads.
