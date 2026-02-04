---
name: .claude/skills/api-versioning/SKILL.md
description: |
  APIバージョニング戦略と後方互換性管理を専門とするスキル。

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/api-versioning/resources/versioning-strategies.md`: バージョニング方式の比較と選択基準
  - `.claude/skills/api-versioning/resources/breaking-changes.md`: 破壊的変更の定義と影響範囲管理
  - `.claude/skills/api-versioning/resources/deprecation-process.md`: 段階的廃止プロセスとHTTPヘッダー活用
  - `.claude/skills/api-versioning/templates/migration-guide-template.md`: バージョン間移行ガイドテンプレート
  - `.claude/skills/api-versioning/templates/deprecation-notice-template.md`: 非推奨化通知テンプレート
  - `.claude/skills/api-versioning/scripts/check-breaking-changes.js`: 破壊的変更検出スクリプト
  - `.claude/skills/api-versioning/scripts/generate-migration-guide.sh`: 移行ガイド自動生成スクリプト

  核心知識:
  - バージョニング方式の選択（URL Path / Header / Query）
  - 破壊的変更の管理と移行戦略
  - 非推奨化（Deprecation）プロセス
  - バージョン間の差分文書化

  使用タイミング:
  - APIバージョニング戦略を決定する時
  - 破壊的変更を導入する時
  - エンドポイントを非推奨化する時
  - バージョン間の移行ガイドを作成する時

version: 1.0.0
---

# API Versioning スキル

## 概要

APIバージョニング戦略の設計と後方互換性管理に関する専門知識を提供します。

## コマンドリファレンス

```bash
# リソース参照
cat .claude/skills/api-versioning/resources/versioning-strategies.md
cat .claude/skills/api-versioning/resources/deprecation-process.md
cat .claude/skills/api-versioning/resources/breaking-changes.md

# テンプレート参照
cat .claude/skills/api-versioning/templates/migration-guide-template.md
cat .claude/skills/api-versioning/templates/deprecation-notice-template.md
```

---

## 知識領域1: バージョニング方式

### 主要な方式比較

| 方式             | 例                                            | メリット             | デメリット     |
| ---------------- | --------------------------------------------- | -------------------- | -------------- |
| **URL Path**     | `/api/v1/users`                               | 明確、キャッシュ容易 | URLが長くなる  |
| **Header**       | `Accept: application/vnd.api+json; version=1` | URLがシンプル        | 発見しにくい   |
| **Query**        | `/api/users?version=1`                        | シンプル             | キャッシュ問題 |
| **Content-Type** | `Content-Type: application/vnd.api.v1+json`   | 標準的               | 複雑           |

### 選択基準

| 条件             | 推奨方式 |
| ---------------- | -------- |
| RESTful純粋主義  | Header   |
| 開発者体験重視   | URL Path |
| レガシー互換性   | Query    |
| 新規プロジェクト | URL Path |
| 外部公開API      | URL Path |
| 内部API          | Header   |

### 推奨: URL Path Versioning

```
/api/v1/users     ← 現行バージョン
/api/v2/users     ← 新バージョン
```

**理由**:

- 直感的で発見しやすい
- キャッシュが容易
- デバッグが簡単
- 広く採用されている

---

## 知識領域2: バージョン番号設計

### Semantic Versioning（SemVer）原則

```
MAJOR.MINOR.PATCH
例: 1.2.3
```

| 種類  | 変更時             | URL反映            |
| ----- | ------------------ | ------------------ |
| MAJOR | 破壊的変更         | ✅ 反映（v1 → v2） |
| MINOR | 後方互換の機能追加 | ❌ 非反映          |
| PATCH | バグ修正           | ❌ 非反映          |

### URL表記

```
/api/v1/...      ← メジャーバージョンのみ
/api/v1.2/...    ← 避ける（複雑化）
```

### バージョン選択ロジック

```
クライアントリクエスト → バージョン解決
├─ /api/v1/users → API v1.x.x の最新を使用
├─ /api/v2/users → API v2.x.x の最新を使用
└─ /api/users    → デフォルトバージョン（v1）を使用
```

---

## 知識領域3: 破壊的変更の定義

### 破壊的変更（Breaking Changes）

| 変更種類                 | 破壊的？ | 説明                     |
| ------------------------ | -------- | ------------------------ |
| エンドポイント削除       | ✅ Yes   | 既存クライアントが壊れる |
| フィールド削除           | ✅ Yes   | 既存クライアントが壊れる |
| フィールド名変更         | ✅ Yes   | 既存クライアントが壊れる |
| 必須フィールド追加       | ✅ Yes   | 既存リクエストが無効に   |
| 型変更                   | ✅ Yes   | パース失敗の可能性       |
| ステータスコード変更     | ✅ Yes   | エラーハンドリング破損   |
| 認証方式変更             | ✅ Yes   | 認証失敗                 |
| オプションフィールド追加 | ❌ No    | 後方互換                 |
| 新エンドポイント追加     | ❌ No    | 後方互換                 |
| レスポンスフィールド追加 | ❌ No    | 後方互換（通常）         |

### 非破壊的変更

| 変更種類                 | 注意点                           |
| ------------------------ | -------------------------------- |
| オプションフィールド追加 | デフォルト値を設定               |
| 新エンドポイント追加     | 既存に影響なし                   |
| レスポンスフィールド追加 | クライアントは無視すべき         |
| 列挙値の追加             | クライアントは未知値を処理すべき |

---

## 知識領域4: 非推奨化プロセス

### 段階的廃止フロー

```
1. 告知期間（2-4週間）
   ├─ ドキュメント更新
   ├─ Sunset ヘッダー追加
   └─ 移行ガイド公開

2. 警告期間（4-8週間）
   ├─ Deprecation ヘッダー追加
   ├─ ログ監視（使用状況）
   └─ 個別通知

3. 移行サポート期間（4-12週間）
   ├─ 新旧両方を並行稼働
   ├─ 移行サポート提供
   └─ 使用量モニタリング

4. 廃止実行
   ├─ エンドポイント無効化
   ├─ 410 Gone レスポンス
   └─ 代替エンドポイント案内
```

### HTTPヘッダー

```http
# 非推奨警告
Deprecation: true
Deprecation: @1735689600  # Unix timestamp

# 廃止日
Sunset: Sat, 01 Mar 2025 00:00:00 GMT

# 代替リソース
Link: </api/v2/users>; rel="successor-version"
```

### OpenAPI での非推奨マーク

```yaml
paths:
  /api/v1/users:
    get:
      deprecated: true
      summary: "[非推奨] ユーザー一覧取得"
      description: |
        ⚠️ このエンドポイントは2025年3月1日に廃止されます。
        代替: GET /api/v2/users
      x-sunset-date: "2025-03-01"
```

---

## 知識領域5: 移行戦略

### 並行稼働パターン

```
期間1: v1のみ
期間2: v1（主）+ v2（ベータ）
期間3: v1（非推奨）+ v2（主）
期間4: v2のみ
```

### バージョン分岐実装

```typescript
// ルーティング例（Next.js）
// app/api/v1/users/route.ts
// app/api/v2/users/route.ts

// バージョン共通ロジック
// lib/api/users/v1.ts
// lib/api/users/v2.ts
```

### データ変換レイヤー

```typescript
// v1 → v2 変換
function transformV1ToV2(v1Data: V1User): V2User {
  return {
    id: v1Data.id,
    fullName: `${v1Data.firstName} ${v1Data.lastName}`, // フィールド統合
    email: v1Data.email,
    role: mapRoleV1ToV2(v1Data.role), // 値マッピング
    createdAt: v1Data.created_at, // 命名規則変更
  };
}
```

---

## 知識領域6: バージョン間差分文書化

### 変更ログ形式

```markdown
# API Changelog

## v2.0.0 (2025-03-01)

### 破壊的変更

- `GET /users` のレスポンス構造が変更されました
  - `first_name` + `last_name` → `full_name` に統合
- `role` フィールドの値が変更されました
  - `"admin"` → `"administrator"`

### 新機能

- `GET /users/{id}/activity` エンドポイント追加
- ページネーションに `cursor` パラメータ追加

### 非推奨

- `GET /users?page=N` は廃止予定（`cursor` を使用してください）

### 移行ガイド

詳細は [Migration Guide v1 → v2](./migration-v1-v2.md) を参照
```

---

## 判断基準チェックリスト

### バージョン戦略

- [ ] バージョニング方式が決定されているか？
- [ ] URLパターンが一貫しているか？
- [ ] デフォルトバージョンが定義されているか？

### 破壊的変更

- [ ] 変更は本当に破壊的か？
- [ ] 非破壊的な代替案はないか？
- [ ] 影響範囲を把握しているか？

### 非推奨化

- [ ] 十分な告知期間があるか？（最低4週間）
- [ ] 移行ガイドが準備されているか？
- [ ] Deprecation/Sunsetヘッダーが設定されているか？
- [ ] 使用状況をモニタリングしているか？

### 移行サポート

- [ ] 新旧バージョンの並行稼働期間があるか？
- [ ] 移行ツールやスクリプトが提供されているか？
- [ ] サポート連絡先が明示されているか？

---

## 関連スキル

- `.claude/skills/openapi-specification/SKILL.md`: OpenAPI仕様書作成
- `.claude/skills/request-response-examples/SKILL.md`: バージョン別実例
- `.claude/skills/authentication-docs/SKILL.md`: 認証バージョニング

---

## 変更履歴

| バージョン | 日付       | 変更内容     |
| ---------- | ---------- | ------------ |
| 1.0.0      | 2025-11-27 | 初版リリース |
