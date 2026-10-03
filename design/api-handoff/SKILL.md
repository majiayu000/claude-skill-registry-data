---
name: api-handoff
description: "Create backend/frontend API handoff docs for endpoints, frontend data needs, and cross-team data requirements."
---

# API Handoff

프론트엔드-백엔드 간 API 핸드오프 문서 생성. 양방향 지원.

## 모드 선택

| 모드 | 용도 | 트리거 |
|------|------|--------|
| **Backend → Frontend** | API 완성 후 프론트 전달 | "create handoff", "document API", "frontend handoff" |
| **Frontend → Backend** | 데이터 요구사항 전달 | "backend requirements", "what data do I need" |

---

## Mode 1: Backend → Frontend Handoff

> **No Chat Output**: 핸드오프 문서만 생성. 설명 없음.

백엔드 개발 완료 후 프론트엔드에 전달하는 구조화된 문서 생성.

### Workflow

1. **Collect context** — feature, endpoints, DTOs, auth, edge cases 확인
2. **Create handoff file** — `docs/ai/<feature-name>/api-handoff.md`
3. **Fill template** — 모든 섹션 작성
4. **Double-check** — 페이로드, auth, validation 검증

### Output Template

```markdown
# API Handoff: [Feature Name]

## Business Context
[2-4 sentences: 문제, 사용자, 중요성, 도메인 용어]

## Endpoints

### [METHOD] /path/to/endpoint
- **Purpose**: [1줄]
- **Auth**: [role/permission 또는 "public"]
- **Request**:
  ```json
  { "field": "type — description, constraints" }
  ```
- **Response** (success):
  ```json
  { "field": "type — description" }
  ```
- **Response** (error): [HTTP codes: 422, 404 등]
- **Notes**: [edge cases, rate limits, pagination]

## Data Models / DTOs
[TypeScript interface 형식]

## Enums & Constants
| Value | Meaning | Display Label |
|-------|---------|---------------|

## Validation Rules
[프론트가 미러링할 검증 규칙]

## Business Logic & Edge Cases
- [비자명한 동작, 제약조건]

## Integration Notes
- **Recommended flow**: [fetch → select → submit → poll]
- **Optimistic UI**: [safe 여부]
- **Caching**: [cache headers]

## Test Scenarios
1. Happy path
2. Validation error
3. Not found
4. Permission denied
```

---

## Mode 2: Frontend → Backend Requirements

> **No Chat Output**: 요구사항 문서만 생성.

프론트엔드가 백엔드에 데이터 요구사항을 전달.

### 핵심 원칙

| Frontend Owns | Backend Owns |
|---------------|--------------|
| 어떤 데이터 필요 | 데이터 구조 |
| 어떤 액션 존재 | 엔드포인트 설계 |
| UI 상태 처리 | 필드명, 타입 |
| 표시 요구사항 | 성능/캐싱 |

### Workflow

1. **Describe feature** — 화면, 사용자, 목표
2. **List data needs** — 표시할 데이터, 액션, 상태
3. **Surface uncertainties** — 모르는 비즈니스 규칙
4. **Leave room** — 백엔드 피드백 요청

### Good vs Bad Requests

| Bad (구현 지시) | Good (필요 설명) |
|----------------|-----------------|
| "GET /api/contracts 필요" | "계약 목록 표시. 제목, 상태, 생성일 보여야 함" |
| "provider 객체 중첩" | "각 계약에서 제공자 이름/로고 필요" |

### Output Template

```markdown
# Backend Requirements: <Feature Name>

## Context
[무엇을, 누구를 위해, 어떤 문제 해결]

## Screens/Components

### <Screen Name>
**Data I need to display**: [데이터 설명]
**Actions**: [액션] → [결과]
**States**: Empty, Loading, Error, Special
**Business rules affecting UI**: [가시성/활성화 규칙]

## Uncertainties
- [ ] [X]가 [Y]일 때 표시 여부 불확실
- [ ] [Z]의 비즈니스 규칙 이해 부족

## Questions for Backend
- [X]와 [Y] 합치는 게 맞을까?
- [Z]가 항상 존재하나?
```

---

## Rules

### Backend → Frontend
- 정확하게: types, constraints, examples
- 비자명한 동작 명시
- 백엔드 구현 세부사항 제외 (파일 경로, 클래스명)
- TBD는 명시적으로 표시

### Frontend → Backend
- 구현 세부사항 지정 금지 (엔드포인트, 메서드, 필드명)
- 설명하되 지시하지 말 것
- 불확실한 점 숨기지 말 것
- 백엔드 피드백 명시적 요청
