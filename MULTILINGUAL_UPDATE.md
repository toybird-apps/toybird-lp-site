# Multilingual routing

- Existing Japanese LP URLs remain at their established root paths.
- English LPs use `/en/<app>/`.
- AI Study Sheet also has full `/ko/ai-memorize-sheet/` and `/zh-cn/ai-memorize-sheet/` LPs.
- KoeSub's dedicated LP is Japanese; its English product information is at https://labs.toybird.com/apps/koesub/.
- Other language aliases may redirect to English rather than duplicate unsupported translations.
- Full translated blog collections have their own language paths.
- Preserve canonical and reciprocal hreflang links for actual translated pages. Do not advertise a redirect alias as an independent translation.
- Existing language switches can store `toybird_language` in localStorage; automatic-selection information can use sessionStorage.
- The shared locale script sends language-aware events when Google Analytics is available.
- The sitemap lists canonical content, not language-redirect aliases.
- When refreshing UI images, use an existing matching-language asset when available. Do not label English UI as a localized screenshot.

Historical product-image folders may remain for old links or noindex media previews. Current LPs and study articles should reference the appropriate current assets.
