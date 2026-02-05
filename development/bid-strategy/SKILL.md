---
name: bid-strategy
description: 입찰 전략 분석 및 최적 투찰가 계산
model: opus
trigger: /strategy, /bid-strategy
---

# 입찰 전략 스킬

> **용도**: 특정 공고에 대한 최적 입찰 전략 수립
> **MCP 연동**: qetta-core, sequential-thinking

---

## 트리거

```bash
/strategy <공고ID> [제품ID] [전략]
/bid-strategy <공고명 검색어>
```

---

## 워크플로우

### 1단계: 공고 정보 수집

```yaml
도구: qetta-core/get_bid_detail
입력: bid_id
출력:
  - 공고명, 발주처
  - 예산 규모
  - 마감 기한
  - 자격 요건
```

### 2단계: 제품 매칭

```yaml
도구: qetta-core/match_products
입력: bid_id, tenant_id
출력:
  - 매칭 점수 (175점 만점)
  - 추천 제품
  - 매칭 키워드
```

### 3단계: 전략 분석

```yaml
도구: qetta-core/get_stofo_prediction
입력:
  - bid_id
  - product_id
  - strategy: balanced (기본)
  - credit_rating: 기업 신용등급

출력:
  - 최적 투찰가
  - 낙찰 확률
  - 적격심사 점수
  - 리스크 레벨
```

### 4단계: 리포트 생성

```markdown
## 입찰 전략 분석 리포트

### 공고 정보
| 항목 | 내용 |
|------|------|
| 공고명 | {title} |
| 발주처 | {organization} |
| 예산 | {estimated_price}원 |
| 마감 | {deadline} |

### 제품 매칭
| 제품 | 점수 | 추천 |
|------|------|------|
| {product} | {score}/175 | {action} |

### 전략 분석

#### 추천: {recommendation}

| 전략 | 투찰가 | 투찰률 | 낙찰확률 |
|------|--------|--------|---------|
| 공격적 | {aggressive}원 | {rate}% | {prob}% |
| 균형형 | {balanced}원 | {rate}% | {prob}% |
| 보수적 | {conservative}원 | {rate}% | {prob}% |

#### 적격심사 점수
- 총점: {total}/95 ({pass})
- 납품실적: {delivery}/25
- 기술능력: {tech}/5
- 신용등급: {credit}/15
- 가격점수: {price}/50

### 리스크 분석
- 리스크 레벨: {risk_level}
- 예상 경쟁업체: {competitors}개사
- 예상 사정률: {assessment_rate}

### 권장사항
{reasoning}
```

---

## 사용 예시

```bash
# 기본 사용
/strategy 7d049fe8-c0a6-4be2-b1cc-e565123b632a

# 제품 지정
/strategy 7d049fe8... 47dbf9b0... balanced

# 키워드 검색
/bid-strategy 서울시 초음파유량계
```

---

## 출력 옵션

```yaml
--json: JSON 형식 출력
--csv: CSV 내보내기
--brief: 요약만 출력
--full: 상세 리포트
```

---

*입찰 전략 스킬 v1.0*
