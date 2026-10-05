---
name: test-design
description: This skill should be used when the user asks to "design test structure", "choose what to assert", "derive expected values", "write a contract test", "eliminate hardcoded test values", "improve test error messages", "review test quality", or discusses source of truth for tests, synchronization points, or diagnosability. Complements functional-testing (what to test) by guiding how to build structurally sound tests.
allowed-tools: [Read, Glob, Grep]
---

# Test Design

Build tests that derive expectations from authoritative sources, eliminate manual synchronization, and produce actionable diagnostics on failure.

## Core Principle

**Never let a test's expected value depend on human memory.**

If a test hardcodes a value that also exists in source code, configuration, or a schema, the test is a synchronization point. When either side changes independently, the test lies — it either passes when it shouldn't, or fails without revealing which side is wrong.

## Decision Framework

Before writing an assertion, answer three questions:

### 1. Where is the source of truth?

| Source of Truth | Import It | Example |
|----------------|-----------|---------|
| Code constant | `import { X }` | `STEP_PHASE`, enum values |
| Schema file | Read and parse | JSON Schema `required` fields |
| Config file | Read and parse | `steps_registry.json` step definitions |
| Design doc | `@design_ref` tag | Allowed intents from design |

If the answer is "my head" or "the PR description", the test will rot.

### 2. What is the relationship being tested?

Test **relationships** (properties/invariants), not **specific values**.

```typescript
// Bad: hardcoded expectation
assertEquals(phases.length, 4);

// Good: relationship — every STEP_PHASE value is accepted by config
const missing = Object.values(STEP_PHASE).filter(p => !pattern.test(p));
assertEquals(missing.length, 0);
```

### 3. When this fails, will the developer know what to fix?

Error messages must state:
- What is mismatched (with both sides named)
- Which file(s) to fix
- IF/THEN guidance when multiple fixes are valid

### 4. Does every assertion serve the stated invariant?

テスト 1 個が持つべき invariant は 1 つ (または密結合した少数)。

各 assertion を書く前に「この assert は **テスト名に書いた invariant** を担保しているか?」を問う。担保していない assert は:

- 別テストの責務 (責務重複)、または
- 証拠に見せかけた over-assertion (assertion bloat)

のどちらか。前者は消す、後者は invariant を言い換えるか消す。

```typescript
// テスト名: "self-heal: T6 failure recovers + marker is idempotent"
// 担保すべき invariant: (a) 次 run で completed 到達 (b) comments.length 不変

assertEquals(second.status, "completed");      // ✓ (a)
assertEquals(github.comments.length, 1);       // ✓ (b)
assertEquals(labelUpdates.length, 6);          // ✗ label 本数は LIFO 契約テストの責務
assertEquals(labelUpdates[4].added, ["review"]); // ✗ 順序は transaction-scope_test.ts
```

### Derivation ladder

expected 値がどこから来るかの優先順位:

```
✓ import from source of truth      // import { STEP_PHASE }
✓ compute from named constants     // const FORWARD_OPS = 2; const expected = FORWARD_OPS * 2;
△ arithmetic with comment          // assertEquals(x, 6) // = 2+2+2  ← 偽装されやすい
✗ bare literal                      // assertEquals(x, 6)
```

**`// 2+2+2=6` コメントは derivation ではない**。コメントは腐るし、定数変更時に追従しない。コード-level で導出すること。

## Test Patterns

### Contract Test (Layer 1)

Verify that a consumer's requirements are met by a provider. Import the consumer's declaration as source of truth.

```
Source of truth:  Module A (declares requirements)
Test target:      Config/Module B (must satisfy them)
Error guidance:   "Fix B to satisfy A" (one direction)
```

When to use: An implementation module **hardcodes** a dependency on a value that a configuration or another module must provide.

See `references/patterns.md` for implementation details.

### Conformance Test (Layer 2)

Verify mutual consistency between two peer configurations. Neither is the sole source of truth — both must agree.

```
Source A:  steps_registry.json (declares c2/c3 values)
Source B:  user.yml (declares accepted patterns)
Error guidance:  IF/THEN for both directions
```

When to use: Two config files that must stay in sync, but either could be the one that changed.

See `references/patterns.md` for implementation details.

### Invariant Test

Verify a property that must always hold, regardless of specific values.

```typescript
// Invariant: every step in registry must have a prompt file
for (const [id, step] of Object.entries(registry.steps)) {
  const path = `${base}/${step.c2}/${step.c3}/f_${step.edition ?? "default"}.md`;
  assert(await exists(path), `Missing prompt file for step "${id}": ${path}`);
}
```

When to use: A structural relationship must hold across all members of a collection.

## Validator as Test Boundary

When a validator exists, the test's responsibility shifts (検証責任の転換):

```
Without validator:  Test → Config ↔ Code  (test directly checks consistency)
With validator:     Test → Validator → Config  (test verifies validator behavior)
```

Four aspects to verify: **Acceptance** (valid input passes) / **Rejection** (invalid input caught) / **Diagnosis** (error message actionable) / **Completeness** (all design constraints covered).

Existing patterns apply: Contract → validator rejects what code cannot handle. Invariant → every design constraint has a validation rule. Conformance → accepted values match runtime support.

See `references/patterns.md` for implementation examples and the Validator Bypass anti-pattern.

## Diagnosability

### Theory

Diagnosability (診断可能性): "a test failure is diagnosable if the failure message alone is sufficient to identify the fix" (Microsoft Research). Gerard Meszaros『xUnit Test Patterns』では Defect Localization として体系化。

テストの失敗メッセージだけで修正先が分かるかどうかが、テスト品質の基礎指標となる。

### Test Pattern Determines Message Structure

テストパターンの選択がエラーメッセージの構造まで決定する:

| Pattern | Fault type | Message structure |
|---------|-----------|-------------------|
| Contract Test | Unambiguous — provider must conform | `Fix:` single directive |
| Conformance Test | Ambiguous — either side could be wrong | `IF/THEN` branching |
| Invariant Test | Unambiguous — the violating member is wrong | `Fix:` with specific member ID |

Contract Test では修正先が一意（provider が consumer に合わせる）なので `Fix:` 形式。Conformance Test では一意に決まらない（どちらの変更が意図的か不明）なので IF/THEN で開発者の意図に委ねる。

### Message Requirements

Every assertion message must contain:

1. **What** — the mismatch, with concrete values from both sides
2. **Where** — file paths of both sides
3. **How to fix** — `Fix:` (single direction) or `IF/THEN` (ambiguous fault)

For full message templates and examples, see `references/patterns.md`.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Hardcoded expected list | Manual sync required when source changes | Import from source of truth |
| Magic number assertion | `assertEquals(x, 4)` — why 4? | Derive from authoritative definition |
| Manual subset selection | `[A, B, C]` cherry-picked from a larger set | `Object.values(SOURCE)` for full coverage |
| Silent pass on empty | Loop over empty collection passes vacuously | Assert collection is non-empty first |
| Opaque failure | `assert(false)` with no context | Include file paths and IF/THEN guidance |
| Partial consumer enumeration | Contract の消費者が複数あるのにテストが一部しか検査しない | 全ての消費箇所を列挙してからテストを書く |
| Shadow contract | パラメータ化された経路をバイパスするハードコード値 | ハードコード値をパラメータに置換し、非デフォルト値で回帰テスト |
| Validator bypass | validator が存在するのにテストが設定を直接検証する | validator の動作をテストする; 検証責任は validator にある |
| Prose derivation alibi | `// 2+2+2=6` コメントで magic number を "derived" に偽装 | named constant で **コード-level に** 導出 (Derivation ladder 参照) |
| Assertion bloat | 1 テストが stated invariant 外の assert を抱える (他テストの責務と重複) | invariant 外の assert は削除し、既存の責務テストに委ねる |
| Delegation trust | sub-agent の skill 適用 summary を検証せず通す | 親が同 skill の lens で re-audit (既存 assert も全スキャン) |

See `references/patterns.md` for detailed explanations of these anti-patterns.

## Workflow

0. **Check for existing validator** — if a validator covers this constraint, test the validator's behavior, not the constraint directly
1. **Identify the invariant** — what relationship must always hold?
2. **Locate the source of truth** — which module/file authoritatively defines the expectation?
3. **Enumerate all consumers** — the invariant を消費する全てのコードパスを洗い出す (steps, validationSteps, retry paths, etc.)
4. **Import, don't copy** — derive expected values from the source
5. **Choose the pattern** — Contract (one-way) or Conformance (two-way)?
6. **Write the assertion** — test the relationship, not a specific value
7. **Craft the error message** — include What/Where/How-to-fix
8. **Verify non-vacuity** — ensure the test exercises real data
9. **Hunt shadow contracts** — grep for hardcoded values that bypass the parameterized path
10. **Scope expansion on review** — 指定された箇所で Anti-Pattern を発見したら、**同ファイル内で grep して同種違反を全スキャン**。レビュー対象行だけ直すのは現状維持バイアス
11. **Re-audit on delegation** — sub-agent にテスト作成を委譲したら、返ってきた diff に対して親が本 skill の lens で再監査 (特に Derivation ladder, Assertion bloat)

## Relation to Other Skills

| Skill | Focus | Complements test-design by |
|-------|-------|---------------------------|
| `functional-testing` | What to test (boundaries, layers) | Identifying which boundaries need tests |
| `fix-checklist` | Root cause before fix | Ensuring the right invariant is identified |
| `contradiction-verification` | Proving a problem exists | Confirming the test's premise is valid |
| `refactoring` | Safe structural changes | Defining before/after contracts |
| `functional-testing` | What aspects of a validator to test (F. Validator Testing) | Defining the four testing aspects (acceptance/rejection/diagnosis/completeness) |
| `breakdown-logger` | Test execution tracing | Visualizing runtime behavior when failure messages alone are insufficient to diagnose |

## Reference

For detailed pattern implementations with full code examples, read `references/patterns.md`.
