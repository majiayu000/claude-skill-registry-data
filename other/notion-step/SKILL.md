---
name: notion-step
description: "교육용 Padlet 클론 Step 1: Notion DB 연동 코드 생성 및 교안 작성 가이드. Express.js 서버 + Notion API 프록시 + Vanilla HTML/CSS/JS 프론트엔드 구현. Notion 연동, Step 1 코드 작성, Notion API 키 설정 가이드가 필요하면 이 스킬을 사용할 것."
---

# Notion Step — Step 1 구현 가이드

교육용 Padlet 클론의 첫 번째 단계: **Notion을 시각적 데이터베이스로 사용**하는 보드 앱.

## 이 단계의 학습 목표

- 데이터베이스란 무엇인가 (Notion 표 = DB)
- 클라이언트-서버 구조 이해 (브라우저 ↔ Express 서버 ↔ Notion)
- API와 HTTP 요청 개념 (fetch, JSON)
- CRUD 동작 직접 확인 (Notion 페이지에서 데이터 변화 관찰)

## 기술 스택

```
브라우저 (HTML/CSS/JS)
    ↕ fetch() — HTTP 요청
localhost:3000 (Express.js 서버)
    ↕ @notionhq/client — Notion SDK
Notion Database (학생이 직접 볼 수 있는 표)
```

**사용 패키지:**
- `express` — 웹 서버
- `@notionhq/client` — Notion 공식 SDK
- `dotenv` — 환경변수 (.env 파일)
- `cors` — 브라우저-서버 통신 허용

## Notion DB 구조 (표준)

학생의 Notion에 만들 데이터베이스 컬럼:

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| Title | Title | 카드 제목 (Notion 기본 컬럼) |
| Content | Text | 카드 내용 |
| Color | Select | 카드 배경색 (yellow/blue/green/pink) |
| BoardId | Text | 어느 보드에 속하는지 |
| CreatedAt | Created time | 자동 생성 |

## 코드 구현 가이드

### server.js 핵심 구조

```javascript
// 필요한 도구들을 가져옵니다
require('dotenv').config();
const express = require('express');
const { Client } = require('@notionhq/client');
const cors = require('cors');

const app = express();
const notion = new Client({ auth: process.env.NOTION_API_KEY });
const DATABASE_ID = process.env.NOTION_DATABASE_ID;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// db.js를 통해 Notion 연동
const db = require('./db');

// 서버 시작 전 환경변수 확인
if (!process.env.NOTION_API_KEY || !process.env.NOTION_DATABASE_ID) {
  console.error('❌ .env 파일에 NOTION_API_KEY와 NOTION_DATABASE_ID가 필요합니다.');
  console.error('   .env.example 파일을 복사해서 .env를 만들고 값을 채워주세요.');
  process.exit(1);
}

// API 엔드포인트
app.get('/api/cards', async (req, res) => { ... });
app.post('/api/cards', async (req, res) => { ... });
app.patch('/api/cards/:id', async (req, res) => { ... });
app.delete('/api/cards/:id', async (req, res) => { ... });

app.listen(3000, () => console.log('✅ 서버 시작! http://localhost:3000'));
```

### db.js (Notion 버전) 표준 구현

code-builder는 아래 인터페이스를 정확히 구현해야 한다:

```javascript
const { Client } = require('@notionhq/client');
require('dotenv').config();

const notion = new Client({ auth: process.env.NOTION_API_KEY });
const DATABASE_ID = process.env.NOTION_DATABASE_ID;

// Notion 응답을 우리 앱 형식으로 변환하는 함수
function notionToCard(page) {
  return {
    id: page.id,
    title: page.properties.Title?.title[0]?.plain_text || '',
    content: page.properties.Content?.rich_text[0]?.plain_text || '',
    color: page.properties.Color?.select?.name || 'yellow',
    boardId: page.properties.BoardId?.rich_text[0]?.plain_text || 'default',
    createdAt: page.created_time,
  };
}

module.exports = {
  // DB 초기화 (Notion은 이미 만들어져 있으므로 연결 테스트만)
  initialize: async () => {
    await notion.databases.retrieve({ database_id: DATABASE_ID });
    console.log('✅ Notion DB 연결 성공');
  },

  // 카드 목록 조회
  getCards: async (boardId = 'default') => {
    const response = await notion.databases.query({
      database_id: DATABASE_ID,
      filter: boardId !== 'all' ? {
        property: 'BoardId',
        rich_text: { equals: boardId }
      } : undefined,
    });
    return response.results.map(notionToCard);
  },

  // 카드 생성
  createCard: async ({ title, content, color = 'yellow', boardId = 'default' }) => {
    const response = await notion.pages.create({
      parent: { database_id: DATABASE_ID },
      properties: {
        Title: { title: [{ text: { content: title } }] },
        Content: { rich_text: [{ text: { content: content } }] },
        Color: { select: { name: color } },
        BoardId: { rich_text: [{ text: { content: boardId } }] },
      },
    });
    return notionToCard(response);
  },

  // 카드 수정
  updateCard: async (id, { title, content, color }) => {
    const properties = {};
    if (title !== undefined) properties.Title = { title: [{ text: { content: title } }] };
    if (content !== undefined) properties.Content = { rich_text: [{ text: { content: content } }] };
    if (color !== undefined) properties.Color = { select: { name: color } };
    const response = await notion.pages.update({ page_id: id, properties });
    return notionToCard(response);
  },

  // 카드 삭제 (Notion은 아카이브 처리)
  deleteCard: async (id) => {
    await notion.pages.update({ page_id: id, archived: true });
    return { success: true };
  },

  // 보드 목록 (Step 1에서는 기본 보드 1개만)
  getBoards: async () => [{ id: 'default', name: '우리 반 보드' }],
  createBoard: async ({ name }) => ({ id: name.toLowerCase(), name }),
};
```

### 프론트엔드 구현 포인트

`public/index.html` + `public/app.js`에서 구현할 내용:

1. **보드 레이아웃** — CSS Grid로 카드 배치 (Masonry 레이아웃 지향)
2. **카드 추가** — 모달 또는 인라인 폼
3. **카드 삭제** — 카드 우상단 X 버튼
4. **카드 색상** — 4가지 색상 선택 (yellow, blue, green, pink)
5. **자동 새로고침** — 5초마다 `GET /api/cards` 호출 (폴링 방식, Step 1 한정)

**app.js 핵심 패턴:**
```javascript
// 서버에서 카드 가져오기
async function loadCards() {
  const res = await fetch('/api/cards');
  const cards = await res.json();
  renderCards(cards);
}

// 카드 HTML로 변환
function renderCards(cards) {
  const board = document.getElementById('board');
  board.innerHTML = cards.map(card => `
    <div class="card ${card.color}" data-id="${card.id}">
      <button class="delete-btn" onclick="deleteCard('${card.id}')">×</button>
      <h3>${card.title}</h3>
      <p>${card.content}</p>
    </div>
  `).join('');
}
```

## .env.example 표준

```
# Notion API 키 (https://www.notion.so/my-integrations 에서 발급)
NOTION_API_KEY=secret_여기에_실제_키를_붙여넣으세요

# Notion 데이터베이스 ID (Notion DB 페이지 URL에서 복사)
# URL 예: https://notion.so/abc123def456?v=... → ID: abc123def456
NOTION_DATABASE_ID=여기에_데이터베이스_ID를_붙여넣으세요
```

## Notion API 키 발급 절차 요약

curriculum-writer가 학생용 가이드를 작성할 때 참고:

1. notion.so 로그인 → 우측 상단 프로필 → Settings
2. 좌측 메뉴 "Connections" → "Develop or manage integrations" 클릭
3. "+ New integration" → 이름 입력 (예: "우리반 패들렛") → Submit
4. "Internal Integration Secret" 복사 → `.env`의 `NOTION_API_KEY`에 붙여넣기
5. Notion에서 DB 페이지 열기 → 우상단 "..." → "Connections" → 방금 만든 인테그레이션 연결
6. DB 페이지 URL에서 ID 복사: `notion.so/[이_부분_32글자]?v=...`

> 상세 스크린샷 설명은 `references/notion-api-guide.md` 참조

## 테스트 시나리오

### 정상 동작 확인 순서
1. `npm install` → 오류 없음
2. `.env.example` → `.env` 복사 후 키 입력
3. `node server.js` → "✅ Notion DB 연결 성공", "✅ 서버 시작!" 출력
4. `http://localhost:3000` → 빈 보드 화면
5. 카드 추가 → Notion DB 새로고침 → 새 행 생성 확인
6. 카드 삭제 → Notion DB 새로고침 → 해당 행 아카이브 처리 확인
