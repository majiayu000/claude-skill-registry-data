---
name: world-miniapp
description: >
  World Chain MiniApp Kit / MiniKit SDKを使ったブロックチェーンアプリケーション開発を包括的に支援するスキル。
  World App内で動作するMiniApp（ミニアプリ）の設計・実装・デプロイまでをカバー。
  World ID（Proof of Personhood）によるユーザー認証、ウォレット認証（SIWE）、
  WLD/USDCトークン決済、スマートコントラクト連携（sendTransaction）、
  Permit2トークン転送、通知、連絡先共有、ハプティクスフィードバックなど、
  MiniKit SDKの全コマンドに対応。Next.jsベースのフルスタック開発をサポート。
  使用場面：(1) MiniAppの新規作成・セットアップ、(2) World ID検証の実装、
  (3) WLD/USDC決済機能の組み込み、(4) スマートコントラクトとの連携、
  (5) ウォレット認証（Wallet Auth / SIWE）実装、(6) World Chainハッカソン参加、
  (7) MiniAppのテスト・デプロイ。World App、World Chain、Worldcoin、MiniKit、
  minikit-js、World ID、Orb検証に関連する質問や開発作業すべてにこのスキルを使用すること。
---

# World MiniApp Development Support

World App内で動作するMiniApp開発を包括的に支援するスキル。
MiniKit SDKを使って、World IDによる人間認証・決済・スマートコントラクト連携を備えたアプリを構築する。

## クイックスタート

### MiniAppとは

MiniAppはWorld App内のWebViewで動作するWebアプリケーション。MiniKit SDKを通じてWorld Appのネイティブ機能にアクセスし、数百万ユーザーへのリーチを得られる。

**コアバリュー:**
- **Proof of Personhood**: World IDによるユニーク人間認証（Sybil耐性）
- **ウォレット統合**: World Walletで即座にトランザクション実行
- **配信チャネル**: World Appの数百万ユーザーにリーチ

### プロジェクトセットアップ

推奨：公式テンプレートを使用する。

```bash
npx @worldcoin/create-mini-app@latest my-mini-app
```

これによりNext.js 15ベースのプロジェクトが生成される。

手動セットアップの場合：

```bash
pnpm install @worldcoin/minikit-js
```

### MiniKitProvider設定

アプリのルートレイアウトでMiniKitProviderをラップする：

```tsx
// app/layout.tsx
import { MiniKitProvider } from "@worldcoin/minikit-js/minikit-provider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <MiniKitProvider>
        <body>{children}</body>
      </MiniKitProvider>
    </html>
  );
}
```

### 環境変数

```bash
# .env.local
APP_ID=app_xxxxx              # Developer Portalで取得
DEV_PORTAL_API_KEY=sk_xxxxx   # バックエンド検証用APIキー
NEXT_PUBLIC_APP_ID=app_xxxxx  # フロントエンド用（公開可）
```

### MiniKit利用可能チェック

World App内で実行されているかを確認：

```typescript
import { MiniKit } from "@worldcoin/minikit-js";

if (!MiniKit.isInstalled()) {
  // World App外 → フォールバックUI表示
  return;
}

// ウォレットアドレス取得
const walletAddress = MiniKit.walletAddress;
```

---

## MiniKit SDKコマンド一覧

全コマンドは `MiniKit.commandsAsync` で非同期呼び出しが推奨。
詳細は [minikit-api-reference.md](references/minikit-api-reference.md) を参照。

### コマンド呼び出しパターン

**推奨：Async パターン**

```typescript
const { commandPayload, finalPayload } = await MiniKit.commandsAsync.method(input);

if (finalPayload.status === "error") {
  console.error(finalPayload.error_code);
  return;
}
// success処理
```

**代替：Event Listener パターン**

```typescript
import { ResponseEvent } from "@worldcoin/minikit-js";

MiniKit.commands.method(input);
MiniKit.subscribe(ResponseEvent.EventName, (payload) => {
  // 処理
});
// クリーンアップ
MiniKit.unsubscribe(ResponseEvent.EventName);
```

### 主要コマンド概要

| コマンド | 用途 | 詳細 |
|---------|------|------|
| `verify` | World ID検証（Incognito Actions） | Orb/Device検証レベル |
| `walletAuth` | ウォレット認証（SIWE） | EIP-4361準拠のサインイン |
| `pay` | WLD/USDC決済 | Developer Portal API検証 |
| `sendTransaction` | スマートコントラクト実行 | Multicall・Permit2対応 |
| `signMessage` | メッセージ署名 | EIP-191準拠 |
| `signTypedData` | 型付きデータ署名 | EIP-712準拠 |
| `shareContacts` | 連絡先共有 | ユーザー選択式 |
| `share` | ネイティブ共有 | ファイル・URL共有 |
| `chat` | World Chatメッセージ | ユーザー名/アドレス指定可 |
| `requestPermission` | 権限リクエスト | 通知・マイク・連絡先 |
| `getPermissions` | 権限状態確認 | 付与済み権限の確認 |
| `sendHapticFeedback` | 触覚フィードバック | impact/notification/selection |

---

## World ID検証（Verify）

ユニーク人間であることを証明するWorld IDのIncognito Actionsを実装する。
これはSybil攻撃防止に重要で、投票・エアドロップ・アクセス制御などに使う。

### フロントエンド

```typescript
import { MiniKit, VerificationLevel } from "@worldcoin/minikit-js";

const verifyUser = async () => {
  const { finalPayload } = await MiniKit.commandsAsync.verify({
    action: "my-voting-action",     // Developer Portalで事前設定
    signal: "optional-signal-data", // オプション：追加データ
    verification_level: VerificationLevel.Orb, // Orb or Device
  });

  if (finalPayload.status === "success") {
    // バックエンドに送信して検証
    const res = await fetch("/api/verify", {
      method: "POST",
      body: JSON.stringify({
        payload: finalPayload,
        action: "my-voting-action",
        signal: "optional-signal-data",
      }),
    });
  }
};
```

### バックエンド検証

```typescript
// app/api/verify/route.ts
import { verifyCloudProof, IVerifyResponse } from "@worldcoin/minikit-js";

export async function POST(req: Request) {
  const { payload, action, signal } = await req.json();

  const verifyRes: IVerifyResponse = await verifyCloudProof(
    payload,
    process.env.APP_ID as `app_${string}`,
    action,
    signal
  );

  if (verifyRes.success) {
    // nullifier_hashをDBに保存（重複チェック用）
    return Response.json({ verified: true });
  }
  return Response.json({ verified: false }, { status: 400 });
}
```

**検証レベル:**
- `VerificationLevel.Orb` — Orb認証済みユーザーのみ（最高セキュリティ）
- `VerificationLevel.Device` — デバイス認証（より多くのユーザーがアクセス可能）

**Developer Portal設定が必要:**
- Incognito Actionの作成（action名の登録）

---

## ウォレット認証（Wallet Auth / SIWE）

Sign-In With Ethereum（EIP-4361）を使ったユーザー認証。セッション管理に使用。

### フロントエンド

```typescript
import { MiniKit } from "@worldcoin/minikit-js";

const signIn = async () => {
  // バックエンドからnonceを取得
  const nonceRes = await fetch("/api/nonce");
  const { nonce } = await nonceRes.json();

  const { finalPayload } = await MiniKit.commandsAsync.walletAuth({
    nonce,                          // 最低8文字の英数字
    statement: "Sign in to MyApp",  // オプション
    expirationTime: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 1週間
  });

  if (finalPayload.status === "success") {
    // バックエンドで署名検証
    const verifyRes = await fetch("/api/verify-auth", {
      method: "POST",
      body: JSON.stringify({ payload: finalPayload, nonce }),
    });
  }
};
```

### バックエンド検証

```typescript
// app/api/verify-auth/route.ts
import { verifySiweMessage, MiniAppWalletAuthSuccessPayload } from "@worldcoin/minikit-js";

export async function POST(req: Request) {
  const { payload, nonce } = await req.json() as {
    payload: MiniAppWalletAuthSuccessPayload;
    nonce: string;
  };

  // SIWE署名を検証
  const isValid = await verifySiweMessage(payload, nonce);

  if (isValid) {
    // セッション作成、payload.addressがウォレットアドレス
    return Response.json({ authenticated: true, address: payload.address });
  }
  return Response.json({ authenticated: false }, { status: 401 });
}
```

**重要な制約:**
- nonceは最低8文字の英数字
- スマートウォレット対応（ERC-1271, EIP-6492）

---

## 決済（Pay）

WLDまたはUSDCでの決済を実装する。World Chain上で実行される。

### フロントエンド

```typescript
import { MiniKit, Tokens, tokenToDecimals } from "@worldcoin/minikit-js";
import { v4 as uuidv4 } from "uuid";

const handlePayment = async () => {
  const reference = uuidv4(); // 一意な参照ID

  const { finalPayload } = await MiniKit.commandsAsync.pay({
    reference,
    to: "0xRecipientAddress...",
    tokens: [
      {
        symbol: Tokens.WLD,
        token_amount: tokenToDecimals(1, Tokens.WLD).toString(),
      },
    ],
    description: "Premium subscription",
  });

  if (finalPayload.status === "success") {
    // バックエンドでトランザクション検証
    await fetch("/api/verify-payment", {
      method: "POST",
      body: JSON.stringify({
        payload: finalPayload,
        reference,
      }),
    });
  }
};
```

### バックエンド検証

```typescript
// app/api/verify-payment/route.ts
export async function POST(req: Request) {
  const { payload, reference } = await req.json();

  // Developer Portal APIでトランザクション検証
  const response = await fetch(
    `https://developer.worldcoin.org/api/v2/minikit/transaction/${payload.transaction_id}?type=transaction`,
    {
      headers: {
        Authorization: `Bearer ${process.env.DEV_PORTAL_API_KEY}`,
      },
    }
  );

  const transaction = await response.json();

  if (transaction.reference === reference && transaction.status === "mined") {
    return Response.json({ success: true });
  }
  return Response.json({ success: false }, { status: 400 });
}
```

**制約:**
- 最小金額: $0.1/トランザクション
- ユーザーあたり1日500件の無料トランザクション
- ガスリミット: 1,000,000
- インドネシア・フィリピンでは利用不可

---

## スマートコントラクト連携（Send Transaction）

任意のスマートコントラクト関数を呼び出す。Multicallでの複数トランザクションに対応。

### 基本的な使い方

```typescript
import { MiniKit } from "@worldcoin/minikit-js";

const mintNFT = async () => {
  const { finalPayload } = await MiniKit.commandsAsync.sendTransaction({
    transaction: [
      {
        address: "0xContractAddress...",
        abi: [
          {
            inputs: [{ name: "to", type: "address" }],
            name: "mint",
            outputs: [],
            stateMutability: "nonpayable",
            type: "function",
          },
        ],
        functionName: "mint",
        args: [MiniKit.walletAddress],
      },
    ],
  });

  if (finalPayload.status === "success") {
    console.log("TX Hash:", finalPayload.transaction_id);
  }
};
```

### Permit2によるトークン転送

ERC-20トークンの転送にはPermit2（Signature Transfer）を使用：

```typescript
const transferWithPermit2 = async () => {
  const deadline = Math.floor(Date.now() / 1000 + 3600).toString();

  const { finalPayload } = await MiniKit.commandsAsync.sendTransaction({
    transaction: [
      {
        address: "0xYourContract...",
        abi: contractABI,
        functionName: "depositWithPermit",
        args: [
          MiniKit.walletAddress,
          tokenToDecimals(10, Tokens.WLD).toString(),
          "PERMIT2_SIGNATURE_PLACEHOLDER_0", // 自動的に署名で置換される
        ],
      },
    ],
    permit2: [
      {
        permitted: {
          token: "0x2cFc85d8E48F8EAB294be644d9E25C3030863003", // WLD
          amount: tokenToDecimals(10, Tokens.WLD).toString(),
        },
        spender: "0xYourContract...",
        nonce: Date.now().toString(),
        deadline,
      },
    ],
  });
};
```

### ETH送金（Payable関数）

```typescript
const sendETH = async () => {
  const { finalPayload } = await MiniKit.commandsAsync.sendTransaction({
    transaction: [
      {
        address: "0xForwardContract...",
        abi: ForwardABI,
        functionName: "pay",
        args: ["0xRecipient..."],
        value: "0x9184E72A000", // hex形式のwei値（0.00001 ETH）
      },
    ],
  });
};
```

---

## 通知（Notifications）

バックエンドからユーザーにプッシュ通知を送信する。

```typescript
// バックエンド
const sendNotification = async (walletAddresses: string[]) => {
  const response = await fetch(
    "https://developer.worldcoin.org/api/v2/minikit/send-notification",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.DEV_PORTAL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        app_id: process.env.APP_ID,
        wallet_addresses: walletAddresses,
        localisations: [
          {
            language: "en",
            title: "Rewards Available!",
            message: "Hey ${username}, your daily rewards are ready!",
          },
        ],
        mini_app_path: `worldapp://mini-app?app_id=${process.env.APP_ID}&path=/rewards`,
      }),
    }
  );
};
```

**制約:** 未認証アプリは4時間あたり40通知まで。

### フロントエンドでの通知権限リクエスト

```typescript
import { MiniKit, Permission } from "@worldcoin/minikit-js";

const requestNotifications = async () => {
  const { finalPayload } = await MiniKit.commandsAsync.requestPermission({
    permission: Permission.Notifications,
  });

  if (finalPayload.status === "success") {
    console.log("Notification permission granted!");
  }
};
```

---

## ソーシャル機能

### 連絡先共有

```typescript
const getContacts = async () => {
  const { finalPayload } = await MiniKit.commandsAsync.shareContacts({
    isMultiSelectEnabled: true,
    inviteMessage: "Join me on MyApp!",
  });

  if (finalPayload.status === "success") {
    // finalPayload.contacts: Array<{ username, walletAddress, profilePictureUrl }>
    for (const contact of finalPayload.contacts) {
      console.log(contact.username, contact.walletAddress);
    }
  }
};
```

### World Chatメッセージ

```typescript
const sendChat = async () => {
  const { finalPayload } = await MiniKit.commandsAsync.chat({
    message: "Check out this awesome mini app!",
    to: ["username1", "0x1234..."], // オプション：事前選択
  });
};
```

### ネイティブ共有

```typescript
await MiniKit.commandsAsync.share({
  title: "Invite Link",
  text: "Join my mini app!",
  url: "https://worldcoin.org/mini-app/xxx",
});
```

### プロフィールカード表示

```typescript
MiniKit.showProfileCard({
  username: "andy",
  walletAddress: "0x1234...",
});
```

---

## ハプティクスフィードバック

```typescript
MiniKit.commands.sendHapticFeedback({
  hapticsType: "impact",   // "impact" | "notification" | "selectionChanged"
  style: "light",          // "light" | "medium" | "heavy" | "success" | "warning" | "error"
});
```

---

## ユーザー情報取得

```typescript
// アドレスからユーザー情報取得
const user = await MiniKit.getUserByAddress("0x123...");
// ユーザー名から取得
const user = await MiniKit.getUserByUsername("andy");

// User型
type User = {
  walletAddress?: string;
  username?: string;
  profilePictureUrl?: string;
  permissions?: { notifications: boolean; contacts: boolean };
  optedIntoOptionalAnalytics?: boolean;
  worldAppVersion?: number;
  deviceOS?: string;
};
```

---

## ユーティリティ

```typescript
import { tokenToDecimals, Tokens } from "@worldcoin/minikit-js";

// 人間が読みやすい金額をトークンの最小単位に変換
const amount = tokenToDecimals(1, Tokens.WLD);   // BigInt
const amount2 = tokenToDecimals(5, Tokens.USDC);  // BigInt
```

---

## 開発ワークフロー

```
1. プロジェクト作成
   └── npx @worldcoin/create-mini-app@latest

2. Developer Portal設定
   ├── App ID取得
   ├── Incognito Actions設定（verify用）
   ├── 受取アドレスホワイトリスト（pay用）
   └── スマートコントラクト登録（sendTransaction用）

3. ローカル開発
   ├── MiniKitProvider設定
   ├── 各コマンド実装
   └── MiniKit.isInstalled()でWorld App外のフォールバック

4. テスト
   ├── World App Simulatorで動作確認
   └── Developer Portal APIのテスト

5. デプロイ
   ├── Vercel/Cloudflareなどにデプロイ
   └── Developer PortalでURL登録・公開
```

### Developer Portal URL

https://developer.worldcoin.org/

---

## トラブルシューティング

| 問題 | 原因 | 解決策 |
|------|------|--------|
| `MiniKit.isInstalled()` が false | World App外で実行中 | World App SimulatorまたはWorld Appで確認 |
| verify でエラー | Incognito Actionが未設定 | Developer Portalでactionを登録 |
| pay が失敗 | 受取アドレス未登録/最小金額未満 | Developer Portalで設定確認、$0.1以上 |
| sendTransaction失敗 | コントラクト未登録/ABI不一致 | Developer Portalでコントラクト登録、ABI確認 |
| walletAuth nonce エラー | nonce不正 | 最低8文字の英数字を使用 |
| 通知が届かない | 権限未取得/レート制限 | requestPermission実行、4h/40件制限 |

---

## 公式ドキュメント・リソース

- **公式ドキュメント**: https://docs.world.org/mini-apps
- **GitHub SDK**: https://github.com/worldcoin/minikit-js
- **Developer Portal**: https://developer.worldcoin.org/
- **LLM向け全文ドキュメント**: https://docs.world.org/llms-full.txt
- **Quick Start**: https://docs.world.org/mini-apps/quick-start/installing

最新情報は `https://docs.world.org/llms-full.txt` をWebFetchで取得して確認すること。
