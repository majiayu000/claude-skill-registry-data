---
name: github-gist-api
description: GitHub Gist API を使用したコードを書く際に使用。Gist作成、GistHack URL変換、ky/zod を使った実装パターンを提供。
---

# GitHub Gist API コード生成スキル

GitHub Gist API を使用したコードを書く際は、以下の仕様に従ってください。

## API 仕様

まず `docs/api-github-gist.md` を読んで、最新の API 仕様を確認してください。

## 基本ルール

1. **HTTP クライアント**: `ky` を使用する
2. **レスポンス検証**: `zod` でバリデーションする
3. **ID生成**: `nanoid` を使用する（必要な場合）
4. **型安全**: TypeScript で記述する

## 実装パターン

### Gist 作成の実装

```typescript
import ky from "ky";
import { z } from "zod";

// zod スキーマ
const GistFileSchema = z.object({
  filename: z.string(),
  type: z.string(),
  language: z.string().nullable(),
  raw_url: z.string().url(),
  size: z.number(),
  truncated: z.boolean(),
  content: z.string().optional(),
});

const GistResponseSchema = z.object({
  id: z.string(),
  url: z.string().url(),
  html_url: z.string().url(),
  files: z.record(z.string(), GistFileSchema),
  public: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
  description: z.string().nullable(),
});

type GistResponse = z.infer<typeof GistResponseSchema>;

// Gist 作成
async function createGist(
  token: string,
  html: string,
  description = "Deployed via PasteHost"
): Promise<GistResponse> {
  const response = await ky
    .post("https://api.github.com/gists", {
      headers: {
        Authorization: `token ${token}`,
        Accept: "application/vnd.github.v3+json",
      },
      json: {
        description,
        public: true, // GistHack を使うため public 必須
        files: {
          "index.html": {
            content: html,
          },
        },
      },
    })
    .json();

  return GistResponseSchema.parse(response);
}
```

### GistHack URL 変換

```typescript
function convertToGistHackUrl(rawUrl: string): string {
  return rawUrl.replace(
    "gist.githubusercontent.com",
    "gist.githack.com"
  );
}

// 使用例
async function deployToGist(token: string, html: string): Promise<string> {
  const gist = await createGist(token, html);
  const rawUrl = gist.files["index.html"].raw_url;
  return convertToGistHackUrl(rawUrl);
}
```

### エラーハンドリング

```typescript
import { HTTPError } from "ky";

try {
  const url = await deployToGist(token, html);
  console.log("Deployed:", url);
} catch (error) {
  if (error instanceof HTTPError) {
    const body = await error.response.json();
    if (error.response.status === 401) {
      console.error("Authentication failed. Check your token.");
    } else if (error.response.status === 422) {
      console.error("Validation error:", body.errors);
    } else {
      console.error("GitHub API Error:", body.message);
    }
  } else if (error instanceof z.ZodError) {
    console.error("Response validation error:", error.errors);
  } else {
    throw error;
  }
}
```

## Chrome 拡張での使用

Chrome 拡張のコンテキストでは:

1. `chrome.storage.sync` からトークンを取得
2. `navigator.clipboard.readText()` でクリップボード取得
3. GistHack URL を `navigator.clipboard.writeText()` でコピー

## 注意事項

- ファイル名に `gistfile` + 数字は使用禁止（Gist内部命名と競合）
- GistHack を使用するには `public: true` が必須
- raw_url は毎回コミットハッシュが変わる

## チェックリスト

コードを書く際は以下を確認:

- [ ] ky を使用している（fetch直接使用は避ける）
- [ ] zod でレスポンスをバリデーションしている
- [ ] GistHack URL変換を実装している
- [ ] `public: true` を設定している
- [ ] エラーハンドリングが適切
- [ ] 型定義が正確
