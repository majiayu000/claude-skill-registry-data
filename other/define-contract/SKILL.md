---
name: define-contract
description: >
  マルチエージェント開発におけるエージェント間契約をVDM-SLで定義し、
  設計文書（PROTOCOL.md、API-SIGNATURES.md）を生成する。
  「エージェントの契約を定義したい」「エージェント間のインターフェースを仕様化したい」
  「契約を書きたい」「仕様を作りたい」「エージェントの入出力を定義したい」
  「新しいエージェントを追加したい」「APIの仕様を形式的に書きたい」
  「プロトコル仕様を作りたい」といったリクエストに使用する。
  English triggers: "define an agent contract", "formalize the agent interface",
  "write a formal spec", "specify agent inputs and outputs", "design the protocol".
  形式手法の知識がないユーザーでも対話的に契約を定義できるよう、
  自然言語から段階的にVDM-SL仕様と設計文書へ変換する。
metadata:
  version: "2.0.0"
  author: Formal Agent Contracts
  tags: [vdm-sl, formal-specification, agent-contracts, protocol-design]
---

# エージェント契約定義スキル (v2.0.0)

形式的エージェント契約を段階的に定義し、VDM-SL（Vienna Development Method Specification Language）仕様と設計文書（PROTOCOL.md、API-SIGNATURES.md）を生成するスキルです。v2.0.0では Phase 1（ドメイン論理）の VDM-SL 仕様に加えて、Phase 2（プロトコル・API 仕様）の設計文書生成に対応し、複雑なマルチエージェントシステムに対応しています。

## 概要

このスキルは以下のワークフローを実行します：

1. **ステップ1：エージェントロール抽出** - 対象エージェントの責務と境界を明確化
2. **ステップ2：データ型定義** - エージェントが扱うデータ構造を形式化（Phase 1: ドメイン論理）
2b. **ステップ2b：通信プロトコル層定義（新機能）** - 設計文書（PROTOCOL.md、API-SIGNATURES.md）を生成（Phase 2: プロトコル・API仕様）
3. **ステップ3：契約定義** - 前提条件と後提条件を含む契約を記述（Phase 1: ドメイン論理）
4. **ステップ4：VDM-SL生成** - Phase 1 VDM-SL仕様書を自動生成
5. **ステップ5：仕様レビュー** - 生成された仕様と設計文書を検証
6. **ステップ6：契約テスト生成の提案** - 自動テスト生成スキルの実行を提案

## ステップ1：エージェントロール抽出

**目的**：対象エージェントの明確な責務定義

ユーザーに以下の情報を聞き出します：

- **エージェント名**：e.g., `HybridJudgeAgent`, `MessageValidator`
- **主要責務**：このエージェントが何をするか（1-2文）
- **入力の形態**：どのようなデータを受け取るか
- **出力の形態**：どのようなデータを返すか
- **状態管理**：ステートレスか、ステートフルか
- **外部依存**：他のエージェントやシステムへの依存関係

**出力例**：
```
エージェント：HybridJudgeAgent
責務：チケットの自動返信可否を判定し、処理方法（自動応答/オペレータ連携/オペレータのみ）を決定する
入力：Ticket型（ID、本文、顧客情報、優先度、複雑度スコア）
出力：Action型（<AutoReply> | <OperatorAndLLM> | <OperatorOnly>）
状態：ステートレス（判定時点の入力値のみに依存）
依存：MessageValidator（メッセージ検証）、ScoreCalculator（スコア計算）
```

## ステップ2：データ型定義

**目的**：エージェントが扱う全データ型を形式化

以下の形式でデータ型を定義します：

```vdm-sl
-- 基本型
Score = nat1  -- 1から100までのスコア
Priority = <Low> | <Medium> | <High>

-- レコード型
Ticket :: 
  id : nat1
  content : seq of char
  priority : Priority
  complexity_score : Score
```

各型について以下を明確にします：

- **型の名前と分類**（基本型、レコード型、合成型）
- **不変式（invariant）**：型が満たすべき制約
- **値域**：取り得る値の範囲
- **デフォルト値**：必要に応じて定義

**ユーザーへの質問**：
- このエージェントが扱う全てのデータ型は何か？
- 各型にどのような制約があるか？（例：スコアは1-100、優先度は3値）
- これらの型がどのような不変式を満たすべきか？

## ステップ2b：通信プロトコル層定義（新機能 v2.0.0）

**目的**：マルチエージェント間の通信仕様を設計文書として形式化

このステップは複数のエージェント間で通信が存在する場合に適用します。ここで生成される成果物は **PROTOCOL.md** と **API-SIGNATURES.md** という設計ドキュメントであり、VDM-SL コードではありません。これらの文書はプロトコル実装エージェントと API 実装エージェントが直接参照します。

### 2b-1. メッセージ型レジストリ

全てのメッセージ型を正規名として宣言。Markdown テーブル形式で記録：

| メッセージ型（正規名） | 送信元 | 受信先 | 同期/非同期 | 説明 |
|---|---|---|---|---|
| `TicketCreate` | User | Server | 同期 | ユーザーがチケットを作成 |
| `TicketUpdate` | User | Server | 同期 | ユーザーがチケットを更新 |
| `EscalationRequest` | User | Server | 同期 | ユーザーがエスカレーションをリクエスト |
| `ReplyManual` | Operator | Server | 同期 | オペレータが手動返信 |
| `TicketCreated` | Server | User | 非同期 | サーバーがチケット作成完了を通知 |
| `AutoReply` | Server | User | 非同期 | サーバーが自動返信を送信 |
| `OperatorReply` | Server | User | 非同期 | サーバーがオペレータからの返信を転送 |

**定義時のチェックポイント**：
- 各メッセージ型は固有で明確か？
- メッセージの方向（送信元→受信先）が明記されているか？
- 同期/非同期の区別が適切か？

### 2b-2. ペイロード構造仕様

各メッセージ型のペイロード（データ本体）をフィールド定義テーブルで記述：

#### TicketCreate ペイロード

| フィールド名 | 型 | 必須/省略可 | 説明 |
|---|---|---|---|
| `content` | string | 必須 | チケット本文 |
| `customerId` | int | 必須 | 顧客ID |
| `priority` | enum: Low \| Medium \| High | 必須 | 優先度 |
| `attachments` | string[] | 省略可 | 添付ファイルURL配列 |

#### ReplyManual ペイロード

| フィールド名 | 型 | 必須/省略可 | 説明 |
|---|---|---|---|
| `ticketId` | int | 必須 | チケットID |
| `operatorId` | int | 必須 | オペレータID |
| `message` | string | 必須 | 返信内容 |
| `resolution` | enum: Resolved \| Pending | 必須 | 解決状態 |

### 2b-3. 共有モジュール API シグネチャ

マルチエージェント通信で参照される API 関数を **正確な署名** で宣言（API-SIGNATURES.md）：

```typescript
// MessageValidator API
interface MessageValidator {
  validatePayload(msgType: string, payload: object): ValidationResult
  // パラメータ順序: msgType, payload
  // 戻り値: { isValid: bool, errors: string[] }
  
  checkDirection(sender: string, msgType: string): boolean
  // パラメータ順序: sender, msgType
}

// StateTransition API
interface StateTransition {
  isValidTransition(currentStatus: string, newStatus: string): boolean
  // パラメータ順序: currentStatus, newStatus
  
  getValidTransitions(currentStatus: string): string[]
  // パラメータ順序: currentStatus
  // 戻り値: 遷移可能な状態の配列
}
```

**重要**：パラメータの名前・順序・型は実装エージェントが直接参照するため、一度決めたら変更不可。

### 2b-4. 状態遷移マトリクス

プロトコルで管理される状態の遷移を Markdown 表で定義（VDM-SL ではなく）：

| 現在の状態 | → Created | → Assigned | → InProgress | → Resolved | → Closed |
|---|:---:|:---:|:---:|:---:|:---:|
| Created | ✗ | ✓ | ✗ | ✗ | ✓ |
| Assigned | ✗ | ✗ | ✓ | ✗ | ✓ |
| InProgress | ✗ | ✗ | ✗ | ✓ | ✓ |
| Resolved | ✗ | ✗ | ✗ | ✗ | ✓ |
| Closed | ✗ | ✗ | ✗ | ✗ | ✗ |

### 2b-5. Null フィールド注釈

各ペイロード型で、null を許容するフィールドを明示：

| メッセージ型 | Null 許容フィールド | デフォルト値 |
|---|---|---|
| TicketCreate | `attachments` | `[]` |
| ReplyManual | なし | — |
| AutoReply | `operatorName` | `null` |

### 2b-6. 命名規約宣言

プロトコル全体で使用する命名規約を統一宣言（一度だけ記述）：

```
【命名規約】
- メッセージ型：PascalCase（例：TicketCreate、AutoReply）
- ペイロード型：メッセージ型 + Payload suffix（例：TicketCreatePayload）
- フィールド名：camelCase（例：ticketId、operatorId）
- 状態値：PascalCase（例：Created、InProgress）
- API 関数名：動詞 + 名詞、camelCase（例：validatePayload、isValidTransition）
- 列挙値：PascalCase（例：Low、Medium、High、Resolved、Pending）
```

設計文書（PROTOCOL.md、API-SIGNATURES.md）に上記全てが含まれていることを確認。

## ステップ3：契約定義

**目的**：エージェントの前提条件と後提条件を形式化

各エージェント操作について、以下の契約を定義します：

```vdm-sl
-- 関数シグネチャ
decide : Ticket -> Score -> Score -> Action
decide(ticket, t1, t2) == ???

-- 前提条件（precondition）
pre decide(ticket, t1, t2) == 
  t1 > t2 and
  ticket.complexity_score >= 0 and t1 <= 100 and t2 <= 100

-- 後提条件（postcondition）
post decide(ticket, t1, t2) == 
  (let action = decide(ticket, t1, t2) in
    (ticket.complexity_score > t1 => action = <OperatorOnly>) and
    (t2 < ticket.complexity_score <= t1 => action = <OperatorAndLLM>) and
    (ticket.complexity_score <= t2 => action = <AutoReply>)
  )
```

**ユーザーへの質問**：
- この操作が前提とする条件は何か？（入力の有効性）
- この操作が保証する結果は何か？（出力の性質）
- 操作実行時のサイドエフェクトはあるか？（状態変化）
- 異常系（エラー条件）をどう扱うか？

**契約記述のチェックポイント**：
- 前提条件は検証可能か？
- 後提条件は実装可能か？
- 前提条件なしで後提条件が成立することはないか？
- エッジケース（境界値）を網羅しているか？

## ステップ4：VDM-SL生成

**目的**：Phase 1（ドメイン論理）のVDM-SL仕様書を自動生成

**重要**：このステップでは、ステップ2で定義したデータ型と、ステップ3で定義した契約（前提条件・後提条件）のみを VDM-SL に変換します。ステップ2bで生成した設計文書（PROTOCOL.md、API-SIGNATURES.md）は VDM-SL に含めません。プロトコル仕様は別ドキュメントとして実装エージェントが直接参照します。

ユーザーが提供した情報を整形して、完全なVDM-SL仕様モジュールを生成します：

```vdm-sl
module HybridJudgeAgent
imports all from Prelude

exports all

definitions

-- ======== 型定義 (Phase 1: ドメイン論理) ========

Score = nat1
Threshold = nat1

-- 不変式付き型
Score inv s == s >= 1 and s <= 100
Threshold inv t == t >= 1 and t <= 100

Action = <AutoReply> | <OperatorAndLLM> | <OperatorOnly>

-- ======== メイン関数 ========

decide : Ticket -> Score -> Score -> Action
decide(ticket, t1, t2) == 
  if ticket.complexity_score > t1
  then <OperatorOnly>
  elseif ticket.complexity_score > t2
  then <OperatorAndLLM>
  else <AutoReply>

pre decide(ticket, t1, t2) == 
  t1 > t2 and
  ticket.complexity_score >= 1 and ticket.complexity_score <= 100 and
  t1 <= 100 and t2 <= 100

post decide(ticket, t1, t2) == 
  (let action = decide(ticket, t1, t2) in
    (ticket.complexity_score > t1 => action = <OperatorOnly>) and
    (t2 < ticket.complexity_score <= t1 => action = <OperatorAndLLM>) and
    (ticket.complexity_score <= t2 => action = <AutoReply>)
  )

end HybridJudgeAgent
```

**生成される出力物**：
- モジュール定義（全型、関数、契約を含む）
- インポート文（必要な依存関係）
- エクスポート文（公開インターフェース）
- 別途：PROTOCOL.md（メッセージ型、ペイロード構造、状態遷移）
- 別途：API-SIGNATURES.md（共有モジュール API シグネチャ）

## ステップ5：仕様レビュー

**目的**：生成された仕様の正確性を確認

以下の観点からレビューをガイドします：

1. **型整合性**
   - 全ての参照型が定義されているか？
   - 型エラーはないか？
   - 集約型の構造は正しいか？

2. **不変式の妥当性**
   - 不変式は実装可能か？
   - 不変式は過度に厳しくないか？
   - 不変式は実装に必要か？

3. **契約の実現可能性**
   - 前提条件を満たす入力は存在するか？
   - 後提条件を満たす出力は存在するか？
   - 前提条件が満たされたとき、後提条件が必ず満たされるか？

4. **プロトコル完全性（v2.0.0）**
   - PROTOCOL.md に全てのメッセージ型が定義されているか？
   - 各メッセージ型に対応するペイロード構造が定義されているか？
   - 状態遷移マトリクスは完全か？
   - API-SIGNATURES.md の関数シグネチャは実装エージェントが参照できるか？

5. **名前付け規約の一貫性**
   - 型名、関数名は規約に従っているか？
   - 同様の概念に異なる名前がついていないか？

**レビューの実施**：
ユーザーに対して、以下の質問を提示します：
- 仕様の何か部分に疑問や不安があるか？
- 実装時に困難になりそうな部分はあるか？
- 現実のビジネス要件と異なる部分はあるか？

## ステップ6：契約テスト生成の提案

**目的**：VDM-SL仕様と設計文書から自動的にテストを生成

仕様レビューが完了したら、以下の提案をします：

```
提案：この仕様からユニットテストを自動生成しますか？

generate-tests スキルを実行すると、以下のテストが自動生成されます：

【Phase 1: ドメイン論理テスト】（VDM-SL仕様に基づく）

1. 型不変式テスト
   - Score型の値域チェック（1-100）
   - Threshold型の値域チェック
   - 無効な型の構築防止

2. 前提条件テスト
   - t1 > t2の検証
   - 複雑度スコアの有効範囲チェック
   - 無効な入力でのエラー処理

3. 後提条件テスト
   - 各判定ロジック（複雑度スコア > t1 => <OperatorOnly>等）
   - エッジケース（複雑度スコア == t1, == t2）
   - 全アクション型の網羅

【Phase 2: プロトコル・API テスト】（設計文書に基づく）

4. メッセージペイロード検証テスト
   - 各ペイロード型のフィールド妥当性チェック
   - null フィールドの処理検証
   - 必須フィールドの存在確認

5. 状態遷移テスト
   - 状態遷移マトリクスの有効性検証
   - 無効な遷移の拒否確認
   - 全状態・遷移パターンの網羅

6. API シグネチャ実装テスト
   - パラメータ順序の正確性
   - 戻り値型の一致確認
   - API 関数呼び出しの互換性

実行：[generate-tests スキルを実行]
```

## テンプレート参照

このスキルで使用される標準テンプレート：

### パターン1: データ変換エージェント
**参照**: `references/contract-templates.md` の「パターン1」セクション
- 入力データを変換し、異なる形式の出力を返すエージェント
- VDM-SL例：テキスト正規化、データ形式変換

### パターン2: CRUD エージェント
**参照**: `references/contract-templates.md` の「パターン2」セクション
- データストア上の作成・読み取り・更新・削除を管理するエージェント
- VDM-SL例：状態遷移、不変式による一貫性保証

### パターン3: パイプラインエージェント
**参照**: `references/contract-templates.md` の「パターン3」セクション
- 複数の処理ステップを順序立てて実行するエージェント
- VDM-SL例：シーケンス処理、ステップ間の整合性

### パターン4: メディエータエージェント
**参照**: `references/contract-templates.md` の「パターン4」セクション
- 複数のエージェント間の通信を仲介するエージェント
- VDM-SL例：メッセージルーティング、例外処理

### パターン5: バリデーション エージェント
**参照**: `references/contract-templates.md` の「パターン5」セクション
- 入力データの妥当性を検証するエージェント
- VDM-SL例：複合制約検証、エラーレポート

### パターン6: Phase 2設計文書テンプレート（新 v2.0.0）
**参照**: `references/contract-templates.md` の「パターン6」セクション
- マルチエージェント間の通信仕様を設計文書として定義するテンプレート
- 設計文書例：メッセージ型レジストリ、ペイロード構造、状態遷移マトリクス、API シグネチャ

### パターン7: ハイブリッド判定エージェント（新 v2.0.0）
**参照**: `references/contract-templates.md` の「パターン7」セクション
- スコアベースの複合判定を行うエージェント
- VDM-SL例：スコア計算、しきい値比較、判定ロジック

## ワークフロー図

```
ステップ1: エージェントロール抽出
    ↓
ステップ2: データ型定義（Phase 1: ドメイン論理）
    ↓
ステップ2b: 設計文書生成（PROTOCOL.md, API-SIGNATURES.md）（Phase 2: プロトコル・API仕様）
    ↓
ステップ3: 契約定義（前提条件・後提条件）
    ↓
ステップ4: VDM-SL仕様生成（Phase 1）
    ↓
ステップ5: 仕様・設計文書レビュー
    ↓
ステップ6: 契約テスト生成の提案（Phase 1 + Phase 2）
    ↓
[完了 または generate-tests スキルへ移行]
```

## 使用例

### 例1：シンプルなスコア計算エージェント

```
ユーザー入力：
- エージェント名：ScoreCalculator
- 責務：チケットの複雑度スコアを計算する
- 入力：Ticket型
- 出力：Score型（1-100）

生成される仕様：
module ScoreCalculator
  Score = nat1
  inv s == s >= 1 and s <= 100
  
  calculateScore : Ticket -> Score
  calculateScore(ticket) == ???
  
  post calculateScore(ticket) ==
    let score = calculateScore(ticket) in
      score >= 1 and score <= 100
end ScoreCalculator
```

### 例2：マルチエージェント通信を含むハイブリッドシステム

```
ユーザー入力：
- エージェント1：HybridJudgeAgent（判定）
- エージェント2：MessageValidator（検証）
- 間の通信：メッセージベースのプロトコル

生成される設計文書（ステップ2b）：
【PROTOCOL.md】
## メッセージ型レジストリ
| メッセージ型 | 送信元 | 受信先 | 同期/非同期 |
|---|---|---|---|
| TicketCreate | User | Server | 同期 |
| TicketUpdate | User | Server | 同期 |
| AutoReply | Server | User | 非同期 |

## ペイロード構造 (TicketCreate)
| フィールド | 型 | 必須 |
|---|---|---|
| content | string | yes |
| priority | enum | yes |
| attachments | string[] | no |

## 状態遷移マトリクス
| 現在 | Created | Assigned | InProgress | Resolved | Closed |
|---|:---:|:---:|:---:|:---:|:---:|
| Created | ✗ | ✓ | ✗ | ✗ | ✓ |
| ...

【API-SIGNATURES.md】
interface MessageValidator {
  validatePayload(msgType: string, payload: object): ValidationResult
  checkDirection(sender: string, msgType: string): boolean
}

interface StateTransition {
  isValidTransition(currentStatus: string, newStatus: string): boolean
}

生成される VDM-SL 仕様（ステップ4、Phase 1）：
module HybridSystem
  -- ステップ3で定義した契約（ドメイン論理）
  decide : Ticket -> Score -> Score -> Action
  pre/post ...
  
  -- 注意：メッセージ型・状態遷移は VDM-SL に含めない
  -- それらは PROTOCOL.md で定義されている
end HybridSystem
```

## トラブルシューティング

### Q: 型定義の時点で型チェックエラーが出ている
**A**: VDM-SLの型参照が循環していないか確認してください。循環参照がある場合は、型の定義順序を変更するか、前方宣言を使用してください。

### Q: 前提条件が厳しすぎて実装が困難
**A**: 前提条件の目的を再考してください。エージェントが入力を検証する責務を持つ場合、前提条件は「検証済み」という仮定として記述するべきです。一方、呼び出し元が責務を持つ場合は前提条件で強く制約してください。

### Q: プロトコル定義で方向判定関数が複雑になっている
**A**: メッセージ型を細分化することを検討してください。例えば `UserMsgType` をさらに `UserInMsgType` と `UserOutMsgType` に分割できます。

### Q: 後提条件が複数の関数に依存している
**A**: 後提条件は単一の関数の動作のみを記述するべきです。複数の関数の相互作用は、別途の統合テストで検証してください。

## 参考資料

- VDM-SL公式仕様：ISO/IEC 13817-1
- テスト生成スキル：`../generate-tests/SKILL.md`
- 仕様検証スキル：`../verify-spec/SKILL.md`

---

**最終更新**: 2026-04-12  
**バージョン**: 2.0.0  
**メンテナ**: Formal Agent Contracts チーム
