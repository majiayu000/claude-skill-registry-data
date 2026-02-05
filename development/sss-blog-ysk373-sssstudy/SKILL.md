---
name: sss-blog
description: SSS Blogプロジェクトの運用スキル。ブログ記事作成、短編小説作成、サムネイル追加、プロジェクト構造の理解、デプロイ作業を支援します。記事追加、コンテンツ作成、Git操作、プロジェクトについての質問に対応します。
---

# SSS Blog 運用スキル

## 概要
SSS Blogは Astro フレームワークで構築された個人技術ブログです。
このスキルはブログの運用に必要な全ての作業を支援します。

## 対応タスク

タスクに応じて以下の参照ファイルを読み込んで実行してください:

### コンテンツ作成
| タスク | 参照ファイル |
|--------|-------------|
| ブログ記事の作成 | `references/create-blog-post.md` |
| 短編小説の作成 | `references/create-story.md` |
| サムネイル画像の追加 | `references/add-thumbnail.md` |

### プロジェクト管理
| タスク | 参照ファイル |
|--------|-------------|
| プロジェクト構造の理解 | `references/project-structure.md` |
| Git操作・デプロイ | `references/deploy.md` |

## 基本情報

### 技術スタック
- Astro 5.x (Static Site Generator)
- TypeScript / JavaScript / Markdown
- Vanilla CSS

### 主要ディレクトリ
- `content/blog/` - ブログ記事
- `content/stories/` - 短編小説
- `public/images/thumbnails/` - サムネイル画像

### 基本コマンド
```bash
npm run dev      # 開発サーバー
npm run build    # 本番ビルド
```

## 使用方法

1. ユーザーのリクエストを分析
2. 該当する参照ファイルを読み込む
3. 参照ファイルの手順に従って実行
4. 結果を報告

## 注意事項
- 外部CSSフレームワーク禁止（Vanilla CSSを使用）
- APIキーのハードコード禁止
- コミットメッセージは `feat:`, `fix:`, `docs:` 形式
