---
name: chatbot-api
description: ChatBotプロジェクトに新しいAI APIを統合するためのスキル。APIクラスの実装パターン、プロキシ設定、ストリーミング実装を提供します。新しいAI APIを追加する時、APIクラスを実装する時、ストリーミング機能を追加する時、サーバープロキシを設定する時に使用してください。
---

# ChatBot API統合スキル

このスキルはChatBotプロジェクトに新しいAI APIを統合する際のガイダンスを提供します。

## API追加手順

### 1. 設定値の追加（config.js）

```javascript
// window.CONFIG.AIAPI.ENDPOINTS に追加
ENDPOINTS: {
    OPENAI: '/openai/v1/chat/completions',
    CLAUDE: '/anthropic/v1/messages',
    GEMINI: '/gemini/v1beta/models',
    NEW_API: '/newapi/v1/chat'  // 新しいエンドポイント
}

// window.CONFIG.STORAGE.KEYS に追加
KEYS: {
    NEW_API_KEY: 'newApiKey'  // 新しいAPIキー
}
```

### 2. APIクラスの作成

`app/public/js/core/newApi.js` に配置。

### 3. サーバープロキシの追加

`app/server/index.js` にプロキシ設定を追加。

### 4. api.js への統合

`AIAPI.callAIAPI` メソッドにルーティングを追加。

### 5. UI設定の追加

APIキー設定モーダルにフォームを追加。

## 既存APIクラス一覧

| クラス | ファイル | 機能 |
|--------|----------|------|
| `OpenAIAPI` | `openaiApi.js` | OpenAI Chat Completions API |
| `ClaudeAPI` | `claudeApi.js` | Anthropic Claude Messages API |
| `GeminiAPI` | `geminiApi.js` | Google Gemini API |
| `ResponsesAPI` | `responsesApi.js` | OpenAI Responses API (Web検索) |

## 必須メソッド

1. `callXxxAPI(messages, model, attachments, options)` - メインAPI呼び出し
2. `#validateAPISettings()` - API設定の検証
3. `#prepareXxxRequest()` - リクエスト準備
4. `#executeXxxRequest()` - 非ストリーミング実行
5. `#executeStreamXxxRequest()` - ストリーミング実行

## 参照ファイル

詳細は以下のファイルを参照：

- `references/api-class-template.md`: 完全なAPIクラステンプレート
- `references/server-proxy-setup.md`: Express プロキシ設定方法
- `references/streaming-implementation.md`: SSE実装パターン
