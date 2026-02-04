---
name: .claude/skills/zero-trust-security/SKILL.md
description: |
  Zero Trust Security原則に基づく機密情報管理スキル。

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/zero-trust-security/resources/continuous-verification-implementation.md`: Continuous Verification Implementationリソース
  - `.claude/skills/zero-trust-security/resources/jit-access-patterns.md`: Jit Access Patternsリソース
  - `.claude/skills/zero-trust-security/resources/rbac-implementation.md`: Rbac Implementationリソース

  - `.claude/skills/zero-trust-security/templates/access-policy-template.yaml`: Access Policyテンプレート

version: 1.0.0
---

# Zero Trust Security

## 概要

Zero Trust（ゼロトラスト）は「誰も信用しない」前提のセキュリティモデルです。
従来の境界防御ではなく、すべてのアクセスを毎回検証し、最小権限で
機密情報へのアクセスを制限します。

## Zero Trust の 5 原則

### 原則 1: 境界の消失

**従来モデル**: 内部ネットワーク = 安全
**Zero Trust**: すべてのアクセスが潜在的に危険

**Secret 管理への適用**:

- 開発者であっても本番 Secret に無制限アクセスは持たない
- 社内ネットワークからのアクセスも認証・認可が必要
- VPN 接続していても追加検証を実施

**実装の詳細**: `resources/boundary-elimination-patterns.md`

### 原則 2: 継続的検証

**概念**: すべてのアクセスリクエストを毎回検証する

**Secret 管理への適用**:

- セッショントークンの短い有効期限（15 分-1 時間）
- Secret アクセス毎の認証・認可チェック
- 異常なアクセスパターンの即座検知

**実装の詳細**: `resources/continuous-verification-implementation.md`

### 原則 3: マイクロセグメンテーション

**概念**: アクセス権限を細分化し、最小単位で管理

**Secret 管理への適用**:

- Secret をサービス単位で分離
- 各サービスは必要最小限の Secret のみにアクセス
- クロスサービスアクセスは明示的な承認が必要

**実装例**:

```typescript
const secretPolicies = {
  "discord-service": ["DISCORD_WEBHOOK_URL"],
  "ai-service": ["OPENAI_API_KEY", "DATABASE_URL"],
  "payment-service": ["STRIPE_SECRET_KEY", "DATABASE_URL"],
};

function validateServiceAccess(service: string, secretName: string): boolean {
  const allowed = secretPolicies[service] || [];
  return allowed.includes(secretName);
}
```

### 原則 4: 動的ポリシー

**概念**: コンテキストに応じてアクセス制御を動的に変更

**適用例**:

- 時間帯制限: 営業時間外のアクセスは追加承認
- 地理的制限: 許可された地域外からのアクセス拒否
- 異常検知: 通常と異なるパターンで追加認証

**実装の詳細**: `resources/dynamic-policy-engine.md`

### 原則 5: 監視と分析

**概念**: すべての活動を監視し、異常を即座に検知

**実装要件**:

- すべての Secret アクセスをリアルタイムログ
- 異常パターンの自動検知
- アラート通知（Slack、Discord、Email）

**実装の詳細**: `resources/monitoring-and-alerting.md`

## アクセス制御パターン

### パターン 1: RBAC (Role-Based Access Control)

**構成**: User → Role → Permissions → Secrets

**実装**:

```typescript
const roles = {
  developer: {
    permissions: [{ action: "read", resources: ["secret/dev/*"] }],
  },
  devops: {
    permissions: [
      { action: "read", resources: ["secret/dev/*", "secret/staging/*"] },
      { action: "rotate", resources: ["secret/staging/*"] },
    ],
  },
  security_admin: {
    permissions: [{ action: "*", resources: ["secret/*"] }],
  },
};
```

**詳細**: `resources/rbac-implementation.md`

### パターン 2: ABAC (Attribute-Based Access Control)

**構成**: User Attributes + Resource Attributes + Environment → Decision

**詳細**: `resources/abac-implementation.md`

### パターン 3: JIT (Just-In-Time) Access

**概念**: 必要な時に、必要な期間だけアクセス権限を付与

**実装**:

```typescript
async function requestJITAccess(
  userId: string,
  secretName: string,
  duration: number,
  justification: string,
): Promise<AccessGrant> {
  const approval = await requestApproval({ userId, secretName, justification });

  return await grantTemporaryAccess({
    userId,
    secretName,
    expiresAt: Date.now() + duration,
    approvedBy: approval.approver,
  });
}
```

**詳細**: `resources/jit-access-patterns.md`

## 異常検知ルール

### ルールベース検知

```typescript
const anomalyRules = [
  {
    name: "rapid_access",
    condition: (event) => event.accessCount > 10 && event.timeWindow < 600000,
    severity: "high",
    action: "alert",
  },
  {
    name: "unusual_time",
    condition: (event) => event.hour < 6 || event.hour > 22,
    severity: "medium",
    action: "require_mfa",
  },
  {
    name: "new_location",
    condition: (event) => !event.user.knownLocations.includes(event.location),
    severity: "high",
    action: "block",
  },
];
```

**詳細**: `resources/anomaly-detection-rules.md`

## 監査とコンプライアンス

### 監査ログ要件

すべての Secret アクセスで記録:

- Who（誰が）: user_id, email, roles
- What（何を）: action, secret_name, classification
- When（いつ）: timestamp
- Where（どこで）: ip_address, location
- How（どのように）: access_method, session_id
- Result（結果）: success/denied/error

**実装**: `resources/audit-logging-implementation.md`

## 実装チェックリスト

### Zero Trust 原則

- [ ] 内部開発者も無制限アクセスを持たない設計か？
- [ ] すべてのアクセスが毎回検証されるか？
- [ ] Secret がサービス単位で分離されているか？
- [ ] 動的ポリシー（時間、地域等）が考慮されているか？
- [ ] すべてのアクセスが監査ログに記録されるか？

### 最小権限

- [ ] 各サービスが必要最小限の Secret のみにアクセスするか？
- [ ] クロスサービスアクセスが明示的に承認制か？
- [ ] 環境間の Secret 共有が防止されているか？

### 継続的検証

- [ ] セッション有効期限が短い（15 分-1 時間）か？
- [ ] 異常アクセスパターンが検知されるか？
- [ ] MFA が高リスクアクセスで要求されるか？

## 関連スキル

- `.claude/skills/secret-management-architecture/SKILL.md` - Secret 管理アーキテクチャ
- `.claude/skills/encryption-key-lifecycle/SKILL.md` - 鍵管理
- `.claude/skills/environment-isolation/SKILL.md` - 環境分離

## リソースファイル

詳細な実装は以下を参照:

- `resources/rbac-implementation.md` - RBAC 詳細実装
- `resources/jit-access-patterns.md` - JIT アクセス実装
- `resources/continuous-verification-implementation.md` - 継続的検証実装

## テンプレート

- `templates/access-policy-template.yaml` - アクセスポリシーテンプレート
