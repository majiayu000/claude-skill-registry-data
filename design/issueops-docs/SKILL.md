---
name: issueops-docs
description: Reflect a finished IssueOps implementation into the project's operating documents. Route the diff to the .issueops documents it touches, check both directions (did the change break a documented rule, and did it create a decision, pitfall, command, or convention the documents do not know yet), update ADR, CAUTIONS, CONVENTIONS, ARCHITECTURE, TESTING, OPERATIONS, TECH_STACK, OPEN_API_SPEC, or DESIGN through the project_docs MCP contract, re-seal the ai-slop-clean fingerprint, and record the project-docs-review verdict. Use when "issueops next" reports docs, or when the user says "문서 반영", "ADR 남겨줘", "주의사항 기록", "update the project docs".
---

# IssueOps Docs

이 스킬의 일은 **끝난 구현을 운영 문서에 반영하는 것**이다. 코드는 고치지 않는다.
문서만 고치고, 그 수정이 바꾼 봉인을 다시 맞춘 뒤 판정을 기록한다.

- 전체 흐름과 단계 판별: [`issueops`](../issueops/SKILL.md)
- 문서 갱신 절차: [`project-docs-update`](../project-docs-update/SKILL.md)
- 이전 단계: [`issueops-slop-clean`](../issueops-slop-clean/SKILL.md)
- 다음 단계: [`issueops-verify`](../issueops-verify/SKILL.md)

## 이 스킬이 맞는지 확인

```bash
issueops next --id "$ISSUEOPS_ID" --json
```

`stage.key`가 `docs`면 이 스킬이다. `clean`이면 정리와 봉인이 아직이므로
[`issueops-slop-clean`](../issueops-slop-clean/SKILL.md)으로 돌아간다.

## 왜 이 단계가 정리 뒤에 오는가

문서에 남길 결정과 함정은 **정리가 끝난 최종 diff**에서 확정된다. 구현 도중에 적으면
정리가 지운 것을 문서가 설명하게 된다.

동시에 문서 수정은 파일 변경이므로 정리 단계의 fingerprint 봉인을 stale로 만든다.
그래서 재봉인은 이 단계가 소유한다. 문서를 고치고 재봉인하지 않으면
`ai_slop_clean_stale`로 다음 단계가 전부 막힌다.

`.issueops/AGENT_WORKFLOW.md`의 Work 절은 작업 도중에도 ADR·CAUTIONS를 append하라고
한다. 두 규칙은 충돌하지 않는다. 4단계 구현 중의 append는 정리 봉인보다 앞서므로 그대로
두고, 이 단계에서는 그 append가 최종 diff와 맞는지 다시 대조한다. 5단계 봉인 뒤에 생긴
append는 이 단계의 재봉인이 흡수한다. 7단계 이후의 append는 두 봉인을 모두 stale로
만들므로 `next`가 이 단계로 되돌린다.

## 1 라우팅

구현 diff 요약을 만들어 읽을 문서를 고른다. 요약에는 변경 파일 목록, 새로 생긴
명령·플래그·구조, 작업 중 만난 함정을 넣는다. UI·스타일을 바꿨으면 그 사실도 적는다.
`project_docs_route`는 요약에 `ux`·`style`·`css`·`theme`·`디자인`·`화면`·`스타일` 같은 단어가 있어야 `DESIGN.md`를 고른다.

```bash
git -C "$WORKTREE" diff --stat "$BASE_SHA"
# MCP: project_docs_route에 위 요약을 넣어 문서를 고른다.
# MCP: project_docs_read로 각 문서의 현재 content와 SHA를 받는다.
```

MCP를 쓸 수 없으면 같은 요약으로 `issueops project route-docs --repo "$WORKTREE" --task "<요약>" --json`을
실행한다. MCP와 같은 라우터라서 고르는 문서도 같다.

route 결과는 **더하는** 후보이고 아래 네 문서를 대신하지 않는다. 2절의 문서 → 구현 대조에 쓰는
`CONSTITUTION.md`, `CONVENTIONS.md`, `ARCHITECTURE.md`, `CAUTIONS.md`는 route가 무엇을 돌려주든 직접
열고, 5절 판정 기록의 `--reviewed-doc`에 실제로 연 문서만 넣는다. 네 문서 중 열지 않은 것이
있으면 판정을 기록하지 않는다.

## 2 양방향 대조

한 방향만 보면 절반을 놓친다.

**문서 → 구현.** CONSTITUTION, CONVENTIONS, ARCHITECTURE, CAUTIONS가 정한 것을 이번
diff가 어겼는가. 문서를 고치기 **전에** 네 문서와 그 색인이 넘기는 모듈에서 이 diff가 닿는 규칙을 찾아
verified-execution report의 `## 문서 → 구현 대조` 절에
`| 문서 경로 | 규칙 문장 인용 | 지킴 또는 어김 | diff의 근거 위치 |` 한 행씩 적는다. 어김이 하나라도
있으면 **문서가 아니라 구현을 고친다.** 이때는 3절로 가지 않고 4단계
[`issueops-implement`](../issueops-implement/SKILL.md)로 돌아간다. 규칙을 지키기 어렵다는
이유로 규칙을 고치는 것은 이 단계의 권한이 아니다. 기존 규칙 문장을 바꾸거나 지우는 수정은
계획의 `## 적용되는 결정과 주의사항`이나 기존 ADR이 그 규칙 변경을 이미 결정했을 때만 하고, 그 근거
경로를 표의 근거 칸에 적는다. 근거가 없으면 그 규칙은 어김이다.

**구현 → 문서.** 이번 변경이 문서가 아직 모르는 것을 만들었는가.

- 구조 결정이나 대안 기각 사유가 생겼다 → ADR
- 다시 밟을 함정이나 재발한 문제를 해결했다 → CAUTIONS
- 새 명령·플래그·컨벤션·모듈 경계가 생겼다 → CONVENTIONS 또는 ARCHITECTURE
- 검증 방식이 바뀌었다 → TESTING
- 설치·실행·배포·운영 절차가 바뀌었다 → OPERATIONS
- 의존성·런타임·도구 버전이 바뀌었다 → TECH_STACK
- API 문서화 게이트나 endpoint·DTO 문서 규칙이 바뀌었다 → OPEN_API_SPEC
- UI·디자인 토큰·컴포넌트 상태가 바뀌었다 → DESIGN(`.issueops/DESIGN.md`가 있는
  클라이언트 저장소만). 루트 `DESIGN.md`가 원본이면 토큰을 복제하지 않고 그 문서를 가리킨다.

계획의 `## 적용되는 결정과 주의사항` 절과 대조한다. 계획 때 몰랐던 항목이 이 단계에서
찾은 것이고, 그것을 evidence에 적는다.

## 3 문서 수정

[`project-docs-update`](../project-docs-update/SKILL.md)를 호출한다. 도구는 셋이다.

| 대상 | 도구 |
|---|---|
| 결정 | `project_docs_append(kind=adr)` |
| 함정·주의사항 | `project_docs_append(kind=caution)` |
| 기존 문서의 내용 변경 | `project_docs_revise` (SHA-CAS, 한 문서씩) |

ADR은 append-only다. 기존 항목을 고치지 않고, 뒤집는 결정이면 그것을 새 항목으로
적는다.

하네스 저장소에서 `.issueops/*.md`를 고쳤으면 응답 계약 골든이 드리프트한다.
같은 단계에서 재생성한다.

```bash
go test ./cmd/issueops/issueopsapp -run TestResponseContractsGolden -update -count=1
```

대상 저장소에 그 골든이 없으면 이 줄은 해당 없음이다.

## 4 재봉인

문서를 하나라도 고쳤으면 변경된 문서·프롬프트·계약에 필요한 검증을 실행한 뒤 정리
단계의 봉인을 다시 맞춘다. 실행된 프롬프트나 생성 계약도 바뀔 수 있으므로 문서라는
이유만으로 이전 검증이 여전히 유효하다고 간주하지 않는다.

```bash
issueops ai-slop-clean record --id "$ISSUEOPS_ID" \
  --category "<5단계와 같은 category>" \
  --verification "<문서 변경 뒤 실행한 검증 명령·결과>" $RECORD_ACTOR_FLAGS --json
```

category는 정리 단계와 같다. 이전 코드 검증의 명령·시점·대상을 보존하고, 새 fingerprint에
대해 실행한 결과로 바꿔 적지 않는다. 재봉인 자체는 테스트 실행 증거가 아니다. 7단계가
`issueops-verify`의 조건으로 필요한 나머지 검사를 결정한다. 고친 문서가 없으면 재봉인하지 않는다.

## 5 판정 기록

```bash
issueops project-docs-review record --id "$ISSUEOPS_ID" \
  --verdict updated --doc "<고친 문서 경로>" --doc "<고친 문서 경로>" \
  --evidence "<무엇을 대조했고 왜 이 문서를 고쳤는가>" $RECORD_ACTOR_FLAGS --json

# 고칠 것이 없을 때
issueops project-docs-review record --id "$ISSUEOPS_ID" \
  --verdict no-change \
  --reviewed-doc "<1절에서 실제로 읽은 문서 경로>" --reviewed-doc "<1절에서 실제로 읽은 문서 경로>" \
  --evidence "<대조한 문서와 판단>" $RECORD_ACTOR_FLAGS --json
```

- `updated`는 `--doc` 경로가 **실제 변경 집합 안에** 있어야 통과한다. 고쳤다는
  자기신고만으로는 통과하지 않는다.
- `no-change`는 `--doc`을 받지 않는다. 대신 실제로 읽은 문서를 `--reviewed-doc`으로
  하나 이상 적어야 통과한다. 경로는 `.issueops/` 아래이거나 루트 `AGENTS.md`여야 하고
  지금 존재해야 한다. "대조했으나 없음"과 "대조하지 않음"을 코드가 구분하는 근거가
  이 경로 목록이다. `updated`에도 같은 규칙으로 `--reviewed-doc`을 덧붙일 수 있다.
- 이 기록도 변경 집합 fingerprint를 봉인한다. 이후 diff가 바뀌면
  `project_docs_review_stale`이 되고 `next`가 이 단계로 되돌린다.

## 출구

다음은 [`issueops-verify`](../issueops-verify/SKILL.md)다. 이 단계에서는 커밋하지 않는다.

## 나쁜 예

| 나쁜 행동 | 문제 |
|---|---|
| 문서를 고치지 않고 `--verdict updated` | `--doc`이 변경 집합에 없어 거부된다 |
| 변경 집합 밖 문서를 `--doc`에 적는다 | 같은 이유로 거부된다. 이번에 고친 것만 적는다 |
| 문서를 고치고 재봉인을 생략한다 | `ai_slop_clean_stale`로 이후 단계가 전부 막힌다 |
| 구현이 규칙을 어겼는데 규칙을 고쳐 덮는다 | 문서가 코드를 따라가면 문서는 아무것도 제약하지 못한다 |
| ADR의 기존 항목을 고친다 | ADR은 append-only다. 뒤집는 결정은 새 항목으로 적는다 |
| `no-change`를 `--reviewed-doc` 없이 기록한다 | 거부된다. 읽지 않은 것과 읽었는데 없는 것을 구분할 수 없다 |
| 존재하지 않거나 `.issueops/` 밖의 경로를 `--reviewed-doc`에 적는다 | 거부된다. 읽은 project doc만 적는다 |
| 이 단계에서 코드를 고친다 | 그 변경은 정리와 검증을 다시 통과해야 한다. 4단계로 돌아간다 |

## 검증

- `issueops status --id "$ISSUEOPS_ID" --json`의 `project_docs_review`에
  이번 판정이 있고 `reviewed_fingerprint`가 현재 변경 집합과 같다.
- `issueops next --id "$ISSUEOPS_ID" --json`의 `stage.key`가 `verify`이거나
  그 뒤 단계다. `docs`나 `clean`으로 남아 있으면 `missing`이 이유를 말한다.
- `verdict updated`로 기록했으면 `git -C "$WORKTREE" status --porcelain`에 그 문서들이
  보인다.
