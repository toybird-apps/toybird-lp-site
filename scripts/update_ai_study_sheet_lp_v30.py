#!/usr/bin/env python3
from pathlib import Path
import re

JP = Path("ai-memorize-sheet/index.html")
EN = Path("en/ai-memorize-sheet/index.html")
CSS = Path("ai-memorize-sheet/styles.css")

LIGHT_START = "/* AI-STUDY-SHEET-V3-LIGHT-REFRESH:START */"
LIGHT_END = "/* AI-STUDY-SHEET-V3-LIGHT-REFRESH:END */"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing expected text for {label}")
    return text.replace(old, new, 1)


def replace_all(text: str, old: str, new: str, label: str, minimum: int = 1) -> str:
    count = text.count(old)
    if count < minimum:
        raise SystemExit(f"Expected at least {minimum} matches for {label}, found {count}")
    return text.replace(old, new)


def replace_regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"Expected one regex match for {label}, found {count}")
    return out


def update_japanese(text: str) -> str:
    old_desc = "AI赤シート v3.0.0。写真・PDFの取り込みから赤シート学習、復習まで。途中から再開できるPDF取り込み、赤シート用教材モード、ライト版アイコンに対応。iPhone・iPadで端末内処理。"
    new_desc = "AI赤シートは、教科書・プリント・ノート・写真・PDFを取り込むと重要語句を自動で隠し、AI選択の調整や手動マスク設定までできるiPhone・iPad向け暗記学習アプリです。PDFの中断・再開、ランダム・弱点優先の復習、赤シート用教材にも対応。教材データは外部AIへ送らず端末内で処理します。"
    text = replace_all(text, old_desc, new_desc, "Japanese metadata description", minimum=3)

    text = replace_regex_once(
        text,
        r'<p class="hero-lead">.*?</p>',
        '<p class="hero-lead">\n            教科書、学校プリント、ノート、資格教材<br/>\n            写真やPDFから重要語句を自動で隠し、AIの選択を調整することも、自分でマスクを設定することもできます\n          </p>',
        "Japanese hero lead",
    )

    text = replace_once(
        text,
        '<div class="floating-card floating-card-top"><strong>PDFを途中から再開</strong><span>準備できたページから学習</span></div>',
        '<div class="floating-card floating-card-top"><strong>AI選択を調整</strong><span>必要な語句を追加・削除</span></div>',
        "Japanese top floating card",
    )
    text = replace_regex_once(
        text,
        r'<div class="floating-card floating-card-bottom">\s*<strong>端末内で完結</strong>\s*<span>教材を外部AIへ送信しない</span>\s*</div>',
        '<div class="floating-card floating-card-bottom">\n<strong>手動でも設定</strong>\n<span>自分で隠す場所を決められる</span>\n</div>',
        "Japanese bottom floating card",
    )

    new_v3 = '''<section class="section v3-update" data-section-id="version_3" data-section-name="Version 3.0.0" data-track-section="" id="version-3">
<div class="container section-heading">
<div><p class="section-kicker">v3.0.0 リリース済み</p><h2>自動で始めて、<br/>自分に合わせて整える</h2></div>
<p>撮るだけで始められる簡単さと、自分で調整できる自由度。その両方を一つの学習フローにしました。</p>
</div>
<div class="container v3-grid">
<article class="feature-card"><h3>写真・PDFをすぐ教材に</h3><p>カメラ、写真、PDFを取り込んでページ単位で処理します。PDFは固定20ページ上限なし。準備できたページから確認でき、中断・再開・再試行にも対応します。</p></article>
<article class="feature-card"><h3>AI選択をそのまま調整</h3><p>自動生成したマスクを出発点に、不要な語句を外したり、必要な語句を追加したりできます。AIに任せきりにせず、自分の覚えたい範囲へ整えられます。</p></article>
<article class="feature-card"><h3>手動でマスク設定</h3><p>AI選択を使わず、自分で隠す場所を決めることもできます。候補を見ながらゼロから必要な語句だけを選べます。</p></article>
<article class="feature-card"><h3>教材の上で直接編集</h3><p>候補をタップして追加・削除。隣り合う語句はドラッグして、ひとまとまりのマスクとして設定できます。</p></article>
<article class="feature-card"><h3>学習量を段階的に変更</h3><p>「少なめ・標準・多め」は重要語句を残しながら段階的に増加。「テスト前」は独立した高密度モードとして使えます。</p></article>
<article class="feature-card"><h3>スワイプでテンポよく復習</h3><p>左右フリックで前後ページ、タップで1つの答えを表示。下から上へフリックすると、そのページの答えをまとめて表示できます。</p></article>
</div>
</section>'''
    text = replace_regex_once(
        text,
        r'<section class="section v3-update".*?</section>(?=<section class="section problem")',
        new_v3,
        "Japanese v3 section",
    )

    text = replace_once(text, '<li>重要語句とマスクを自動生成</li>', '<li>AIで自動生成し、そのまま自分で調整</li>', "Japanese comparison pillar")

    text = replace_regex_once(
        text,
        r'<article class="step-item reveal">\s*<span class="step-number">02</span>\s*<div>.*?</div>\s*</article>',
        '''<article class="step-item reveal">
<span class="step-number">02</span>
<div>
<h3>隠す場所を整える</h3>
<p>AIが選んだ語句をそのまま使う、追加・削除して調整する、最初から手動で設定する。教材や勉強方法に合わせて選べます。</p>
</div>
</article>''',
        "Japanese step 02",
    )
    text = replace_regex_once(
        text,
        r'<article class="step-item reveal">\s*<span class="step-number">03</span>\s*<div>.*?</div>\s*</article>',
        '''<article class="step-item reveal">
<span class="step-number">03</span>
<div>
<h3>出題して覚える</h3>
<p>順番・ランダム・弱点優先で出題。左右フリックでページ移動、タップで1問表示、上フリックですべて表示。10・20・50問・すべてから学習量も選べます。</p>
</div>
</article>''',
        "Japanese step 03",
    )

    text = replace_once(
        text,
        '<p class="section-kicker">学習を続けるための機能</p>\n<h2>作って終わりではなく、<br/>覚えるところまで支えます</h2>',
        '<p class="section-kicker">自動で始めて、自分に合わせる</p>\n<h2>AIの速さと、<br/>自分で決められる自由さを両立</h2>',
        "Japanese features heading",
    )
    text = replace_once(
        text,
        '<h3>マスクを編集・切り替え</h3>\n<p>マスク量は「少なめ・標準・多め・テスト前」の4段階。不要なマスクの削除、追加、別パターンへの切り替えができます。赤シート用教材モードでは、手動編集・量・パターンの変更はできません。</p>',
        '<h3>AI選択を調整・手動で設定</h3>\n<p>AIが選んだマスクを追加・削除して整えることも、最初から自分でマスクを設定することもできます。「少なめ・標準・多め・テスト前」で学習量も切り替えられます。</p>',
        "Japanese mask feature",
    )
    text = replace_once(
        text,
        '<p>教材、画像、フォルダ、マスク、学習履歴をまとめてバックアップマスク付き画像の共有にも対応します</p>',
        '<p>教材、画像、フォルダ、マスク、学習履歴をまとめてバックアップ。マスク付き画像の共有にも対応します。</p>',
        "Japanese backup copy fix",
    )

    old_faq = '<details class="reveal" data-faq-id="v3_2" data-track-faq=""><summary>通常モードのマスクを調整</summary><p>マスク量は「少なめ・標準・多め・テスト前」の4段階。不要なマスクの削除、追加、別パターンへの切り替えができます。赤シート用教材モードでは、手動編集・量・パターンの変更はできません。</p></details>'
    new_faq = '<details class="reveal" data-faq-id="v3_2" data-track-faq=""><summary>AIの選択は自分で直せますか？</summary><p>はい。AIが選んだ語句を追加・削除して調整できます。AI選択を使わず、最初から自分でマスクを設定することもできます。通常モードでは「少なめ・標準・多め・テスト前」も選べます。</p></details><details class="reveal" data-faq-id="v3_swipe" data-track-faq=""><summary>学習画面はどんな操作に対応していますか？</summary><p>左右フリックで前後ページへ移動し、マスクをタップすると1つずつ答えを表示できます。下から上へフリックすると、そのページの答えをまとめて表示できます。</p></details>'
    text = replace_once(text, old_faq, new_faq, "Japanese FAQ mask and swipe")
    return text


def update_english(text: str) -> str:
    old_desc = "AI Study Sheet v3.0.0 turns photos and PDFs into active-recall practice on iPhone and iPad. Resume PDF imports, study pre-marked materials, and use the new light app icon. Processing stays on device."
    new_desc = "AI Study Sheet turns photos and PDFs into active-recall practice on iPhone and iPad. Start with AI-generated masks, adjust the selection or set masks manually, resume large PDF imports, and review in order, randomly, or by weak points. Materials stay on device."
    text = replace_all(text, old_desc, new_desc, "English metadata description", minimum=3)

    text = replace_regex_once(
        text,
        r'<p class="hero-lead">.*?</p>',
        '<p class="hero-lead">\n            Textbooks, worksheets, notes, and exam-prep materials<br/>\n            Start with AI-generated masks, then adjust the selection or set masks yourself to match the way you study\n          </p>',
        "English hero lead",
    )
    text = replace_once(
        text,
        '<div class="floating-card floating-card-top"><strong>Resume PDF imports</strong><span>Study pages as they become ready</span></div>',
        '<div class="floating-card floating-card-top"><strong>Adjust the AI selection</strong><span>Add or remove the terms you need</span></div>',
        "English top floating card",
    )
    text = replace_regex_once(
        text,
        r'<div class="floating-card floating-card-bottom">\s*<strong>Processed on your device</strong>\s*<span>Your materials are never sent to external AI services</span>\s*</div>',
        '<div class="floating-card floating-card-bottom">\n<strong>Set masks manually</strong>\n<span>Choose exactly what you want to hide</span>\n</div>',
        "English bottom floating card",
    )

    new_v3 = '''<section class="section v3-update" data-section-id="version_3" data-section-name="Version 3.0.0" data-track-section="" id="version-3">
<div class="container section-heading">
<div><p class="section-kicker">v3.0.0 Released</p><h2>Start automatically,<br/>then make it yours</h2></div>
<p>The speed of automatic setup and the freedom to decide what you want to study, in one workflow.</p>
</div>
<div class="container v3-grid">
<article class="feature-card"><h3>Turn photos and PDFs into study material</h3><p>Import with the camera, photos, or a PDF and process pages individually. PDFs have no fixed 20-page cap. Open ready pages, pause, resume, or retry an import.</p></article>
<article class="feature-card"><h3>Adjust the AI selection</h3><p>Use AI-generated masks as a starting point, remove terms you do not need, and add the ones you do. You can shape the material around what you actually want to remember.</p></article>
<article class="feature-card"><h3>Set masks manually</h3><p>Skip the AI selection and choose what to hide yourself. Start from zero and keep only the terms that matter to your own study plan.</p></article>
<article class="feature-card"><h3>Edit directly on the material</h3><p>Tap candidates to add or remove them. Drag across neighboring terms to turn them into one combined mask.</p></article>
<article class="feature-card"><h3>Change study density</h3><p>Low, Standard, and High increase progressively while preserving important terms. Before a test is a separate high-density mode for final review.</p></article>
<article class="feature-card"><h3>Review quickly with gestures</h3><p>Swipe left or right between pages, tap a mask to reveal one answer, or swipe up to reveal all answers on the current page.</p></article>
</div>
</section>'''
    text = replace_regex_once(
        text,
        r'<section class="section v3-update".*?</section>(?=<section class="section problem")',
        new_v3,
        "English v3 section",
    )
    text = replace_once(text, '<li>Generate key terms and masks automatically</li>', '<li>Generate with AI, then adjust it yourself</li>', "English comparison pillar")

    text = replace_regex_once(
        text,
        r'<article class="step-item reveal">\s*<span class="step-number">02</span>\s*<div>.*?</div>\s*</article>',
        '''<article class="step-item reveal">
<span class="step-number">02</span>
<div>
<h3>Shape what gets hidden</h3>
<p>Use the AI selection as-is, add or remove terms, or set masks manually from the start. Choose the workflow that fits your material and study method.</p>
</div>
</article>''',
        "English step 02",
    )
    text = replace_regex_once(
        text,
        r'<article class="step-item reveal">\s*<span class="step-number">03</span>\s*<div>.*?</div>\s*</article>',
        '''<article class="step-item reveal">
<span class="step-number">03</span>
<div>
<h3>Quiz yourself and remember</h3>
<p>Study in order, randomly, or with weak points first. Swipe between pages, tap to reveal one answer, or swipe up to reveal all. Choose 10, 20, 50, or all questions.</p>
</div>
</article>''',
        "English step 03",
    )

    text = replace_once(
        text,
        '<p class="section-kicker">Features that support continued learning</p>',
        '<p class="section-kicker">Start automatically, then make it yours</p>',
        "English features kicker",
    )
    return text


def update_css(text: str) -> str:
    # Remove a previous managed block when the script is rerun.
    text = re.sub(r'\n?/\* AI-STUDY-SHEET-V3-LIGHT-REFRESH:START \*/.*?/\* AI-STUDY-SHEET-V3-LIGHT-REFRESH:END \*/\n?', '\n', text, flags=re.S)
    block = r'''
/* AI-STUDY-SHEET-V3-LIGHT-REFRESH:START */
:root {
  --bg: #f7f8fb;
  --bg-soft: #ffffff;
  --panel: #ffffff;
  --panel-2: #f2f4f7;
  --text: #1d1d1f;
  --muted: #5f6368;
  --muted-2: #858b94;
  --line: rgba(29, 29, 31, 0.10);
  --blue: #007aff;
  --blue-2: #005ed8;
  --red: #ff3b30;
  --green: #1f9d63;
  --shadow: 0 24px 70px rgba(48, 60, 75, 0.14);
}
body {
  color: var(--text);
  background:
    radial-gradient(circle at 8% 4%, rgba(0, 122, 255, 0.08), transparent 26rem),
    radial-gradient(circle at 92% 18%, rgba(255, 59, 48, 0.045), transparent 24rem),
    var(--bg);
}
::selection { background: rgba(0, 122, 255, 0.18); color: #111; }
.skip-link { background: #1d1d1f; color: #fff; }
.site-header {
  border-bottom-color: rgba(29, 29, 31, 0.08);
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 8px 28px rgba(40, 48, 58, 0.05);
}
.nav-links { color: var(--muted); }
.nav-links a:hover { color: var(--text); }
.button-primary {
  color: #fff;
  background: linear-gradient(135deg, #168cff, #0067d8);
  box-shadow: 0 15px 34px rgba(0, 105, 220, 0.20);
}
.button-ghost {
  color: var(--text);
  border-color: rgba(29,29,31,.12);
  background: rgba(255,255,255,.82);
}
.store-symbol { background: rgba(255,255,255,.18); }
.eyebrow, .section-kicker { color: var(--blue); }
.eyebrow { border-color: rgba(0,122,255,.16); background: rgba(0,122,255,.07); }
h1 span { color: var(--text); }
.hero-lead { color: #50555d; }
.purchase-note { color: #717780; }
.hero-glow-one { background: radial-gradient(circle, rgba(0,122,255,.14), transparent 68%); }
.hero-glow-two { background: radial-gradient(circle, rgba(255,59,48,.07), transparent 70%); }
.phone {
  border-color: #d7dce3;
  background: #fff;
  box-shadow: 0 30px 70px rgba(58, 70, 84, 0.18);
}
.phone::after { box-shadow: inset 0 0 0 1px rgba(0,0,0,.05); }
.floating-card {
  border-color: rgba(29,29,31,.09);
  background: rgba(255,255,255,.94);
  box-shadow: 0 18px 42px rgba(48, 60, 75, 0.14);
}
.floating-card span { color: var(--muted); }
.quick-facts { border-block-color: var(--line); background: rgba(255,255,255,.62); }
.compare-card, .feature-card, .use-case-card, .step-item {
  border-color: var(--line);
  background: #fff;
  box-shadow: 0 12px 32px rgba(48, 60, 75, 0.055);
}
.compare-card.active {
  border-color: rgba(0,122,255,.20);
  background: linear-gradient(140deg, rgba(0,122,255,.08), transparent 50%), #fff;
  box-shadow: 0 18px 48px rgba(0,90,180,.09);
}
.compare-card.muted { opacity: 1; background: #f2f3f5; }
.compare-label { color: var(--muted); background: rgba(29,29,31,.05); }
.active .compare-label { color: var(--blue); background: rgba(0,122,255,.09); }
.use-cases { background: radial-gradient(circle at 18% 20%, rgba(0,122,255,.055), transparent 24rem), #fafbfc; }
.steps { background: linear-gradient(180deg, transparent, rgba(0,122,255,.035), transparent); }
.step-number { color: var(--blue); background: rgba(0,122,255,.08); }
.steps-cta,
.privacy-card,
.ios-card,
.purchase-card,
.final-card {
  border-color: var(--line);
  background: linear-gradient(145deg, rgba(0,122,255,.035), transparent 55%), #fff;
  box-shadow: 0 18px 50px rgba(48, 60, 75, 0.08);
}
.gallery { background: #f5f6f8; }
.gallery-item figcaption { color: var(--muted); }
.privacy-icon, .document-visual, .purchase-badge { background: rgba(0,122,255,.08); }
.faq-list details {
  border-color: var(--line);
  background: #fff;
  box-shadow: 0 8px 22px rgba(48, 60, 75, 0.04);
}
.faq-list summary { color: var(--text); }
.final-cta { background: linear-gradient(180deg, transparent, rgba(0,122,255,.035)); }
footer { border-top-color: var(--line); color: var(--muted); }
@media (max-width: 800px) {
  .site-header { background: rgba(255,255,255,.94); }
  .floating-card { background: rgba(255,255,255,.97); }
}
/* AI-STUDY-SHEET-V3-LIGHT-REFRESH:END */
'''
    return text.rstrip() + "\n" + block.lstrip()


def main() -> None:
    jp = update_japanese(JP.read_text(encoding="utf-8"))
    en = update_english(EN.read_text(encoding="utf-8"))
    css = update_css(CSS.read_text(encoding="utf-8"))

    JP.write_text(jp, encoding="utf-8")
    EN.write_text(en, encoding="utf-8")
    CSS.write_text(css, encoding="utf-8")

    # Final safety checks.
    checks = {
        JP: ["AI選択をそのまま調整", "手動でマスク設定", "スワイプでテンポよく復習"],
        EN: ["Adjust the AI selection", "Set masks manually", "Review quickly with gestures"],
        CSS: [LIGHT_START, "--bg: #f7f8fb", "background: rgba(255, 255, 255, 0.86)"],
    }
    for path, needles in checks.items():
        data = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"Validation failed: {needle!r} missing in {path}")
    print("Updated Japanese and English AI Study Sheet landing pages for v3.0 Build 30.")
    print("Applied default light LP design and two-pillar messaging.")


if __name__ == "__main__":
    main()
