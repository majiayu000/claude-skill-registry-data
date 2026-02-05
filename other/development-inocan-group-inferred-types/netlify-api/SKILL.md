---
name: netlify-api
description: Netlify API を使用したコードを書く際に使用。ZIPデプロイ、サイト作成、ky/fflate/zod を使った実装パターンを提供。
---

# Netlify API コード生成スキル

Netlify API を使用したコードを書く際は、以下の仕様に従ってください。

## API 仕様

まず `docs/api-netlify.md` を読んで、最新の API 仕様を確認してください。

## 基本ルール

1. **HTTP クライアント**: `ky` を使用する
2. **レスポンス検証**: `zod` でバリデーションする
3. **ZIP生成**: `fflate` を使用する（jszipより軽量）
4. **型安全**: TypeScript で記述する

## 実装パターン

### ZIPデプロイの実装

```typescript
import ky from "ky";
import { zipSync, strToU8 } from "fflate";
import { z } from "zod";

// zod スキーマ
const NetlifyDeployResponseSchema = z.object({
  id: z.string(),
  state: z.string(),
  name: z.string(),
  url: z.string().url(),
  ssl_url: z.string().url(),
  admin_url: z.string().url(),
  deploy_url: z.string().url().optional(),
  created_at: z.string(),
  updated_at: z.string(),
});

type NetlifyDeployResponse = z.infer<typeof NetlifyDeployResponseSchema>;

// ZIP生成
function createZip(html: string): Uint8Array {
  return zipSync({
    "index.html": strToU8(html),
  });
}

// デプロイ実行
async function deployToNetlify(
  token: string,
  html: string
): Promise<NetlifyDeployResponse> {
  const zipData = createZip(html);
  const blob = new Blob([zipData], { type: "application/zip" });

  const response = await ky
    .post("https://api.netlify.com/api/v1/sites", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: blob,
    })
    .json();

  return NetlifyDeployResponseSchema.parse(response);
}
```

### エラーハンドリング

```typescript
import { HTTPError } from "ky";

try {
  const result = await deployToNetlify(token, html);
  console.log("Deployed:", result.ssl_url);
} catch (error) {
  if (error instanceof HTTPError) {
    const body = await error.response.json();
    console.error("Netlify API Error:", body.message);
  } else if (error instanceof z.ZodError) {
    console.error("Validation Error:", error.errors);
  } else {
    throw error;
  }
}
```

## Chrome 拡張での使用

Chrome 拡張のコンテキストでは:

1. `chrome.storage.sync` からトークンを取得
2. `navigator.clipboard.readText()` でクリップボード取得
3. 結果URLを `navigator.clipboard.writeText()` でコピー

## チェックリスト

コードを書く際は以下を確認:

- [ ] ky を使用している（fetch直接使用は避ける）
- [ ] zod でレスポンスをバリデーションしている
- [ ] fflate でZIPを生成している
- [ ] エラーハンドリングが適切
- [ ] 型定義が正確
