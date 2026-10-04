---
name: supabase-step
description: "교육용 Padlet 클론 Step 3: Supabase(PostgreSQL 관리형)로 전환하는 코드 및 교안 가이드. 클라우드 DB, 배포, 실제 서비스 개념 학습. Step 2에서 db.js만 교체. Supabase 연동, 클라우드 DB, Step 3 코드 작성이 필요하면 이 스킬을 사용할 것."
---

# Supabase Step — Step 3 구현 가이드

교육용 Padlet 클론의 세 번째 단계: **인터넷 어딘가에 있는 DB**, 친구도 접속 가능한 서비스로 발전.

## 이 단계의 핵심 메시지

> "지금까지는 내 컴퓨터에만 있었어요. 이제 인터넷에 올려서 친구도 쓸 수 있게 해봅시다."

## 이 단계의 학습 목표

- 클라우드 DB 개념 (내 컴퓨터 밖에 데이터가 저장)
- PostgreSQL 기본 (SQLite와 차이점)
- 환경변수의 중요성 (API 키 보안)
- 배포 개념 (Vercel로 서버 올리기 — 선택)
- 실시간 기능 맛보기 (Supabase Realtime — 선택 심화)

## 왜 Supabase인가 (PostgreSQL 대신)

| 비교 | 직접 PostgreSQL | Supabase |
|------|----------------|---------|
| 설치 | 복잡 | 없음 (브라우저) |
| 테이블 확인 | 커맨드라인 | 웹 UI (Excel처럼) |
| API 자동 생성 | 직접 코딩 | 자동 |
| 무료 | 무료 | 무료 (2개 프로젝트) |
| 학생 경험 | 어려움 | "Notion이랑 비슷!" |

## 기술 스택

```
브라우저 (HTML/CSS/JS)  ← Step 1, 2와 동일
    ↕ fetch()
localhost:3000 (Express.js)  ← Step 1, 2와 동일
    ↕ @supabase/supabase-js
Supabase (클라우드 PostgreSQL)  ← NEW
```

**변경 사항:**
- `db.js` 교체 (better-sqlite3 → @supabase/supabase-js)
- `.env` 변경 (Supabase URL + anon key 추가)

**유지 사항:** `server.js`, `public/` — 변경 없음

## Supabase 프로젝트 설정

curriculum-writer가 학생 가이드에 포함할 내용:

1. supabase.com 접속 → "Start your project" → GitHub으로 로그인
2. "New project" → 이름: `edu-padlet`, 비밀번호 설정, 지역: Southeast Asia
3. 프로젝트 생성 대기 (1~2분)
4. 좌측 "Table Editor" → "Create a new table"

**생성할 테이블:**

```sql
-- Supabase SQL Editor에서 실행
CREATE TABLE cards (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title      TEXT NOT NULL,
  content    TEXT DEFAULT '',
  color      TEXT DEFAULT 'yellow',
  board_id   TEXT DEFAULT 'default',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE boards (
  id   TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO boards (id, name) VALUES ('default', '우리 반 보드');
```

5. 좌측 "Settings" → "API" → 다음 2가지 복사:
   - **Project URL**: `https://xxx.supabase.co`
   - **anon public key**: `eyJ...` 로 시작하는 긴 문자열

## db.js (Supabase 버전) 표준 구현

```javascript
// Supabase db.js — Step 2의 db.js를 이것으로 교체하세요
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

module.exports = {
  // 연결 테스트
  initialize: async () => {
    const { error } = await supabase.from('cards').select('id').limit(1);
    if (error) throw new Error(`Supabase 연결 실패: ${error.message}`);
    console.log('✅ Supabase 연결 성공');
  },

  // 카드 목록 조회
  getCards: async (boardId = 'default') => {
    const query = supabase.from('cards').select('*').order('created_at', { ascending: false });
    if (boardId !== 'all') query.eq('board_id', boardId);
    const { data, error } = await query;
    if (error) throw error;
    return data;
  },

  // 카드 생성
  createCard: async ({ title, content = '', color = 'yellow', boardId = 'default' }) => {
    const { data, error } = await supabase
      .from('cards')
      .insert({ title, content, color, board_id: boardId })
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  // 카드 수정
  updateCard: async (id, updates) => {
    const { data, error } = await supabase
      .from('cards')
      .update(updates)
      .eq('id', id)
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  // 카드 삭제
  deleteCard: async (id) => {
    const { error } = await supabase.from('cards').delete().eq('id', id);
    if (error) throw error;
    return { success: true };
  },

  // 보드 목록
  getBoards: async () => {
    const { data, error } = await supabase.from('boards').select('*');
    if (error) throw error;
    return data;
  },
  createBoard: async ({ name }) => {
    const id = name.toLowerCase().replace(/\s/g, '-');
    const { data, error } = await supabase
      .from('boards').insert({ id, name }).select().single();
    if (error) throw error;
    return data;
  },
};
```

## .env.example (Step 3용)

```
# Supabase 프로젝트 URL (Settings > API > Project URL)
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co

# Supabase anon key (Settings > API > anon public)
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 선택 심화: 실시간 기능 (Supabase Realtime)

고3 또는 심화반에서 추가 가능:

```javascript
// public/app.js에 추가 — 다른 사람이 카드 추가하면 자동 반영
const { createClient } = require('@supabase/supabase-js'); // 프론트에서는 CDN 사용

// CDN 방식 (index.html <head>에 추가)
// <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

supabase
  .channel('cards-changes')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'cards' },
    () => loadCards() // 변경 감지 시 카드 새로고침
  )
  .subscribe();
```

이 기능을 추가하면 폴링(5초 주기) 대신 **진짜 실시간 협업**이 된다.

## 선택 심화: Vercel 배포

```bash
npm i -g vercel
vercel  # 프로젝트 폴더에서 실행
# 환경변수 설정: vercel env add SUPABASE_URL
# 환경변수 설정: vercel env add SUPABASE_ANON_KEY
```

배포 후 `https://프로젝트명.vercel.app` 주소로 친구에게 공유 가능.

## 교육 포인트: 3단계 비교표

curriculum-writer가 최종 교안에 포함할 비교:

| | Step 1 (Notion) | Step 2 (SQLite) | Step 3 (Supabase) |
|--|----------------|----------------|-----------------|
| DB 위치 | Notion 서버 | 내 컴퓨터 파일 | 클라우드 서버 |
| 데이터 확인 | Notion 앱 | VS Code / 파일 | Supabase 대시보드 |
| 동시 접속 | 가능 | 불가 (1명) | 가능 (여러 명) |
| 인터넷 없이 | 불가 | 가능 | 불가 |
| 배포 가능 | 어려움 | 어려움 | 쉬움 (Vercel) |
| SQL 사용 | 안 함 | 직접 작성 | 자동 생성 |

## 테스트 시나리오

1. `npm install` → `node server.js` → "✅ Supabase 연결 성공"
2. 카드 추가 → Supabase 대시보드 Table Editor에서 새 행 확인
3. 서버 종료 후 재시작 → 데이터 유지됨 (SQLite와 동일)
4. (심화) 두 브라우저 창 열기 → 한쪽에서 카드 추가 → 다른 쪽 새로고침 → 반영됨
5. (심화 Realtime) 한쪽에서 카드 추가 → 다른 쪽 자동으로 카드 나타남
