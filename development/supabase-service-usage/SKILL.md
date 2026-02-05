---
name: supabase-service-usage
description: アプリ全域の Supabase 利用ルール。サービス層の統一、Service Role の安全な使い分け、ログ付与、Server Actions 連携を規定。
---

# Supabase サービス利用規約

このスキルは、プロジェクトにおける Supabase 操作の「唯一の正解 (SSoT)」を定義します。常にこの規約を遵守してください。

## 1. サービス層の統一 (Unification)

- **原則**: すべての Supabase 操作は、基底クラス `SupabaseService` (実ファイル: `src/server/services/supabaseService.ts`) またはそのドメイン別サブクラス（例: `userService.ts`, `chatService.ts`）を介して実行してください。
- **禁止事項**: 業務ロジック内で `@supabase/supabase-js` を直接インポートして `createClient` を呼び出し、アドホックなクエリを記述することは厳禁です。

## 2. クライアント管理 (Client Management)

- **管理層**: クライアントの生成・管理は `src/lib/client-manager.ts` (`SupabaseClientManager`) が一括して担います。
- **インスタンス取得**:
  - `SupabaseService` 内では `SupabaseClientManager.getInstance().getServiceRoleClient()` を使用して特権操作を行います。
  - 特殊なケースを除き、直接 `manager` を叩くのではなく `SupabaseService` を継承・利用してください。

## 3. Service Role 利用の安全基準

- [IMPORTANT] `Service Role` は RLS を完全にバイパスするため、利用は以下の用途に限定してください。
  - **管理処理 (Admin)**: ユーザーロールの変更、全ユーザー一覧の取得など。
  - **バックグラウンド処理 (Batch/Cron)**: GSC データインポート、定期的なデータ評価など。
  - **特権が必要な内部 API**: LINE 認証紐付け、システム整合性チェックなど。
- [WARNING] RLS が効かないため、**アプリケーション層での明示的な ID チェックを省略してはなりません**。
  - クエリに `.eq('user_id', userId)` 等を含め、操作対象がそのユーザーの所有物であることを必ず保証してください。
- **推奨パターン**: 静的な特権操作が必要な場合は、`SupabaseService` を継承し、実在する `protected static withServiceRoleClient()` ユーティリティを活用してください（自動的に詳細なログが付与されます）。

## 4. エラーハンドリングとログ (Error Handling)

- **統一フォーマット**: 実在する `SupabaseService.failure()` メソッドを必ず使用し、ユーザー向けメッセージとエンジニア向け詳細ログ（`PostgrestError`, `context`）を適切に分離・記録してください。

## 5. 実装パターン (Recommended Pattern)

- Server Actions / Route Handlers 等からは、ドメイン固有のサービスを通じて `SupabaseService` の機能を呼び出します。
  ```typescript
  // 推奨される実装例 (サブクラス経由)
  export class AnalyticsContentService extends SupabaseService {
    static async getSomething(userId: string) {
      return this.withServiceRoleClient(
        async client => {
          const { data, error } = await client
            .from('content_annotations')
            .select('*')
            .eq('user_id', userId); // 権限チェックの必須化
          if (error) throw error;
          return data;
        },
        { logMessage: 'データ取得エラー:' }
      );
    }
  }
  ```

## 運用ルール

1. 新規テーブル追加時は、`supabaseService.ts` またはそのサブクラスに CRUD メソッドを追加することを基本としてください。
2. 複雑な結合クエリやパフォーマンスが重要な操作は、可能な限り Supabase RPC (関数) として実装し、サービス層から呼び出してください。
   - 目安: 3 テーブル以上の結合、サブクエリ/CTE/ウィンドウ関数を含む集計、条件分岐が 3 つ以上のビジネスロジック、クライアント側での後処理が重いケース、レイテンシに敏感なバッチ処理。
