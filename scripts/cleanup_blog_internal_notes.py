from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

INDEX_COPY = {
    "ja": {
        "path": "blog/index.html",
        "title": "Toybird Labs Blog | 生成AI・Mac・学習の実用ガイド",
        "summary": "生成AIを仕事で使うためのプロンプト例、Macで資料を見ながら作業する方法、画面共有で注目箇所を伝える方法、教材をスマホで暗記する方法をまとめています。",
        "kicker": "このブログについて",
        "bullets": [
            "生成AIを仕事で使うためのプロンプトと実例",
            "Mac・画面共有を快適にする使い方",
            "スマホで教材を復習・暗記する方法",
        ],
    },
    "en": {
        "path": "en/blog/index.html",
        "title": "Toybird Labs Blog | Practical guides for AI, Mac workflows and study",
        "summary": "Practical guides to using AI at work, working more efficiently on a Mac, directing attention during screen sharing, and reviewing study material on a phone.",
        "kicker": "About this blog",
        "bullets": [
            "Prompts and practical examples for using AI at work",
            "Mac and screen-sharing workflows that reduce friction",
            "Ways to review and memorise your own study material on a phone",
        ],
    },
    "de": {
        "path": "de/blog/index.html",
        "title": "Toybird Labs Blog | Praxisleitfäden für KI, Mac und Lernen",
        "summary": "Praxisleitfäden für KI im Arbeitsalltag, effizientere Mac-Workflows, klare Bildschirmfreigaben und das Wiederholen eigener Lernunterlagen auf dem Smartphone.",
        "kicker": "Über diesen Blog",
        "bullets": [
            "Prompts und Praxisbeispiele für KI im Arbeitsalltag",
            "Effiziente Mac- und Bildschirmfreigabe-Workflows",
            "Eigene Lernunterlagen auf dem Smartphone wiederholen und einprägen",
        ],
    },
    "fr": {
        "path": "fr/blog/index.html",
        "title": "Toybird Labs Blog | Guides pratiques sur l’IA, le Mac et l’apprentissage",
        "summary": "Des guides pratiques pour utiliser l’IA au travail, gagner en efficacité sur Mac, mieux guider l’attention pendant un partage d’écran et réviser ses supports sur smartphone.",
        "kicker": "À propos de ce blog",
        "bullets": [
            "Prompts et exemples concrets pour utiliser l’IA au travail",
            "Méthodes de travail efficaces sur Mac et en partage d’écran",
            "Façons de réviser et mémoriser ses propres supports sur smartphone",
        ],
    },
    "es": {
        "path": "es/blog/index.html",
        "title": "Toybird Labs Blog | Guías prácticas de IA, Mac y estudio",
        "summary": "Guías prácticas para usar la IA en el trabajo, trabajar con más fluidez en Mac, dirigir la atención al compartir pantalla y repasar materiales de estudio en el móvil.",
        "kicker": "Sobre este blog",
        "bullets": [
            "Prompts y ejemplos prácticos para usar la IA en el trabajo",
            "Flujos de trabajo más cómodos en Mac y al compartir pantalla",
            "Formas de repasar y memorizar tus propios materiales en el móvil",
        ],
    },
    "it": {
        "path": "it/blog/index.html",
        "title": "Toybird Labs Blog | Guide pratiche su AI, Mac e studio",
        "summary": "Guide pratiche per usare l’AI al lavoro, lavorare meglio su Mac, guidare l’attenzione durante la condivisione dello schermo e ripassare i propri materiali sullo smartphone.",
        "kicker": "Informazioni sul blog",
        "bullets": [
            "Prompt ed esempi pratici per usare l’AI al lavoro",
            "Flussi di lavoro più semplici su Mac e in condivisione schermo",
            "Metodi per ripassare e memorizzare i propri materiali sullo smartphone",
        ],
    },
    "pt-br": {
        "path": "pt-br/blog/index.html",
        "title": "Toybird Labs Blog | Guias práticos de IA, Mac e estudos",
        "summary": "Guias práticos para usar IA no trabalho, trabalhar com mais eficiência no Mac, direcionar a atenção durante o compartilhamento de tela e revisar materiais de estudo no celular.",
        "kicker": "Sobre este blog",
        "bullets": [
            "Prompts e exemplos práticos para usar IA no trabalho",
            "Fluxos de trabalho mais simples no Mac e no compartilhamento de tela",
            "Formas de revisar e memorizar seus próprios materiais no celular",
        ],
    },
    "ko": {
        "path": "ko/blog/index.html",
        "title": "Toybird Labs Blog | AI·Mac·학습 실용 가이드",
        "summary": "업무에서 AI를 활용하는 프롬프트 예시, Mac 작업 효율을 높이는 방법, 화면 공유 중 시선을 안내하는 방법, 학습 자료를 스마트폰으로 복습하는 방법을 소개합니다.",
        "kicker": "블로그 소개",
        "bullets": [
            "업무에서 AI를 활용하는 프롬프트와 실전 예시",
            "Mac과 화면 공유를 더 편하게 쓰는 방법",
            "내 학습 자료를 스마트폰으로 복습하고 암기하는 방법",
        ],
    },
    "zh-cn": {
        "path": "zh-cn/blog/index.html",
        "title": "Toybird Labs Blog | AI、Mac 与学习实用指南",
        "summary": "介绍工作中使用 AI 的提示词示例、提升 Mac 工作效率的方法、屏幕共享时引导注意力的方法，以及用手机复习学习资料的方法。",
        "kicker": "关于本博客",
        "bullets": [
            "工作中使用 AI 的提示词与实用示例",
            "提升 Mac 与屏幕共享体验的方法",
            "用手机复习和记忆自己的学习资料",
        ],
    },
    "zh-tw": {
        "path": "zh-tw/blog/index.html",
        "title": "Toybird Labs Blog | AI、Mac 與學習實用指南",
        "summary": "介紹工作中使用 AI 的提示詞範例、提升 Mac 工作效率的方法、螢幕分享時引導注意力的方法，以及用手機複習學習資料的方法。",
        "kicker": "關於本部落格",
        "bullets": [
            "工作中使用 AI 的提示詞與實用範例",
            "提升 Mac 與螢幕分享體驗的方法",
            "用手機複習與記憶自己的學習資料",
        ],
    },
}


def sub_once(pattern: str, repl: str, text: str, label: str, flags: int = 0) -> str:
    new_text, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, found {count}")
    return new_text


def rewrite_blog_index(locale: str, cfg: dict[str, object]) -> bool:
    path = ROOT / str(cfg["path"])
    if not path.exists():
        raise RuntimeError(f"Missing expected blog index: {path.relative_to(ROOT)}")

    text = path.read_text(encoding="utf-8")
    original = text
    title = str(cfg["title"])
    summary = str(cfg["summary"])
    kicker = str(cfg["kicker"])
    bullets = [str(x) for x in cfg["bullets"]]

    text = sub_once(r"<title>.*?</title>", f"<title>{title}</title>", text, f"{locale} title")
    text = sub_once(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{summary}" name="description"/>',
        text,
        f"{locale} meta description",
    )
    text = sub_once(
        r'<meta content="[^"]*" property="og:description"/>',
        f'<meta content="{summary}" property="og:description"/>',
        text,
        f"{locale} OG description",
    )
    text = sub_once(
        r'("@type":"Blog".*?"description":)"[^"]*"(,"inLanguage":)',
        lambda m: f'{m.group(1)}"{summary}"{m.group(2)}',
        text,
        f"{locale} schema description",
        flags=re.S,
    )

    hero_pattern = r'(<section class="hub-hero"><p>.*?</p><h1>.*?</h1><div>).*?(</div></section>)'
    text = sub_once(
        hero_pattern,
        lambda m: f"{m.group(1)}<p>{summary}</p>{m.group(2)}",
        text,
        f"{locale} hub hero",
        flags=re.S,
    )

    bullet_html = "".join(f"<li>{item}</li>" for item in bullets)
    replacement = (
        '<section class="method"><div>'
        f'<p class="kicker">{kicker}</p><h2>Toybird Labs Blog</h2><p>{summary}</p>'
        f'</div><ul>{bullet_html}</ul></section>'
    )
    text = sub_once(
        r'<section class="method">.*?</section>',
        replacement,
        text,
        f"{locale} summary section",
        flags=re.S,
    )

    # Release/build labels are maintenance metadata, not navigation content for readers.
    text = re.sub(r'<p>[^<]*v3\.0\.0[^<]*</p>', '', text, flags=re.I)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def cleanup_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    # Remove editorial/process boilerplate from the byline while keeping publication,
    # update and reading-time information.
    text = re.sub(
        r'(<div class="byline">)\s*<span>.*?</span>\s*(?=<time\b)',
        r'\1',
        text,
        count=1,
        flags=re.S,
    )

    # Product-specific field notes can remain useful, but the internal "what we tested"
    # kicker is editorial process language and should not lead the section.
    text = re.sub(
        r'(<section class="field-note" id="first-party">)\s*<p class="kicker">.*?</p>',
        r'\1',
        text,
        count=1,
        flags=re.S,
    )

    # Remove site-wide methodology claims from article footers. Source attribution that
    # belongs to an individual fact remains in the article's source section.
    text = re.sub(
        r'(<footer class="global-footer"><div><strong>Toybird Labs</strong>)\s*<span>.*?</span>(\s*</div>)',
        r'\1\2',
        text,
        count=1,
        flags=re.S,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def article_paths() -> list[Path]:
    paths: set[Path] = set()
    for cfg in INDEX_COPY.values():
        index = ROOT / str(cfg["path"])
        blog_dir = index.parent
        for path in blog_dir.glob("*/index.html"):
            paths.add(path)
    return sorted(paths)


def validate() -> None:
    errors: list[str] = []
    visible_internal_markers = [
        "Editorial method",
        "First-party product testing is separated from statements supported by official sources",
        "Hands-on checks by Toybird Labs · official documentation referenced",
        "Toybird Labsによる実機確認・公式資料参照",
        "実機で確認した内容と、公式資料で確認した事実を区別して掲載しています",
    ]

    for locale, cfg in INDEX_COPY.items():
        path = ROOT / str(cfg["path"])
        text = path.read_text(encoding="utf-8")
        if str(cfg["summary"]) not in text:
            errors.append(f"{path.relative_to(ROOT)}: new reader summary missing")
        if "v3.0.0" in text:
            errors.append(f"{path.relative_to(ROOT)}: v3.0.0 remains")
        if "<section class=\"method\">" not in text:
            errors.append(f"{path.relative_to(ROOT)}: summary section missing")
        for marker in visible_internal_markers:
            if marker in text:
                errors.append(f"{path.relative_to(ROOT)}: internal marker remains: {marker}")

    for path in article_paths():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if re.search(r'<div class="byline">\s*<span>.*?</span>\s*<time\b', text, flags=re.S):
            errors.append(f"{rel}: process span still leads byline")
        if re.search(r'<section class="field-note" id="first-party">\s*<p class="kicker">', text, flags=re.S):
            errors.append(f"{rel}: first-party process kicker remains")
        if re.search(r'<footer class="global-footer"><div><strong>Toybird Labs</strong>\s*<span>', text, flags=re.S):
            errors.append(f"{rel}: process footer span remains")
        for marker in visible_internal_markers:
            if marker in text:
                errors.append(f"{rel}: internal marker remains: {marker}")

    if errors:
        raise SystemExit("\n".join(errors))


def main() -> None:
    changed: list[str] = []
    for locale, cfg in INDEX_COPY.items():
        if rewrite_blog_index(locale, cfg):
            changed.append(str(cfg["path"]))
    for path in article_paths():
        if cleanup_article(path):
            changed.append(str(path.relative_to(ROOT)))

    validate()
    print(f"Validated 10 localized blog indexes and {len(article_paths())} article pages.")
    print(f"Changed {len(changed)} files.")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
