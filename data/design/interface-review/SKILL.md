---
name: interface-review
description: Review web interface implementations across Interactivity, Typography, Motion, Touch, Optimizations, Accessibility, and Design/UX. Based on industry best practices and UX psychology principles. Use for UI component and page implementation reviews.
allowed-tools: Read, Grep, Glob
---

# Interface Review Skill

このスキルは、Web インターフェースの実装を業界のベストプラクティスと UX 心理学に基づいてレビューします。

## 目的

- インタラクティブ要素のユーザビリティを検証
- タイポグラフィの品質を確認
- アニメーションとモーションの適切性をチェック
- タッチデバイス対応を検証
- パフォーマンス最適化を確認
- アクセシビリティ準拠を検証
- デザイン、ユーザー体験、UX 心理効果を統合的に評価

## レビュー領域

### 1. Interactivity（インタラクティビティ）

**主要チェックポイント**:

- フォーム要素の適切な実装
- ボタンの二重送信防止
- インタラクティブ要素の `user-select` 設定
- ラベルとインプットの関連付け
- Enter キーでのフォーム送信

**検証項目**:

```typescript
// ✅ 正しい実装
<form onSubmit={handleSubmit}>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    type="email"
    required
    autoComplete="off"
    spellCheck="false"
  />
  <button type="submit" disabled={isSubmitting}>
    Submit
  </button>
</form>

// ❌ 問題のある実装
<div> {/* form タグなし */}
  <span>Email</span> {/* label なし */}
  <input type="text" /> {/* type が不適切 */}
  <button onClick={handleClick}> {/* 二重送信防止なし */}
    Submit
  </button>
</div>
```

### 2. Typography（タイポグラフィ）

**主要チェックポイント**:

- フォントスムージングの適用
- フォントウェイトの適切な使用（400 以上）
- タブラー数字の使用（テーブル、タイマーなど）
- レスポンシブなフォントサイズ（`clamp()` の使用）
- iOS での予期しないテキストリサイズ防止

**検証項目**:

```css
/* ✅ 推奨スタイル */
body {
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  -webkit-text-size-adjust: 100%;
}

h1 {
  font-size: clamp(48px, 5vw, 72px);
  font-weight: 500; /* 400 以上 */
}

.timer {
  font-variant-numeric: tabular-nums;
}

/* ❌ 問題のあるスタイル */
p {
  font-weight: 300; /* 400 未満 */
}
```

### 3. Motion（モーション・アニメーション）

**主要チェックポイント**:

- アニメーション時間は 200ms 以内
- テーマ切り替え時のトランジション防止
- 頻繁な操作には過度なアニメーションを避ける
- スケールアニメーションの適切な値
- 画面外での無限ループアニメーション停止

**検証項目**:

```typescript
// ✅ 適切なアニメーション
const Dialog = styled.div`
  animation: fadeIn 150ms ease-out;

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95); /* 0 からではなく 0.95 から */
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
`;

// ❌ 過度なアニメーション
const Button = styled.button`
  transition: all 500ms; /* 長すぎる */

  &:active {
    transform: scale(0.5); /* 変化が大きすぎる */
  }
`;
```

### 4. Touch（タッチデバイス対応）

**⚠️ プロジェクト固有**: `:hover` は PostCSS プラグイン (`postcss-media-hover-any-hover`) が自動的に `@media (any-hover: hover)` でラップします。手動でメディアクエリを追加しないでください。

**主要チェックポイント**:

- インプットのフォントサイズ 16px 以上（iOS ズーム防止）
- タッチデバイスでの自動フォーカス無効化
- ビデオの自動再生設定（`muted`, `playsinline`）
- iOS タップハイライトの適切な置き換え

**検証項目**:

```css
/* ✅ 正しい実装 */
button {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

button:hover {
  background-color: #eee; /* PostCSS が自動ラップ */
}

input {
  font-size: 16px; /* iOS ズーム防止 */
}

/* ❌ 間違った実装 */
@media (any-hover: hover) {
  /* 冗長 */
  button:hover {
    background-color: #eee;
  }
}

input {
  font-size: 14px; /* iOS でズーム発生 */
}
```

### 5. Optimizations（パフォーマンス最適化）

**主要チェックポイント**:

- 大きな `blur()` 値の回避
- GPU レンダリングの適切な使用 (`transform: translateZ(0)`)
- `will-change` の慎重な使用
- 画面外ビデオの停止または削除
- React レンダリングのバイパス（必要時のみ）

**検証項目**:

```typescript
// ✅ 最適化された実装
const BlurredBox = styled.div`
  backdrop-filter: blur(8px); /* 適度な値 */
`;

// スクロールアニメーション時のみ will-change を適用
const handleScroll = () => {
  element.style.willChange = 'transform';
  // アニメーション処理
  requestAnimationFrame(() => {
    element.style.willChange = 'auto'; // 終了後に削除
  });
};

// ❌ パフォーマンス問題
const HeavyBlur = styled.div`
  backdrop-filter: blur(50px); /* 重すぎる */
  will-change: transform, opacity; /* 常時適用は避ける */
`;
```

### 6. Accessibility（アクセシビリティ）

**主要チェックポイント**:

- 無効化ボタンへのツールチップ禁止
- フォーカスリングに `box-shadow` を使用
- アイコンのみの要素に `aria-label` 追加
- 画像は `<img>` タグで実装
- キーボードナビゲーション対応（↑↓ キー）

**検証項目**:

```typescript
// ✅ アクセシブルな実装
<button aria-label="閉じる">
  <CloseIcon />
</button>

<img src="photo.jpg" alt="製品写真" />

const FocusRing = styled.button`
  &:focus-visible {
    box-shadow: 0 0 0 3px rgba(0, 0, 255, 0.5);
    outline: none;
  }
`;

// ❌ アクセシビリティ問題
<button disabled title="保存できません"> {/* disabled + tooltip */}
  保存
</button>

<button> {/* aria-label なし */}
  <Icon />
</button>

<div style={{backgroundImage: 'url(photo.jpg)'}} /> {/* img タグなし */}
```

### 7. Design & UX（デザイン・UX・心理効果）

#### 実装面のチェックポイント

**UI パターンと実装**:

- 楽観的 UI 更新とロールバック
- サーバー側での認証リダイレクト
- `::selection` のスタイリング
- フィードバックのトリガー相対配置
- 空状態の適切な処理

**検証項目**:

```typescript
// ✅ 楽観的 UI 更新
const handleDelete = async (id) => {
  // 即座に UI を更新
  setItems(items.filter((item) => item.id !== id));

  try {
    await api.delete(id);
  } catch (error) {
    // エラー時にロールバック
    setItems(originalItems);
    showError('削除に失敗しました');
  }
};

// ✅ フィードバックの相対配置
<button onClick={handleCopy}>
  コピー
  {copied && <CheckIcon />} {/* ボタン内に表示 */}
</button>;

// ❌ 不適切なフィードバック
const handleCopy = () => {
  copy(text);
  showNotification('コピーしました'); /* 通知は不要 */
};
```

#### UX 心理効果のチェックポイント

**主要な心理効果**:

- 美的ユーザビリティ効果（視覚的洗練さ）
- 認知負荷の軽減（情報量、レイアウト、タイポグラフィ）
- 視覚的階層（見出し、本文、コードの優先度）
- ドハティの閾値（応答 400ms 以内）
- バナー・ブラインドネス回避（広告風デザインを避ける）
- 段階的開示（アコーディオン、タブの活用）
- 系列位置効果（重要項目の配置）
- ピーク・エンドの法則（ハイライトと締めくくり）

**技術ブログで特に重視すべき点**:

- コンテンツの質と明確性を最優先
- 技術記事ではコードブロック、シンタックスハイライト、適切な空白に注意
- タイトルの明確性（クリックベイト回避）
- 各記事の完結性を重視
- 過度な CTA や購読促進は控えめに

**検証項目**:

```typescript
// ✅ 認知負荷の軽減と視覚的階層
const Article = () => (
  <article>
    <h1>明確なタイトル</h1> {/* 好奇心ギャップ回避 */}

    {/* 視覚的階層: 見出し → 本文 → コード */}
    <section>
      <h2>セクション見出し</h2>
      <p>説明文...</p>
      <CodeBlock language="typescript">
        {/* シンタックスハイライト適用 */}
      </CodeBlock>
    </section>

    {/* 段階的開示 */}
    <Accordion>
      <AccordionItem title="詳細な説明">
        複雑な内容は折りたたみ
      </AccordionItem>
    </Accordion>
  </article>
);

// ✅ ドハティの閾値（400ms 以内）
const handleAction = async () => {
  // 即座に UI フィードバック
  setLoading(true);

  // バックグラウンド処理
  await processData();

  setLoading(false);
};

// ✅ バナー・ブラインドネス回避
const ImportantNotice = styled.div`
  /* 広告風デザインを避ける */
  background: transparent; /* 派手な背景色を避ける */
  border: 1px solid var(--border);
  padding: 16px;
`;

// ❌ 問題のある実装
const ClickbaitTitle = () => (
  <h1>この方法を知らないと損します！</h1> {/* 好奇心ギャップ */}
);

const OverwhelmingContent = () => (
  <div>
    {/* 認知負荷が高すぎる */}
    <p>段落1段落1段落1...</p>
    <p>段落2段落2段落2...</p>
    {/* 適切な空白・階層なし */}
  </div>
);

const SlowResponse = async () => {
  await heavyOperation(); // 400ms 超過
  updateUI(); // 遅すぎるフィードバック
};
```

**チェックリスト**:

- [ ] 楽観的 UI 更新を実装（実装面）
- [ ] フィードバックが適切な位置に表示（実装面）
- [ ] 空状態が適切に処理される（実装面）
- [ ] ページ応答時間が 400ms 以内（心理効果）
- [ ] 視覚的階層が明確（見出し、本文、コードの区別）（心理効果）
- [ ] 適切な空白とレイアウト（認知負荷軽減）（心理効果）
- [ ] コードブロックにシンタックスハイライト適用（心理効果）
- [ ] 重要情報が広告風デザインになっていない（心理効果）
- [ ] ナビゲーション項目が 7±2 個以内（心理効果）
- [ ] タイトルが明確で具体的（心理効果）
- [ ] 過度な購読促進・ポップアップなし（心理効果）
- [ ] 美的に洗練されたデザイン（心理効果）
- [ ] 複雑な情報は段階的に開示（心理効果）

## レビュー手順

### Step 1: ファイルの特定

対象ファイルを特定します：

- UI コンポーネント（`src/components/UI/`）
- Page コンポーネント（`src/components/Page/`）
- スタイル定義（`src/ui/`）

### Step 2: 領域別チェック

各領域のチェックポイントに従って検証：

1. **Interactivity**: フォーム、ボタン、インタラクティブ要素
2. **Typography**: CSS のフォント設定、font-weight
3. **Motion**: アニメーション、トランジション
4. **Touch**: メディアクエリ、フォントサイズ、タップ処理
5. **Optimizations**: blur, will-change、GPU 処理
6. **Accessibility**: aria-label、フォーカス、キーボード対応
7. **Design & UX**: UI パターン、フィードバック、心理効果、認知負荷、視覚的階層

### Step 3: 優先度の判定

検出された問題を優先度別に分類：

| 優先度 | 問題の種類                               |
| ------ | ---------------------------------------- |
| 高     | アクセシビリティ違反、重大なUX問題       |
| 中     | パフォーマンス問題、タッチデバイス非対応 |
| 低     | 最適化の余地、細かいUX改善               |

### Step 4: レビュー結果の生成

検出された問題と改善提案を報告します。

## 出力形式

````markdown
## インターフェースレビュー結果

### 📊 レビューサマリー

- ファイル: `src/components/UI/Button/Button.tsx`
- チェック領域: 7
- 合格: 5
- 改善推奨: 1
- 問題検出: 1

### ✅ 適切に実装されている項目

- [✓] Interactivity: フォーム送信、ボタン無効化
- [✓] Typography: フォントスムージング適用
- [✓] Accessibility: aria-label 設定

### ⚠️ 改善推奨

- [例] **Performance**: 画像最適化が必要
  **影響**: ページロード時間が長くなる
  **提案**: Next.js Image コンポーネントを使用

> **Note**: このプロジェクトでは `:hover` のメディアクエリは PostCSS プラグインが自動処理するため、手動での追加を推奨しません

### ❌ 問題検出

- [Button.tsx:45] **Motion**: アニメーション時間が長すぎる (500ms)
  **影響**: インタラクションが遅く感じられる
  **修正**:
  ```diff
  - transition: all 500ms;
  + transition: all 150ms ease-out;
  ```
````

### 📝 総合評価

- **評価**: ⚠️ 改善推奨
- **優先修正**: Motion のアニメーション時間短縮
- **推奨改善**: Touch デバイス対応の強化

```

## 使用例

### 例 1: UI コンポーネントのレビュー

```

User: Button コンポーネントのインターフェースをレビューして
Assistant: [スキルを起動して 7 つの領域から検証]

```

### 例 2: ページ全体のレビュー

```

User: HomePage のアクセシビリティとタッチ対応をチェック
Assistant: [Accessibility と Touch の領域を重点的に検証]

```

### 例 3: 特定領域のレビュー

```

User: このアニメーションがベストプラクティスに従っているか確認
Assistant: [Motion 領域を重点的に検証]

```

### 例 4: Design & UX のレビュー

```

User: この記事ページの認知負荷と視覚的階層をチェック
Assistant: [Design & UX 領域（UX 心理効果）を重点的に検証]

```

## 参照ドキュメント

詳細なガイドラインは以下を参照してください：

- `references/web-interface-guidelines.md` - Web インターフェースのベストプラクティス（raunofreiberg/interfaces より）
- `references/ux-psychology.md` - UX 心理効果と認知負荷のガイドライン（技術ブログ向け）

## 注意事項

- このスキルは **read-only** です（allowed-tools: Read, Grep, Glob）
- コードの自動修正は行いません
- レビュー結果に基づき、ユーザーが手動で修正します
- WAI-ARIA 仕様の詳細は含まれていませんが、基本的なアクセシビリティはカバーされています

## ベストプラクティスの出典

このスキルは以下のガイドラインに基づいています：
- [raunofreiberg/interfaces](https://github.com/raunofreiberg/interfaces) - Web インターフェース実装
- プロジェクト独自の UX 心理効果ガイドライン - 技術ブログにおける心理効果
```
