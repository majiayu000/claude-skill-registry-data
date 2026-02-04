---
name: eld-sense-task-decomposition
description: |
  PCE (Process-Context Engine) のタスク分解スキル。親→子→孫の入れ子構造でタスクを分解し、各プロセスへのコンテキスト継承を設計する。

  トリガー条件:
  - 大きなタスクを受け取った時
  - 「このタスクを分解して」
  - 「実装計画を立てて」
  - 「作業を整理して」
  - 複雑な機能の実装開始時
---

# PCE Task Decomposition Skill

タスクを入れ子構造で分解し、各レベルでのコンテキスト継承を設計する。

## 分解の原則

1. **3段階まで**: 親→子→孫の3レベルを上限とする
2. **単一責務**: 各タスクは1つの責務に集中
3. **独立性**: 可能な限り並列実行可能に
4. **境界明確**: 責務の重複・漏れを防ぐ
5. **原子性**: 末端タスクは5-10分で完了する原子タスクに（Superpowers統合）

## 原子タスクの定義（Superpowers統合）

原子タスク = **5-10分で完了する最小単位のタスク**

### 原子性の基準

- [ ] 単一の概念変更（1つのシンボル/Law/Termに集中）
- [ ] 独立してテスト可能（他のタスクに依存しない）
- [ ] ロールバック可能（git checkout で戻せる）
- [ ] Evidence Ladder L0以上で検証可能
- [ ] 1タスク = 1コミット の原則

### 分解の粒度目安

| タスクサイズ | 時間目安 | 例 |
|------------|---------|-----|
| 原子タスク | 5-10分 | 型定義追加、1関数の実装、1テスト追加 |
| 子タスク | 20-40分 | モジュール実装、API層実装 |
| 親タスク | 2-4時間 | 機能全体の実装 |

詳細は `references/atomic-task-definition.md` を参照。

## Evidence付与ルール

各タスク（特に原子タスク）には以下を明示:

```yaml
task:
  name: <タスク名>
  level: L0 | L1 | L2 | L3 | L4  # Evidence Ladderレベル
  verification: <検証方法の具体的記述>
  law_term: [<関連Law ID>, <関連Term ID>]
  time_estimate: 5-10min        # 時間見積もり（原子タスクの場合）
```

### Law/Term紐付けの必須化

すべての原子タスクは、最低1つのLawまたはTermに紐付ける。
紐付けがない場合は、タスク分解が不適切と判断。

詳細は `references/evidence-requirement.md` を参照。

## 分解テンプレート

```markdown
# Task Decomposition: [親タスク名]

## Level 0: Root Task
**Goal**: [全体目標]
**Constraints**: [全体制約]
**Success Criteria**: [完了条件]

## Level 1: Major Components
### 1.1 [子タスク1]
- Goal: [目的]
- Boundary: [責務境界]
- Dependencies: [依存関係]
- Parallel: Yes/No
- Time Estimate: [時間見積もり]

### 1.2 [子タスク2]
...

## Level 2: Atomic Tasks（原子タスク）
### 1.1.1 [原子タスク1]
- Goal: [目的]
- Evidence Level: L0/L1/L2/L3/L4
- Verification: [検証方法]
- Law/Term: [LAW-xxx, TERM-yyy]
- Time Estimate: 5-10min
- Rollback Point: Yes

### 1.1.2 [原子タスク2]
...

## Context Inheritance Map
| From | To | Inherit | Return |
|------|-----|---------|--------|
| Root | 1.1 | [継承情報] | [戻す情報] |
| 1.1 | 1.1.1 | [Law/Term仕様] | [実装成果物] |

## Evidence Summary
| Task | Evidence Level | Law/Term | Verification |
|------|----------------|----------|--------------|
| 1.1.1 | L1 | LAW-xxx | ユニットテスト |
| 1.1.2 | L0 | TERM-yyy | 型チェック |
```

## 分解パターン

### パターン1: 機能分割
```
機能A実装
├── データ層
├── ビジネスロジック層
└── API層
```

### パターン2: フェーズ分割
```
機能A実装
├── 設計フェーズ
├── 実装フェーズ
└── テストフェーズ
```

### パターン3: ドメイン分割
```
Eコマース機能
├── 商品管理
├── カート管理
└── 決済処理
```

## 使用例

```
User: ユーザー認証システムを実装して

Claude:
# Task Decomposition: ユーザー認証システム

## Level 0: Root Task
**Goal**: JWT認証による安全なユーザー認証
**Constraints**: OWASP準拠、既存DBスキーマ活用
**Success Criteria**: ログイン/ログアウト/リフレッシュ動作

## Level 1: Major Components

### 1.1 認証コア
- Goal: JWTトークン生成・検証
- Boundary: トークン操作のみ、ユーザー管理は含まない
- Dependencies: なし
- Parallel: Yes
- Time Estimate: 30-40min

### 1.2 ユーザーセッション管理
- Goal: セッション状態の管理
- Boundary: セッションのみ、認証ロジックは含まない
- Dependencies: 1.1
- Parallel: No
- Time Estimate: 20-30min

### 1.3 API エンドポイント
- Goal: /auth/* のREST API
- Boundary: HTTPインターフェースのみ
- Dependencies: 1.1, 1.2
- Parallel: No
- Time Estimate: 30-40min

## Level 2: Atomic Tasks（1.1の原子タスク例）

### 1.1.1 JWTペイロード型定義
- Goal: JWTペイロードのTypeScript型定義
- Evidence Level: L0
- Verification: tsc型チェック通過
- Law/Term: TERM-jwt-payload (S1)
- Time Estimate: 5-7min
- Rollback Point: Yes

### 1.1.2 トークン生成関数実装
- Goal: JWT生成関数 generateToken() の実装
- Evidence Level: L1
- Verification: ユニットテスト（正常系+異常系）
- Law/Term: LAW-token-expiry (S0), LAW-token-signature (S0)
- Time Estimate: 8-10min
- Rollback Point: Yes

### 1.1.3 トークン検証関数実装
- Goal: JWT検証関数 verifyToken() の実装
- Evidence Level: L1
- Verification: ユニットテスト（期限切れ、改ざん検出）
- Law/Term: LAW-token-expiry (S0), LAW-token-signature (S0)
- Time Estimate: 8-10min
- Rollback Point: Yes

## Context Inheritance Map
| From | To | Inherit | Return |
|------|-----|---------|--------|
| Root | 1.1 | ADR-003, セキュリティ要件 | トークン仕様 |
| Root | 1.2 | セッション要件 | セッション設計 |
| 1.1 | 1.3 | トークン仕様 | API仕様 |
| 1.1 | 1.1.1 | JWTペイロード仕様 | 型定義ファイル |
| 1.1 | 1.1.2 | LAW-token-expiry, LAW-token-signature | generateToken実装 |
| 1.1 | 1.1.3 | LAW-token-expiry, LAW-token-signature | verifyToken実装 |

## Evidence Summary
| Task | Evidence Level | Law/Term | Verification |
|------|----------------|----------|--------------|
| 1.1.1 | L0 | TERM-jwt-payload | tsc型チェック |
| 1.1.2 | L1 | LAW-token-expiry, LAW-token-signature | ユニットテスト |
| 1.1.3 | L1 | LAW-token-expiry, LAW-token-signature | ユニットテスト |

分解完了。1.1.1から開始しますか？
```

---

## 品質優先原則（Superpowers統合）

### 核心原則

1. **Epistemic Humility**: 推測を事実として扱わない。`unknown`と言う勇気を持つ
2. **Evidence First**: 結論ではなく因果と証拠を中心にする
3. **Minimal Change**: 最小単位で変更し、即時検証する
4. **Grounded Laws**: Lawは検証可能・観測可能でなければならない
5. **Source of Truth**: 真実は常に現在のコード。要約はインデックス

### 「速さより質」の実践

- 要件の曖昧さによる手戻りを根本から排除
- テストなし実装を許さない
- 観測不能な変更を防ぐ

### 完了の定義

- [ ] Evidence Ladder目標レベル達成
- [ ] Issue Contractの物差し満足
- [ ] Law/Termが接地している（Grounding Map確認）
- [ ] Link Mapに孤立がない
- [ ] ロールバック可能な状態

### 停止条件

以下が発生したら即座に停止し、追加計測またはスコープ縮小：

- 予測と現実の継続的乖離（想定外テスト失敗3回以上）
- 観測不能な変更の増加（物差しで検証できない変更）
- ロールバック線の崩壊（戻せない変更の発生）
