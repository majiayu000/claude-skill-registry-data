---
name: refactor
description: >-
  ユーザーが「リファクタリング」「コードを整理」「可読性を上げて」「きれいにして」「保守性を改善」等と要求した時に発動。
  機能を変更せずに、コードの保守性・可読性・パフォーマンスを向上させる。
  テストが存在する場合は必ずテストをパスすることを確認し、機能不変を保証する。
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

### 手順
1. **対象の特定**: リファクタリング対象のファイル/関数を特定
2. **既存テストの確認**:
   - 対応する `*_test.go` を確認
   - `go test ./...` を実行してベースライン確立（全テストがパスすることを確認）
3. **リファクタリング計画**: 以下の観点で改善機会を特定
   - 命名改善（変数名、関数名の明確化）
   - 関数分割（長すぎる関数、複数の責任を持つ関数）
   - 重複コード削除（DRY原則）
   - 複雑な条件式の簡素化
   - マジックナンバーの定数化
   - エラーハンドリングの改善
4. **リファクタリング実施**: 小さなステップで段階的に変更
5. **テスト実行**: 各ステップ後に `go test ./...` で機能不変を確認
6. **コード品質確認**:
   - `go fmt ./...` でフォーマット
   - `go vet ./...` で静的解析
7. **コミット**: 変更が成功したら、適切なメッセージでコミット（`refactor: ...`形式）

### リファクタリングパターン

#### 1. 命名改善
```go
// Before
func f(n []int) int { ... }

// After
func Sum(numbers []int) int { ... }
```

#### 2. 関数分割
```go
// Before: 1つの関数が複数の責任
func ProcessData(data []byte) error {
    // バリデーション
    // パース
    // 変換
    // 保存
}

// After: 単一責任に分割
func ValidateData(data []byte) error { ... }
func ParseData(data []byte) (*Data, error) { ... }
func TransformData(data *Data) *Result { ... }
func SaveResult(result *Result) error { ... }
```

#### 3. 重複削除
```go
// Before: 重複コード
func AddUser(u User) { db.Insert("users", u) }
func AddPost(p Post) { db.Insert("posts", p) }

// After: 汎用化
func Add[T any](table string, entity T) { db.Insert(table, entity) }
```

#### 4. マジックナンバーの定数化
```go
// Before
if len(items) > 100 { ... }

// After
const MaxItems = 100
if len(items) > MaxItems { ... }
```

### 重要な原則
- ✅ **機能不変**: 外部から見た動作は一切変更しない
- ✅ **テストファースト**: リファクタ前に必ずテストを実行
- ✅ **小さなステップ**: 一度に多くを変更しない
- ✅ **継続的な検証**: 各ステップ後にテスト実行
- ❌ **新機能追加**: リファクタリングと機能追加は分離

### リファクタリング対象の優先順位
1. **High**: 複雑度が高く、バグを生みやすい箇所
2. **Medium**: 頻繁に変更される箇所
3. **Low**: 安定していて変更頻度が低い箇所

### 出力例
```markdown
# Refactoring Report

## Target
- File: `pkg/calc/sum.go`

## Changes Applied
1. ✅ Improved function naming clarity
2. ✅ Added nil check for defensive programming
3. ✅ Simplified loop condition

## Test Results
✅ All tests pass (before and after)
- Tests run: 5
- Coverage: 85% (unchanged)

## Performance Impact
No performance regression detected
```

### ベストプラクティス
- リファクタリング前後でベンチマークを取る（パフォーマンス改善の場合）
- コミットメッセージに「何を」「なぜ」を明記
- レビューしやすいように、変更を論理的に分割
