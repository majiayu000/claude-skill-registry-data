---
name: generate-props-documentation
description: 全コンポーネントのProps定義（型、デフォルト値、説明）を自動的に解析し、統一されたマークダウンドキュメントを生成します。
allowed-tools: "Read, Write, Glob, Grep"
---

# Props一覧ドキュメント自動生成

このスキルは、全コンポーネントのProps定義を解析し、統一されたドキュメントを自動生成します。

## 実行手順

1. **コンポーネントの収集**
   - `src/components/ui/`内の全`.astro`ファイルを取得
   - 各ファイルを読み込み

2. **Props情報の抽出**
   各コンポーネントから以下の情報を抽出：
   - プロパティ名
   - 型（TypeScript型定義）
   - デフォルト値
   - JSDocコメント（説明）
   - 必須/オプションの区別

3. **ドキュメント生成**
   - マークダウン形式でドキュメントを生成
   - コンポーネントごとにセクションを作成
   - Props一覧表を作成

4. **出力フォーマット**

```markdown
# Astro Components Props リファレンス

このドキュメントは自動生成されています。

## Button

Windows Forms風のボタンコンポーネント

### Props

| プロパティ | 型 | デフォルト値 | 必須 | 説明 |
|-----------|-----|-------------|------|------|
| label | string | 'Button' | いいえ | ボタンのテキスト |
| variant | 'default' \| 'primary' \| 'flat' | 'default' | いいえ | ボタンの種類 |
| size | 'small' \| 'medium' \| 'large' | 'medium' | いいえ | ボタンのサイズ |
| disabled | boolean | false | いいえ | 無効化 |
| type | 'button' \| 'submit' \| 'reset' | 'button' | いいえ | HTMLボタンのtype属性 |
| fullWidth | boolean | false | いいえ | ボタンの幅を100%にする |

### 使用例

\`\`\`astro
<Button variant="primary" size="large">送信</Button>
\`\`\`

---

## TextBox

... (他のコンポーネントも同様)
```

5. **ファイル出力**
   - ユーザーに保存場所を確認
   - デフォルト: `docs/PROPS_REFERENCE.md`
   - 既存ファイルがある場合は上書き確認

6. **統計情報の表示**
   - 処理したコンポーネント数
   - 抽出したProps総数
   - Props型の種類（string, boolean, number等の使用頻度）

## 実装ガイドライン

### Propsの抽出方法

1. **インターフェース定義の検出**
   ```typescript
   interface Props {
     label?: string;  // オプショナル（?付き）
     required: boolean;  // 必須
   }
   ```

2. **デフォルト値の検出**
   ```typescript
   const { label = 'Default', required } = Astro.props;
   ```

3. **JSDocコメントの抽出**
   ```typescript
   /** ボタンのテキスト */
   label?: string;
   ```

### エラーハンドリング

- Props定義が見つからない場合は「Props定義なし」と記載
- 型情報が不完全な場合は「any」と表示し警告
- JSDocコメントがない場合は「説明なし」と記載

## 追加機能（オプション）

- **検索機能**: 特定のProp名や型でフィルタリング
- **JSON出力**: JSON形式でも出力可能にする
- **バリデーション**: 不正な型定義やデフォルト値の不整合を検出

## 注意事項

- TypeScriptの型定義を正確に解析すること
- Union型（`'a' | 'b'`）は見やすく整形
- 複雑なオブジェクト型は簡潔に表現
- 生成後は手動での微調整を推奨
