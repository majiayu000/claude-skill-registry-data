---
name: eld-record-maintenance
description: |
  PCE (Process Context Engine) のメンテナンススキル。現存する Claim の品質を維持し、
  間違い・不要・古い・重複した Claim を整理する。pce_memory_feedback を使用して
  更新・削除・評価を行う。メモリの健全性を保ちたい場合、Claim の品質問題を発見した場合、
  定期的なメモリ整理を行いたい場合に使用する。
  Observation 収集、AC の構築、タスクごとのメモリ最適化は行わない。
---

# PCE Maintenance Skill

## 概要

PCE Maintenance は、pce-memory に保存された Claim の品質を維持・改善するためのスキルである。

### このスキルの責任範囲

**行うこと:**
- Claim の品質評価（正確性、関連性、鮮度）
- 問題のある Claim の特定と修正
- 重複 Claim の検出と統合
- 古い/無効な Claim の削除
- feedback を通じた Claim の評価記録

**行わないこと:**
- Observation 収集（Collection Skill に委譲）
- AC の構築（Activation Skill に委譲）
- タスクごとのメモリ最適化

## メンテナンス対象の問題タイプ

### 1. 不正確な Claim（Incorrect）

事実と異なる、または誤った情報を含む Claim。

**例:**
```yaml
# 不正確な Claim
text: "認証には Firebase を使用している"
# 実際は AWS Cognito を使用
```

**対応:** 修正または削除

### 2. 古い Claim（Outdated）

以前は正しかったが、現在は適用されない情報。

**例:**
```yaml
# 古い Claim
text: "状態管理には Redux を使用する"
# ADR-0009 で XState に移行済み
```

**対応:** 削除または SUPERSEDES 関係で置換

### 3. 重複 Claim（Duplicate）

同じ内容を異なる表現で記述した複数の Claim。

**例:**
```yaml
# Claim A
text: "pnpm のみ使用する"

# Claim B（重複）
text: "パッケージマネージャーは pnpm を使用"
```

**対応:** 統合して1つに

### 4. 不要な Claim（Unnecessary）

価値が低い、または他の Claim に包含される情報。

**例:**
```yaml
# 不要な Claim（より具体的な Claim が存在）
text: "TypeScript を使用している"
# 既に "TypeScript 厳密モード、any 禁止" が存在
```

**対応:** 削除

### 5. 矛盾する Claim（Contradictory）

互いに矛盾する複数の Claim。

**例:**
```yaml
# Claim A
text: "console.log を使用する"

# Claim B（矛盾）
text: "console.* は禁止、logger.* を使用"
```

**対応:** 正しい方を残し、他を削除

## メンテナンスワークフロー

### Step 1: Claim の一覧取得

pce-memory から現在の Claim を取得する:

```
pce_memory_activate({
  goal: "現在のすべての Claim を確認"
})
```

### Step 2: 問題の検出

各 Claim について以下を確認する:

```
問題検出チェックリスト:
├─ 正確性: 現在の事実と一致するか？
├─ 鮮度: 情報は最新か？
├─ 重複: 同様の Claim が他にないか？
├─ 価値: この Claim は必要か？
└─ 一貫性: 他の Claim と矛盾しないか？
```

### Step 3: 問題の分類

検出した問題を分類する:

| 問題タイプ | 緊急度 | 推奨アクション |
|-----------|--------|---------------|
| 不正確 | 高 | 即時修正または削除 |
| 矛盾 | 高 | 解決して片方を削除 |
| 古い | 中 | SUPERSEDES で置換または削除 |
| 重複 | 中 | 統合 |
| 不要 | 低 | 削除検討 |

### Step 4: feedback の送信

`pce_memory_feedback` を使用して評価・修正を行う:

#### 4.1 肯定的評価（Claim が有用な場合）

```
pce_memory_feedback({
  claim_hash: "sha256:abc123...",
  signal: "positive",
  note: "この Claim は現在も正確で有用"
})
```

#### 4.2 否定的評価（問題がある場合）

```
pce_memory_feedback({
  claim_hash: "sha256:def456...",
  signal: "negative",
  note: "ADR-0009 により XState に移行済み。この Claim は古い"
})
```

#### 4.3 削除要求

```
pce_memory_feedback({
  claim_hash: "sha256:ghi789...",
  signal: "delete",
  note: "重複: sha256:xyz... と同一内容"
})
```

### Step 5: 修正 Claim の作成（必要な場合）

古い Claim を置き換える新しい Claim を作成:

```
pce_memory_upsert({
  text: "状態管理には XState を使用する（ADR-0009）",
  kind: "policy_hint",
  scope: "project",
  boundary_class: "internal",
  content_hash: "sha256:...",
  provenance: {
    at: "2025-01-15T16:00:00Z",
    actor: "claude-code",
    note: "旧 Redux 方針を置換"
  }
})

# 置換関係を登録
pce_memory_upsert_relation({
  id: "rel-xstate-supersedes-redux",
  src_id: "claim-xstate-policy",
  dst_id: "claim-redux-policy",
  type: "SUPERSEDES"
})
```

## メンテナンスパターン

### パターン A: 単純削除

明らかに不要または不正確な Claim を削除する。

**手順:**
1. 問題の Claim を特定
2. 削除理由を記録
3. feedback で削除要求

**例:**
```
# 不正確な Claim を削除
pce_memory_feedback({
  claim_hash: "sha256:...",
  signal: "delete",
  note: "事実と異なる: Firebase ではなく Cognito を使用"
})
```

### パターン B: 置換（Supersede）

古い Claim を新しい Claim で置き換える。

**手順:**
1. 新しい Claim を作成
2. SUPERSEDES 関係を登録
3. 古い Claim に negative feedback

**例:**
```
# 1. 新しい Claim を作成
pce_memory_upsert({
  text: "認証には AWS Cognito を使用（Cognito sub を ID として使用）",
  ...
})

# 2. 置換関係を登録
pce_memory_upsert_relation({
  src_id: "claim-cognito",
  dst_id: "claim-firebase",
  type: "SUPERSEDES"
})

# 3. 古い Claim に negative feedback
pce_memory_feedback({
  claim_hash: "sha256:...",
  signal: "negative",
  note: "SUPERSEDED by claim-cognito"
})
```

### パターン C: 統合（Merge）

重複する複数の Claim を1つに統合する。

**手順:**
1. 統合した新しい Claim を作成
2. 元の Claim すべてに SUPERSEDES 関係
3. 元の Claim に negative feedback

**例:**
```yaml
# 重複 Claim A
text: "pnpm を使用する"

# 重複 Claim B
text: "npm は禁止"

# 統合後
text: "パッケージ管理は pnpm のみ使用（npm 禁止）"
```

### パターン D: 矛盾解決

矛盾する Claim を調査し、正しい方を残す。

**手順:**
1. 矛盾の原因を調査（どちらが正しいか）
2. 正しい Claim に positive feedback
3. 誤った Claim に delete feedback
4. CONTRADICTS 関係があれば削除

**例:**
```
# 正しい Claim を確認
pce_memory_feedback({
  claim_hash: "sha256:correct...",
  signal: "positive",
  note: "CLAUDE.md で確認: logger.* 使用が正しい"
})

# 誤った Claim を削除
pce_memory_feedback({
  claim_hash: "sha256:wrong...",
  signal: "delete",
  note: "矛盾解決: console.log 使用は誤り"
})
```

### パターン E: 品質向上

正確だが不完全な Claim を改善する。

**手順:**
1. 既存 Claim の問題点を特定
2. 改善した新 Claim を作成
3. SUPERSEDES 関係で置換

**例:**
```yaml
# 既存（不完全）
text: "Cognito を使用"

# 改善版
text: "認証には AWS Cognito を使用。Cognito sub (UUID) を安定識別子として使用、username は使わない"
```

## 定期メンテナンスガイド

### 日次チェック（推奨）

- [ ] 新規追加された Claim の品質確認
- [ ] session スコープ Claim の有効性確認

### 週次チェック

- [ ] 重複 Claim の検出と統合
- [ ] 低評価 Claim のレビュー

### 月次チェック

- [ ] 全 Claim の鮮度確認
- [ ] 未使用 Claim の特定と削除検討
- [ ] Entity/Relation の整合性確認

## feedback シグナルの使い分け

| シグナル | 用途 | 効果 |
|----------|------|------|
| `positive` | Claim が有用・正確 | 優先度向上 |
| `negative` | Claim に問題あり | 優先度低下、レビュー対象 |
| `delete` | Claim を削除すべき | 削除候補としてマーク |

## 品質指標

### Claim の健全性指標

| 指標 | 良好 | 要注意 | 問題 |
|------|------|--------|------|
| 正確性 | 100% | 95-99% | <95% |
| 重複率 | 0% | 1-5% | >5% |
| 鮮度（30日以内更新） | >80% | 50-80% | <50% |
| 矛盾 | 0件 | 1-2件 | >2件 |

### メンテナンス完了基準

- [ ] すべての矛盾が解決済み
- [ ] 重複 Claim なし
- [ ] 明らかに不正確な Claim なし
- [ ] 古い Claim に適切な対応済み

## 注意事項

1. **慎重な削除**: 削除前に必ず影響を確認。他の Claim や Relation が参照していないか
2. **証跡の保持**: feedback の note に必ず理由を記録
3. **段階的対応**: 大量の問題がある場合は優先度順に対応
4. **可逆性の確保**: 可能な限り SUPERSEDES を使用し、削除は最終手段

## 関連リソース

- `references/feedback_guide.md` - feedback の詳細ガイド
- `references/quality_criteria.md` - 品質評価基準の詳細
