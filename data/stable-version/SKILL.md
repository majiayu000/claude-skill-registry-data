---
name: stable-version
description: |
  各言語/フレームワークの安定版バージョン確認ガイド。
  LTSの考え方、EOLチェック、アップグレード判断をサポート。
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Task
---

# 安定版バージョン確認スキル

## 目的

技術スタックのバージョンを最適な状態に維持し、セキュリティリスクと技術的負債を最小化する。

## LTS（Long Term Support）の考え方

### LTS優先の原則

1. **本番環境**: LTSバージョンを使用（安定性・長期サポート重視）
2. **開発環境**: Current/Latest対応も許容（新機能の検証用）
3. **EOL前6ヶ月**: アップグレード計画を開始
4. **セキュリティパッチ**: EOL後はパッチ提供なし

### EOL（End of Life）対応

- **EOL後のリスク**: セキュリティパッチなし、脆弱性対応不可
- **EOL 6ヶ月前**: アップグレード計画開始
- **EOL 3ヶ月前**: アップグレード実施推奨
- **EOL到達**: 緊急アップグレード必須

## 並列監査（複数技術スタック対応）

**複数の技術スタックがあるプロジェクトの場合**、並列でサブエージェントに監査を委譲することで効率的にチェックできます。

**並列監査の実施方法:**

Taskツールで複数のサブエージェントを並列起動し、各技術スタックを同時に監査：

1. **Node.js** - バージョン、LTS状態、EOL確認
2. **Python** - バージョン、サポート状況
3. **Java** - バージョン、LTS確認
4. **フレームワーク** - Spring Boot, React, Vue.js等のバージョン
5. **その他** - PHP, Ruby, データベース等

各技術スタックの監査結果を統合し、全体のバージョン状況とEOLリスクをレポートします。

**メリット:**
- 複数技術を同時にチェック
- コンテキスト使用量を削減
- EOLリスクの早期発見
- アップグレード計画の優先度付け

---

## バージョン確認方法

### Node.js

```bash
# 現在のLTSバージョン確認
curl -s https://nodejs.org/dist/index.json | jq '[.[] | select(.lts != false)] | .[0]'

# ローカルバージョン確認
node --version

# nvm使用時の最新LTS
nvm ls-remote --lts | tail -1

# LTSスケジュール確認
# https://nodejs.org/en/about/releases/
# - 偶数バージョン（18, 20, 22）: LTS
# - 奇数バージョン（19, 21）: Current（短期サポート）
```

**LTS例:**
- Node.js 18.x: EOL 2025-04-30
- Node.js 20.x: EOL 2026-04-30
- Node.js 22.x: EOL 2027-04-30

### Python

```bash
# 公式リリーススケジュール
# https://devguide.python.org/versions/

# ローカルバージョン確認
python --version
python3 --version

# pyenv使用時
pyenv install --list | grep -E '^\s+3\.'
pyenv install --list | grep -v '[a-zA-Z]' | grep '^\s+3\.' | tail -5
```

**LTS例:**
- Python 3.9: EOL 2025-10
- Python 3.10: EOL 2026-10
- Python 3.11: EOL 2027-10
- Python 3.12: EOL 2028-10

### Java

```bash
# LTSバージョン: 8, 11, 17, 21
java -version

# SDKMAN使用時
sdk list java | grep -E '(8|11|17|21)\.'

# OpenJDK LTS確認
# https://openjdk.org/
```

**LTS例:**
- Java 8: 長期サポート（ベンダーにより異なる）
- Java 11: EOL 2026-09 (Oracle)
- Java 17: EOL 2029-09 (Oracle)
- Java 21: EOL 2031-09 (Oracle)

### Spring Boot

```bash
# 公式サポート状況確認
# https://spring.io/projects/spring-boot#support

# 現在のバージョン確認
./gradlew dependencies | grep spring-boot

# または pom.xml / build.gradle から確認
grep 'spring-boot' pom.xml
```

**サポート例:**
- Spring Boot 2.7.x: OSS support ended 2023-11-18
- Spring Boot 3.0.x: OSS support ended 2023-11-24
- Spring Boot 3.1.x: OSS support ended 2024-05-18
- Spring Boot 3.2.x: OSS support until 2025-02-23
- Spring Boot 3.3.x: OSS support until 2025-08-23

### PHP

```bash
# バージョン確認
php --version

# サポート状況確認
# https://www.php.net/supported-versions.php
```

**サポート例:**
- PHP 8.1: Security fixes until 2024-11-25
- PHP 8.2: Security fixes until 2025-12-08
- PHP 8.3: Security fixes until 2026-11-23

### その他フレームワーク

| 技術 | LTS確認方法 |
|------|-----------|
| React | GitHub releases確認 (https://github.com/facebook/react/releases) |
| Vue.js | https://v3.vuejs.org/guide/migration/introduction.html |
| Angular | https://angular.io/guide/releases |
| Rails | https://rubyonrails.org/ |
| Django | https://www.djangoproject.com/download/ |

## アップグレード判断基準

### 即時アップグレード推奨（Critical）

- ⚠️ セキュリティ脆弱性（CVE）が公開された場合
- ⚠️ EOLまで3ヶ月以内
- ⚠️ 重大なバグ修正リリース

### 計画的アップグレード（Warning）

- 📅 新LTSリリース後6ヶ月以内に計画開始
- 📅 メジャーバージョンアップは十分なテスト期間確保
- 📅 EOLまで6ヶ月〜3ヶ月

### アップグレード見送り可（Info）

- ✅ マイナーバージョン差（例: 3.2.1 → 3.2.3）
- ✅ 新機能のみのリリース（セキュリティパッチなし）
- ✅ 現行バージョンが最新LTS

## EOLチェックツール

### endoflife.date（推奨）

```bash
# Web API経由でEOL情報を取得
curl -s https://endoflife.date/api/nodejs.json | jq '.[] | select(.eol | contains("2025"))'
curl -s https://endoflife.date/api/python.json | jq '.[] | select(.eol | contains("2025"))'
curl -s https://endoflife.date/api/java.json | jq '.[] | select(.eol | contains("2025"))'
```

### 各プロジェクト公式

| 言語/FW | EOL情報URL |
|---------|-----------|
| Node.js | https://nodejs.org/en/about/releases/ |
| Python | https://devguide.python.org/versions/ |
| Java | https://www.oracle.com/java/technologies/java-se-support-roadmap.html |
| PHP | https://www.php.net/supported-versions.php |
| Ruby | https://www.ruby-lang.org/en/downloads/branches/ |

## アップグレードパスの設計

### メジャーバージョンアップ（例: Node.js 16 → 20）

```
Phase 1: 調査（1週間）
- Breaking changesの確認
- 依存パッケージの互換性確認
- テスト計画策定

Phase 2: 開発環境移行（1週間）
- Node.js 20インストール
- ローカルテスト実行
- 問題の洗い出しと修正

Phase 3: ステージング環境移行（1週間）
- CI/CD設定変更
- E2Eテスト実行
- パフォーマンステスト

Phase 4: 本番環境移行（1週間）
- ブルーグリーンデプロイメント
- モニタリング強化
- ロールバック準備
```

### マイナーバージョンアップ（例: 3.10.1 → 3.10.8）

```
即座に実施可能:
1. ローカルでテスト
2. CI/CD通過確認
3. 本番デプロイ
```

## CI/CDへの組み込み

### GitHub Actions 例

```yaml
name: Version Audit

on:
  schedule:
    - cron: '0 0 * * 1'  # 毎週月曜日
  workflow_dispatch:

jobs:
  version-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Check Node.js version
        run: |
          CURRENT=$(node --version | sed 's/v//')
          LATEST_LTS=$(curl -s https://nodejs.org/dist/index.json | jq -r '[.[] | select(.lts != false)] | .[0].version' | sed 's/v//')
          echo "Current: $CURRENT"
          echo "Latest LTS: $LATEST_LTS"
          if [ "$CURRENT" != "$LATEST_LTS" ]; then
            echo "⚠️ Node.js update available: $CURRENT → $LATEST_LTS"
          fi
```

## 参考資料

- [endoflife.date](https://endoflife.date/) - 複数技術のEOL情報
- [Node.js Releases](https://nodejs.org/en/about/releases/)
- [Python EOL](https://devguide.python.org/versions/)
- [Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)
- [PHP Supported Versions](https://www.php.net/supported-versions.php)
