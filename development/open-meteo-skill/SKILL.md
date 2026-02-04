---
name: open-meteo-skill
description: |
  전세계 날씨 API Open-Meteo 스킬. 무료 오픈소스 날씨 API로 16일 예보, 80년 역사 데이터, 대기질, 해양 날씨 등 제공.
  사용 시점: (1) 날씨 예보 조회 (2) 과거 날씨 데이터 조회 (3) 대기질/미세먼지 조회 (4) 해양 날씨/파도 정보 (5) 위치 좌표 검색 (6) 고도 정보 조회
  키워드: 날씨, weather, 기온, 강수량, 습도, 풍속, 미세먼지, PM2.5, 파도, 일출, 일몰, geocoding
---

# Open-Meteo API 스킬

전 세계 국가 기상청 데이터를 통합한 무료 오픈소스 날씨 API.

## 핵심 특징

- **무료 & API 키 불필요**: 비상업적 사용 무료, 즉시 사용 가능
- **빠른 응답**: 10ms 이하 응답 시간
- **다양한 데이터**: 16일 예보, 80년 역사 데이터, 대기질, 해양 날씨
- **라이선스**: 데이터 CC BY 4.0, 코드 AGPLv3

## 기본 API 호출

```bash
# 날씨 예보 (서울)
curl "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation&daily=temperature_2m_max,temperature_2m_min&timezone=Asia/Seoul"
```

## 주요 엔드포인트

| 엔드포인트 | URL | 용도 |
|-----------|-----|------|
| Forecast | api.open-meteo.com/v1/forecast | 날씨 예보 |
| Archive | archive-api.open-meteo.com/v1/archive | 과거 데이터 |
| Air Quality | air-quality-api.open-meteo.com/v1/air-quality | 대기질 |
| Marine | marine-api.open-meteo.com/v1/marine | 해양 날씨 |
| Geocoding | geocoding-api.open-meteo.com/v1/search | 위치 검색 |
| Elevation | api.open-meteo.com/v1/elevation | 고도 조회 |

## 필수 파라미터

- `latitude`: 위도 (-90 ~ 90)
- `longitude`: 경도 (-180 ~ 180)

## 상세 문서

- **API 상세 명세**: [references/api-spec.md](references/api-spec.md)
- **MCP 서버 가이드**: [references/mcp-guide.md](references/mcp-guide.md)
- **날씨 변수 목록**: [references/weather-variables.md](references/weather-variables.md)

## 테스트 스크립트

```bash
# 테스트 실행
./scripts/test-forecast.sh          # 날씨 예보 테스트
./scripts/test-air-quality.sh       # 대기질 테스트
./scripts/test-geocoding.sh         # 지오코딩 테스트
./scripts/test-all.sh               # 전체 테스트
```

## 공식 레퍼런스

- [Open-Meteo 공식 문서](https://open-meteo.com/en/docs)
- [Open-Meteo GitHub](https://github.com/open-meteo/open-meteo)
- [Open-Meteo MCP GitHub](https://github.com/cmer81/open-meteo-mcp)
