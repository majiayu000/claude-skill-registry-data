---
name: researching-libraries
description: Researches existing libraries before implementation. Required before writing any new functionality. Prevents reinventing the wheel by finding and evaluating existing packages.
---

# ライブラリ調査（車輪の再発明禁止）

## 🎯 使用タイミング

- **新機能実装前（必須）**
- **ユーティリティ関数を書こうとした時**
- **複雑なロジック実装前**
- **外部サービス連携時**

## 🚨 絶対ルール

```
❌ 調査せずに実装を始める → 禁止
✅ 必ず既存ライブラリを調査してから実装
```

**自作が許可されるケース**:
- 適切なライブラリが存在しない
- ライブラリが要件を満たさない
- セキュリティ・ライセンス上の問題がある
- 依存関係が過剰になる

## 📚 ドキュメント構成

### 1. [言語別検索方法](./SEARCH-METHODS.md)
各言語のパッケージ検索コマンドとMCP活用法：
- JavaScript/TypeScript (npm)
- Python (PyPI)
- Go (pkg.go.dev)
- Rust (crates.io)
- Ruby (RubyGems)

### 2. [評価基準](./EVALUATION-CRITERIA.md)
ライブラリ採用の判断基準：
- 信頼性指標（Stars、ダウンロード数）
- メンテナンス状況
- セキュリティチェック
- ライセンス確認

## 🔄 調査フロー

### Step 1: 機能の明確化
```
「〇〇を実装したい」
  ↓
キーワードを抽出
  ↓
検索クエリを作成
```

### Step 2: ライブラリ検索

**MCP優先（推奨）**:
```bash
# Context7でライブラリドキュメント取得
context7: resolve-library-id("zod")
context7: get-library-docs("/colinhacks/zod")

# DeepWikiでGitHubリポジトリ調査
deepwiki: ask_question("vercel/next.js", "認証ライブラリの推奨は？")
```

**コマンド実行（補助）**:
```bash
# npm
npm search <keyword> --long

# Go
go list -m all | grep <keyword>
```

### Step 3: 候補の評価

| 基準 | 最低ライン |
|------|-----------|
| ⭐ GitHub Stars | 500+ |
| 📅 最終更新 | 6ヶ月以内 |
| 📦 週間DL数 | 10,000+ |
| 🔒 脆弱性 | 0件 |

### Step 4: 決定とドキュメント

```markdown
## ライブラリ選定理由

### 採用: `zod`
- 目的: スキーマバリデーション
- Stars: 30k+
- 理由: TypeScript-first、軽量、活発なメンテナンス

### 見送り: `yup`
- 理由: TypeScriptサポートが限定的
```

## 🎯 よくある実装とライブラリ対応

### JavaScript/TypeScript

| やりたいこと | 使うべきライブラリ |
|-------------|-------------------|
| バリデーション | zod, valibot, yup |
| 日付操作 | date-fns, dayjs |
| HTTP通信 | ky, axios, got |
| 状態管理 | zustand, jotai |
| フォーム | react-hook-form |
| テーブル | @tanstack/table |
| アニメーション | framer-motion |
| ユーティリティ | lodash-es, radash |

### Python

| やりたいこと | 使うべきライブラリ |
|-------------|-------------------|
| バリデーション | pydantic |
| HTTP通信 | httpx, aiohttp |
| CLI作成 | typer, click |
| 設定管理 | python-dotenv, dynaconf |
| 日付操作 | pendulum, arrow |
| データ処理 | polars, pandas |

### Go

| やりたいこと | 使うべきライブラリ |
|-------------|-------------------|
| HTTP Router | chi, echo, gin |
| バリデーション | go-playground/validator |
| 設定読込 | viper, envconfig |
| ログ | slog (標準), zerolog |
| テスト | testify, ginkgo |

## 💡 アンチパターン

### ❌ よくある間違い

```typescript
// ❌ Bad: 自作のdebounce関数
function debounce(fn, ms) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
}

// ✅ Good: lodash-esを使用
import { debounce } from 'lodash-es';
```

```python
# ❌ Bad: 自作の日付パース
def parse_date(date_str):
    # 複雑なパース処理...

# ✅ Good: pendulumを使用
import pendulum
dt = pendulum.parse(date_str)
```

### ❌ 過度な依存も避ける

```typescript
// ❌ Bad: 1関数のためにlodash全体をインポート
import _ from 'lodash';
_.isEmpty(obj);

// ✅ Good: 必要な関数のみインポート
import isEmpty from 'lodash-es/isEmpty';

// ✅ Better: 標準機能で十分な場合
Object.keys(obj).length === 0;
```

## 🔗 関連スキル

- **[applying-solid-principles](../applying-solid-principles/SKILL.md)**: 依存性逆転の原則
- **[securing-code](../securing-code/SKILL.md)**: 依存ライブラリのセキュリティ
- **[testing](../testing/SKILL.md)**: モックとスタブ

## 📖 次のステップ

1. **検索方法を知りたい**: [言語別検索方法](./SEARCH-METHODS.md)
2. **評価基準を確認**: [評価基準](./EVALUATION-CRITERIA.md)
3. **すぐに探したい**: 上の「よくある実装とライブラリ対応」表を参照
