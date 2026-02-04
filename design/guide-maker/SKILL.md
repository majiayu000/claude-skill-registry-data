---
name: guide-maker
description: Place 프로젝트 사용자 가이드를 Notion에 생성하는 스킬. 테이블, 색상, 코드블록, 화살표, 이모지를 활용한 가시성 높은 문서 생성. "가이드 만들어줘", "사용자 매뉴얼 작성해줘", "도움말 문서 생성해줘", "Notion에 문서 작성해줘" 요청 시 사용. Notion MCP (MCP_DOCKER) 필요.
---

# Guide Maker

Place 프로젝트 기능에 대한 **가시성 높은** 사용자 가이드를 Notion에 생성.

## 사전 요구사항

- Notion MCP (`MCP_DOCKER`) 연결
- 부모 페이지 ID: `0656783731824d52aa4ac9523521bd14`

## 워크플로우

### 1. 기능 분석
해당 기능의 코드(`app/` 폴더) 분석 → 주요 버튼, 폼, 테이블, 상태값 파악

### 2. 콘텐츠 구조 설계
문서 구조에 맞춰 **전체 블록 배열 설계** (페이지 위치, Part별 Step, 테이블, FAQ 등)

### 3. 한 번에 생성 (🚨 필수!)

**반드시 `code-mode` 스크립트 한 번으로 전체 가이드 생성:**

```javascript
// 1. 페이지 생성
const result = JSON.parse(this['API-post-page']({
  parent: { page_id: "0656783731824d52aa4ac9523521bd14" },
  properties: { title: [{ text: { content: "📑 [기능명]" } }] }
}));
const pageId = result.id;

// 2. 모든 블록을 하나의 배열로 구성
const allBlocks = [
  // Part 1 헤더 + Step 1~N + divider
  // Part 2 헤더 + Step 1~N + divider
  // 테이블들
  // FAQ 토글들
];

// 3. 단 한 번의 API 호출로 콘텐츠 추가
this['API-patch-block-children']({ block_id: pageId, children: allBlocks });

return `https://www.notion.so/${pageId.replace(/-/g, '')}`;
```

**❌ 금지:** Step별/Part별로 나눠서 여러 번 API 호출
**✅ 필수:** 전체 블록을 하나의 배열로 → 단 1회 API 호출

### 4. 완료
URL 전달: `https://www.notion.so/[page_id_without_hyphens]`

---

## 문서 구조 (필수)

```
## 페이지 위치
**가맹점 대시보드** → **기능명**
[이미지]
---

## [기능] 방법

### Step 1. [작업 제목]
[설명]
[이미지]
1. **'버튼명'**을 클릭합니다.
2. [동작]
💡 Tip: [정보]
---

### Step 2. ...

## [테이블명] 컬럼 설명
| 컬럼명 | 설명 |
|--------|------|
| ... | ... |
---

## [상태] 안내
| 상태 | 색상 | 설명 |
|------|------|------|
| ✅ 완료 | 🟢 초록 | ... |
| ⏳ 대기 | 🟡 노랑 | ... |
| ❌ 실패 | 🔴 빨강 | ... |
---

## 자주 묻는 질문
> Q: [질문]?
A: [답변]
```

---

## 가시성 원칙

| 요소 | 용도 | 예시 |
|------|------|------|
| **테이블** | 컬럼/상태/필드 설명 | 상태 테이블, 입력 필드 테이블 |
| **→ 화살표** | 경로/흐름 | `대시보드 → 원비청구` |
| **이모지+색상** | 상태 구분 | `✅ 완납 🟢`, `❌ 미납 🔴` |
| **굵은 텍스트** | 버튼/메뉴 강조 | `**'저장'**` |
| **인라인 코드** | 입력값/형식 | `` `010-1234-5678` `` |
| **콜아웃** | 팁/주의/자동화 | 💡⚠️⚡ |
| **코드 블록** | 예시 데이터 | 입력 예시 |

---

## 레퍼런스

- **Notion 블록 JSON**: [references/notion-blocks.md](references/notion-blocks.md)
- **가시성 패턴 예시**: [references/visual-patterns.md](references/visual-patterns.md)

---

## 체크리스트

### 필수
- [ ] 페이지 위치 (→ 화살표 + 이미지)
- [ ] 모든 Step에 이미지 블록
- [ ] 버튼/메뉴: **'작은따옴표'와 굵게**
- [ ] 각 Step 끝에 divider
- [ ] FAQ 섹션 (최소 3개 토글)

### 가시성
- [ ] 컬럼 설명 테이블
- [ ] 상태값 테이블 (이모지+색상)
- [ ] 입력 형식: 인라인 코드
- [ ] 콜아웃 활용 (💡⚠️⚡)
