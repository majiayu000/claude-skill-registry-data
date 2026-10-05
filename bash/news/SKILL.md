---
name: news
description: |
  国内（Japan）および国際（International）の主要メディアから最新のニュースヘッドラインをカテゴリ別に取得する。
---

# News CLI Skill Runbook

## 概要
`newscli` を使用して、世界の多角的な視点（Global Perspectives）と日本の主要メディア（Domestic）から最新のニュースを取得します。フィードリストは `feeds.opml` で管理され、最新 3 件のヘッドラインを並列で高速に取得します。

## 前提
- 実行ディレクトリ: `/home/yuiseki/Workspaces/repos/_cli/newscli`
- 実行コマンド: `make` (tsx 経由で `src/index.ts` を実行)
- フィード定義: `feeds.opml` (OPML 2.0 形式)
- キャッシュ: `./cache/news.json` (30 分間保持)

## 基本コマンド

### 1. すべてのニュースを取得
全カテゴリ（Japan, International, Others）のヘッドラインを表示します。
```bash
cd /home/yuiseki/Workspaces/repos/_cli/newscli && make run
```

### 2. カテゴリを指定して取得
引数（`--japan`, `--international`）を渡して、特定のカテゴリのみを表示します。
```bash
make ls-japan          # 国内ニュースのみ表示
make ls-international  # 国際ニュースのみ表示
```

### 3. キャッシュを強制更新
30 分間のキャッシュを無視して、最新の RSS を取得（同期）します。
```bash
make sync
```

## AI 秘書としての活用シナリオ
- **朝・昼のサマリー:** `heartbeat` スキルの中で実行し、最新の重要ニュースをユーザーに提示する。
- **特定トピックの深掘り:** 特定のキーワードに関連するニュースをフィルタリングして表示する。
- **視点の多様化:** 海外メディア（BBC, Al Jazeera, DW 等）と国内メディア（NHK, 日経等）の報じ方の違いを提示する。

## 運用ルール
- 30 分以内であれば `cache/news.json` から高速に表示します。
- ニュースソースの追加・削除は `feeds.opml` を編集することで動的に反映されます。
- `Japan`, `International`, `Others` の順で整理して出力します。

## 出力例
```text
news (Cache)
Date: 2026-02-24
Updated: 2026-02-24T01:23:45.678Z

>>> Japan <<<
- [2026-02-24 01:23] [NHK ニュース] 山口 下関 寺が焼ける火事 焼け跡から5人の遺体
  http://www3.nhk.or.jp/news/html/2026-02-24/k10015056861000.html
- [2026-02-24 01:23] [Yahoo! ニュース (国内)] 高市内閣の支持率73% NNN・読売
  https://news.yahoo.co.jp/pickup/6570538?source=rss
```

### 2. カテゴリを指定して取得
引数（`--japan`, `--international`）を渡して、特定のカテゴリのみを表示します。
```bash
make ls-japan          # 国内ニュースのみ表示
make ls-international  # 国際ニュースのみ表示
```

### 3. キャッシュを強制更新
30 分間のキャッシュを無視して、最新の RSS を取得（同期）します。
```bash
make sync
```

## AI 秘書としての活用シナリオ
- **朝・昼のサマリー:** `heartbeat` スキルの中で実行し、最新の重要ニュースをユーザーに提示する。
- **特定トピックの深掘り:** 特定のキーワードに関連するニュースをフィルタリングして表示する。
- **視点の多様化:** 海外メディア（BBC, Al Jazeera, DW 等）と国内メディア（NHK, 日経等）の報じ方の違いを提示する。

## 運用ルール
- 30 分以内であれば `cache/news.json` から高速に表示します。
- ニュースソースの追加・削除は `feeds.opml` を編集することで動的に反映されます。
- `Japan`, `International`, `Others` の順で整理して出力します。

## 出力例
```text
Global & Japan NewsCLI (Cache)
Filtering by category: japan
======================

>>> Japan <<<
[NHK ニュース] 山口 下関 寺が焼ける火事 焼け跡から5人の遺体
      http://www3.nhk.or.jp/news/html/20260220/k10015056861000.html
[Yahoo! ニュース (国内)] 高市内閣の支持率73% NNN・読売
      https://news.yahoo.co.jp/pickup/6570538?source=rss
```
