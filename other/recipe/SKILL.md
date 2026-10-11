---
name: recipe
description: >
  프로젝트에서 잘 만든 것을 다른 프로젝트에서 다시 쓰도록 레시피로 수확하고, 찾아서 적용한다.
  레시피 한 건은 LLM이 읽는 설명서(recipe.md — 이른바 llm.md)와 혼자 실행되는 견본(sample/)의 쌍이다.
  UI(팝업·표·폼), 백엔드(인증·웹훅·업로드·페이지네이션), MCP 도구, 인프라(Docker·CI·스크립트)를 모두 다룬다.
  라이브러리는 이 레포 밖의 개인 폴더(CODE_RECIPES_DIR, 기본 ~/code-recipes)에 둔다.
  /recipe, 레시피, 레시피로 뽑아줘, 레시피 수확, llm.md로 추출, 레시피 찾아줘, 레시피 적용 요청에 사용한다.
---

# Recipe — 레시피 수확과 적용

> 코드는 다시 만들 수 있지만, 왜 그렇게 만들었는지와 어디서 데였는지는 다시 만들 수 없다.
> 레시피는 그 둘을 견본 코드와 함께 묶어 다음 프로젝트로 옮긴다.

LLM은 설명만 보고는 정확히 재현하지 못하고, 코드만 보고는 언제 쓰는지·왜 그런지 모른다. 그래서 레시피는
**설명서(`recipe.md`) + 혼자 실행되는 견본(`sample/`)** 한 쌍이다. 디자인만이 아니라 백엔드·MCP·인프라도
같은 방식으로 다룬다 — 백엔드는 "한 번 데여서 알게 된 것"이 코드에 숨어 있어 오히려 얻는 것이 크다.

## Quick Start

```
/recipe harvest <파일·폴더·컴포넌트>   # 수확: 고르기 → 떼어내기 → 설명서 → 견본 검증 → (재현 검사) → 등록
/recipe find <단어...>                  # 라이브러리 검색
/recipe use <id>                        # 현재 프로젝트에 적용
/recipe list                            # 전체 목록 (index.md)
/recipe where                           # 라이브러리 위치
```

자연어로도 시작한다: "이 팝업 레시피로 뽑아줘", "llm.md로 추출해줘", "업로드 처리 레시피 있나 찾아줘".

## 라이브러리

| 항목 | 내용 |
|------|------|
| 위치 | 환경 변수 `CODE_RECIPES_DIR`, 없으면 `~/code-recipes`. Claude·Codex·Antigravity·Grok·Devin이 같은 경로를 쓴다(Grok·Devin은 Claude 설치본의 이 스킬을 그대로 읽는다) |
| 두지 않는 곳 | 이 레포(공개 저장소)와 작업 중인 프로젝트 안 — 내 프로젝트 코드가 공개되거나 프로젝트마다 갈라진다 |
| 생성 | 처음 수확할 때 `init`으로 만든다. 버전 이력이 필요하면 사용자가 원할 때 그 폴더를 private git 저장소로 만들 수 있다(자동으로 하지 않음) |
| 도구 | `node <module_root>/scripts/recipe-lib.js <where\|init\|index\|check <dir>\|search <단어...>>` — `module_root`는 이 `SKILL.md`가 있는 폴더 |

```
~/code-recipes/
  index.md              ← recipe-lib.js index가 만드는 목록 (손으로 고치지 않음)
  ui/  backend/  mcp/  infra/
    <id>/
      recipe.md         ← LLM이 읽는 설명서
      sample/           ← 혼자 실행되는 견본
      source/           ← (선택) 원래 프레임워크로 쓴 구현
```

`recipe.md` 양식, 종류별 견본 규칙, 떼어내기 체크리스트는 [references/recipe-format.md](references/recipe-format.md)가 정본이다.

## 수확 (harvest)

1. **고르기** — 대상이 실제로 동작이 검증됐고, 다시 만들 일이 있거나 만들 때 시행착오가 있었던 것인지 본다.
   아니면 이유를 말하고 수확하지 않는 쪽을 제안한다. 종류(`ui`·`backend`·`mcp`·`infra`)와 id(소문자·하이픈)를 정한다.
   **사용 범위(`reuse`)는 사용자에게 확인한다** — 회사 코드를 개인 라이브러리로 옮겨도 되는지는 에이전트가 판단할 수 없다.
   이것이 수확의 유일한 필수 질문이다.
2. **떼어내기** — 원래 프로젝트의 흔적을 지운다: 브랜드 값·고유 설정 → 토큰·설정 변수, 실데이터·API 호출 → 가짜 데이터·인터페이스,
   비밀값·개인정보·회사 고유 문구 삭제. 체크리스트는 형식 문서의 `## 떼어내기`.
3. **설명서** — `recipe.md`를 양식대로 쓴다. 가장 값진 부분은 `## 결정과 이유`와 `## 함정`이다. 프로젝트의 Mnemo 기억
   (`memory/gotchas/`·`learned/`·`architecture/`), 커밋 메시지, 코드 주석에서 가져오고 근거를 적는다. 근거가 없으면
   지어내지 말고 "기록 없음"이라고 쓴다.
4. **견본과 검증** — `sample/`이 원래 프로젝트 없이 혼자 실행되게 만들고 실제로 실행한다. ui는 브라우저 렌더(콘솔 에러 0,
   상태 전환, 키보드, 다크 모드, 모바일 폭), backend·mcp는 테스트 통과, infra는 dry-run이나 lint. 결과를 `## 견본`의
   `검증:` 줄에 명령·결과·날짜로 적는다. 실행할 수 없으면 `검증: NOT RUN — <이유>`로 적고 그대로 보고한다.
5. **재현 검사** (처음 수확하거나 크게 바꿀 때 권장) — 맥락을 모르는 네이티브 작업자(Claude `general-purpose`·Codex `worker`·
   Gemini `generalist`·Grok `general-purpose`·Devin `run_subagent`의 `subagent_general` — 파일을 만들고 테스트를 돌려야 하므로
   포그라운드로, 백그라운드는 미리 허용된 도구만 쓴다)에게 `recipe.md`와 `sample/`만 주고 빈 폴더나 다른 스택에서 다시 만들게 한다.
   작업자를 띄울 수 없는 환경이면 메인 대화에서 recipe.md와 sample만 다시 읽고 순차로 재현하되, 맥락이 섞였다는 한계를 `## 견본`에 적는다.
   막힌 곳과 다르게 만든 곳이 설명서의 빈틈이다. 보완한 뒤 `## 견본`에 재현 검사 결과를 한 줄 남긴다.
6. **등록** — 라이브러리에 넣고 `check`를 통과시킨다(오류 0, 경고는 하나씩 확인). 그다음 `index`로 목록을 다시 만든다.
   같은 id가 이미 있으면 `version`을 올리고 `## 변경 이력`에 무엇을 왜 바꿨는지 한 줄 남긴다.

## 찾기와 목록 (find, list)

`search <단어...>`로 `index.md`에서 모든 단어가 들어간 행을 찾는다. 고른 레시피는 `recipe.md`를 읽고
"언제 쓰나 / 쓰지 않을 때"와 함께 요약한다. `list`는 `index.md`를 그대로 보여 준다.

## 적용 (use)

1. `recipe.md` 전체와 `sample/`을 읽는다.
2. **현재 프로젝트의 스택과 규약으로 다시 구현한다.** DESIGN.md 토큰, `api-spec.md` Conventions, `mcp-spec.md` 규약,
   기존 코드 패턴을 따른다. 견본을 통째로 붙여 넣지 않는다 — 견본은 기준이지 부품이 아니다.
3. 출처를 남긴다: 구현의 진입 파일 주석이나 설계 문서(섹션 파일, DESIGN.md)에 `recipe: <id>@<version>`.
   나중에 레시피가 개선되면 옛 버전을 쓰는 프로젝트를 이 표시로 찾는다.
4. 레시피의 `## 계약`과 `## 상태와 흐름`을 현재 프로젝트의 테스트·화면으로 확인한다.
5. 적용하면서 더 나아진 점이 있으면 다시 수확(버전 올림)을 제안한다.

## 다른 스킬과의 연결 (읽기만)

| 스킬 | 언제 라이브러리를 읽나 |
|------|------------------------|
| design-plan (아프로디테) | Phase 0-1 기존 자산 확인 — `ui` 레시피 |
| frontend-design | 레시피 우선 단계 — 내장 스타일 레시피보다 내 `ui` 레시피를 먼저 |
| zephermine (젭마인) | 섹션 작성 — 맞는 레시피를 섹션에 `recipe: <id>@<version>`과 경로로 참조(복사하지 않음) |
| workpm (다이달로스) | Phase 1 리서치 — 기존 구현 탐색과 함께 라이브러리 검색 |

라이브러리가 없으면 이 단계들은 조용히 건너뛴다.

## 하지 않는 것

- 라이브러리를 이 레포나 작업 중인 프로젝트 안에 만들지 않는다
- 실행해 보지 않은 코드를 검증된 레시피처럼 등록하지 않는다 (`NOT RUN`이면 그렇게 적는다)
- 레시피를 새 프로젝트에 통째로 복사하지 않는다
- 비밀값·실데이터·개인정보를 수확하지 않는다
- 라이브러리 폴더에 `git init`·push를 자동으로 하지 않는다

## Related Files

| 파일 | 역할 |
|------|------|
| `skills/recipe/references/recipe-format.md` | `recipe.md` 양식, 종류별 견본 규칙, 떼어내기 체크리스트, 사용 범위 값 |
| `skills/recipe/scripts/recipe-lib.js` | 라이브러리 위치·생성·목록 재생성·검사·검색 |
| `skills/design-plan/SKILL.md` | Phase 0-1에서 `ui` 레시피 확인 |
| `skills/frontend-design/SKILL.md` | 레시피 우선 단계에서 내 `ui` 레시피 확인 |
| `skills/zephermine/references/section-splitting.md` | 섹션에 레시피 참조 |
| `skills/orchestrator/commands/workpm.md` | Phase 1 리서치에서 레시피 검색 |
| `scripts/tests/recipe-contract.test.js` | 도구 동작과 연결 지점 계약 테스트 |
