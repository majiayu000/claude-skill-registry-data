---
name: meeting-brief
description: This skill should be used when the user asks to "회의 준비해줘", "회의 브리핑", "미팅 전 정리해줘", "오늘 회의 뭐 챙겨야 해", "회의 안건 정리", "메일이랑 일정 정리해줘", "회의 전 확인할 거", "meeting brief", "pre-meeting summary", "prepare for meeting". Make sure to use this skill whenever the user wants to prepare for an upcoming meeting by cross-analyzing Gmail and Calendar. Even if the user just says "회의 준비" or mentions a specific meeting name, this skill should trigger. This is different from daily-briefing — this skill focuses on a SPECIFIC meeting and produces actionable agenda items, not a general day overview.
arguments:
  - name: meeting
    description: "특정 회의명 지정 (미지정 시 오늘 가장 임박한 회의 자동 선택)"
    default: ""
tools:
  - mcp__claude_ai_Gmail__gmail_search_messages
  - mcp__claude_ai_Gmail__gmail_read_message
  - mcp__claude_ai_Google_Calendar__gcal_list_events
  - Read
  - Glob
  - Grep
---

# Meeting Brief

> 회의 전 Gmail + Calendar를 교차 분석해 "결론 먼저, 짧고 실무적인" 사전 브리핑을 생성한다.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

사용자가 회의 준비를 요청하면 즉시 Step 1부터 실행한다. 추가 질문 없이 바로 데이터를 수집한다.

---

## Workflow

### Step 1: 캘린더 조회 (회의 특정)
**Type**: api_mcp

캘린더를 **먼저** 조회해 오늘 회의 목록을 확보한다. 회의 제목·설명에서 키워드를 추출해 Gmail 검색에 활용한다.

```
mcp__claude_ai_Google_Calendar__gcal_list_events:
  calendarId: "primary"
  timeMin: "{오늘}T00:00:00"
  timeMax: "{오늘}T23:59:59"
  timeZone: "Asia/Seoul"
  condenseEventDetails: false
```

내일 일정도 함께 조회 (사전 준비 목적):
```
mcp__claude_ai_Google_Calendar__gcal_list_events:
  calendarId: "primary"
  timeMin: "{내일}T00:00:00"
  timeMax: "{내일}T23:59:59"
  timeZone: "Asia/Seoul"
  condenseEventDetails: true
```

**회의 특정 로직:**
- `$MEETING` 인자가 있으면 해당 이름과 가장 유사한 이벤트 선택
- 인자 없으면 현재 시각 이후 가장 임박한 회의 자동 선택
- 오늘 회의 없으면 내일 첫 회의 기준으로 전환

선택된 회의에서 추출할 정보:
- 회의 제목 키워드 (예: "생산회의" → "생산", "실적", "불량", "달성률")
- 참석자 이메일 주소
- 회의 설명(description) 내 키워드

### Step 2: Gmail 교차 조회 (병렬)
**Type**: api_mcp

Step 1에서 추출한 키워드로 Gmail을 검색한다. 캘린더 조회와 Gmail 일반 검색은 **병렬**로 실행 가능.

```
mcp__claude_ai_Gmail__gmail_search_messages:
  q: "is:unread newer_than:2d -category:promotions -category:social"
  maxResults: 20
```

**KST 보정**: `newer_than:1d`는 UTC 기준이므로 `newer_than:2d`를 사용해 누락 방지. 결과에서 KST 기준 오늘/어제 메일만 필터링.

**결과가 20건 초과 시**: 키워드 필터 추가 — 회의 제목 키워드 또는 참석자 이메일로 범위 축소.

### Step 3: 이메일 우선순위 분류 + 상세 읽기
**Type**: prompt + api_mcp

검색된 이메일을 **생산관리 도메인 키워드**로 우선순위 분류한다.

**우선순위 키워드 (높음→낮음):**
- 최우선: `입고지연`, `납기`, `불량`, `클레임`, `긴급`, `URGENT`
- 높음: `승인`, `결재`, `검토요청`, `확인요청`
- 중간: `생산순서`, `계획변경`, `긴급투입`, `설비`, `고장`
- 보통: `생산실적`, `달성률`, `일보`, `자료공유`

분류 후 **상위 5건**만 본문을 읽는다:
```
mcp__claude_ai_Gmail__gmail_read_message:
  messageId: "{해당 메일 ID}"
```

- 본문이 2,000자 초과 시 앞부분만 읽고 "[요약 처리됨]" 표시
- 첨부 파일은 파일명만 목록 표시 (본문 읽기 금지)
- 본문에서 숫자(달성률, 수량, 날짜) 추출

**달성률 플래그:**
- < 80% → 경고
- 80~90% → 주의
- >= 90% → 정상

### Step 4: 교차 분석 + 브리핑 합성
**Type**: prompt

이메일과 캘린더를 교차 분석해 브리핑을 합성한다.

**이메일-회의 연결 기준 (강도순):**
1. 이메일 제목에 회의 이름 직접 언급
2. 이메일 발신자 = 회의 참석자
3. 이메일 키워드가 회의 설명 키워드와 겹침
4. 수신 시각이 회의 48시간 이내

**핵심 안건 도출:**
- 우선순위 상위 이메일을 업무 유형별 클러스터링
- 클러스터별 대표 안건 1개씩 → 최대 3개
- 안건마다 반드시 출처 메일 명시

**액션아이템 추출:**
- 이메일 본문에 명시된 요청/지시만 추출 (비서가 임의 생성 금지)
- 시간 타깃: 메일에 날짜/시한 있으면 그대로, 없으면 "확인 필요"
- 회의 시각 역산: "회의 전까지" 처리 가능한 것 표시

### Step 5: 출력
**Type**: generate

아래 형식으로 출력한다. **결론 먼저, 짧고 실무적으로.**

```markdown
## 결론
> [한 줄: 이 회의에서 가장 중요한 것 + 위험 신호]

---

### 핵심 안건 (3개)
1. **[안건명]** — [1~2줄 설명]
   출처: [메일 제목 / 발신자]
2. ...
3. ...

### 액션아이템
- [ ] [할 일] — [시한] (출처: [메일/일정])
- [ ] ...

### 먼저 확인해야 할 메일
| 순서 | 제목 | 발신 | 핵심 |
|------|------|------|------|
| ... | ... | ... | ... |

### 관련 일정
| 시간 | 일정 | 연결 메일 |
|------|------|----------|
| ... | ... | ... |
```

**출력 규칙:**
- 시간은 모두 KST 표기
- 메일은 최대 5건, 안건은 정확히 3개, 액션아이템은 최대 5개
- 숫자마다 출처(메일 제목·발신자) 명시
- 회의와 무관한 메일은 제외 (연결 근거 없는 메일은 버린다)
- 불확실한 내용은 크로스체크 포인트로 분리

---

## Edge Cases

| 상황 | 처리 |
|------|------|
| 오늘 회의 없음 | 내일 첫 회의 기준 전환, "오늘 예정 회의 없음 — 내일 [회의명] 사전 준비" 안내 |
| 관련 메일 0건 | "관련 이메일 없음" 명시, 캘린더 기반 안건만 제시 |
| 메일 50건 초과 | 도메인 키워드 필터 후 상위 20건만 처리, "전체 N건 중 M건 분석" 명시 |
| Gmail MCP 실패 | "Gmail 연결 실패 — 캘린더 기반 브리핑만 제공" 후 일정 단독 출력 |
| Calendar MCP 실패 | "캘린더 연결 실패 — 이메일 기반 브리핑만 제공" 후 메일 단독 출력 |
| 두 MCP 모두 실패 | 즉시 안내 후 종료 |
| 본문 읽기 실패 (개별) | 제목+snippet만으로 요약, 전체 중단하지 않음 |

---

## Constraints (하드 제약)

- 이메일 답장/전달/삭제 **금지**
- 일정 생성/수정/삭제 **금지**
- 이메일 본문을 파일로 저장 **금지**
- 본문 읽기 최대 **5건**
- 출처 없는 안건 생성 **금지** — 할루시네이션 차단
- 읽기 전용 스킬 — 외부 상태 변경 일절 없음

---

## Integration Points

- **daily-briefing**: 하루 전체 개요가 필요하면 daily-briefing, 특정 회의 준비면 meeting-brief
- **pptx**: 브리핑 후 "PPT로 만들어줘" 요청 시 pptx 스킬 연계
- **cross-check**: 안건 검증이 필요하면 cross-check 스킬 연계
