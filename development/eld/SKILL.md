---
name: eld
description: |
  Evidence-Loop Development (ELD) - 証拠で回す統合開発手法。
  コード観測（旧DCCA）、Law/Term規範（旧LDE）、安全な変更（旧Proprioceptive）、
  知識管理（旧PCE）を統一ループで実行する。

  トリガー条件:
  - 「ELDで進めて」「証拠ループで実装して」
  - 「コードベースを理解して」「影響範囲を分析して」（旧DCCA）
  - 「Lawを定義して」「Termをカード化して」（旧LDE）
  - 「安全に変更して」「証拠パックを作成して」（旧Proprioceptive）
  - 「コンテキスト駆動で実装して」「PCEで進めて」（旧PCE）
  - 「ELDでデバッグして」「法則視点でバグ調査して」（デバッグ）
  - 新機能開発、バグ修正、リファクタリング、障害調査
---

# Evidence-Loop Development (ELD)

**証拠で回す**統合開発手法。コードを「相互接続された意味のグラフ」として理解し、
Law/Termで規範を定め、安全な微小変更で実装し、知識を構造化して蓄積する。

## 核心原則

1. **Epistemic Humility**: 推測を事実として扱わない。`unknown`と言う勇気を持つ
2. **Evidence First**: 結論ではなく因果と証拠を中心にする
3. **Grounded Laws**: Lawは検証可能・観測可能でなければならない
4. **Minimal Change**: 最小単位で変更し、即時検証する
5. **Source of Truth**: 真実は常に「現在のコード」。要約をインデックスとして扱う

## 統一ループ

```
Sense → Model → Predict → Change → Ground → Record
  ↑                                            ↓
  └──────────────── 循環 ←─────────────────────┘
```

| Phase | 内容 | 参照 |
|-------|------|------|
| **Sense** | コードの事実/意図/関係を観測、身体図を更新 | `10-sense.md` |
| **Model** | 語彙（Term）と関係（Law）を同定、カード化 | `20-model.md` |
| **Predict** | 影響を因果タイプ分類、段階化戦略と停止条件を確定 | `30-predict.md` |
| **Change** | 最小単位で変更、Pure/IO分離を優先 | `40-change.md` |
| **Ground** | テスト/Telemetry/再現手順で接地 | `50-ground.md` |
| **Record** | Context Deltaをpce-memory/ADR/Catalogへ反映 | `60-record.md` |

## 統一概念

### Evidence Pack（証拠パック）
変更の正当性を証明する一式の証拠。PRの中心。

### Epistemic Status（認識論的状態）
- **verified**: コードまたはテストで確認済み
- **inferred**: 構造や慣習から推論
- **unknown**: 確認不能/要調査

### Evidence Ladder（証拠の梯子）
| Level | 内容 | 備考 |
|-------|------|------|
| L0 | 静的整合（型/lint） | **ここで完了扱いしない** |
| L1 | ユニットテスト | Law/Termの観測写像の最小 |
| L2 | 統合テスト・再現手順 | 境界越えの因果 |
| L3 | 失敗注入/フェイルセーフ | 違反時動作の確認 |
| L4 | 本番Telemetry | 実運用でのLaw違反検知 |

### Issue Contract（ローカル契約）
- 目的（Goal）
- 不変条件（Invariants）
- 物差し（Acceptance Criteria）
- 停止条件（Stop Conditions）

### Law/Term（グローバル法則）
- **Law**: ビジネス上の「守るべき条件」（Invariant/Pre/Post/Policy）
- **Term**: ドメインの語彙（Entity/Value/Context/Boundary）
- **Link Map**: Law ↔ Term の相互参照。孤立禁止

詳細は `00-glossary.md` を参照。

## 開発フロー

### Phase 1: Issue（受付）

```yaml
成果物:
  - Issue Contract: 目的/不変条件/物差し/停止条件
  - 現状証拠: Senseフェーズの観測結果
  - Term/Law候補: Modelフェーズの初期出力
```

**実行内容**:
1. `pce.memory.activate` で関連知識を活性化
2. `context_bundle` でゴールベースのコード検索
3. Issue Contractを作成（`issue-template.md`使用）
4. Term/Law候補を列挙

使用スキル: `/eld-sense-activation`, `/eld-model-law-discovery`

### Phase 2: Design（設計）

```yaml
成果物:
  - Law/Term Cards: 相互参照あり、孤立なし
  - Grounding Plan: 必要テスト/Telemetry（Evidence Ladder対応）
  - Change Plan: 微小変更列＋各ステップのチェック
```

**実行内容**:
1. Law Card化（Scope/例外/違反時動作）
2. Term Card化（意味/境界/観測写像）
3. Link Map更新（孤立チェック）
4. 影響予測と段階化計画
5. **Grounding Plan策定**（`/test-design-audit`でテスト設計）

使用スキル: `/eld-model-law-card`, `/eld-model-term-card`, `/test-design-audit`

### Phase 3: Implementation（実装ループ）

各ステップを同じ型で回す:

```
1. Sense   → 触るシンボル/境界/設定の身体図更新
2. Predict → 期待される因果と失敗モード
3. Change  → 最小単位で変更、Pure/IO分離を維持
4. Ground  → テスト/Telemetryで観測写像を満たす
5. Record  → Context Delta記録
```

**停止条件チェック**:
- 予測と現実の継続的乖離
- 観測不能な変更の増加
- ロールバック線の崩壊

### Phase 4: Review（レビュー）

```yaml
証拠パック中心:
  - 因果と証拠の整合
  - Law/Term孤立チェック
  - 影響範囲のグラフ証拠
  - Evidence Ladder達成レベル
```

使用スキル: `/eld-ground-check`

PR作成: `pr-template.md` 使用

### Phase 5: Ops（運用）

- Telemetryで Law違反を監視
- Context Deltaを回収→構造化
- 物差しの再点検
- pce-memoryへのフィードバック

## 知識ストア

| ストア | 役割 | 内容 |
|--------|------|------|
| pce-memory | 履歴・痕跡 | Fact/Semantic/Relational 3層 |
| Law/Term Catalog | 規範の正本 | Cards、Link Map、Grounding Map |
| ADR | アーキテクチャ決定 | 重要な意思決定の記録 |

### pce-memory 3層構造

| Layer | 内容 | 更新頻度 | scope |
|-------|------|----------|-------|
| **Fact** | 関数シグネチャ、型定義、パス | 高 | `session` |
| **Semantic** | モジュールの意図、ビジネスルール | 中 | `project` |
| **Relational** | 呼び出し関係、データフロー | 低 | `project` |

## 完了条件と停止条件

### 完了条件
- Issue Contractの物差しが満たされている
- Law/Termが接地している（Evidence Ladder L1以上）
- Evidence Packが揃っている
- Link Mapに孤立がない

### 停止条件（発生時は追加計測/スコープ縮小）
- 予測と現実の継続的乖離（想定外のテスト失敗3回以上）
- 観測不能な変更の増加（物差しで検証できない変更）
- ロールバック線の崩壊（戻せない変更の発生）

## リファレンス

### 概念定義
- `00-glossary.md` - 統一語彙

### フェーズ詳細
- `10-sense.md` - 感知フェーズ（旧DCCA）
- `20-model.md` - モデル化フェーズ（旧LDE Law/Term発見）
- `30-predict.md` - 予測フェーズ（旧Proprioceptive）
- `40-change.md` - 変更フェーズ
- `50-ground.md` - 接地フェーズ
- `60-record.md` - 記録フェーズ（旧PCE）

### テンプレート
- `issue-template.md` - Issue Contract雛形
- `pr-template.md` - PR & Evidence Pack雛形
- `law-term-card.md` - Law/Term Card雛形

## 使用例

```
User: ユーザー認証機能をELDで実装して

Claude:
## ELD Phase 1: Issue

### Issue Contract
- 目的: JWTベースの認証機能実装
- 不変条件: 既存APIとの後方互換性
- 物差し: 認証テスト通過 + レスポンス<200ms
- 停止条件: セキュリティ脆弱性発見時

### 現状証拠（Sense）
[verified]
- 既存認証: src/auth/legacy.ts:23-45（Basic認証）
- 関連モジュール: src/middleware/auth.ts

[unknown]
- 外部認証プロバイダとの連携状況

### Term/Law候補（Model）
- TERM-jwt-token: JWT形式のアクセストークン（S1）
- TERM-refresh-token: リフレッシュトークン（S1）
- LAW-token-expiry: アクセストークンは1時間で失効（S0）
- LAW-refresh-validity: リフレッシュトークンは7日間有効（S1）

Phase 2: Designに進みますか？
```

## デバッグへの適用

ELDの統一ループはデバッグにも適用できる。バグを「法則（Law）からの逸脱」として捉え、
証拠ループで系統的に解決する。

### デバッグループ

```
Sense → Model → Predict → Change → Ground → Record
  ↑                                            ↓
  └──────────── 法則復元まで循環 ←──────────────┘
```

| Phase | 通常開発 | デバッグ適用 |
|-------|----------|--------------|
| **Sense** | コード観測 | 症状の観測 + 関連法則候補の列挙 |
| **Model** | Law/Term同定 | 破られた法則の仮説形成 + 論理式化 |
| **Predict** | 影響予測 | 法則違反の伝播範囲予測 |
| **Change** | 微小変更 | 法則復元のための最小修正 |
| **Ground** | 接地検証 | 証拠の梯子での法則復元確認 |
| **Record** | 知識蓄積 | バグパターン + 法則違反パターン記録 |

### ELD的デバッグの特徴

| 観点 | 従来 | ELD的 |
|------|------|-------|
| 視点 | 「なぜ壊れた？」 | 「どの法則が破られた？」 |
| 証拠 | ログ・スタックトレース | 法則違反の論理的証明 |
| 修正 | 症状の除去 | 法則の復元 |
| 検証 | 「動いた」 | 「法則が満たされた」（L0-L4） |
| 蓄積 | バグ票 | Law/Term Card + パターン |

詳細は `/eld-debug` スキルを参照。

## ユーティリティスキル

ELDループ内で使用する補助スキル:

### Sense（感知）
| スキル | 用途 |
|--------|------|
| `/eld-sense-activation` | アクティブコンテキスト構築 |
| `/eld-sense-scope` | タスクスコープの定義 |
| `/eld-sense-task-decomposition` | タスク分解 |

### Model（モデル化）
| スキル | 用途 |
|--------|------|
| `/eld-model-law-discovery` | Law候補の発見 |
| `/eld-model-law-card` | Law Card作成 |
| `/eld-model-term-card` | Term Card作成 |
| `/eld-model-link-map` | Link Map管理 |

### Ground（接地）
| スキル | 用途 |
|--------|------|
| `/test-design-audit` | **テスト設計監査（ELD統合版）** - Law/Term駆動のテスト設計 |
| `/eld-ground-check` | 接地状況の検証 |
| `/eld-ground-evaluate` | 成果物評価 |
| `/eld-ground-law-monitor` | Law違反監視 |
| `/eld-ground-pr-review` | PRレビュー |

### Record（記録）
| スキル | 用途 |
|--------|------|
| `/eld-record-collection` | Context Delta収集 |
| `/eld-record-structuring` | 知識の構造化 |
| `/eld-record-compact` | 履歴圧縮 |
| `/eld-record-maintenance` | 知識メンテナンス |
| `/eld-record-memory-collector` | メモリ収集 |
| `/eld-record-knowledge-transfer` | 知識転送 |

### Debug（デバッグ）
| スキル | 用途 |
|--------|------|
| `/eld-debug` | 法則駆動デバッグ（バグ=法則違反として分析・修正） |
