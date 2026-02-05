---
name: scan-existing-implementation
description: プロジェクト内の既存ユーティリティ・実装をスキャンして発見するスキル。プランニング時に再利用可能なコードを見つけ、車輪の再発明を防ぐ。
---

# Existing Implementation Scanner

実装タスクに対して、プロジェクト内の既存ユーティリティ・実装を発見する。

## 実行手順

### 1. タスク分析

実装しようとしているタスクを分析し、必要な処理を列挙：

- データ変換・操作（コピー、変換、フォーマット）
- リソース管理（解放、クリーンアップ）
- キャッシュ・メモ化
- API呼び出し・外部連携
- 状態管理
- UI/コンポーネント

### 2. 優先ディレクトリの決定

タスクの性質に基づいてスキャン優先度を決定
以下は例

| カテゴリ          | 優先スキャンパス                |
| ----------------- | ------------------------------- |
| UI/コンポーネント | `src/components/`, `src/hooks/` |
| データ処理        | `src/lib/utils/`, `src/lib/`    |
| 状態管理          | `src/stores/`                   |
| バックエンド連携  | `backend/`, `src/lib/`          |
| 型定義            | `types/`                        |

### 3. スキャン実行

優先度の高いディレクトリから順に実行：

**Step 3.1: ユーティリティファイルの特定**

Globでファイル名パターン検索：

- `**/utils*.ts`
- `**/*-utils.ts`
- `**/*Helper*.ts`
- `**/*-helper*.ts`

**Step 3.2: export関数の検索**

Grepで優先ディレクトリ内のexport関数を検索：

- `export function`
- `export const`

**Step 3.3: 特定機能キーワード検索**

処理に応じたキーワードで検索：

| 処理               | 検索キーワード                            |
| ------------------ | ----------------------------------------- |
| コピー             | `copy`, `clone`, `duplicate`              |
| キャッシュ         | `cache`, `memoize`, `store`               |
| リソース解放       | `dispose`, `cleanup`, `release`, `using`  |
| 変換               | `convert`, `transform`, `parse`, `format` |
| バリデーション     | `validate`, `check`, `assert`             |
| エラーハンドリング | `Result`, `ok`, `err`, `neverthrow`       |

### 4. レポート出力

以下の形式で発見した実装を報告：

```
## スキャン結果

### 直接利用可能
- `src/lib/pdf/utils.ts`
  - `copyArrayBuffer()` - ArrayBufferのコピー（Transferable対策）
- `src/lib/utils/disposable.ts`
  - `disposableCanvas()` - using構文でcanvasを自動解放
  - `disposableBlobUrl()` - using構文でBlob URLを自動解放

### 参考パターン
- `src/hooks/usePdfConfig.ts`
  - `PDF_OPTIONS` - 共有定数をhookと非hook両方から参照するパターン

### 該当なし
- [処理X] に対応する既存実装は見つかりませんでした
```

## 重要なルール

1. **発見優先**: 新規実装を提案する前に、必ず既存実装をスキャン
2. **パス明記**: 発見した実装はプロジェクトルートからの相対パスで報告
3. **用途説明**: 各実装が何に使えるか、1行で説明
4. **不足も報告**: 見つからなかった処理も明示し、新規実装が必要であることを示す
5. **コード例**: 発見した実装の使用例を簡潔に示す
