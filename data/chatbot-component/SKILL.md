---
name: chatbot-component
description: ChatBotプロジェクトに新しいUIコンポーネントを追加するためのスキル。コンポーネント作成手順、CSS構成ルール、イベントハンドリングパターンを提供します。新しいUIコンポーネントを作成する時、モーダルを追加する時、CSSスタイルを追加する時、UIイベントを処理する時に使用してください。
---

# ChatBot コンポーネント追加スキル

このスキルはChatBotプロジェクトに新しいUIコンポーネントを追加する際のガイダンスを提供します。

## コンポーネント作成手順

### 1. JavaScriptクラスの作成

`app/public/js/components/{機能名}/{機能名}.js` に配置：

```javascript
class ComponentName {
    static #instance = null;

    constructor() {
        if (ComponentName.#instance) {
            return ComponentName.#instance;
        }
        ComponentName.#instance = this;
    }

    static get getInstance() {
        if (!ComponentName.#instance) {
            ComponentName.#instance = new ComponentName();
        }
        return ComponentName.#instance;
    }

    initialize() {
        this.#setupEventListeners();
    }

    #setupEventListeners() {
        // イベントリスナーの設定
    }
}
```

### 2. CSSスタイルの作成

`app/public/css/components/{カテゴリ}/{ファイル名}.css` に配置：

```css
.component-name {
    background: var(--background-secondary);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-md);
}

.component-name__element {
    /* BEM命名規則 */
}
```

### 3. HTMLの追加

`app/public/index.html` の適切な位置に要素を追加。

### 4. スクリプト読み込み

`app/public/index.html` の末尾にscriptタグを追加。

## CSS変数（必須使用）

色・間隔・サイズはすべてCSS変数で定義：

- 背景色: `--background-primary`, `--background-secondary`, `--background-tertiary`
- テキスト色: `--text-primary`, `--text-secondary`, `--text-tertiary`
- 間隔: `--spacing-xs` ~ `--spacing-xl`
- 角丸: `--border-radius-sm` ~ `--border-radius-xl`
- アニメーション: `--transition-fast`, `--transition-normal`

## 参考コンポーネント

- **チャット系**: `chatRenderer.js`, `chatUI.js`
- **サイドバー**: `sidebar.js`
- **モーダル**: `apiSettingsModal.js`, `systemPromptModal.js`

## 参照ファイル

詳細は以下のファイルを参照：

- `references/component-template.md`: コンポーネントテンプレート
- `references/css-structure.md`: CSS構成ルール
- `references/event-handling.md`: イベントハンドリングパターン
