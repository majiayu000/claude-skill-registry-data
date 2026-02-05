---
name: cpp14-code-review
description: 'AUTOSAR C++14およびCERT C++コーディング規約に準拠したC++14コードレビュー。安全性重視のC++システムのコードレビュー、セキュリティ監査、品質評価、静的解析ツール設定を行う際に使用。'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# C++14 Code Review with AUTOSAR and CERT Standards

このスキルは、AUTOSAR C++14およびCERT C++コーディング規約に基づいたC++14コードレビューを支援します。

## いつこのスキルを使用するか

以下の場合に本スキルを活用してください:

- AUTOSAR C++14準拠のコードレビューを実行する
- CERT C++セキュアコーディング基準に基づくセキュリティ監査を行う
- 組込みシステムや安全性が重視されるコードを評価する
- Git差分レビュー（プルリクエスト）を効率的に実施する
- 静的解析ツール（Clang-Tidy、Cppcheck）の設定とCI/CD統合を行う
- メモリ安全性、スレッド安全性、例外安全性を検証する

## コードレビュープロセス

### ステップ1: レビュー準備

```bash
# Git差分の取得（プルリクエストレビュー）
git diff <base-commit> <head-commit> > changes.diff

# または特定ファイルのみ
git diff <base-commit> <head-commit> -- src/core/*.cpp > core-changes.diff
```

### ステップ2: 自動チェック実行

#### Clang-Tidyの使用

[Clang-Tidy設定ファイル](./configs/.clang-tidy)を参照してください。

```bash
# AUTOSAR/CERTチェック実行
clang-tidy --config-file=.clang-tidy src/**/*.cpp

# または特定ファイル
clang-tidy --checks='autosar-*,cert-*' src/core/Parser.cpp
```

#### Cppcheckの使用

```bash
# MISRA/CERT準拠チェック
cppcheck --addon=misra --addon=cert --enable=all src/

# XML出力（CI/CD向け）
cppcheck --addon=cert --xml --xml-version=2 src/ 2> report.xml
```

### ステップ3: 手動レビュー観点

[レビューチェックリスト](./checklists/review-checklist.md)を参照してください。

## 優先度別レビュー基準

### 優先度1: Critical（即座に修正）

**メモリ安全性違反**
- バッファオーバーフロー（CERT ARR30-C, ARR38-C）
- Use-after-free（CERT MEM50-CPP）
- ダングリングポインタ（CERT EXP54-CPP）
- メモリリーク（AUTOSAR A18-5-2）

**セキュリティ脆弱性**
- 整数オーバーフロー（CERT INT50-CPP）
- SQLインジェクション、コマンドインジェクション
- 入力バリデーション欠如

**未定義動作**
- 初期化されていない変数の使用（AUTOSAR A8-5-2）
- ヌルポインタデリファレンス（CERT EXP34-C）
- 配列範囲外アクセス

### 優先度2: High（早急に修正）

**AUTOSAR必須ルール違反**
- A5-0-3: 明示的な型変換の使用
- A7-1-1: constexpr変数の使用
- A12-8-1: コピー制御（Rule of Five/Zero）
- A15-5-1: 例外のthrow by value, catch by reference

**リソース管理**
- RAIIパターンの未使用（AUTOSAR A15-1-2）
- スマートポインタの未使用（AUTOSAR A18-5-2）
- 例外安全性の欠如（CERT ERR50-CPP）

### 優先度3: Medium（計画的に修正）

**AUTOSARアドバイザリールール違反**
- A0-1-6: 未使用の値（戻り値の無視）
- A2-13-3: 型の不一致
- M5-0-21: ビット演算の優先順位

**const correctness**
- const修飾の不徹底（AUTOSAR A7-1-1）
- constexpr関数の未使用
- const参照の未使用（AUTOSAR A8-4-1）

### 優先度4: Low（改善推奨）

**コード品質**
- 命名規約の不統一
- コメント不足
- 循環的複雑度が高い（> 10）

**Modern C++機能の未活用**
- ラムダ式の活用可能箇所
- 範囲forループの使用可能箇所
- auto型推論の適用可能箇所

## AUTOSAR C++14主要ルール

### メモリ管理

**A18-5-2: 動的メモリは例外的にのみ使用**
```cpp
// ❌ 悪い例
void process() {
    int* data = new int[100];
    // 例外発生時にメモリリーク
    processData(data);
    delete[] data;
}

// ✅ 良い例
void process() {
    std::vector<int> data(100);  // RAII
    processData(data.data());
}  // 自動的に解放
```

**A18-1-1: C言語メモリ管理関数を使用しない**
```cpp
// ❌ 悪い例
char* buffer = (char*)malloc(256);
free(buffer);

// ✅ 良い例
std::vector<char> buffer(256);
```

### 型安全性

**A5-0-3: 明示的な型変換を使用**
```cpp
// ❌ 悪い例
double d = 3.14;
int i = (int)d;  // C言語スタイルキャスト

// ✅ 良い例
int i = static_cast<int>(d);
```

**A8-4-1: 関数パラメータは参照またはポインタで渡す**
```cpp
// ❌ 悪い例
void process(std::vector<int> data) {  // コピー発生
    // ...
}

// ✅ 良い例
void process(const std::vector<int>& data) {  // 参照渡し
    // ...
}
```

### 例外処理

**A15-5-1: throw by value, catch by reference**
```cpp
// ❌ 悪い例
throw new std::runtime_error("Error");  // ポインタをthrow

// ✅ 良い例
throw std::runtime_error("Error");  // 値をthrow

// キャッチ
try {
    // ...
} catch (const std::exception& e) {  // 参照でキャッチ
    // ...
}
```

### オブジェクト指向

**A12-8-1: Rule of Five/Zero**
```cpp
// ✅ Rule of Zero（推奨）
class Resource {
    std::unique_ptr<Data> data_;  // スマートポインタを使用
    // コピー・ムーブが自動生成される
};

// ✅ Rule of Five（リソース管理が必要な場合）
class CustomResource {
public:
    ~CustomResource();  // デストラクタ
    CustomResource(const CustomResource&);  // コピーコンストラクタ
    CustomResource& operator=(const CustomResource&);  // コピー代入
    CustomResource(CustomResource&&) noexcept;  // ムーブコンストラクタ
    CustomResource& operator=(CustomResource&&) noexcept;  // ムーブ代入
};
```

## CERT C++主要ルール

### セキュリティ

**INT50-CPP: 整数オーバーフローを防ぐ**
```cpp
// ❌ 悪い例
int calculate(int a, int b) {
    return a * b;  // オーバーフロー未チェック
}

// ✅ 良い例
#include <limits>
int calculate(int a, int b) {
    if (a > 0 && b > std::numeric_limits<int>::max() / a) {
        throw std::overflow_error("Integer overflow");
    }
    return a * b;
}
```

**STR50-CPP: 文字列リテラルを変更しない**
```cpp
// ❌ 悪い例
char* str = "Hello";  // 文字列リテラルへのポインタ
str[0] = 'h';  // 未定義動作

// ✅ 良い例
const char* str = "Hello";  // 変更不可
// または
std::string str = "Hello";  // 変更可能なコピー
```

### メモリ管理

**MEM51-CPP: 適切にメモリを解放**
```cpp
// ❌ 悪い例
void process() {
    Resource* res = new Resource();
    if (someCondition) {
        return;  // メモリリーク
    }
    delete res;
}

// ✅ 良い例
void process() {
    auto res = std::make_unique<Resource>();
    if (someCondition) {
        return;  // 自動的に解放
    }
}
```

## 静的解析ツール設定

### Clang-Tidy設定

[完全な設定ファイル](./configs/.clang-tidy)を参照。

主要チェック:
- `autosar-*`: AUTOSAR C++14ルール
- `cert-*`: CERT C++ルール
- `modernize-*`: Modern C++への移行
- `cppcoreguidelines-*`: C++ Core Guidelines

### CI/CD統合

#### GitHub Actions例

[CI/CD設定例](./configs/github-actions.yml)を参照。

```yaml
name: C++ Code Review

on: [pull_request]

jobs:
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Clang-Tidy
        run: |
          clang-tidy --checks='autosar-*,cert-*' src/**/*.cpp
      - name: Run Cppcheck
        run: |
          cppcheck --addon=cert --xml src/ 2> report.xml
```

## Git差分レビューワークフロー

### 1. 変更ファイルの特定

```bash
# プルリクエストの変更ファイル一覧
git diff --name-only origin/main...HEAD

# C++ファイルのみ抽出
git diff --name-only origin/main...HEAD | grep -E '\.(cpp|hpp|h)$'
```

### 2. 変更箇所の詳細確認

```bash
# 関数単位で変更を表示
git diff -U5 origin/main...HEAD -- src/core/Parser.cpp

# 統計情報
git diff --stat origin/main...HEAD
```

### 3. レビューポイントの集中

変更箇所のみに以下を集中確認:
- [ ] 新規追加されたポインタ・動的メモリ割り当て
- [ ] 変更された例外処理
- [ ] 型変換の追加・変更
- [ ] ループ・条件分岐の変更

## レビューレポートテンプレート

```markdown
# コードレビューレポート

## ファイル: `src/core/Parser.cpp`

### Critical Issues (優先度1)
- **Line 156**: バッファオーバーフロー（CERT ARR30-C）
  - 問題: 固定サイズバッファ使用
  - 修正案: `std::vector<char>`または`std::string`を使用

### High Issues (優先度2)
- **Line 203**: AUTOSAR A18-5-2違反
  - 問題: `new`の直接使用
  - 修正案: `std::make_unique`を使用

### Medium Issues (優先度3)
- **Line 89**: const correctness
  - 問題: const参照で渡すべき
  - 修正案: `void process(const Data& data)`

## サマリー
- Critical: 1件
- High: 1件
- Medium: 1件
- 推奨: マージ前に修正が必要
```

## 参考リソース

- [AUTOSAR C++14 Guidelines](https://www.autosar.org/fileadmin/standards/R22-11/AP/AUTOSAR_RS_CPP14Guidelines.pdf)
- [CERT C++ Coding Standard](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Clang-Tidy Documentation](https://clang.llvm.org/extra/clang-tidy/)
- [設定ファイル集](./configs/)
- [チェックリスト](./checklists/)

## 次のステップ

1. [静的解析ツール設定](./configs/.clang-tidy)をプロジェクトに適用
2. [レビューチェックリスト](./checklists/review-checklist.md)を使用してレビュー実施
3. [CI/CD統合](./configs/github-actions.yml)を設定
4. レビュー結果を文書化
