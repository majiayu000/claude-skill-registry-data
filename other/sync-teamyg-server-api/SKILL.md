---
name: sync-teamyg-server-api
description: TEAMYG-SERVER main 기준 parfait/api 계약 문서 점검(반복 워크플로). 사용자가 "/sync-teamyg-server-api", "서버 API 문서 점검", "서버 계약 갱신", "TEAMYG-SERVER delta 감사", "서버 API 바뀐 거 문서에 반영해줘"라고 할 때 사용. 기준선 이후 신규 커밋 delta만 감사해 parfait/api 계약 드리프트를 제거한다.
---

# sync-teamyg-server-api — 서버 main 기준 API 계약 문서 점검

TEAMYG-SERVER `main`에 새로 들어온 것과 `parfait/api/` 계약 문서의 드리프트를 제거한다.
**기준선(서버 main 커밋 해시)의 단일 출처는 `parfait/api/server-baseline.md`** — 절차 권위도 그 파일.
이 스킬은 실행 순서만 요약한다.

## 핵심 규율
- **전체 재감사 금지** — 기준선 이후 **신규 커밋 delta만** 본다.
- **브랜치는 `main`.** 서버 기본 브랜치가 main이고 기능 PR이 거기로 머지된다. `develop`은 뒤처진다.
  (TEAMYG-Android는 `develop` 추적 — 헷갈리지 말 것.)
- **워킹트리를 믿지 않는다.** 파일 조회는 항상 `git -C <S> show origin/main:<path>`.
- 로컬 절대경로는 개인정보 → `wiki/personal-private/project-paths.md`의 `TEAMYG-SERVER` 경로(아래 `<S>`).
- **서버 저장소는 read-only.** 커밋·브랜치·수정 일절 금지(fetch만 한다).
- 커밋/push/PR은 **CLAUDE.md 규율** — 사용자 확인 후. main 직접 금지, 브랜치→PR→머지.

## 단계

1. **기준선 확인** — `parfait/api/server-baseline.md` 읽어 현재 기준 커밋 확보.
2. **최신화 + delta 나열**:
   - `git -C <S> fetch origin main`
   - `git -C <S> log --oneline <기준선>..origin/main`
     — **`--merges` 필터를 쓰지 않는다.** 기능 PR이 squash로 들어와 merge 커밋이 아닐 수 있다.
   - 각 커밋: `git -C <S> show --stat <hash>`로 변경 파일 파악
   - delta 0건이면 기준선 해시만 갱신하고 종료 보고.
3. **계약 ↔ 문서 대조** — 아래가 바뀌었는지 본다:
   - 컨트롤러(`*Controller.kt`): 경로·메서드·`@ResponseStatus`·인증 사용 여부
   - DTO(`*Request.kt`·`*Response.kt`): 필드명·타입·널 허용·검증 애노테이션
   - 에러코드 enum(`*ErrorCode.kt`): 추가·삭제·status 변경
   - `SecurityConfig`(화이트리스트) · `ApiResponse`(envelope) · `GlobalExceptionHandler`(errorDetail 채움 여부)
   - **신규 도메인**이면 `parfait/api/template.md`로 문서 신설 + `README.md` 인덱스 등록.
   - 전역 계약이 바뀌었으면 `conventions.md` 갱신.
4. **드리프트 수정** — 해당 도메인 문서의 표·상세 절을 고치고 frontmatter `server_commit`·`verified` 갱신.
   Android 대응 심볼이 있는데 계약과 어긋나면 Android 열을 `⚠️불일치`로 바꾸고
   `parfait/android/synthesis/open-questions.md`에 `### [YYYY-MM-DD] 주제`로 등록한다.
   **기존 도메인의 엔드포인트가 증감했으면**(신규 도메인이 아니어도) `parfait/api/README.md` 도메인 표의
   해당 행 개수·엔드포인트 나열도 함께 갱신한다 — 신규 도메인일 때만 인덱스를 건드리는 게 아니다.
   **`parfait/api/spec/`에 대응 명세 문서가 있으면 그 `## 코드 대조` 절도 다시 돌린다** — 서버가 바뀌면
   "일치 / 코드에만 / 명세에만"의 분류가 이동한다(예: 명세에만 있던 항목이 구현되면 "일치"로 옮겨간다).
   명세 원문 자체는 팀이 고치는 것이지 이 스킬이 고치지 않는다.
5. **기준선 갱신** — `server-baseline.md` "현재 기준선"을 새 `origin/main` HEAD로 교체 + 이력 표에 1줄.
   `parfait/index.md` "지금 상태" 줄의 도메인 건수·엔드포인트 수도 함께 정정한다(이 문서의 도메인 개수를
   갱신하는 스킬은 이것뿐이다).
6. **보고 → 커밋**(사용자 확인 후) — delta 요약·드리프트 건수·조치 목록 보고.

## 경계 — 이 스킬이 하지 않는 것
- **Android 쪽 변화**(구현이 진행돼 `android_status`·Android 매핑 절이 바뀌는 경우)는
  `sync-teamyg-develop-baseline`이 잡는다. 나눔은 이렇다:
  - **서버 delta → 계약 절**(엔드포인트·필드·에러코드) = 이 스킬
  - **Android delta → `android_status`·Android 매핑 절** = `sync-teamyg-develop-baseline`
- TEAMYG-Android 코드 수정은 이 스킬의 일이 아니다.
- **frontmatter `verified` 필드는 서버 계약 대조일로 고정한다** — `sync-teamyg-server-api`만 갱신하고, `sync-teamyg-develop-baseline`의 Android 델타 갱신은 이 필드를 건드리지 않는다(두 스킬 문서에 동일 문구).

## 주의
- 파르페 규율: 라인번호·변동수치·색 hex는 문서에 안 적는다. 근거는 파일명 + 심볼명.
- 확인 못 한 것을 추측해 적지 않는다 — `## 미결`에 남기고 `open-questions.md`에 등록한다.
