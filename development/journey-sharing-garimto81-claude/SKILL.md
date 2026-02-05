---
name: journey-sharing
description: >
  세션 여정 자동 기록 및 PR 연동. 작업 흐름, 의사결정, 컨텍스트 사용량 추적.
version: 2.0.0

triggers:
  keywords:
    - "여정 저장"
    - "journey"
    - "세션 기록"
    - "PR 여정"
  file_patterns: []
  context:
    - "세션 기록 저장"
    - "PR 여정 첨부"

capabilities:
  - record_milestone
  - export_journey
  - track_context_usage

model_preference: haiku

phase: [4]
auto_trigger: true
dependencies: []
token_budget: 300
---

# Journey Sharing Skill

세션 작업 여정을 자동으로 기록하고 PR에 첨부하는 워크플로우입니다.

## 자동 트리거 조건

다음 키워드 감지 시 자동 활성화:

- "여정 저장", "journey save"
- "세션 기록", "session log"
- "PR 여정", "journey export"

## 수집 데이터

| 항목 | 수집 시점 |
|------|----------|
| 마일스톤 | 주요 작업 완료 시 |
| 의사결정 | 선택지 제시/선택 시 |
| 파일 변경 | git diff 기반 |
| 컨텍스트 사용량 | 주기적 체크 |
| 장애물 | 에러/실패 발생 시 |

## 워크플로우

```
세션 시작
    ↓
[자동 기록] milestones, decisions
    ↓
/journey save (세션 종료 시)
    ↓
/create pr → 여정 섹션 자동 포함
    ↓
리뷰어가 컨텍스트 확인
```

## PR 여정 섹션 예시

```markdown
## 여정 (Journey)

### 작업 흐름
1. 14:00 - 이슈 분석 시작
2. 14:15 - 기존 코드 탐색 (context: 15%)
3. 14:30 - 구현 방향 결정
4. 15:00 - 코드 작성 완료 (context: 45%)
5. 15:20 - 테스트 통과 확인

### 주요 결정
- **구현 방식**: Option A 선택 (이유: 기존 패턴과 일관성)
- **테스트 범위**: Unit + Integration (E2E는 별도 PR)

### 변경 파일 (5개)
- `src/feature.py` - 핵심 로직
- `tests/test_feature.py` - 테스트
- `docs/FEATURE.md` - 문서

### 참고사항
- 장애물: 타입 에러 1건 (해결됨)
- 컨텍스트 최대 사용: 45%
```

## 설정

`.claude/settings.local.json`:

```json
{
  "journey": {
    "auto_save": true,
    "include_context_usage": true,
    "max_milestones": 20
  }
}
```

## 관련 커맨드

| 커맨드 | 용도 |
|--------|------|
| `/journey save` | 세션 저장 |
| `/journey export` | PR용 마크다운 생성 |
| `/create pr` | PR 생성 (여정 포함) |

---

> 참조: `.claude/commands/journey.md`
