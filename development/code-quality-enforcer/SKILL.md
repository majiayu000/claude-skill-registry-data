---
name: code-quality-enforcer
description: Enforce test quality and prevent implementation shortcuts when writing or modifying code. Use when implementing features, fixing bugs, or refactoring code. Prevents test tampering (FP-1) and implementation shortcuts (FP-2).
---

# Code Quality Enforcer

**Version**: 1.0.0
**対策対象**: FP-1 (テスト改ざん), FP-2 (実装ショートカット)
**優先度**: 最高
**出典**: vibration-diagnosis-prototype失敗事例、obra/superpowers、びーぐるPDF

## The Iron Laws

### Law 1: TDD鉄則 (obra/superpowers)
> NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

### Law 2: Fix Forward, Not Backward
> When tests fail, fix the implementation, never weaken the tests

### Law 3: No Shortcuts
> Every feature requires: error handling, input validation, edge case handling

---

## Workflow

### Phase 1: Pre-Implementation (必須)

**1. Test-First Development**:
```
□ Write a failing test for the feature
□ Run the test (verify it fails for the right reason)
□ Document expected behavior in test
```

**禁止事項**:
- ❌ テストなしで実装を始める
- ❌ 「後でテストを書く」と先送りする
- ❌ 既存のテストを変更してから実装を始める

### Phase 2: Implementation (段階的)

**1. Minimal Implementation**:
```
□ Write the minimum code to pass the test
□ Include error handling
□ Include input validation
□ Run the test (verify it passes)
```

**2. Required Components** (すべて必須):
- **Error Handling**: try-catch, エラーメッセージ、ログ
- **Input Validation**: 型チェック、範囲チェック、null/undefined処理
- **Edge Cases**: 空配列、ゼロ値、境界値の処理

**禁止事項**:
- ❌ エラーハンドリングを省略する
- ❌ 入力バリデーションを省略する
- ❌ "Happy Path" だけ実装する

### Phase 3: Test Failure Response (厳格)

**テストが失敗した場合**:

**Step 1: 診断フェーズ (10分)**:
```
□ エラーログを完全に読む
□ スタックトレースを確認
□ 実際のファイルを確認 (推測禁止)
□ 全ての問題をリストアップ
```

**Step 2: 修正フェーズ**:
```
□ 実装コードを修正 (テストは変更しない)
□ 全ての問題を一度に修正
□ コミット前に再テスト
```

**絶対禁止**:
- ❌ テストの期待値を実装に合わせて変更する
- ❌ アサーションを削除・コメントアウトする
- ❌ テストケースを無効化する
- ❌ テストの厳格さを下げる（toEqual → toContain等）

**例外**: テストそのものにバグがある場合のみ、以下の手順で修正可能:
1. テストのバグであることを証明（実装は仕様通り）
2. 修正前後でテストの厳格さが同等以上であることを確認
3. コメントに修正理由を記録

### Phase 4: Completion Check (完了基準)

**Definition of Done**:
```
✅ 全テストがパス
✅ エラーハンドリングが実装済み
✅ 入力バリデーションが実装済み
✅ エッジケースが処理済み
✅ コードが仕様を完全に満たす
→ 完了
```

**未完了の例**:
- ❌ テストがパスしたが、エラーハンドリングなし
- ❌ "ほとんど動く" 状態
- ❌ 一部のテストだけパス

---

## Prohibited Patterns (アンチパターン)

### Anti-Pattern 1: Test Tampering (テスト改ざん)

**症状**:
- テストが失敗 → テストを変更 → パス

**具体例** (vibration-diagnosis-prototype):
```python
# ❌ 絶対禁止
# 変更前: 厳格なテスト
assert result == expected_value

# 変更後: 緩めたテスト（改ざん）
assert result is not None  # 期待値チェックを削除
```

**正しい対応**:
```python
# ✅ 正しい: テストはそのまま、実装を修正
# テスト（変更なし）
assert result == expected_value

# 実装を修正して期待値を返すようにする
def calculate():
    # バグ修正して expected_value を正しく返す
    return expected_value
```

### Anti-Pattern 2: Implementation Shortcut (実装ショートカット)

**症状**:
- 「簡易実装で後で直す」
- エラーハンドリング省略
- バリデーション省略

**具体例** (vibration-diagnosis-prototype):
```python
# ❌ 絶対禁止: ショートカット実装
def process_data(data):
    return data.process()  # エラーハンドリングなし

# ✅ 正しい: 完全な実装
def process_data(data):
    # Input validation
    if data is None:
        raise ValueError("Data cannot be None")

    # Error handling
    try:
        result = data.process()
    except ProcessingError as e:
        logger.error(f"Processing failed: {e}")
        raise

    # Output validation
    if result is None:
        raise ValueError("Processing returned None")

    return result
```

### Anti-Pattern 3: "後で修正" (Technical Debt Accumulation)

**症状**:
- TODO コメント多数
- 既知のバグを放置
- "一部動けばOK" 思考

**具体例**:
```python
# ❌ 絶対禁止
def important_function(data):
    # TODO: Add error handling later
    # TODO: Add validation later
    return data.process()
```

**正しい対応**:
```python
# ✅ 正しい: 完了基準を満たしてからコミット
def important_function(data):
    # All validation and error handling implemented
    if not isinstance(data, DataType):
        raise TypeError(f"Expected DataType, got {type(data)}")

    try:
        result = data.process()
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise ProcessingError(f"Failed to process: {e}") from e

    return result
```

---

## Multi-layer Defense (3層防御)

このSkillは3層防御システムのLayer 2として機能します:

**Layer 1: Rules** (弱)
- `docs/rules/test.md` - テスト品質ルール
- `docs/rules/implementation.md` - 実装品質ルール
- LLMが無視する可能性あり

**Layer 2: Skills** (中) ← **このSkill**
- **code-quality-enforcer**: コンテキスト起動で強制
- タスク開始時に自動適用
- より強い誘導力

**Layer 3: Hooks** (強)
- `quality_check.sh`: 実行前/後ブロック
- テスト改ざん検出
- 最も強力な防御

---

## Invocation Examples

### Example 1: 新機能実装時

**User**: "ユーザー認証機能を実装してください"

**Skill Response**:
```
Code Quality Enforcer が起動しました。

Phase 1: Test-First Development
まず、認証機能のテストを書きます。

1. どのような認証方式ですか？（JWT, Session, OAuth等）
2. 失敗時の期待動作は？（エラーメッセージ、ステータスコード）
3. 入力バリデーション要件は？（パスワード強度、メール形式等）

テストが完成し、失敗することを確認してから実装を開始します。
```

### Example 2: バグ修正時

**User**: "テストが失敗しています。修正してください"

**Skill Response**:
```
Code Quality Enforcer が起動しました。

Phase 3: Test Failure Response を適用します。

Step 1: 診断フェーズ
□ エラーログを読んでいます...
□ スタックトレースを確認...
□ 実際のファイルを確認...

問題を特定しました:
- 実装の○○行目で期待値と異なる値を返している

Step 2: 修正フェーズ
テストは変更せず、実装コードを修正します。

【重要】テストの期待値を変更することは絶対禁止です。
```

### Example 3: リファクタリング時

**User**: "このコードをリファクタリングしてください"

**Skill Response**:
```
Code Quality Enforcer が起動しました。

リファクタリング前チェック:
□ 既存テストがすべてパスしていますか？
□ テストカバレッジは十分ですか？

リファクタリング中:
□ テストを先に実行（Green状態確認）
□ 小さな変更を加える
□ テストを再実行（Green維持確認）
□ コミット

リファクタリング後:
✅ 全テストがパス
✅ 機能的には変更なし
✅ コード品質が向上
```

---

## Best Practices

### 1. Test Quality (テスト品質)

**Good Tests**:
- 単一の責任を持つ（1 test = 1 assertion concept）
- 独立している（テスト順序に依存しない）
- 高速である（ミリ秒単位）
- 決定的である（常に同じ結果）

**Bad Tests**:
- 複数の概念をテスト
- 他のテストに依存
- 外部サービスに依存（モック使用推奨）
- ランダム要素がある

### 2. Error Messages (エラーメッセージ)

**Good**:
```python
raise ValueError(f"Invalid email format: '{email}'. Expected format: user@domain.com")
```

**Bad**:
```python
raise ValueError("Invalid input")
```

### 3. Validation Patterns (バリデーションパターン)

**Input Validation**:
```python
# Type check
if not isinstance(value, ExpectedType):
    raise TypeError(f"Expected {ExpectedType}, got {type(value)}")

# Range check
if value < MIN or value > MAX:
    raise ValueError(f"Value {value} out of range [{MIN}, {MAX}]")

# Null check
if value is None:
    raise ValueError("Value cannot be None")
```

---

## Related Resources

### Internal
- `docs/rules/test.md` - テスト品質ルール詳細
- `docs/rules/implementation.md` - 実装品質ルール詳細
- `test-process-requirements.md` - テストプロセス要件

### External
- obra/superpowers - TDD Skill実装例
- びーぐるPDF - テスト品質のベストプラクティス
- WORK_PROCESS_PROTOCOLS - 証拠ベース思考

### Phase 3成果物
- `step3.5-failure-case-analysis.md` - FP-1, FP-2詳細分析
- `CRITICAL_FAILURE_REPORT_20251226.md` - vibration-diagnosis-prototype失敗事例

---

## Completion Criteria

このSkillは以下の条件で完了とします:

```yaml
✅ Test-First: テストを先に書いた
✅ All Tests Pass: 全テストがパス
✅ Error Handling: エラーハンドリング実装済み
✅ Input Validation: 入力バリデーション実装済み
✅ Edge Cases: エッジケース処理済み
✅ No Shortcuts: 実装ショートカットなし
✅ No Tampering: テスト改ざんなし
```

**不完全な状態での完了宣言は禁止**

---

**注意**: このSkillは自動的に起動されます。無効化したい場合は `.claude/settings.local.json` から削除してください。
