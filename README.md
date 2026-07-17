# Toybird LP Site — Japanese + English Full Set

このフォルダが `lp.toybird.com` の公開用フルセットです。
日本語版と英語版を分けて管理しつつ、サイト全体をこの1フォルダから公開できます。

## フォルダ構成

```text
toybird-lp-site/
├── index.html                         # ルート：空白・noindex
├── robots.txt
├── sitemap.xml                        # 日本語4ページ＋英語4ページ
├── shared/                            # 言語判定・言語切替の共通ファイル
│   ├── locale.js
│   ├── locale.css
│   └── app-store-badge-en.svg
│
├── ai-memorize-sheet/                 # 日本語版
├── pocket-screen/                     # 日本語版
├── prompt-ready/                      # 日本語版
├── pointer-cue/                       # 日本語版
│
└── en/
    ├── ai-memorize-sheet/             # 英語版
    ├── pocket-screen/                 # 英語版
    ├── prompt-ready/                  # 英語版
    └── pointer-cue/                   # 英語版
```

## 日本語版URL（従来URLを維持）

- `https://lp.toybird.com/ai-memorize-sheet/`
- `https://lp.toybird.com/pocket-screen/`
- `https://lp.toybird.com/prompt-ready/`
- `https://lp.toybird.com/pointer-cue/`

日本語版の本文・画像・CSS・JavaScriptは各アプリの従来フォルダに残しています。
多言語対応のため、言語切替・hreflang・canonical・GA4言語情報のみ追加しています。

## 英語版URL

- `https://lp.toybird.com/en/ai-memorize-sheet/`
- `https://lp.toybird.com/en/pocket-screen/`
- `https://lp.toybird.com/en/prompt-ready/`
- `https://lp.toybird.com/en/pointer-cue/`

## 公開方法

このZipを展開し、**中身をすべてサイトのルートへアップロード**してください。
`en/`だけ、または日本語フォルダだけを個別に公開しないでください。

## 多言語動作

- 初回アクセス時、ブラウザの優先言語が日本語なら日本語版を表示
- 日本語以外なら対応する英語版へ移動
- ページ上の `日本語 / English` で手動切替可能
- 手動選択はブラウザへ保存し、次回以降も優先
- 日本語・英語の全ページに canonical / hreflang を設定

## 素材

- AI暗記シート：公開用に教材名、ロゴ、社名などを匿名化した英語画像を使用
- Pocket Screen：英語プロモーション動画を英語LP内に収録・埋め込み
- Pointer Cue：macOS直接配布Zipを従来どおり収録

## 共通設定

- GA4測定ID：`G-MTD9Z8S7QG`
- ルート `index.html`：空白・noindex
- `sitemap.xml`：日本語4URL＋英語4URL
- `robots.txt`：サイトマップを案内

## Pointer Cue macOS直接配布版

- パス：`/pointer-cue/downloads/PointerCue_v1.1.0_Direct2026.zip`
- バージョン：1.1.0（Build 8）
- アーキテクチャ：Universal（Apple Silicon / Intel）
- 最低対応OS：macOS 13.5
- 利用期限：2026年12月31日
