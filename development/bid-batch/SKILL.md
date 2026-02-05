---
name: bid-batch
description: 배치 입찰 분석 - 다중 공고 일괄 처리
model: opus
trigger: /batch, /bid-batch
---

# 배치 입찰 분석 스킬

> **용도**: 여러 공고를 한번에 분석하여 우선순위 결정
> **모델**: Opus 4.5 (병렬 처리)

---

## 트리거

```bash
/batch [기간] [필터]
/bid-batch --days=7 --action=BID
```

---

## 워크플로우

### 1단계: 대상 공고 수집

```yaml
도구: qetta-core/search_bids
필터:
  - deadline_from: today
  - deadline_to: +7days
  - source: g2b
```

### 2단계: 제품 매칭 (병렬)

```yaml
도구: qetta-core/match_products
각 공고에 대해 병렬 실행
필터: score >= 50
```

### 3단계: 전략 분석 (병렬)

```yaml
도구: qetta-core/get_stofo_prediction
BID/REVIEW 액션 공고만 분석
전략: balanced
```

### 4단계: 우선순위 정렬

```yaml
정렬 기준:
  1. 낙찰확률 (내림차순)
  2. 매칭점수 (내림차순)
  3. 예산규모 (내림차순)
  4. 마감일 (오름차순)
```

### 5단계: 대시보드 리포트

```markdown
## 주간 입찰 배치 분석

### 요약
- 총 분석 공고: {total}건
- BID 권장: {bid_count}건
- REVIEW: {review_count}건
- SKIP: {skip_count}건

### TOP 5 BID 권장 공고

| 순위 | 공고명 | 예산 | 매칭점수 | 낙찰확률 | 마감 |
|------|--------|------|---------|---------|------|
| 1 | {title} | {budget} | {score} | {prob}% | {deadline} |
| 2 | ... | ... | ... | ... | ... |

### 일별 마감 현황

| 날짜 | BID | REVIEW | SKIP |
|------|-----|--------|------|
| 12/30 | 2 | 1 | 3 |
| 12/31 | 1 | 2 | 1 |

### 예상 수주 금액
- 총 예산: {total_budget}억원
- 기대 수주: {expected_win}억원 (낙찰확률 기반)
```

---

## 필터 옵션

```yaml
기간:
  --days=7          # 향후 7일
  --from=2025-01-01 # 시작일
  --to=2025-01-07   # 종료일

액션:
  --action=BID      # BID만
  --action=REVIEW   # REVIEW만
  --action=all      # 전체

예산:
  --min-price=100000000   # 1억 이상
  --max-price=500000000   # 5억 이하

점수:
  --min-score=80    # 매칭점수 80점 이상
  --min-prob=10     # 낙찰확률 10% 이상
```

---

## 사용 예시

```bash
# 이번 주 전체 분석
/batch

# 1억 이상 공고만
/batch --min-price=100000000

# BID 권장 공고만
/batch --action=BID --min-prob=10

# CSV 내보내기
/batch --export=csv
```

---

## 알림 연동

```yaml
슬랙 알림:
  - 높은 기회 공고 즉시 알림
  - 일일 요약 리포트

이메일:
  - 주간 배치 분석 리포트
  - 마감 임박 공고 알림
```

---

*배치 입찰 분석 스킬 v1.0*
