---
name: hardhat3-dev
description: >
  Hardhat 3を使ったスマートコントラクト開発を包括的に支援するスキル。
  プロジェクト初期化、Solidity/TypeScriptテスト、Hardhat Ignitionデプロイ、
  ネットワーク設定、チートコード、ファズテスト、インバリアントテスト、
  Viem統合、マルチチェーン対応、Hardhat 2からの移行まで完全カバー。
  Use when building smart contracts with Hardhat, writing Solidity or TypeScript tests,
  deploying with Hardhat Ignition, configuring networks, using cheatcodes,
  migrating from Hardhat 2 to 3, or any Ethereum/EVM development task involving Hardhat.
  Also use when the user mentions hardhat.config.ts, forge-std, .t.sol files,
  EDR simulated networks, or asks about Solidity testing frameworks.
---

# Hardhat 3 Smart Contract Development

Hardhat 3はEthereum/EVMスマートコントラクト開発のための次世代開発環境。
Hardhat 2から大幅にアーキテクチャが刷新され、ESMファースト、宣言的設定、
Foundry互換Solidityテスト、マルチチェーンシミュレーション、新しいフックシステムなど
根本的な変更が加えられている。

このスキルはHardhat 3の正しいパターンに従ったコード生成・設定・テスト・デプロイを保証する。
Hardhat 2のパターンを使わないこと — 互換性がない部分が多い。

## 前提条件

- Node.js v22以上（必須）
- パッケージマネージャ: pnpm推奨（npm, yarnも可）
- VS Code + Hardhat公式拡張推奨

## クイックリファレンス

### プロジェクト初期化
```bash
mkdir my-project && cd my-project
npx hardhat --init
# ↑ "npx hardhat init" ではない（v2の書き方）
```

### 基本コマンド
```bash
npx hardhat build          # コンパイル（v2の"compile"から変更）
npx hardhat test            # 全テスト実行（Solidity + TypeScript）
npx hardhat test solidity   # Solidityテストのみ
npx hardhat test nodejs     # TypeScript（node:test）テストのみ
npx hardhat test <path>     # 特定ファイルのテスト
npx hardhat node            # ローカルノード起動
npx hardhat ignition deploy ignition/modules/MyModule.ts  # デプロイ
npx hardhat --help          # ヘルプ
```

### プロジェクト構造
```
my-project/
├── hardhat.config.ts       # メイン設定（ESM必須）
├── contracts/              # Solidityコントラクト
│   ├── MyContract.sol
│   └── MyContract.t.sol    # Solidityテスト（.t.sol拡張子）
├── test/                   # TypeScriptテスト
│   └── MyContract.ts
├── ignition/modules/       # Hardhat Ignitionデプロイモジュール
│   └── MyModule.ts
├── scripts/                # カスタムスクリプト
└── package.json
```

## Hardhat 3の核心的変更点（v2との違い）

Hardhat 2のパターンは動作しないため、以下の変更を必ず守ること。

### 1. ESMファースト
- `hardhat.config.ts`はESモジュール形式が必須
- `package.json`に`"type": "module"`を設定
- `import`/`export`を使う（`require`は設定ファイルでは使えない）

### 2. 宣言的設定（副作用ベースの登録は廃止）
```typescript
// Hardhat 3 ✅ — プラグインを明示的にインポートして配列で指定
import { defineConfig } from "hardhat/config";
import hardhatToolboxViem from "@nomicfoundation/hardhat-toolbox-viem";

export default defineConfig({
  plugins: [hardhatToolboxViem],
  solidity: "0.8.28",
});
```
```typescript
// Hardhat 2 ❌ — 副作用インポートは廃止
import "@nomicfoundation/hardhat-toolbox";
```

### 3. ネットワーク接続の管理
```typescript
// Hardhat 3 ✅ — 明示的に接続を作成
const { viem, networkHelpers } = await hre.network.connect();

// Hardhat 2 ❌ — hre.ethers のようなグローバルアクセスは廃止
const signers = await hre.ethers.getSigners();
```

### 4. タスク定義
```typescript
// Hardhat 3 ✅ — 宣言的タスク定義
import { task } from "hardhat/config";

const myTask = task("my-task", "説明")
  .setInlineAction(async (taskArgs, hre) => {
    const { provider } = await hre.network.connect();
    // ...
  })
  .build();

export default defineConfig({
  tasks: [myTask],
  // ...
});
```

### 5. ビルドコマンド
```bash
npx hardhat build    # ✅ Hardhat 3
npx hardhat compile  # ❌ Hardhat 2（廃止）
```

## 設定ファイル（hardhat.config.ts）

詳細は `references/configuration.md` を参照。以下は典型的な設定例：

```typescript
import { defineConfig, configVariable } from "hardhat/config";
import hardhatToolboxViem from "@nomicfoundation/hardhat-toolbox-viem";

export default defineConfig({
  plugins: [hardhatToolboxViem],
  solidity: {
    version: "0.8.28",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    // ローカルシミュレーション（Ethereum L1）
    hardhatMainnet: {
      type: "edr-simulated",
      chainType: "l1",
    },
    // OP Mainnetシミュレーション
    hardhatOp: {
      type: "edr-simulated",
      chainType: "op",
    },
    // テストネット
    sepolia: {
      type: "http",
      chainType: "l1",
      url: configVariable("SEPOLIA_RPC_URL"),
      accounts: [configVariable("SEPOLIA_PRIVATE_KEY")],
    },
  },
  test: {
    solidity: {
      timeout: 40000,
    },
  },
});
```

### ネットワークタイプ
- `"edr-simulated"`: インメモリシミュレーション（ローカル開発用）
- `"http"`: JSON-RPC接続（テストネット・メインネット用）

### チェーンタイプ
- `"l1"`: Ethereum Mainnet
- `"op"`: OP Mainnet（L2）
- `"generic"`: その他のチェーン

### configVariable
秘密情報（秘密鍵、RPC URL）は`configVariable()`でラップし、環境変数から読み込む。
ハードコードは絶対に避ける。

## Solidityテスト

Hardhat 3はFoundry互換のSolidityテストをネイティブサポート。
詳細は `references/solidity-testing.md` を参照。

### 基本パターン
```solidity
// contracts/Counter.t.sol
import { Counter } from "./Counter.sol";
import { Test } from "forge-std/Test.sol";

contract CounterTest is Test {
    Counter counter;

    function setUp() public {
        counter = new Counter();
    }

    function test_InitialValue() public view {
        assertEq(counter.x(), 0);
    }

    function test_Inc() public {
        counter.inc();
        assertEq(counter.x(), 1);
    }

    function test_IncByZero_Reverts() public {
        vm.expectRevert();
        counter.incBy(0);
    }
}
```

### テストファイルの配置
- `contracts/` 内の `.t.sol` ファイル
- `test/` 内の `.sol` ファイル
- `test` プレフィックスを持つ関数がテストとして認識される

### forge-stdのインストール
```bash
npm add --save-dev 'github:foundry-rs/forge-std#v1.9.7'
```

### ファズテスト
パラメータを持つtest関数は自動的にファズテストになる：
```solidity
function testFuzz_IncBy(uint8 amount) public {
    vm.assume(amount > 0);
    counter.incBy(amount);
    assertEq(counter.x(), amount);
}
```

### チートコード（vm.*）
Hardhat 3はFoundry互換のチートコードをフルサポート：
- `vm.prank(address)` — 次のコールの`msg.sender`を変更
- `vm.deal(address, amount)` — ETH残高を設定
- `vm.warp(timestamp)` — ブロックタイムスタンプを変更
- `vm.roll(blockNumber)` — ブロック番号を変更
- `vm.expectRevert()` — 次のコールがリバートすることを期待
- `vm.expectEmit()` — イベント発火を期待
- `vm.snapshot()` / `vm.revertTo()` — 状態スナップショット
- `vm.startPrank()` / `vm.stopPrank()` — 連続的なsender偽装
- `vm.assume()` — ファズテストの前提条件

全チートコード一覧: `references/cheatcodes.md`

### マルチチェーンテスト
```bash
npx hardhat test solidity --chain-type op  # OPチェーンとしてテスト
```

## TypeScriptテスト（Viem + node:test）

Hardhat 3の推奨TypeScriptテストスタックはViem + node:testビルトインテストランナー。
詳細は `references/typescript-testing.md` を参照。

### 基本パターン
```typescript
import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { network } from "hardhat";

describe("Counter", async function () {
  const { viem, networkHelpers } = await network.connect();

  it("should increment", async function () {
    const counter = await viem.deployContract("Counter");
    await counter.write.inc();
    assert.equal(await counter.read.x(), 1n);
  });
});
```

### 重要なポイント
- `network.connect()` で毎回新しいブロックチェーン状態を取得
- `viem.deployContract()` で型安全なコントラクトインスタンスを取得
- `counter.write.*()` で状態変更、`counter.read.*()` で参照
- コントラクト変更後は `npx hardhat build` で型定義を更新

### フィクスチャパターン
```typescript
async function deployFixture() {
  const counter = await viem.deployContract("Counter");
  const [owner, other] = await viem.getWalletClients();
  return { counter, owner, other };
}

it("test", async function () {
  const { counter } = await networkHelpers.loadFixture(deployFixture);
  // フィクスチャはスナップショットを使って高速にリセット
});
```

### イベントとリバートのテスト
```typescript
// イベント発火テスト
await viem.assertions.emitWithArgs(
  counter.write.inc(),
  counter,
  "Increment",
  [1n],
);

// リバートテスト
await viem.assertions.revertWith(
  counter.write.inc({ account: nonOwnerAddress }),
  "only the owner can increment",
);
```

### 必要なパッケージ
```bash
npm add --save-dev \
  @nomicfoundation/hardhat-viem \
  @nomicfoundation/hardhat-viem-assertions \
  @nomicfoundation/hardhat-node-test-runner \
  @nomicfoundation/hardhat-network-helpers \
  viem
```

## Hardhat Ignitionデプロイ

宣言的なデプロイモジュールシステム。詳細は `references/ignition.md` を参照。

### 基本モジュール
```typescript
// ignition/modules/Counter.ts
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("CounterModule", (m) => {
  const counter = m.contract("Counter");
  m.call(counter, "incBy", [5n]);
  return { counter };
});
```

### デプロイコマンド
```bash
# ローカルシミュレーション
npx hardhat ignition deploy ignition/modules/Counter.ts

# テストネット
npx hardhat ignition deploy ignition/modules/Counter.ts --network sepolia
```

### プロキシパターン（アップグレーダブル）
```typescript
const proxyModule = buildModule("ProxyModule", (m) => {
  const proxyAdminOwner = m.getAccount(0);
  const impl = m.contract("MyContract");
  const proxy = m.contract("TransparentUpgradeableProxy", [
    impl, proxyAdminOwner, "0x",
  ]);
  const proxyAdminAddress = m.readEventArgument(
    proxy, "AdminChanged", "newAdmin",
  );
  const proxyAdmin = m.contractAt("ProxyAdmin", proxyAdminAddress);
  return { proxyAdmin, proxy };
});
```

### テストでのIgnition使用
```typescript
const { ignition, viem } = await hre.network.connect();
const { counter } = await ignition.deploy(CounterModule);
assert.equal(await counter.read.x(), 0n);
```

## Hardhat 2からの移行

移行は段階的に行うこと。詳細は `references/migration.md` を参照。

### 移行手順の概要
1. `npx hardhat clean` で古いアーティファクトを削除
2. 全Hardhat 2パッケージをアンインストール
3. `package.json`に`"type": "module"`を追加
4. `tsconfig.json`のmoduleを`"node16"`に変更
5. `npm add --save-dev hardhat` でHardhat 3をインストール
6. `hardhat.config.ts`を宣言的形式に書き換え
7. テストを新しいAPIに移行
8. タスクを新しい形式に移行

### 主な破壊的変更
- ESM必須（設定ファイル）
- プラグインは`plugins`配列で明示的に登録
- `hre.ethers` → `const { viem } = await hre.network.connect()`
- `compile` → `build`
- `init` → `--init`
- `extendConfig`/`extendEnvironment` → フックシステム
- ネットワーク接続は明示的に管理

## プラグインシステム

### 推奨ツールボックス
- **hardhat-toolbox-viem**: Viem + node:test（推奨・新規プロジェクト向け）
- **hardhat-toolbox-mocha-ethers**: Mocha + ethers.js（v2互換寄り）

### プラグイン設定
```typescript
import { defineConfig } from "hardhat/config";
import hardhatToolboxViem from "@nomicfoundation/hardhat-toolbox-viem";

export default defineConfig({
  plugins: [hardhatToolboxViem],
});
```

### フックシステム
Hardhat 3はv2の`extendConfig`/`extendEnvironment`に代わるフックシステムを導入。
プラグイン作者はフックを使ってコア機能を拡張する。

## コード生成のガイドライン

Hardhat 3のコードを生成する際は以下を遵守：

1. **常にESM構文を使う** — `import`/`export`、`require`は使わない
2. **`defineConfig`を使う** — 型安全な設定
3. **`configVariable`で秘密情報を管理** — 直接ハードコードしない
4. **Viem + node:testを推奨** — ethers.js + Mochaも可能だが新規はViem推奨
5. **`build`コマンドを使う** — `compile`ではない
6. **ネットワーク接続は明示的に** — `const { viem } = await network.connect()`
7. **型安全を活用** — Hardhat 3は型付きアーティファクトを自動生成する
8. **forge-std v1.9.7を使う** — Solidityテストのアサーションライブラリ
9. **テストファイルは適切な場所に** — `.t.sol`は`contracts/`、`.ts`は`test/`
10. **Ignitionモジュールは`ignition/modules/`に** — 宣言的に記述

## リファレンスファイル

より詳細な情報が必要な場合は以下を参照：

- `references/configuration.md` — 設定オプション完全リファレンス
- `references/solidity-testing.md` — Solidityテスト・チートコード詳細
- `references/typescript-testing.md` — TypeScriptテスト・Viem統合詳細
- `references/ignition.md` — Hardhat Ignitionデプロイ詳細
- `references/migration.md` — Hardhat 2からの完全移行ガイド
- `references/cheatcodes.md` — 全チートコード一覧
