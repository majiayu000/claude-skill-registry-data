---
name: hatebu
description: Hatena Bookmark CLI を操作して、ユーザーのブックマーク履歴を同期・取得・検索する。ユーザーの興味関心や過去に読んだ記事を調査する際に使用する。
---

# Hatena Bookmark CLI Skill Runbook

## 概要
`hatebu` CLI ツールを使用して、はてなブックマークのデータを操作します。ブックマークの取得、ローカル検索、統計分析（ドメイン、タグ、頻出単語）、およびキャッシュの同期が可能です。

## 前提
- 実行バイナリ: `hatebu`
- 認証設定: `hatebu config set username <name>`（`~/.config/hatebu/credentials.json` に保存）。
- キャッシュ: `~/.cache/hatebucli/` に `YYYY/MM/DD.json` 形式で保存される。

## 基本コマンド

### 1. 設定と認証確認
```bash
hatebu config set username <name>
hatebu config get username
```

### 2. ブックマークの一覧取得
特定の日付のブックマークを取得します。
```bash
hatebu ls --date 2026-02-19
hatebu ls --json
```
- **今日:** API から最新データを取得します。
- **過去:** ローカルキャッシュから読み込みます。

### 3. ローカル検索
キャッシュされたブックマークを検索します。
```bash
hatebu search "検索ワード"
hatebu search "Go" --field title --limit 20
```

### 4. 使用状況の分析と統計
特定の日付や期間におけるドメイン、タグ、頻出単語の統計を取得します。
デフォルトでは直近1週間のデータ（8日前〜昨日）が対象となります。

#### 項目別リスト
```bash
hatebu domains --today         # 今日のドメイン統計
hatebu tags --date 2026-02     # 2月のタグ統計
hatebu words --date 2026       # 2026年の頻出単語統計（形態素解析を使用）
```

#### 総合レポート (Stats)
週間の Markdown サマリーを表示します。
```bash
hatebu stats                   # 直近1週間のサマリー
hatebu stats --date 2026-02-20 --days 30  # 指定日から30日分遡ったサマリー
```

### 5. 同期とインポート
```bash
hatebu sync --days 7           # 指定日数分（昨日以前）を同期
hatebu sync --date 2026-01-01  # 特定の日付を同期してキャッシュに保存
hatebu import <path>           # 既存のデータディレクトリ（YYYY/MM/*.json）から一括インポート
```

## AI 秘書としての活用シナリオ
- **長期的な興味分析:** `words` や `tags` を期間指定（年単位など）で実行し、興味関心の変遷を可視化する。
- **今日のサマリー:** `hatebu ls` で今日のブックマークをリアルタイムに取得し、その日のニュースまとめを作成する。
- **活動傾向の把握:** `stats` を確認し、ユーザーが最近どのようなサイト（ドメイン）を頻繁にチェックしているか把握する。

## 運用ルール
- 今日のデータは `sync` せず、`ls` や分析コマンド（`--today` 付与）で最新を取得する。
- 設定が未完了の場合は `hatebu config set username` を案内する。
