from __future__ import annotations

from pathlib import Path
import json
import re
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_REF = "9142bf066ce88d702c31019c689296658375c361"
SHARED_DIR = ROOT / "shared" / "ai-study-sheet-v3"

LATIN_FONT = Path("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf")
CJK_FONT = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")

JSONLD_RE = re.compile(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
SOFTWARE_VERSION_RE = re.compile(
    r',?\s*"softwareVersion"\s*:\s*"3\.0\.0"\s*,?', re.IGNORECASE
)
SHARED_ARTICLE_RE = re.compile(
    r"https://lp\.toybird\.com/shared/ai-study-sheet-v3/(article-[0-9a-f]+\.png)"
)


def clean_json_commas(text: str) -> str:
    text = re.sub(r",\s*([}\]])", r"\1", text)
    text = re.sub(r"([\[{])\s*,", r"\1", text)
    return text


def validate_jsonld(text: str, label: str) -> None:
    blocks = JSONLD_RE.findall(text)
    if not blocks:
        raise RuntimeError(f"{label}: JSON-LD block missing")
    for raw in blocks:
        json.loads(raw)


def cleanup_page(path: Path, locale: str) -> None:
    text = path.read_text(encoding="utf-8")

    if locale == "ja":
        replacements = {
            "AI赤シート v3.0.0 — 写真・PDFから赤シート学習 | Toybird Labs":
                "AI赤シート — 写真・PDFから赤シート学習 | Toybird Labs",
            '<div class="eyebrow">v3.0.0 リリース済み · iPhone・iPad対応</div>':
                '<div class="eyebrow">iPhone・iPad対応 · 写真・PDF・カメラから取り込み</div>',
            'alt="AI赤シート v3.0.0 作成画面"':
                'alt="AI赤シート 作成画面"',
            '<div><strong>v3.0.0</strong><span>リリース済み</span></div>':
                '<div><strong>写真・PDF</strong><span>教材をそのまま取り込み</span></div>',
            'data-section-id="version_3" data-section-name="Version 3.0.0" data-track-section="" id="version-3"':
                'data-section-id="flexible_setup" data-section-name="Flexible Setup" data-track-section="" id="flexible-setup"',
            '<p class="section-kicker">v3.0.0 リリース済み</p>':
                '<p class="section-kicker">取り込みから復習まで</p>',
        }
    else:
        replacements = {
            "AI Study Sheet v3.0.0 — Photos and PDFs for active recall | Toybird Labs":
                "AI Study Sheet — Photos and PDFs for active recall | Toybird Labs",
            '<div class="eyebrow">v3.0.0 Released · For iPhone and iPad</div>':
                '<div class="eyebrow">For iPhone and iPad · Camera, photos, and PDFs</div>',
            'alt="AI Study Sheet v3.0.0 creation screen"':
                'alt="AI Study Sheet creation screen"',
            '<div><strong>v3.0.0</strong><span>Released</span></div>':
                '<div><strong>Photos &amp; PDFs</strong><span>Import your own material</span></div>',
            'data-section-id="version_3" data-section-name="Version 3.0.0" data-track-section="" id="version-3"':
                'data-section-id="flexible_setup" data-section-name="Flexible Setup" data-track-section="" id="flexible-setup"',
            '<p class="section-kicker">v3.0.0 Released</p>':
                '<p class="section-kicker">From import to review</p>',
        }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = SOFTWARE_VERSION_RE.sub(
        lambda m: ","
        if m.group(0).strip().startswith(",") and m.group(0).strip().endswith(",")
        else "",
        text,
    )
    text = clean_json_commas(text)

    if "v3.0.0" in text:
        occurrences = [m.start() for m in re.finditer(r"v3\.0\.0", text, re.IGNORECASE)]
        raise RuntimeError(f"{path.relative_to(ROOT)}: v3.0.0 remains at {occurrences}")
    if re.search(r'"softwareVersion"\s*:', text):
        raise RuntimeError(f"{path.relative_to(ROOT)}: softwareVersion remains")

    validate_jsonld(text, str(path.relative_to(ROOT)))
    path.write_text(text, encoding="utf-8")


def cleanup_overview_image(path: Path, label: str, locale: str) -> None:
    with Image.open(path) as src:
        image = src.convert("RGB")
    if image.size != (1200, 630):
        raise RuntimeError(f"Unexpected overview image size: {path.relative_to(ROOT)} {image.size}")

    background = image.getpixel((400, 250))
    draw = ImageDraw.Draw(image)
    draw.rectangle((42, 235, 360, 282), fill=background)
    font_path = CJK_FONT if locale == "ja" else LATIN_FONT
    if not font_path.exists():
        raise RuntimeError(f"Missing font: {font_path}")
    font = ImageFont.truetype(str(font_path), 22 if locale == "ja" else 21)
    draw.text((50, 248), label, font=font, fill=(183, 57, 54))
    image.save(path, format="PNG", optimize=True)


def historical_article_mapping() -> dict[str, Path]:
    names = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", HISTORICAL_REF],
        text=True,
    ).splitlines()
    mapping: dict[str, Path] = {}
    for name in names:
        if not name.endswith("/index.html") or "/blog/" not in f"/{name}":
            continue
        try:
            text = subprocess.check_output(
                ["git", "show", f"{HISTORICAL_REF}:{name}"],
                text=True,
            )
        except subprocess.CalledProcessError:
            continue
        if "app-id=6782023263" not in text:
            continue
        match = SHARED_ARTICLE_RE.search(text)
        if not match:
            continue
        shared_name = match.group(1)
        page_dir = ROOT / Path(name).parent
        slug = page_dir.name
        target = page_dir / "assets" / f"{slug}-og.png"
        if not target.exists():
            raise RuntimeError(
                f"Current cleaned local visual missing for historical {shared_name}: {target.relative_to(ROOT)}"
            )
        if shared_name in mapping and mapping[shared_name] != target:
            raise RuntimeError(f"Duplicate historical mapping for {shared_name}")
        mapping[shared_name] = target

    if len(mapping) != 38:
        raise RuntimeError(f"Expected 38 historical shared article visuals, found {len(mapping)}")
    return mapping


def replace_legacy_shared_article_visuals() -> None:
    mapping = historical_article_mapping()
    for shared_name, target in mapping.items():
        destination = SHARED_DIR / shared_name
        if not destination.exists():
            raise RuntimeError(f"Missing legacy shared visual: {destination.relative_to(ROOT)}")
        shutil.copyfile(target, destination)


def validate_shared_visuals() -> None:
    mapping = historical_article_mapping()
    for shared_name, target in mapping.items():
        destination = SHARED_DIR / shared_name
        if destination.read_bytes() != target.read_bytes():
            raise RuntimeError(f"Legacy URL was not replaced exactly: {shared_name}")
        with Image.open(destination) as im:
            if im.size != (1200, 630):
                raise RuntimeError(f"Unexpected legacy visual size: {shared_name} {im.size}")

    for name in ("ja-overview.png", "en-overview.png"):
        with Image.open(SHARED_DIR / name) as im:
            if im.size != (1200, 630):
                raise RuntimeError(f"Unexpected overview size after cleanup: {name} {im.size}")


def main() -> None:
    cleanup_page(ROOT / "ai-memorize-sheet" / "index.html", "ja")
    cleanup_page(ROOT / "en" / "ai-memorize-sheet" / "index.html", "en")
    cleanup_overview_image(SHARED_DIR / "ja-overview.png", "iPhone・iPad対応", "ja")
    cleanup_overview_image(SHARED_DIR / "en-overview.png", "For iPhone and iPad", "en")
    replace_legacy_shared_article_visuals()
    validate_shared_visuals()
    print("Cleaned AI Study Sheet public version/release messaging from product pages and legacy public visuals.")


if __name__ == "__main__":
    main()
