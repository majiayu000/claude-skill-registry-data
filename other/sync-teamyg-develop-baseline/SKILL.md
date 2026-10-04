---
name: sync-teamyg-develop-baseline
description: TEAMYG-Android develop 기준 parfait 문서 점검(반복 워크플로). 사용자가 "/sync-teamyg-develop-baseline", "/sync-tjyg-develop-baseline"(구 이름), "develop 기준 문서 점검", "develop 문서 점검", "parfait 문서 드리프트 점검", "TEAMYG develop delta 감사", "TJYG develop delta 감사", "develop 이전 해시부터 지금까지 diff 확인해 문서 갱신"이라고 할 때 사용. 기준선 이후 신규 머지 delta만 감사해 spec/plan/architecture/adr/open-questions 드리프트 제거.
---

# sync-teamyg-develop-baseline — develop 기준 parfait 문서 점검

TEAMYG-Android `develop`에 새로 머지된 것과 parfait 문서의 드리프트를 제거한다.
**기준선(develop 커밋 해시)의 단일 출처는 `parfait/android/doc-baseline.md`** — 절차 권위도 그 파일. 이 스킬은 실행 순서만 요약한다.

## 핵심 규율
- **전체 재감사 금지** — 기준선 이후 **신규 머지 delta만** 본다(낭비·누락 방지). 드리프트는 대개 문서 `verified` 날짜 **이후 머지된 PR**에서 발생.
- 로컬 절대경로는 개인정보 → `wiki/personal-private/project-paths.md`의 `TEAMYG-Android` 경로(아래 `<T>`).
- 커밋/push/PR은 **CLAUDE.md 규율** — 사용자 확인 후. main 직접 금지, 브랜치→PR→머지.

## 단계

1. **기준선 확인** — `parfait/android/doc-baseline.md` 읽어 현재 기준선 커밋 해시 확보.
2. **최신화 + delta 나열**:
   - `git -C <T> fetch origin develop`
   - `git -C <T> log --oneline --merges <기준선>..origin/develop` (신규 머지 PR/브랜치)
   - 각 머지: `git -C <T> show --stat <merge-hash>` 로 변경 컴포넌트/모듈 파악
   - delta 0건이면 기준선 해시만 갱신하고 종료 보고.
3. **코드 ↔ 문서 대조** — 변경된 심볼(컴포넌트/토큰/시그니처)이 parfait 문서와 어긋나는지:
   - 관련 `specs/`·`plans/`(status·related_code), `architecture/*` 인벤토리, `open-questions.md` "미머지" 항목, `adr/`.
   - 실제 머지 코드는 `git -C <T> show origin/develop:<path>` 로 확인. 선작성 spec/plan이 있으면 설계 vs 실제 코드 라인별 대조.
   - **미머지 심볼 확인**: `git -C <T> ls-tree -r --name-only origin/develop | grep <심볼>`.
4. **드리프트 수정 + 구현 완료분 아카이브**:
   - spec: `status: implemented` + `specs/archive/` 이동. plan: `status: done`(+`archived_reason`) + `plans/archive/` 이동.
   - **이동 시 상대링크 `../` → `../../` 보정**(archive는 한 단계 깊음). 이동 후 링크 resolve 검증.
   - `specs/README.md`·`plans/README.md` active→아카이브 표 등록. 신규 컴포넌트면 spec 신규 작성.
   - 새 드리프트/미결은 `open-questions.md`에 `### [YYYY-MM-DD] 주제` 형식으로 등록(라인번호·색hex 금지, 파일명+심볼명).
5. **기준선 갱신** — `doc-baseline.md` "현재 기준선"을 새 `origin/develop` HEAD로 교체 + 이력 표에 1줄. `index.md`의 doc-baseline 라인(해시·날짜)도 정정. 미머지 추적 항목은 유지.
6. **보고 → 커밋**(사용자 확인 후) — delta 요약·드리프트 건수·조치 목록 보고. 승인 시 브랜치→commit→push→PR→merge, 로컬 main 동기화.

## 경계 — 서버 API 계약과의 분담
`parfait/api/`의 **계약 절**(엔드포인트·요청/응답 필드·에러코드)은 서버가 정본이라
`sync-teamyg-server-api`가 갱신한다. 이 스킬은 그 문서의 **Android 쪽**만 본다 —
develop delta에 원격 연동 코드(Service·Response·RemoteDataSource·`ApiResponse`·`TokenProvider`)가
있으면 아래 **다섯 표면**을 갱신한다.
- 해당 도메인 문서의 `android_status`
- 해당 도메인 문서의 `## Android 매핑` 절
- 해당 도메인 문서 엔드포인트 표의 Android 열(`미구현`/`구현됨`/`⚠️불일치`)
- `parfait/api/conventions.md`의 "Android 불일치" 표 — 델타가 해당 불일치를 해소했으면 이 표에서 제거한다
  (`open-questions.md` 해소 메모가 "여기서 제거한다"고 지시하는 대상이 이 표다)
- `parfait/api/README.md` 도메인 표의 Android 열

**frontmatter `verified` 필드는 서버 계약 대조일로 고정한다** — `sync-teamyg-server-api`만 갱신하고, `sync-teamyg-develop-baseline`의 Android 델타 갱신은 이 필드를 건드리지 않는다(두 스킬 문서에 동일 문구).

## 주의
- `<기준선>..origin/develop` 범위 밖(기준선 이전)은 건드리지 않는다.
- 파르페 규율: SoT는 코드 > wiki > CLAUDE.md. 라인번호·변동수치·색 hex는 문서에 안 적는다.
- 반복 컨텍스트는 메모리 `parfait-doc-baseline-check`에도 있음(포인터, SoT는 `doc-baseline.md`).
