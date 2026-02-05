---
name: securing-code
description: Enforces secure coding practices. Required after all code implementations to run CodeGuard security check. Covers input validation, secrets management, and OWASP countermeasures.
---

# セキュアコーディング

## 📚 目次

### 基本
- [使用タイミング](#-使用タイミング)
- [CodeGuard統合](#-codeguard統合必須)
- [クイックリファレンス](#-クイックリファレンス)

### 詳細ガイド
- [OWASP Top 10対策](OWASP-TOP10.md) - OWASP Top 10の各項目の詳細解説と対策
- [入力検証とインジェクション対策](INPUT-VALIDATION.md) - 入力検証、サニタイゼーション、SQLインジェクション、XSS、CSRF対策
- [認証・認可と機密情報管理](AUTH-SECRETS.md) - 認証、認可、パスワード管理、環境変数、暗号化
- [セキュアヘッダーとその他の対策](SECURE-HEADERS.md) - HTTPヘッダー、ファイルアップロード、レート制限、ログ管理

## 🎯 使用タイミング

**必須タイミング**:
- **すべてのコード実装完了時（必須）**
- **外部入力処理時**
- **認証・認可実装時**
- **機密情報取扱時**

**推奨タイミング**:
- API実装時
- データベース操作時
- ファイルアップロード処理時
- セッション管理実装時

## 🔒 CodeGuard統合（必須）

### 基本フロー
```
1. コード実装完了
   ↓
2. CodeGuard実行（必須）
   Skill tool: /codeguard-security:software-security
   ↓
3. 脆弱性検出
   ↓
4. 指摘された問題を修正
   ↓
5. 再度CodeGuardで検証
   ↓
6. すべてクリアを確認
   ↓
7. 完了報告
```

### CodeGuard実行コマンド
```bash
# Skill toolを使用
/codeguard-security:software-security
```

**重要**:
- CodeGuardの指摘を無視してはいけません
- 必ずすべての問題を修正してから次のステップに進んでください
- 完了報告にはCodeGuardチェック結果を含めてください

### CodeGuardチェック項目
- SQLインジェクション
- XSS（クロスサイトスクリプティング）
- CSRF（クロスサイトリクエストフォージェリ）
- 認証・認可の問題
- 機密情報漏洩
- 安全でない暗号化
- パストラバーサル
- コマンドインジェクション
- etc.

## ⚡ クイックリファレンス

### 最優先対策（必須）

#### 1. すべての外部入力を検証
```typescript
// ✅ 入力検証
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(150)
})

const validated = schema.parse(input)
```

#### 2. SQLインジェクション対策
```typescript
// ✅ プリペアドステートメント
const user = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]  // パラメータバインディング
)
```

#### 3. XSS対策
```typescript
// ✅ エスケープ処理
import DOMPurify from 'dompurify'
const sanitized = DOMPurify.sanitize(userContent)
```

#### 4. 機密情報管理
```typescript
// ✅ 環境変数
const apiKey = process.env.API_KEY

// ❌ ハードコーディング禁止
const apiKey = "key123"  // 絶対禁止
```

#### 5. 認証・認可
```typescript
// ✅ パスワードハッシュ化
import bcrypt from 'bcrypt'
const hashed = await bcrypt.hash(password, 10)

// ✅ 認可チェック
if (currentUser.role !== 'admin') {
  throw new Error('Unauthorized')
}
```

### 実装完了前チェックリスト

コード実装完了時に必ず確認：
- [ ] **CodeGuardセキュリティチェック実施済み**
- [ ] すべての外部入力を検証・サニタイゼーション
- [ ] SQLインジェクション対策（プリペアドステートメント）
- [ ] XSS対策（エスケープ処理）
- [ ] CSRF対策（トークン検証）
- [ ] 機密情報は環境変数で管理
- [ ] パスワードはハッシュ化
- [ ] 認可チェック実装
- [ ] セキュリティヘッダー設定
- [ ] エラーメッセージに機密情報を含まない
- [ ] ログに機密情報を出力しない

## 📖 詳細ガイドへのナビゲーション

### [OWASP Top 10対策](OWASP-TOP10.md)
OWASP Top 10の各脆弱性についての詳細解説と対策方法：
- A01: アクセス制御の不備
- A02: 暗号化の失敗
- A03: インジェクション
- A04: 安全が確認されない不安全な設計
- A05: セキュリティの設定ミス
- A06: 脆弱で古くなったコンポーネント
- A07: 識別と認証の失敗
- A08: ソフトウェアとデータの整合性の不備
- A09: セキュリティログとモニタリングの失敗
- A10: サーバーサイドリクエストフォージェリ

### [入力検証とインジェクション対策](INPUT-VALIDATION.md)
入力検証、サニタイゼーション、各種インジェクション攻撃への対策：
- 入力検証の実装方法
- サニタイゼーション技術
- SQLインジェクション対策
- XSS（クロスサイトスクリプティング）対策
- CSRF（クロスサイトリクエストフォージェリ）対策
- コマンドインジェクション対策

### [認証・認可と機密情報管理](AUTH-SECRETS.md)
認証、認可、機密情報の安全な管理方法：
- セキュアな認証実装
- 認可とアクセス制御
- パスワード管理のベストプラクティス
- 環境変数による機密情報管理
- 暗号化とハッシュ化
- JWTトークンの安全な使用

### [セキュアヘッダーとその他の対策](SECURE-HEADERS.md)
HTTPヘッダー、ファイルアップロード、その他のセキュリティ対策：
- セキュアHTTPヘッダーの設定
- ファイルアップロード対策
- レート制限の実装
- セキュアなログ管理
- 依存関係のセキュリティ管理

## 🔗 関連スキル

- **[enforcing-type-safety](../enforcing-type-safety/SKILL.md)**: 型安全性でセキュリティ向上
- **[testing](../testing/SKILL.md)**: セキュリティテストの実施
- **[applying-solid-principles](../applying-solid-principles/SKILL.md)**: セキュアな設計原則

## 💡 ベストプラクティス

### セキュリティファースト開発
1. **設計段階からセキュリティを考慮**
   - Threat Modeling（脅威モデリング）
   - Principle of Least Privilege（最小権限の原則）
   - Defense in Depth（多層防御）

2. **実装時の心構え**
   - すべての入力は信頼できないと仮定
   - セキュアなデフォルト設定
   - 早期失敗（Fail Fast）

3. **継続的なセキュリティ向上**
   - 定期的な依存関係更新
   - セキュリティスキャンの自動化
   - インシデント対応計画の策定

### セキュリティツールの活用
- **CodeGuard**: AIによるセキュリティコードレビュー（必須）
- **依存関係スキャン**: npm audit, Snyk, Dependabot
- **静的解析**: ESLint security plugins, SonarQube
- **動的解析**: OWASP ZAP, Burp Suite

## ⚠️ よくある間違い

### ❌ やってはいけないこと
- CodeGuardチェックをスキップする
- エラーメッセージに機密情報を含める
- `eval()`や`exec()`を使用する（特別な理由がない限り）
- クライアントサイドのバリデーションのみに依存
- 古い依存関係を放置する
- セキュリティ警告を無視する

### ✅ 正しいアプローチ
- すべてのコード実装後にCodeGuardを実行
- サーバーサイドでの検証を必須とする
- 定期的な依存関係更新
- セキュリティ警告への迅速な対応
- セキュリティテストの自動化

## 📚 参考資料

### 公式ガイド
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

### セキュリティツール
- [CodeGuard Documentation](https://github.com/anthropics/codeguard)
- [Snyk](https://snyk.io/)
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit)

---

**次のステップ**: 各詳細ガイドを参照して、セキュアなコードを実装してください。
