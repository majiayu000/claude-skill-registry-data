---
name: daily-briefing
description: This skill should be used when the user asks to "오늘 브리핑", "아침 브리핑", "데일리 브리핑", "오늘 메일 확인", "받은 메일 정리", "메일 요약", "오늘 일정 확인", "오늘 스케줄", "캘린더 확인", "오늘 뭐 있어", "오늘 뭐해야 해", "daily briefing", "morning briefing", "check my email", "check my calendar". Make sure to use this skill whenever the user wants to know what's on their plate for the day — it combines Gmail and Google Calendar into one unified briefing. Even partial mentions like "메일" + "일정" together should trigger this skill.
arguments:
  - name: mode
    description: "quick (기본값: 일정+메일 요약만) 또는 detailed (메일 본문 요약 포함)"
    default: "quick"
tools:
  - mcp__claude_ai_Gmail__gmail_search_messages
  - mcp__claude_ai_Gmail__gmail_read_message
  - mcp__claude_ai_Google_Calendar__gcal_list_events
  - mcp__claude_ai_Google_Calendar__gcal_list_calendars
  - Bash
  - Read
---

# Daily Briefing

> Gmail과 Google Calendar를 조회해 오늘의 일정, 주요 메일, 액션 아이템을 하나의 브리핑으로 제공한다.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

사용자가 브리핑을 요청하면 즉시 Step 1부터 실행한다. 추가 질문 없이 바로 데이터를 수집한다.

---

## Workflow

### Step 1: 날짜 확정 및 인증 확인
**Type**: review

1. KST 기준 오늘 날짜를 확인한다.
2. Gmail MCP와 Google Calendar MCP가 연결되어 있는지 확인한다.
   - 연결 확인 방법: `mcp__claude_ai_Gmail__gmail_search_messages`로 테스트 쿼리 실행.
   - **미연결 시**: "Gmail/Calendar MCP가 연결되지 않았습니다. Claude Desktop 설정에서 Gmail과 Google Calendar를 연결한 후 다시 시도해 주세요." 안내 후 종료.
   - **한쪽만 연결된 경우**: 연결된 서비스만으로 부분 브리핑 제공. 미연결 서비스를 명시.

### Step 2: 데이터 수집 (병렬)
**Type**: api_mcp

Gmail과 Calendar를 **동시에** 조회한다. 반드시 병렬로 호출할 것.

#### Gmail 조회
```
mcp__claude_ai_Gmail__gmail_search_messages:
  q: "is:unread newer_than:1d"
  maxResults: 20
```

- 결과가 20건 초과면 중요 메일 우선 필터 추가: `is:unread is:important newer_than:1d`
- 프로모션/소셜 카테고리는 제외: `-category:promotions -category:social`

#### Google Calendar 조회
```
mcp__claude_ai_Google_Calendar__gcal_list_events:
  calendarId: "primary"
  timeMin: "{오늘}T00:00:00"
  timeMax: "{오늘}T23:59:59"
  timeZone: "Asia/Seoul"
  condenseEventDetails: false
```

내일 일정도 함께 조회 (회의 준비 목적):
```
mcp__claude_ai_Google_Calendar__gcal_list_events:
  calendarId: "primary"
  timeMin: "{내일}T00:00:00"
  timeMax: "{내일}T23:59:59"
  timeZone: "Asia/Seoul"
  condenseEventDetails: true
```

### Step 3: 메일 상세 읽기 (선택적)
**Type**: api_mcp

mode가 `detailed`이거나, 메일 제목에 다음 키워드가 포함된 경우 본문을 읽는다:
- "긴급", "urgent", "ASAP", "중요", "확인 요청", "승인", "결재"

```
mcp__claude_ai_Gmail__gmail_read_message:
  messageId: "{해당 메일 ID}"
```

- 최대 5건까지만 본문 읽기 (API 호출 최소화).
- 본문은 200자 이내로 요약. 전문은 사용자 요청 시에만.

### Step 4: 브리핑 합성
**Type**: prompt

수집된 데이터를 아래 형식으로 통합 정리한다.

```
## {오늘 날짜} ({요일}) 데일리 브리핑

### 오늘 일정 (N건)
- HH:MM ~ HH:MM  일정명 (장소/참석자)
- HH:MM ~ HH:MM  일정명
- (일정 없음 → "오늘 등록된 일정이 없습니다.")

### 주요 메일 (N건 미확인)
| 발신자 | 제목 | 수신 시각 | 비고 |
|--------|------|----------|------|
| 홍길동 | 원재료 납기 지연 건 | 08:30 | 확인 필요 |
| ... | ... | ... | ... |
- (미확인 메일 없음 → "새 메일이 없습니다.")
- 20건 초과 시: "총 N건 중 주요 M건만 표시"

### 오늘 체크리스트
- [ ] {메일에서 추출한 액션 아이템}
- [ ] {일정 기반 준비 사항}
- (금요일이면) [ ] 생산회의 PPT 준비

### 내일 예고
- HH:MM  일정명 (간략히)
- (없으면 생략)
```

**합성 규칙:**
- 시간은 모두 KST 표기.
- 금요일 감지 시 "생산회의 PPT 준비" 체크리스트 자동 추가.
- 메일에서 "확인", "요청", "승인" 등 액션 키워드가 있으면 체크리스트에 반영.
- 숫자 출처 명시: (Gmail 조회 결과), (Calendar 조회 결과).

### Step 5: 출력
**Type**: generate

합성된 브리핑을 사용자에게 제시한다.

- quick 모드: Step 4 형식 그대로 출력.
- detailed 모드: 주요 메일 섹션에 본문 요약(200자) 추가.

---

## Edge Cases

| 상황 | 처리 |
|------|------|
| MCP 미연결 | 안내 메시지 후 종료. 부분 연결 시 가능한 서비스만 브리핑 |
| 메일 0건 | "새 메일이 없습니다" 명시, 일정 브리핑은 계속 진행 |
| 일정 0건 | "오늘 등록된 일정이 없습니다" 명시, 메일 브리핑은 계속 진행 |
| 메일 50건 초과 | 중요/미읽음 우선 상위 20건만, 나머지는 건수만 보고 |
| 메일 본문 과다 | 제목+발신자+200자 요약만 표시 |
| 주말/공휴일 | "오늘은 주말입니다" 안내 후 브리핑 계속 (메일은 있을 수 있으므로) |
| MCP 타임아웃 | 실패한 소스 명시, 나머지로 부분 브리핑 |

---

## Constraints (하드 제약)

- 메일 자동 답장/전달 **금지**
- 일정 생성/수정/삭제 **금지**
- 메일 본문을 파일로 저장 **금지** (개인정보)
- 읽기 전용 스킬 — 외부 상태 변경 일절 없음
- 사용자 승인 없이 외부 액션 금지

---

## Integration Points

- **daily-note**: 브리핑 결과를 `memory/daily/YYYY-MM-DD.md`에 기록하고 싶으면 사용자에게 제안
- **SessionStart**: 세션 시작 시 자동 브리핑 옵션 (향후 확장)
- **data-analyst**: 메일/일정 패턴 분석이 필요하면 연계
