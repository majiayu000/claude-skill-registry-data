---
name: eip8183-agentic-commerce
description: >
  EIP-8183（Agentic Commerce）準拠のスマートコントラクト開発を包括的に支援するスキル。
  AI Agent間の信頼不要な商取引（Job escrow + evaluator attestation）を実現する
  ERC-8183プロトコルの設計・実装・テスト・デプロイをカバー。
  3者構造（Client/Provider/Evaluator）、6状態ステートマシン、
  IACPHookによる拡張、ERC-8004レピュテーション連携、x402マイクロペイメント統合、
  OpenZeppelin UUPS対応のリファレンス実装まで完全対応。
  Use when building AI agent commerce systems, implementing ERC-8183 or EIP-8183,
  creating job escrow contracts, building agentic marketplaces,
  integrating AI agents with smart contracts, implementing evaluator attestation patterns,
  or working with Virtuals Protocol ACP. Also use when the user mentions
  agent-to-agent commerce, agentic commerce, job escrow, evaluator contracts,
  ERC-8004 reputation integration, or asks about AI agent on-chain transactions.
---

# EIP-8183: Agentic Commerce スマートコントラクト開発ガイド

ERC-8183はEthereum Foundation dAIチームとVirtuals Protocolが共同策定した、
AI Agent間の信頼不要な商取引を可能にするERC標準（Draft）。
「Job escrow with evaluator attestation」パターンにより、
中央集権プラットフォームなしで「依頼→実行→検証→決済」を自動化する。

## コア概念

### 3者構造（Client / Provider / Evaluator）

| 役割 | 権限 | 実体の例 |
|------|------|---------|
| **Client** | Job作成、Provider設定、Budget合意、エスクロー資金供託、Open状態でのReject | AI Agent、EOA、マルチシグ |
| **Provider** | Budget提案、成果物提出（submit）、完了時に報酬受取 | AI Agent、サービスコントラクト |
| **Evaluator** | 唯一のcomplete/reject権限、Submitted状態の最終判定 | AI Agent、ZK検証コントラクト、マルチシグDAO |

Evaluatorが最も重要な役割。Job作成時に固定され変更不可。
Client自身がEvaluatorを兼ねることも可能（自己評価シナリオ）。

### 6状態ステートマシン

```
Open ──fund()──→ Funded ──submit()──→ Submitted ──complete()──→ Completed
 │                  │                      │
 │reject()      reject()/expire        reject()/expire
 ↓                  ↓                      ↓
Rejected          Rejected/Expired     Rejected/Expired
```

| 状態 | 遷移先 | トリガー |
|------|--------|---------|
| **Open** | Funded / Rejected | fund() / reject() |
| **Funded** | Submitted / Rejected / Expired | submit() / reject() / claimRefund() |
| **Submitted** | Completed / Rejected / Expired | complete() / reject() / claimRefund() |
| **Completed** | Terminal | エスクロー→Provider（手数料差引） |
| **Rejected** | Terminal | エスクロー→Client返金 |
| **Expired** | Terminal | エスクロー→Client返金 |

### Job構造体

```solidity
struct Job {
    uint256 id;
    address client;
    address provider;      // address(0)で後から設定可能
    address evaluator;     // 必須・不変
    string  description;   // ジョブの説明
    uint256 budget;        // ERC-20トークン量
    uint256 expiredAt;     // タイムアウトタイムスタンプ
    JobStatus status;      // 現在の状態
    address hook;          // オプショナルな拡張コントラクト
}
```

## コアインターフェース

```solidity
// Job作成・設定
function createJob(address provider, address evaluator, uint256 expiredAt,
    string calldata description, address hook) external returns (uint256 jobId);
function setProvider(uint256 jobId, address provider, bytes calldata optParams) external;
function setBudget(uint256 jobId, uint256 amount, bytes calldata optParams) external;

// 資金供託・成果物提出
function fund(uint256 jobId, uint256 expectedBudget, bytes calldata optParams) external;
function submit(uint256 jobId, bytes32 deliverable, bytes calldata optParams) external;

// 評価・終了
function complete(uint256 jobId, bytes32 reason, bytes calldata optParams) external;
function reject(uint256 jobId, bytes32 reason, bytes calldata optParams) external;
function claimRefund(uint256 jobId) external;
```

### 重要な設計ポイント
- `fund()` の `expectedBudget` はフロントラン保護（Budget変更攻撃を防止）
- `submit()` の `deliverable` はbytes32（IPFSハッシュ/CID等のオフチェーン参照）
- `complete()/reject()` の `reason` はbytes32（評価証拠ハッシュ、ERC-8004連携用）
- `claimRefund()` はパーミッションレス（誰でも呼べる、タイムアウト後の安全弁）
- `optParams` は将来の拡張用バイト列

## イベント

```solidity
event JobCreated(uint256 indexed jobId, address client, address provider,
    address evaluator, uint256 expiredAt);
event ProviderSet(uint256 indexed jobId, address provider);
event BudgetSet(uint256 indexed jobId, uint256 amount);
event JobFunded(uint256 indexed jobId, address client, uint256 amount);
event JobSubmitted(uint256 indexed jobId, address provider, bytes32 deliverable);
event JobCompleted(uint256 indexed jobId, address evaluator, bytes32 reason);
event JobRejected(uint256 indexed jobId, address rejector, bytes32 reason);
event JobExpired(uint256 indexed jobId);
event PaymentReleased(uint256 indexed jobId, address provider, uint256 amount);
event Refunded(uint256 indexed jobId, address client, uint256 amount);
```

## Hook（IACPHook）拡張システム

Hookにより、各アクションの前後にカスタムロジックを注入できる。
詳細は `references/hooks.md` を参照。

```solidity
interface IACPHook {
    function beforeAction(uint256 jobId, bytes4 selector, bytes calldata data) external;
    function afterAction(uint256 jobId, bytes4 selector, bytes calldata data) external;
}
```

**Hookable関数:** setProvider, setBudget, fund, submit, complete, reject
**Non-hookable:** claimRefund（安全弁として意図的にHook不可）

### 主要Hookパターン
- **レピュテーションゲート**: `beforeAction(fund)` でERC-8004スコアをチェック
- **入札マーケット**: `beforeAction(setProvider)` で複数Provider入札を管理
- **ZKプライバシー**: `afterAction(submit)` でZK証明の検証
- **アクセス制御**: `beforeAction(fund)` でNFTホールドやステーキング要件をチェック

## リファレンス実装パターン

詳細は `references/implementation.md` を参照。

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuardTransient.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract AgenticCommerce is
    UUPSUpgradeable,
    AccessControlUpgradeable,
    ReentrancyGuardTransient
{
    using SafeERC20 for IERC20;

    IERC20 public paymentToken;  // 1コントラクト=1トークン
    uint256 public jobCounter;
    mapping(uint256 => Job) public jobs;

    // コア実装...
}
```

### 設計上の制約
- **1コントラクト=1 ERC-20トークン**（USDC用とDAI用は別デプロイ）
- **成果物はオフチェーン保存**（IPFS/Arweave）、オンチェーンにはハッシュのみ
- **Evaluatorは作成時に固定**（変更不可）
- **紛争解決メカニズムなし**（reject/expireは最終決定）

## エコシステム統合

### ERC-8004（レピュテーション）
Agentの身元確認・評判管理標準。ERC-8183のcomplete/rejectイベントの
`reason`ハッシュをERC-8004レジストリに送ることで、Agent実績がオンチェーンに蓄積される。

### x402（HTTPマイクロペイメント）
同期的な単発APIアクセス課金プロトコル。
- **x402**: 1 HTTPラウンドトリップの同期支払い向き
- **ERC-8183**: 非同期マルチステップ作業 + エスクロー + 評価プロセス向き

### フルスタック構成
```
ERC-8004 (Identity/Reputation) — 「誰で、信頼できるか」
    ↕
ERC-8183 (Agentic Commerce) — 「依頼→実行→検証→決済」
    ↕
x402 (HTTP Payments) — 「どう支払うか（API課金）」
```

## Evaluator実装パターン

Evaluatorの設計がERC-8183システムの品質を決定する最重要部分。

| パターン | 用途 | 信頼性 |
|---------|------|--------|
| **Client自身** | 低リスク・信頼関係あり | 低（自己評価） |
| **単一AI Agent** | 主観的タスク評価 | 中（単一障害点） |
| **マルチモデル合意** | 高品質要求（3+モデルで70%合意） | 高 |
| **ZKスマートコントラクト** | 決定論的タスク検証 | 最高 |
| **マルチシグDAO** | 高価値・高リスク案件 | 高 |

## Agent統合パターン

### イベント監視（WebSocket）
```typescript
const contract = new Contract(ACP_ADDRESS, ACP_ABI, wsProvider);

contract.on("JobCreated", (jobId, client, provider, evaluator, expiredAt) => {
  if (provider === MY_AGENT_ADDRESS) handleNewJob(jobId);
});

contract.on("JobFunded", (jobId) => startWork(jobId));
contract.on("JobCompleted", (jobId) => updateReputation(jobId));
contract.on("JobRejected", (jobId) => handleRejection(jobId));
```

### コスト考慮
- 1 Jobライフサイクル = 最低4トランザクション（create + fund + submit + complete）
- Ethereum L1: ジョブあたり$20-50（ガス代）→ **L2デプロイが実質必須**
- L2（Base, Arbitrum等）: ジョブあたり〜$1

## コード生成ガイドライン

ERC-8183のコードを生成する際は以下を遵守：

1. **OpenZeppelinを使う** — SafeERC20、AccessControl、ReentrancyGuard、UUPS
2. **状態遷移を厳密に** — 各関数で正しい状態チェック + 権限チェックを実装
3. **Evaluatorアドレスの検証** — address(0)は不可、作成後は不変
4. **claimRefundはHook不可** — 悪意あるHookによるロック防止のため意図的設計
5. **expectedBudgetパラメータ** — fund()でフロントラン保護を必ず実装
6. **reasonハッシュを活用** — complete/rejectでオフチェーン証拠のハッシュを記録
7. **1コントラクト=1トークン** — マルチトークンは攻撃面を増やす
8. **L2デプロイを前提** — L1はガスコスト的に高頻度取引に不向き
9. **ERC-2771対応推奨** — `_msgSender()`でガスレス取引をサポート
10. **イベントは全て発火** — オフチェーン監視・レピュテーション連携に必須

## セキュリティ考慮事項

詳細は `references/security.md` を参照。

- Evaluator共謀リスク → レピュテーション/ステーキングで軽減
- 紛争解決メカニズムなし → アプリケーション層で対応
- 成果物可用性 → オフチェーンストレージのSLA保証が必要
- Hook悪用 → ホワイトリスト化、ガスリミット設定
- リエントランシー → ReentrancyGuardTransient使用

## リファレンスファイル

- `references/implementation.md` — 完全なリファレンス実装コードとパターン
- `references/hooks.md` — IACPHookの詳細と実装例
- `references/ecosystem.md` — ERC-8004/x402統合・エコシステム詳細
- `references/security.md` — セキュリティ考慮事項・監査チェックリスト
- `references/agent-integration.md` — AI Agent統合パターン（TypeScript/Python）
