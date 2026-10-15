---
name: verify-spec
description: >
  VDM-SL仕様ファイルの検証（構文チェック・型チェック・証明責務生成）と、
  設計文書（PROTOCOL.md、API-SIGNATURES.md）の完全性チェックを実行する。
  「仕様を検証して」「VDMファイルをチェックして」「型チェックして」
  「PO（証明責務）を生成して」「仕様に問題がないか確認して」
  「エラーがないかチェックして」「.vdmslファイルを検証」といったリクエストに使用する。
  English triggers: "verify the spec", "type-check the VDM file",
  "generate proof obligations", "check the specification for errors".
  VDMJを使って検証を実行し、結果を形式手法の知識がない開発者にも
  わかるように自然言語で解説する。
metadata:
  version: "2.0.0"
  author: Formal Agent Contracts
  tags: [vdm-sl, verification, type-checking, formal-specification]
---

# 仕様検証スキル (v2.0.0)

VDM-SL仕様ファイルの構文チェック、型チェック、証明責務（PO: Proof Obligation）生成を実行し、開発者にわかりやすく結果を報告するスキルです。v2.0.0ではプロトコル層の整合性検証が追加されています。

## 概要

VDM-SLで記述された形式仕様は、以下の複数のレベルで検証が必要です：

1. **構文検証**：VDM-SL文法に従っているか
2. **型チェック**：型参照、型不整合がないか
3. **不変式検証**：不変式が一貫しているか
4. **契約検証**：前提条件と後提条件の整合性
5. **設計文書の完全性検証**（新v2.0.0）：PROTOCOL.md、API-SIGNATURES.mdの内容の完全性と矛盾確認
6. **証明責務生成**：形式証明が必要な条件を生成

このスキルは**VDMJツール**（ISO VDM-SLの標準実装）を使用して、これらの検証を自動実行します。

## ステップ1：検証ファイルの指定

**目的**：検証対象のVDM-SLファイルを特定

ユーザーに以下の情報を聞き出します：

- **ファイルパス**：検証するVDM-SLファイル（`.vdmsl`形式）
- **モジュール名**：検証対象のモジュール（例：`HybridJudgeAgent`）
- **検証範囲**：全モジュール / 特定の関数のみ
- **既存の検証結果**：過去に検証したことがあるか、前回のエラーは何か

**質問例**：
```
検証するVDM-SLファイルを教えてください：
形式：ファイルパスまたはファイル名
例：/path/to/agents/HybridJudgeAgent.vdmsl
```

## ステップ2：構文検証

**目的**：VDM-SL文法に従っているか確認

VDMJツールの構文チェッカーを実行し、以下を検証：

- キーワード（`module`, `exports`, `definitions`等）の正確性
- 型定義の文法（`Record ::`, `= ... |`等）
- 関数定義の文法（`pre/post`キーワード）
- クォーテーション（`<`,`>`の対応）
- コメント（`--`）の形式

**報告内容**：
```
構文検証結果
=============
✓ ファイル: /path/to/agents/HybridJudgeAgent.vdmsl
✓ エンコーディング: UTF-8
✓ 行数: 245行

✓ 構文チェック: PASSED

詳細：
- module定義: ✓
- 型定義: ✓ (8個の型を検出)
- 関数定義: ✓ (5個の関数を検出)
- pre/post条件: ✓
```

**エラー例**：
```
❌ 構文エラー (行127, 列14):
  予期しないトークン: 'def' の代わりに 'definitions' が必要
  
  126: export all
  127: defs
       ^^^^
  128:   Score = nat1
  
修正：'defs' → 'definitions'
```

## ステップ3：型チェック

**目的**：型の定義と参照の整合性を確認

VDMJツールの型チェッカーを実行し、以下を検証：

- 全ての型参照が定義されているか
- 型の構造が一貫しているか
- 関数のシグネチャが正しいか
- 不変式の型が正しいか

**報告内容**：
```
型チェック結果
==============
✓ ファイル: HybridJudgeAgent.vdmsl

✓ 型チェック: PASSED

検出された型：
  [1] Score = nat1
  [2] Threshold = nat1
  [3] Action = <AutoReply> | <OperatorAndLLM> | <OperatorOnly>
  [4] Ticket = ::
       - id: nat1
       - title: seq of char
       - content: seq of char
       - priority: nat0
       - complexity_score: Score

関数シグネチャ：
  [1] decide : Ticket -> Score -> Score -> Action
  [2] scoreAll : (seq of Score) -> seq of Score
  [3] explain_decision : (Score * Score * Score * Action) -> seq of char
```

**エラー例**：
```
❌ 型チェックエラー (行89):
  未定義の型を参照
  
  88: post decide(ticket, t1, t2) ==
  89:   let action = decide(...) in
  90:     action in set {<AutoReply>, <UnknownAction>}
                                    ^^^^^^^^^^^^^^^
問題：<UnknownAction> は Action型で定義されていません
定義されたアクション型：<AutoReply>, <OperatorAndLLM>, <OperatorOnly>
```

## ステップ4：不変式検証

**目的**：型の不変式が一貫性を保つか確認

各型に定義された`inv`（不変式）について：

- 不変式の型が正しいか（`bool`を返すか）
- 不変式が実装可能か（満たす値が存在するか）
- 不変式が矛盾していないか

**報告内容**：
```
不変式検証
==========

[1] Score inv s == s >= 1 and s <= 100
    ✓ 型: nat1 -> bool
    ✓ 実装可能性: 1, 2, ..., 100 が満たす
    ✓ 矛盾チェック: なし

[2] Threshold inv t == t >= 1 and t <= 100
    ✓ 型: nat1 -> bool
    ✓ 実装可能性: OK
    ✓ 矛盾チェック: なし

[3] WsMessage inv msg_inv(...) == (複雑な論理式)
    ⚠ 警告: 不変式が複雑（30個以上の論理句）
    推奨：より小さな補助不変式に分割してください

検証結果：3個中2個が完全に検証済み
```

**警告例**：
```
⚠ 不変式が矛盾している可能性（行156）:

inv confusing(x : nat1) == x > 10 and x < 5

この不変式を満たす自然数は存在しません。
確認：x > 10 AND x < 5 は常に偽です。
```

## ステップ5：契約検証

**目的**：前提条件と後提条件の実現可能性を確認

各関数について：

- 前提条件を満たす入力が存在するか
- 後提条件を満たす出力が存在するか
- 前提条件下で後提条件が必ず成立するか（証明責務）

**報告内容**：
```
契約検証
========

[1] 関数: decide(ticket, t1, t2) -> Action

前提条件分析：
  pre decide(ticket, t1, t2) ==
    t1 > t2 and
    ticket.complexity_score >= 1 and ticket.complexity_score <= 100 and
    t1 >= 1 and t1 <= 100 and
    t2 >= 1 and t2 <= 100

  ✓ 実現可能性: 有効な入力が存在
    例：ticket={id:1, complexity_score:50}, t1=80, t2=20

後提条件分析：
  post decide(ticket, t1, t2) ==
    (let action = decide(ticket, t1, t2) in
      (ticket.complexity_score > t1 => action = <OperatorOnly>) and
      (t2 < ticket.complexity_score <= t1 => action = <OperatorAndLLM>) and
      (ticket.complexity_score <= t2 => action = <AutoReply>)
    )

  ✓ 実装可能性: 後提条件を満たす動作が実装可能
  ✓ カバレッジ: 3つの判定ケースを網羅

[証明責務 PO1-1]
  前提条件: t1 > t2
  証明責務: 後提条件が必ず成立することを証明
  難易度: 低 (構造的に明白)
```

## ステップ6：設計文書の完全性検証（新 v2.0.0）

**目的**：エージェント間通信を定義するPROTOCOL.mdおよびAPI-SIGNATURES.mdの完全性と内部矛盾を確認

VDM-SL仕様ファイルが参照する設計文書（PROTOCOL.md、API-SIGNATURES.md）について、以下を検証します：

### 6a. 設計文書の存在確認

**検証項目**：
- PROTOCOL.mdが存在し、必須セクションを含むか
- API-SIGNATURES.mdが存在し、全モジュールのAPIが記載されているか

**報告内容**：
```
設計文書の存在確認
================

[1] PROTOCOL.md
    ✓ ファイル存在: あり
    ✓ 必須セクション:
      - メッセージ型レジストリ: ✓
      - ペイロード構造定義: ✓
      - 通信方向規約: ✓
      - 命名規約: ✓
    ✓ 行数: 347行
    ✓ エンコーディング: UTF-8

[2] API-SIGNATURES.md
    ✓ ファイル存在: あり
    ✓ モジュール数: 3個
      - HybridJudgeAgent: ✓
      - OperatorReplyHandler: ✓
      - StateTransitionManager: ✓
    ✓ 各モジュール: パラメータ名・型が記載
    ✓ 行数: 212行
    ✓ エンコーディング: UTF-8

検証結果: 全ての必須設計文書が存在
```

**エラー例**：
```
❌ ファイル欠落

PROTOCOL.mdが見つかりません：
  期待されるパス: /specs/PROTOCOL.md
  現在の状態: ファイルなし

修正：
  1. PROTOCOL.mdを作成してください
  2. メッセージ型、ペイロード構造、通信方向を記載してください
```

### 6b. PROTOCOL.mdの完全性検証

**検証項目**：
- すべてのメッセージ型がメッセージ型レジストリに記載されているか
- ペイロード構造がすべてのフィールド定義を含むか
- 通信方向が明記されているか

**報告内容**：
```
PROTOCOL.md 完全性検証
====================

メッセージ型レジストリ：
  [1] TicketCreate (Client → Server)
      定義あり ✓ - 必須フィールド確認
      ペイロード構造記載: ✓
      
  [2] TicketUpdate (Client → Server)
      定義あり ✓
      ペイロード構造記載: ✓
      
  [3] ReplyManual (Operator → Server)
      定義あり ✓
      ペイロード構造記載: ✓
      
  [4] AutoReply (Server → Client)
      定義あり ✓
      ペイロード構造記載: ✓

ペイロード構造例：
  TicketCreatePayload:
    - ticket_id: string (required)
    - title: string (required)
    - content: string (required)
    - priority: number (0-10, required)
    - nullable フィールド: なし ✓

命名規約チェック：
  ✓ メッセージ型: PascalCase (TicketCreate, AutoReply等)
  ✓ ペイロード型: {MessageType}Payload 形式
  ✓ フィールド: snake_case (ticket_id, msg_type等)
  ✓ 状態値: ALL_CAPS (CREATED, IN_PROGRESS等)

検証結果: PROTOCOL.md は完全で矛盾なし
```

**エラー例**：
```
❌ メッセージ型未記載 (PROTOCOL.md 行 34)

VDM-SL では以下のメッセージ型が定義されています：
  - TicketCreate
  - TicketUpdate
  - EscalationRequest
  - ReplyManual
  - MarkComplete
  - EscalateOperator ← PROTOCOL.md に記載されていません

修正：PROTOCOL.md メッセージ型レジストリに以下を追加してください：
  | EscalateOperator | Operator → Server | 操作者がチケットをシステム外にエスカレート |
```

### 6c. API-SIGNATURES.mdの完全性検証

**検証項目**：
- VDM-SLで定義された全モジュールのAPI（関数シグネチャ）が記載されているか
- パラメータ名、型情報が完全か
- 戻り値型が記載されているか

**報告内容**：
```
API-SIGNATURES.md 完全性検証
===========================

HybridJudgeAgent モジュール:
  関数 [1] decide(ticket, t1, t2) → Action
      VDM-SL定義: decide(ticket : Ticket, t1 : Score, t2 : Score) → Action
      API記載: ✓
        パラメータ: ticket (Ticket型), t1 (nat1, 1-100), t2 (nat1, 1-100)
        戻り値: Action (<AutoReply> | <OperatorAndLLM> | <OperatorOnly>)
        説明: チケットとスコアから判定アクションを決定
      
  関数 [2] scoreAll(scores) → seq of Score
      VDM-SL定義: scoreAll(scores : seq of Score) → seq of Score
      API記載: ✓
        パラメータ: scores (seq of Score)
        戻り値: seq of Score
        説明: スコア列を処理して出力スコア列を返す

  関数 [3] explain_decision(params) → string
      VDM-SL定義と API記載 ✓ 一致

OperatorReplyHandler モジュール:
  [1] processReply(msg) → Result ✓
  [2] validatePayload(payload) → bool ✓
  [3] sendToClient(msg, client_id) → void ✓

StateTransitionManager モジュール:
  [1] validTransition(from, to) → bool ✓
  [2] getValidNextStates(current_state) → set of TicketStatus ✓

検証結果: 全モジュール API が記載され、完全です
```

**エラー例**：
```
❌ API 未記載 (API-SIGNATURES.md)

VDM-SL で以下の関数が定義されていますが、API-SIGNATURES.md にはありません：

関数: validateTicketCreate(ticket : Ticket) → bool
      VDM-SLファイル行: 145-152
      必要な API エントリ:
        - パラメータ名と型
        - 戻り値型
        - 簡潔な説明

修正：API-SIGNATURES.md に以下を追加してください：
  #### validateTicketCreate
  - **Parameters**: ticket (Ticket)
  - **Returns**: bool
  - **Description**: チケットが作成条件を満たすかを検証
```

### 6d. VDM-SL定義との相互参照検証

**検証項目**：
- PROTOCOL.mdで定義されたメッセージ型がVDM-SLドメイン型と対応しているか
- API-SIGNATURES.mdのパラメータ型がVDM-SL関数シグネチャと一致しているか
- 状態値がPROTOCOL.mdとVDM-SLで同一か

**報告内容**：
```
VDM-SL定義との対応検証
====================

ドメイン型対応：
  VDM-SL定義: TicketStatus = <Created> | <Assigned> | <InProgress> | <Resolved> | <Closed>
  PROTOCOL.md参照: チケット状態の定義
    - CREATED ✓
    - ASSIGNED ✓
    - IN_PROGRESS ✓
    - RESOLVED ✓
    - CLOSED ✓
  対応状態: 完全一致

  VDM-SL定義: Score = nat1 inv s == s >= 1 and s <= 100
  PROTOCOL.md参照: スコア範囲
    記載: "スコアは 1 から 100 の自然数"
  対応状態: 一致 ✓

関数シグネチャ対応：
  VDM-SL: decide : Ticket -> Score -> Score -> Action
  API-SIGNATURES.md: decide(ticket: Ticket, t1: Score, t2: Score) -> Action
  対応状態: パラメータ名と型が一致 ✓

検証結果: VDM-SL定義と設計文書が完全に対応
```

**エラー例**：
```
❌ 型不一致 (VDM-SL vs 設計文書)

VDM-SL で定義されたメッセージ型：
  AllMsgType = UserMsgType | OperatorMsgType | ServerToUserMsgType

PROTOCOL.md に記載されたメッセージ型:
  TicketCreate, TicketUpdate, ReplyManual, AutoReply, OperatorReply
  (計 5個)

ただし VDM-SL でも 5個のメッセージしか定義されていないため、実際には矛盾がありません。

警告: より詳細に検証するため、メッセージ型定義セクションを再確認してください。
```

### 6e. 命名規約と可null性の一貫性

**検証項目**：
- 命名規約がPROTOCOL.md内で一貫しているか（snake_case, PascalCaseの混在がないか）
- nullable フィールドが PROTOCOL.md で明記されているか
- 設計文書と実装の命名が対応しているか

**報告内容**：
```
命名規約・可null性検証
===================

命名規約の一貫性：
  ✓ メッセージ型: PascalCase
    TicketCreate, TicketUpdate, AutoReply, OperatorReply
  
  ✓ ペイロード型: {Type}Payload 形式
    TicketCreatePayload, TicketUpdatePayload, AutoReplyPayload
  
  ✓ フィールド名: snake_case
    ticket_id, msg_type, timestamp, priority_level
  
  ✓ 状態値: ALL_CAPS
    CREATED, IN_PROGRESS, RESOLVED, CLOSED

可null性の注釈：
  ✓ TicketCreatePayload.description: nullable (✓ 注釈あり)
  ✓ OperatorReplyPayload.notes: nullable (✓ 注釈あり)
  ✓ その他全フィールド: required (✓ 注釈一貫)

設計文書の一貫性チェック：
  ✓ PROTOCOL.md での定義と API-SIGNATURES.md の記載が対応
  ✓ フィールド名の一貫性: 100% 一致

検証結果: 命名規約が統一されており、可null性が明記されている
```

**エラー例**：
```
❌ 命名規約の混在 (PROTOCOL.md 行 78)

ペイロード型の定義でケースが混在しています：

× TicketCreatePayload:
    - ticket_id (snake_case)
    - TicketStatus (PascalCase) ← 不一貫
    - messageType (camelCase) ← 不一貫

修正：すべてのフィールドを snake_case に統一してください：
  ✓ ticket_id
  ✓ ticket_status
  ✓ message_type
```

## ステップ7：証明責務生成と報告

**目的**：形式証明が必要な事項を特定し、開発者に提示

VDMJツールが自動生成する証明責務（PO: Proof Obligation）を分析し、以下をまとめます：

- 証明責務の種類（型健全性、前提条件実現可能性、後提条件充足可能性等）
- 難易度分類（自明、構造的に明白、要証明）
- テスト生成スキルへの提案

**報告例**：
```
証明責務（Proof Obligations）
============================

合計 3個の証明責務が生成されました。

[PO1] 型健全性: decide 関数の戻り値
  難易度: 自明 (Action型の値は必ず3値のいずれか)
  状態: ✓ 自動検証済み

[PO2] 前提条件実現可能性: t1 > t2
  難易度: 自明 (t1=80, t2=20等の例が存在)
  状態: ✓ 自動検証済み

[PO3] 後提条件充足: decide関数の正確性
  難易度: 構造的に明白
  条件:
    前提: t1 > t2, 1 <= complexity_score <= 100
    結論: 
      complexity_score > t1 => decide(...) = <OperatorOnly> AND
      t2 < complexity_score <= t1 => decide(...) = <OperatorAndLLM> AND
      complexity_score <= t2 => decide(...) = <AutoReply>
  
  証明スケッチ:
    complexity_scoreが確定した値であり、t1 > t2という前提の下では、
    3つの条件は排他的かつ網羅的。したがって正確に1つのアクションが決定される。
  
  状態: ✓ 論理的に明白（証明ツールで自動検証可能）

検証結果サマリー
================
✓ 構文検証: PASSED
✓ 型チェック: PASSED
✓ 不変式検証: PASSED
✓ 契約検証: PASSED
✓ 設計文書の完全性検証: PASSED
✓ 証明責務: 3個中3個が検証済み

全体結果: ✓ 仕様は形式的に正確です。

次のステップ：
1. generate-tests スキルを実行してユニットテストを生成
2. テストを実行して実装の正確性を検証
3. 必要に応じて仕様を改善
```

## ステップ8：契約テスト生成の提案

**目的**：検証が完了した仕様からテストを自動生成

検証がすべてパスしたら、以下を提案します：

```
提案：この仕様からユニットテストを自動生成しますか？

generate-tests スキルが以下のテストを生成します：

1. 型不変式テスト（Score, Threshold）
2. 前提条件テスト（t1 > t2の検証）
3. 後提条件テスト（判定ロジック3ケース）
4. プロトコルテスト（メッセージ整合性、状態遷移）
5. エッジケーステスト（境界値）

実行：[generate-tests スキルを実行]
```

## エラーレベルと対応

| レベル | 例 | 対応 |
|--------|-----|------|
| エラー❌ | 構文エラー、未定義型の参照 | 修正必須。VDMファイルが無効 |
| 警告⚠️ | 複雑な不変式、到達不可能な状態 | 推奨修正。仕様は有効だが改善余地あり |
| 情報ℹ️ | 検証完了、統計情報 | 参考情報。対応不要 |

## よくある検証エラーと修正例

### エラー1：未定義の型参照

```vdm-sl
❌ エラー（行45）:
  post decide(ticket, t1, t2) ==
    (ticket.complexity_score > t1 => result = <UnknownAction>)
                                                 ^^^^^^^^^^^^^^
  未定義の型: <UnknownAction>
  定義済み: <AutoReply>, <OperatorAndLLM>, <OperatorOnly>
```

**修正**：
```vdm-sl
-- ✓ 修正後
post decide(ticket, t1, t2) ==
  (ticket.complexity_score > t1 => result = <OperatorOnly>)
```

### エラー2：不変式が常に偽

```vdm-sl
❌ エラー（行12）:
  Score inv s == s >= 1 and s <= 100 and s > 200
                                         ^^^^^^^
  この不変式を満たす自然数は存在しません。
```

**修正**：
```vdm-sl
-- ✓ 修正後
Score inv s == s >= 1 and s <= 100
```

### 警告1：複雑な不変式

```vdm-sl
⚠️ 警告（行78）:
  WsMessage inv msg_inv(...) ==
    ... (35個の論理句)
  
  推奨：不変式が複雑すぎます。
```

**修正戦略**：
```vdm-sl
-- ✓ 補助不変式に分割
isValidTicketCreateMsg : WsMessage -> bool
isValidTicketCreateMsg(m) ==
  m.msg_type = <TicketCreate> => is_TicketCreatePayload(m.payload)

isValidAutoReplyMsg : WsMessage -> bool
isValidAutoReplyMsg(m) ==
  m.msg_type = <AutoReply> => is_AutoReplyPayload(m.payload)

-- メイン不変式は補助関数を呼び出す
inv msg_inv(m : WsMessage) ==
  isValidTicketCreateMsg(m) and
  isValidAutoReplyMsg(m) and
  ...
```

## トラブルシューティング

### Q: VDMJツールが見つからない
**A**: VDMJを以下の手順でインストールしてください：
1. [VDMJ GitHub](https://github.com/nickbattle/vdmj) からダウンロード
2. PATH に追加するか、スキル設定で vdmj パスを指定

### Q: "Record type used in set" というエラー
**A**: VDM-SLではレコード型を set 内に直接使用できません。map を使用してください：
```vdm-sl
❌ 間違い: set of Ticket
✓ 修正: map nat1 to Ticket  -- チケットID → チケット
```

### Q: 証明責務が多すぎる
**A**: 前提条件が弱すぎる可能性があります。前提条件を強化してください：
```vdm-sl
-- 弱い前提条件
pre decide(t1, t2) == true

-- 強い前提条件（推奨）
pre decide(t1, t2) == t1 > t2 and t1 >= 1 and t2 >= 1 and t1 <= 100
```

## VDMJコマンド参照

このスキルが使用するVDMJコマンド（VDMJ 4.x。jarは実行可能で、Main-Classは `com.fujitsu.vdmj.plugins.VDMJ`）：

```bash
# 構文チェック＋型チェック（デフォルト動作。ファイルは引数で渡す）
java -jar vdmj-4.7.0.jar -vdmsl spec.vdmsl

# 証明責務（PO）生成
java -jar vdmj-4.7.0.jar -vdmsl -p spec.vdmsl

# インタープリタ起動（型チェック成功後に対話モード）
java -jar vdmj-4.7.0.jar -vdmsl -i spec.vdmsl

# 式を評価して終了
java -jar vdmj-4.7.0.jar -vdmsl -e "式" spec.vdmsl
```

補助オプション：`-q`（情報メッセージ抑制）、`-w`（警告抑制）、`-default <モジュール名>`（デフォルトモジュール指定）。

**注意**：構文チェックのみ・型チェックのみを行う個別フラグはありません。デフォルト実行で構文→型の順に検証され、エラーは各段階で報告されます。`vdmj -check` や `-types`、`-fullcheck` というオプションは存在しません。

## 参考資料

- VDM-SL仕様：ISO/IEC 13817-1
- VDMJ ドキュメント：[VDMJ User Guide](https://github.com/nickbattle/vdmj/wiki)
- 形式手法のベストプラクティス：`../formal-methods-guide/SKILL.md`
- 仕様定義スキル：`../define-contract/SKILL.md`
- テスト生成スキル：`../generate-tests/SKILL.md`

---

**最終更新**: 2026-04-12  
**バージョン**: 2.0.0  
**メンテナ**: Formal Agent Contracts チーム
