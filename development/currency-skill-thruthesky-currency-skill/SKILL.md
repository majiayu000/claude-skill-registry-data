---
name: currency-skill
description: |
  Frankfurter API를 사용한 환율 정보 조회 스킬. 무료 오픈소스 환율 API로 유럽중앙은행(ECB) 데이터 기반.
  사용 시점: (1) 환율 정보 조회, (2) 통화 변환 기능 구현, (3) 환율 시계열 데이터 필요, (4) 지원 통화 목록 확인
---

# Frankfurter Currency Exchange API

무료 오픈소스 환율 API. API 키 불필요, 사용량 제한 없음.

## Base URL

```
https://api.frankfurter.dev/v1
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/latest` | 최신 환율 |
| `/{YYYY-MM-DD}` | 특정 날짜 환율 |
| `/{start}..{end}` | 기간별 시계열 |
| `/currencies` | 지원 통화 목록 |

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `base` | 기준 통화 코드 | EUR |
| `symbols` | 대상 통화 (쉼표 구분) | 전체 |
| `amount` | 변환할 금액 | 1 |

## Examples

### Latest Rates

```bash
# EUR 기준 전체 통화
curl "https://api.frankfurter.dev/v1/latest"

# USD 기준 KRW, PHP 환율
curl "https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW,PHP"

# 100 USD를 KRW로 변환
curl "https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW&amount=100"
```

### Historical Rates

```bash
# 특정 날짜
curl "https://api.frankfurter.dev/v1/2024-01-15?base=USD&symbols=KRW"

# 기간별 시계열
curl "https://api.frankfurter.dev/v1/2024-01-01..2024-01-31?base=USD&symbols=KRW"
```

### Currencies List

```bash
curl "https://api.frankfurter.dev/v1/currencies"
```

## Response Format

### Latest/Historical

```json
{
  "amount": 1,
  "base": "USD",
  "date": "2024-01-15",
  "rates": {
    "KRW": 1350.50,
    "PHP": 56.20
  }
}
```

### Time Series

```json
{
  "amount": 1,
  "base": "USD",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "rates": {
    "2024-01-01": {"KRW": 1340.00},
    "2024-01-02": {"KRW": 1342.50},
    ...
  }
}
```

### Currencies

```json
{
  "AUD": "Australian Dollar",
  "BGN": "Bulgarian Lev",
  "KRW": "South Korean Won",
  "PHP": "Philippine Peso",
  "USD": "United States Dollar",
  ...
}
```

## Supported Currencies

AUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, EUR, GBP, HKD, HUF, IDR, ILS, INR, ISK, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, SEK, SGD, THB, TRY, USD, ZAR

## Notes

- 데이터 출처: 유럽중앙은행(ECB)
- 업데이트: 매일 16:00 CET
- 시간대: UTC 기준 저장
- 주말/휴일: 마지막 영업일 환율 반환

## Test Scripts

API 테스트용 스크립트:

```bash
# 모든 테스트 실행
./scripts/test_frankfurter.sh

# Dart 테스트 실행
dart run scripts/test_frankfurter.dart
```
