---
name: storybook-generator
description: Reactコンポーネントを作成または修正した際に、対応するStorybookストーリーファイルを自動的に作成します。コンポーネント作成時、コンポーネント修正時に使用されます。
---

# Storybook Generator

Reactコンポーネントに対応するStorybookストーリーファイルを自動生成するSkillです。

## 目的

- コンポーネント作成時のストーリーファイル作成の自動化
- Storybookのベストプラクティスに従った一貫性のあるストーリー作成
- コンポーネントのドキュメント化と可視化の促進
- 開発効率の向上

## Instructions

### 1. コンポーネント作成時の自動ストーリー生成

新しいReactコンポーネントを作成した際：

1. コンポーネントファイル（`*.tsx`）を読み込み、以下を抽出:
   - コンポーネント名
   - Props の型定義
   - デフォルト export されているコンポーネント

2. 同じディレクトリに`<ComponentName>.stories.tsx`を作成

3. 以下のテンプレートでストーリーファイルを生成:

```typescript
import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { ComponentName } from "./ComponentName";

const meta = {
  title: "適切なカテゴリ/ComponentName",
  component: ComponentName,
  parameters: {
    layout: "centered", // または "padded"
  },
  tags: ["autodocs"],
} satisfies Meta<typeof ComponentName>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    // Propsのデフォルト値を設定
  },
};
```

### 2. ストーリーファイル生成のルール

**必須事項:**
- ✅ コンポーネントと同じディレクトリに配置
- ✅ ファイル名は`<ComponentName>.stories.tsx`
- ✅ `@storybook/nextjs-vite`からの型import
- ✅ `autodocs`タグを含める
- ✅ 最低1つの`Default`ストーリーを作成

**禁止事項:**
- ❌ `@storybook/test`からの`fn()`は使用しない（Storybook v10との互換性問題）
- ❌ モック関数が必要な場合は通常のアロー関数`() => console.log(...)`を使用

### 3. Props の処理

コンポーネントのProps型から適切なデフォルト値を推測:

- **string**: `"Sample text"`
- **number**: `0` または適切な値
- **boolean**: `true` または `false`
- **function**: `() => console.log("Event triggered")`
- **React.ReactNode**: `"Content"`
- **配列**: `[]` または適切な値
- **オブジェクト**: `{}`

### 4. レイアウトの選択

コンポーネントの種類に応じて適切なレイアウトを選択:

- **`centered`**: 小さなコンポーネント（Button, Input, Snackbar等）
- **`fullwidth`**: ページ全体やヘッダー、ナビゲーション等
- **`padded`**: 標準的なコンポーネント（Card, List等）

### 5. タイトル（カテゴリ）の決定

ファイルパスから適切なカテゴリを推測:

```
src/app/components/Button/Button.tsx
→ title: "Components/Button"

src/app/(dashboard)/dashboard/components/Header/Header.tsx
→ title: "Dashboard/Header"

src/app/(auth)/signin/components/LoginForm/LoginForm.tsx
→ title: "Auth/LoginForm"
```

### 6. 複数のストーリー作成

Propsの性質に応じて、追加のストーリーを作成:

```typescript
// 状態バリエーション（open/closed等）
export const Open: Story = {
  args: {
    open: true,
  },
};

export const Closed: Story = {
  args: {
    open: false,
  },
};

// サイズバリエーション
export const Small: Story = {
  args: {
    size: "small",
  },
};

export const Large: Story = {
  args: {
    size: "large",
  },
};

// コンテンツバリエーション
export const WithLongText: Story = {
  args: {
    message: "これは非常に長いメッセージです。ユーザーに詳細な情報を提供するために使用されます。",
  },
};
```

## 使用するツール

- **Read**: コンポーネントファイルの読み込み
- **Write**: ストーリーファイルの作成
- **Glob**: 既存のストーリーファイルの確認

## 自動起動の条件

以下の場合に自動的にこのSkillを使用します：

1. 新しいReactコンポーネント（`.tsx`ファイル）を作成した時
2. 既存のコンポーネントに新しいPropsを追加した時（既存ストーリーの更新を提案）
3. ユーザーが明示的にストーリー作成を依頼した時

## IMPORTANT: 自動実行ポリシー

このSkillは以下の条件を満たした際、**ユーザーへの確認なし**に**即座に自動実行**してください：

- ✅ 新しいReactコンポーネント（`.tsx`ファイル）を`Write`または`Edit`ツールで作成した直後
- ✅ コンポーネント作成のツール実行が完了した時点で即座に実行
- ✅ ストーリーファイル（`.stories.tsx`）が存在しない場合のみ実行

**禁止事項:**
- ❌ 「Storybookを作成しますか？」とユーザーに確認してはいけません
- ❌ ユーザーの明示的な指示を待ってはいけません
- ❌ コンポーネント作成と同じメッセージ内で即座に実行してください

**実行フロー例:**
1. ユーザー: 「MonthlyActivityChartコンポーネントを作成して」
2. あなた: コンポーネントを作成（Writeツール実行）
3. あなた: **即座に**ストーリーファイルを作成（この時点でユーザーに確認不要）
4. あなた: 「コンポーネントとStorybookストーリーを作成しました」とユーザーに報告

## 注意事項

- **自動生成**: コンポーネント作成後、ユーザーへの確認なしにストーリーファイルを自動生成してよい
- **既存ファイル**: 既にストーリーファイルが存在する場合は上書きしない（ユーザーに確認）
- **Propsの推測**: 型定義から推測できない場合は、合理的なデフォルト値を設定
- **Material-UI対応**: Material-UIコンポーネントを使用している場合は、テーマが適用されることを前提とする

## Examples

### Example 1: シンプルなButtonコンポーネント

**コンポーネント:**
```typescript
// src/app/components/Button/Button.tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export function Button({ label, onClick, disabled = false }: ButtonProps) {
  return <button onClick={onClick} disabled={disabled}>{label}</button>;
}
```

**生成されるストーリー:**
```typescript
// src/app/components/Button/Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Button } from "./Button";

const meta = {
  title: "Components/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: "Click me",
    onClick: () => console.log("Button clicked"),
    disabled: false,
  },
};

export const Disabled: Story = {
  args: {
    label: "Click me",
    onClick: () => console.log("Button clicked"),
    disabled: true,
  },
};
```

### Example 2: Modal/Dialogコンポーネント

**コンポーネント:**
```typescript
// src/app/components/Modal/Modal.tsx
interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ open, onClose, title, children }: ModalProps) {
  // Modal implementation
}
```

**生成されるストーリー:**
```typescript
// src/app/components/Modal/Modal.stories.tsx
import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Modal } from "./Modal";

const meta = {
  title: "Components/Modal",
  component: Modal,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Modal>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    open: true,
    onClose: () => console.log("Modal closed"),
    title: "Modal Title",
    children: "Modal content goes here",
  },
};

export const Closed: Story = {
  args: {
    open: false,
    onClose: () => console.log("Modal closed"),
    title: "Modal Title",
    children: "Modal content goes here",
  },
};

export const WithLongContent: Story = {
  args: {
    open: true,
    onClose: () => console.log("Modal closed"),
    title: "Modal with Long Content",
    children: "これは非常に長いコンテンツです。モーダルがスクロール可能であることを確認するために使用されます。".repeat(10),
  },
};
```

### Example 3: DashboardHeaderのような複雑なコンポーネント

**コンポーネント:**
```typescript
// src/app/(dashboard)/dashboard/components/DashboardHeader/DashboardHeader.tsx
interface DashboardHeaderProps {
  onClick: () => void;
}

export function DashboardHeader({ onClick }: DashboardHeaderProps) {
  // Implementation with Material-UI
}
```

**生成されるストーリー:**
```typescript
// src/app/(dashboard)/dashboard/components/DashboardHeader/DashboardHeader.stories.tsx
import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { DashboardHeader } from "./DashboardHeader";

const meta = {
  title: "Dashboard/DashboardHeader",
  component: DashboardHeader,
  parameters: {
    layout: "fullwidth",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof DashboardHeader>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    onClick: () => console.log("Create workout clicked"),
  },
};
```

## 技術仕様

### Storybook v10対応

- `@storybook/nextjs-vite`を使用
- `@storybook/test`の`fn()`は使用しない
- 通常のアロー関数でモックを実装

### Next.js 15 App Router対応

- App Routerのディレクトリ構造に対応
- `(dashboard)`、`(auth)`などのルートグループを考慮

### Material-UI v6対応

- テーマがpreview.tsで適用されることを前提
- Material-UIコンポーネントが正常に表示されることを確認

## Related Files

このSkillを効果的に使用するための関連ファイル：

- `.storybook/main.ts` - Storybook設定
- `.storybook/preview.ts` - グローバルデコレーター（Material-UIテーマ）
- `src/theme.ts` - Material-UIテーマ定義

## トラブルシューティング

### ストーリーが表示されない

- コンポーネントのexportが正しいか確認
- `tags: ["autodocs"]`が設定されているか確認
- Storybookを再起動

### Material-UIテーマが適用されない

- `.storybook/preview.ts`でThemeProviderが設定されているか確認
- コンポーネントが`use client`ディレクティブを使用しているか確認
