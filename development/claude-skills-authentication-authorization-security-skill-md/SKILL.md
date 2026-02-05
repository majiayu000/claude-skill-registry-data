---
name: .claude/skills/authentication-authorization-security/SKILL.md
description: |
  認証・認可機構のセキュリティ評価とベストプラクティスを提供します。
  ブルース・シュナイアーの『Secrets and Lies』とOAuth 2.0仕様に基づき、
  認証メカニズム、セッション管理、アクセス制御、JWT/トークンセキュリティの
  包括的な評価基準と実装ガイダンスを提供します。

  使用タイミング:
  - 認証システムのセキュリティレビュー時
  - OAuth/OpenID Connect実装の評価時
  - セッション管理とトークンセキュリティの設計時
  - アクセス制御（RBAC/ABAC）の実装評価時
  - JWT署名アルゴリズムとトークン管理の検証時

  Use this skill when reviewing authentication code, designing authorization systems,
  or validating token security implementations.

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/authentication-authorization-security/resources/access-control-models.md`: RBAC/ABAC/ACLアクセス制御モデルの詳細比較と選択基準
  - `.claude/skills/authentication-authorization-security/resources/jwt-security-checklist.md`: JWT署名アルゴリズム選択とトークンセキュリティ検証項目
  - `.claude/skills/authentication-authorization-security/resources/oauth2-flow-comparison.md`: OAuth 2.0フロー（Authorization Code、PKCE等）の選択決定ツリー
  - `.claude/skills/authentication-authorization-security/resources/password-hashing-guide.md`: bcrypt/argon2/scryptハッシュアルゴリズムの設定と実装ガイド
  - `.claude/skills/authentication-authorization-security/resources/session-management-patterns.md`: サーバーサイドセッションとCookie属性のセキュリティパターン
  - `.claude/skills/authentication-authorization-security/scripts/analyze-auth-endpoints.mjs`: 認証エンドポイントのセキュリティ分析スクリプト
  - `.claude/skills/authentication-authorization-security/scripts/check-token-security.mjs`: JWTトークンセキュリティ検証スクリプト
  - `.claude/skills/authentication-authorization-security/scripts/validate-session-config.mjs`: セッション設定のセキュリティ検証スクリプト
  - `.claude/skills/authentication-authorization-security/templates/session-security-checklist.md`: セッション管理セキュリティチェックリストテンプレート
version: 1.0.0
related_skills:
  - .claude/skills/owasp-top-10/SKILL.md
  - .claude/skills/input-sanitization/SKILL.md
  - .claude/skills/security-testing/SKILL.md
---

# Authentication & Authorization Security

## スキル概要

このスキルは、認証・認可機構のセキュリティ評価に特化した専門知識を提供します。

**専門分野**:

- 認証メカニズムの評価（パスワード、OAuth、MFA）
- セッション管理とトークンセキュリティ
- アクセス制御モデルの評価（RBAC、ABAC）
- 権限昇格脆弱性の検出
- JWT/トークンセキュリティの評価

**理論的基盤**:

- ブルース・シュナイアー『Secrets and Lies』: セキュリティプロセスと防御層
- Aaron Parecki『OAuth 2.0 Simplified』: OAuth標準とベストプラクティス
- OWASP Authentication Cheat Sheet: 認証実装ガイドライン

---

## 1. 認証機構の評価基準

### 1.1 パスワードベース認証

**強度要件**:

- 最小長: 8文字以上（推奨: 12文字以上）
- 複雑性: 大文字、小文字、数字、記号の組み合わせ
- 辞書攻撃対策: 一般的なパスワードのブラックリスト
- パスワード履歴: 過去N個のパスワード再利用禁止

**ハッシュアルゴリズム評価**:

```
✅ 推奨:
  - bcrypt (cost factor: 10-12)
  - argon2id (メモリハード関数、PHC推奨)
  - scrypt (メモリハード、PBKDF2より強固)

⚠️ 許容:
  - PBKDF2-HMAC-SHA256 (iteration: 100,000+)

❌ 非推奨:
  - MD5, SHA1 (高速すぎ、衝突攻撃可能)
  - 平文保存
  - 可逆暗号化（AES等でパスワード暗号化）
```

**判断基準**:

- [ ] パスワードは安全なハッシュアルゴリズム（bcrypt/argon2）でハッシュ化されているか？
- [ ] ソルトは各ユーザーでユニークか？
- [ ] ハッシュのcost factorは適切か（bcrypt: 10-12）？
- [ ] レインボーテーブル攻撃への対策があるか？

### 1.2 セッション管理

**セッショントークン要件**:

- 予測不可能性: 暗号論的に安全な乱数生成器（CSPRNG）使用
- エントロピー: 最低128ビット（推奨: 256ビット）
- 有効期限: アクティビティに基づいた適切な期限設定
- 再生成: ログイン成功時、権限変更時にセッションIDを再生成

**Cookie設定**:

```typescript
// ✅ 推奨設定
Set-Cookie: sessionId=xxx; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=3600
```

**セッション固定攻撃対策**:

1. ログイン成功時に新しいセッションIDを発行
2. 古いセッションIDを無効化
3. セッションIDをURLパラメータに含めない

**判断基準**:

- [ ] セッショントークンは予測不可能か（CSPRNG使用）？
- [ ] HttpOnlyフラグが設定されているか（XSS対策）？
- [ ] Secureフラグが設定されているか（HTTPS強制）？
- [ ] SameSite属性が設定されているか（CSRF対策）？
- [ ] ログイン時にセッションIDが再生成されるか？

### 1.3 多要素認証（MFA）

**実装評価基準**:

- TOTP（Time-based OTP）: RFC 6238準拠、30秒ウィンドウ
- SMS/Email OTP: レート制限、有効期限（5-10分）
- ハードウェアトークン: WebAuthn/FIDO2対応
- バックアップコード: 使い捨て、安全に保存

**判断基準**:

- [ ] MFAは任意ではなく、管理者やセンシティブ操作で強制されているか？
- [ ] TOTP実装はタイムドリフトに対応しているか？
- [ ] バックアップコードは1回限りの使用に制限されているか？
- [ ] MFAバイパス攻撃（リプレイ攻撃等）への対策があるか？

---

## 2. OAuth 2.0 / OpenID Connect

### 2.1 フロー選択の妥当性

**Authorization Code Flow + PKCE**:

- 用途: Webアプリケーション、モバイルアプリ
- セキュリティ: 最も安全、リフレッシュトークン対応
- 必須要素: PKCE（Proof Key for Code Exchange）

**Implicit Flow**:

- 状態: **非推奨** - セキュリティリスクが高い
- 理由: アクセストークンがURLフラグメントに露出

**Client Credentials Flow**:

- 用途: サーバー間通信、M2M認証
- 制約: ユーザーコンテキストなし

**判断基準**:

- [ ] SPAやモバイルアプリでPKCEが使用されているか？
- [ ] Implicit Flowは使用されていないか？
- [ ] stateパラメータでCSRF対策がされているか？
- [ ] nonceパラメータでリプレイ攻撃対策がされているか？

### 2.2 トークン管理

**アクセストークン**:

- 有効期限: 短期（15分-1時間）
- 保存場所: メモリ内（LocalStorageは避ける）
- 送信方法: Authorizationヘッダー（Bearer Token）

**リフレッシュトークン**:

- 有効期限: 長期（数日-数週間）
- 保存場所: HttpOnly Secure Cookie（推奨）
- ローテーション: 使用時に新しいトークンを発行
- 取り消し: ログアウト時、不正検出時に即座に無効化

**判断基準**:

- [ ] アクセストークンの有効期限は適切に短いか？
- [ ] リフレッシュトークンはHttpOnly Cookieで保護されているか？
- [ ] トークンローテーションが実装されているか？
- [ ] トークン取り消しメカニズムが存在するか？

---

## 3. アクセス制御モデル

### 3.1 RBAC（Role-Based Access Control）

**実装評価**:

- ロール定義: 明確な責任範囲を持つロール
- ロール階層: 継承関係の設計
- 権限マッピング: ロールから権限への適切なマッピング
- デフォルト拒否: 明示的な許可がない限り拒否

**権限チェックのポイント**:

```typescript
// ✅ サーバーサイドで検証
function deleteUser(userId, currentUser) {
  if (!currentUser.roles.includes("admin")) {
    throw new ForbiddenError();
  }
  // 処理...
}

// ❌ クライアントサイドのみで制御
// UIで削除ボタンを非表示にするだけでは不十分
```

**判断基準**:

- [ ] 権限チェックはサーバーサイドで行われているか？
- [ ] すべてのAPIエンドポイントで認可チェックがあるか？
- [ ] デフォルト拒否原則が適用されているか？
- [ ] ロール定義は最小権限の原則に従っているか？

### 3.2 権限昇格脆弱性

**垂直権限昇格**:

- 一般ユーザーが管理者機能にアクセス
- 検証ポイント: ロールチェックの一貫性

**水平権限昇格**:

- ユーザーAがユーザーBのデータにアクセス
- 検証ポイント: リソース所有権の確認

**検出パターン**:

```
// ❌ 危険: IDパラメータのみで検証なし
GET /api/users/{userId}/profile

// ✅ 安全: 所有権を検証
if (requestedUserId !== currentUser.id && !currentUser.isAdmin) {
  throw new ForbiddenError();
}
```

**判断基準**:

- [ ] ユーザーIDパラメータは所有権検証されているか？
- [ ] ロール昇格のチェックが全エンドポイントにあるか？
- [ ] 間接的なオブジェクト参照（IDOR）への対策があるか？

---

## 4. JWT（JSON Web Token）セキュリティ

### 4.1 署名アルゴリズム

**安全なアルゴリズム**:

```
✅ 推奨:
  - RS256 (RSA署名、公開鍵検証)
  - ES256 (楕円曲線、RS256より高速)

⚠️ 許容（シークレット管理が確実な場合）:
  - HS256 (HMAC、対称鍵)

❌ 危険:
  - none (署名なし)
  - HS256でシークレットが弱い場合
```

**alg header攻撃対策**:

- アルゴリズムをホワイトリスト化
- `alg: none`を拒否
- 署名検証を必ず実行

### 4.2 クレーム設計

**標準クレーム**:

- `iss` (issuer): トークン発行者
- `sub` (subject): ユーザー識別子
- `aud` (audience): トークン対象
- `exp` (expiration): 有効期限（必須）
- `iat` (issued at): 発行時刻
- `jti` (JWT ID): リプレイ攻撃対策

**判断基準**:

- [ ] expクレームが設定され、検証されているか？
- [ ] audクレームで対象アプリケーションを制限しているか？
- [ ] センシティブデータ（パスワード、SSN）がペイロードに含まれていないか？

### 4.3 トークン保存

**保存場所の評価**:

```
✅ 推奨:
  - メモリ内（SPA、短命アクセストークン）
  - HttpOnly Secure Cookie（リフレッシュトークン）

⚠️ 注意:
  - LocalStorage（XSSリスク）
  - SessionStorage（XSSリスク）

❌ 危険:
  - URLパラメータ
  - 通常のCookie（HttpOnlyなし）
```

**判断基準**:

- [ ] トークンはLocalStorageではなく、安全な場所に保存されているか？
- [ ] XSS攻撃でトークンが漏洩しないか？
- [ ] トークンはHTTPSでのみ送信されるか（Secureフラグ）？

---

## 5. セキュアなセッションライフサイクル

### 5.1 セッション開始

**ログインフロー**:

1. 認証情報の検証（ユーザー名/パスワード）
2. MFA検証（有効な場合）
3. 新しいセッションIDの生成（CSPRNG）
4. 古いセッション（ある場合）の無効化
5. セッション固定攻撃対策

### 5.2 セッション維持

**アクティビティベースの有効期限**:

- 絶対タイムアウト: ログインから一定時間後に強制ログアウト
- アイドルタイムアウト: 非アクティブ時間後に自動ログアウト
- スライディングウィンドウ: アクティビティで期限延長

**同時セッション管理**:

- 単一デバイス制限: 1ユーザー1セッションのみ許可
- 複数デバイス許可: すべてのアクティブセッション管理
- セッション一覧: ユーザーが自身のセッションを確認・削除可能

### 5.3 セッション終了

**ログアウト処理**:

1. サーバーサイドでセッションを無効化
2. トークンをブラックリストに追加（JWT使用時）
3. クライアント側でトークンを削除
4. Cookieをクリア

**強制ログアウト**:

- パスワード変更時
- 権限変更時
- 不正アクセス検出時
- セキュリティポリシー違反時

**判断基準**:

- [ ] ログアウト時にサーバーサイドでセッションが無効化されるか？
- [ ] トークン取り消しメカニズムが実装されているか？
- [ ] クライアント側のトークンが確実に削除されるか？

---

## 6. アクセス制御の一貫性

### 6.1 エンドポイント保護

**すべてのエンドポイントでの検証**:

```typescript
// ✅ 一貫した権限チェック
app.use("/api/admin/*", requireRole("admin"));
app.get("/api/admin/users", listUsers);
app.delete("/api/admin/users/:id", deleteUser);

// ❌ 一部のエンドポイントでチェック漏れ
app.get("/api/admin/users", requireRole("admin"), listUsers);
app.delete("/api/admin/users/:id", deleteUser); // チェックなし
```

**リソースレベル認可**:

- オブジェクトIDの検証
- 所有権の確認
- 関連リソースへのアクセス制御

### 6.2 デフォルト拒否原則

**実装パターン**:

1. すべてのエンドポイントにデフォルトで認証を要求
2. 公開エンドポイントのみ明示的に許可
3. ホワイトリストアプローチ（ブラックリストではない）

**判断基準**:

- [ ] 新しいエンドポイント追加時、デフォルトで保護されるか？
- [ ] 公開エンドポイントは明示的にマークされているか？
- [ ] 認可チェックの漏れを検出する仕組みがあるか？

---

## 7. よくある認証・認可の脆弱性

### 7.1 脆弱性パターン

| 脆弱性タイプ         | 説明                                   | 検出方法                             |
| -------------------- | -------------------------------------- | ------------------------------------ |
| **セッション固定**   | 攻撃者が事前にセッションIDを設定       | ログイン時のセッションID再生成を確認 |
| **CSRF**             | 偽造リクエストでユーザーを騙す         | CSRF トークン、SameSite Cookie確認   |
| **権限昇格**         | 一般ユーザーが管理者機能を実行         | 全エンドポイントの認可チェック確認   |
| **IDOR**             | 直接オブジェクト参照で他人のデータ取得 | リソース所有権検証を確認             |
| **トークン漏洩**     | XSS/ログでトークンが露出               | トークン保存場所、ログ出力を確認     |
| **ブルートフォース** | パスワード総当たり攻撃                 | Rate Limiting、アカウントロック確認  |

### 7.2 攻撃シナリオと対策

**シナリオ1: セッションハイジャック**

- 攻撃: XSSでセッションCookieを窃取
- 対策: HttpOnly Cookie、CSP、入力サニタイズ

**シナリオ2: トークンリプレイ攻撃**

- 攻撃: 盗んだトークンを再利用
- 対策: 短い有効期限、jtiクレーム、トークンバインディング

**シナリオ3: パスワードスプレー攻撃**

- 攻撃: 共通パスワードで多数のアカウントを試行
- 対策: レート制限、CAPTCHA、異常検出

---

## 8. 実装チェックリスト

### 認証システム全体

- [ ] パスワードは安全にハッシュ化されている（bcrypt/argon2）
- [ ] セッショントークンは予測不可能である
- [ ] ログイン時にセッションIDが再生成される
- [ ] MFAが適切に実装されている（該当する場合）
- [ ] ブルートフォース攻撃対策がある（Rate Limiting、アカウントロック）

### OAuth/OpenID Connect

- [ ] PKCEが実装されている（Webアプリ、モバイルアプリ）
- [ ] stateパラメータでCSRF対策がされている
- [ ] トークンは安全に保存されている（HttpOnly Cookie推奨）
- [ ] リフレッシュトークンローテーションが実装されている
- [ ] Implicit Flowは使用されていない

### アクセス制御

- [ ] 認可チェックはサーバーサイドで行われている
- [ ] すべてのAPIエンドポイントで権限検証がある
- [ ] リソース所有権が検証されている（IDOR対策）
- [ ] デフォルト拒否原則が適用されている
- [ ] ロールは最小権限の原則に従っている

### セッション管理

- [ ] セッションCookieにHttpOnly、Secure、SameSite属性がある
- [ ] セッション有効期限が適切に設定されている
- [ ] ログアウト時にサーバーサイドでセッションが無効化される
- [ ] 同時セッション管理が実装されている（該当する場合）

---

## リソース・スクリプト・テンプレート

### リソース

- `resources/password-hashing-guide.md`: パスワードハッシュアルゴリズム詳細
- `resources/oauth2-flow-comparison.md`: OAuth 2.0フローの比較と選択ガイド
- `resources/jwt-security-checklist.md`: JWT実装セキュリティチェックリスト
- `resources/session-management-patterns.md`: セッション管理のベストプラクティス
- `resources/access-control-models.md`: RBAC、ABAC、ACLの詳細比較

### スクリプト

- `scripts/analyze-auth-endpoints.mjs`: 認証・認可エンドポイントの分析
- `scripts/check-token-security.mjs`: JWT/トークンセキュリティチェック
- `scripts/validate-session-config.mjs`: セッション設定の検証

### テンプレート

- `templates/rbac-policy-template.yaml`: RBACポリシー定義テンプレート
- `templates/oauth2-config-template.json`: OAuth 2.0設定テンプレート
- `templates/session-security-checklist.md`: セッションセキュリティチェックリスト

---

## 関連スキル

このスキルは以下のスキルと組み合わせて使用されます:

- `.claude/skills/owasp-top-10/SKILL.md`: OWASP A07（識別と認証の失敗）
- `.claude/skills/input-sanitization/SKILL.md`: 認証フォームの入力検証
- `.claude/skills/rate-limiting-strategies/SKILL.md`: ブルートフォース攻撃対策
- `.claude/skills/security-testing/SKILL.md`: 認証システムのセキュリティテスト

---

## 変更履歴

### v1.0.0 (2025-11-26)

- 初版リリース
- .claude/agents/sec-auditor.mdエージェントから知識領域3を抽出
- 認証機構、OAuth 2.0、アクセス制御、JWT、セッション管理の評価基準を定義
- パスワードハッシング、トークン管理、権限昇格検出のガイドライン追加
