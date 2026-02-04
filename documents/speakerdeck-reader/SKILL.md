---
name: speakerdeck-reader
description: SpeakerDeck スライドの内容を取得・要約するスキル。URL が speakerdeck.com/{user}/{slug} 形式の場合に使用。PDF をダウンロードして Read ツールで読み取る。
---

# SpeakerDeck スライド読み取り

## 手順

### 1. WebFetch でページ情報と PDF URL を取得

- WebFetch でスライドページを取得
- HTML 内のテキストトランスクリプト（`speakerdeck-transcript` クラス）があれば、それを要約に使用
- PDF ダウンロード URL を抽出（`https://files.speakerdeck.com/presentations/{id}/{filename}.pdf` 形式）

### 2. PDF をダウンロードして読み取り

トランスクリプトがない場合、または詳細な内容が必要な場合：

```bash
curl -L -o /tmp/slide.pdf "{PDF_URL}"
```

ダウンロード後、Read ツールで PDF を直接読み取り：
- Read ツールは PDF を直接読み取れる（マルチモーダル機能）
- 各スライドの内容を視覚的に解析可能

### 3. 要約に含める内容

- 発表タイトル
- 発表者名・所属
- 発表の目的・背景
- 主要なポイント（スライドごとの要点）
- 結論・まとめ
- 発表日・イベント名（分かれば）

### 4. 読了時間の推定

- スライド枚数 × 1〜2分 を目安に
