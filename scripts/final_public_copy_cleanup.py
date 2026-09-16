from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
JSONLD_RE = re.compile(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
VERSION_3_RE = re.compile(r'\b(?:v(?:ersion)?\s*)?3\.0\.0\b', re.IGNORECASE)

INTERNAL_MARKERS = [
    "Editorial method",
    "First-party testing · Official sources · Practical limitations",
    "First-party product testing is separated from statements supported by official sources",
    "Hands-on checks by Toybird Labs · official documentation referenced",
    "Toybird Labsによる実機確認・公式資料参照",
    "実機で確認した内容と、公式資料で確認した事実を区別して掲載しています",
    "Toybird Labs自社アプリの開発・検証で得た一次情報",
]


def validate_jsonld(text: str, label: str) -> None:
    for raw in JSONLD_RE.findall(text):
        json.loads(raw)


def update_root_portfolio() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        'alt="AI Study Sheet v3.0.0"',
        'alt="AI Study Sheet app icon"',
    )
    text = text.replace(
        "AI Study Sheet v3.0.0 is released. Turn photos and PDFs into study sheets on your device, resume PDF imports, and use pre-marked materials.",
        "Turn photos and PDFs into study sheets on your device, resume PDF imports, and use pre-marked materials.",
    )
    if text == original:
        raise RuntimeError("Root portfolio cleanup produced no change")
    if VERSION_3_RE.search(text):
        raise RuntimeError("Root portfolio still contains AI Study Sheet 3.0.0 messaging")
    validate_jsonld(text, "index.html")
    path.write_text(text, encoding="utf-8")


def update_english_product_page() -> None:
    path = ROOT / "en" / "ai-memorize-sheet" / "index.html"
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        "Version 3.0.0 app screens with sample study materials.",
        "App screens with sample study materials.",
    )
    if text == original:
        raise RuntimeError("English AI Study Sheet gallery cleanup produced no change")
    if VERSION_3_RE.search(text):
        raise RuntimeError("English AI Study Sheet page still contains 3.0.0 messaging")
    validate_jsonld(text, "en/ai-memorize-sheet/index.html")
    path.write_text(text, encoding="utf-8")


def validate_public_html() -> None:
    errors: list[str] = []
    html_files = sorted(
        path for path in ROOT.rglob("*.html")
        if ".git" not in path.parts and ".github" not in path.parts
    )
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for marker in INTERNAL_MARKERS:
            if marker in text:
                errors.append(f"{rel}: internal editorial marker remains: {marker}")
        if VERSION_3_RE.search(text):
            errors.append(f"{rel}: public 3.0.0 version messaging remains")
        try:
            validate_jsonld(text, str(rel))
        except Exception as exc:
            errors.append(f"{rel}: invalid JSON-LD: {exc}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(html_files)} public HTML files: no internal markers or 3.0.0 messaging remain; JSON-LD parses.")


def main() -> None:
    update_root_portfolio()
    update_english_product_page()
    validate_public_html()
    print("Final public copy cleanup completed.")


if __name__ == "__main__":
    main()
