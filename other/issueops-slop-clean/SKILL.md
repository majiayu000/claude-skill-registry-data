---
name: issueops-slop-clean
description: Run the IssueOps ai-slop-clean stage on the canonical worktree. Confirm the phase, remove lazy agent residue from the task diff one pass at a time while preserving behavior, measure before and after with code-quality-metrics, re-run the gate ledger and the focused verification, and record the cleanup evidence that seals the change fingerprint. Use when "issueops next" reports clean, or when the user says "AI slop 정리", "slop 치워줘", "정리 단계".
---

# IssueOps Slop Clean

이 스킬의 일은 **구현이 남긴 찌꺼기를 걷어 내고 그 결과를 봉인하는 것**이다. 넓은
리팩터가 아니라 이번 변경 범위 안의 정리다. 운영 문서 반영과 구현 리뷰는 다음 단계다.

- 전체 흐름과 단계 판별: [`issueops`](../issueops/SKILL.md)
- 게이트 원장: [`gates-ledger`](../gates-ledger/SKILL.md)
- 정리 전후 측정: [`code-quality-metrics`](../code-quality-metrics/SKILL.md)
- 다음 단계: [`issueops-docs`](../issueops-docs/SKILL.md)

## 이 스킬이 맞는지 확인

```bash
issueops next --id "$ISSUEOPS_ID" --json
```

`stage.key`가 `clean`이면 이 스킬이다. `implement`면 아직
[`issueops-implement`](../issueops-implement/SKILL.md)의 출구인
`phase --to ai-slop-clean`을 실행하지 않은 것이므로 그 스킬로 돌아간다.

`stage.key`가 다시 `clean`으로 돌아오는 경우가 있다. 봉인 뒤 어떤 파일이든 바뀌면
`ai_slop_clean_stale`이 되어 이 단계로 되돌아온다. 그것은 오류가 아니라 의도된
회귀다. 바뀐 것을 확인하고 다시 봉인한다.

## 프로젝트 문서 확인

무엇이 slop인지는 저장소의 코드 규칙이 정한다. 정리 프롬프트를 실행하기 **전에**
`.issueops/CONVENTIONS.md`를 읽고 이름·주석·레이어 경계·의존 방향 규칙을 골라 프롬프트의
`<PROJECT_RULES>`에 넣는다. 그 규칙과 아래 분류 표가 충돌하면 저장소 규칙을 따른다.
정리 기록에는 삭제·통합의 근거가 된 규칙을 문서 경로와 함께 적는다.

## 정리 프롬프트

정확히 canonical worktree에서, 구현 단계의 테스트가 최소 한 번 통과한 뒤에 실행한다.

```text
You are running the IssueOps ai-slop-clean phase.

Scope boundary:
- Work only in the expected IssueOps worktree: <EXPECTED_WORKTREE>.
- CLEANUP_BOUNDARY = files in the current task diff plus directly related touched files.
- Every file you edit must be inside CLEANUP_BOUNDARY. A smell found outside it is
  recorded under "Out-of-scope findings" and left untouched. Never widen scope to fix it.

Inputs:
- Issue URL: <ISSUE_URL>
- Plan path: <PLAN_PATH>
- Worktree branch: <BRANCH>
- Diff command: git -C <EXPECTED_WORKTREE> diff --stat && git -C <EXPECTED_WORKTREE> diff
- Verification commands already run: <COMMANDS_AND_RESULTS>
- Project rules from .issueops/CONVENTIONS.md: <PROJECT_RULES>
  These rules win over the generic table below when they conflict.

Step 1 - Lock current behavior before editing:
- Identify what must stay the same inside CLEANUP_BOUNDARY.
- Confirm targeted regression tests exist and pass now. If none cover a piece of
  behavior you intend to touch during cleanup, add the narrowest test first or
  record an explicit verification plan before editing.

Step 2 - Classify the slop before deleting anything:
| Category | Signs |
| --- | --- |
| Dead code | Unused helpers, unreachable branches, stale flags, debug logs, console prints, commented-out blocks |
| Duplication | Repeated logic, copy-paste branches, redundant one-off wrappers |
| Needless abstraction | Pass-through layers, speculative indirection, single-use "flexibility" |
| Boundary violations | Hidden coupling, wrong-layer imports, misplaced responsibilities |
| Weak artifacts | Comments that restate code, vague TODOs, placeholder text, "temporary" scaffolding |
| Unsupported claims | "all", "always", "guarantees", "complete", "safe", "verified", "보장", "완전", "검증됨" without fresh evidence |

Step 3 - Run one pass at a time, safest first, re-running targeted checks between passes:
1. Dead-code deletion (only items provably unused).
2. Duplicate consolidation.
3. Naming, error-message, and comment cleanup: keep comments that explain
   non-obvious domain decisions, invariants, migration constraints, or external
   contracts; remove the rest by the deletion test.
4. Claim audit: search the plan, PR draft, commit notes, and issue body for
   unsupported claims from the table above. Downgrade each to precise wording
   backed by current file evidence, or add the missing verification.
5. Minimality check: could the same acceptance criteria be met with fewer changed
   lines, fewer new names, or less custom machinery? Simplify only when behavior
   preservation is clear.

Do not bundle unrelated refactors into one edit set. If a check fails after a
pass, revert that specific change and continue; do not force it through.

Step 4 - Contract check:
- Re-check public API, schema, migration, permission, runtime, and review-thread
  obligations touched by the diff.
- If endpoint/controller/DTO/schema/OpenAPI behavior changed, run the target
  repo's API-doc command first, then the harness API-doc gate against the worktree.

Step 5 - Fresh evidence:
- Run the smallest relevant tests/checks again after the final pass.
- Record exact commands and outcomes.

Output:
- Changed during ai-slop-clean: files and rationale.
- Removed slop: concrete examples per category.
- Preserved intentionally: suspicious-looking code kept on purpose and why.
- Out-of-scope findings: smells outside CLEANUP_BOUNDARY, listed only.
- Verification: fresh commands and results.
- Project rules applied: each rule that justified a removal, with its doc path.
- Remaining risks or explicit none.
```

## 측정

[`code-quality-metrics`](../code-quality-metrics/SKILL.md)으로 정리 전후를 측정한다. 신호 대 잡음 비율, 중복
비율, boilerplate 비율을 숫자로 남긴다. 측정은 그 스킬 파일을 열어 거기 적힌 셸 레시피(`git diff` 기반)로 한다.
`issueops`에는 품질 측정 명령이 없다(`issueops quality`는 `inspect`뿐이다). 없는 명령을 지어내 적지 않는다.

측정 없이 "더 깔끔해졌다"고 적지 않는다. 측정값이 없으면 그 주장은 검증할 수 없고,
검증할 수 없는 주장은 다음 리뷰가 공격할 대상이 된다.

## 재검증과 증거 확정

정리는 동작을 바꿀 수 있다. 마지막 pass 뒤에 다시 확인한다.

```bash
issueops gates check --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE" --write --json
git -C "$WORKTREE" diff --check
# 변경 범위의 focused 테스트를 다시 실행한다.
```

focused 테스트가 원장의 CHECK에 포함되어 있으면 위 `gates check`의 실행 결과를
사용한다. 같은 pass에서 같은 입력에 같은 테스트를 별도로 한 번 더 실행하지 않는다.

verified-execution report를 확정한다. report는 워크트리 **안**의 정규 파일이어야 하고, 형식은
[`verified-execution`](../verified-execution/SKILL.md)의 보고 계약을 따른다. 이번 변경의 **side effect 목록**과
**성능 측정값**을 반드시 담는다. 링크나 임시 경로가 아니라 커밋될 파일이어야 한다.

## 기록

봉인하기 **전에** 정리 프롬프트 출력의 `Project rules applied` 항목을 verified-execution report의
`## 적용한 문서 규칙` 절에 `| 문서 경로 | 해당 문장 인용 | 이 규칙으로 지운·합친 것 |` 행으로 옮긴다.
아래 명령이 report까지 봉인하므로, 기록 뒤에 옮기면 `ai_slop_clean_stale`이 된다.

```bash
issueops ai-slop-clean record --id "$ISSUEOPS_ID" \
  --category "dead-code" --category "duplication" \
  --verification "go test ./internal/... -count=1 → ok" \
  $RECORD_ACTOR_FLAGS --json
```

`--category`에는 위 분류표의 여섯 이름(`dead-code`, `duplication`,
`needless-abstraction`, `boundary-violation`, `weak-artifact`, `unsupported-claim`)
중 **실제로 제거한 것만** 쓴다. 하지 않은 정리를 적으면 그 기록이 다음 리뷰의 첫 공격
대상이 된다.

이 명령이 change fingerprint를 현재 diff로 봉인한다. fingerprint에는 gates.md, verified-execution
report, 문서까지 **변경된 모든 파일과 untracked 파일**이 들어간다. 그래서 기록 뒤에
어떤 파일이라도 고치면 `ai_slop_clean_stale`이 되어 pr 진입과 create-pr이 막힌다.

- 6단계 [`issueops-docs`](../issueops-docs/SKILL.md)가 운영 문서를 고쳤으면 **그 단계가**
  이 명령을 다시 실행해 재봉인한다.
- 그 밖의 이유로 파일이 바뀌면 `next`가 이 단계로 되돌린다. 되돌아왔으면 무엇이
  바뀌었는지 확인하고 다시 정리·재검증·봉인한다.

## 출구

다음은 [`issueops-docs`](../issueops-docs/SKILL.md)다. 이 단계에서는 커밋하지 않는다.
커밋은 8단계이며, 그 전에 문서 반영과 검증이 fingerprint를 한 번 더 바꾼다.

## 나쁜 예

| 나쁜 행동 | 문제 |
|---|---|
| CLEANUP_BOUNDARY 밖을 리팩터한다 | 이번 변경과 무관한 diff가 섞여 리뷰가 판정할 수 없다. 범위 밖 발견은 목록으로만 남긴다 |
| 재검증 없이 record한다 | 정리가 동작을 바꿨는지 아무도 모른다 |
| 정리 뒤 focused 테스트를 다시 돌리지 않는다 | 마지막 pass가 깬 것을 다음 단계가 발견한다 |
| 측정 없이 "더 깔끔해졌다"고 적는다 | 검증할 수 없는 주장이다 |
| source checkout을 편집한다 | 워크트리 계약 위반이고 fingerprint에도 잡히지 않는다 |
| 근거 없이 "unused"로 판단해 지운다 | 동적 참조나 다른 패키지의 사용을 놓친다. 증명한 것만 지운다 |
| 이 단계에서 커밋한다 | 뒤 두 단계가 fingerprint를 바꾸므로 다시 커밋해야 한다 |

## 검증

- `issueops next --id "$ISSUEOPS_ID" --json`의 `stage.key`가 `docs`이거나
  그 뒤 단계다. 여전히 `clean`이면 `missing`이 무엇이 남았는지 말한다.
- `issueops status --id "$ISSUEOPS_ID" --json`의 `ai_slop_clean_at`,
  `ai_slop_clean_head`, `ai_slop_clean_fingerprint`가 채워져 있다.
- `git -C "$WORKTREE" diff --check`가 통과하고, source checkout의
  `git status --short`가 비어 있다.
- verified-execution report가 워크트리 안 정규 파일로 존재하고 side effect 목록과 성능 측정값을
  담고 있다.
