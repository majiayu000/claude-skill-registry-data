---
name: semaphore-protocol
description: Comprehensive guide for integrating Semaphore V4 zero-knowledge protocol. Use when developing anonymous voting systems, privacy-preserving authentication, ZK proofs, smart contracts with group membership verification, or implementing Semaphore SDK features (Identity management, Group operations, Proof generation/verification). Also use when modifying, upgrading, or debugging existing Semaphore integrations.
---

# Semaphore Protocol Integration

## Overview

Semaphore V4は、ゼロ知識証明を使用してグループメンバーシップを匿名で証明できるプロトコルです。このスキルは、SemaphoreをSolidityコントラクトやTypeScript/JavaScriptアプリケーションに統合する際のガイドを提供します。

**主な機能:**

- 匿名グループメンバーシップの証明
- 二重シグナリング防止
- プライバシー保持型投票・認証システム

## Quick Start

### Installation

```bash
# コア機能（推奨）
npm install @semaphore-protocol/core

# または個別パッケージ
npm install @semaphore-protocol/identity
npm install @semaphore-protocol/group
npm install @semaphore-protocol/proof
npm install @semaphore-protocol/contracts
```

### 基本的な使い方

```javascript
import { Identity } from "@semaphore-protocol/identity"
import { Group } from "@semaphore-protocol/group"
import { generateProof, verifyProof } from "@semaphore-protocol/proof"

// 1. アイデンティティを作成
const identity = new Identity()

// 2. グループを作成してメンバーを追加
const group = new Group()
group.addMember(identity.commitment)

// 3. 証明を生成
const message = BigInt(1)
const scope = group.root
const proof = await generateProof(identity, group, message, scope)

// 4. 証明を検証
const isValid = await verifyProof(proof)
```

## Development Workflow

### 1. 新規コントラクト開発

Semaphoreを統合した新しいコントラクトを開発する場合：

**ステップ:**

1. **テンプレートを選択**: `assets/contract-templates/` から適切なテンプレートを選択
   - `BasicSemaphore.sol`: 基本的な統合
   - `VotingContract.sol`: 匿名投票システム
   - `AnonymousAuth.sol`: 匿名認証システム
2. **パッケージをインストール**: `npm install @semaphore-protocol/contracts`
3. **テンプレートをカスタマイズ**: 要件に応じてテンプレートを修正
4. **テストを作成**: 証明の生成・検証をテスト
5. **デプロイ**: Semaphoreコントラクトアドレスを指定してデプロイ

**テンプレートの使い方:**

```solidity
import "@semaphore-protocol/contracts/interfaces/ISemaphore.sol";

contract MyContract {
    ISemaphore public semaphore;
    uint256 public groupId;

    constructor(ISemaphore _semaphore) {
        semaphore = _semaphore;
        groupId = semaphore.createGroup();
    }

    function validateProof(
        ISemaphore.SemaphoreProof calldata proof
    ) external {
        semaphore.validateProof(groupId, proof);
        // 証明が有効な場合の処理...
    }
}
```

### 2. 既存コントラクトの修正

既存のSemaphore統合コントラクトを修正する場合：

**よくある変更:**

- **グループメンバー管理**: メンバーの追加・削除ロジックの変更
- **証明検証ロジック**: スコープやnullifierチェックのカスタマイズ
- **アクセス制御**: 誰がメンバーを追加できるかの変更

**ベストプラクティス:**

- 詳細なリファレンスが必要な場合は `references/semaphore-guide.md` を参照
- トラブルシューティングはリファレンスガイドの該当セクションを確認

### 3. コントラクトのアップグレード

Semaphoreプロトコルまたは統合コントラクトをアップグレードする場合：

**考慮事項:**

- **互換性**: 新しいSemaphoreバージョンとの互換性を確認
- **マイグレーション**: 既存のグループデータの移行計画
- **テスト**: アップグレード後の完全なテストスイート実行

**推奨手順:**

1. 新しいバージョンのドキュメントを確認
2. テストネットで検証
3. 段階的にロールアウト

## TypeScript/JavaScript Integration

TypeScriptでのフロントエンド統合例は `assets/typescript-examples/` を参照：

- **`identity-example.ts`**: Identity管理の完全な例
- **`group-example.ts`**: Group操作の完全な例
- **`proof-example.ts`**: Proof生成と検証の完全な例

### フロントエンドでの基本パターン

```typescript
// ユーザーのアイデンティティを管理
class IdentityManager {
  saveIdentity(id: string, identity: Identity): void {
    const exported = identity.export()
    localStorage.setItem(`identity-${id}`, exported)
  }

  loadIdentity(id: string): Identity | null {
    const exported = localStorage.getItem(`identity-${id}`)
    return exported ? Identity.import(exported) : null
  }
}

// 証明を生成してコントラクトに送信
async function submitVote(identity: Identity, group: Group, vote: bigint) {
  const proof = await generateProof(identity, group, vote, group.root)

  // コントラクトを呼び出す（ethers.js の例）
  const tx = await contract.castVote(vote, proof)
  await tx.wait()
}
```

## コアコンセプト

### 主要コンポーネント

1. **Identity（アイデンティティ）**: ユーザーの暗号学的なID（秘密鍵・公開鍵・コミットメント）
2. **Group（グループ）**: アイデンティティコミットメントのマークル木
3. **Proof（証明）**: グループメンバーシップのゼロ知識証明
4. **Nullifier（ヌリファイア）**: 二重シグナリング防止のための一意識別子
5. **Scope（スコープ）**: 証明が有効なコンテキスト（トピック/リソースID）

### 重要なセキュリティ注意事項

⚠️ **アイデンティティの再利用**: 同じアイデンティティを複数のグループで使用すると、すべてのグループのプライバシーが損なわれます。

⚠️ **Nullifierの管理**: 同じアイデンティティ+スコープからは常に同じNullifierが生成されるため、二重使用を検出できます。

## 詳細リファレンス

より詳しい情報が必要な場合は、以下を参照してください：

### `references/semaphore-guide.md`

完全なAPIリファレンス、トラブルシューティング、アーキテクチャの詳細を含む包括的なガイド。

**含まれる内容:**

- 各コンポーネントの詳細なAPI説明
- 設定パラメータ（MAX_DEPTH、証明有効期限など）
- よくあるエラーと解決方法
- サーキットとコントラクトのアーキテクチャ
- 公式リソースへのリンク集

**使用タイミング:**

- 特定のAPIの詳細が必要な場合
- エラーのトラブルシューティング
- パフォーマンス最適化
- セキュリティのベストプラクティス確認

## Contract Templates

### `assets/contract-templates/`

すぐに使える3つのSolidityテンプレート：

1. **`BasicSemaphore.sol`**: 基本的なSemaphore統合
   - グループ管理
   - メンバー追加・削除
   - メッセージの提出と検証

2. **`VotingContract.sol`**: 匿名投票システム
   - 提案の作成と管理
   - 匿名投票の記録
   - 二重投票防止

3. **`AnonymousAuth.sol`**: 匿名認証システム
   - リソースベースのアクセス制御
   - スコープごとのアクセス管理
   - アクセス履歴の追跡

## TypeScript Examples

### `assets/typescript-examples/`

実践的なTypeScript実装例：

1. **`identity-example.ts`**:
   - ランダム・決定論的アイデンティティの生成
   - エクスポート・インポート
   - ストレージ統合
   - セキュリティのベストプラクティス

2. **`group-example.ts`**:
   - グループ作成と管理
   - メンバー追加・削除・更新
   - マークル証明の生成
   - 投票グループ管理の実装例

3. **`proof-example.ts`**:
   - 基本的な証明生成と検証
   - カスタムスコープの使用
   - 二重シグナリング防止のデモ
   - 実用的な投票システムの実装

## Quick Reference

### デプロイ済みコントラクト

- Ethereum Mainnet
- Sepolia Testnet
- Arbitrum / Optimism
- 最新アドレス: [公式ドキュメント](https://docs.semaphore.pse.dev/deployed-contracts)

### 公式リソース

- [Documentation](https://docs.semaphore.pse.dev/)
- [GitHub](https://github.com/semaphore-protocol/semaphore)
- [Boilerplate App](https://github.com/semaphore-protocol/boilerplate)

## Common Use Cases

- **匿名投票**: プライバシーを保持した投票システム
- **内部告発**: 認証されたメンバーによる匿名報告
- **匿名DAO**: アイデンティティを明かさずにガバナンス参加
- **匿名認証**: グループメンバーシップの証明
- **ミキサー**: プライバシー保持型の価値転送
