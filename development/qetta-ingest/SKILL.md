---
name: qetta-ingest
description: "V2 데이터 수집 파이프라인 - TED/SAM.gov API 연동, 공고 수집, 정규화, DB 저장. 수집/인제스트/커넥터 관련 작업 시 자동 호출"
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Qetta V2 수집 파이프라인 스킬

> 글로벌 입찰 데이터 수집 자동화

## 트리거 조건

- "수집", "ingest", "sync"
- "TED", "SAM.gov", "커넥터"
- "공고 가져오기", "데이터 수집"

## 파이프라인 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                   Ingest Pipeline                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌───────┐│
│  │  TED    │───▶│Normalize│───▶│Dedup    │───▶│  DB   ││
│  │Connector│    │         │    │(Hash)   │    │ Save  ││
│  └─────────┘    └─────────┘    └─────────┘    └───────┘│
│                                                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌───────┐│
│  │ SAM.gov │───▶│Normalize│───▶│Dedup    │───▶│  DB   ││
│  │Connector│    │         │    │(Hash)   │    │ Save  ││
│  └─────────┘    └─────────┘    └─────────┘    └───────┘│
│                                                          │
│  ┌─────────┐                                             │
│  │G2B Stub │───▶ (테스트용 데이터)                        │
│  └─────────┘                                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 핵심 인터페이스

### NormalizedBid

```typescript
interface NormalizedBid {
  sourceId: 'ted' | 'sam_gov' | 'g2b' | 'g2b_stub';
  sourceNoticeId: string;
  sourceUrl: string | null;

  title: string;
  organization: string | null;
  country: string;  // ISO 3166-1 alpha-2
  region: string | null;

  publishedAt: Date | null;
  deadline: Date | null;

  estimatedPrice: number | null;
  currency: string;

  description: string | null;
  category: string | null;
  keywords: string[];

  contentHash: string;  // SHA-256(title|org|deadline|noticeId)
  rawData: Record<string, unknown>;
}
```

## 구현 체크리스트

### 1. 커넥터 개발

```bash
# TED 커넥터
src/lib/connectors/ted-connector.ts
- [ ] API 인증 설정
- [ ] 검색 쿼리 빌더
- [ ] 응답 파싱
- [ ] 정규화 로직
- [ ] 에러 처리

# SAM.gov 커넥터
src/lib/connectors/sam-connector.ts
- [ ] API 키 발급
- [ ] 검색 파라미터
- [ ] 응답 파싱
- [ ] 정규화 로직
```

### 2. API 샘플 확보 (필수!)

```bash
# TED 샘플 저장
docs/api-samples/ted.sample.json

# SAM 샘플 저장
docs/api-samples/sam.sample.json
```

### 3. 테스트

```bash
# 커넥터 유닛 테스트
npm run test -- src/lib/connectors/

# 통합 테스트
npm run test:e2e -- ingest
```

## 사용 예시

### CLI 명령어

```bash
# 전체 수집
/sync all

# 특정 소스
/sync ted
/sync sam_gov

# 날짜 범위
/sync ted --from 2025-01-01 --to 2025-01-31
```

### 프로그래매틱

```typescript
import { TEDConnector } from '@/lib/connectors/ted-connector';
import { SAMConnector } from '@/lib/connectors/sam-connector';

const ted = new TEDConnector();
const result = await ted.fetch({
  fromDate: new Date('2025-01-01'),
  maxResults: 100,
});

console.log(`수집: ${result.bids.length}건`);
```

## 런타임 요구사항

```typescript
// Node 런타임 필수 (Edge 금지)
export const runtime = 'nodejs';

// crypto 모듈 사용
import { createHash } from 'crypto';
```

## 관련 파일

```
src/lib/connectors/
├── types.ts              # 공통 인터페이스
├── base-connector.ts     # 추상 클래스
├── ted-connector.ts      # TED 커넥터
├── sam-connector.ts      # SAM.gov 커넥터
└── g2b-stub-connector.ts # G2B 스텁

src/app/api/v1/admin/ingest/
└── route.ts              # 수집 API

docs/api-samples/
├── ted.sample.json       # TED 응답 샘플
└── sam.sample.json       # SAM 응답 샘플
```

## 에러 처리

| 에러 | 재시도 | 알림 |
|------|--------|------|
| Rate Limit (429) | 3회 (exponential) | ❌ |
| Timeout | 2회 | ❌ |
| Auth Error (401/403) | 0회 | ✅ |
| Parse Error | 0회 | ✅ (로그) |
| DB Error | 1회 | ✅ |
