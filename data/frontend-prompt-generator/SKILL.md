---
name: frontend-prompt-generator
description: Generate structured prompts for frontend development tasks following established patterns. Use when the user requests prompts for wireframes, UI implementation, data binding, or routing functionality in React/Next.js projects with specific formatting requirements (Cursor rules, file paths, test-driven development).
allowed-tools: [Read, Grep, Glob]
---

# Frontend Prompt Generator

Generate consistent, well-structured prompts for frontend development tasks that follow established patterns for wireframe creation, UI implementation, data binding, and routing functionality.

## When to Use This Skill

Use this skill when the user wants to:
- Create prompts for frontend development tasks (wireframes, UI, data binding, routing)
- Generate prompts that follow a specific format with conditions and requirements
- Build prompts for React/Next.js components with TDD approach
- Create prompts for Figma-to-code workflows
- Generate prompts with GraphQL API integration

## Prompt Types

This skill supports four main prompt types:

1. **Wireframe**: Create HTML/flexbox wireframe structure with precise dimensions
2. **UI Implementation**: Implement Figma designs into existing wireframes using MCP
3. **Data Binding**: Bind GraphQL API data to components with TDD
4. **Routing**: Add navigation and linking functionality with TDD

## How to Use This Skill

### Step 1: 스마트 정보 추출 및 프롬프트 타입 결정

**먼저 사용자 메시지에서 컨텍스트를 분석하여 다음을 추출합니다:**

1. **컴포넌트명 감지**:
   - 사용자가 언급한 컴포넌트 이름 찾기 (예: "boards", "profile", "comments")
   - 없으면 질문하기

2. **프롬프트 타입 추론**:
   - "와이어프레임", "구조", "레이아웃" → Wireframe
   - "피그마", "디자인", "UI 구현" → UI Implementation
   - "데이터", "바인딩", "API", "GraphQL" → Data Binding
   - "클릭", "이동", "라우팅", "링크" → Routing
   - 명확하지 않으면 사용자에게 선택지 제공

3. **기존 파일 확인**:
   - `src/components/[컴포넌트명]/` 디렉토리 존재 여부 확인
   - 있으면 기존 파일 경로 재사용, 없으면 새로 생성

### Step 2: 타입별 필수 정보 수집 및 검증

각 프롬프트 타입별로 **필수 정보**와 **선택 정보**를 구분하여 수집합니다.

#### 2.1 Wireframe 프롬프트

**필수 정보:**
- ✅ 컴포넌트명 (예: "boards", "profile")
- ✅ 연결할 페이지 경로 (예: "src/app/boards/page.tsx")
- ✅ 영역 구조 및 크기 (예: "header: 1280 * 80")

**선택 정보:**
- gap 영역 (기본값: 각 영역 사이에 자동 추가)

**기본값 제안:**
- 컴포넌트명이 "boards"면 → 페이지 경로: `src/app/boards/page.tsx`
- 컴포넌트명이 "profile"면 → 페이지 경로: `src/app/profile/page.tsx`

**입력값 검증:**
- 영역 크기는 "이름: 너비 * 높이" 형식이어야 함
- 너비와 높이는 숫자여야 함 (단위: px)

#### 2.2 UI Implementation 프롬프트

**필수 정보:**
- ✅ 컴포넌트명
- ✅ Figma 채널명 (예: "abc123")
- ✅ Figma 노드 ID (예: "123:456")

**선택 정보:**
- 없음 (UI 구현은 필수 정보만으로 충분)

**기본값 제안:**
- 컴포넌트명에서 파일 경로 자동 생성

**입력값 검증:**
- 노드 ID는 "숫자:숫자" 형식이어야 함 (예: "123:456", "1:2")
- 잘못된 형식이면 재요청

#### 2.3 Data Binding 프롬프트

**필수 정보:**
- ✅ 컴포넌트명
- ✅ API 쿼리명 (예: "fetchBoards", "FETCH_BOARD")
- ✅ GraphQL 쿼리 구조
- ✅ 필드 매핑 (화면 필드 → API 필드)

**선택 정보:**
- 특수 처리 규칙 (text overflow, 날짜 포맷 등)
- CSS 처리 요구사항
- 테스트 시나리오

**기본값 제안:**
- 컴포넌트가 "boards"면 → API: "fetchBoards" 또는 "FETCH_BOARDS"
- 필드명이 유사하면 자동 매핑 제안 (예: title → title, writer → author)

**입력값 검증:**
- GraphQL 쿼리 구조가 유효한지 확인
- 필드 매핑이 명확한지 확인

#### 2.4 Routing 프롬프트

**필수 정보:**
- ✅ 컴포넌트명
- ✅ 클릭 가능한 요소 설명 (예: "게시글", "카드")
- ✅ 라우팅에 사용할 ID 필드명 (예: "boardId", "postId")
- ✅ 목적지 페이지 패턴 (예: "/boards/[boardId]")

**선택 정보:**
- 로컬스토리지 데이터 구조 (필요한 경우만)

**기본값 제안:**
- 컴포넌트가 "boards"면 → ID 필드: "boardId", 경로: "/boards/[boardId]"
- 컴포넌트가 "posts"면 → ID 필드: "postId", 경로: "/posts/[postId]"

**입력값 검증:**
- 경로 패턴에 동적 세그먼트가 있는지 확인 (예: [id])
- ID 필드명이 유효한 변수명인지 확인

### Step 3: 대화형 정보 수집 프로세스

**정보가 충분한 경우:**
- Step 4로 즉시 진행하여 프롬프트 생성

**정보가 부족한 경우:**
- 부족한 필수 정보를 명확하게 나열
- 각 정보에 대해 **기본값을 제안**하며 질문
- 예시 형식과 함께 설명

**질문 예시:**

```
[Wireframe 프롬프트 생성에 필요한 정보를 수집하겠습니다]

1. 컴포넌트명: boards
   ✅ 확인됨

2. 연결할 페이지 경로:
   💡 제안: src/app/boards/page.tsx
   이 경로를 사용하시겠습니까? 다른 경로가 필요하면 알려주세요.

3. 영역 구조 및 크기:
   ❓ 필요합니다. 다음 형식으로 알려주세요:
   예시:
   - header: 1280 * 80
   - content: 1280 * 600
   - footer: 1280 * 120
```

**재질문 시 규칙:**
- 이미 제공된 정보는 다시 묻지 않음
- 잘못된 형식인 경우 올바른 예시 제공
- 한 번에 최대 3개 정보까지만 질문 (사용자 피로도 방지)

### Step 4: 컨텍스트 기반 추론 및 검증

**수집한 정보를 검증하고 추가 정보를 추론합니다:**

1. **파일 경로 자동 생성**:
   - TSX: `src/components/[컴포넌트명]/index.tsx`
   - CSS: `src/components/[컴포넌트명]/styles.module.css`
   - HOOK: `src/components/[컴포넌트명]/hooks/[기능명].hook.ts`
   - TEST: `src/components/[컴포넌트명]/tests/[기능명].spec.ts`

2. **기존 코드 확인** (Data Binding, Routing 타입):
   - 컴포넌트 디렉토리에서 기존 GraphQL 쿼리 찾기
   - 기존 타입 정의 확인
   - 이미 바인딩된 필드 확인

3. **입력값 형식 검증**:
   - Figma 노드 ID: 정규식 `^\d+:\d+$` 매칭 확인
   - 영역 크기: `이름: 숫자 * 숫자` 형식 확인
   - GraphQL 쿼리: 기본 문법 검증

4. **검증 실패 시**:
   - 구체적인 오류 메시지와 올바른 예시 제공
   - 재입력 요청

### Step 5: 템플릿 읽기

프롬프트 생성 전 항상 템플릿 파일을 읽습니다:

```bash
# 메인 템플릿 읽기
Read .claude/skills/frontend-prompt-generator/references/prompt-templates.md

# 예시 참조 (필요시)
Read .claude/skills/frontend-prompt-generator/references/examples.md
```

### Step 6: 프롬프트 생성

템플릿의 정확한 형식을 따라 프롬프트를 생성합니다:

1. 표준 헤더로 시작
2. 조건 섹션을 올바른 들여쓰기로 추가
3. 핵심요구사항 섹션 추가
4. 정확한 구분선 사용 (46개 등호)
5. 일관된 들여쓰기 유지 (하위 항목 16칸)
6. 올바른 번호 형식 사용

**품질 체크리스트:**
- [ ] 모든 필수 조건 섹션 포함됨
- [ ] 구분선이 정확히 46개 등호
- [ ] 들여쓰기가 일관됨 (16칸/20칸)
- [ ] 커서룰이 프롬프트 타입에 맞게 설정됨
- [ ] 파일 경로가 올바름
- [ ] 테스트 조건이 명확함 (기능 프롬프트)

### Step 7: 최종 확인 및 제시

생성된 프롬프트를 사용자에게 제시하고:

1. **생성 결과 요약**:
   - 프롬프트 타입
   - 주요 설정 (컴포넌트명, 타겟 파일 등)
   - 적용된 기본값

2. **수정 제안 받기**:
   - "프롬프트를 수정하시겠습니까?"
   - "추가로 생성할 프롬프트가 있나요?" (예: 와이어프레임 → UI → 데이터바인딩)
   - "다른 타입의 프롬프트가 필요하신가요?"

3. **워크플로우 제안**:
   - Wireframe 생성 후 → UI Implementation 제안
   - UI Implementation 후 → Data Binding 제안
   - Data Binding 후 → Routing 제안

## 핵심 포맷팅 규칙

- **구분선**: 정확히 46개 등호 (`==============================================`)
- **들여쓰기**: 하위 항목 16칸, 하위의 하위 20칸
- **번호 형식**: 최상위 `1)`, `2)`, 하위 `1-1)`, `1-2)`
- **커서룰**: 항상 `@01-common.mdc` 포함 + 작업별 추가 룰
- **파일 경로**: `src/components/[컴포넌트명]/[파일타입]` 패턴
- **강조**: 중요 금지사항은 `**중요금지사항**` 사용

## 커서룰 패턴

- Wireframe: `@01-common.mdc`, `@02-wireframe.mdc`
- UI: `@01-common.mdc`, `@02-wireframe.mdc`, `@03-ui.mdc`
- Functionality: `@01-common.mdc`, `@04-func.mdc`

## 프롬프트 공통 구성요소

모든 프롬프트는 다음을 포함합니다:
- 시작 지침 라인
- 체크리스트 반환 요구사항
- 조건 섹션 (커서룰, 파일 경로 등)
- 핵심요구사항 섹션
- TDD 명세 (기능 프롬프트의 경우)

## 실제 동작 예시

### 예시 1: 정보가 충분한 경우 (즉시 생성)

**사용자 입력:**
> "boards 컴포넌트에 데이터 바인딩 프롬프트 만들어줘. fetchBoards API 사용하고, 제목이랑 작성자랑 날짜 바인딩할거야."

**스킬 동작:**
1. ✅ 컴포넌트명 감지: "boards"
2. ✅ 프롬프트 타입 추론: Data Binding
3. ✅ API 쿼리명: "fetchBoards"
4. ✅ 필드 매핑: 제목, 작성자, 날짜
5. 기존 코드 확인 → GraphQL 쿼리 찾기
6. 즉시 프롬프트 생성 및 제시

### 예시 2: 정보가 부족한 경우 (대화형)

**사용자 입력:**
> "profile 페이지 와이어프레임 프롬프트 만들어줘"

**스킬 응답:**
```
[Wireframe 프롬프트 생성에 필요한 정보를 수집하겠습니다]

1. 컴포넌트명: profile
   ✅ 확인됨

2. 연결할 페이지 경로:
   💡 제안: src/app/profile/page.tsx
   이 경로를 사용하시겠습니까?

3. 영역 구조 및 크기:
   ❓ 필요합니다. 다음 형식으로 알려주세요:
   예시:
   - header: 1280 * 80
   - content: 1280 * 600
```

**사용자 응답:**
> "경로는 그대로 쓰고, 영역은 header 1280 * 100, main 1280 * 700, footer 1280 * 80으로"

**스킬 동작:**
1. 경로 확정: src/app/profile/page.tsx
2. 영역 파싱 및 검증
3. 프롬프트 생성

### 예시 3: 잘못된 형식 입력 (검증 및 재요청)

**사용자 입력:**
> "boards UI 프롬프트 만들어줘. 노드 ID는 123-456"

**스킬 응답:**
```
⚠️ Figma 노드 ID 형식 오류

입력하신 값: 123-456
올바른 형식: 123:456 (콜론(:)으로 구분)

Figma에서 노드 ID를 확인하여 "숫자:숫자" 형식으로 다시 입력해주세요.
예시: 123:456, 1:2, 999:888
```

### 예시 4: 워크플로우 제안

**사용자가 Wireframe 프롬프트 생성 완료 후:**

**스킬 제안:**
```
✅ Wireframe 프롬프트가 생성되었습니다!

다음 단계 제안:
1. 이 프롬프트로 와이어프레임을 먼저 구현하세요
2. 완료 후 "UI 구현 프롬프트 만들어줘"라고 요청하시면
   Figma 디자인을 와이어프레임에 적용하는 프롬프트를 생성해드립니다

추가로 생성할 프롬프트가 있나요?
```

## 참고 리소스

- `references/prompt-templates.md` - 각 프롬프트 타입별 상세 템플릿 패턴
- `references/examples.md` - 생성된 프롬프트의 완전한 예시

## 주의사항

1. **읽기 전용 도구만 사용**: 이 스킬은 파일을 수정하지 않고 읽기만 합니다
2. **템플릿 필수 참조**: 프롬프트 생성 전 항상 references 파일을 읽어야 합니다
3. **형식 엄격 준수**: 생성된 프롬프트는 정확한 형식을 따라야 합니다
4. **사용자 확인 우선**: 기본값을 제안하되 항상 사용자 확인을 받습니다
