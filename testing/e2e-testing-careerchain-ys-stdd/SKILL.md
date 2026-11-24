---
name: e2e-testing
description: |-
  E2Eテストの作成・実行ガイドライン。Playwrightベストプラクティス、Locator選択、Web First Assertions、フレーキーテスト対策を提供。「E2Eテスト」「Playwright」「テスト作成」「E2Eテスト実行」「GitHub Actions」に関する作業で使用。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# E2Eテスト作成・実行スキル

対象プロジェクトにおけるPlaywright E2Eテストの作成・実行ガイド。

## Quick Start

### 1. テストファイルの配置

`.stdd.config.yml` の各 `apps[]` ごとにサブディレクトリを分けて配置する（`apps[].id` をディレクトリ名に用いる）。

```
e2e/tests/
├── <apps[].id>/       # 各 apps[] の E2Eテスト（apps[] の数だけ繰り返す）
│   └── *.spec.ts
└── ...
```

### 2. 基本的なテスト構造

対象アプリのベースURLは `.stdd.config.yml` の `apps[].port` から組み立てる（`http://localhost:<apps[].port>`）。ハードコードしないこと。

```typescript
import {
  test,
  expect,
  loginWithCredentials,
} from '../../fixtures/<apps[].id>/test-fixtures';

test.describe('機能名', () => {
  test('テストケース名', async ({ page, testUser }) => {
    // 認証が必要な場合はUIからログイン
    await loginWithCredentials(page, testUser.email, testUser.password);

    // テスト実行（ベースURLは apps[].port から組み立てる）
    await page.goto(`http://localhost:${process.env.PORT}/dashboard`);
    await expect(
      page.getByRole('heading', { name: 'ダッシュボード' }),
    ).toBeVisible();
  });
});
```

### 3. テスト実行（ローカル）

```bash
cd e2e
npx playwright test tests/<apps[].id>/login.spec.ts --headed
```

## Locator選択の優先順位

**重要原則**: ユーザーが実際に見たり操作する「レンダリングされた出力」をテスト対象にすること。

| 優先度 | Locator               | 用途                                 | 例                                          |
| ------ | --------------------- | ------------------------------------ | ------------------------------------------- |
| 1      | `getByRole`           | ボタン、リンク、見出し、フォーム要素 | `getByRole('button', { name: 'ログイン' })` |
| 2      | `getByLabel`          | フォーム入力欄（label紐づき）        | `getByLabel('メールアドレス')`              |
| 3      | `getByPlaceholder`    | プレースホルダーがある入力欄         | `getByPlaceholder('example@email.com')`     |
| 4      | `getByText`           | 静的テキストコンテンツ               | `getByText('登録完了しました')`             |
| 5      | `getByTestId`         | 上記で特定できない場合の最終手段     | `getByTestId('submit-button')`              |
| ❌     | `locator('selector')` | **避ける**: CSSセレクタやXPath       | `locator('input[type="email"]')`            |

### 良い例と悪い例

```typescript
// ✅ 良い例: アクセシビリティlocatorを使用
await page.getByRole('button', { name: 'ログイン' }).click();
await page.getByLabel('メールアドレス').fill('test@example.com');
await expect(
  page.getByRole('heading', { name: 'ダッシュボード' }),
).toBeVisible();

// ❌ 悪い例: CSSセレクタを使用
await page.locator('button[type="submit"]').click();
await page.locator('input[type="email"]').fill('test@example.com');
await expect(page.locator('h1')).toContainText('ダッシュボード');
```

## Web First Assertions（自動リトライ）

**重要原則**: Playwrightの自動リトライ機能を持つアサーションを使用すること。

```typescript
// ✅ 良い例: Web First Assertions（自動リトライ）
await expect(page.getByText('ログイン完了')).toBeVisible();
await expect(page.getByRole('button', { name: '送信' })).toBeEnabled();
await expect(page).toHaveURL('/dashboard');

// ❌ 悪い例: 非リトライアサーション
expect(await page.getByText('ログイン完了').isVisible()).toBe(true);
```

**主要アサーション**:

- `toBeVisible()` / `toBeHidden()` - 表示/非表示
- `toBeEnabled()` / `toBeDisabled()` - 有効/無効
- `toHaveText()` / `toContainText()` - テキスト内容
- `toHaveURL()` - ページURL
- `toHaveValue()` - 入力値

## 手動の待機を避ける

```typescript
// ✅ 良い例: 条件ベースの待機
await page.getByRole('button', { name: '送信' }).click();
await expect(page.getByText('送信完了')).toBeVisible();
await page.waitForURL('/success');

// ❌ 悪い例: 固定時間の待機
await page.waitForTimeout(2000); // 禁止！
```

## テストの独立性

**重要原則**: 各テストは他のテストに依存せず、単独で実行できること。

1. **テスト間でデータを共有しない**
2. **テストごとに必要なセットアップを行う**
3. **テスト後のクリーンアップ**

```typescript
test('ユーザー情報を更新できる', async ({ page, testUser }) => {
  // このテスト用にログイン
  await loginWithCredentials(page, testUser.email, testUser.password);

  // テスト実行
  await page.goto('/profile');
  // ...
});
```

## 並列実行時のテスト間干渉対策（必須）

⚠️ **対象プロジェクトのE2Eは `playwright.config.ts` で `fullyParallel: true` + 複数workerで動作する**。具体的には:

- 同じspecファイル内のテストはデフォルトで並列実行される
- specファイル間も並列実行される
- 各テストは別 worker（別 OS process）で実行される

つまり、別 spec が同時並行で **同じテーブル** を insert/update/delete する。これを考慮しないテストは「単独実行ではpass、CI実行で再現するflaky」になる。

### 干渉が起きやすい代表ケース

| ケース                                                   | 何が起こるか                                                         | 対策                                                                |
| -------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agents.select('id').limit(1)` で seed agent を取得      | 並行 spec が agents を insert/delete → 取得結果が不安定              | 専用 agent を beforeAll で **新規作成** して isolation              |
| `getByTestId('listing-card').first()` で先頭カードを操作 | 並行 spec が新規 record を insert → 「先頭」が他 spec のものに変わる | `.filter({ hasText: '専用prefix' })` で**特定のレコード**を選ぶ     |
| 共有 seed user (`test@example.com`) を使う複数テスト     | 同 user の `saved_*` テーブル状態がテスト間で引きずる                | `mode: 'serial'` + `beforeEach` で関連テーブル clear                |
| `from('agents').delete()`（user_id 等の限定なし）        | 他 spec のテストデータも消える                                       | `.eq('user_id', ...)` または `.in('id', createdIds)` で**必ず限定** |
| spec内テストが共有テーブルを操作                         | 同 spec 内のテスト同士で順序依存                                     | spec全体を `mode: 'serial'` 化                                      |

### 必須ルール

#### 1. 共有テーブル（agents/opportunities/applies/saved\_\* 等）は専用 prefix で完全分離

```typescript
// ❌ 悪い例: seed agent をそのまま借りる
const { data: agents } = await supabase.from('agents').select('id').limit(1);
const agentId = agents[0].id;

// ✅ 良い例: spec 専用 prefix で新規作成し、cleanup で完全削除
const PREFIX = 'E2E_<spec_name>_';
let testAgentId: string;
test.beforeAll(async () => {
  const { data: agent } = await supabase
    .from('agents')
    .insert({
      name: `${PREFIX}専用エージェント`,
      organization: `${PREFIX}テスト会社`,
      // ...
    })
    .select('id')
    .single();
  testAgentId = agent.id;
});
test.afterAll(async () => {
  await supabase.from('agents').delete().eq('id', testAgentId);
});
```

#### 2. spec内で複数テストが共有リソースを操作する場合は必ず `mode: 'serial'`

```typescript
test.describe('機能名', () => {
  // beforeAllで作成した opportunity/agent を複数テストで共有 → serial 必須
  test.describe.configure({ mode: 'serial' });

  test.beforeAll(async () => {
    /* 共有データ投入 */
  });
  test.afterAll(async () => {
    /* cleanup */
  });

  test('test1', async ({ page, testUser }) => {
    /* ... */
  });
  test('test2', async ({ page, testUser }) => {
    /* ... */
  });
});
```

`mode: 'serial'` を入れる判断基準:

- spec内に `test.beforeAll` で共有データを投入している
- 各テストが共通の seed user / 同一 opportunity / 同一 agent を操作する
- spec内テスト間で **テスト1の状態がテスト2に影響する**ロジックがある

#### 3. 「先頭/末尾」依存ロケータを避ける

```typescript
// ❌ 悪い例: 並行 spec が新規record を insert すると先頭が変わる
const card = page.getByTestId('listing-card').first();

// ✅ 良い例: 特定のテキスト/属性で限定
const card = page
  .getByTestId('listing-card')
  .filter({ hasText: 'E2E_専用エージェント' })
  .first();

// ✅ 良い例: 「特定のbadge等を持つカード」で限定（共有seed userを使うケース）
const cardWithEvaluation = page
  .getByTestId('listing-card')
  .filter({ has: page.getByTestId('agent-evaluation-overall') })
  .first();
```

#### 4. delete 操作は必ず ID/user_id で限定

```typescript
// ❌ 危険: 他 spec のデータも消す可能性
await supabase.from('agents').delete();
await supabase.from('skills').delete().neq('user_id', SEED_USER_ID); // SEED以外を全削除

// ✅ 安全: 自分が作成したIDだけ削除
await supabase.from('agents').delete().in('id', createdAgentIds);
await supabase.from('skills').delete().eq('user_id', testUser.id);
```

#### 5. flaky の根本対応 vs retry 対応

`playwright.config.ts` の `retries: 1` は**最後の防衛線**であり、それで吸収できる前提でテストを書かない:

- **まず spec 構造（serial mode + isolation）で根本対応**
- どうしても消し切れない並列 dev-server 遅延等のみ retry に任せる
- 修正後は **必ず `--workers=2` の全テスト実行で再現しないことを確認**（単独 spec 実行や `--workers=1` では flaky 再現しないことが多い）

### 検証手順（テスト追加・修正後）

```bash
# 1. DBリセット（実際のコマンドは .stdd.config.yml の commands.db_reset に従う）
<commands.db_reset>

# 2. 全テスト並列実行（flakyの再現条件）。--project は対象 apps[].id を指定
cd e2e && npx playwright test --project=<apps[].id>

# 3. 失敗があれば --workers=1 で再実行し、flaky vs 真の bug を切り分け
cd e2e && npx playwright test --project=<apps[].id> --workers=1
```

`workers=1` で pass するが `workers=2` で fail → 並列干渉のflaky → 上記ルールで対応。
`workers=1` でも fail → 真のbug or テストロジックの問題。

## 複数カードから特定要素を選択

**問題のあるパターン**:

```typescript
// ❌ 悪い例: .first()/.last()で間接的に選択
await page.getByRole('button', { name: '依頼主評価' }).first().click();
// → 最初のボタンが別のカードのボタンかもしれない
```

**推奨される方法**:

```typescript
// ✅ 良い例: data-testidでカードを特定
const projectCard = page.locator('[data-testid="project-card"]').filter({
  hasText: '完了プロジェクト',
});
await projectCard.getByRole('button', { name: '依頼主評価' }).click();
```

## フレーキーテストへの対処

| 原因               | 対策                               |
| ------------------ | ---------------------------------- |
| 不安定なlocator    | アクセシビリティlocatorに変更      |
| ネットワークの遅延 | Web First Assertionsで自動リトライ |
| 固定時間の待機     | 条件ベースの待機に変更             |
| テスト間の依存     | テストを独立させる                 |

**デバッグ方法**:

```bash
npx playwright test --trace on
npx playwright show-report
```

## 認証が必要なテスト

**重要原則**: 新規登録/ログイン導線のテスト以外では、必ず対象アプリのログインヘルパー（例: `loginWithCredentials`）を使用。

```typescript
import {
  test,
  loginWithCredentials,
} from '../../fixtures/<apps[].id>/test-fixtures';

test('認証が必要な機能のテスト', async ({ page, testUser }) => {
  await loginWithCredentials(page, testUser.email, testUser.password);
  // ...
});
```

**例外**: 新規登録機能やログイン機能自体をテストする場合は直接テスト。

---

## E2Eテスト実行（ローカルworktree環境）

devcontainer内のworktree環境でE2Eテストを実行する手順。

### 前提条件

- worktreeが作成済み（`./scripts/create-worktree.sh -b claude/<name> -i <id>`）
- devcontainerが起動済み（`devcontainer up --workspace-folder ... --override-config ...`）

### セットアップ手順

```bash
# 変数定義（IDはworktreeのインスタンスID）
WT_ID=2
WF=/path/to/worktree-$WT_ID
OC=$WF/.devcontainer/devcontainer.override.json

# 1. DBリセット（テストデータ投入）。実際のコマンドは .stdd.config.yml の commands.db_reset に従う
devcontainer exec --workspace-folder $WF --override-config $OC \
  bash -c "cd /workspace/supabase && <commands.db_reset>"

# 2. Playwrightブラウザインストール（chromiumのみで十分）
# ※ e2eの依存パッケージはルートのnpm install（workspaces）で一括インストール済み
devcontainer exec --workspace-folder $WF --override-config $OC \
  bash -c "cd /workspace/e2e && npx playwright install --with-deps chromium"
```

### テスト実行

```bash
# 各アプリの E2Eテスト（--project には対象 apps[].id を指定。apps[] の数だけ繰り返す）
devcontainer exec --workspace-folder $WF --override-config $OC \
  bash -c "cd /workspace/e2e && npx playwright test --project=<apps[].id>"

# 特定テストファイルのみ
devcontainer exec --workspace-folder $WF --override-config $OC \
  bash -c "cd /workspace/e2e && npx playwright test tests/<apps[].id>/login.spec.ts"
```

### 注意事項

- e2e/.env.localはworktree作成スクリプトがポート番号を自動調整済み
- devcontainerの`postStartCommand`で各 `apps[]` は自動起動される（`SKIP_EMAIL_SEND=true` が設定された状態で起動される）
- Supabaseもdevcontainer起動時に自動起動される

---

## E2Eテスト実行（GitHub Actions経由）

Claude Code上でE2Eテストの実行を指示された場合、以下の手順に従う。

### 実行手順

1. **テスト実行用ブランチを作成してpush**

   各アプリについて、対象の `apps[].id`（`.stdd.config.yml`）をブランチ名・ワークフロー名に用いる（apps[] の数だけ繰り返す）。

   ```bash
   # 対象アプリ（<apps[].id>）のE2Eテスト
   git checkout -b claude/execute-<apps[].id>-e2e/[change_name]
   git push -u origin claude/execute-<apps[].id>-e2e/[change_name]
   ```

2. **ワークフローが自動実行される**
   - `claude/execute-<apps[].id>-e2e/**` → `e2e-<apps[].id>.yml`

3. **結果を確認**

   ```bash
   git fetch origin
   git checkout origin/claude/results-e2e/[change_name]/<apps[].id>-{run_id} -- result.json test-output.log
   cat result.json
   cat test-output.log
   ```

4. **結果に応じた対応**
   - **成功**: 作業完了、元のブランチに戻る
   - **失敗**: `test-output.log`で確認し、修正後に再実行

### result.json の構造

```json
{
  "workflow_name": "E2E Tests - <apps[].id>",
  "workflow_run_id": "12345678",
  "test_outcome": "success" | "failure",
  "target_app": "<apps[].id>"
}
```

### 注意事項

- テスト実行には5〜15分程度かかる
- 結果ブランチが作成されるまでポーリングが必要

---

## 参考リンク

- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Locators](https://playwright.dev/docs/locators)
- [Playwright Assertions](https://playwright.dev/docs/test-assertions)
