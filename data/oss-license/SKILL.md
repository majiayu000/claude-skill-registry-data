---
name: oss-license
description: |
  OSSライセンス確認とコンプライアンスガイド。
  許可/禁止ライセンス一覧、確認ツール使用法をガイド。
allowed-tools: Bash, Read, Grep, Glob, Task
---

# OSSライセンス確認スキル

## 目的

依存パッケージのライセンスを確認し、ライセンス違反リスクを早期発見する。

## 重要な原則

### ✅ 許可ライセンス（一般的に使用可能）

- **MIT License** - 最も寛容なライセンス
- **Apache License 2.0** - 特許条項付き
- **BSD 2-Clause / 3-Clause** - シンプルな寛容ライセンス
- **ISC License** - MITと同等
- **CC0 / Public Domain** - 著作権放棄

### ⚠️ 要注意ライセンス（条件付き使用）

- **LGPL v2.1 / v3.0** - 動的リンクのみ許可（静的リンクは要注意）
- **MPL 2.0 (Mozilla Public License)** - ファイル単位のコピーレフト
- **CC BY-SA** - ドキュメント用（ShareAlike条項あり）
- **EPL (Eclipse Public License)** - 弱いコピーレフト

### ❌ 禁止ライセンス（商用利用時に要確認）

- **GPL v2 / v3** - 強いコピーレフト（全体がGPLになる）
- **AGPL v3** - ネットワーク経由でも適用される最も強いコピーレフト
- **SSPL (Server Side Public License)** - MongoDBなどで使用
- **CPAL (Common Public Attribution License)** - 帰属表示要求

## 並列監査（複数言語/技術スタック対応）

**複数の言語や技術スタックがあるプロジェクトの場合**、並列でサブエージェントに監査を委譲することで効率的にチェックできます。

**並列監査の実施方法:**

Taskツールで複数のサブエージェントを並列起動し、各言語の依存関係を同時に監査：

1. **Node.js依存関係** - package.json, package-lock.json
2. **Python依存関係** - requirements.txt, Pipfile, pyproject.toml
3. **Java依存関係** - pom.xml, build.gradle
4. **PHP依存関係** - composer.json
5. **その他** - 言語に応じたツール

各言語の監査結果を統合し、全体のライセンス状況をレポートします。

**メリット:**
- 複数言語を同時にチェック
- コンテキスト使用量を削減
- 抜け漏れのない網羅的監査
- 言語ごとの専門的なチェック

---

## ライセンス確認ツール

### Node.js プロジェクト

```bash
# license-checker インストール
npm install -g license-checker

# 依存関係のライセンス一覧
license-checker --summary

# 問題のあるライセンスを検出
license-checker --failOn "GPL;AGPL;SSPL"

# JSON出力（詳細分析用）
license-checker --json > licenses.json

# 特定ライセンスのみ表示
license-checker --onlyAllow "MIT;Apache-2.0;BSD"
```

### Python プロジェクト

```bash
# pip-licenses インストール
pip install pip-licenses

# 一覧表示
pip-licenses

# Markdown形式で出力
pip-licenses --format=markdown

# 許可リスト形式（違反を検出）
pip-licenses --allow-only="MIT;Apache 2.0;BSD"

# 禁止リスト形式
pip-licenses --fail-on="GPL;AGPL"
```

### Java プロジェクト（Gradle）

```gradle
// build.gradleに追加
plugins {
    id 'com.github.hierynomus.license' version '0.16.1'
}

license {
    header rootProject.file('LICENSE_HEADER')
    strictCheck true
}
```

または Maven:

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>license-maven-plugin</artifactId>
    <version>2.0.0</version>
</plugin>
```

### PHP プロジェクト（Composer）

```bash
# composer-licenses インストール
composer require dominikzogg/composer-licenses --dev

# ライセンス一覧
./vendor/bin/composer-licenses
```

### 汎用ツール

```bash
# FOSSA CLI（多言語対応）
fossa analyze
fossa test

# Snyk（セキュリティ + ライセンス）
snyk test --all-projects
snyk monitor

# Black Duck（エンタープライズ）
# GitHub App: License Compliance Action
```

## ライセンス違反発見時の対応フロー

### Step 1: 問題のある依存関係を特定

```bash
# Node.js の例
license-checker --json | jq '.[] | select(.licenses | contains("GPL"))'

# Python の例
pip-licenses --fail-on="GPL"
```

### Step 2: 依存関係の調査

1. **直接依存か間接依存か確認**
   ```bash
   # Node.js
   npm ls <package-name>

   # Python
   pipdeptree -p <package-name>
   ```

2. **使用箇所を特定**
   ```bash
   grep -r "import <package-name>" .
   ```

### Step 3: 代替パッケージを調査

- **同等機能のパッケージを検索**
  - npmtrends.com（Node.js）
  - pypi.org（Python）
  - Maven Central（Java）

- **ライセンス互換性を確認**
  - 代替パッケージのライセンスをチェック
  - 依存関係も確認

### Step 4: 対応策の実施

**A) 代替パッケージに置換**
```bash
npm uninstall <問題パッケージ>
npm install <代替パッケージ>
```

**B) 除外（使用していない場合）**
```bash
npm uninstall <問題パッケージ>
```

**C) 法務/コンプライアンスチームに相談**
- GPLライセンスの影響範囲を評価
- デュアルライセンスの可能性を確認
- 商用ライセンス購入の検討

## ライセンス互換性マトリクス

| 使用するライセンス | 依存先で許可されるライセンス |
|------------------|--------------------------|
| MIT/BSD/Apache   | ほぼすべて（GPL除く） |
| GPL v2           | GPL v2のみ |
| GPL v3           | GPL v3, AGPL v3 |
| LGPL             | すべて（動的リンク時） |
| 商用ライセンス     | MIT/BSD/Apache推奨 |

## CI/CDへの組み込み

### GitHub Actions 例

```yaml
name: License Check

on: [push, pull_request]

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install license-checker
        run: npm install -g license-checker

      - name: Check licenses
        run: license-checker --failOn "GPL;AGPL;SSPL"
```

### Screwdriver 例

```yaml
jobs:
  main:
    steps:
      - license-check: npm run license-check
```

## 参考資料

- [SPDX License List](https://spdx.org/licenses/) - 標準ライセンス一覧
- [choosealicense.com](https://choosealicense.com/) - ライセンス選択ガイド
- [OSS Watch License Compliance](https://www.oss-watch.ac.uk/) - コンプライアンスガイド
- [FOSSA Documentation](https://fossa.com/docs) - ライセンス管理ツール
- [GNU License List](https://www.gnu.org/licenses/license-list.html) - GPLとの互換性情報
