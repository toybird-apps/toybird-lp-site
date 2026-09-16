from __future__ import annotations

from pathlib import Path
import json
import re
import shutil
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://lp.toybird.com"

SLUGS = [
    "교재-사진-빈칸-복습",
    "내신-수능-자격증-내-교재",
]

SHARED_IMAGE_RE = re.compile(
    r"https://lp\.toybird\.com/shared/ai-study-sheet-v3/article-[0-9a-f]+\.png"
)
SOFTWARE_VERSION_RE = re.compile(
    r',?\s*"softwareVersion"\s*:\s*"3\.0\.0"\s*,?', re.IGNORECASE
)
VERSION_RELEASE_RE = re.compile(
    r"\s*(?:[·•—–|-]\s*)?v3\.0\.0(?:\s*출시)?\.?",
    re.IGNORECASE,
)
JSONLD_RE = re.compile(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


def clean_version_copy(text: str) -> str:
    text = SOFTWARE_VERSION_RE.sub(
        lambda m: ","
        if m.group(0).strip().startswith(",")
        and m.group(0).strip().endswith(",")
        else "",
        text,
    )
    text = re.sub(r",\s*([}\]])", r"\1", text)
    text = re.sub(r"([\[{])\s*,", r"\1", text)
    text = VERSION_RELEASE_RE.sub("", text)
    text = re.sub(r"[ \t]+([,.。])", r"\1", text)
    text = re.sub(r" {2,}", " ", text)
    return text


def validate_jsonld(text: str, page: Path) -> None:
    blocks = JSONLD_RE.findall(text)
    if not blocks:
        raise RuntimeError(f"{page.relative_to(ROOT)}: JSON-LD block missing")
    for raw in blocks:
        json.loads(raw)


def migrate(slug: str) -> list[Path]:
    canonical_dir = ROOT / "ko" / "blog" / slug
    page = canonical_dir / "index.html"
    if not page.exists():
        raise RuntimeError(f"Missing Korean canonical page: {page.relative_to(ROOT)}")

    nfd_slug = unicodedata.normalize("NFD", slug)
    source_asset = (
        ROOT
        / "ko"
        / "blog"
        / nfd_slug
        / "assets"
        / f"{nfd_slug}-og.png"
    )
    if not source_asset.exists():
        raise RuntimeError(
            f"Missing cleaned Korean alias visual: {source_asset.relative_to(ROOT)}"
        )

    asset_dir = canonical_dir / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    target_asset = asset_dir / f"{slug}-og.png"
    shutil.copyfile(source_asset, target_asset)

    text = page.read_text(encoding="utf-8")
    text = clean_version_copy(text)

    image_url = f"{SITE}/ko/blog/{slug}/assets/{slug}-og.png"
    text, replaced = SHARED_IMAGE_RE.subn(image_url, text)
    if replaced < 4:
        raise RuntimeError(
            f"{page.relative_to(ROOT)}: expected shared image in metadata/schema/hero, replaced {replaced} references"
        )

    if "v3.0.0" in text:
        raise RuntimeError(f"{page.relative_to(ROOT)}: v3.0.0 remains")
    if re.search(r'"softwareVersion"\s*:', text):
        raise RuntimeError(f"{page.relative_to(ROOT)}: softwareVersion remains")
    if "shared/ai-study-sheet-v3/article-" in text:
        raise RuntimeError(f"{page.relative_to(ROOT)}: shared legacy article visual remains")

    expected_tokens = [
        f'<meta content="{image_url}" property="og:image"/>',
        f'<meta content="{image_url}" name="twitter:image"/>',
        f'src="{image_url}"',
    ]
    for token in expected_tokens:
        if token not in text:
            raise RuntimeError(f"{page.relative_to(ROOT)}: missing expected image reference {token}")
    if f'"image": "{image_url}"' not in text and f'"image":"{image_url}"' not in text:
        raise RuntimeError(f"{page.relative_to(ROOT)}: JSON-LD image was not updated")

    validate_jsonld(text, page)
    page.write_text(text, encoding="utf-8")
    return [page, target_asset]


def main() -> None:
    changed: list[Path] = []
    for slug in SLUGS:
        changed.extend(migrate(slug))

    print("Fixed Korean canonical AI Study Sheet articles:")
    for path in changed:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
