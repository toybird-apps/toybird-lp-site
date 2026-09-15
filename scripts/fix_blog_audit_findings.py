from __future__ import annotations

from html import escape
from pathlib import Path
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://lp.toybird.com"

BLOG_ROOTS = [
    ROOT / "blog",
    ROOT / "en" / "blog",
    ROOT / "de" / "blog",
    ROOT / "fr" / "blog",
    ROOT / "es" / "blog",
    ROOT / "it" / "blog",
    ROOT / "pt-br" / "blog",
    ROOT / "ko" / "blog",
    ROOT / "zh-cn" / "blog",
    ROOT / "zh-tw" / "blog",
]

AI_APP_MARKER_HTML = "app-id=6782023263"

INTERNAL_MARKERS = [
    "Editorial method",
    "First-party product testing is separated from statements supported by official sources",
    "Hands-on checks by Toybird Labs · official documentation referenced",
    "Toybird Labsによる実機確認・公式資料参照",
    "実機で確認した内容と、公式資料で確認した事実を区別して掲載しています",
    "本文區分自家產品測試與官方資料支持的事實",
    "本文區分自家產品測試與官方資料支援的事實",
]

RELEASE_WORDS = (
    r"リリース済み|released|available|veröffentlicht|verfuegbar|verfügbar|"
    r"disponible|disponível|disponibile|출시|已发布|已發布|已發佈|发布|發布|發佈"
)
VERSION_RELEASE_RE = re.compile(
    rf"\s*(?:[·•—–|-]\s*)?v3\.0\.0(?:\s*(?:{RELEASE_WORDS}))?\.?",
    re.IGNORECASE,
)
SOFTWARE_VERSION_RE = re.compile(
    r',?\s*"softwareVersion"\s*:\s*"3\.0\.0"\s*,?', re.IGNORECASE
)


def article_paths() -> list[Path]:
    paths: list[Path] = []
    for root in BLOG_ROOTS:
        if root.exists():
            paths.extend(sorted(root.glob("*/index.html")))
    return sorted(set(paths))


def public_page_dir(path: Path) -> str:
    rel = path.parent.relative_to(ROOT).as_posix()
    return f"{SITE}/{rel}/"


def local_og(path: Path) -> tuple[Path, str] | None:
    slug = path.parent.name
    asset = path.parent / "assets" / f"{slug}-og.png"
    if not asset.exists():
        return None
    return asset, f"{public_page_dir(path)}assets/{slug}-og.png"


def is_nfd_korean_duplicate(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if len(rel.parts) < 4 or rel.parts[0] != "ko" or rel.parts[1] != "blog":
        return False
    slug = path.parent.name
    return unicodedata.normalize("NFC", slug) != slug


def is_indexable(path: Path) -> bool:
    return 'content="index,follow' in path.read_text(encoding="utf-8")


def redirect_target_for_korean_duplicate(path: Path) -> str:
    slug = unicodedata.normalize("NFC", path.parent.name)
    target_dir = path.parent.parent / slug
    target = target_dir / "index.html"
    if not target.exists():
        raise RuntimeError(
            f"Missing NFC target for {path.relative_to(ROOT)}: {target.relative_to(ROOT)}"
        )
    return f"{SITE}/ko/blog/{slug}/"


def redirect_html(target: str) -> str:
    target_attr = escape(target, quote=True)
    target_js = json.dumps(target, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<meta content="noindex,follow" name="robots"/>
<link href="{target_attr}" rel="canonical"/>
<meta content="0; url={target_attr}" http-equiv="refresh"/>
<title>페이지 이동 | Toybird Labs Blog</title>
<script>location.replace({target_js}+location.search+location.hash);</script>
</head>
<body><p><a href="{target_attr}">이 페이지의 표준 URL로 이동합니다.</a></p></body>
</html>
'''


def clean_internal_markers(text: str) -> str:
    for marker in INTERNAL_MARKERS:
        text = text.replace(marker, "")
    text = re.sub(r"<span>\s*</span>", "", text)
    text = re.sub(r"<p(?:\s+class=\"[^\"]*\")?>\s*</p>", "", text)
    return text


def clean_ai_version_copy(text: str) -> str:
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
    text = re.sub(r"([·•—–|-])[ \t]*(?=</h2>)", "", text)
    text = re.sub(r" {2,}", " ", text)
    return text


def point_to_local_visual(text: str, image_url: str) -> str:
    text, count = re.subn(
        r'(<meta content=")[^"]+(" property="og:image"/>)',
        lambda m: f"{m.group(1)}{image_url}{m.group(2)}",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Missing og:image")

    text = re.sub(
        r'(<meta content=")[^"]+(" name="twitter:image"/>)',
        lambda m: f"{m.group(1)}{image_url}{m.group(2)}",
        text,
        count=1,
    )

    text, count = re.subn(
        r'("image"\s*:\s*")[^"]+(\")',
        lambda m: f"{m.group(1)}{image_url}{m.group(2)}",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Missing Article JSON-LD image")

    text, count = re.subn(
        r'(<figure class="hero-image">\s*<img\b[^>]*\bsrc=")[^"]+(\")',
        lambda m: f"{m.group(1)}{image_url}{m.group(2)}",
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Missing hero image")
    return text


def process_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if is_nfd_korean_duplicate(path):
        target = redirect_target_for_korean_duplicate(path)
        text = redirect_html(target)
    else:
        text = clean_internal_markers(text)
        if AI_APP_MARKER_HTML in text:
            text = clean_ai_version_copy(text)

        visual = local_og(path)
        if visual is None:
            raise RuntimeError(f"Missing local OG visual for {path.relative_to(ROOT)}")
        _, image_url = visual
        try:
            text = point_to_local_visual(text, image_url)
        except RuntimeError as exc:
            raise RuntimeError(f"{path.relative_to(ROOT)}: {exc}") from exc

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def validate(
    paths: list[Path],
    expected_redirects: int,
    expected_ai_after: int,
    expected_active_count: int,
) -> None:
    errors: list[str] = []
    redirect_count = 0
    active_ai = 0
    active_count = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)

        if is_nfd_korean_duplicate(path):
            redirect_count += 1
            target = redirect_target_for_korean_duplicate(path)
            if 'content="noindex,follow"' not in text:
                errors.append(f"{rel}: Korean duplicate is not noindex")
            if f'href="{target}" rel="canonical"' not in text:
                errors.append(f"{rel}: Korean duplicate canonical is wrong")
            continue

        active_count += 1
        if AI_APP_MARKER_HTML in text:
            active_ai += 1
            if "v3.0.0" in text:
                errors.append(
                    f"{rel}: v3.0.0 remains in evergreen AI Study Sheet article"
                )
            if re.search(r'"softwareVersion"\s*:', text):
                errors.append(
                    f"{rel}: softwareVersion remains in evergreen article schema"
                )

        for marker in INTERNAL_MARKERS:
            if marker in text:
                errors.append(f"{rel}: internal marker remains: {marker}")

        visual = local_og(path)
        if visual is None:
            errors.append(f"{rel}: local OG visual missing")
            continue
        _, image_url = visual
        if f'<meta content="{image_url}" property="og:image"/>' not in text:
            errors.append(f"{rel}: og:image is not localised article visual")
        if 'name="twitter:image"' in text and (
            f'<meta content="{image_url}" name="twitter:image"/>' not in text
        ):
            errors.append(f"{rel}: twitter:image is not localised article visual")
        if (
            f'"image": "{image_url}"' not in text
            and f'"image":"{image_url}"' not in text
        ):
            errors.append(f"{rel}: schema image is not localised article visual")
        if f'src="{image_url}"' not in text:
            errors.append(f"{rel}: hero image is not localised article visual")

    if redirect_count != expected_redirects:
        errors.append(
            f"Expected {expected_redirects} Korean Unicode redirects, found {redirect_count}"
        )
    if active_ai != expected_ai_after:
        errors.append(
            f"Expected {expected_ai_after} canonical AI Study Sheet articles, found {active_ai}"
        )
    if active_count != expected_active_count:
        errors.append(
            f"Expected {expected_active_count} canonical reader-facing articles, found {active_count}"
        )

    if errors:
        raise SystemExit("\n".join(errors))


def main() -> None:
    all_paths = article_paths()
    if len(all_paths) < 150:
        raise SystemExit(
            f"Unexpectedly small blog set: found {len(all_paths)} article/redirect files"
        )

    # Work only on current reader-facing articles plus the two Unicode aliases
    # that must become redirects. Existing legacy/noindex redirects are untouched.
    paths = [
        path
        for path in all_paths
        if is_nfd_korean_duplicate(path)
        or (is_indexable(path) and local_og(path) is not None)
    ]
    if len(paths) < 90:
        raise SystemExit(
            f"Unexpectedly small reader-facing set: found {len(paths)} article files"
        )

    expected_redirects = sum(is_nfd_korean_duplicate(path) for path in paths)
    if expected_redirects != 2:
        raise SystemExit(
            f"Expected 2 Korean Unicode duplicate aliases, found {expected_redirects}"
        )

    ai_before = sum(
        AI_APP_MARKER_HTML in path.read_text(encoding="utf-8") for path in paths
    )
    ai_duplicate_count = sum(
        is_nfd_korean_duplicate(path)
        and AI_APP_MARKER_HTML in path.read_text(encoding="utf-8")
        for path in paths
    )
    if ai_before < 30:
        raise SystemExit(
            f"Unexpectedly small AI Study Sheet article set before cleanup: {ai_before}"
        )

    changed: list[str] = []
    for path in paths:
        if process_article(path):
            changed.append(str(path.relative_to(ROOT)))

    validate(
        paths,
        expected_redirects=expected_redirects,
        expected_ai_after=ai_before - ai_duplicate_count,
        expected_active_count=len(paths) - expected_redirects,
    )

    print(f"Validated {len(all_paths)} total article/redirect files.")
    print(f"Validated {len(paths)} reader-facing/alias article files.")
    print(f"AI Study Sheet article files before cleanup: {ai_before}.")
    print(
        f"Canonical reader-facing articles after cleanup: {len(paths) - expected_redirects}; "
        f"Korean Unicode redirects: {expected_redirects}."
    )
    print(f"Changed {len(changed)} files.")
    for name in changed:
        print(name)


if __name__ == "__main__":
    main()
