---
name: review-perspective-selector
description: Automatically selects appropriate review perspectives based on file type and characteristics. Use when initiating code review to determine which review-points files should be applied.
allowed-tools: Read
---

# Review Perspective Selector Skill

このskillは、実装ファイルの種別に応じて適切なレビュー観点デッキを自動選択します。

## 目的

- ファイルの特性（ビジネスロジック、UI、ユーティリティ等）を判定
- 適切なレビュー観点ファイル（`.claude/review-points/*.md`）を選択
- review-fileエージェントに渡す観点リストを生成

## ファイル分類と観点マッピング

### 1. ビジネスロジック（ドメインロジック）

**ファイルパターン**:
- `src/utils/*.ts` - ユーティリティ関数
- `src/lib/*.ts` - ライブラリ関数
- `src/services/*.ts` - ビジネスロジック

**適用観点**:
- ✅ `typescript.md` (必須) - 型安全性

**理由**: ビジネスロジックの正確性と型安全性が重要

---

### 2. 型定義

**ファイルパターン**:
- `src/types/*.ts`
- `src/**/*.types.ts`

**適用観点**:
- ✅ `typescript.md` (必須) - 型安全性

**理由**: 型の正確性とnull安全性が重要

---

### 3. React コンポーネント（UI層）

**ファイルパターン**:
- `src/components/**/*.tsx`
- `src/pages/**/*.tsx`
- `src/app/**/*.tsx`
- `src/App.tsx`

**適用観点**:
- ✅ `typescript.md` (必須) - 型安全性
- ✅ `react-component.md` (推奨) - Reactのベストプラクティス
- ✅ `project-structure.md` (推奨) - コンポーネント配置

**理由**: Reactのベストプラクティスと型安全性が重要

---

### 4. 状態管理

**ファイルパターン**:
- `src/stores/*.ts` - Zustand/Redux等
- `src/store/*.ts`
- `src/state/*.ts`

**適用観点**:
- ✅ `typescript.md` (必須) - 型安全性

**理由**: 状態の型安全性が重要

---

### 5. カスタムフック

**ファイルパターン**:
- `src/hooks/*.ts`
- `src/hooks/*.tsx`

**適用観点**:
- ✅ `typescript.md` (必須) - 型安全性
- ✅ `react-component.md` (推奨) - Reactフックのルール

**理由**: Reactフックのルールと型安全性が重要

---

### 6. 定数定義

**ファイルパターン**:
- `src/utils/constants.ts`
- `src/constants/*.ts`
- `src/config/*.ts`

**適用観点**:
- ✅ `typescript.md` (必須) - 型安全性

**理由**: 定数の型安全性が重要

---

### 7. テストファイル

**ファイルパターン**:
- `src/**/*.test.ts`
- `src/**/*.test.tsx`
- `src/**/*.spec.ts`
- `src/**/*.spec.tsx`
- `src/__tests__/**/*.ts`

**適用観点**:
- ✅ `test-quality.md` (必須) - テスト品質チェック
- ✅ `typescript.md` (必須) - 型安全性
- ✅ 対応する実装ファイルの観点を継承
  - 例: `utils.test.ts` → 実装ファイル `utils.ts` の観点を継承
  - 例: `Component.test.tsx` → `react-component.md` も適用

**理由**: テストは実装と同じ観点で検証すべき + テスト固有の品質観点

---

### 8. 設定ファイル

**ファイルパターン**:
- `vite.config.ts`
- `tsconfig.json`
- `package.json`
- `biome.json`

**適用観点**:
- ✅ `project-structure.md` (推奨) - プロジェクト構成

**理由**: プロジェクト全体の構成に影響する

---

## 自動選択ロジック

```typescript
function selectReviewPerspectives(filePath: string): string[] {
  const perspectives: string[] = [];

  // 全ファイルに適用
  perspectives.push('typescript.md');

  // テストファイル
  if (/\.(test|spec)\.(ts|tsx)$/.test(filePath) || /__tests__\//.test(filePath)) {
    perspectives.push('test-quality.md'); // テスト品質チェック（必須）

    // 対応する実装ファイルの観点を継承
    const implFilePath = filePath
      .replace(/\.(test|spec)\.(ts|tsx)$/, '.$1')
      .replace(/__tests__\//, '');
    perspectives.push(...selectReviewPerspectives(implFilePath).filter(p => p !== 'test-quality.md'));

    return [...new Set(perspectives)];
  }

  // React コンポーネント
  if (/\.tsx$/.test(filePath) && /components|pages|app/.test(filePath)) {
    perspectives.push('react-component.md');
    perspectives.push('project-structure.md');
  }

  // カスタムフック
  if (/hooks\//.test(filePath)) {
    perspectives.push('react-component.md');
  }

  // プロジェクト構造（新規ファイル追加時）
  if (isNewFile(filePath)) {
    perspectives.push('project-structure.md');
  }

  // 設定ファイル
  if (/vite\.config|tsconfig|package\.json|biome\.json/.test(filePath)) {
    perspectives.push('project-structure.md');
  }

  return [...new Set(perspectives)]; // 重複削除
}
```

---

## 使用例

### review-fileエージェント呼び出し時

```javascript
// classify-filesの結果からファイル種別を取得
const filePath = "src/utils/helpers.ts";

// skillを使って観点を自動選択
Use the review-perspective-selector skill to determine appropriate review perspectives for ${filePath}

// 出力例:
// - typescript.md

// review-fileエージェントに渡す
{
  "subagent_type": "review-file",
  "prompt": `以下の観点ファイルを使用して ${filePath} をレビューしてください:

観点ファイル:
- .claude/review-points/typescript.md

PASS/WARN/FAILで判定してください。`
}
```

---

## 観点デッキのskill化について

**結論: 現状の `.claude/review-points/` のままでOK**

**理由**:
1. **参照効率は同じ**: skillとして読み込んでも、直接ファイルを読んでも、Read toolの呼び出し回数は同じ
2. **明確な責務分離**:
   - `.claude/review-points/` = 観点の**内容**（what）
   - `.claude/skills/review-perspective-selector/` = 観点の**選択ロジック**（which）
3. **保守性**: 観点ファイルは独立したドキュメントとして管理しやすい

**skillにすべき場合**:
- 観点ファイルが頻繁に更新され、バージョン管理が必要な場合
- 観点の内容が複雑で、プログラム的な処理（計算、条件分岐）が必要な場合

---

## 使用方法

### TDDパイプライン (`/tdd-next`) での使用

```markdown
### ステップ5: review-file エージェント起動 (Refactor判断)

1. review-perspective-selector skill を使用して観点を選択
2. 選択された観点ファイルを指定してreview-fileエージェントを起動
3. テストファイルも必ず確認
```

### スラッシュコマンド `/review-code` での使用

既存の `/review-code` コマンドは classify-files エージェントが観点を自動選択しているため、このskillと統合できます。

---

## 今後の拡張

### 観点の追加が必要なケース

1. **パフォーマンス観点** (`performance.md`)
   - 対象: アニメーションループ、大量データ処理
2. **アクセシビリティ観点** (`accessibility.md`)
   - 対象: UIコンポーネント
3. **セキュリティ観点** (`security.md`)
   - 対象: 入力バリデーション、localStorage操作
4. **テストカバレッジ観点** (`test-coverage.md`)
   - 対象: すべてのテストファイル

これらの観点が追加されたら、このskillの選択ロジックを更新してください。
