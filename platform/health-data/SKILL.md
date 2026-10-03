---
name: health-data
description: >
  Health Connect(Android)와 HealthKit(iOS) 건강 데이터 수집/동기화/저장 종합 가이드.
  React Native(Expo), Swift, Kotlin, Web 환경에서의 구현 패턴과 실전 gotcha 포함.
  Health Connect, HealthKit, 헬스커넥트, 헬스킷, 심박수, 수면, 걸음 수, 건강 데이터,
  health sync, 백그라운드 동기화 요청에 사용한다.
---

# Health Data Integration Guide

Health Connect(Android)와 HealthKit(iOS)를 활용한 건강 데이터 수집/동기화/저장 종합 가이드.
React Native(Expo), Swift, Kotlin, Web 환경에서의 구현 패턴과 실전 gotcha 포함.
심박수, 수면, 걸음, 활동 에너지 등 주요 데이터 타입별 처리법.

## Trigger

다음 키워드에 자동 활성화:
- "Health Connect", "HealthKit", "헬스커넥트", "헬스킷"
- "심박수", "수면 데이터", "걸음 수", "heart rate", "sleep data", "steps"
- "건강 데이터 동기화", "health sync", "백그라운드 동기화"
- "HKAnchoredObjectQuery", "getChanges", "health permission"

---

## 핵심 개념: 건강 데이터는 "내 데이터"가 아니다

> 건강 데이터의 가장 큰 함정: **우리 앱이 데이터의 주인이 아니다.**

Health Connect/HealthKit은 OS가 관리하는 **공유 저장소**입니다.
다른 앱이 데이터를 쓸 수 있고, 사용자가 직접 삭제할 수도 있습니다.

```
[워치/센서] → [Health Connect / HealthKit] → [우리 앱] → [백엔드 서버] → [DB]
               ↑ 다른 앱도 읽기/쓰기      ↑ 여기서부터 우리 책임
               ↑ 사용자가 직접 삭제 가능
```

**이것이 의미하는 것:**
- 데이터가 갑자기 사라질 수 있다 (사용자 삭제, 앱 제거)
- 같은 시간대에 다른 앱이 쓴 중복 데이터가 있을 수 있다
- 권한이 언제든 취소될 수 있다
- **증분 동기화(incremental sync)**가 필수 — 매번 전체를 다시 읽으면 비용 폭발

---

## 상세 내용

이 스킬의 전체 내용(플랫폼 비교, 데이터 타입별 처리, 동기화 아키텍처, 권한 관리, 삭제 전파, 로컬 캐시, 워치 연동, 디버깅 가이드)은 글로벌 설치본을 참조하세요.

핵심 gotcha 요약:
- Health Connect `DeletionChange`에 recordType 없음 → 데이터 타입별 별도 token 유지
- iOS `authorizationStatus()`는 read 권한을 정확히 알려주지 않음
- 심박수 raw 저장 시 파티셔닝 필수 (월 수만 row)
- 수면 `sleepDate` 단위 upsert → 낮잠+밤잠 덮어쓰기 위험
- 걸음 수 `user+date` upsert → 워치+폰 데이터 덮어쓰기 위험 (deviceId 포함 필요)
- 로그아웃 시 pending buffer 미삭제 → 다른 사용자 데이터 업로드 위험
- Observer Query + Background Delivery 함께 사용 필수 (iOS)
- 동시 sync 방지: shared promise 패턴

## Related Files

| 파일 | 역할 |
|------|------|
| `skills/social-login/SKILL.md` | 소셜 로그인 (앱 인증과 함께 사용) |
| `skills/database-schema-designer/SKILL.md` | DB 스키마 설계 (파티셔닝 포함) |
| 네이티브 백엔드 작업자 | 프로젝트 Spring/JPA 버전·기존 persistence 경계·파티셔닝 테스트를 기준으로 구현 |
| `skills/python-backend-fastapi/SKILL.md` | FastAPI 백엔드 |
