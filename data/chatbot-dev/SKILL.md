---
name: chatbot-dev
description: ChatBotプロジェクトの開発全般を支援するスキル。プロジェクト構造、コーディング規約、開発ワークフローに関する知識を提供します。ChatBotプロジェクトで作業する時、プロジェクト構造について質問された時、コーディング規約について質問された時、新しい機能を追加する時に使用してください。
---

# ChatBot 開発スキル

このスキルはChatBotプロジェクトの開発全般を支援します。

## プロジェクト概要

- **フロントエンド**: HTML5/CSS3/JavaScript (ES6+)
- **バックエンド**: Node.js + Express (`app/server/index.js`)
- **AI API**: OpenAI, Claude, Gemini, Azure OpenAI対応
- **コード実行**: JavaScript, Python (Pyodide), C++ (g++/JSCPP), HTML
- **RAG**: Transformers.js + IndexedDB（ローカル埋め込み）
- **ポート**: 50000（デフォルト）

## 主要ディレクトリ

| パス | 説明 |
|------|------|
| `app/public/js/core/` | コアモジュール（API、config、storage等） |
| `app/public/js/core/rag/` | RAG機能（ベクトルストア、埋め込み、検索） |
| `app/public/js/components/` | UIコンポーネント |
| `app/public/js/modals/` | モーダルダイアログ |
| `app/public/js/utils/` | ユーティリティ関数 |
| `app/public/css/` | スタイルシート |
| `app/server/` | バックエンドサーバー |

## クラス設計パターン

### シングルトンパターン（必須）

すべてのクラスはシングルトンパターンで実装：

```javascript
class ClassName {
    static #instance = null;

    constructor() {
        if (ClassName.#instance) {
            return ClassName.#instance;
        }
        ClassName.#instance = this;
    }

    static get getInstance() {
        if (!ClassName.#instance) {
            ClassName.#instance = new ClassName();
        }
        return ClassName.#instance;
    }
}
```

### プライベートメソッド

ES2022のプライベートフィールド/メソッドを使用：

```javascript
#privateField = null;
#privateMethod() { /* ... */ }
```

## 設定管理

すべての設定値は `window.CONFIG` オブジェクトで管理：

```javascript
window.CONFIG.AIAPI.ENDPOINTS.OPENAI  // APIエンドポイント
window.CONFIG.STORAGE.KEYS.API_TYPE   // ストレージキー
window.CONFIG.AIAPI.DEFAULT_PARAMS    // デフォルトパラメータ
```

## 開発手順

1. 関連するコアファイルを確認
2. 既存パターンに従って実装
3. 適切なエラーハンドリングを追加
4. JSDocコメントで型情報を記載
5. **ドキュメント更新**（下記参照）

## ドキュメント更新ルール

**実装変更後は必ず以下を確認・更新すること：**

| 変更内容 | 更新対象 |
|----------|----------|
| 新機能追加 | `README.md`、`CLAUDE.md`、`references/project-structure.md` |
| ディレクトリ追加 | `CLAUDE.md`（構造）、`references/project-structure.md` |
| 設定値追加 | `CLAUDE.md`、`config.js`コメント |
| API変更 | `README.md`、`CLAUDE.md`、該当Skillファイル |
| 技術スタック変更 | `README.md`（技術スタック節）、`CLAUDE.md` |
| 既存機能の仕様変更 | 関連するすべてのドキュメント |

### 更新対象ファイル一覧

| ファイル | 内容 | 対象読者 |
|----------|------|----------|
| `README.md` | ユーザー向けガイド、機能説明、技術スタック | エンドユーザー |
| `CLAUDE.md` | 開発者向け概要、必須ルール、主要ファイル | AI/開発者 |
| `references/project-structure.md` | 詳細ディレクトリ構成 | AI/開発者 |

### チェックリスト

実装完了時に確認：

- [ ] `README.md` の主な特徴・技術スタックは最新か
- [ ] `CLAUDE.md` の機能説明は最新か
- [ ] `references/project-structure.md` のファイル構成は正確か
- [ ] 新しいモジュールは主要ファイル表に追加されているか
- [ ] 技術スタック（ライブラリ等）の変更は記載されているか

## 参照ファイル

詳細は以下のファイルを参照：

- `references/project-structure.md`: 詳細なディレクトリ構成
- `references/coding-conventions.md`: 命名規則、JSDoc
- `references/development-workflow.md`: 開発フロー
