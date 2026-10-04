---
name: figma-edit
description: Use when editing or restyling an existing Figma design via the Figma MCP (use_figma / Plugin API) — especially comment- or requirement-driven changes. Covers the safe-copy workflow, reading Figma comments via REST, the Plugin API editing gotchas, and a screenshot verification loop. Trigger on requests to change/adjust/restyle a Figma screen or component, reflect Figma comments into the design, or iterate on a Figma file.
---

# figma-edit

Figma の既存デザインを `use_figma`（Plugin API）で編集するためのワークフロー。コメントや要件を起点にした修正で特に有効。

## 前提（毎回）

- **`use_figma` を呼ぶ前に必ず figma-use スキルを読む**。Figma プラグインのスキルが無い環境では MCP リソース `skill://figma/figma-use/SKILL.md` を `ReadMcpResourceTool` で読む。`use_figma` 呼び出し時は `skillNames` に `resource:figma-use`（リソース経由の場合）を付ける。
- 必要ツールは `ToolSearch` で一括ロード: `select:mcp__figma__use_figma,mcp__figma__get_metadata,mcp__figma__get_screenshot,ReadMcpResourceTool`。
- **ツール呼び出しは前置きトークンを付けず、正しい構文で出す**。長いコードを含む呼び出しほど崩れやすいので、不安なら 1 メッセージ 1 ツールの単発で。送信できたか毎回確認する。

## 手順

1. **対象を特定**: URL から fileKey とノードIDを取る（`node-id=A-B` は `A:B`）。`get_metadata` で構造（ID/名前/型/座標/サイズ）を把握してから触る。
2. **作業用コピー運用**: オリジナルは編集しない。対象セクション/フレームを `clone()` して別位置（既存と重ならない座標）に置き、名前に「（作業用コピー）」等を付けて *コピー側だけ* を編集する。元はビフォー比較・Feedback 用に残す。
3. **コメント駆動の場合**: Figma コメント本文は Plugin API では読めない。Figma REST `GET /v1/files/{fileKey}/comments` を Personal Access Token で取得する。**トークンの値はコードや会話履歴に残さない**（ローカルの token ファイル等から読む）。`client_meta.node_id` や座標で対象周辺のコメントを抽出し、要件を補完する。
4. **編集の定石（ハマりどころ）**:
   - 各 `use_figma` の冒頭で `await figma.setCurrentPageAsync(page)`（ページ切替は 1 呼び出し 1 回）。
   - テキスト編集は `await figma.loadFontAsync(node.fontName)` の後に `characters` を変更。
   - `createAutoLayout` で作った枠はデフォルトで**白 fill**。透過したいときは `fills = []`。
   - `layoutSizingHorizontal/Vertical` の `HUG`/`FILL` は `appendChild` した**後**に設定。
   - 子の挿入位置は **id 一致で index を求める**（`children.indexOf(node)` は別経路取得のノードだと参照不一致で `-1` になり `insertChild` が失敗する。`children.findIndex(c => c.id === ID)` か固定 index を使う）。
   - スクリプトは atomic（エラー時は一切適用されない）。エラーメッセージを読んで修正し再試行する。
   - 作成・変更したノードIDは必ず `return` する。
5. **確認ループ**: `get_screenshot`（または `await node.screenshot()`）→ 返ってきた URL を curl で DL → 画像を読んで視覚確認。崩れ（はみ出し・白背景の被り・余白）を直してから次へ進む。
6. **デザイントークンを踏襲**: 新規要素は色・フォント・角丸・余白を**既存ノードから読み取って**合わせる。独自の値を発明しない。カテゴリ系はタグ/バッジ、地理・属性はテキスト、など既存の表現パターンに寄せる。

## 規模が大きい / 失敗が続くとき

このスキルを読んだ**サブエージェント（Agent ツール）に実装を委譲**すると、メインの呼び出し回数が減って安定しやすい。サブエージェントには fileKey・対象ノードID・デザイントークン・各タスクの具体手順を渡し、タスクごとにスクリーンショット確認させる。
