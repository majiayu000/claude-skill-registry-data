---
name: notion-pilot
description: "Notion API 통합 스킬. DB/페이지/블록 CRUD, 마크다운 읽기/쓰기, 파일 업로드, 이미지 커버 설정, upsert, 코멘트, 페이지 이동 등 모든 Notion 작업을 notion-api.mjs 모듈로 처리합니다. Use when: (1) 노션에 추가/수정/조회, (2) 노션 DB 생성, (3) 노션 이미지 업로드, (4) 노션 커버 설정, (5) 노션 파일 업로드, (6) Notion API 작업. 트리거: '노션', 'Notion', '노션에', '노션 DB', '노션 페이지', '노션 업로드'."
allowed-tools: Bash(node *), Read, Write, Glob, Grep
---

# Notion Pilot 스킬

Notion API를 `notion-api.mjs` 모듈로 직접 호출하여 DB, 페이지, 블록, 파일 업로드 등 모든 작업을 처리하는 스킬.

## Workflow

모든 노션 작업은 아래 순서를 **반드시** 따른다.

### Step 1. config.json 확인

이 스킬 디렉토리 내 `config.json`을 Read 도구로 확인한다.

**config.json이 없는 경우 (최초 실행):**

먼저 이 스킬 디렉토리에 빈 토큰으로 `config.json`을 **즉시 생성**한다:

```json
{
  "token": ""
}
```

그 다음 사용자에게 아래와 같이 안내한다:

```
Notion 토큰 설정이 필요합니다. 두 가지 방법 중 선택하세요:

1️⃣ 여기에 토큰을 붙여넣기 (ntn_으로 시작하는 값)
2️⃣ 직접 파일에 입력: ~/.claude/skills/notion-pilot/config.json

토큰 발급: https://www.notion.so/profile/integrations → '새 API 통합' → 토큰 복사
```

- 사용자가 토큰을 붙여넣으면 → config.json의 `token` 값을 채워준다.
- 사용자가 "직접 입력할게" 등으로 응답하면 → config.json 경로를 다시 알려주고 작업을 중단한다.

**config.json이 있지만 token이 빈 문자열인 경우:**

위와 동일하게 토큰 입력을 안내한다.

**config.json이 있고 token이 채워져 있으면** 바로 Step 2로 진행한다.

### Step 2. 작업 실행

`notion-api.mjs` 모듈을 import하여 작업을 수행한다.

## API 호출 방법

### `notion-api.mjs` 모듈 (유일한 방법)

모든 Notion API 작업에 이 모듈을 사용한다. **`mcp__notion-mcp__*` 도구는 절대 사용하지 않는다.** OAuth MCP 토큰 만료 등의 문제가 발생해도 notion-api.mjs로만 작업한다.

```javascript
import { notion } from 'file:///<이 스킬의 scripts 디렉토리>/notion-api.mjs';

// 검색
const results = await notion.search('키워드', { filter: 'database' });

// DB 생성
const db = await notion.createDatabase(parentPageId, '새 DB', '📋', {
  '이름': { title: {} },
  '상태': { select: { options: [{ name: '진행중', color: 'blue' }] } },
});

// 페이지 생성 (DB 내) - prop 헬퍼 사용
const page = await notion.createPage(dbId, {
  '이름': notion.prop.title('홍길동'),
  '상태': notion.prop.status('시작 전'),   // status 타입 속성
  '분류': notion.prop.select('진행중'),    // select 타입 속성
  '점수': notion.prop.number(95),
  '태그': notion.prop.multiSelect(['A', 'B']),
});

// ── 페이지 본문 읽기/쓰기 (마크다운 우선) ──
// 읽기: 특수 블록도 <callout>, <database> 등 확장 태그로 반환됨 (누락 없음)
const content = await notion.getPageMarkdown(pageId);

// 쓰기: 마크다운 문자열로 본문 전체 교체 (블록 API 대비 토큰 6배 절약)
await notion.updatePageMarkdown(pageId, '## 섹션 제목\n\n본문 내용\n\n- 항목 1\n- 항목 2');

// 블록 API는 마크다운으로 불가능한 세밀한 조작이 필요할 때만 사용
await notion.appendBlocks(pageId, [
  notion.block.callout('안내', '📝', 'blue_background'),
  notion.block.toDo('할 일 항목', false),
  notion.block.toggle('토글 제목', [notion.block.paragraph('토글 내부')]),
  notion.block.code('console.log("hi")', 'javascript'),
]);
// ※ appendBlocks는 rich_text의 text 객체 안에 잘못 넣은 annotations를
//   rich_text 아이템 최상위로 자동으로 옮긴 뒤 전송한다.

// 하위 블록 전체 조회 (100개 넘는 블록도 자동 페이지네이션, 평탄 배열 반환)
const allBlocks = await notion.getBlocksAll(pageId);

// ── 마크다운 쓰기 시 특수 블록 레퍼런스 ──
// ✅ 읽기/쓰기 모두 지원:
//
//   [callout] 반드시 아래 형식 준수 — 태그와 내용이 별도 줄, 내용은 탭(\t) 들여쓰기:
//   <callout icon="📌">
//   	한 줄 내용
//   </callout>
//   <callout icon="📌" color="blue_bg">
//   	멀티라인 내용
//   	두 번째 줄 (탭 들여쓰기 필수)
//   </callout>
//   ※ 색상 단축키: blue_bg, green_bg, yellow_bg, orange_bg, red_bg, purple_bg, pink_bg, gray_bg
//   ⚠️ 금지: <callout icon="📌">내용</callout> (한 줄 인라인 형식은 단순 텍스트만 가능)
//   ⚠️ 금지: 내용에 빈 줄(\n\n) 포함 — 빈 줄 대신 탭+빈줄(\t\n) 사용
//
//   [toggle/details] 반드시 아래 형식 준수 — 내용은 탭(\t) 들여쓰기:
//   <details>
//   <summary>토글 제목</summary>
//   	내용 (탭 들여쓰기 필수)
//   	
//   	빈 줄도 탭+빈줄(\t\n\t) 형태로
//   </details>
//   ⚠️ 금지: <details><summary>제목</summary>내용</details> (한 줄 인라인 형식 — 파싱 실패)
//
//   > 인용문 (quote)
//   --- (divider)
//   - [ ] 미완료 / - [x] 완료 (to_do)
//   | 헤더 | ... | (table)
//   ```lang ... ``` (code)
//   $`E=mc^2`$ (인라인 수식)
//   $$\nE=mc^2\n$$ (수식 블록)
//
// ⚠️ 읽기전용 (쓰기 불가, 블록 API로 대체):
//   bookmark → 읽으면 <unknown alt="bookmark"/> 로 표시
//   embed → 읽으면 <unknown alt="embed"/> 로 표시
//   synced_block → 블록 API 필수

// DB 전체 조회 (자동 페이지네이션)
const allPages = await notion.queryAll(dbId);

// ── 저수준 API 호출 (call) ──
// 시그니처: notion.call(method, path, body?)
// - method: 'GET' | 'POST' | 'PATCH' | 'DELETE'
// - path: 슬래시(/)로 시작하는 API 경로 (예: '/pages/PAGE_ID')
// - body: POST/PATCH 시 요청 본문 (선택)
// ⚠️ queryAll/createPage 등 고수준 함수는 DB ID → DS ID 자동 변환을 하지만,
//    call()은 자동 변환하지 않으므로 DS ID가 필요한 엔드포인트에서는 직접 DS ID를 사용해야 한다.
const page = await notion.call('GET', '/pages/PAGE_ID');
const children = await notion.call('GET', '/blocks/BLOCK_ID/children?page_size=100');
await notion.call('PATCH', '/pages/PAGE_ID', { in_trash: true });
// 블록을 특정 위치에 삽입: `after` 파라미터는 폐기됨(2026-03-11) → `position` 객체 사용
await notion.call('PATCH', '/blocks/PARENT_ID/children', {
  position: { type: 'after_block', after_block: { id: 'BLOCK_ID' } }, // 시작/끝: { type:'start' } / { type:'end' }(기본)
  children: [ /* 블록 배열 */ ],
});

// 배치 처리 (동시성 15)
await notion.batch(items, async (item) => {
  await notion.createPage(dbId, { '이름': notion.prop.title(item.name) });
});

// Upsert (단건)
const result = await notion.upsertPage(dbId, '이름', 'title', '홍길동', {
  '이름': notion.prop.title('홍길동'),
  '점수': notion.prop.number(95),
});

// Bulk Upsert (대량, queryAll 캐시 + 동시성 15)
const stats = await notion.bulkUpsert(dbId, '이름', [
  { matchValue: '홍길동', properties: { '이름': notion.prop.title('홍길동'), '점수': notion.prop.number(100) } },
]);

// 파일 업로드 → 페이지 커버 설정 / 이미지 블록 추가
await notion.setCover(pageId, 'C:/path/to/cover.webp');
await notion.addImageBlock(pageId, 'C:/path/to/photo.png');

// URL에서 다운로드 → Notion 업로드 (실패 시 null)
const uploadId = await notion.uploadFromUrl('https://example.com/img.jpg');

// 로컬 파일 업로드만 (ID 반환). 업로드 완료(status 'uploaded')까지 확인한 뒤 ID를 돌려준다.
// 지원 확장자: 이미지(webp/png/jpg/gif/svg), pdf, mp4, mp3, zip, html
const id = await notion.uploadFile('C:/path/to/file.pdf');

// 파일 속성(files)에 첨부 + 정말 붙었는지 확인 (실패하면 새로 업로드해 1회 재시도, 그래도 안 되면 에러)
// ⚠️ files 속성 첨부는 uploadFile + updatePage 직접 조합 대신 이 함수를 쓴다.
//    완료 확인 없이 붙이면 저장 직후에는 보이다가 1시간 뒤 첨부만 사라질 수 있다.
const att = await notion.attachFileToProperty(pageId, '첨부파일', 'C:/path/to/자료.zip');
// → { uploadId, entryType: 'file', status: 'uploaded', expiry_time: null, url, bytes }

// 첨부 재확인: 실제로 내려받아 바이트 수까지 대조 (첨부 직후 + 몇 분 뒤 두 번 확인 권장)
const check = await notion.verifyFileProperty(pageId, '첨부파일', { expectBytes: att.bytes });
// → { count, files: [{ name, type, ok, bytes, ... }], ok: true|false }

// 업로드 객체 상태 조회 (status, expiry_time 등)
const fu = await notion.getFileUpload(id);

// 코멘트
await notion.createComment(pageId, '코멘트 내용');
const comments = await notion.listComments(pageId);

// 페이지 이동
await notion.movePage(pageId, { page_id: targetPageId });
```

**주의사항**:
- 크리덴셜은 모듈이 `config.json`에서 자동 로드
- API 버전 `2026-03-11` (DB ID → DS ID 자동 변환 내장)
- `createDatabase`는 요청한 속성이 하나라도 만들어지지 않으면 에러를 낸다 (조용히 빠진 채 넘어가지 않음)
- Formula에서 다른 Formula/Rollup 참조 시 `{{notion:block_property:PROP_ID:...}}` 내부 형식 필요 (prop() 불가)

## 실패 시 자가 수복 프로토콜

모듈 함수 호출이 실패하면 아래 순서를 따른다. **MCP 폴백은 절대 하지 않는다.**

1. **에러 패턴 가이드 조회** — 아래 표에서 에러 코드+메시지 패턴을 먼저 확인
2. **가이드에 있으면** — 해당 해법을 즉시 적용하여 재시도
3. **가이드에 없으면** — 모듈을 import하되, 실패한 부분만 `notion.call()`로 우회하는 인라인 스크립트 작성
4. **우회 성공 시** — 우회 코드를 `notion-api.mjs`에 반영하고, 새 패턴을 아래 표에 추가

### 에러 패턴 가이드

| 코드 | 메시지 패턴 | 원인 | 해법 |
|------|------------|------|------|
| 400 | `body.parent.database_id should be a string` | `createPage`에 객체를 넘김 | 첫 인자로 DB ID **문자열**만 넘긴다: `createPage('db-id', { props })` |
| 400 | `text.annotations should be not present` | `annotations`를 `text` 객체 안에 넣음 | `annotations`는 rich_text 아이템 최상위에 배치: `{ text: { content: '...' }, annotations: { bold: true } }` (`appendBlocks`는 자동 교정함) |
| 400 | `rich_text should be an array` | rich_text에 문자열을 넣음 | `rich_text: [{ text: { content: '...' } }]` 배열 형태 필수 |
| 400 | `Could not find property` | DB 속성명 오타 | `notion.prop.*` 헬퍼 사용 + `getDatabase()`로 실제 속성명 확인 |
| 400 | `body.children[N]` 관련 | 블록 구조 오류 | `notion.block.*` 헬퍼 사용. 직접 JSON 구성 시 Notion API 블록 스펙 확인 |
| 404 | `Could not find database` | DB ID가 DS ID로 변경됨 | 자동 폴백 작동. `_dsCache`에 매핑 저장됨 |
| 404 | `Could not find page/block` | Integration에 해당 페이지가 공유되지 않음 | 노션 페이지 우측 상단 `···` → `연결` → 만든 Integration 선택 |
| 401 | `API token is invalid` | 토큰 만료/오입력 | 이 스킬 폴더의 `config.json` 토큰 교체 |
| 429 | `Rate limited` | 요청 과다 | `notion.batch()` 동시성 15 사용. 자동 재시도 대기 |
| 200 | (사일런트) `createDatabase` 후 properties 없음 | API 2026-03-11에서 `POST /databases`의 properties 파라미터가 무시됨 | 모듈에서 처리됨: DB 생성 → `data_sources[0].id` 추출 → `PATCH /data_sources/{dsId}`로 properties 추가. 기본 'Name' 속성은 title 타입 속성명으로 자동 rename. 그래도 빠진 속성이 있으면 에러 |
| 400 | `body.archived should be not present` | 페이지/DB 휴지통 처리에 `{ archived: true }` 사용 (구 필드명) | API 2026-03-11부터 `in_trash`로 변경됨. `notion.call('PATCH', '/pages/ID', { in_trash: true })` 사용. 복원은 `{ in_trash: false }`. 응답 객체에서도 `response.in_trash`를 읽는다 |
| 400 | `filename has an extension that is not supported for the File Upload API` | 폰트(.ttf/.otf/.woff/.woff2) 등 미지원 확장자 업로드 | File Upload API는 image/audio/video/document(.pdf/.json/.txt) + `.zip`만 허용. 폰트 등은 **개별 .zip으로 묶어** 업로드하고 `attachFileToProperty()`로 files 속성에 첨부 |
| 400 | `content type application/octet-stream is not supported for the File Upload API` | 모듈의 MIME_MAP에 없는 확장자 → octet-stream 폴백, Notion이 거부 | `notion-api.mjs`의 MIME_MAP에 해당 확장자의 정확한 MIME 추가(`.zip`→`application/zip` 등). octet-stream은 거부됨 |
| 400 | `body.after should be not present` | 블록 삽입 위치 지정에 `after` 사용 (폐기됨) | API 2026-03-11부터 `after` → `position` 객체로 변경. 특정 블록 뒤 삽입: `call('PATCH','/blocks/PARENT_ID/children', { position:{ type:'after_block', after_block:{ id:BLOCK_ID } }, children:[...] })`. 시작/끝: `{ type:'start' }` / `{ type:'end' }`(기본) |
| — | (사일런트) 파일 첨부가 며칠 뒤 사라짐 | 업로드가 `pending`인 채로 첨부 → 1시간 안에 완료되지 않으면 노션이 파일을 회수 | 모듈에서 처리됨: `uploadFile()`이 완료 상태를 확인한다. files 속성은 `attachFileToProperty()`로 붙이고 `verifyFileProperty()`로 재확인 |

> 새로운 에러 패턴을 발견할 때마다 이 표에 추가한다.

## 토큰 절약 규칙

1. **페이지 본문은 마크다운 API 우선**: 읽기 `getPageMarkdown()`, 쓰기 `updatePageMarkdown()`. 특수 블록도 확장 태그로 보존됨. 블록 API 대비 읽기 20배, 쓰기 6배 토큰 절약.
2. **블록 API는 세밀한 조작이 필요할 때만**: 특정 블록 하나만 수정/삭제, 블록 순서 조작 등.
3. **여러 페이지 작업 시** `notion.batch()`로 동시성 15 병렬 처리.
4. **전체 조회 시** `notion.queryAll()`로 자동 페이지네이션.
5. **Upsert 전략 선택**: 10건 미만 → `upsertPage()`, 10건 이상 → `bulkUpsert()`.
6. **하위 블록 전체 조회 시** `notion.getBlocksAll()`로 자동 페이지네이션 (`getBlocks()`는 첫 100개만).

## 헬퍼 레퍼런스

### `notion.block.*` — 블록 빌더

| 헬퍼 | 인자 | Notion 블록 타입 |
|-------|------|-----------------|
| `paragraph(text, {link?, color?})` | 텍스트, 옵션 | paragraph |
| `heading1(text)` | 텍스트 | heading_1 |
| `heading2(text)` | 텍스트 | heading_2 |
| `heading3(text)` | 텍스트 | heading_3 |
| `heading4(text)` | 텍스트 | heading_4 |
| `bullet(text)` | 텍스트 | bulleted_list_item |
| `numbered(text)` | 텍스트 | numbered_list_item |
| `toDo(text, checked?)` | 텍스트, 체크 여부(기본 false) | to_do |
| `quote(text, color?)` | 텍스트, 색상(기본 default) | quote |
| `toggle(text, children?)` | 텍스트, 하위 블록 배열 | toggle |
| `callout(text, emoji?, color?)` | 텍스트, 이모지(기본 💡), 색상 | callout |
| `code(text, language?)` | 코드 문자열, 언어(기본 plain text) | code |
| `bookmark(url, caption?)` | URL, 캡션 | bookmark |
| `equation(expression)` | LaTeX 수식 | equation |
| `divider()` | — | divider |
| `tableOfContents(color?)` | 색상(기본 default) | table_of_contents |

> table, column_list, synced_block 등 복잡한 구조체는 헬퍼 없이 JSON 직접 구성

### `notion.prop.*` — 속성 빌더

| 헬퍼 | 인자 | Notion 속성 타입 |
|-------|------|-----------------|
| `title(text)` | 텍스트 | title |
| `richText(text)` | 텍스트 | rich_text |
| `number(n)` | 숫자 | number |
| `select(name)` | 옵션명 | select |
| `multiSelect(names)` | 옵션명 배열 | multi_select |
| `status(name)` | 상태명 | status |
| `checkbox(checked)` | boolean | checkbox |
| `date(start, end?)` | ISO 날짜, 종료일(선택) | date |
| `url(url)` | URL 문자열 | url |
| `email(email)` | 이메일 문자열 | email |
| `phone(phone)` | 전화번호 문자열 | phone_number |
| `people(ids)` | 사용자 ID 또는 배열 | people |
| `relation(ids)` | 페이지 ID 또는 배열 | relation |
