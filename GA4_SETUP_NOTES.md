# GA4 implementation notes

Measurement ID: `G-MTD9Z8S7QG`.

Google Analytics is embedded in the portfolio homepage, active product LPs, and published blog pages. Redirect aliases are not separate content pages. Preserve existing instrumentation when editing content.

## Existing events

Event availability varies by page and platform:

- `app_store_click`
- `microsoft_store_click`
- `store_click`
- `os_tab_select`
- `comparison_view`
- `language_switch`
- `language_auto_selected`

Parameters can include app name, store platform, link URL/text, page language, page location, and target language. Read the page's actual script before changing event names or assuming every page emits every event.

Retired direct-binary trial download events are not a current Pointer Cue acquisition path.

## Verification

After publication, verify that existing CTA handlers and language switches still work. A live GA4 Realtime check requires authorized access to the analytics account; a successful page deployment alone does not prove event ingestion.

Website privacy information: https://labs.toybird.com/privacy/#websites.
