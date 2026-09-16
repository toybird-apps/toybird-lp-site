from __future__ import annotations

from pathlib import Path
import json
import re
import shutil

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
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

LEGACY_ARTICLE_TARGETS = {
    "article-0a775d639ebe1bad.png": "blog/school-print-smartphone-memorization/assets/school-print-smartphone-memorization-og.png",
    "article-0eaa5176c92ebbad.png": "blog/gyoseishoshi-memorization-study/assets/gyoseishoshi-memorization-study-og.png",
    "article-111060dec43a82e2.png": "blog/junior-high-regular-test-print-study/assets/junior-high-regular-test-print-study-og.png",
    "article-25b2bb9ea7a42c90.png": "blog/takken-memorization-study/assets/takken-memorization-study-og.png",
    "article-2798faf5d52282ef.png": "blog/red-sheet-vs-flashcards/assets/red-sheet-vs-flashcards-og.png",
    "article-3286fd86e25cf51c.png": "ko/blog/내신-수능-자격증-내-교재/assets/내신-수능-자격증-내-교재-og.png",
    "article-3a2a978d3bd6804f.png": "en/blog/worksheets-without-rewriting/assets/worksheets-without-rewriting-og.png",
    "article-3c797846b63df2a9.png": "blog/sharoshi-memorization-study/assets/sharoshi-memorization-study-og.png",
    "article-4cbc75ad69f4904b.png": "blog/high-school-entrance-exam-memorization/assets/high-school-entrance-exam-memorization-og.png",
    "article-4f0be911769ad5af.png": "de/blog/lernzettel-arbeitsblaetter-aktiv-abfragen/assets/lernzettel-arbeitsblaetter-aktiv-abfragen-og.png",
    "article-5c9c50ae9734d859.png": "it/blog/maturita-universita-concorsi-materiali-propri/assets/maturita-universita-concorsi-materiali-propri-og.png",
    "article-5ff322fce341a3e3.png": "blog/pdf-material-iphone-memorization/assets/pdf-material-iphone-memorization-og.png",
    "article-631c0eeb0e1e744b.png": "blog/fp-memorization-study/assets/fp-memorization-study-og.png",
    "article-636cadec278c1d2f.png": "ko/blog/내신-수능-자격증-내-교재/assets/내신-수능-자격증-내-교재-og.png",
    "article-651587365e0a6492.png": "blog/it-passport-memorization-study/assets/it-passport-memorization-study-og.png",
    "article-73fe17a950c133c2.png": "blog/qualification-exam-smartphone-memorization/assets/qualification-exam-smartphone-memorization-og.png",
    "article-77cb66edb24668f3.png": "zh-tw/blog/課本講義-遮罩自我測驗/assets/課本講義-遮罩自我測驗-og.png",
    "article-7ae4e087abffff88.png": "zh-tw/blog/會考學測國考-自己的pdf/assets/會考學測國考-自己的pdf-og.png",
    "article-7c023948dd65f8cc.png": "zh-cn/blog/高考考研-自己的讲义-pdf/assets/高考考研-自己的讲义-pdf-og.png",
    "article-83290ce5ce6df7e9.png": "blog/high-school-regular-test-print-study/assets/high-school-regular-test-print-study-og.png",
    "article-8da8101a65d991b7.png": "es/blog/fotos-apuntes-repaso-activo/assets/fotos-apuntes-repaso-activo-og.png",
    "article-8f12c54afd02b968.png": "blog/iphone-red-sheet-study/assets/iphone-red-sheet-study-og.png",
    "article-9042fad6e36ea37e.png": "de/blog/abitur-ausbildung-studium-eigene-unterlagen/assets/abitur-ausbildung-studium-eigene-unterlagen-og.png",
    "article-ae5d607d00f21194.png": "fr/blog/photo-cours-revision-active/assets/photo-cours-revision-active-og.png",
    "article-afa2026348e9e749.png": "blog/university-entrance-exam-memorization/assets/university-entrance-exam-memorization-og.png",
    "article-b76db4041fd77423.png": "zh-cn/blog/教材照片-遮挡自测/assets/教材照片-遮挡自测-og.png",
    "article-b9d8a60dac3fae82.png": "ko/blog/교재-사진-빈칸-복습/assets/교재-사진-빈칸-복습-og.png",
    "article-bc204e02026f40c6.png": "ko/blog/교재-사진-빈칸-복습/assets/교재-사진-빈칸-복습-og.png",
    "article-bfe82cb40a38254e.png": "it/blog/foto-appunti-ripasso-attivo/assets/foto-appunti-ripasso-attivo-og.png",
    "article-c43ef683a4de68d3.png": "pt-br/blog/fotos-apostilas-revisao-ativa/assets/fotos-apostilas-revisao-ativa-og.png",
    "article-c5071596916034c2.png": "blog/registered-seller-memorization-study/assets/registered-seller-memorization-study-og.png",
    "article-c8c572f4b6d6065f.png": "es/blog/eso-bachillerato-oposiciones-material-propio/assets/eso-bachillerato-oposiciones-material-propio-og.png",
    "article-dbe6c7e9e2131f1f.png": "blog/chugaku-juken-juku-print-review/assets/chugaku-juken-juku-print-review-og.png",
    "article-ed17e704cfc556ad.png": "en/blog/photos-pdfs-active-recall-iphone/assets/photos-pdfs-active-recall-iphone-og.png",
    "article-f10c8da800fd33f2.png": "fr/blog/bac-brevet-concours-propres-supports/assets/bac-brevet-concours-propres-supports-og.png",
    "article-f603038f498bb81a.png": "pt-br/blog/enem-vestibular-concurso-material-proprio/assets/enem-vestibular-concurso-material-proprio-og.png",
    "article-faa8cf49c2cd7db4.png": "zh-tw/blog/學習資料-本機處理-隱私/assets/學習資料-本機處理-隱私-og.png",
    "article-fd724c449d7f0374.png": "zh-cn/blog/学习资料-本地处理-隐私/assets/学习资料-本地处理-隐私-og.png",
}


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
            '<p>v3.0.0のアプリ画面。教材は掲載用のサンプルです。</p>':
                '<p>実際のアプリ画面です。教材は掲載用のサンプルです。</p>',
        }
        versioned_alt_prefix = "AI赤シート v3.0.0 — "
        evergreen_alt_prefix = "AI赤シート — "
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
        versioned_alt_prefix = "AI Study Sheet v3.0.0 — "
        evergreen_alt_prefix = "AI Study Sheet — "

    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace(versioned_alt_prefix, evergreen_alt_prefix)

    text = SOFTWARE_VERSION_RE.sub(
        lambda m: ","
        if m.group(0).strip().startswith(",") and m.group(0).strip().endswith(",")
        else "",
        text,
    )
    text = clean_json_commas(text)

    if "v3.0.0" in text:
        matches = list(re.finditer(r"v3\.0\.0", text, re.IGNORECASE))
        snippets = []
        for match in matches:
            start = max(0, match.start() - 90)
            end = min(len(text), match.end() + 130)
            snippets.append(text[start:end].replace("\n", " "))
        raise RuntimeError(
            f"{path.relative_to(ROOT)}: v3.0.0 remains in contexts: {snippets}"
        )
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


def article_mapping() -> dict[str, Path]:
    if len(LEGACY_ARTICLE_TARGETS) != 38:
        raise RuntimeError(f"Expected 38 legacy article mappings, found {len(LEGACY_ARTICLE_TARGETS)}")
    mapping: dict[str, Path] = {}
    for shared_name, target_name in LEGACY_ARTICLE_TARGETS.items():
        target = ROOT / target_name
        if not target.exists():
            raise RuntimeError(f"Missing cleaned target visual: {target_name}")
        mapping[shared_name] = target
    return mapping


def replace_legacy_shared_article_visuals() -> None:
    for shared_name, target in article_mapping().items():
        destination = SHARED_DIR / shared_name
        if not destination.exists():
            raise RuntimeError(f"Missing legacy shared visual: {destination.relative_to(ROOT)}")
        shutil.copyfile(target, destination)


def validate_shared_visuals() -> None:
    for shared_name, target in article_mapping().items():
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
