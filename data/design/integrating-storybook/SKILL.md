---
name: integrating-storybook
description: >
  spec.mdとのStorybook統合。Component APIからStoriesを自動生成。
  トリガー: storybook, stories, component api, props, argTypes, variants,
  csf, csf3, autodocs, frontend component
allowed-tools: Read, Write, Glob, Grep
---

# Storybook統合

## 目的

spec.mdのComponent API仕様からStoriesスケルトンを自動生成。

## コアコンセプト

| コンセプト | 説明 |
| --- | --- |
| Component API | spec.mdで定義されたProps、Variants、States |
| CSF3 | Component Story Format 3 + autodocs |
| 自動生成 | `/code`がspec.mdからStoriesを生成 |

## Component APIセクション（spec.md内）

`/think`がフロントエンド機能を検出すると自動追加。

**場所**: `## 4. UI仕様`内の`### 4.x Component API: [ComponentName]`

**内容**:

- Propsインターフェース（TypeScript）
- Variants（size、color、state）
- States（default、hover、disabled、loading）
- 使用例

## ワークフロー

| コマンド | アクション |
| --- | --- |
| `/think "Add Button"` | spec.mdにComponent APIセクションを追加 |
| `/code` | specから`Button.stories.tsx`を生成 |

## 既存Storiesとの統合

Storiesファイルが存在する場合:

| オプション | アクション |
| --- | --- |
| [O] 上書き | 既存ファイルを置き換え |
| [S] スキップ | 既存ファイルを維持 |
| [M] マージ | diffを表示、手動統合 |
| [D] diffのみ | 新しいStoriesのみ追加 |

## フロントエンド検出キーワード

Component API生成をトリガー:

- component, ui, button, form, modal, dialog, card, list, table

## 参照

- [@./references/component-api-template.md](./references/component-api-template.md) - Props/Variantsテンプレート
- [@./references/csf3-patterns.md](./references/csf3-patterns.md) - CSF3パターン
- [Storybook Docs](https://storybook.js.org/docs/writing-stories)
