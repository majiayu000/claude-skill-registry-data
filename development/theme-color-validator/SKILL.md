---
name: theme-color-validator
description: コンポーネントやページで色を定義する際、必ずtheme.tsから参照することを強制し、カラーコードのハードコードを禁止するSkillです。新規コンポーネント作成時、既存コンポーネント編集時に自動的に使用されます。
---

# Theme Color Validator

コンポーネントやページでの色定義において、theme.tsからの参照を強制し、カラーコードのハードコードを防ぐSkillです。

## 目的

- テーマカラーの一貫性を保つ
- カラーコードのハードコード（例: `#6246ea`, `rgb(98, 70, 234)`）を禁止
- 既存のテーマカラーパレットの活用を促進
- デザインシステムの統一性を維持

## 利用可能なカラーパレット

### 1. happyHuesColors（UIコンポーネント用）

```typescript
import { happyHuesColors } from "@/theme";

happyHuesColors.background   // #fffffe (白背景)
happyHuesColors.headline     // #2b2c34 (見出し/テキスト)
happyHuesColors.paragraph    // #2b2c34 (段落テキスト)
happyHuesColors.button       // #6246ea (プライマリボタン)
happyHuesColors.buttonText   // #fffffe (ボタンテキスト)
happyHuesColors.stroke       // #2b2c34 (ストローク/枠線)
happyHuesColors.main         // #fffffe (メイン背景)
happyHuesColors.highlight    // #6246ea (ハイライト)
happyHuesColors.secondary    // #d1d1e9 (セカンダリ)
happyHuesColors.tertiary     // #e45858 (ターシャリ/エラー)
```

### 2. chartColors（データ可視化・統計用）

```typescript
import { chartColors } from "@/theme";

// 強度・レベル表示用
chartColors.high      // #5a3fd6 (高強度)
chartColors.medium    // #b8a7f5 (中強度)
chartColors.low       // #e8e2fc (低強度)

// ワークアウトタイプ用
chartColors.strength    // #e45858 (筋トレ)
chartColors.cardio      // #7d6ce8 (有酸素)
chartColors.mixed       // #a995ee (ミックス)
chartColors.bodyweight  // #9b9ba8 (体重)

// チャート・グラフ用
chartColors.chart1   // #6246ea (プライマリ)
chartColors.chart2   // #e45858 (セカンダリ)
chartColors.chart3   // #d1d1e9 (背景)
chartColors.chart4   // #a68eec (補助1)
chartColors.chart5   // #f08585 (補助2)

// 統計メトリクス用
chartColors.metric1  // #6246ea (青紫)
chartColors.metric2  // #8871e9 (ライトパープル)
chartColors.metric3  // #d1a0e8 (紫ピンク)
chartColors.metric4  // #e45858 (赤)

// 装飾・アイコン用
chartColors.gold     // #f5c84c (ゴールド)
chartColors.success  // #6bbb6e (成功/緑)
chartColors.info     // #6246ea (情報/青紫)
```

### 3. MUIテーマパレット（Material-UIコンポーネント用）

```typescript
// sx propsで使用
sx={{
  color: "primary.main",        // #6246ea
  backgroundColor: "error.main", // #e45858
  borderColor: "text.primary",   // #2b2c34
}}

// useTheme hookで使用
import { useTheme } from "@mui/material/styles";
const theme = useTheme();
const primaryColor = theme.palette.primary.main;
```

## Instructions

### 1. 新規コンポーネント・ページ作成時

新しいコンポーネントやページで色を使用する場合：

1. **適切なパレットをインポート**:
   ```typescript
   import { happyHuesColors, chartColors } from "@/theme";
   ```

2. **用途に応じたパレットを選択**:
   - UI要素（ボタン、カード、テキスト等） → `happyHuesColors`
   - チャート、グラフ、統計データ → `chartColors`
   - Material-UIコンポーネント → `theme.palette` または `sx` props

3. **カラーコードのハードコードは禁止**:
   ```typescript
   // ❌ 悪い例: ハードコード
   <Box sx={{ backgroundColor: "#6246ea" }} />

   // ✅ 良い例: テーマ参照
   <Box sx={{ backgroundColor: happyHuesColors.button }} />
   ```

4. **既存の色で表現できない場合**:
   - ユーザーに確認を取り、`theme.ts`への追加を提案
   - 追加理由と用途を明確に説明
   - 既存の色との一貫性を保つ

### 2. 既存コンポーネント編集時

既存のコンポーネントを編集する場合：

1. **ハードコードされた色を検出**:
   - Grepツールで `#[0-9a-fA-F]{6}` パターンを検索
   - `rgb()`, `rgba()` の使用を検索

2. **適切なテーマカラーに置き換え**:
   ```typescript
   // 変更前
   const tipColor = "#9c27b0";

   // 変更後
   import { chartColors } from "@/theme";
   const tipColor = chartColors.chart1;
   ```

3. **置き換えマッピングの例**:
   - `#6246ea` → `happyHuesColors.button` または `chartColors.chart1`
   - `#e45858` → `happyHuesColors.tertiary` または `chartColors.chart2`
   - `#d1d1e9` → `happyHuesColors.secondary` または `chartColors.chart3`
   - `#2b2c34` → `happyHuesColors.headline`
   - `#fffffe` → `happyHuesColors.background`

### 3. 色が見つからない場合のフロー

適切な色がパレットに存在しない場合：

1. **類似色を探す**:
   - 既存のパレットから最も近い色を選択
   - 用途が同じ色を優先

2. **ユーザーに確認**:
   ```markdown
   このコンポーネントで使用したい色「#abc123」に該当するテーマカラーが見つかりませんでした。

   以下のいずれかをお選びください：
   1. 既存の類似色を使用: `chartColors.chart4` (#a68eec)
   2. 新しい色を `theme.ts` に追加（用途: ○○表示用）
   3. 別の色で代替
   ```

3. **追加する場合**:
   - `theme.ts` の適切なパレット（`happyHuesColors` or `chartColors`）に追加
   - コメントで用途を明記
   - 既存の命名規則に従う

## 自動起動の条件

以下の場合に自動的にこのSkillを使用します：

1. ✅ 新しいコンポーネント（`.tsx`ファイル）を作成する時
2. ✅ 既存のコンポーネントで色（`color`, `backgroundColor`, `borderColor`等）を編集する時
3. ✅ `sx` propsでカラーコードをハードコードしようとした時
4. ✅ styled-componentsやEmotionで色を定義する時

## IMPORTANT: 自動実行ポリシー

このSkillは以下の条件を満たした際、**ユーザーへの確認なし**に**即座に自動実行**してください：

### 1. コンポーネント作成時（Write/Edit前）
- ✅ 新しい`.tsx`ファイルを作成する直前
- ✅ 色を使用する可能性がある場合は、必ずインポート文を含める
- ✅ テーマカラーパレットから適切な色を選択

### 2. カラーコード検出時（Edit実行前）
- ✅ `#[0-9a-fA-F]{6}` パターンを検出した時
- ✅ `rgb()`, `rgba()` を検出した時
- ✅ 即座にテーマカラーに置き換え

### 3. 適切な色が見つからない場合のみユーザーに確認
- ✅ 既存のパレットに適切な色が存在しない
- ✅ 色の用途が不明確
- ✅ 新しい色の追加が必要

**禁止事項:**
- ❌ カラーコードをハードコードしてはいけません
- ❌ 「色を追加しますか？」と安易に確認してはいけません（まず既存の色を探す）
- ❌ theme.tsを読まずに新しい色を提案してはいけません

**実行フロー例:**
1. ユーザー: 「WorkoutCardに強度インジケーターを追加して」
2. あなた: `theme.ts`を読み込み、`chartColors.high/medium/low`が存在することを確認
3. あなた: コンポーネントに`import { chartColors } from "@/theme"`を追加
4. あなた: 強度に応じて`chartColors.high/medium/low`を使用してインジケーターを実装
5. あなた: ユーザーに実装完了を報告

## 検証チェックリスト

コンポーネント作成・編集時に以下を確認：

- [ ] `import { happyHuesColors, chartColors } from "@/theme"` が含まれているか
- [ ] カラーコード（`#`, `rgb()`, `rgba()`）のハードコードがないか
- [ ] 色の用途に応じた適切なパレットを使用しているか
- [ ] MUIコンポーネントでは`theme.palette`または`sx`を使用しているか
- [ ] 新しい色を追加する場合、ユーザーに確認を取ったか

## Examples

### Example 1: WorkoutCardの強度インジケーター

```typescript
// ❌ 悪い例: カラーコードのハードコード
const IntensityBadge = ({ level }: { level: number }) => {
  const color = level > 3 ? "#d32f2f" : level > 2 ? "#ff9800" : "#4caf50";
  return <Chip label={level} sx={{ backgroundColor: color }} />;
};

// ✅ 良い例: テーマカラー参照
import { chartColors } from "@/theme";

const IntensityBadge = ({ level }: { level: number }) => {
  const color = level > 3 ? chartColors.high : level > 2 ? chartColors.medium : chartColors.low;
  return <Chip label={level} sx={{ backgroundColor: color }} />;
};
```

### Example 2: ダッシュボードカード

```typescript
// ❌ 悪い例: Material-UIデフォルト色を直接指定
<Card sx={{ backgroundColor: "#9c27b0" }}>
  <CardContent>
    <Typography color="#ffffff">ワークアウト統計</Typography>
  </CardContent>
</Card>

// ✅ 良い例: テーマパレット使用
<Card sx={{ backgroundColor: "primary.main" }}>
  <CardContent>
    <Typography color="primary.contrastText">ワークアウト統計</Typography>
  </CardContent>
</Card>
```

### Example 3: チャートの色設定

```typescript
// ❌ 悪い例: ハードコードされた配列
const chartData = {
  datasets: [
    { data: [10, 20, 30], backgroundColor: "#6246ea" },
    { data: [15, 25, 35], backgroundColor: "#e45858" },
  ],
};

// ✅ 良い例: chartColorsから参照
import { chartColors } from "@/theme";

const chartData = {
  datasets: [
    { data: [10, 20, 30], backgroundColor: chartColors.chart1 },
    { data: [15, 25, 35], backgroundColor: chartColors.chart2 },
  ],
};
```

### Example 4: 適切な色が見つからない場合

```typescript
// ユーザーリクエスト: 「警告メッセージに黄色いバッジを追加して」

// Step 1: theme.tsを確認
// → chartColors.gold (#f5c84c) が存在することを確認

// Step 2: 実装
import { chartColors } from "@/theme";

const WarningBadge = () => {
  return <Chip label="警告" sx={{ backgroundColor: chartColors.gold }} />;
};

// ユーザーに確認は不要（既存の色で対応可能）
```

## 禁止パターン

### 絶対に避けるべきコード

```typescript
// ❌ カラーコードの直接指定
sx={{ color: "#6246ea" }}

// ❌ RGB指定
sx={{ backgroundColor: "rgb(98, 70, 234)" }}

// ❌ インラインスタイル
style={{ color: "#e45858" }}

// ❌ CSS定数の定義
const PRIMARY_COLOR = "#6246ea"; // theme.tsに定義すべき

// ❌ グラデーション（フラットデザイン原則に反する）
background: "linear-gradient(45deg, #6246ea 30%, #e45858 90%)"
```

## Related Files

このSkillを効果的に使用するための関連ファイル：

- [src/theme.ts](../../../src/theme.ts) - テーマカラーパレット定義
- [CLAUDE.md](../../../CLAUDE.md) - プロジェクトガイドライン
- `.claude/skills/work-log/SKILL.md` - 作業ログ記録Skill

## Notes

- **色の追加は慎重に**: 新しい色を追加する前に、既存のパレットで代替できないか必ず確認
- **用途を明確に**: 新しい色を追加する場合は、用途をコメントで明記
- **一貫性を保つ**: 同じ用途の色は同じパレット色を使用
- **フラットデザイン**: グラデーションは使用禁止、ソリッドカラーのみ
