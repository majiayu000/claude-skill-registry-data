---
name: google-search-console
description: Google Search Console API 통합 스킬. 검색 성과 분석, URL 검사, 사이트맵 관리, 사이트 인증 지원. "GSC", "서치콘솔", "검색 성과", "SEO 분석" 키워드로 활성화.
trigger-keywords: google search console, gsc, search console, 구글 서치콘솔, 서치콘솔, 검색 성과, 검색 분석, seo 분석, url 검사, 색인 상태, sitemap, 사이트맵
allowed-tools: Read, Write, Edit, Bash
---

# Google Search Console Skill

## Overview

Google Search Console API를 통합한 포괄적인 SEO 분석 스킬입니다.
검색 성과 분석, URL 인덱싱 상태 확인, 사이트맵 관리, 사이트 인증 기능을 제공합니다.

## When to Use

**명시적 요청:**
- "검색 성과 분석해줘"
- "URL 인덱싱 상태 확인해줘"
- "사이트맵 제출해줘"
- "CTR과 노출수 보여줘"

**자동 활성화 키워드:**

- User mentions "Google Search Console", "GSC", "서치콘솔"
- User asks about search performance, clicks, impressions, CTR
- User needs URL indexing status or inspection
- User wants to manage sitemaps
- User asks "검색 성과", "색인 상태", "검색 순위"
- User needs SEO analytics data from Google

## Features

### 1. **Search Analytics** ⭐
- Query search performance data (clicks, impressions, CTR, position)
- Filter by date range, page, query, country, device
- Group by dimensions (query, page, country, device, date)
- Compare time periods
- Export to CSV/JSON

### 2. **URL Inspection**
- Check indexing status of specific URLs
- View crawl information
- Check mobile usability
- Identify indexing issues
- Request indexing for URLs

### 3. **Sitemap Management**
- List all sitemaps for a site
- Submit new sitemaps
- Delete sitemaps
- Check sitemap status and errors

### 4. **Site Management**
- List all verified sites
- Add new sites
- Remove sites
- Check verification status

## Environment Variables

This skill uses environment variables managed by `jelly-dotenv`. See `skills/jelly-dotenv/SKILL.md` for configuration details.

### Option 1: Service Account (Recommended)

```bash
# Service account JSON key file path
GOOGLE_SERVICE_ACCOUNT_KEY_FILE=/path/to/service-account.json

# Or inline JSON (for CI/CD environments)
GOOGLE_SERVICE_ACCOUNT_KEY_JSON='{"type":"service_account","project_id":"...","private_key":"..."}'
```

### Option 2: OAuth 2.0 Client Credentials

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token
```

### Common Settings

```bash
# Default site URL (optional, can be specified per request)
GOOGLE_SEARCH_CONSOLE_SITE_URL=https://your-site.com

# Alternative naming patterns (auto-detected)
GSC_SITE_URL=https://your-site.com
SEARCH_CONSOLE_SITE=sc-domain:your-site.com
```

Variables can be configured in either:
- `skills/jelly-dotenv/.env` (skill-common, highest priority)
- Project root `/.env` (project-specific, fallback)

## Configuration

### Setting Up Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Google Search Console API"
4. Create a Service Account:
   - Go to IAM & Admin → Service Accounts
   - Create service account
   - Download JSON key file
5. Add service account email to Search Console:
   - Go to [Search Console](https://search.google.com/search-console)
   - Settings → Users and permissions
   - Add user with service account email
   - Grant "Full" or "Restricted" access

### Setting Up OAuth 2.0

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials (Web application)
3. Set authorized redirect URI
4. Use OAuth playground or your app to get refresh token
5. Required scope: `https://www.googleapis.com/auth/webmasters.readonly`

## Usage Scenarios

### Scenario 1: Search Performance Overview

**User Request**: "Show me search performance for the last 7 days"

**Skill Actions**:
1. Load credentials from environment
2. Query Search Analytics API with date range
3. Aggregate clicks, impressions, CTR, position
4. Format as Markdown table with trends

**Output**:
```markdown
## Search Performance (Last 7 Days)

| Metric | Value | Change |
|--------|-------|--------|
| Clicks | 1,234 | +12% |
| Impressions | 45,678 | +8% |
| CTR | 2.7% | +0.3% |
| Avg Position | 15.2 | -2.1 |

### Top Queries
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| keyword 1 | 234 | 5,678 | 4.1% | 8.5 |
| keyword 2 | 189 | 4,321 | 4.4% | 12.3 |
```

### Scenario 2: URL Inspection

**User Request**: "Check indexing status for https://example.com/page"

**Skill Actions**:
1. Call URL Inspection API
2. Parse indexing result
3. Check coverage status
4. Display mobile usability

**Output**:
```markdown
## URL Inspection: https://example.com/page

| Property | Status |
|----------|--------|
| Index Status | ✅ Indexed |
| Crawled | 2024-01-15 |
| Canonical | https://example.com/page |
| Mobile Usability | ✅ Mobile friendly |
| Rich Results | ⚠️ 2 warnings |
```

### Scenario 3: Sitemap Management

**User Request**: "Show all sitemaps and submit a new one"

**Skill Actions**:
1. List existing sitemaps
2. Show status and last submitted date
3. Submit new sitemap URL
4. Confirm submission

### Scenario 4: Top Pages Analysis

**User Request**: "What are my top performing pages?"

**Skill Actions**:
1. Query Search Analytics grouped by page
2. Sort by clicks
3. Include impressions, CTR, position
4. Highlight pages with high impressions but low CTR

## API Reference

### Search Analytics Query

```typescript
interface SearchAnalyticsRequest {
  startDate: string;      // YYYY-MM-DD
  endDate: string;        // YYYY-MM-DD
  dimensions?: ('query' | 'page' | 'country' | 'device' | 'date')[];
  searchType?: 'web' | 'image' | 'video' | 'news';
  dimensionFilterGroups?: FilterGroup[];
  aggregationType?: 'auto' | 'byPage' | 'byProperty';
  rowLimit?: number;      // Max 25000
  startRow?: number;
}
```

### URL Inspection

```typescript
interface UrlInspectionRequest {
  inspectionUrl: string;
  siteUrl: string;
  languageCode?: string;
}
```

### Sitemap Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List | GET | `/webmasters/v3/sites/{siteUrl}/sitemaps` |
| Get | GET | `/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` |
| Submit | PUT | `/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` |
| Delete | DELETE | `/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` |

## Output Formats

### Markdown (Default)
- Formatted tables with metrics
- Trend indicators (↑↓)
- Status icons (✅⚠️❌)
- Summary insights

### JSON
- Raw API response
- Full data structure
- Programmatic access

### CSV
- Spreadsheet-compatible export
- All data rows
- For further analysis

## Error Handling

### Authentication Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Check service account key or OAuth tokens |
| 403 Forbidden | No access to site | Add service account to Search Console |
| Invalid scope | Wrong OAuth scope | Use `webmasters.readonly` scope |

### API Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | Site not in Search Console | Add site to Search Console first |
| 400 Bad Request | Invalid parameters | Check date format (YYYY-MM-DD) |
| 429 Rate Limit | Too many requests | Wait and retry with backoff |

### Common Issues

**"Configuration error: No Google credentials found"**
```bash
# Solution: Add credentials to .env
GOOGLE_SERVICE_ACCOUNT_KEY_FILE=/path/to/key.json
```

**"Site not found or no access"**
```bash
# Solution: Add service account email to Search Console
# Go to: Search Console → Settings → Users and permissions
```

**"Invalid date range"**
```bash
# Solution: Use YYYY-MM-DD format, max 16 months historical data
```

## Security Policy

### Authentication
- **Service Account**: Recommended for server-side usage
- **OAuth 2.0**: For user-authenticated requests
- **Credentials**: Loaded from environment variables only
- **Logging**: Private keys and tokens automatically redacted

### Data Access
- **Read-Only by Default**: Uses `webmasters.readonly` scope
- **Write Operations**: Sitemap submit/delete requires full scope
- **Site-Scoped**: Access limited to authorized sites only

### Rate Limiting
- **Automatic**: Respects Google API quotas
- **Retry**: Exponential backoff on 429 errors
- **Daily Quota**: 1,200 queries per day (default)

## Limitations

- **Historical Data**: Maximum 16 months of search data
- **Data Freshness**: 2-3 day delay for search analytics
- **URL Inspection**: 2,000 requests per day per site
- **Row Limit**: Maximum 25,000 rows per query
- **Dimensions**: Maximum 3 dimensions per query

## Integration with Claude Code

This skill activates automatically when users mention:
- "google search console", "gsc", "서치콘솔"
- "search performance", "검색 성과"
- "url inspection", "색인 상태"
- "sitemap", "사이트맵"
- "seo analytics", "검색 분석"

The skill will:
1. Load Google credentials from .env
2. Execute the requested query/operation
3. Format results as Markdown tables
4. Provide actionable insights and recommendations

## References

- [Google Search Console API Documentation](https://developers.google.com/webmaster-tools)
- [Search Analytics API Reference](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [URL Inspection API Reference](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)
- [OAuth 2.0 Setup](https://developers.google.com/webmaster-tools/v1/how-tos/authorizing)
- [API Quotas and Limits](https://developers.google.com/webmaster-tools/limits)

---

## Workflow

### Step 1: 인증 확인

```bash
# 서비스 계정 키 파일 확인
ls -la $GOOGLE_SERVICE_ACCOUNT_KEY_FILE

# 또는 환경변수 확인
echo $GOOGLE_CLIENT_ID
```

### Step 2: 작업 유형별 분기

**검색 성과 분석:**
1. 날짜 범위 결정 (기본: 최근 7일)
2. Search Analytics API 호출
3. 결과를 마크다운 테이블로 포맷

**URL 검사:**
1. 대상 URL 확인
2. URL Inspection API 호출
3. 인덱싱 상태 및 문제점 보고

**사이트맵 관리:**
1. 기존 사이트맵 목록 조회
2. 새 사이트맵 제출 또는 삭제
3. 상태 확인

---

## Examples

### 예시 1: 검색 성과 조회

```
사용자: "지난 7일간 검색 성과 보여줘"

Claude: Google Search Console에서 검색 성과를 조회합니다.

→ 검색 성과 (Last 7 Days):
| Metric | Value | Change |
|--------|-------|--------|
| Clicks | 1,234 | +12% |
| Impressions | 45,678 | +8% |
| CTR | 2.7% | +0.3% |
| Avg Position | 15.2 | -2.1 |
```

### 예시 2: URL 인덱싱 상태 확인

```
사용자: "/blog/my-post URL 인덱싱 상태 확인해줘"

Claude: URL Inspection API를 호출합니다.

→ URL 검사 결과: https://example.com/blog/my-post
| 항목 | 상태 |
|------|------|
| Index Status | Indexed |
| Crawled | 2025-01-10 |
| Mobile Usability | Mobile friendly |
```

### 예시 3: 상위 쿼리 분석

```
사용자: "어떤 검색어로 가장 많이 유입되고 있어?"

Claude: 상위 검색어를 분석합니다.

→ Top Queries:
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| react tutorial | 234 | 5,678 | 4.1% | 8.5 |
| typescript guide | 189 | 4,321 | 4.4% | 12.3 |
```

---

## Best Practices

**DO:**
- 서비스 계정 이메일을 Search Console에 추가
- 날짜 범위는 최대 16개월까지만 조회 가능
- 대량 쿼리 시 rowLimit 파라미터 활용
- 정기적으로 사이트맵 상태 확인
- API 응답을 캐싱하여 쿼터 절약

**DON'T:**
- API 키를 코드에 하드코딩하지 않기
- 일일 쿼터(1,200) 초과하지 않기
- 2-3일 이내 데이터 기대하지 않기 (지연 있음)
- 쿼리당 3개 이상 dimension 사용하지 않기
- 25,000행 이상 단일 쿼리로 요청하지 않기

---

## Troubleshooting

### 403 Forbidden
- 서비스 계정이 Search Console에 추가되었는지 확인
- Search Console → Settings → Users and permissions

### 404 Site Not Found
- 사이트가 Search Console에 등록되었는지 확인
- 사이트 URL 형식 확인 (https://, sc-domain:)

### Invalid Date Range
- 날짜 형식: YYYY-MM-DD
- 최대 16개월 이전까지만 조회 가능
