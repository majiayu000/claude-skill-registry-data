---
name: reconcile-code
description: >
  Reconcile existing code with the confirmed VDM-SL specification.
  Compare spec vs code item-by-item, generate a diff report,
  produce code fixes prioritized by Finding category, and auto-generate tests.
  Triggered by: "reconcile code with spec", "fix code to match spec",
  「仕様とコードを照合して」「コードを仕様に合わせて」「差分を出して」「コードを直して」
metadata:
  version: "1.3.0"
---

# Reconcile Code Skill

## Overview / 概要

This skill reconciles existing code with a confirmed VDM-SL specification through systematic comparison, generates diff reports, produces prioritized code fixes, and auto-generates comprehensive tests.

このスキルは、確認済みのVDM-SL仕様との間で既存コードを体系的に比較し、差分レポートを生成し、優先度付きコード修正を生成し、包括的なテストを自動生成します。

---

## Step 1: Item-by-Item Comparison

### Type Definitions

**EN:** For each VDM-SL type definition in the confirmed spec, locate the corresponding code type (TypeScript interface/type, Python dataclass, etc.):
- Verify all field names match spec exactly
- Verify all field types match spec types (accounting for language-specific representations)
- Verify optional/required markers match (nullable, Optional[], etc.)
- Check for extra fields in code not in spec
- Check for missing fields in code that are in spec

**JP:** 確認済み仕様のVDM-SL型定義ごとに、対応するコード型（TypeScriptインターフェース/型、Pythonデータクラスなど）を見つけます:
- すべてのフィールド名が仕様と正確に一致することを確認
- すべてのフィールド型が仕様型と一致することを確認（言語固有の表現を考慮）
- オプション/必須マーカーが一致することを確認（nullable、Optional[]など）
- 仕様にない仕様にないコード内の余分なフィールドをチェック
- 仕様にあるがコードにない欠落フィールドをチェック

**Status Codes:**
- ✅ Match: All fields present, types correct, required/optional markers align
- ⚠️ Partial: Some fields missing/extra, or minor type representation differences that don't affect runtime
- ❌ Mismatch: Type definitions are incompatible, will cause runtime errors
- 🔍 Not Found: No corresponding type found in code

### Pre-conditions

**EN:** For each VDM-SL pre-condition (guards in the function specification), find the corresponding code implementation:
- Look for guard clauses, early returns with error checks, parameter validation
- Verify the guard logic is equivalent to the pre-condition
- Check that appropriate errors/exceptions are thrown on violation
- Identify if the guard is implicit (e.g., type system enforces) or explicit (runtime check)

**JP:** VDM-SL仕様の各前提条件（関数仕様のガード）について、対応するコード実装を見つけます:
- ガード句、エラーチェック付きの早期リターン、パラメータ検証を探す
- ガードロジックが前提条件と等価であることを確認
- 違反時に適切なエラー/例外がスロウされることを確認
- ガードが暗黙的（型システムが強制）か明示的（実行時チェック）かを識別

**Status Codes:**
- ✅ Match: Guard logic matches spec, error handling present
- ⚠️ Partial: Guard exists but may be weaker than spec, or error handling incomplete
- ❌ Mismatch: Guard logic differs from spec or missing entirely
- 🔍 Not Found: No corresponding guard in code

### Post-conditions

**EN:** For each VDM-SL post-condition (expected behavior after operation), verify the code implements it:
- Check return value structure and content against post-condition guarantees
- Verify state mutations match post-condition expectations
- Confirm side effects are correctly implemented
- Check that return values are validated before returning

**JP:** VDM-SL仕様の各後提条件（操作後の期待される動作）について、コードがそれを実装していることを確認します:
- 後提条件の保証に対して戻り値の構造と内容を確認
- 状態変異が後提条件の期待と一致することを確認
- 副作用が正しく実装されていることを確認
- 戻り値が戻る前に検証されることを確認

**Status Codes:**
- ✅ Match: Return values match post-condition, state changes correct
- ⚠️ Partial: Post-condition partially implemented, some guarantees missing
- ❌ Mismatch: Implementation doesn't match post-condition behavior
- 🔍 Not Found: No implementation found

### Invariants

**EN:** For each VDM-SL class invariant, identify where validation must occur:
- Find invariant checks at object construction points
- Check all mutation points that could violate invariant
- Verify invariants are enforced consistently
- Identify if invariants are encoded in types or checked at runtime

**JP:** VDM-SLクラス不変式ごとに、検証が必要な場所を特定します:
- オブジェクト構築時の不変式チェックを見つける
- 不変式を違反する可能性のあるすべての変異ポイントをチェック
- 不変式が一貫して強制されることを確認
- 不変式が型にエンコードされているか実行時にチェックされるかを識別

**Status Codes:**
- ✅ Match: Invariants enforced at all critical points
- ⚠️ Partial: Invariants enforced at construction but not all mutation points
- ❌ Mismatch: Invariants violated or inconsistently enforced
- 🔍 Not Found: No invariant enforcement found

### Reconciliation Table Output

Present results in a formatted table:

```
┌─────────────────────┬──────────┬─────────────────────┬─────────────┐
│ Spec Item           │ Status   │ Code Location       │ Note        │
├─────────────────────┼──────────┼─────────────────────┼─────────────┤
│ User (Type)         │ ✅ Match │ src/User.ts:10-25   │ -           │
│ createUser (Pre)    │ ❌ Mis   │ src/User.ts:30      │ Missing null│
│ createUser (Post)   │ ⚠️ Part  │ src/User.ts:30-40   │ Partial ID  │
│ UserInvariant       │ 🔍 Found │ -                   │ No check    │
└─────────────────────┴──────────┴─────────────────────┴─────────────┘
```

---

## Step 2: Fix Generation (prioritized by Finding category)

### Priority High: Bug Fixes

**EN:** Code behavior differs from confirmed spec, causing runtime failures or incorrect results:
- Code implements wrong logic
- Missing critical guards that could cause crashes
- State mutations don't match spec guarantees
- Error types are wrong or errors aren't thrown

For each Bug Finding:
1. Show the specific code that's wrong (with line numbers)
2. Explain how it differs from the spec
3. Generate the fixed code (before/after diff)
4. Include the Finding reference and confidence level

Example structure:
````
Bug Fix #1: createUser() pre-condition validation missing
Finding: BUG-001 [Confidence: High]
Spec requirement: User email must be non-empty string
Code issue: No email validation before DB insert
Location: src/User.ts:35-45

Before:
```typescript
function createUser(user: any) {
  return db.insert(user);
}
```

After:
```typescript
function createUser(user: User) {
  if (!user.email || user.email.trim() === '') {
    throw new ValidationError('Email is required and must be non-empty');
  }
  return db.insert(user);
}
```
````

**JP:** コード動作が確認済み仕様と異なり、実行時エラーまたは不正な結果を引き起こす:
- コードが間違ったロジックを実装
- クラッシュを引き起こす可能性のある重要なガード欠落
- 状態変異が仕様の保証と一致しない
- エラー型が間違っているか、エラーがスロウされていない

### Priority Medium: Spec Gap Fills

**EN:** Spec defines behavior but code lacks implementation:
- Missing validation logic
- Missing runtime contract checks
- Missing helper methods referenced in spec
- Missing error handling for exceptional cases

For each Spec Gap Finding:
1. Explain what spec item is unimplemented
2. Show where the code should have this logic
3. Generate new code to implement the gap
4. Include runtime contract checks

**JP:** 仕様は動作を定義していますが、コードは実装を欠いています:
- 検証ロジックを欠落
- 実行時契約チェックを欠落
- 仕様で参照されているヘルパーメソッドを欠落
- 例外的なケースのエラー処理を欠落

### Priority Low: Type Safety Improvements

**EN:** Strengthen types to prevent potential issues:
- Replace overly permissive types (any, object) with specific types
- Add missing null/undefined checks
- Add boundary value validation
- Improve type inference with better annotations

**JP:** 潜在的な問題を防ぐための型の強化:
- 過度に許容度の高い型（any、object）を特定の型に置き換える
- 欠落したnull/undefinedチェックを追加
- 境界値検証を追加
- より良い注釈で型推論を改善

### Fix Metadata

Each fix must include:
```yaml
finding_id: BUG-001 or SPEC-GAP-002 or TYPE-SAFE-003
spec_reference: "User :: createUser pre-condition"
affected_file: src/User.ts
line_range: 35-45
severity: High | Medium | Low
confidence: High | Medium | Low
before_code: |
  function createUser(user: any) { ... }
after_code: |
  function createUser(user: User) { ... }
explanation: "Added email validation guard missing from pre-condition"
```

---

## Step 3: Test Auto-Generation

### Pre-condition Tests

**EN:** For each pre-condition, generate tests covering:

1. **Valid input test** — Operation succeeds without throwing
   - Name: `test_<operationName>_with_valid_inputs_succeeds`
   - Verify: No exception thrown, return value present

2. **Pre-condition violation tests** — Each condition creates a separate test
   - Name: `test_<operationName>_violates_<conditionName>_throws_<ErrorType>`
   - Verify: Specific error type thrown with correct message
   - Vary: One condition violation per test

3. **Boundary value tests** — Test limits of pre-condition
   - Name: `test_<operationName>_<conditionName>_boundary_<value>`
   - Verify: Behavior at min/max allowed values

Example (Jest):
```javascript
describe('User.createUser pre-conditions', () => {
  test('valid input succeeds', () => {
    const user = { email: 'test@example.com', name: 'Test' };
    expect(() => User.createUser(user)).not.toThrow();
  });

  test('empty email throws ValidationError', () => {
    const user = { email: '', name: 'Test' };
    expect(() => User.createUser(user))
      .toThrow(ValidationError);
    expect(() => User.createUser(user))
      .toThrow('Email is required');
  });

  test('null email throws ValidationError', () => {
    const user = { email: null, name: 'Test' };
    expect(() => User.createUser(user))
      .toThrow(ValidationError);
  });
});
```

**JP:** 各前提条件について、以下をカバーするテストを生成:

1. **有効入力テスト** — 操作がスロウなしで成功
2. **前提条件違反テスト** — 各条件が個別のテストを作成
3. **境界値テスト** — 前提条件の制限をテスト

### Post-condition Tests

**EN:** For each post-condition, generate tests:

1. **Valid input verification** — Return value matches post-condition
   - Name: `test_<operationName>_returns_correct_<property>`
   - Verify: Specific properties in return value match spec

2. **State change verification** — State mutations match post-condition
   - Name: `test_<operationName>_state_mutation_<stateName>`
   - Verify: State changed as guaranteed by post-condition

Example (Jest):
```javascript
describe('User.createUser post-conditions', () => {
  test('returns user with assigned ID', () => {
    const user = { email: 'test@example.com', name: 'Test' };
    const result = User.createUser(user);
    expect(result).toHaveProperty('id');
    expect(typeof result.id).toBe('string');
  });

  test('persists user to database', () => {
    const user = { email: 'test@example.com', name: 'Test' };
    const result = User.createUser(user);
    const retrieved = User.findById(result.id);
    expect(retrieved).toEqual(result);
  });
});
```

**JP:** 各後提条件について:

1. **有効入力検証** — 戻り値が後提条件と一致
2. **状態変化検証** — 状態変異が後提条件と一致

### Invariant Tests

**EN:** For each invariant, generate:

1. **Valid construction test** — Object created with valid state
   - Name: `test_<className>_valid_construction_succeeds`
   - Verify: Object created, invariant holds

2. **Invariant violation at construction** — Invalid construction fails
   - Name: `test_<className>_violates_<invariantName>_at_construction_fails`
   - Verify: Construction throws appropriate error

3. **Invariant violation at mutation** — Attempted mutation rejected
   - Name: `test_<className>_mutation_violates_<invariantName>_rejected`
   - Verify: Mutation prevented or error thrown

Example (Jest):
```javascript
describe('User invariants', () => {
  test('valid user construction succeeds', () => {
    const user = new User('test@example.com', 'Test', 18);
    expect(user.email).toBe('test@example.com');
    expect(user.age).toBeGreaterThanOrEqual(0);
  });

  test('negative age at construction fails', () => {
    expect(() => new User('test@example.com', 'Test', -1))
      .toThrow('Age must be non-negative');
  });

  test('setting negative age rejected', () => {
    const user = new User('test@example.com', 'Test', 18);
    expect(() => { user.age = -1; })
      .toThrow('Age must be non-negative');
  });
});
```

**JP:** 各不変式について:

1. **有効な構築テスト** — 有効な状態でオブジェクトが作成される
2. **不変式違反テスト** — 無効な構築が失敗
3. **変異違反テスト** — 試行された変異が拒否される

### Finding-Specific Tests

**EN:** For each Bug or Spec Gap Finding:

1. **Regression test** — Tests that the bug fix works
   - Reference the Finding ID
   - Test the specific scenario that was failing
   - Verify fix behavior

2. **New behavior test** — Tests the newly implemented feature
   - Reference the Finding ID and Spec item
   - Test the new implementation

Example:
```javascript
describe('Bug Fix: BUG-001 - Email validation missing', () => {
  test('regression: empty email now properly rejected', () => {
    const user = { email: '', name: 'Test' };
    expect(() => User.createUser(user))
      .toThrow(ValidationError);
  });

  test('regression: whitespace-only email rejected', () => {
    const user = { email: '   ', name: 'Test' };
    expect(() => User.createUser(user))
      .toThrow(ValidationError);
  });
});

describe('Spec Gap Fill: SPEC-GAP-001 - User password validation', () => {
  test('password must be at least 8 characters', () => {
    const user = { email: 'test@example.com', password: 'short' };
    expect(() => User.createUser(user))
      .toThrow(/at least 8 characters/);
  });
});
```

**JP:** 各Bug または Spec Gap Finding について:

1. **回帰テスト** — バグ修正が機能することをテスト
2. **新しい動作テスト** — 新たに実装されたフィーチャーをテスト

### Test Framework Detection

Detect the test framework from:
1. Package.json dependencies (jest, vitest, mocha, pytest, unittest, etc.)
2. Existing test files in project (*.test.js, *.spec.js, test_*.py, *_test.py, etc.)
3. tsconfig.json or pytest.ini configuration
4. If detection fails, ask user or default to project convention

Generate tests using the detected framework's syntax and conventions.

### Test Organization

- **File location:** Place tests in same directory structure as source, or in dedicated test/ directory
- **File naming:** Match project convention (*.test.js, *.spec.js, test_*.py, etc.)
- **Test grouping:** Use describe/test blocks, test classes, or test functions per framework
- **Test data:** Use fixtures/factories if they exist in project
- **Additive only:** Never delete or modify existing tests
- **Integration:** Import/reference production code same way existing tests do

---

## Step 4: Reconciliation Report

Generate a comprehensive summary:

### Report Structure

**EN:**

```markdown
# Reconciliation Report: [Project Name]

## Executive Summary
- Total spec items analyzed: N
- Matched: N (X%)
- Partial matches: N (X%)
- Mismatches: N (X%)
- Not found: N (X%)

## Finding Summary
- Bug Fixes (High priority): N
- Spec Gap Fills (Medium priority): N
- Type Safety Improvements (Low priority): N

## Test Generation Summary
- Pre-condition tests generated: N
- Post-condition tests generated: N
- Invariant tests generated: N
- Finding-specific tests generated: N
- Total tests generated: N

## Files Modified
- src/File1.ts (N fixes)
- src/File2.ts (N fixes)
- test/File1.test.ts (new file, N tests)

## Detailed Findings
[List each finding with details]

## Remaining Manual Work
[Identify any items that require manual review]
```

**JP:**

```markdown
# 照合レポート: [プロジェクト名]

## エグゼクティブサマリー
- 分析された仕様項目の合計: N
- 一致: N (X%)
- 部分一致: N (X%)
- 不一致: N (X%)
- 見つからない: N (X%)

## 調査結果の要約
- バグ修正（高優先度）: N
- 仕様ギャップ埋め（中優先度）: N
- 型安全性改善（低優先度）: N

## テスト生成の要約
- 生成された前提条件テスト: N
- 生成された後提条件テスト: N
- 生成された不変式テスト: N
- 生成された調査結果特定テスト: N
- 生成されたテスト合計: N

## 修正されたファイル
- src/File1.ts (N修正)
- src/File2.ts (N修正)
- test/File1.test.ts (新規ファイル、Nテスト)

## 詳細な調査結果
[各調査結果の詳細をリスト]

## 残りの手動作業
[手動レビューが必要な項目を特定]
```

### Important Notes / 重要な注意事項

**EN:**
- Always show all fixes to user before applying them to code
- Never modify code without explicit user approval
- Generated tests are additive — preserve all existing tests
- If multiple test frameworks exist, ask user which to prioritize
- Confidence levels guide whether to auto-apply or require approval
- High confidence fixes may be auto-applied if user has enabled auto-fix mode
- Reference Finding IDs consistently throughout report and code

**JP:**
- コード修正前に常にユーザーにすべての修正を表示
- ユーザーの明示的な承認なしにコードを修正しない
- 生成されたテストは加算的 — 既存のテストをすべて保持
- 複数のテストフレームワークが存在する場合、ユーザーにどちらを優先するかを確認
- 信頼レベルは自動適用するか承認が必要かを指示
- 高信頼度修正は、ユーザーが自動修正モードを有効にした場合、自動適用される可能性がある
- レポートとコード全体を通じて一貫してFinding IDを参照

---

## Usage Patterns / 使用パターン

### Trigger Phrases

**EN:**
- "reconcile code with spec"
- "fix code to match spec"
- "generate diff report"
- "produce code fixes"
- "auto-generate tests for reconciliation"

**JP:**
- 「仕様とコードを照合して」
- 「コードを仕様に合わせて」
- 「差分レポートを出して」
- 「コード修正を生成して」
- 「照合テストを自動生成して」

### Integration Points

This skill is designed to work with:
- `formal-agent-contracts/plugin.json` — loads confirmed spec findings
- VDM-SL specification documents — source of truth
- Project source code — target of reconciliation
- Test frameworks — Jest, Vitest, Mocha, Pytest, Unittest, etc.

---

## Version History

**v1.3.0** (Current)
- Full item-by-item comparison for types, pre/post-conditions, invariants
- Three-tier fix prioritization (Bug/Spec Gap/Type Safety)
- Comprehensive test auto-generation
- Bilingual EN/JP documentation

