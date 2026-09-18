#!/usr/bin/env python3
"""Normalize Open Graph social-sharing metadata for public LP pages.

Only <head> metadata is changed. Visible <body> content is preserved.
"""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

SITEMAP = Path("sitemap.xml")
BASE_URL = "https://lp.toybird.com/"

LOCALE_MAP = {
    "ja": "ja_JP",
    "en": "en_US",
    "de": "de_DE",
    "es": "es_ES",
    "fr": "fr_FR",
    "it": "it_IT",
    "ko": "ko_KR",
    "pt-br": "pt_BR",
    "zh-cn": "zh_CN",
    "zh-tw": "zh_TW",
}

IMAGE_OVERRIDES = {
    "index.html": "https://lp.toybird.com/assets/toybird-labs-og.png",
    "pointer-cue/index.html": "https://lp.toybird.com/pointer-cue/assets/og-image.png",
    "en/pointer-cue/index.html": "https://lp.toybird.com/pointer-cue/assets/og-image.png",
}

HTML_LANG_RE = re.compile(r'<html\\b[^>]*\\blang=["\\']([^"\\']+)["\\']', re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)


def meta_re(attr: str, key: str) -> re.Pattern[str]:
    return re.compile(
        rf'<meta\\b(?=[^>]*\\b{attr}=["\\']{re.escape(key)}["\\'])[^>]*>',
        re.I,
    )


def get_meta(text: str, attr: str, key: str) -> str:
    match = meta_re(attr, key).search(text)
    if not match:
        return ""
    content = re.search(r'\\bcontent=["\\']([^"\\']*)["\\']', match.group(0), re.I)
    return html.unescape(content.group(1)).strip() if content else ""


def set_meta(text: str, attr: str, key: str, value: str, anchor_key: str | None = None) -> str:
    tag = f'<meta {attr}="{key}" content="{html.escape(value, quote=True)}">'
    pattern = meta_re(attr, key)
    if pattern.search(text):
        return pattern.sub(tag, text, count=1)

    if anchor_key:
        anchor = meta_re("property", anchor_key).search(text)
        if anchor:
            return text[: anchor.end()] + "\n" + tag + text[anchor.end() :]

    return text.replace("</head>", tag + "\n</head>", 1)


def title_text(text: str) -> str:
    og_title = get_meta(text, "property", "og:title")
    if og_title:
        return og_title
    m = TITLE_RE.search(text)
    if m:
        return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    return "Toybird Labs"


def lang_code(text: str, path: Path) -> str:
    parts = path.parts
    if parts and parts[0] in LOCALE_MAP:
        return parts[0]
    m = HTML_LANG_RE.search(text)
    if m:
        raw = m.group(1).lower()
        if raw in LOCALE_MAP:
            return raw
        if raw.startswith("pt"):
            return "pt-br"
        if raw.startswith("zh-cn") or raw == "zh-hans":
            return "zh-cn"
        if raw.startswith("zh-tw") or raw == "zh-hant":
            return "zh-tw"
        return raw.split("-", 1)[0]
    return "en"


def sitemap_pages() -> list[Path]:
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(SITEMAP)
    pages: list[Path] = []
    for node in tree.findall(".//sm:loc", ns):
        url = (node.text or "").strip()
        if not url.startswith(BASE_URL):
            continue
        rel = urlparse(url).path.lstrip("/")
        path = Path(rel) / "index.html" if rel else Path("index.html")
        if path.exists():
            pages.append(path)
    return pages


def update(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original

    image_override = IMAGE_OVERRIDES.get(path.as_posix())
    if image_override:
        text = set_meta(text, "property", "og:image", image_override, anchor_key="og:url")

    locale_key = lang_code(text, path)
    locale = LOCALE_MAP.get(locale_key)
    if locale:
        text = set_meta(text, "property", "og:locale", locale, anchor_key="og:type")

    image = get_meta(text, "property", "og:image")
    if image:
        alt = title_text(text)
        if path == Path("index.html"):
            alt = "Toybird Labs apps, products, and practical AI projects"
        text = set_meta(text, "property", "og:image:alt", alt, anchor_key="og:image")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    pages = sitemap_pages()
    changed: list[str] = []
    for path in pages:
        if update(path):
            changed.append(path.as_posix())
    print(f"Processed {len(pages)} sitemap pages.")
    print(f"Changed {len(changed)} files.")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
