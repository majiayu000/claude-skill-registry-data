---
name: qiita-operations
description: Qiita CLI操作とワークフローの共通知識。記事作成、公開状態変更、プレビュー時に参照。
---

# Qiita CLI 操作ガイド

## 基本コマンド

| コマンド | 説明 |
|----------|------|
| `bunx qiita new <basename>` | 新規記事の雛形を作成 |
| `bunx qiita preview` | ローカルプレビューサーバーを起動（port: 8888） |
| `bunx qiita publish` | 記事を Qiita に公開（CI 経由推奨） |

## ファイル構造

```
public/
├─ .remote/          # Qiita CLI 管理ディレクトリ（編集禁止）
└─ <basename>.md     # 記事ファイル
```

- ファイル名（basename）は一度決めると変更不可（Qiita 記事 ID と紐付く）
- `public/.remote/` は自動生成のため、手動編集禁止

## フロントマッター構造

```yaml
---
title: 記事タイトル
tags:
  - Tag1
  - Tag2
private: true    # 公開状態
updated_at: '...'
id: <qiita-article-id>
---
```

## 公開状態（private フィールド）

| 値 | 状態 | 説明 |
|----|------|------|
| `true` | 限定共有 | URL を知っている人のみ閲覧可能 |
| `false` | 公開 | 全ユーザーに公開、検索対象 |

### 公開状態変更時の影響

- **限定共有 → 公開**（`private: true → false`）
  - 全 Qiita ユーザーに記事が公開される
  - 検索結果に表示される
  - タイムラインに流れる可能性がある
  - **慎重な確認が必要**

- **公開 → 限定共有**（`private: false → true`）
  - URL を知っている人のみアクセス可能
  - 検索結果から除外される

## 安全要件

### 新規記事作成時の強制ルール

**新規記事は必ず `private: true` で作成する。**

1. `bunx qiita new <basename>` を実行
2. 生成されたファイルの `private: false` を `private: true` に変更
3. その後、記事を執筆

これにより、意図しない公開を防止する。

### 公開状態変更時の確認フロー

**ユーザー確認なしに公開状態を変更してはならない。**

必ず AskUserQuestion を使用して確認を取る：

```yaml
header: "公開状態変更の確認"
question: |
  「{title}」の公開状態を変更します。

  現在: {current_state}
  変更後: {new_state}

  この変更を実行しますか？
options:
  - label: "変更する"
    description: "公開状態を変更します"
  - label: "キャンセル"
    description: "変更せずに終了します"
```

確認なしでの変更、特に `private: true → false`（公開への変更）は絶対に禁止。
