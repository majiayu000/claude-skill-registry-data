---
name: software-architecture
description: |-
  Clean Architecture・DDD ベースのソフトウェア設計ガイドライン。Library-First アプローチ、命名規則、アンチパターン回避を提供する。
when_to_use: |-
  「アーキテクチャ」「設計」「Clean Architecture」「DDD」「ドメイン駆動設計」「リファクタリング」「コード品質」「命名規則」「責務分離」に関する作業のとき。
allowed-tools: Read, Edit, Grep, Glob
---

# ソフトウェアアーキテクチャ

Clean ArchitectureとDDD（ドメイン駆動設計）の原則に基づく、対象プロジェクトの設計ガイドライン。

## Domain層の実装パターン

> **本セクションのコード例は Next.js + Supabase + TypeScript スタックでの一例**。Clean Architecture /
> DDD のレイヤ責務（Entity / Repository / Service の分離、Interface によるモック差し替え）は
> スタック非依存の普遍的な原則であり、構文・生成ファイル名・ハンドラ種別は採用スタックに読み替えること。
> 実際のレイヤ規約は common `ARCHITECTURE.md` を SSoT とする。

データフローの一例（4層構造）:

```
DB型（database.types.ts） → Entity型（models/） → Service（service/） → Server Actions（app/*/actions.ts）
                              ↓
                         Repository（repository/）
```

### 1. Entity層（models/）

**型定義とクラスの併用パターン**: 型で構造定義、クラスでビジネスロジックを実装する。

```typescript
// domain/models/opportunity/index.ts

// 構造定義（Type）
export type OpportunityEntity = {
  id: string;
  title: string;
  salary_min: number;
  salary_max: number | null;
  deleted_at: string | null;
};

// ロジック実装（Class）
export class Opportunity {
  public readonly id: string;
  public readonly salaryMin: number;

  constructor(entity: OpportunityEntity) {
    this.id = entity.id;
    this.salaryMin = entity.salary_min;
  }

  isHighPay(): boolean {
    return this.salaryMin >= 1000000;
  }

  isDeleted(): boolean {
    return this.deletedAt !== null;
  }

  // Entity型 → UI型への変換
  toJob(): Job {
    return {
      id: this.id,
      salary: this.formatSalary(),
      highPay: this.isHighPay(),
    };
  }
}
```

**判断基準**: ビジネスルールが含まれる場合はClass、単純なデータ構造ならTypeのみで十分。

### 2. Repository層（repository/）

**Interface + 実装クラスパターン**: テスト時のモック差し替えを可能にする。

```typescript
// domain/repository/saved-agent/index.ts

export interface ISavedAgentRepository {
  create(userId: string, agentId: string): Promise<SavedAgent>;
  findByUserAndAgent(
    userId: string,
    agentId: string,
  ): Promise<SavedAgent | null>;
  softDeleteByUserAndAgent(
    userId: string,
    agentId: string,
  ): Promise<SavedAgent | null>;
}

export class SavedAgentRepository implements ISavedAgentRepository {
  private admin = createSupabaseAdmin();

  async create(userId: string, agentId: string): Promise<SavedAgent> {
    const { data, error } = await this.admin
      .from('saved_agents')
      .insert({ user_id: userId, agent_id: agentId })
      .select()
      .single();

    if (error?.code === '23505') {
      throw new Error('既に保存済みです');
    }
    if (error) throw error;
    return SavedAgent.fromDatabase(data);
  }
}
```

**パフォーマンス最適化の定石**:

| 手法       | 実装例                                                       |
| ---------- | ------------------------------------------------------------ |
| N+1回避    | 一括取得後にMapで結合: `new Map(agents.map(a => [a.id, a]))` |
| 計数最適化 | `.select('*', { count: 'exact', head: true })`               |
| 並列化     | `Promise.all([countQuery, dataQuery])`                       |
| 論理削除   | `.is('deleted_at', null)` を常に付与                         |

### 3. Service層（service/）

**Repository間の連携とビジネスロジックの集約場所**。

```typescript
// domain/service/saved-agent/index.ts
export class SavedAgentService {
  private repository: ISavedAgentRepository;

  constructor(repo?: ISavedAgentRepository) {
    this.repository = repo || new SavedAgentRepository();
  }

  async toggle(userId: string, agentId: string): Promise<{ isSaved: boolean }> {
    const existing = await this.repository.findByUserAndAgent(userId, agentId);

    if (existing && !existing.isDeleted()) {
      await this.repository.softDeleteByUserAndAgent(userId, agentId);
      return { isSaved: false };
    }

    if (existing && existing.isDeleted()) {
      await this.repository.restore(userId, agentId);
      return { isSaved: true };
    }

    await this.repository.create(userId, agentId);
    return { isSaved: true };
  }
}
```

**Service層の役割判断**:

- ビジネスロジックがない場合: Repositoryを直接呼んでもよい（不要な委譲層は作らない）
- 複数Repositoryの連携が必要な場合: Serviceで集約する
- 型変換（Entity → UI型）: Entity自身の`toXxx()`メソッド、またはServiceで実装

### 4. アプリケーション層 / ハンドラ（例: Server Actions）

UI からのエントリーポイントとなるハンドラ層。**フレームワークの推奨に従う**（例: Next.js なら
API ルートより Server Actions を優先）。戻り値は `{ success, error?, data? }` のような統一形式にする。

```typescript
// 例: Next.js Server Actions での一例
// app/feature/actions.ts
'use server';

export async function approveCertification(id: string) {
  try {
    const certification = await certificationRepository.getById(id);
    if (!certification) {
      return { success: false, error: '証明書が見つかりません' };
    }

    if (!certification.canApprove()) {
      return { success: false, error: '承認できない状態です' };
    }

    const approved = certification.approve();
    await certificationRepository.update(approved);
    await sendApprovalNotification(certification.userId);

    return { success: true };
  } catch (error) {
    console.error('Approval error:', error);
    return { success: false, error: '承認処理中にエラーが発生しました' };
  }
}
```

## コードスタイルルール

### 基本原則

- **Early return**: ネストを減らすため、ガード節で早期リターンする
- **Arrow functions**: function宣言よりアロー関数を優先
- **関数の長さ**: 50行を超えたら分割を検討
- **ファイルの長さ**: 200行を超えたら分割を検討
- **ネストの深さ**: 最大3レベル
- **コード重複回避**: 再利用可能な関数・モジュールに切り出す

### Library-Firstアプローチ

カスタムコードを書く前に、既存のライブラリ・サービスを検討する。すべてのカスタムコードは保守・テスト・ドキュメントのコストを伴うため、ライブラリで解決できるならそちらを優先する。

**カスタムコードが正当化される場合**:

- ドメイン固有のビジネスロジック
- パフォーマンスクリティカルな処理
- 既存ライブラリが要件を満たさない場合

### 命名規則

| 対象              | ルール                             | 例                            |
| ----------------- | ---------------------------------- | ----------------------------- |
| Entity型          | `XxxEntity`                        | `UserEntity`, `ProjectEntity` |
| Repository        | `IXxxRepository` / `XxxRepository` | `IProjectRepository`          |
| Service           | `XxxService`                       | `OpportunityService`          |
| ハンドラ関数（例: Server Action） | camelCase + 動詞                   | `createProject`, `updateUser` |
| ファイル/フォルダ | kebab-case                         | `saved-agent/index.ts`        |

**避けるべき名前**: `utils`, `helpers`, `common`, `shared`, `misc`
→ ドメイン固有の名前を使う: `SalaryFormatter`, `CertificationValidator`

### アンチパターン

| アンチパターン               | 代わりに                                     |
| ---------------------------- | -------------------------------------------- |
| `utils.ts`に雑多な関数を集約 | ドメインごとにモジュール分割                 |
| Repositoryにビジネスロジック | Service層に分離                              |
| UIコンポーネント内でDB操作   | アプリケーション層/ハンドラ経由（例: Server Actions）|
| 使用箇所1つで抽象化          | Rule of Three: 3箇所以上で重複してから抽象化 |
| `as`型キャスト               | 型注釈、`satisfies`、明示的マッピング関数    |
| `!`非nullアサーション        | `assert()`で明示チェック                     |

> コーディング規約の詳細は `.claude/docs/coding-conventions.md`（存在する場合）を参照

## 設計判断のガイドライン

### サーバー処理 vs クライアント処理（例: Next.js のサーバー/クライアントコンポーネント）

> 以下はサーバー/クライアント分割を持つフレームワーク（例: Next.js の React Server Components）での一例。
> 採用フレームワークの描画モデルに読み替えること。

| 基準             | サーバー側             | クライアント側               |
| ---------------- | ---------------------- | ---------------------------- |
| データ取得       | DB直接アクセス可能     | ハンドラ経由（例: Server Actions） |
| インタラクション | なし                   | フォーム、モーダル、状態管理 |
| SEO              | 対応                   | 非対応                       |

**原則（例: Next.js）**: デフォルトはサーバーコンポーネント。`'use client'`はインタラクションが必要な場合のみ。

### 責務の配置判断

```
Q1. 単純なCRUD操作？ → Repository
Q2. 複数Entity間のロジック？ → Service
Q3. Entity自身の状態チェック/変換？ → Entity（Model）のメソッド
Q4. UI操作のエントリーポイント？ → アプリケーション層/ハンドラ（例: Server Action）
Q5. 表示のための計算/整形？ → コンポーネント or Entity.toXxx()
```

## When NOT to Use This Skill

- **UI実装のみ**: `implementing-ui` skill を使用（`.stdd.config.yml` の `plugins` に列挙時。例: `plugins/nextjs-supabase/skills/implementing-ui/`）
- **DBマイグレーション**: `migrating-supabase` skill を使用（同上。例: `plugins/nextjs-supabase/skills/migrating-supabase/`）
- **テスト作成**: E2E プラグインの skill を使用（同上。例: `plugins/playwright/skills/e2e-testing/`）
