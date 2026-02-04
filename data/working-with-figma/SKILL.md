---
name: working-with-figma
description: FigmaデザインをMCPツールで取得し、既存コードベースへ正確に実装します。デザイン情報の取得から実装までを一貫して支援します。Figmaデザインとの作業が必要なときに使用してください。
allowed-tools: Read, Write, Bash, Glob
disable-model-invocation: true
---

# Figma デザインワークフロー

## 概要

Figmaデザインの参照から実装までを統合的に支援するスキルです。2つの主要機能を提供:

1. **デザイン情報取得**: Figma MCPでデザイン仕様を正確に取得
2. **実装**: 取得した情報を既存コードベースへ正確に反映

## Quick Start

### デザイン情報取得モード

1. Figma URLを受け取る
2. Figma MCPでデザイン情報を取得
3. 実測値を整理して共有

### 実装モード

1. デザイン情報を確認
2. 既存コードベースの設計体系を把握
3. コンポーネント設計 → 実装 → 検証

## 実行フロー

### Phase 1: デザイン情報の取得

**ツール:**

- `mcp__figma-desktop__get_design_context` - 構造とプロパティ取得
- `mcp__figma-desktop__get_screenshot` - ビジュアル確認

**抽出する情報:**

- 配色（カラートークン、HEX値）
- タイポグラフィ（サイズ、行高、ウェイト）
- スペーシング（余白、gap、padding）
- レイアウト（constraints、autolayout）
- 角丸・影（border-radius、box-shadow）
- バリアント（prop名と値）

詳細は [FETCHING.md](./FETCHING.md) を参照。

### Phase 2: 実装

**ステップ:**

1. **設計確認**
   - 既存のレイアウト/コンポーネント構造確認
   - props・state・variant整理

2. **実装**
   - デザイントークンに沿って適用
   - アクセシビリティ確保
   - 状態管理（default/hover/focus/active/disabled）

3. **検証**
   - ブレークポイントごとの表示確認
   - ビルド・テスト・リント実行

詳細は [IMPLEMENTING.md](./IMPLEMENTING.md) を参照。

## 実装ガイドライン

### スタイル適用の優先順位

1. 既存のデザイントークンを使用
2. 既存コンポーネントを再利用/拡張
3. 新規作成は最小限に

### 出力フォーマット

```markdown
## デザイン情報

- **対象**: [URL]（ページ/ノード、デバイス、テーマ）
- **配色**: primary/500: `#0A84FF`
- **タイポグラフィ**: Heading/LG: 28px/34px, weight 700

## 実装結果

### 変更ファイル
- `src/components/Button.tsx`: variant追加

### テスト結果
- ビルド: OK
- リント: OK
```

## 注意事項

- 推測せず、必ずFigma MCPの結果を根拠にする
- 取得できない場合は「どのノード/権限が不足しているか」を具体的に伝える
- 変更範囲を最小化し、影響範囲が広い場合は理由とリスクを明示

## 関連ファイル

- [FETCHING.md](./FETCHING.md) - デザイン情報取得の詳細ガイド
- [IMPLEMENTING.md](./IMPLEMENTING.md) - 実装の詳細ガイド
