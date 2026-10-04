---
name: erc8004-trustless-agents
description: >
  ERC-8004（Trustless Agents）準拠のスマートコントラクト開発を包括的に支援するスキル。
  ブロックチェーンを活用した事前信頼不要のAgent発見・レピュテーション・検証プロトコルの
  設計・実装・テスト・デプロイをカバー。
  3つのレジストリ（Identity / Reputation / Validation）、ERC-721ベースのAgent ID、
  階層的信頼モデル（レピュテーション / ステーク担保 / zkML / TEE）、
  マルチチェーンデプロイ（35+ネットワーク）、ERC-8183 Agentic Commerce連携、
  A2A/MCPプロトコル統合、UUPSアップグレーダブル実装まで完全対応。
  Use when building AI agent discovery systems, implementing ERC-8004 or EIP-8004,
  creating agent identity registries, building reputation systems for AI agents,
  implementing validation registries, integrating agent trust mechanisms,
  or working with trustless agent protocols. Also use when the user mentions
  agent discovery, agent reputation, agent validation, trustless agents,
  identity registry, reputation registry, validation registry,
  A2A protocol integration, MCP tool registration, or asks about
  on-chain agent identity and trust infrastructure.
---

# ERC-8004: Trustless Agents スマートコントラクト開発ガイド

ERC-8004はブロックチェーンを使用して、事前の信頼関係なく組織の枠を超えて
AIエージェントを発見し、選択し、相互作用できるようにするERC標準（Draft）。
Model Context Protocol（MCP）やAgent2Agent（A2A）が解決しない
「エージェント発見と信頼」の課題を、3つの軽量レジストリで解決する。

## コア概念

### 3つのレジストリアーキテクチャ

```
┌─────────────────────────────────────────────────────┐
│            ERC-8004 Trustless Agents                 │
├─────────────────────────────────────────────────────┤
│  Identity Registry    │ ERC-721ベースのAgent ID       │
│  (IdentityRegistry)   │ 検出可能・転送可能・検閲耐性   │
├───────────────────────┼─────────────────────────────┤
│  Reputation Registry  │ フィードバック信号の標準化      │
│  (ReputationRegistry) │ オン/オフチェーン評判管理       │
├───────────────────────┼─────────────────────────────┤
│  Validation Registry  │ 第三者検証フック               │
│  (ValidationRegistry) │ zkML / TEE / ステーク検証      │
└───────────────────────┴─────────────────────────────┘
```

### グローバル識別子形式

```
{namespace}:{chainId}:{identityRegistry}
例: eip155:1:0x742d35Cc6634C0532925a3b844Bc9e7595f2bD68
```

| 要素 | 説明 | 例 |
|------|------|-----|
| **namespace** | チェーンファミリー識別子 | `eip155`（EVMチェーン） |
| **chainId** | ブロックチェーンネットワークID | `1`（Ethereum）、`8453`（Base） |
| **identityRegistry** | レジストリコントラクトアドレス | `0x742...` |
| **agentId** | 増分割り当てのトークンID | `22` |

### 階層的信頼モデル

リスクレベルに応じて信頼メカニズムを選択可能：

| 信頼モデル | リスクレベル | 用途例 | 特徴 |
|-----------|------------|--------|------|
| **レピュテーション** | 低〜中 | ピザ注文、データ取得 | クライアントフィードバック集約 |
| **ステーク担保再実行** | 中〜高 | コード生成、分析 | 複数参加者がタスク結果を検証 |
| **zkML証明** | 高 | ML推論検証 | ゼロ知識証明で計算正当性を保証 |
| **TEEオラクル** | 最高 | 医療診断、金融取引 | 信頼実行環境でのオラクル検証 |

## Identity Registry

ERC-721拡張のAgent ID管理。各AgentはNFTとして登録され、
ポータブルで検閲耐性のあるIDを保有する。

### コア構造体・関数

```solidity
struct MetadataEntry {
    string metadataKey;
    bytes metadataValue;
}

// 登録（3つのオーバーロード）
function register() external returns (uint256 agentId);
function register(string memory agentURI) external returns (uint256 agentId);
function register(string memory agentURI, MetadataEntry[] memory metadata)
    external returns (uint256 agentId);

// URI管理
function setAgentURI(uint256 agentId, string calldata newURI) external;

// メタデータ管理
function getMetadata(uint256 agentId, string memory metadataKey)
    external view returns (bytes memory);
function setMetadata(uint256 agentId, string memory metadataKey,
    bytes memory metadataValue) external;

// Agent Wallet管理（EIP-712署名検証）
function setAgentWallet(uint256 agentId, address newWallet,
    uint256 deadline, bytes calldata signature) external;
function getAgentWallet(uint256 agentId) external view returns (address);
function unsetAgentWallet(uint256 agentId) external;
```

### イベント

```solidity
event Registered(uint256 indexed agentId, string agentURI, address indexed owner);
event URIUpdated(uint256 indexed agentId, string newURI, address indexed updatedBy);
event MetadataSet(uint256 indexed agentId, string indexed indexedMetadataKey,
    string metadataKey, bytes metadataValue);
```

### Agent Registration File構造

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "agentName",
  "description": "自然言語説明",
  "image": "https://example.com/image.png",
  "services": [
    {
      "name": "A2A",
      "endpoint": "https://agent.example.com/.well-known/agent.json",
      "version": "0.3.0"
    },
    {
      "name": "MCP",
      "endpoint": "https://agent.example.com/mcp",
      "version": "1.0.0"
    }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [
    {
      "agentId": 22,
      "agentRegistry": "eip155:1:0x742..."
    }
  ],
  "supportedTrust": ["reputation", "crypto-economic", "tee-attestation"]
}
```

## Reputation Registry

フィードバック投稿・取得の標準インターフェース。

### フィードバック管理

```solidity
// フィードバック投稿
function giveFeedback(
    uint256 agentId,
    int128 value,           // フィードバック値（正負可）
    uint8 valueDecimals,    // 小数点桁数（0〜18）
    string calldata tag1,   // カテゴリタグ1
    string calldata tag2,   // カテゴリタグ2
    string calldata endpoint, // 評価対象エンドポイント
    string calldata feedbackURI, // オフチェーン詳細URI
    bytes32 feedbackHash    // オフチェーンデータハッシュ
) external;

// フィードバック取消
function revokeFeedback(uint256 agentId, uint64 feedbackIndex) external;

// レスポンス追加（Agent側からの応答）
function appendResponse(
    uint256 agentId,
    address clientAddress,
    uint64 feedbackIndex,
    string calldata responseURI,
    bytes32 responseHash
) external;
```

### フィードバック値の例

| tag1 | 測定対象 | サンプル | value | valueDecimals |
|------|--------|--------|-------|---------------|
| starred | 品質（0-100） | 87/100 | 87 | 0 |
| reachable | エンドポイント到達可能性 | true | 1 | 0 |
| uptime | 稼働率（%） | 99.77% | 9977 | 2 |
| successRate | 成功率（%） | 89% | 89 | 0 |
| latency | レイテンシ（ms） | 145.5ms | 1455 | 1 |

### 読み取り関数

```solidity
// サマリー取得（集約スコア）
function getSummary(
    uint256 agentId,
    address[] calldata clientAddresses,
    string calldata tag1,
    string calldata tag2
) external view returns (uint64 count, int128 summaryValue, uint8 summaryValueDecimals);

// 個別フィードバック読み取り
function readFeedback(uint256 agentId, address clientAddress, uint64 feedbackIndex)
    external view returns (
        int128 value, uint8 valueDecimals,
        string memory tag1, string memory tag2, bool isRevoked
    );

// クライアント一覧
function getClients(uint256 agentId) external view returns (address[] memory);

// 最終インデックス
function getLastIndex(uint256 agentId, address clientAddress)
    external view returns (uint64);
```

### イベント

```solidity
event NewFeedback(
    uint256 indexed agentId, address indexed clientAddress,
    uint64 feedbackIndex, int128 value, uint8 valueDecimals,
    string indexed indexedTag1, string tag1, string tag2,
    string endpoint, string feedbackURI, bytes32 feedbackHash
);

event FeedbackRevoked(
    uint256 indexed agentId, address indexed clientAddress,
    uint64 indexed feedbackIndex
);

event ResponseAppended(
    uint256 indexed agentId, address indexed clientAddress,
    uint64 feedbackIndex, address indexed responder,
    string responseURI, bytes32 responseHash
);
```

### オフチェーンフィードバックファイル

```json
{
  "agentRegistry": "eip155:1:{identityRegistry}",
  "agentId": 22,
  "clientAddress": "eip155:1:{clientAddress}",
  "createdAt": "2025-09-23T12:00:00Z",
  "value": 100,
  "valueDecimals": 0,
  "tag1": "starred",
  "tag2": "quality",
  "endpoint": "https://agent.example.com/GetPrice",
  "mcp": { "tool": "ToolName" },
  "a2a": {
    "skills": ["AgentSkill"],
    "contextId": "contextId",
    "taskId": "taskId"
  },
  "proofOfPayment": {
    "fromAddress": "0x00...",
    "toAddress": "0x00...",
    "chainId": "1",
    "txHash": "0x00..."
  }
}
```

## Validation Registry

第三者検証リクエスト・レスポンスの標準インターフェース。

### 検証フロー

```
Agent所有者 ─── validationRequest() ──→ Validation Registry
                                              │
Validator    ←── ValidationRequest event ─────┘
    │
    └── validationResponse() ──→ Validation Registry
                                      │
                                      └── ValidationResponse event
```

### コア関数

```solidity
// 検証リクエスト（Agent所有者/オペレーターのみ）
function validationRequest(
    address validatorAddress,
    uint256 agentId,
    string calldata requestURI,
    bytes32 requestHash
) external;

// 検証レスポンス（指定Validatorのみ）
function validationResponse(
    bytes32 requestHash,
    uint8 response,        // 0〜100（0=失敗、100=合格）
    string calldata responseURI,
    bytes32 responseHash,
    string calldata tag
) external;

// ステータス取得
function getValidationStatus(bytes32 requestHash)
    external view returns (
        address validatorAddress, uint256 agentId,
        uint8 response, bytes32 responseHash,
        string memory tag, uint256 lastUpdate
    );

// サマリー取得
function getSummary(
    uint256 agentId,
    address[] calldata validatorAddresses,
    string calldata tag
) external view returns (uint64 count, uint8 avgResponse);

// Agent/Validator別のリクエスト一覧
function getAgentValidations(uint256 agentId)
    external view returns (bytes32[] memory requestHashes);
function getValidatorRequests(address validatorAddress)
    external view returns (bytes32[] memory requestHashes);
```

### イベント

```solidity
event ValidationRequest(
    address indexed validatorAddress,
    uint256 indexed agentId,
    string requestURI, bytes32 indexed requestHash
);

event ValidationResponse(
    address indexed validatorAddress,
    uint256 indexed agentId,
    bytes32 indexed requestHash, uint8 response,
    string responseURI, bytes32 responseHash, string tag
);
```

## リファレンス実装パターン

詳細は `references/implementation.md` を参照。

### コントラクト構成

```
contracts/
├── IdentityRegistryUpgradeable.sol    # ERC-721 + メタデータ + EIP-712署名
├── ReputationRegistryUpgradeable.sol  # フィードバック管理
├── ValidationRegistryUpgradeable.sol  # 検証リクエスト/レスポンス
├── ERC1967Proxy.sol                   # UUPSプロキシ
├── MinimalUUPS.sol                    # デプロイヘルパー
└── SingletonFactory.sol               # CREATE2デプロイ
```

### 設計上の重要ポイント

- **ERC-721拡張**: Agent IDはNFTとして転送・売却・マーケットプレイス互換
- **ERC-7201準拠ストレージ**: Namespaced Storage Layoutでアップグレード安全性確保
- **EIP-712署名**: `setAgentWallet`でWallet所有権の暗号的証明
- **ERC-1271対応**: スマートコントラクトウォレット（AA）にも対応
- **自己フィードバック防止**: `giveFeedback`で所有者/オペレーターからのフィードバックを拒否
- **転送時Wallet自動クリア**: NFT転送でagentWalletを自動リセット（CEIパターン準拠）
- **チェーンごとのシングルトンレジストリ**: CREATE2で全チェーン同一アドレス

## エコシステム統合

### ERC-8183（Agentic Commerce）連携

```
ERC-8004 (Identity/Reputation) — 「誰で、信頼できるか」
    ↕
ERC-8183 (Agentic Commerce) — 「依頼→実行→検証→決済」
    ↕
x402 (HTTP Payments) — 「どう支払うか（API課金）」
```

- **Agent発見**: Identity Registryから Provider/Evaluator 候補を検索
- **レピュテーションゲート**: HookでERC-8004スコアに基づくアクセス制御
- **実績蓄積**: Job完了/拒否イベントのreasonハッシュをReputation Registryにフィードバック

### A2A / MCP プロトコル統合

Registration Fileの `services` フィールドで複数プロトコルエンドポイントを登録：
- **A2A**: `agent.json` エンドポイントでスキル・タスク管理
- **MCP**: ツール・プロンプト・リソース公開
- **ENS / DID**: 分散型識別子との連携

## マルチチェーンデプロイ

35+ネットワークにデプロイ済み。詳細は `references/deployments.md` を参照。

| チェーン | タイプ | 推奨用途 |
|---------|--------|---------|
| Ethereum | L1 | 高価値Agent、最高セキュリティ |
| Base | L2 (OP) | 一般的なAgent登録 |
| Arbitrum | L2 (Optimistic) | 一般的なAgent登録 |
| Polygon | L2 | 高頻度フィードバック |
| Monad | L1 | 高スループット |

## コード生成ガイドライン

ERC-8004のコードを生成する際は以下を遵守：

1. **OpenZeppelinを使う** — ERC721URIStorage、Ownable、UUPS、EIP712
2. **ERC-7201ストレージ** — Namespaced Storage Layoutでアップグレード安全性確保
3. **自己フィードバック防止** — `giveFeedback`で`isAuthorizedOrOwner`チェック必須
4. **agentWalletは予約キー** — `setMetadata`で"agentWallet"キーの直接設定を禁止
5. **転送時Wallet自動クリア** — `_update`オーバーライドでCEIパターン準拠
6. **EIP-712署名検証** — `setAgentWallet`でECDSA + ERC-1271フォールバック
7. **valueDecimalsは0〜18** — Reputation Registryでの入力バリデーション必須
8. **レスポンスは0〜100** — Validation Registryでの範囲チェック必須
9. **イベントは全て発火** — Subgraph/インデクサー連携に必須
10. **CREATE2デプロイ** — 全チェーン同一アドレスのためSingletonFactory使用

## セキュリティ考慮事項

詳細は `references/security.md` を参照。

- Sybil攻撃（偽Agent評判水増し） → レビュアー評判フィルタリングで対抗
- 自己フィードバック → `isAuthorizedOrOwner`チェックで防止
- agentWallet不正設定 → EIP-712署名 + deadline制限（MAX 5分）
- 転送時のWallet残存 → `_update`で自動クリア
- メタデータ改ざん → 所有者/オペレーターのみ書き込み可
- requestHash衝突 → 一意性チェック（既存requestHashの上書き防止）

## リファレンスファイル

- `references/implementation.md` — 完全なリファレンス実装コードとパターン
- `references/security.md` — セキュリティ考慮事項・監査チェックリスト
- `references/agent-integration.md` — AI Agent統合パターン（TypeScript/Python）
- `references/deployments.md` — マルチチェーンデプロイ情報
- `references/ecosystem.md` — ERC-8183/x402/A2A/MCP統合・エコシステム詳細
