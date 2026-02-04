---
name: practice-writer
description: 技術研修演習問題を執筆。概要・問題・解答形式・解答例の構造、:::stepディレクティブでハンズオン手順を記述。演習問題作成時に使用。
---

# 演習問題執筆 Skill

技術研修用演習教材の作成基準を定義します。

## 演習問題作成の情報源

- **演習問題作成のする上での情報源はテキスト教材（各研修コースのtextフォルダ）の内容から作成します。**
  - 演習問題のファイル名から、同じ章番号ののテキスト教材の内容を確認し、その内容に合わせて演習問題を作成します。
  - （演習問題のファイル名が`practice/chapter-02.md`なら、`text/chapter-02.md`の内容を基に演習問題を作成します。）
- 演習問題の数は1つの章ごとに複数作成します。（5問以内）
- 演習問題はテキストで学習した内容を着実に手を動かして理解させるための問題を作成します。

## 参照ルール

以下のルールファイルも参照してください：

- @rules/common/writing-style.md - 文章作成の基本方針
- @rules/common/codeblock-rules.md - コードブロック記述ルール

## 基本構造

### Frontmatter設定（必須）

各章ごとに独立したMarkdownファイルとし、frontmatterでメタデータを設定：

```yaml
---
title: [その章のタイトル]
draft: false
---
```

### ページ構成要素（必須順序）

1. Frontmatter
2. `{{ toc }}`
3. 演習問題（複数の演習を段階的に配置）

```markdown
---
title: [その章のタイトル]
draft: false
---

{{ toc }}

## [演習1のタイトル]

## 概要

[演習1の概要]

### 問題

[演習1の問題]

### 解答形式

[演習1の解答形式、解答するファイルの使用を記載]

//clearpage

### 解答例

[演習1の解答に仕方の詳細を記述]

:::step

[（必要に応じて）演習1を理解させるためのハンズオン手順の詳細]

:::


## [演習2のタイトル]

## 概要

[演習2の概要]

### 問題

[演習2の問題]

### 解答形式

[演習2の解答形式]

//clearpage

### 解答例

[演習2の解答に仕方の詳細を記述]

:::step

[（必要に応じて）演習2を理解させるためのハンズオン手順の詳細]

:::
```

## 演習問題の具体例

```markdown
## 演習1 DI（依存性注入）の利用

### 概要

Spring FrameworkのDI（依存性注入）を使ってクラス依存を確認する。

### 問題

Spring FrameworkのDIを使ってクラス依存を確認しなさい。次のように`MorningGreet`クラスをDIコンテナに登録し、`MorningGreetTest`のテストクラスでDIコンテナから取得した`MorningGreet`クラスのインスタンスを使ってテストを実行する。

![](../images/di/di-p1.drawio.svg)

### 解答形式

#### MorningGreetクラスの作成

`src/main/java`の`com.example.practice.di`パッケージの中に`MorningGreet.java`クラスを作成する。

- `@Component`アノテーションを付与する。
- 下記のメソッドを実装する。

戻り値型|メソッド名|引数|内容
---|---|---|---
String|say|String name|「nameさん、おはようございます」を戻す

#### MorningGreetTestクラスの作成

`src/test/java`の`com.example.practice.di`パッケージの中に`MorningGreetTest.java`クラスを作成する。下記のメソッドを実装する。

戻り値型|メソッド名|引数|内容
---|---|---|---
void|testSay|なし|「nameさん、おはようございます。」が戻ることをテストする

### 解答例

#### MorningGreetクラス

- `@Component`アノテーションを付与することにより、DIコンテナに登録されます。
- 次のように`MorningGreet`クラスを作成します。

_src/main/java/com.example.practice.di/MorningGreet.java_
```java
//addstart
@Component
public class MorningGreet {
  public String say(String name) {
    return name + "さん、おはようございます";
  }
}
//addend
```

#### MorningGreetTestクラス

- `@SpringBootTest`アノテーションを付与することにより、Spring Bootのテスト環境になります。
- 次のように`MorningGreetTest`クラスを作成します。

_src/test/java/com.example.practice.di/MorningGreetTest.java_
```java
//addstart
@SpringBootTest
public class MorningGreetTest {
  @Autowired
  private MorningGreet morningGreet;
  @Test
  public void testSay() {
    assertEquals("nameさん、おはようございます", morningGreet.say("name"));
  }
}
//addend
```
```

## 設計原則

### 段階的難易度

1. **基礎演習**: 単一概念の実践
2. **応用演習**: 複数概念の組み合わせ
3. **統合演習**: 実際の開発シナリオに近い問題

### 問題の明確性

- 要求事項を具体的に記述
- 成果物の形式を明確化
- 評価基準を明示

### 実践性

- 実際の開発業務に即した内容
- 現場で使用される技術やツールを活用
- 実装可能な範囲での現実的な問題設定

## ファイル命名規則

- `chapter-XX.md` 形式（XXは章番号の2桁）
- 出力先: `dist/exercise/chapter-XX.md`
