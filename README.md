# Toybird LP Site

このZIPには、既存の「AI暗記シート」LPと、新規作成した「Pocket Screen」LPが含まれています。

```text
toybird-lp-site/
├── README.md
├── ai-memorize-sheet/
└── pocket-screen/
    ├── index.html
    ├── styles.css
    ├── script.js
    ├── favicon.svg
    └── assets/
        ├── app-icon.png
        ├── app-store-badge.svg
        ├── word-pdf-real-screen.png
        └── og-image.png
```

## Pocket Screen 公開URL

`https://lp.toybird.com/pocket-screen/`

## 公開前に必要な作業

`pocket-screen/index.html` 内の以下の文字列を、Pocket Screenの実際のMac App Store URLへ一括置換してください。

```text
https://apps.apple.com/jp/app/id6788211562
```

App Store URLが未提供だったため、現時点では誤ったリンクを入れず、明示的な置換トークンにしています。

## Pocket Screen LPの前提

- メイン訴求：MacBook一台でも、資料を見ながら仕事ができる
- ターゲット：カフェ、コワーキングスペース、オフィス、出張先などで一画面作業をする人
- CTA：Mac App Storeから無料ダウンロード
- 無料版：1回10分まで、期間制限なく何度でも利用可能
- 無制限版：1,500円の買い切り
- 対応環境：macOS 14以降
- 実画面素材：Word + PDFのPocket Screen実画面
- 動画：初期版には含めていません

## 外部依存

外部ライブラリ、外部フォント、外部解析ツールは使用していません。


Pocket Screen App Store: https://apps.apple.com/jp/app/id6788211562

SEO files
- `sitemap.xml`: lists the public LPs that should be indexed
- `robots.txt`: allows crawling and points search engines to the sitemap

When adding or removing an LP, update `sitemap.xml` before publishing.
