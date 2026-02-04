---
name: code-impact-checker
description: 破壊的変更に基づいてプロジェクト内のコードを検索し、影響を受けるファイルと行を特定する。テストカバレッジも確認する
allowed-tools: Read, Grep, Glob
---

# コード影響分析スキル

**役割**: コード検索に特化。破壊的変更の影響を受けるコードを特定する。

**入力**: 検索対象のAPI/パターン、ソースディレクトリ、テストディレクトリ（呼び出し元から渡される）

## 検索タスク

### 1. 影響箇所の検索

破壊的変更ごとに、該当するコードを検索:

```bash
# import文の検索
grep -r "import.*{.*oldAPI.*}.*from" --include="*.ts" --include="*.tsx" src/

# 関数呼び出しの検索
grep -rn "oldFunction\s*(" --include="*.ts" --include="*.tsx" src/

# Props使用の検索
grep -rn "deprecatedProp" --include="*.tsx" src/
```

### 2. テストファイルの特定

```bash
# テストファイルのパターン
**/*.test.ts
**/*.test.tsx
**/*.spec.ts
**/*.spec.tsx
**/__tests__/**/*
```

### 3. カバレッジ確認

影響を受けるファイルに対応するテストがあるか確認:

| ソースファイル | テストファイル検索パターン |
|--------------|------------------------|
| src/hooks/useData.ts | src/hooks/useData.test.ts, src/hooks/__tests__/useData.test.ts |
| src/utils/format.ts | src/utils/format.test.ts, src/utils/__tests__/format.test.ts |

## 出力フォーマット

```json
{
  "affectedFiles": [
    {
      "file": "src/components/Example.tsx",
      "lines": [15, 42, 78],
      "pattern": "useRouter",
      "context": "import { useRouter } from 'next/router'"
    }
  ],
  "testCoverage": {
    "covered": [
      {
        "source": "src/hooks/useData.ts",
        "test": "src/hooks/__tests__/useData.test.ts"
      }
    ],
    "notCovered": [
      "src/utils/format.ts"
    ]
  },
  "summary": {
    "totalFiles": 5,
    "totalLines": 12,
    "testCoverage": "60%"
  }
}
```

## 検索パターン集

### React
```regex
# Hooks
use(Effect|State|Callback|Memo|Ref|Context)\s*\(

# コンポーネント
<ComponentName\s+[^>]*prop=
```

### Next.js
```regex
# Router
import.*from\s+['"]next/router['"]
useRouter\s*\(\)

# Pages
getServerSideProps|getStaticProps|getStaticPaths

# App Router
import.*from\s+['"]next/navigation['"]
```

### 一般
```regex
# 特定の関数
functionName\s*\(

# 特定のimport
import\s*{\s*[^}]*targetName[^}]*}\s*from

# 特定のメソッド
\.methodName\s*\(
```
