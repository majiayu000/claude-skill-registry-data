---
name: generate-tests
description: >
  VDM-SL仕様と設計文書（PROTOCOL.md、API-SIGNATURES.md）から
  Jest/Vitest互換の契約テストを自動生成する。
  「仕様からテストを生成して」「契約テストを作って」「テストを自動生成して」
  「不変条件のテストを書いて」「プロトコルのテストを作って」
  「境界値テストを生成して」といったリクエストに使用する。
  English triggers: "generate tests from the spec", "create contract tests",
  "auto-generate tests", "generate boundary tests from the VDM spec".
  型不変式・事前条件・事後条件・状態遷移規則・ペイロード構造から
  テストコードを導出し、実装と仕様の乖離を検出する。
metadata:
  version: "2.1.0"
  author: Formal Agent Contracts
  tags: [vdm-sl, test-generation, automated-testing, vitest, model-routing]
---

# 契約テスト自動生成スキル (v2.1.0)

VDM-SL形式仕様および設計文書から自動的にユニットテストコードを生成するスキルです。VDM-SL仕様に記述された型不変式、前提条件、後提条件と、設計文書（PROTOCOL.md、API-SIGNATURES.md）に記述されたプロトコル規則をテストコードに変換し、実装の正確性を検証します。

## 背景：VDM-SL仕様と設計文書の役割分担

エージェント開発は2つのフェーズで契約を定義します：

| フェーズ | 役割 | 成果物 | このスキルでの使用 |
|--------|------|--------|-----------------|
| **Phase 1：ドメイン設計** | 各エージェント内部のロジックを形式化 | VDM-SL仕様ファイル | 型不変式、前後提条件テスト生成 |
| **Phase 2：インターフェース設計** | エージェント間通信を定義 | PROTOCOL.md、API-SIGNATURES.md | プロトコルテスト生成 |

### 実装時に発生する可能性のある問題と検出方法

| 問題カテゴリ | 例 | 検出方法 |
|------------|-----|--------|
| **実装バグ（ドメイン層）** | 後提条件のロジック誤り | ✓ VDM-SLテストで検出 |
| **言語固有の問題** | JavaScriptの型強制、nullの扱い | ✓ VDM-SLテストで検出 |
| **プロトコル層バグ** | メッセージ型とペイロードの不整合 | ✓ 設計文書テストで検出 |
| **エッジケース** | 境界値での動作未定義 | ✓ VDM-SLテストで検出 |
| **並行処理の問題** | レースコンディション（複数エージェント） | 統合テストで検出 |

このスキルは以下の2つのソースから自動テスト生成します：

**VDM-SL仕様から生成：**
1. **型不変式テスト**：型の制約が常に満たされるか
2. **前提条件テスト**：関数が前提条件を期待通り検証するか
3. **後提条件テスト**：関数が後提条件を満たす結果を返すか
4. **境界値テスト**：エッジケースでの動作

**設計文書（PROTOCOL.md）から生成：**
5. **プロトコルテスト**（新v2.0.0）：メッセージの型安全性、状態遷移の正確性、API署名の一貫性

## ステップ1：VDM-SLファイルと設計文書の解析

**目的**：VDM-SLファイルと設計文書から型、関数、契約、プロトコル仕様を抽出

ユーザーに以下の情報を提供してもらいます：

- **VDM-SLファイル**：解析対象のファイルパス
- **設計文書**：PROTOCOL.md、API-SIGNATURES.md（プロトコルテスト対象）
- **テスト対象関数**：全関数 / 特定関数のみ
- **テスト対象言語**：JavaScript / TypeScript / その他
- **テストフレームワーク**：Vitest（推奨） / Jest / Mocha

**スキルの処理**：
```
ステップ1a: VDM-SLファイルの構文解析
  ✓ モジュール構造を抽出
  ✓ 型定義を解析
  ✓ 関数シグネチャを抽出

ステップ1b: 契約情報の抽出
  ✓ 前提条件（pre）を読み込み
  ✓ 後提条件（post）を読み込み
  ✓ 不変式（inv）を収集

ステップ1c: メタデータの生成
  ✓ 関数の入出力型を記録
  ✓ テスト生成戦略を決定
  ✓ テストケース数を見積もり

出力例：
  [解析結果サマリー]
  ファイル: HybridJudgeAgent.vdmsl
  検出された型: 6個
    - Score (nat1, inv: 1<=s<=100)
    - Threshold (nat1, inv: 1<=t<=100)
    - Action (Quote型)
    - Ticket (Record型)
    - ...
  
  検出された関数: 3個
    - decide(Ticket, Score, Score) -> Action
    - scoreAll(seq of Score) -> seq of Score
    - explain_decision(...) -> seq of char
  
  推定テストケース数: 25-35個
```

## ステップ1.5：モデルルーティングの確認（任意・トークン削減）

仕様ファイルの隣に `model-routing.json`（`route-models` スキルの成果物）が存在する場合：

- モジュールごとに、割り当てモデルのサブエージェントでテスト生成を実行する
  （Claude Code では Task ツールの `model` パラメータ。層→モデル対応は必ず
  ルーティングファイルの `tiers` から読み、モデル名をハードコードしない）
- ファイルに記載のないモジュールは `defaults.tier` を適用する
- 生成テストのゲートは「実行して緑・型チェック」だけでは不十分（薄いスイートは
  自明に通ってしまう）。契約から機械的に導いた**条項→テスト対照表**で判定する：
  モジュール内のすべての inv / pre / post / 状態遷移条項に、対応するテストが
  少なくとも1つあること。対応漏れは検証失敗として数える。
  同一モジュールで2回検証に失敗したら1層上げて再生成し、`escalation.history` と
  MODEL-ROUTING.md の「Escalations」の両方に追記する（詳細は `route-models`
  スキルの `references/routing-rules.md` §4）
- サブエージェントのモデル指定が使えない環境では、推奨表として提示して
  通常どおり進める。ルーティング不可を理由にフェーズを失敗させない

ルーティングファイルが無ければ、このステップはスキップして通常どおり進める。

## ステップ2：テスト戦略の選択

**目的**：各関数に適したテスト生成戦略を決定

関数ごとに以下の戦略から選択：

### 戦略 A：型値テスト
**適用対象**：入力型が単純（nat1, bool, Quote型等）な関数
**テスト内容**：
- 有効な値の入力
- 無効な値の入力（型チェック）
- 境界値

```javascript
describe('Score type validation', () => {
  it('accepts valid score (1-100)', () => {
    expect(isValidScore(50)).toBe(true);
  });
  
  it('rejects invalid score (0)', () => {
    expect(isValidScore(0)).toBe(false);
  });
  
  it('rejects invalid score (101)', () => {
    expect(isValidScore(101)).toBe(false);
  });
});
```

### 戦略 B：前提条件テスト
**適用対象**：複雑な前提条件を持つ関数
**テスト内容**：
- 前提条件を満たす入力：実行可能
- 前提条件を満たさない入力：エラーまたは例外

```javascript
describe('decide function preconditions', () => {
  it('executes when t1 > t2', () => {
    const result = decide(ticket, 80, 20);
    expect(result).toBeDefined();
  });
  
  it('throws error when t1 <= t2', () => {
    expect(() => decide(ticket, 20, 80)).toThrow();
  });
});
```

### 戦略 C：後提条件テスト
**適用対象**：複雑な出力ロジックを持つ関数
**テスト内容**：
- 各ケースでの出力が後提条件を満たすか
- すべての出力パスをカバー

```javascript
describe('decide function postconditions', () => {
  it('returns OperatorOnly when complexity > t1', () => {
    const ticket = { complexity_score: 90 };
    const result = decide(ticket, 80, 20);
    expect(result).toBe('OperatorOnly');
  });
  
  it('returns OperatorAndLLM when t2 < complexity <= t1', () => {
    const ticket = { complexity_score: 50 };
    const result = decide(ticket, 80, 20);
    expect(result).toBe('OperatorAndLLM');
  });
  
  it('returns AutoReply when complexity <= t2', () => {
    const ticket = { complexity_score: 10 };
    const result = decide(ticket, 80, 20);
    expect(result).toBe('AutoReply');
  });
});
```

### 戦略 D：プロトコルテスト（新v2.0.0）
**適用対象**：PROTOCOL.md、API-SIGNATURES.mdに定義されたプロトコル仕様
**テスト内容**：
- メッセージ型とペイロードの整合性（PROTOCOL.mdから抽出）
- 状態遷移の有効性（PROTOCOL.mdから抽出）
- API署名の一貫性（API-SIGNATURES.mdから抽出）
- 方向判定関数の正確性（PROTOCOL.mdから抽出）

```javascript
describe('WsMessage protocol invariants', () => {
  it('TicketCreate message has correct payload type', () => {
    const msg = createMessage('TicketCreate', {
      customer_id: 1,
      title: 'Test'
    });
    expect(msg.msg_type).toBe('TicketCreate');
    expect(isTicketCreatePayload(msg.payload)).toBe(true);
  });
  
  it('rejects mismatched message and payload', () => {
    const msg = {
      msg_type: 'TicketCreate',
      payload: { ticket_id: 1, message: 'wrong' }  // AutoReplyPayload
    };
    expect(validateWsMessage(msg)).toBe(false);
  });
});

describe('State transitions', () => {
  it('allows valid transition Created->Assigned', () => {
    expect(validTransition('Created', 'Assigned')).toBe(true);
  });
  
  it('rejects invalid transition Created->InProgress', () => {
    expect(validTransition('Created', 'InProgress')).toBe(false);
  });
});
```

### 戦略 E：境界値テスト
**適用対象**：数値制約を持つ関数
**テスト内容**：
- 制約の下限・上限
- 制約外の値

```javascript
describe('boundary values', () => {
  it('accepts score at minimum boundary (1)', () => {
    expect(isValidScore(1)).toBe(true);
  });
  
  it('accepts score at maximum boundary (100)', () => {
    expect(isValidScore(100)).toBe(true);
  });
  
  it('rejects score below minimum (0)', () => {
    expect(isValidScore(0)).toBe(false);
  });
  
  it('rejects score above maximum (101)', () => {
    expect(isValidScore(101)).toBe(false);
  });
});
```

**選択ロジック**：
```
関数の特性 → 適用すべき戦略

1. 入力型が単純 → 戦略A（型値テスト）
2. 複雑な前提条件 → 戦略B（前提条件テスト）
3. 複雑な後提条件 → 戦略C（後提条件テスト）
4. プロトコル関連 → 戦略D（プロトコルテスト）
5. 数値制約あり → 戦略E（境界値テスト）

複数の戦略を組み合わせることも可能
（例：戦略A + B + E）
```

## ステップ3：テストコード生成

**目的**：VDM-SL仕様をテストコードに自動変換

### 3a. テスト構造の生成

```javascript
import { describe, it, expect } from 'vitest';
import {
  decide,
  scoreAll,
  explainDecision,
  validateTicket
} from './HybridJudgeAgent';

// ============================================
// テストスイート1：型不変式テスト
// ============================================

describe('HybridJudgeAgent - Type Invariants', () => {
  // Score不変式のテスト
  describe('Score type (nat1, inv: 1 <= s <= 100)', () => {
    // テストケース...
  });
  
  // Threshold不変式のテスト
  describe('Threshold type (nat1, inv: 1 <= t <= 100)', () => {
    // テストケース...
  });
});

// ============================================
// テストスイート2：前提条件テスト
// ============================================

describe('HybridJudgeAgent - Preconditions', () => {
  describe('decide(ticket, t1, t2) precondition: t1 > t2', () => {
    // テストケース...
  });
});

// ============================================
// テストスイート3：後提条件テスト
// ============================================

describe('HybridJudgeAgent - Postconditions', () => {
  describe('decide(ticket, t1, t2) postcondition', () => {
    // テストケース...
  });
});

// ============================================
// テストスイート4：プロトコルテスト（v2.0.0）
// ============================================

describe('MessageProtocol - Invariants', () => {
  // メッセージ型テスト...
});
```

### 3b. テストケースの生成

VDM-SL仕様から自動抽出したテストケース例：

```javascript
describe('decide function', () => {
  // 前提条件テストケース
  describe('precondition: t1 > t2', () => {
    it('succeeds when t1 (80) > t2 (20)', () => {
      const ticket = { 
        id: 1, 
        complexity_score: 50 
      };
      expect(() => decide(ticket, 80, 20)).not.toThrow();
    });
    
    it('throws when t1 (20) == t2 (20)', () => {
      const ticket = { id: 1, complexity_score: 50 };
      expect(() => decide(ticket, 20, 20)).toThrow(
        'Precondition failed: t1 > t2'
      );
    });
    
    it('throws when t1 (20) < t2 (80)', () => {
      const ticket = { id: 1, complexity_score: 50 };
      expect(() => decide(ticket, 20, 80)).toThrow(
        'Precondition failed: t1 > t2'
      );
    });
  });
  
  // 後提条件テストケース
  describe('postcondition: action determination', () => {
    const cases = [
      // [complexity_score, t1, t2, expectedAction]
      [90, 80, 20, 'OperatorOnly'],     // complexity > t1
      [50, 80, 20, 'OperatorAndLLM'],   // t2 < complexity <= t1
      [10, 80, 20, 'AutoReply'],        // complexity <= t2
      [80, 80, 20, 'OperatorAndLLM'],   // complexity == t1（エッジケース）
      [20, 80, 20, 'AutoReply'],        // complexity == t2（エッジケース）
    ];
    
    cases.forEach(([score, t1, t2, expected]) => {
      it(`returns ${expected} for complexity=${score}, t1=${t1}, t2=${t2}`, () => {
        const ticket = { id: 1, complexity_score: score };
        const result = decide(ticket, t1, t2);
        expect(result).toBe(expected);
      });
    });
  });
  
  // 境界値テスト
  describe('boundary values', () => {
    it('works with minimum score (1)', () => {
      const ticket = { id: 1, complexity_score: 1 };
      const result = decide(ticket, 80, 20);
      expect(result).toBe('AutoReply');
    });
    
    it('works with maximum score (100)', () => {
      const ticket = { id: 1, complexity_score: 100 };
      const result = decide(ticket, 80, 20);
      expect(result).toBe('OperatorOnly');
    });
  });
});
```

## ステップ4：設計文書ベースのプロトコルテスト生成（新v2.0.0）

**目的**：PROTOCOL.md および API-SIGNATURES.md に定義されたプロトコル契約とAPI契約の正確性をテスト

### プロトコル設計文書（PROTOCOL.md）の構造例

PROTOCOL.md は Markdown 形式で以下の情報を含む設計文書です：

```markdown
# WsMessage Protocol Specification

## Message Types

| Message Type | Direction | Payload Type | Description |
|-------------|-----------|--------------|-------------|
| TicketCreate | client→server | TicketCreatePayload | ユーザーがチケットを作成 |
| TicketCreated | server→client | TicketCreatedPayload | サーバーが作成確認 |
| AutoReply | server→client | AutoReplyPayload | 自動返信を送信 |
| Escalation | server→client | EscalationPayload | エスカレーションを通知 |

## State Transitions

```
Created → Assigned → InProgress → Resolved → Closed
         ↓ ↓
       ├─ Closed
```

## API Signatures (shared)

All API handlers must match these signatures:
- `processMessage(msg: WsMessage) -> Promise<Result>`
- `validatePayload(payload: any) -> boolean`
- `getMessageType(msg: WsMessage) -> MessageType`
```

このスキルは上記の設計文書をパースして、対応するテストを自動生成します。

### 4a. メッセージ型整合性テスト（設計文書から生成）

PROTOCOL.md の Message Types テーブルをパースして生成されるテスト：

```javascript
describe('WsMessage protocol layer (from PROTOCOL.md)', () => {
  describe('Message type and payload consistency', () => {
    // PROTOCOL.md のメッセージ定義テーブルから自動生成
    // 各メッセージ型について、指定されたペイロード型を持つことを検証
    
    it('TicketCreate message (client→server) has TicketCreatePayload', () => {
      const msg = {
        msg_type: 'TicketCreate',
        payload: { customer_id: 1, title: 'Test' },
        timestamp: Date.now()
      };
      // PROTOCOL.mdに定義されたペイロード構造を検証
      expect(validateWsMessage(msg)).toBe(true);
    });
    
    it('rejects TicketCreate with wrong payload (contract violation)', () => {
      const msg = {
        msg_type: 'TicketCreate',
        payload: { ticket_id: 1, reason: 'wrong' },  // EscalationPayload
        timestamp: Date.now()
      };
      // PROTOCOL.mdで指定されたペイロード型と不整合
      expect(validateWsMessage(msg)).toBe(false);
    });
    
    it('AutoReply message (server→client) has AutoReplyPayload', () => {
      const msg = {
        msg_type: 'AutoReply',
        payload: { ticket_id: 1, reply_text: 'Got it' },
        timestamp: Date.now()
      };
      // PROTOCOL.mdに定義されたペイロード構造を検証
      expect(validateWsMessage(msg)).toBe(true);
    });
    
    // ... PROTOCOL.mdに定義されたすべてのメッセージ型の組み合わせ
  });
  
  // 方向判定関数のテスト（PROTOCOL.mdのDirectionカラムから生成）
  describe('Direction validation (from PROTOCOL.md)', () => {
    it('TicketCreate is client→server per PROTOCOL.md', () => {
      const msg = { msg_type: 'TicketCreate' };
      expect(isClientToServer(msg)).toBe(true);
    });
    
    it('AutoReply is server→client per PROTOCOL.md', () => {
      const msg = { msg_type: 'AutoReply' };
      expect(isClientToServer(msg)).toBe(false);
    });
    
    it('rejects message from wrong direction', () => {
      const msg = { msg_type: 'TicketCreate' };
      // PROTOCOL.mdでclient→serverと指定されているが、
      // serverから送信しようとする
      expect(isValidDirection('server', msg)).toBe(false);
    });
  });
});
```

### 4b. 状態遷移テスト（設計文書から生成）

PROTOCOL.md の State Transitions セクションをパースして生成されるテスト：

```javascript
describe('TicketStatus state transitions (from PROTOCOL.md)', () => {
  describe('validTransition function - contract compliance', () => {
    // PROTOCOL.mdで定義された有効な遷移
    // 設計文書と実装の一貫性を検証（コントラクトテスト）
    const validTransitions = [
      ['Created', 'Assigned'],
      ['Created', 'Closed'],
      ['Assigned', 'InProgress'],
      ['Assigned', 'Closed'],
      ['InProgress', 'Resolved'],
      ['InProgress', 'Closed'],
      ['Resolved', 'Closed'],
      ['Closed', 'Closed'],
    ];
    
    validTransitions.forEach(([from, to]) => {
      it(`allows ${from} -> ${to} (PROTOCOL.md定義)`, () => {
        expect(validTransition(from, to)).toBe(true);
      });
    });
    
    // PROTOCOL.mdに定義されていない無効な遷移
    const invalidTransitions = [
      ['Created', 'InProgress'],
      ['Created', 'Resolved'],
      ['Assigned', 'Created'],
      ['InProgress', 'Assigned'],
      ['Resolved', 'InProgress'],
      ['Closed', 'Created'],
    ];
    
    invalidTransitions.forEach(([from, to]) => {
      it(`rejects ${from} -> ${to} (PROTOCOL.md違反)`, () => {
        expect(validTransition(from, to)).toBe(false);
      });
    });
  });
  
  // 到達可能性テスト（PROTOCOL.mdの状態遷移図から導出）
  describe('reachability (state diagram from PROTOCOL.md)', () => {
    it('all states are reachable from Created per PROTOCOL.md', () => {
      // PROTOCOL.mdの状態遷移図に従い、初期状態から全状態への到達可能性を検証
      const reachable = computeReachable('Created');
      expect(reachable).toContain('Created');
      expect(reachable).toContain('Assigned');
      expect(reachable).toContain('InProgress');
      expect(reachable).toContain('Resolved');
      expect(reachable).toContain('Closed');
    });
  });
});
```

### 4c. 複合プロトコルテスト（設計文書ベース）

PROTOCOL.md全体の整合性を検証する統合テスト：

```javascript
describe('Hybrid protocol scenario (from PROTOCOL.md)', () => {
  it('complete ticket lifecycle respects PROTOCOL.md contract', () => {
    // ユーザーがチケットを作成（PROTOCOL.mdで client→server と定義）
    const createMsg = {
      msg_type: 'TicketCreate',
      payload: { customer_id: 1, title: 'Bug' },
      timestamp: 1000
    };
    expect(isClientToServer(createMsg)).toBe(true);
    expect(validateWsMessage(createMsg)).toBe(true);
    
    // サーバーがチケットを確認応答（PROTOCOL.mdで server→client と定義）
    const createdMsg = {
      msg_type: 'TicketCreated',
      payload: { ticket_id: 100, status: 'Created' },
      timestamp: 1001
    };
    expect(isServerToClient(createdMsg)).toBe(true);
    expect(validateWsMessage(createdMsg)).toBe(true);
    
    // ステータスが PROTOCOL.md の状態遷移図に従って遷移
    expect(validTransition('Created', 'Assigned')).toBe(true);
    expect(validTransition('Assigned', 'InProgress')).toBe(true);
    expect(validTransition('InProgress', 'Resolved')).toBe(true);
    expect(validTransition('Resolved', 'Closed')).toBe(true);
  });
});
```

### 4d. 共有API署名テスト（API-SIGNATURES.mdから生成）

API-SIGNATURES.md に定義された共有API契約を検証：

```javascript
describe('Shared API signatures (from API-SIGNATURES.md)', () => {
  describe('Common handler interface compliance', () => {
    // API-SIGNATURES.mdで定義された関数シグネチャを実装が満たすか検証
    
    it('processMessage(msg) returns Promise<Result>', async () => {
      const handler = getMessageHandler('TicketCreate');
      const msg = { msg_type: 'TicketCreate', payload: { customer_id: 1 } };
      
      const result = handler.processMessage(msg);
      expect(result).toBeInstanceOf(Promise);
      
      const resolved = await result;
      expect(resolved).toHaveProperty('status');
      expect(resolved).toHaveProperty('data');
    });
    
    it('validatePayload(payload) returns boolean', () => {
      const handler = getMessageHandler('TicketCreate');
      const validPayload = { customer_id: 1, title: 'Test' };
      const invalidPayload = { wrong: 'fields' };
      
      expect(handler.validatePayload(validPayload)).toBe(true);
      expect(handler.validatePayload(invalidPayload)).toBe(false);
    });
    
    it('getMessageType(msg) returns MessageType string', () => {
      const handler = getMessageHandler('TicketCreate');
      const msg = { msg_type: 'TicketCreate', payload: {} };
      
      const msgType = handler.getMessageType(msg);
      expect(typeof msgType).toBe('string');
      expect(['TicketCreate', 'AutoReply', 'Escalation']).toContain(msgType);
    });
  });
});
```

## ステップ5：生成後の指導

**目的**：開発者がテストを実装に統合できるようサポート

### 5a. テスト実行ガイド

```bash
# テストの実行
npm test

# 特定のテストスイートのみ実行
npm test -- --grep "Type Invariants"

# カバレッジ測定
npm test -- --coverage
```

### 5b. テストカバレッジ確認

```
テストカバレッジレポート
=======================

ファイル: HybridJudgeAgent.js
行カバレッジ: 95%（57/60行）
分岐カバレッジ: 100%（12/12分岐）
関数カバレッジ: 100%（5/5関数）

行カバレッジ：
  ✓ 1-23行（型定義）: 100%
  ✓ 24-45行（decide関数）: 100%
  ✓ 46-60行（補助関数）: 85%（警告：1行未カバー）

警告：
  ⚠️ 60行目（explain_decision内の未知アクション処理）が未テスト
     修正：新しいアクション型を追加した場合、対応するテストケースを追加してください
```

### 5c. 失敗テストの解釈ガイド

```javascript
// テスト失敗例：
// ❌ decide function postcondition - returns OperatorOnly when complexity > t1
//    Expected: "OperatorOnly"
//    Received: "OperatorAndLLM"

// デバッグ手順：
// 1. 前提条件を確認：t1 > t2 が満たされているか？
console.log('t1:', 80, 't2:', 20, 't1 > t2:', 80 > 20); // true

// 2. 入力を確認：complexity_score の値は何か？
const ticket = { complexity_score: 50 };
console.log('complexity_score:', ticket.complexity_score);
console.log('complexity > t1:', 50 > 80); // false
console.log('t2 < complexity <= t1:', 20 < 50 && 50 <= 80); // true

// 3. 実装ロジックを確認
function decide(ticket, t1, t2) {
  if (ticket.complexity_score > t1) {
    return 'OperatorOnly';
  } else if (ticket.complexity_score > t2) {
    return 'OperatorAndLLM';  // ✓ この分岐が正しい
  } else {
    return 'AutoReply';
  }
}
// 実装は正しい。テストケースを再確認してください。
```

### 5d. テストメンテナンスガイド

```javascript
// ❌ 悪い例：ハードコードされた値
it('returns OperatorOnly for high complexity', () => {
  const ticket = { complexity_score: 95 };
  const result = decide(ticket, 80, 20);
  expect(result).toBe('OperatorOnly');
});

// ✓ 良い例：テストケース定義の集約化
const testCases = [
  { score: 95, t1: 80, t2: 20, expected: 'OperatorOnly' },
  { score: 50, t1: 80, t2: 20, expected: 'OperatorAndLLM' },
  { score: 10, t1: 80, t2: 20, expected: 'AutoReply' },
];

testCases.forEach(({ score, t1, t2, expected }) => {
  it(`returns ${expected} for score=${score}`, () => {
    const ticket = { complexity_score: score };
    const result = decide(ticket, t1, t2);
    expect(result).toBe(expected);
  });
});

// VDM-SL仕様が変更された場合、テストケースを一箇所で更新すれば全テストが更新される
```

## VDM-SL → テスト変換リファレンス

| VDM-SL要素 | テスト手法 | 生成されるテストコード例 |
|-----------|---------|----------------------|
| `inv s == s >= 1 and s <= 100` | 境界値テスト | `isValidScore(0)`, `isValidScore(1)`, `isValidScore(100)`, `isValidScore(101)` |
| `pre f(x) == x > 0` | 前提条件テスト | `expect(() => f(-1)).toThrow()` |
| `post f(x) == result > 0` | 後提条件テスト | `expect(f(x)).toBeGreaterThan(0)` |
| `Action = <A> \| <B> \| <C>` | 全値テスト | 各アクション型で別テストケース |
| `validTransition(from, to)` | 遷移テスト | `expect(validTransition('A', 'B')).toBe(true/false)` |
| `map T1 to T2` | マップ操作テスト | キー存在確認、値取得、更新テスト |

## バグ検出パターンと対策

| VDM-SL要素 | 想定バグ | テスト |
|-----------|--------|------|
| 不変式 | 常に真/偽のバグ | 型値テスト |
| 前提条件 | チェック漏れ | 前提条件テスト |
| 後提条件 | ロジック誤り | 後提条件テスト＋境界値 |
| Quote型の定義 | メッセージ型追加漏れ | メッセージ型カバレッジ |
| 状態遷移 | 無効遷移を許可 | 状態遷移テスト |
| 方向判定 | 双方向メッセージを許可 | 方向判定テスト |

## テスト実行とCI/CD統合

### GitHubActions例

```yaml
name: Formal Spec Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      # VDM-SL検証
      - name: Verify VDM-SL specification
        run: |
          npm run verify-spec
      
      # テスト実行
      - name: Run generated tests
        run: |
          npm test -- --coverage
      
      # カバレッジレポート
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

## トラブルシューティング

### Q: テストが多すぎて実行時間が長い
**A**: テスト戦略を絞ってください：
```
// ✗ すべてのテスト実行
npm test

// ✓ 特定のテストスイートのみ
npm test -- --grep "postcondition"

// ✓ 実装完了後の完全テスト
npm run test:full
```

### Q: テストが常に成功してしまう
**A**: テストが検証実装と一致していない可能性があります：
```javascript
// ❌ 悪い例：いつも成功する
it('decide returns Action', () => {
  const result = decide(ticket, 80, 20);
  expect(result).toBeDefined();  // 常に真
});

// ✓ 良い例：仕様を厳密に検証
it('decide returns OperatorOnly when score > t1', () => {
  const ticket = { complexity_score: 90 };
  const result = decide(ticket, 80, 20);
  expect(result).toBe('OperatorOnly');  // 具体的な値を期待
});
```

### Q: プロトコルテストでメッセージ型が追加されたのにテストが失敗する
**A**: PROTOCOL.md を更新してからテストを再生成してください：
```bash
# PROTOCOL.md と API-SIGNATURES.md を更新した場合
npm run regenerate-tests

# または手動で再生成（設計文書を指定）
node scripts/generate-tests.js \
  --vdmsl-file HybridJudgeAgent.vdmsl \
  --protocol-file PROTOCOL.md \
  --api-signatures-file API-SIGNATURES.md
```

**重要**: プロトコルテストはPROTOCOL.md の内容に従います。VDM-SL仕様の変更ではなく、 PROTOCOL.md を更新することがプロトコルテストの同期につながります。

## 参考資料

- テンプレート集：`./references/test-templates.md`
- Vitest ドキュメント：[https://vitest.dev](https://vitest.dev)
- VDM-SL型変換リファレンス：本ドキュメント内の表を参照
- 仕様検証スキル：`../verify-spec/SKILL.md`
- 仕様定義スキル：`../define-contract/SKILL.md`

---

**最終更新**: 2026-07-03  
**バージョン**: 2.1.0  
**メンテナ**: Formal Agent Contracts チーム
