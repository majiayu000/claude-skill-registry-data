---
name: api-tester
description: API 연동 테스트 스킬. 프론트-백엔드 통신 검증, 프록시 설정 확인, CORS, JWT 토큰, 에러 응답, 파일 업로드 테스트. "API 테스트해줘"로 실행.
---

# API Tester

프론트엔드 ↔ 백엔드 API 연동을 실제로 검증하는 테스트 스킬.

## 사용법

```
"로그인 API 테스트해줘"
"프론트-백엔드 연동 검증해줘"
"/api-tester"
```

---

## 워크플로우

### 1. 환경 감지

서버 실행 상태 확인:
```bash
# 백엔드 포트 확인
curl -s http://localhost:8000/health || curl -s http://localhost:3001/health

# 프론트엔드 포트 확인
curl -s http://localhost:3000 || curl -s http://localhost:5173
```

프록시 설정 확인 (vite.config.ts, next.config.js, package.json proxy 등):
```bash
# Vite 프록시
grep -r "proxy" vite.config.* 2>/dev/null

# Next.js rewrites
grep -r "rewrites\|destination" next.config.* 2>/dev/null

# CRA proxy
grep "proxy" package.json 2>/dev/null
```

### 2. CORS 검증

```bash
# preflight OPTIONS 요청
curl -v -X OPTIONS http://localhost:8000/api/users \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type,Authorization" \
  2>&1 | grep -i "access-control"
```

**기대 결과:**
- `Access-Control-Allow-Origin`: 프론트엔드 origin 포함
- `Access-Control-Allow-Methods`: 필요한 HTTP 메서드 포함
- `Access-Control-Allow-Headers`: Content-Type, Authorization 포함
- `Access-Control-Allow-Credentials`: true (쿠키 사용 시)

### 3. 인증 흐름 검증

```bash
# 로그인 → 토큰 발급
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test1234"}' \
  | jq -r '.token // .access_token // .accessToken')

echo "Token: ${TOKEN:0:20}..."

# 보호된 API 호출
curl -s http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# 만료/잘못된 토큰
curl -s -w "\nHTTP Status: %{http_code}\n" \
  http://localhost:8000/api/users/me \
  -H "Authorization: Bearer invalid-token"
```

**기대 결과:**
- 올바른 토큰: 200 + 사용자 정보
- 잘못된 토큰: 401 Unauthorized
- 토큰 없음: 401 또는 403

### 3-1. API 직접 호출·서버 검증 (관련 API 필수)

상세 기준은 `skills/code-reviewer/references/security-audit.md`의 `API 직접 호출·서버 검증 계약`이다.
프로젝트에 없으면 현재 CLI 활성 루트, 이어서 `SKILLS-CATALOG.md`의 code-reviewer 원본 경로로
해석하고 그 모듈의 참조를 직접 읽는다. source-only를 slash 호출하거나 전역 활성화하지 않는다.
참조 누락은 `NOT RUN`으로 남긴다. 대상 API에 계약 ID별 사례를 매핑하고 기존 QA의 누락을 보충한다.
UI 입력만으로 끝내지 않고 독립 계정의 직접 HTTP 요청(기존 API 테스트 또는 Playwright request)을 실행한다.
정상 대조군·거부 응답·저장/상태/부수 효과의 전후 비교와 실행 증거를 계약 형식으로 남긴다.
기존 증거는 대상 버전·환경·조건이 같을 때 재사용한다. 서버·계정·관찰 수단 부족은 `NOT RUN`이며,
필수 사례 미실행을 전체 PASS로 표시하지 않는다. 명시적 UI-only 범위에서는 API 시험을 확장하지 않고
API 보안 검증 제외를 보고한다. 테스트를 통과시키려고 검증을 제거하거나 거부 기대값을 완화하지 않는다.

### 4. CRUD 엔드포인트 검증

```bash
# CREATE
curl -s -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"테스트 항목","description":"테스트용"}' | jq .

# READ (목록) — 페이지네이션 응답 형태 확인 (items + page/size/total 또는 nextCursor)
curl -s "http://localhost:8000/api/items?page=1&size=20" \
  -H "Authorization: Bearer $TOKEN" | jq '{count: (.items | length), page, size, total, nextCursor}'

# READ (목록) — size 상한: 큰 값을 요청해도 상한 건수 이하만 와야 함
curl -s "http://localhost:8000/api/items?size=1000" \
  -H "Authorization: Bearer $TOKEN" | jq '.items | length'

# READ (목록) — 허용 안 된 정렬 컬럼은 400
curl -s "http://localhost:8000/api/items?sort=password,asc" \
  -H "Authorization: Bearer $TOKEN" -w "\nHTTP: %{http_code}\n"

# READ (단건)
curl -s http://localhost:8000/api/items/1 \
  -H "Authorization: Bearer $TOKEN" | jq .

# UPDATE
curl -s -X PUT http://localhost:8000/api/items/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"수정된 항목"}' | jq .

# DELETE
curl -s -X DELETE http://localhost:8000/api/items/1 \
  -H "Authorization: Bearer $TOKEN" -w "\nHTTP: %{http_code}\n"
```

### 5. 에러 응답 검증

```bash
# 404 Not Found
curl -s http://localhost:8000/api/items/99999 \
  -H "Authorization: Bearer $TOKEN" | jq .

# 400 Bad Request (유효성 검증)
curl -s -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":""}' | jq .

# 409 Conflict (중복)
curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test1234"}' | jq .
```

**에러 응답 포맷 확인:**
```json
{
  "error": "EMAIL_DUPLICATE",
  "message": "사용자 친화적 메시지",
  "details": {}
}
```

`error`는 프론트가 분기하는 대문자 스네이크 코드, `message`는 표시용 문구, `details`는 선택(검증 오류는 `{ "fields": { "email": "INVALID_FORMAT" } }`). 젭마인 `api-spec.md` Conventions의 공통 에러 형식과 같은 형태입니다.

### 6. 파일 업로드 검증

```bash
# 파일 업로드
curl -s -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test-file.pdf" | jq .

# 크기 제한 테스트 (100MB+)
dd if=/dev/zero of=/tmp/large-file.bin bs=1M count=101 2>/dev/null
curl -s -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/large-file.bin" -w "\nHTTP: %{http_code}\n"
rm -f /tmp/large-file.bin
```

### 7. 응답 시간 검증

```bash
# 응답 시간 측정
for endpoint in "/api/health" "/api/users" "/api/items"; do
  TIME=$(curl -s -o /dev/null -w "%{time_total}" \
    http://localhost:8000$endpoint \
    -H "Authorization: Bearer $TOKEN")
  echo "$endpoint: ${TIME}s"
done
```

**기준:** 일반 API < 500ms, 목록 API < 1000ms, 파일 업로드 < 5000ms

---

## 체크리스트

### 필수 (CRITICAL)
- [ ] CORS 설정 올바름 (preflight 통과)
- [ ] 프록시 경로 정상 작동 (`/api/*` → 백엔드)
- [ ] JWT 토큰 발급/검증 정상
- [ ] 에러 응답 포맷 일관적 (`error` 코드 + `message` + `details`)
- [ ] 목록 API 페이지네이션 (offset `page`/`size` + `total` 또는 cursor `nextCursor`), size 상한 동작
- [ ] 목록 API의 허용 안 된 정렬 컬럼 → 400

### 권장 (HIGH)
- [ ] 인증 실패 시 적절한 상태 코드 (401/403)
- [ ] 유효성 검증 실패 시 400 + 상세 메시지
- [ ] 파일 업로드 크기/확장자 제한
- [ ] 응답 시간 기준 충족 (< 500ms)

### 선택 (MEDIUM)
- [ ] Rate Limiting 동작
- [ ] 캐싱 헤더 (ETag, Cache-Control)

---

## 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| CORS 에러 | 백엔드 CORS 미설정 | `Access-Control-Allow-Origin` 추가 |
| 프록시 404 | 경로 불일치 | vite.config/next.config 프록시 경로 확인 |
| 토큰 거부 | 비밀키 불일치 | `.env` SECRET_KEY 일치 확인 |
| 타임아웃 | 서버 미실행 | `docker ps` 또는 프로세스 확인 |
| 413 Payload Too Large | 업로드 제한 | nginx/express body-parser 설정 |
| 목록 API 느림 (> 1000ms) | 필터·정렬 컬럼 인덱스 없음, 행마다 추가 쿼리(N+1), 페이지네이션 없음 | 실행 계획(`EXPLAIN`) 확인 → 인덱스 추가, 조인·일괄 조회, 페이지네이션 적용 |

---

## 보고서 형식

```markdown
# API 연동 테스트 결과

**날짜:** {date}
**환경:** 로컬 / 스테이징 / 프로덕션

## 결과 요약
| 항목 | 상태 | 비고 |
|------|------|------|
| CORS | ✅/❌ | |
| 프록시 | ✅/❌ | |
| 인증 | ✅/❌ | |
| CRUD | ✅/❌ | |
| 에러 응답 | ✅/❌ | |
| 파일 업로드 | ✅/❌ | |
| 응답 시간 | ✅/❌ | |

## 발견된 문제
1. {issue description}
   - **심각도:** Critical / High / Medium
   - **재현:** {steps}
   - **권장 조치:** {fix}
```
