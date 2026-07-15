# GA4 implementation notes

Measurement ID: `G-MTD9Z8S7QG`

Implemented on:

- `/index.html`
- `/ai-memorize-sheet/index.html`
- `/pocket-screen/index.html`

In addition to GA4 enhanced measurement, App Store links send a custom event:

- Event name: `app_store_click`
- Parameters: `app_name`, `link_url`, `link_text`, `page_location`

After publishing, open GA4 Realtime and click an App Store button to confirm both `page_view` and `app_store_click`.
