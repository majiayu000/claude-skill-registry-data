---
name: coding-rules
description: TypeScript/React コーディング規約、インポート順序、Server/Client Components使い分け、コミット規約。コード実装、レビュー、リファクタリング時に使用。
---

# コーディング規約 (MUED LMS v2)

## TypeScript/React

- Strict mode 有効
- 関数コンポーネント + Hooks
- Props 型定義必須
- `any` 禁止（やむを得ない場合はコメント必須）

## ファイル構成

- 1ファイル1コンポーネント
- 200行超えたら分割検討
- UI層とロジックを分離

## インポート順序

```typescript
// 1. React/Next.js
import { useState } from 'react';
import { useRouter } from 'next/navigation';

// 2. 外部ライブラリ
import { clsx } from 'clsx';

// 3. 内部モジュール
import { Button } from '@/components/ui/button';

// 4. 型定義
import type { User } from '@/types';
```

## Server Components vs Client Components

```typescript
// デフォルト: Server Component（use client なし）
// データフェッチ、静的レンダリングに使用

// Client Component が必要な場合のみ
'use client';
// useState, useEffect, イベントハンドラ, ブラウザAPI使用時
```

## コミット規約

Conventional Commits 形式を使用：

```
feat: 新機能追加
fix: バグ修正
docs: ドキュメント
refactor: リファクタリング
test: テスト
chore: その他
```

## PR 作成時の確認事項

1. `npm run typecheck` パス
2. `npm run lint` パス
3. `npm run test` パス
4. 必要に応じて E2E テスト
