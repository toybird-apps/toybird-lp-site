# GA4 implementation notes

Measurement ID: `G-MTD9Z8S7QG`

Implemented on:

- `/index.html`
- `/ai-memorize-sheet/index.html`
- `/pocket-screen/index.html`
- `/prompt-ready/index.html`
- `/pointer-cue/index.html`

Pointer Cue custom events:

- `microsoft_store_click`
- `app_store_click`
- `trial_download_click`
- `os_tab_select`
- `comparison_view`

Common parameters include:

- `app_name`
- `store_platform`
- `link_url`
- `link_text`
- `page_location`

After publishing, open GA4 Realtime and confirm `page_view` and each CTA event.
