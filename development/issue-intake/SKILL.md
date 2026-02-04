---
name: issue-intake
description: |
  Issueの初期トリアージスキル。Issueを受け取り、標準化された分析結果（分類・深刻度・影響スコープ・不確実性・次アクション参照）を生成する。GitHub/Jira/Linear等のトラッカーからissue_payload形式で受け取る。

  トリガー条件:
  - 「Issue #N を分析して」「このIssueの深刻度は？」「このバグはCritical？」
  - 「Issue本文を初期トリアージして」「Issueを取り込んで」
  - 新しいIssueを受け取り、最初の分類・判断が必要な時

  注意: 根本原因の断定、修正案の確定、優先度の最終決定は行わない（材料提供まで）
---

# Issue Intake（初期トリアージ）

Issueを受け取り、標準化された初期トリアージ結果を生成する。

## Non-Goals（このスキルがやらないこと）

- 根本原因の断定（可能性の列挙は可、確定口調は禁止）
- 修正案の確定
- 優先度の最終決定（材料の提供まで）

## 入力

### 必須（いずれか）

**issue_ref形式**:
```yaml
issue_ref:
  repo: "owner/repo"
  number: 123
```

**issue_payload形式**:
```yaml
issue_payload:
  id: "#123"           # 任意
  url: "https://..."   # 任意
  title: "..."         # 必須
  body: "..."          # 必須
  labels: ["bug"]      # 任意
  comments: [...]      # 任意
  created_at: "..."    # 任意
  updated_at: "..."    # 任意
```

### オプション

```yaml
service_context:
  environments: ["prod", "stg", "dev"]
  critical_user_flows: ["login", "checkout"]
  data_sensitivity_notes: "PII/決済/監査対象など"

taxonomy:
  module_map: {"auth": ["login", "oauth"], "session": ["cookie", "token"]}
```

## 出力

```yaml
issue_intake:
  id: "#123"
  title: "..."
  type: "bug"                    # bug/feature/question/task/unknown
  classification: "Major"        # Critical/Major/Minor/Enhancement/NeedsInfo
  severity_score: "7/10"         # 1-10。根拠弱ければ下げる
  confidence: "0.55"             # 0-1（情報充足度と矛盾の少なさ）
  severity_rationale:
    - "根拠1"
    - "根拠2"
  scope:
    modules: ["auth", "session"] # 不明なら ["unknown"]
    user_impact:
      breadth: "unknown"         # unknown/some/many/all
      segment: "unknown"         # 例: iOSのみ, SSO利用者のみ
    environments: ["unknown"]    # prod/stg/dev/unknown
    data_risk: "none"            # none/possible/certain
    estimated_files: "5-10"      # レンジ。根拠薄い場合は "unknown"
  uncertainty_flags:
    - "missing_repro_steps"
    - "missing_environment"
  suspected_categories:
    - "auth_failure"             # 分類タグ
  recommended_workflow: "standard" # emergency/standard/lightweight
  next_actions:
    - "/resolving-uncertainty"
    - "/eld-sense-activation"
```

## 処理フロー

### Step 1: Issue解析（parse_issue）

Issue本文から以下を抽出:

| 項目 | 説明 | 不在時のフラグ |
|------|------|----------------|
| symptoms | 発生している症状 | - |
| expected_behavior | 期待される動作 | `missing_expected_vs_actual` |
| actual_behavior | 実際の動作 | `missing_expected_vs_actual` |
| repro_steps | 再現手順 | `missing_repro_steps` |
| environment | 環境情報 | `missing_environment` |
| logs_or_errors | ログ/エラーメッセージ | `missing_logs` |
| frequency | 発生頻度 | `missing_frequency` |
| workaround | 回避策 | - |
| regression_hint | 回帰の兆候 | - |
| security_signal | セキュリティ関連の兆候 | - |

### Step 2: タイプ分類（classify_type）

| type | 判定条件 |
|------|----------|
| `bug` | 実際の挙動が期待から逸脱 |
| `feature` | 新規要求/改善要求 |
| `question` | 質問/サポート |
| `task` | 作業依頼（バグでも機能でもない） |
| `unknown` | 判定不能 |

### Step 3: 深刻度スコアリング（severity_scoring）

詳細は [references/scoring-rules.md](references/scoring-rules.md) を参照。

**ベーススコア**:
- Security疑い（credential/権限/データ露出）: base 9
- データ損失/破損の可能性: base 8
- 主要機能が成立しない可能性: base 7
- 性能劣化/部分機能不全: base 4-6
- UI崩れ/軽微: base 1-3
- Enhancement: base 1-2

**修正子（Modifiers）**:
- +1: prod影響が明記
- +1: 多数ユーザー/広範囲が明記
- +1: 回避策なし
- +1: 回帰（以前は動いた）が明記
- -1: 影響が限定的
- -1: 回避策あり
- -1: 再現性が低い/断片的

**不確実性ポリシー**:
- 不確実性フラグが多いほど confidence を下げる
- severity_score は上限側に寄せない（過剰確信禁止）
- セキュリティ疑いのみ例外で高めに保持

### Step 4: 分類マッピング（classification_mapping）

| classification | 条件 |
|----------------|------|
| `Critical` | severity >= 9 または security_signal が強い |
| `Major` | severity 6-8 |
| `Minor` | severity 3-5 |
| `Enhancement` | type=feature かつ severity <= 2 |
| `NeedsInfo` | 本文が極端に不足し、分類に必要な最小情報が欠落 |

### Step 5: ワークフロー推奨（workflow_recommendation）

| workflow | 条件 |
|----------|------|
| `emergency` | Critical または security_signal 強 / outage疑い |
| `standard` | Major または 不確実性が中程度以上 |
| `lightweight` | Minor/Enhancement かつ 不確実性が低い |

### Step 6: 次アクション選択（next_actions_selection）

next_actions は**別スキル参照のみ**。理由は severity_rationale 側に記載。

**デフォルト**:
- `/resolving-uncertainty`
- `/eld-sense-activation`

**条件分岐**:

| 条件 | 追加アクション |
|------|----------------|
| security_signal == true | `/security-observation` |
| `missing_repro_steps` in flags | 再現手順の追加依頼を検討 |
| `missing_logs` in flags | ログ取得依頼を検討 |
| `missing_environment` in flags | 環境情報の追加依頼を検討 |

## ガードレール

1. **過剰確信の禁止**: 情報不足時は confidence を下げ、NeedsInfo を積極的に使う
2. **断定口調の禁止**: 「〜である」ではなく「〜の可能性がある」「〜が示唆される」
3. **セキュリティ例外**: セキュリティ疑いは軽視より重視側に倒す
4. **根拠の明示**: severity_rationale に判断根拠を必ず記載

## 出力例

```yaml
issue_intake:
  id: "#123"
  title: "認証エラーが発生する"
  type: "bug"
  classification: "Major"
  severity_score: "7/10"
  confidence: "0.50"
  severity_rationale:
    - "認証は主要導線であり、失敗が継続すると利用が成立しなくなる可能性がある"
    - "再現条件・影響範囲が未記載のため、Critical まで断定できない"
  scope:
    modules: ["auth", "session"]
    user_impact:
      breadth: "unknown"
      segment: "unknown"
    environments: ["unknown"]
    data_risk: "none"
    estimated_files: "5-10"
  uncertainty_flags:
    - "missing_repro_steps"
    - "missing_environment"
    - "missing_impact_breadth"
  suspected_categories:
    - "auth_failure"
  recommended_workflow: "standard"
  next_actions:
    - "/eld-sense-activation"
    - "/resolving-uncertainty"
```

## リファレンス

- [references/scoring-rules.md](references/scoring-rules.md) - 詳細なスコアリングルール
- [references/uncertainty-flags.md](references/uncertainty-flags.md) - 不確実性フラグの標準語彙
- [references/category-taxonomy.md](references/category-taxonomy.md) - suspected_categories の標準タグ
