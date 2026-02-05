---
name: lesson-generator
description: カリキュラムからレッスン番号を指定してJavaScript学習教材のmdファイルを生成する。ユーザーが「レッスンXXの教材を作成して」と依頼したときに使用する。
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# JavaScript学習教材生成スキル

## 概要

curriculum.mdからレッスン情報を抽出し、詳細な解説付きの学習教材を生成する。

## 重要な原則：カリキュラム追従

**そのレッスンまでに学んだ概念だけを使用すること。**

- まだ習っていない概念（関数、配列、ループ等）は絶対に使わない
- □ステップに書かれているコードだけを使用する
- 【知識】に書かれている概念だけを説明する
- 練習問題もそのレッスンで学んだことだけで解ける内容にする

### レッスン進度の目安

- レッスン1-6: console.log、alert、基本的なブラウザ操作のみ
- レッスン7-11: 変数（let/const）の導入
- レッスン12: 復習
- レッスン13-24: DOM操作（getElementById、textContent、style）
- レッスン20以降: 関数の基礎が登場

**関数やVitestテストは、関数を学ぶレッスン以降でのみ使用する。**

## 文章スタイルのガイドライン

### 基本方針

- **十分な文章量**：あっさりしすぎず、丁寧に説明する（1レッスン300-400行程度）
- **論理的なつながり**：セクション間の流れを明確にする
- **初学者への配慮**：不安への共感、励ましの言葉を含める
- **具体例を豊富に**：身近なサービス（YouTube、Amazon、Twitter等）を例示

### 文章量の目安

各セクションで以下の内容を含めて、十分な説明を行う。

**概念説明セクション**
- 概念の定義と重要性
- なぜその概念が必要なのかの背景
- 身近な例え（料理のレシピ、日常生活など）
- コード例は複数パターン用意
- 各コードの動作を詳しく解説
- よくある間違いや注意点

**練習問題セクション**
- 課題の説明
- 詳細な手順
- ヒントは複数の観点から
- 解答例に加えて追加チャレンジを用意

**まとめセクション**
- 労いの言葉
- 各キーポイントの詳細な説明
- 次のレッスンへの具体的な導入

### 表記ルール

- 「ウェブ」ではなく「Web」と表記
- 「今日」ではなく「今回」と表記
- 「ゴール」ではなく「目標」と表記
- ですます調を厳守
- 「〜ですよね」「〜ますよね」という表現は使用しない（「〜です」「〜ます」で終える）
- 感嘆符（！）は使用しない
- 行末に「：」を置かない（単語の説明で使用するのはOK）

## 実行手順

### 1. レッスン情報の抽出

curriculum.mdを読み込み、指定されたレッスン番号の以下の情報を抽出する：

- レッスン番号とタイトル（時間）
- □ チェックボックス形式のステップ（すべて）
- 【知識】習得する知識項目
- ✅ 成果物

また、前のレッスン（レッスン番号-1）の情報も抽出して「前回の復習」に使用する。

### 1.5. 既習概念の確認

指定されたレッスン番号より前のレッスンを確認し、どの概念が既に学習済みかを把握する。
練習問題では、既習の概念のみを使用する。

### 2. 教材の生成

以下の構成で教材を生成する。

#### レッスン1（最初のレッスン）の場合の構成:

```
## はじめに
- 歓迎メッセージ（不安への共感、励まし）
- このカリキュラムで作れるようになるもの（具体的なアプリ例）
- 学習のコツ（毎日少しずつ、手を動かす、間違いを恐れない）

## 今回の学習
- なぜJavaScriptを学ぶのか（身近なサービスの具体例：YouTube、Amazon、Twitter）
- 今回の目標

## [概念の説明]
- 詳細な説明（身近な例え）

## [実践セクション]
- 手順の詳細な説明
- コードの意味の解説

## 練習問題

## まとめ
```

#### レッスン2以降の構成:

```
## 今回の学習
- 前回の復習
- 今回の目標

## [概念の説明]

## [実践セクション]

## 練習問題

## まとめ
```

#### 生成時の注意点

**YAMLフロントマター:**
- title: "Lesson XXX: [レッスンタイトル]"（XXXは3桁ゼロ埋め）
- author: "JavaScript学習教材"
- date: 生成日（YYYY-MM-DD形式）

**今回の学習セクション:**
- 前回の復習: 前のレッスンの【知識】と✅成果物を参照（レッスン1では不要）
- 今回の目標: □ステップから3つ選んで目標形式に変換
- ※「なぜこれを学ぶか」セクションは不要（レッスン1の「なぜJavaScriptを学ぶのか」は例外）

**概念説明セクション:**
- 【知識】の各項目について詳細に説明
- 日常生活での具体例を含める（十分な文章量で）
- □ステップのコードをサンプルコードとして使用
- 各コード行にコメントで説明を追加
- 実行結果も記載
- コードの各部分の意味を丁寧に解説

**練習問題セクション（すべてのレッスンで共通形式）:**

### 全レッスン共通の構成:
- 課題: ✅成果物を課題として設定
- **保存場所**: 練習問題でファイルを使用する場合は、以下の形式で記載
  - **レッスン12以前の場合:**
    - 「`exercises/lesson-XXX/index.html` を使用してください。このファイルは既に用意されています。各課題のコードを `<script>` タグの中に入力し、ブラウザで開いて動作を確認しましょう。」
  - **レッスン13以降（DOM操作）の場合:**
    - 「`exercises/lesson-XXX/` フォルダに以下のファイルが用意されています。」
    - 「- `index.html` - HTML要素を追加するファイル」
    - 「- `script.js` - JavaScriptコードを書くファイル」
    - 「HTML要素は `index.html` のコメント部分に追加し、JavaScriptコードは `script.js` に記述してください。ブラウザで `index.html` を開いて動作を確認しましょう。」
  - レッスン番号は3桁ゼロ埋め（例：lesson-004, lesson-013）
- 手順: □ステップをそのまま番号付きリストで記載
- **テスト確認（レッスン4以降）**: 以下の形式で記載
  - 「### テストで確認する」
  - 「以下のコマンドを実行すると、課題が正しく実装できているか確認できます。」
  - 「```bash」
  - 「npm test exercises/lesson-XXX」
  - 「```」
  - 「すべてのテストがパス（✓マーク）すれば完成です。」
- ヒント: 初心者がつまずきやすいポイントを詳細に記載
- 解答例: □ステップのコードを組み合わせた完成形
- 解説: 各部分の役割を詳しく説明

**テストケース作成のガイドライン（レッスン4以降すべて）:**
- Vitestテストファイルを `exercises/lesson-XXX/index.test.js` に作成
- describe/it/expectを使用
- テストの目的:
  - **学習者は自分でテストを書かない**
  - 講師が用意したテストを実行して、正解・不正解を確認する
  - 学習者の実装が要件を満たしているかを即座にフィードバック
- テストケースの構成:
  - **基礎レッスン（レッスン1-12）**: 変数の値を確認
    - 特定の変数名が定義されているか
    - 変数の値が期待値と一致するか
    - console.logが呼ばれているか（必要に応じて）
  - **DOM操作レッスン（レッスン13以降）**: DOM要素を確認
    - getElementById等で取得した要素が存在するか
    - textContent、style等のプロパティが正しく設定されているか
    - 要素の構造が正しいか
  - **関数レッスン（レッスン20以降）**: 関数の動作を確認
    - 関数が正しい値を返すか
    - 関数が正しく動作するか（正常系・境界値・エラーケース）
- テストの説明は日本語で分かりやすく
- 期待値は具体的な値を使用
- **そのレッスンまでに学んだ概念のみ使用（配列を学ぶ前は配列を使わない等）**
- 最低3つのテストケースを含める

**まとめセクション:**
- 労いの言葉（「お疲れ様でした！」等）
- 【知識】の各項目をキーポイントとして要約
- 各キーポイントに十分な説明を付ける
- 次のレッスンへの導入

### 3. ファイルの保存

レッスンの進度に応じて生成するファイルが異なる。

#### レッスン1-3（練習問題なし）

```
materials/
└── lesson-XXX.md              # 教材本体のみ
```

**生成ファイル:**
- `materials/lesson-XXX.md` - 教材本体

#### レッスン4-12（変数・基礎文法を学ぶ）

```
materials/
└── lesson-XXX.md              # 教材本体

exercises/
└── lesson-XXX/
    ├── index.html             # HTMLテンプレート
    └── index.test.js          # テストファイル（講師側が用意）

solutions/
└── lesson-XXX/
    └── index.html             # 解答ファイル
```

**生成ファイル:**
- `materials/lesson-XXX.md` - 教材本体
- `exercises/lesson-XXX/index.html` - HTMLテンプレート（学習者が編集）
- `exercises/lesson-XXX/index.test.js` - Vitestテスト（講師が用意）
- `solutions/lesson-XXX/index.html` - 解答コード

**index.htmlの内容:**
```html
<script>
// ここにコードを書いてください

</script>
```

**index.test.jsの内容例（変数を確認する形式）:**
```javascript
import { describe, it, expect, beforeEach } from 'vitest';
import { JSDOM } from 'jsdom';
import fs from 'fs';
import path from 'path';

describe('Lesson XXX: [レッスンタイトル]', () => {
  let dom;
  let window;
  let document;

  beforeEach(() => {
    const html = fs.readFileSync(
      path.resolve(__dirname, 'index.html'),
      'utf-8'
    );
    dom = new JSDOM(html, { runScripts: 'dangerously' });
    window = dom.window;
    document = window.document;
  });

  it('[テスト内容の説明]', () => {
    // テストコード
    expect(window.変数名).toBe(期待値);
  });

  // 追加のテストケース...
});
```

#### レッスン13以降（DOM操作を学ぶ）

```
materials/
└── lesson-XXX.md              # 教材本体

exercises/
└── lesson-XXX/
    ├── index.html             # HTMLファイル
    ├── script.js              # 外部JavaScriptファイル
    └── index.test.js          # テストファイル（講師側が用意）

solutions/
└── lesson-XXX/
    ├── index.html             # 解答HTMLファイル
    └── script.js              # 解答JSファイル
```

**生成ファイル:**
- `materials/lesson-XXX.md` - 教材本体
- `exercises/lesson-XXX/index.html` - HTMLテンプレート
- `exercises/lesson-XXX/script.js` - 外部JSファイル
- `exercises/lesson-XXX/index.test.js` - Vitestテスト（講師が用意）
- `solutions/lesson-XXX/index.html` - 解答HTML
- `solutions/lesson-XXX/script.js` - 解答JS

**index.htmlの内容:**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lesson XXX</title>
</head>
<body>
    <!-- ここにHTML要素を追加してください -->

    <script src="script.js"></script>
</body>
</html>
```

**script.jsの内容:**
```javascript
// ここにコードを書いてください
```

**index.test.jsの内容例（DOM要素を確認する形式）:**
```javascript
import { describe, it, expect, beforeEach } from 'vitest';
import { JSDOM } from 'jsdom';
import fs from 'fs';
import path from 'path';

describe('Lesson XXX: [レッスンタイトル]', () => {
  let dom;
  let document;

  beforeEach(() => {
    const html = fs.readFileSync(
      path.resolve(__dirname, 'index.html'),
      'utf-8'
    );
    const js = fs.readFileSync(
      path.resolve(__dirname, 'script.js'),
      'utf-8'
    );

    dom = new JSDOM(html, {
      runScripts: 'outside-only',
      resources: 'usable'
    });
    document = dom.window.document;

    // JavaScriptを実行
    const scriptEl = document.createElement('script');
    scriptEl.textContent = js;
    document.body.appendChild(scriptEl);
  });

  it('[テスト内容の説明]', () => {
    const element = document.getElementById('要素ID');
    expect(element).not.toBeNull();
    expect(element.textContent).toBe('期待値');
  });

  // 追加のテストケース...
});
```

ディレクトリが存在しない場合は自動作成する。

## エラー処理

- 指定されたレッスン番号が見つからない場合はエラーメッセージを表示
- curriculum.mdが見つからない場合はエラーメッセージを表示

## 使用例

ユーザー: 「レッスン1の教材を作成して」
→ materials/lesson-001.md を生成

ユーザー: 「レッスン13の教材を生成」
→ materials/lesson-013.md を生成（関数を学んだ後ならexercises/とsolutions/も生成）
