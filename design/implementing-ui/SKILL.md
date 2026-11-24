---
name: implementing-ui
description: |-
  UI実装の包括的ガイドライン。管理画面パターン、React Hook Formフォーム実装、レスポンシブデザインを提供。「UI」「コンポーネント」「管理画面」「一覧画面」「テーブル表示」「フォーム」「React Hook Form」「バリデーション」「useForm」「レスポンシブ」「モバイル対応」「ブレークポイント」「Tailwind」に関する作業で使用。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# UI実装スキル

対象プロジェクトにおけるUI実装の包括的ガイド。

## 重要: 仕様書の参照

⚠️ **UI実装を開始する前に、必ず以下の仕様書を確認すること**:

1. **REQUIREMENTS.md** - 画面の目的・ユースケースを理解
2. **TECH_DESIGN.md** - 技術設計・型定義、および「画面項目定義」セクション（画面 feature は必須・非画面 feature は省略）の項目詳細・バリデーションルール・表示形式

TECH_DESIGN.md の画面項目定義セクションがある場合:
- フォーム項目名・データ型は定義に従うこと
- バリデーションルールは定義通りに実装すること
- 表示形式（日付フォーマット、通貨など）は定義に従うこと
- 選択肢の値・表示テキストは定義通りに実装すること

## Quick Navigation

| セクション | トリガーキーワード |
|-----------|------------------|
| [管理画面パターン](#管理画面パターン) | 管理画面、一覧画面、テーブル表示 |
| [React Hook Formガイドライン](#react-hook-form-ガイドライン) | フォーム、React Hook Form、バリデーション、useForm |
| [レスポンシブデザイン](#レスポンシブデザインガイドライン) | レスポンシブ、モバイル対応、ブレークポイント、Tailwind |

---

## 管理画面パターン

管理画面アプリ（`.stdd.config.yml` の該当する `apps[]`）の一覧管理画面は、以下の統一されたUIパターンを採用すること。

### 画面構成

```
┌─────────────────────────────────────────────────────────┐
│ 画面タイトル                       [bg-[#1e3a5f] 濃い青] │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 検索条件                               [bg-blue-600 青] │
├─────────────────────────────────────────────────────────┤
│  フィールド1 [________]   フィールド2 [________]        │
│  フィールド3 [▼_______]   フィールド4 [▼_______]        │
│                                    [検索] [リセット]   │
└─────────────────────────────────────────────────────────┘

該当件数: XX件                   [新規登録] [編集] [削除]

┌─────────────────────────────────────────────────────────┐
│ ☐ │カラム1│カラム2│...│              [bg-blue-600 青]  │
├───┼───────┼───────┼───┼──────────────────────────────┤
│ ☐ │       │       │   │                 [白背景]     │
└─────────────────────────────────────────────────────────┘

        [前へ] [1] [2] [3] [次へ]
```

### 実装パターン

```tsx
<div className="space-y-4 w-full">
  {/* ページヘッダー */}
  <div className="bg-[#1e3a5f] text-white px-6 py-4 rounded-t-lg -mx-4 -mt-4 md:-mx-6 md:-mt-6">
    <h1 className="text-xl font-bold">画面タイトル</h1>
  </div>

  {/* 検索条件セクション */}
  <div className="border border-gray-300 rounded-lg overflow-hidden">
    <div className="bg-blue-600 text-white px-4 py-2">
      <span className="font-medium">検索条件</span>
    </div>
    <div className="p-4 bg-white">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        {/* 検索フィールド */}
      </div>
      <div className="flex justify-end gap-2">
        <Button className="bg-blue-600 hover:bg-blue-700">検索</Button>
        <Button variant="outline">リセット</Button>
      </div>
    </div>
  </div>

  {/* 結果セクション */}
  <div className="flex justify-between items-center">
    <div>該当件数: {count}件</div>
    <div className="flex gap-2">{/* アクションボタン */}</div>
  </div>

  {/* テーブル */}
  <div className="border rounded-lg overflow-hidden">
    <table className="w-full min-w-[1000px]">
      <thead className="bg-blue-600 text-white">{/* ヘッダー行 */}</thead>
      <tbody className="bg-white divide-y divide-gray-200">{/* データ行 */}</tbody>
    </table>
  </div>

  {/* ページネーション */}
</div>
```

### 行選択機能

- チェックボックスで行を選択（単一/複数）
- ヘッダーのチェックボックスで全選択/解除
- 選択状態に応じてボタンの有効/無効を制御
  - 編集ボタン: 1件選択時のみ有効
  - 削除ボタン: 1件以上選択時に有効

### 参考実装

管理画面アプリ（`.stdd.config.yml` の該当する `apps[].path`）内の既存の一覧管理画面コンポーネントを参考にすること。例: `<apps[].path>/app/dashboard/<feature>/<Feature>Client.tsx`

---

## React Hook Form ガイドライン

### 基本原則

- React Hook Form と Zod バリデーションを使用
- フォームコンポーネントは`Form`、`FormField`、`FormItem`などの shadcn/ui コンポーネントを使用
- バリデーションエラーメッセージは日本語で表示
- 必須フィールドには`*`マークを付ける

### 型管理

**重要**: API の型とフォームの型は明確に分けること。

1. **API の型とフォームの型を分ける**
   - API 用の Entity 型（例: `UserWorkPreferencesEntity`）とフォーム用の型（例: `UserWorkPreferencesFormData`）を別々に定義
   - フォームでは string 型で扱うが、API では number 型や boolean 型で扱うフィールドを明確に区別

2. **defaultValues の設定時にキャストして渡す**
   ```typescript
   const form = useForm<UserWorkPreferencesFormData>({
     resolver: zodResolver(userWorkPreferencesSchema),
     defaultValues: {
       // API Entity (number) → フォーム (string) に変換
       desired_workload_min: workPreferences?.desired_workload_min?.toString() || '',
       // API Entity (boolean) → フォーム (string) に変換
       business_trip_available: workPreferences?.business_trip_available ? 'true' : 'false',
     },
   });
   ```

3. **API リクエスト時にフォーム値を再度キャストする**
   ```typescript
   const onSubmit = async (data: UserWorkPreferencesFormData) => {
     await saveAction({
       // フォーム (string) → API Entity (number) に変換
       desired_workload_min: data.desired_workload_min ? parseInt(data.desired_workload_min, 10) : null,
       // フォーム (string) → API Entity (boolean) に変換
       business_trip_available: data.business_trip_available === 'true',
     });
   };
   ```

### フォーム初期化とuseEffectの使用制限

**重要原則**: useEffectをむやみやたらに使用しないこと。

❌ **悪い例**: useEffectでform.reset()を呼ぶ
```typescript
const form = useForm<FormType>({
  resolver: zodResolver(schema),
  defaultValues: { title: '', company: '' },
});

useEffect(() => {
  if (isEditing && editingItem) {
    form.reset({
      title: editingItem.title || '',
      company: editingItem.company || '',
    });
  }
}, [isEditing, editingItem]);
```

✅ **良い例**: useMemoでdefaultValuesを動的に生成
```typescript
const defaultValues = useMemo(() => {
  if (isEditing && editingItem) {
    return {
      title: editingItem.title || '',
      company: editingItem.company || '',
      start_date: convertDateForMonthInput(editingItem.start_date) || '',
      end_date: convertDateForMonthInput(editingItem.end_date) || '',
    };
  }
  return { title: '', company: '', start_date: '', end_date: '' };
}, [isEditing, editingItem]);

const form = useForm<FormType>({
  resolver: zodResolver(schema),
  defaultValues,
});

useEffect(() => {
  form.reset(defaultValues);
}, [defaultValues]);
```

### undefined項目の扱い

- フォームのdefaultValuesでは、undefined項目にはnullか空文字('')を設定すること
- string型のフィールドは空文字('')を使用
- number型やboolean型のフィールドは適切なデフォルト値（0、false等）を使用
- オプショナルな参照型（配列、オブジェクト）はnullまたは空配列[]を使用

### useEffectが許容される場合

- データフェッチ（APIコール）
- DOM操作が必要な場合
- サブスクリプション（WebSocket、イベントリスナー等）
- defaultValuesの変更に応じたフォームリセット
- 外部ライブラリとの連携

### useEffectを避けるべき場合

- 状態の派生計算（useMemoやuseCallbackを使用）
- フォームの初期値設定（defaultValuesを使用）
- イベントハンドラ内で完結する処理
- 不要なモーダル開閉状態（isOpen）の監視

### コード修正後のデッドコードチェック

**重要原則**: コードを修正した後は、不要になった関数・変数定義・import文がないか必ず確認すること。

**削除対象**:
- 使用されていない関数定義、変数定義
- 使用されていないimport文、型定義
- コメントアウトされた古いコード

**確認方法**:
- IDEの未使用コード警告を確認
- `commands.typecheck`（`.stdd.config.yml`）を実行し、型エラーとともに未使用の警告を確認

---

## レスポンシブデザインガイドライン

### 基本方針

- **モバイルファーストアプローチ**: 基本スタイルはモバイル向けに設計し、大きい画面向けにブレークポイントで拡張する
- **すべての新規コンポーネント・ページはレスポンシブ対応を必須とする**
- Tailwind CSS のブレークポイントプレフィックスを使用してレスポンシブスタイルを適用

### ブレークポイント定義

| プレフィックス | 最小幅 | 対象ビュー |
|--------------|--------|-----------|
| (なし) | 0px | モバイル（320px〜767px） |
| `md:` | 768px | タブレット |
| `lg:` | 1024px | デスクトップ |

> **禁止プレフィックス**: `sm:`, `xl:`, `2xl:` は使用しないこと（3ビュー統一方針）

### グリッドレイアウト

```tsx
// 1列 → 2列 → 3列（推奨パターン）
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map((item) => <Card key={item.id} />)}
</div>

// 1列 → 2列 → 4列
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* ... */}
</div>
```

### Flexbox レイアウト

```tsx
// モバイル: 縦並び → タブレット以上: 横並び
<div className="flex flex-col md:flex-row gap-4 md:gap-8">
  {/* ... */}
</div>
```

### コンテナ幅とパディング

```tsx
<div className="mx-auto max-w-7xl px-4 md:px-6 lg:px-8">
  {content}
</div>
```

### 表示/非表示の切り替え

```tsx
// デスクトップナビゲーション（モバイルで非表示）
<nav className="hidden lg:flex">
  <DesktopNavigation />
</nav>

// モバイルメニューボタン（デスクトップで非表示）
<button className="lg:hidden">
  <MenuIcon />
</button>
```

### テキストサイズ

```tsx
// 見出しのレスポンシブサイズ
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">タイトル</h1>

// 本文のレスポンシブサイズ
<p className="text-sm md:text-base lg:text-lg">説明文</p>
```

### フォームのレスポンシブ対応

```tsx
// フォームフィールドの並び
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <FormField name="lastName" label="姓" />
  <FormField name="firstName" label="名" />
</div>

// ボタンの配置
<div className="flex flex-col md:flex-row justify-end gap-4">
  <Button variant="outline" className="w-full md:w-auto">キャンセル</Button>
  <Button type="submit" className="w-full md:w-auto">保存</Button>
</div>
```

### テーブルのレスポンシブ対応

```tsx
// 横スクロール対応
<div className="overflow-x-auto">
  <Table className="min-w-[600px]">
    {/* テーブル内容 */}
  </Table>
</div>

// モバイルではカード表示に切り替え（複雑なテーブルの場合）
<div className="hidden md:block">
  <Table>{/* テーブル表示 */}</Table>
</div>
<div className="md:hidden space-y-4">
  {items.map((item) => <MobileCard key={item.id} />)}
</div>
```

### ダイアログ実装パターン

#### レスポンシブ対応

```tsx
<DialogContent className="w-[95vw] max-w-md md:max-w-lg">
  {/* モバイルでは95%幅、大きい画面では最大幅を制限 */}
</DialogContent>
```

#### backdrop close（枠外クリック）

**一律閉じる**。`closeOnClickOverlay={false}`は使用しない。

入力ありダイアログでは以下のルールで入力状態を保持する:

- **閉じた時にreset()しない**: useStateやReact Hook Formの状態はアンマウントされない限り維持されるため、何もしなければ状態保持される
- **送信成功時のみリセット**: reset()は送信成功後に呼ぶ
- **対象変更時にリセット**: 同じダイアログを別の対象（別のユーザー、別のプロジェクト等）で開く場合、useEffectで対象IDの変更を検知してリセットする

```tsx
// ✅ 閉じた時にリセットしない（状態保持）
const [reason, setReason] = useState('');

const handleSubmit = async () => {
  await onRegister(reason);
  setReason(''); // 送信成功時のみリセット
};

// ✅ 対象変更時にリセット
useEffect(() => {
  setReason('');
}, [targetId]); // 対象が変わったらリセット
```

#### props展開とハンドラの順序

共通UIコンポーネント（`dialog.tsx`等）でハンドラを定義する場合、`{...props}`を**先に展開**し、ハンドラを**後に定義**すること。逆にするとpropsで渡されたハンドラに上書きされる。

```tsx
// ❌ 悪い例: propsで上書きされる
onInteractOutside={(e) => { /* 内部ロジック */ }}
{...props}

// ✅ 良い例: 内部ロジックが常に有効 + 呼び出し側のハンドラも実行
{...props}
onInteractOutside={(e) => {
  // 内部ロジック
  props.onInteractOutside?.(e);
}}
```

### レスポンシブ実装チェックリスト

```
□ モバイル（320px）で正しく表示されるか
□ タブレット（768px）でレイアウトが適切に変化するか
□ デスクトップ（1024px以上）で余白やコンテンツ幅が適切か
□ タッチ操作に適したボタン・リンクサイズか（最小44px推奨）
□ 横スクロールが発生していないか（意図した場合を除く）
□ フォントサイズが各画面サイズで読みやすいか
```

---

## UI実装チェックリスト

### 実装開始前

```
□ REQUIREMENTS.md で画面の目的・ユースケースを確認
□ TECH_DESIGN.md の画面項目定義セクションを確認（画面 feature は必須・非画面 feature は省略）
□ TECH_DESIGN.md で型定義・API設計を確認
```

### TECH_DESIGN.md に画面項目定義がある場合

```
□ フォーム項目名（項目ID）が定義と一致しているか
□ データ型（string, number, date, select等）が定義と一致しているか
□ 必須項目が定義通りに設定されているか
□ バリデーションルール（形式、桁数、範囲）が定義通りか
□ エラーメッセージが定義通りか
□ 選択肢の値・表示テキストが定義通りか
□ 表示形式（日付、数値、テキスト）が定義通りか
□ 相関チェックが定義通りに実装されているか
```

---

## When NOT to Use This Skill

以下の場合はこのスキルを使用しない:

- **ロジックのみの変更**: UIに影響しないビジネスロジックの修正
- **バックエンドの変更**: Server Actions、API、データベースのみの変更
- **テストの追加**: UIに影響しないテストの追加
