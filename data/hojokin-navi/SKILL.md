---
name: hojokin-navi
description: |
  補助金ナビ開発スキル。JグランツAPI連携、Supabase操作、補助金データ処理のベストプラクティス。
  使用タイミング: (1) JグランツAPIからデータ取得 (2) 補助金データのDB保存・検索 (3) HTMLフィールドの処理 (4) Slack通知実装
---

# 補助金ナビ開発スキル

## JグランツAPI

### エンドポイント

```
BASE_URL = https://api.jgrants-portal.go.jp/exp/v1/public
```

| エンドポイント | 用途 |
|---------------|------|
| `/subsidies` | 一覧取得（検索） |
| `/subsidies/id/{id}` | 詳細取得 |

### 一覧取得

```typescript
// 募集中の補助金を取得
const request = {
  acceptance: 1,        // 1=募集中, 0=全て
  keyword: "IT",        // オプション
  area: "東京都",       // オプション
};

const url = `${BASE_URL}/subsidies?request=${encodeURIComponent(JSON.stringify(request))}`;
const res = await fetch(url);
const { result, metadata } = await res.json();
// result: JGrantsSubsidy[]
// metadata.resultset.count: 総件数
```

### 詳細取得

```typescript
const res = await fetch(`${BASE_URL}/subsidies/id/${jgrantsId}`);
const { result } = await res.json();
const subsidy = result[0]; // 単一オブジェクト
```

### レスポンス型定義

```typescript
type JGrantsSubsidy = {
  id: string;                          // "a0WJ200000CDWaWMAX"
  name: string;                        // "S-00007689"
  title: string;
  subsidy_catch_phrase?: string;
  detail?: string;                     // ⚠️ HTML含む
  target_area_search?: string;
  target_area_detail?: string;
  industry?: string;                   // ⚠️ "/"区切り
  use_purpose?: string;
  subsidy_max_limit?: number;
  subsidy_rate?: string;
  target_number_of_employees?: string;
  acceptance_start_datetime?: string;
  acceptance_end_datetime?: string;
  front_subsidy_detail_page_url?: string;
  application_guidelines?: Array<{     // ⚠️ 大容量
    name: string;
    data: string;  // base64
  }>;
};
```

## データ変換

### 業種パース

```typescript
// "製造業/建設業/情報通信業" → ["製造業", "建設業", "情報通信業"]
function parseIndustry(industry?: string): string[] {
  if (!industry) return [];
  return industry.split('/').map(s => s.trim()).filter(Boolean);
}
```

### HTMLサニタイズ

```typescript
import DOMPurify from 'isomorphic-dompurify';

function sanitizeHtml(html?: string): string {
  if (!html) return '';
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a'],
    ALLOWED_ATTR: ['href', 'target'],
  });
}
```

### DB保存用変換

```typescript
function toDbSubsidy(api: JGrantsSubsidy) {
  return {
    jgrants_id: api.id,
    name: api.name,
    title: api.title,
    catch_phrase: api.subsidy_catch_phrase,
    description: sanitizeHtml(api.detail),
    target_area: api.target_area_search ? [api.target_area_search] : [],
    target_area_detail: api.target_area_detail,
    industry: parseIndustry(api.industry),
    use_purpose: api.use_purpose,
    max_amount: api.subsidy_max_limit,
    subsidy_rate: api.subsidy_rate,
    start_date: api.acceptance_start_datetime,
    end_date: api.acceptance_end_datetime,
    front_url: api.front_subsidy_detail_page_url,
    is_active: true,
    updated_at: new Date().toISOString(),
  };
}
```

## Supabase操作

### Upsert（作成 or 更新）

```typescript
const { error } = await supabase
  .from('subsidies')
  .upsert(toDbSubsidy(apiData), {
    onConflict: 'jgrants_id',
  });
```

### 検索クエリ

```typescript
// 基本検索
let query = supabase
  .from('subsidies')
  .select('*')
  .eq('is_active', true)
  .order('end_date', { ascending: true });

// キーワード検索（ILIKE）
if (keyword) {
  query = query.or(`title.ilike.%${keyword}%,description.ilike.%${keyword}%`);
}

// 地域フィルター
if (area) {
  query = query.contains('target_area', [area]);
}

// 業種フィルター（JSONB配列）
if (industry) {
  query = query.contains('industry', [industry]);
}

// 金額フィルター
if (maxAmount) {
  query = query.lte('max_amount', maxAmount);
}

// ページネーション
const { data, count } = await query
  .range(offset, offset + limit - 1)
  .select('*', { count: 'exact' });
```

## Slack通知

### Webhook送信

```typescript
async function sendSlackNotification(message: string, blocks?: any[]) {
  await fetch(process.env.SLACK_WEBHOOK_URL!, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: message,
      blocks,
    }),
  });
}
```

### 新着補助金通知テンプレート

```typescript
const blocks = [
  {
    type: 'header',
    text: { type: 'plain_text', text: '🆕 新着補助金' },
  },
  {
    type: 'section',
    text: {
      type: 'mrkdwn',
      text: `*${subsidy.title}*\n${subsidy.catch_phrase || ''}`,
    },
  },
  {
    type: 'section',
    fields: [
      { type: 'mrkdwn', text: `*上限額:* ${formatCurrency(subsidy.max_amount)}` },
      { type: 'mrkdwn', text: `*締切:* ${formatDate(subsidy.end_date)}` },
    ],
  },
  {
    type: 'actions',
    elements: [{
      type: 'button',
      text: { type: 'plain_text', text: '詳細を見る' },
      url: `${APP_URL}/subsidies/${subsidy.id}`,
    }],
  },
];
```

## バッチ処理

### データ同期フロー

```
1. JグランツAPI一覧取得（acceptance=1）
2. 各補助金の詳細取得（並列、rate limit考慮）
3. データ変換（業種パース、HTMLサニタイズ）
4. Supabase Upsert
5. 新規追加分をSlack通知
6. 募集終了分のis_active更新
```

### Vercel Cron設定

```json
// vercel.json
{
  "crons": [{
    "path": "/api/cron/sync-subsidies",
    "schedule": "0 3 * * 1"  // 毎週月曜3時
  }]
}
```

## ユーティリティ

### 金額フォーマット

```typescript
function formatCurrency(amount?: number): string {
  if (!amount) return '金額未定';
  if (amount >= 100000000) return `${(amount / 100000000).toFixed(1)}億円`;
  if (amount >= 10000) return `${(amount / 10000).toFixed(0)}万円`;
  return `${amount.toLocaleString()}円`;
}
```

### 残り日数計算

```typescript
function getDaysRemaining(endDate?: string): number | null {
  if (!endDate) return null;
  const end = new Date(endDate);
  const now = new Date();
  const diff = end.getTime() - now.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}
```

### 締切ステータス

```typescript
function getDeadlineStatus(days: number | null): 'urgent' | 'soon' | 'normal' | 'closed' {
  if (days === null) return 'normal';
  if (days < 0) return 'closed';
  if (days <= 7) return 'urgent';
  if (days <= 30) return 'soon';
  return 'normal';
}
```

## 注意事項

1. **APIレート**: 公式制限なしだが、並列リクエストは5件程度に抑える
2. **PDF**: `application_guidelines`は保存しない（数MB/件）
3. **文字コード**: APIはUTF-8、特殊文字エスケープ済み
4. **日付**: ISO 8601形式、タイムゾーンはJST想定
5. **NULL処理**: オプショナルフィールドは全てnull許容
