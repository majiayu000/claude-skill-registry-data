---
name: eld-ground-check
description: |
  LDE（Law-Driven Engineering）の接地（Grounding）検証スキル。
  LawとTermの両方について、検証手段・観測手段が設定されているか検証する。
  CI/CD統合のためのチェックリストとスクリプトを提供。
  使用タイミング: (1) PR作成前の接地確認、(2) CI/CDパイプラインでの自動検証、
  (3) 「Grounding Mapを検証して」、(4) Law/Term追加後の接地完了確認、
  (5) Phase Eで接地を完了させる時
---

# LDE Grounding Check

LawとTermの接地（検証手段・観測手段の設定）を検証する。

## 接地要件

### Law接地

| 重要度 | 検証手段 | 観測手段 |
|--------|---------|---------|
| S0 | **必須** (Test + Runtime) | **必須** (Telemetry全量) |
| S1 | **必須** (Test or Runtime) | **必須** (Telemetry) |
| S2 | 推奨 | 推奨 |
| S3 | 任意 | 任意 |

### Term接地

| 重要度 | 境界検証 | 観測フィールド |
|--------|---------|---------------|
| S0 | **必須** (Validation + Normalization) | **必須** (Observable Fields) |
| S1 | **必須** (Validation or Normalization) | **必須** (Observable Fields) |
| S2 | 推奨 | 推奨 |
| S3 | 任意 | 任意 |

## 検証プロセス

### Step 1: Catalog読み込み

```
docs/lde/law-catalog.md から全Lawを取得
docs/lde/vocabulary-catalog.md から全Termを取得
```

### Step 2: Law接地チェック

各Law IDについて以下を確認：

```yaml
law_grounding_check:
  law_id: LAW-xxx
  severity: S0 | S1 | S2 | S3
  terms: [TERM-a, TERM-b]  # 参照Term

  verification:
    test:
      exists: true | false
      path: <テストファイルパス>
      coverage: <カバレッジ%>
    runtime_check:
      exists: true | false
      type: assert | guard | validation
      location: <実装箇所>

  observability:
    telemetry:
      exists: true | false
      metric: <メトリクス名>
    log_event:
      exists: true | false
      event_name: <イベント名>

  status: PASS | FAIL | WARN
  missing: [<欠落項目>]
```

### Step 3: Term接地チェック

各Term IDについて以下を確認：

```yaml
term_grounding_check:
  term_id: TERM-xxx
  importance: S0 | S1 | S2 | S3
  related_laws: [LAW-a, LAW-b]  # 関連Law

  boundary_verification:
    validation:
      exists: true | false
      method: <検証方法（Zod/手動等）>
      location: <実装箇所>
    normalization:
      exists: true | false
      method: <正規化方法>
      location: <実装箇所>

  observability:
    observable_fields:
      exists: true | false
      fields: [<フィールド名>]
    telemetry:
      exists: true | false
      metric: <メトリクス名>

  status: PASS | FAIL | WARN
  missing: [<欠落項目>]
```

### Step 4: 相互拘束チェック

```yaml
mutual_constraint_check:
  orphan_laws: [<Terms欄が空のLaw>]
  orphan_terms: [<Related Lawsが空のS0/S1 Term>]
  status: PASS | FAIL
```

## チェック項目

### Law検証手段（Verification）

| チェック | 内容 |
|---------|------|
| テスト存在 | Law IDに対応するテストがあるか |
| テスト品質 | 例示テストだけでなくPBTも含むか（S0/S1） |
| 実行時チェック | assert/guard/validationが実装されているか |
| カバレッジ | Law関連コードが80%以上カバーされているか |

### Law観測手段（Observability）

| チェック | 内容 |
|---------|------|
| Telemetry | law.<domain>.<name>.* メトリクスが定義されているか |
| Log/Event | 違反時のログイベントが設定されているか |
| アラート | S0/S1違反時のアラートが設定されているか |

### Term境界検証（Boundary Verification）

| チェック | 内容 |
|---------|------|
| Validation | IO境界で検証が実装されているか |
| Normalization | 正規化処理が実装されているか |
| Type Safety | Brand/Newtypeで型安全性が確保されているか |

### Term観測手段（Observability）

| チェック | 内容 |
|---------|------|
| Observable Fields | ログ/テレメトリで観測するフィールドが設定されているか |
| Telemetry | term.<domain>.<name>.* メトリクスが定義されているか |

## 出力形式

### Grounding Report

```markdown
# Grounding Check Report

## Summary
- Total Laws: 25 (S0: 3, S1: 5, S2: 10, S3: 7)
- Total Terms: 18 (S0: 2, S1: 4, S2: 8, S3: 4)
- Law Grounding: 7/8 S0/S1 (87.5%)
- Term Grounding: 5/6 S0/S1 (83.3%)
- Mutual Constraint: PASS

## Status: ⚠️ WARN (2 issues)

---

## Law Grounding Status

### S0/S1 Laws

| Law ID | Severity | Terms | Test | Runtime | Telemetry | Status |
|--------|----------|-------|------|---------|-----------|--------|
| LAW-inv-balance | S0 | 3 | ✅ | ✅ | ✅ | PASS |
| LAW-pre-order | S1 | 2 | ✅ | ✅ | ✅ | PASS |
| LAW-inv-stock | S1 | 3 | ✅ | ❌ | ✅ | WARN |
| LAW-post-payment | S0 | 2 | ❌ | ❌ | ❌ | FAIL |

---

## Term Grounding Status

### S0/S1 Terms

| Term ID | Importance | Laws | Validation | Normalization | Observable | Status |
|---------|------------|------|------------|---------------|------------|--------|
| TERM-inventory-available | S1 | 2 | ✅ | ✅ | ✅ | PASS |
| TERM-order-quantity | S1 | 2 | ✅ | ✅ | ✅ | PASS |
| TERM-user-balance | S1 | 1 | ✅ | ❌ | ❌ | WARN |

---

## Action Required

### FAIL: LAW-post-payment (S0)
- ❌ Test missing: 決済完了後の状態検証テストがない
- ❌ Runtime check missing: 事後条件のアサーションがない
- ❌ Telemetry missing: law.payment.completed.* メトリクスがない
- Terms: TERM-payment-amount, TERM-payment-status

**推奨アクション**:
1. tests/payment.test.ts に事後条件テストを追加
2. src/payment/service.ts に事後アサーション追加
3. src/payment/telemetry.ts にメトリクス追加

### WARN: TERM-user-balance (S1)
- ✅ Validation exists: Zod schema
- ❌ Normalization missing: 小数点処理なし
- ❌ Observable fields missing: ログ出力なし
- Related Laws: LAW-inv-user-balance

**推奨アクション**:
1. src/users/schema.ts に正規化処理を追加
2. src/users/telemetry.ts にobservable fieldsを追加
```

## 相互拘束チェック結果

```markdown
## Mutual Constraint Check

### 孤立Law
- LAW-policy-discount: ❌ Terms欄が空
  - Action: 参照するTermを追加

### 孤立Term
- TERM-customer-tier (S1): ❌ Related Lawsが空
  - Action: 関連Lawを追加するか重要度を見直し

### パターン検出
- 名辞インフレ: ❌ 検出なし
- 関係スープ: ❌ 検出なし
```

## CI/CD統合

### pre-commit hook

```bash
#!/bin/bash
# .husky/pre-commit

# Law/Term関連ファイルのチェック
changed_files=$(git diff --cached --name-only)
lde_files=$(echo "$changed_files" | grep -E "(law|term|invariant|assert)")

if [ -n "$lde_files" ]; then
  echo "⚠️ LDE関連ファイルが変更されています"
  echo "$lde_files"
  echo "Grounding Map/Link Mapの更新を確認してください"
fi
```

### CI workflow

```yaml
# .github/workflows/lde-grounding.yml
name: eld-ground-check

on: [pull_request]

jobs:
  grounding-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check Law Grounding
        run: |
          # S0/S1 Lawの接地状態を検証
          python scripts/check_law_grounding.py

      - name: Check Term Grounding
        run: |
          # S0/S1 Termの接地状態を検証
          python scripts/check_term_grounding.py

      - name: Check Mutual Constraint
        run: |
          # 相互拘束（孤立チェック）
          python scripts/check_link_map.py

      - name: Run Law Tests
        run: |
          # Law関連テストのみ実行
          npm test -- --grep "LAW-"
```

## 使用例

```
User: PRを出す前にGrounding Checkして

Claude:
## Grounding Check実行中...

### Catalog読み込み
- Law Catalog: 25件 (S0: 3, S1: 5, S2: 10, S3: 7)
- Vocabulary Catalog: 18件 (S0: 2, S1: 4, S2: 8, S3: 4)

### Law接地チェック中...
### Term接地チェック中...
### 相互拘束チェック中...

---

## Grounding Check Report

### Status: ✅ PASS

| 項目 | 結果 |
|------|------|
| S0/S1 Law接地 | 8/8 (100%) |
| S0/S1 Term接地 | 6/6 (100%) |
| 孤立Law | 0件 |
| 孤立Term | 0件 |

すべてのS0/S1 Law/Termが正しく接地されています。
PRを作成できます。
```
