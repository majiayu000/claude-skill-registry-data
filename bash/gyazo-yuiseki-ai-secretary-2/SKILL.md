---
name: gyazo
description: Gyazo CLI を操作して過去のキャプチャ（画像、OCRテキスト、メタデータ）を検索・取得・同期する。ユーザーの視覚的な記憶やリサーチ内容を調査する際に使用する。
---

# Gyazo CLI Skill Runbook

## 概要
`gyazo` CLI ツールを使用して、Gyazo に保存されたキャプチャ画像を操作します。OCR テキストやウィンドウタイトルなどのメタデータを含めて取得・検索・時間軸での列挙が可能です。

## 前提
- 実行バイナリ: `gyazo`
- 認証設定: `gyazo config set token <token>`（`~/.config/gyazo/credentials.json` に保存）。
- キャッシュ: `~/.cache/gyazocli/` に画像詳細と時間軸インデックスが保存される。

## 基本コマンド

### 1. 設定と認証確認
```bash
gyazo config set token <token>
gyazo config get me            # 現在のユーザー情報を取得（疎通確認）
```

### 2. 画像の列挙
直近の画像、または特定の属性（写真、アップロード済み）や時間帯を指定して列挙します。
AI エージェントが結果を後続処理する場合は `--json` を優先します。
```bash
gyazo ls --limit 10
gyazo ls --limit 10 --json      # 構造化出力（推奨）
gyazo ls --hour 2026-01-01-10  # 2026年1月1日 10時台の画像をキャッシュから取得
gyazo ls --photos              # 位置情報を持つ画像（写真）のみ
gyazo ls --uploaded            # gyazocli からアップロードした画像のみ
```

### 3. 検索
Gyazo API の検索機能を使用します。デフォルトでキャッシュを使用しますが、`--no-cache` で強制的に最新化できます。
```bash
gyazo search "date:2026-02-19" --json
gyazo search "検索ワード" --json
```

### 4. 画像詳細の取得 (OCR/物体認識含む)
特定の `image_id` の詳細情報を取得します。
```bash
gyazo get <image_id> --ocr --objects
```

### 5. アップロード
```bash
gyazo upload image.png --title "メモ" --desc "詳細説明"
```

### 6. 使用状況の分析と統計
特定の日付や期間における使用アプリ、ドメイン、タグ、位置情報の統計を取得します。
デフォルトでは直近1週間のデータ（8日前〜昨日）が対象となります。

#### 項目別リスト
```bash
gyazo apps --today             # 今日のアプリ使用状況
gyazo domains --date 2026-02   # 2月のドメイン統計
gyazo tags --date 2026         # 2026年のタグ統計
gyazo locations --days 30      # 直近30日間の位置情報統計
```

#### 総合レポート (Stats)
週間の Markdown サマリーを表示します。
```bash
gyazo stats                    # 直近1週間のサマリー
gyazo stats --date 2026-02-20 --days 30  # 指定日から30日分遡ったサマリー
```

### 7. 同期とインポート
```bash
gyazo sync --days 7            # 指定日数分を同期
gyazo sync --date 2026-01      # 特定の月をまるごと同期
gyazo import json <path>       # 既存の JSON キャッシュを一括インポート
gyazo import hourly <path>     # 既存の hourly インデックスを一括インポート
```

## AI 秘書としての活用シナリオ
- **時間軸での記憶探索:** 「元日の午前中に何してた？」に対し、`gyazo ls --hour 2026-01-01-09` 等を実行して視覚情報を得る。
- **特定情報の深掘り:** 画像の OCR テキストから技術的なキーワードや商品名を抽出し、リサーチに役立てる。
- **コンテキストの把握:** `stats` を確認し、ユーザーが最近どのようなツールやサイトを使っていたか、どこにいたかなどの活動傾向を把握する。

## 運用ルール
- 証拠に基づかない推測は行わない。特に「購入した」「契約した」といった断定は、注文完了画面や支払い完了画面のキャプチャが明確に存在する場合のみ行う。商品ページやカート画面のキャプチャだけでは「検討中」とみなす。
- 今日の画像は `sync` の対象外（デフォルト）。最新の画像が必要な場合は `ls` や `search`、あるいは分析コマンドで `--today` を使用する。
- `ls` で機械処理する場合は `gyazo ls --json` を優先する（パースの安定性向上）。
- キャッシュが古そうな場合は `--no-cache` オプションを検討する。
- 設定が未完了の場合は `gyazo config set token` を案内する。
