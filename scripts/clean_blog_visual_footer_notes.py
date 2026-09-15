from __future__ import annotations

from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

LATIN_FONT = Path('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf')
CJK_FONT = Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

Category = Literal['prompt', 'pointer', 'pocket', 'study']

CAPTIONS: dict[str, dict[Category, str]] = {
    'ja': {
        'prompt': '実務で使えるプロンプト例を、すぐ試せる形で紹介。',
        'pointer': '画面共有やプレゼンで、見てほしい場所をすぐ強調。',
        'pocket': '必要な資料を見える位置に置いたまま、作業を続ける。',
        'study': '教材の写真やPDFを、そのまま暗記テストに。',
    },
    'en': {
        'prompt': 'Practical prompts you can adapt to real work.',
        'pointer': 'Highlight what matters without interrupting your presentation.',
        'pocket': 'Keep the reference you need visible while you work.',
        'study': 'Turn your own photos and PDFs into quick recall practice.',
    },
    'de': {
        'prompt': 'Praktische Prompts, direkt für den Arbeitsalltag.',
        'pointer': 'Wichtige Stellen zeigen, ohne die Präsentation zu unterbrechen.',
        'pocket': 'Benötigte Unterlagen sichtbar halten und weiterarbeiten.',
        'study': 'Eigene Fotos und PDFs direkt zum aktiven Wiederholen nutzen.',
    },
    'fr': {
        'prompt': 'Des prompts pratiques à adapter directement au travail.',
        'pointer': 'Mettez l’essentiel en évidence sans interrompre la présentation.',
        'pocket': 'Gardez la référence utile visible pendant que vous travaillez.',
        'study': 'Transformez vos photos et PDF en exercices de rappel actif.',
    },
    'es': {
        'prompt': 'Prompts prácticos que puedes adaptar a tu trabajo.',
        'pointer': 'Destaca lo importante sin interrumpir la presentación.',
        'pocket': 'Mantén la referencia que necesitas visible mientras trabajas.',
        'study': 'Convierte tus fotos y PDF en práctica rápida de recuerdo.',
    },
    'it': {
        'prompt': 'Prompt pratici da adattare subito al lavoro.',
        'pointer': 'Evidenzia ciò che conta senza interrompere la presentazione.',
        'pocket': 'Tieni visibile il riferimento che ti serve mentre lavori.',
        'study': 'Trasforma foto e PDF in esercizi rapidi di richiamo attivo.',
    },
    'pt-br': {
        'prompt': 'Prompts práticos para adaptar ao trabalho real.',
        'pointer': 'Destaque o que importa sem interromper a apresentação.',
        'pocket': 'Mantenha a referência necessária visível enquanto trabalha.',
        'study': 'Transforme suas fotos e PDFs em prática rápida de revisão.',
    },
    'ko': {
        'prompt': '업무에 바로 맞춰 쓸 수 있는 실용적인 프롬프트 예시.',
        'pointer': '화면 공유 흐름을 끊지 않고 중요한 곳을 바로 강조하세요.',
        'pocket': '필요한 참고 자료를 띄워 둔 채 작업을 이어가세요.',
        'study': '내 사진과 PDF를 바로 암기 복습 자료로 활용하세요.',
    },
    'zh-cn': {
        'prompt': '可直接用于实际工作的实用提示词示例。',
        'pointer': '不中断演示，也能迅速突出重点。',
        'pocket': '工作时让所需参考资料始终保持可见。',
        'study': '把自己的照片和 PDF 直接用于快速记忆练习。',
    },
    'zh-tw': {
        'prompt': '可直接套用到實際工作的實用提示詞範例。',
        'pointer': '不中斷簡報，也能快速突顯重點。',
        'pocket': '工作時讓需要的參考資料持續保持可見。',
        'study': '把自己的照片與 PDF 直接用於快速記憶練習。',
    },
}

POINTER_SLUGS = {
    'screen-sharing-show-where-to-look',
    'screenbrush-pointer-cue',
    'mac-highlight-active-window',
}


def locale_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.parts[0] == 'blog':
        return 'ja'
    return rel.parts[0]


def category_for(path: Path) -> Category:
    slug = path.parent.parent.name
    if slug.startswith('chatgpt-'):
        return 'prompt'
    if slug in POINTER_SLUGS:
        return 'pointer'
    if slug.startswith('mac-'):
        return 'pocket'
    return 'study'


def font_path_for(locale: str) -> Path:
    if locale in {'ja', 'ko', 'zh-cn', 'zh-tw'}:
        return CJK_FONT
    return LATIN_FONT


def fit_font(draw: ImageDraw.ImageDraw, text: str, locale: str, max_width: int = 650) -> ImageFont.FreeTypeFont:
    font_path = font_path_for(locale)
    if not font_path.exists():
        raise RuntimeError(f'Missing font: {font_path}')
    for size in range(24, 17, -1):
        font = ImageFont.truetype(str(font_path), size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return ImageFont.truetype(str(font_path), 18)


def replace_footer(path: Path, caption: str, locale: str) -> None:
    with Image.open(path) as src:
        image = src.convert('RGB')

    if image.size != (1200, 630):
        raise RuntimeError(f'Unexpected image size for {path.relative_to(ROOT)}: {image.size}')

    # These generated OG cards all use the same left-card geometry. The old
    # internal note lived in this footer band. Copy a clean row from the same
    # card to remove it without changing the article title or product visual.
    x1, x2 = 88, 745
    y1, y2 = 526, 575
    clean_row = image.crop((x1, 520, x2 + 1, 521))
    fill = clean_row.resize((x2 - x1 + 1, y2 - y1 + 1))
    image.paste(fill, (x1, y1))

    draw = ImageDraw.Draw(image)
    font = fit_font(draw, caption, locale)
    draw.text((92, 540), caption, font=font, fill=(88, 101, 130))
    image.save(path, format='PNG', optimize=True)


def localized_blog_pngs() -> list[Path]:
    roots = [
        ROOT / 'blog',
        ROOT / 'en' / 'blog',
        ROOT / 'de' / 'blog',
        ROOT / 'fr' / 'blog',
        ROOT / 'es' / 'blog',
        ROOT / 'it' / 'blog',
        ROOT / 'pt-br' / 'blog',
        ROOT / 'ko' / 'blog',
        ROOT / 'zh-cn' / 'blog',
        ROOT / 'zh-tw' / 'blog',
    ]
    paths: list[Path] = []
    for blog_root in roots:
        if blog_root.exists():
            paths.extend(sorted(blog_root.glob('*/assets/*-og.png')))
    return paths


def main() -> None:
    changed: list[Path] = []
    for path in localized_blog_pngs():
        locale = locale_for(path)
        if locale not in CAPTIONS:
            raise RuntimeError(f'No caption set for locale {locale}: {path.relative_to(ROOT)}')
        category = category_for(path)
        replace_footer(path, CAPTIONS[locale][category], locale)
        changed.append(path)

    # Shared Pointer Cue visuals are reused by English and several localized
    # pages, so clean both aliases in place as well.
    for name in ('pointer-cue-en.png', 'pointer-cue-en-v2.png'):
        path = ROOT / 'shared' / 'blog-visuals' / name
        if path.exists():
            replace_footer(path, CAPTIONS['en']['pointer'], 'en')
            changed.append(path)

    if len(changed) != 102:
        raise RuntimeError(f'Expected to update 102 known generated visuals, updated {len(changed)}')

    print(f'Updated {len(changed)} blog visuals.')
    for path in changed:
        print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
