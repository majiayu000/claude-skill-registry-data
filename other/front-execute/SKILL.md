---
name: front-execute
description: 프론트엔드 구현 + UI 검증 루프 + 최종 코드 리뷰를 한 번에 돌리는 파이프라인. 인자로 문서 경로를 받거나, IDE 열린 파일/대화 맥락에서 구현 의도를 추출한다. 호출 시 입력이 불명확하면 AskUserQuestion 으로 직접 물어본다. 트리거 - "front-execute", "프론트 구현하고 검증해줘", "UI 스펙대로 구현하고 마무리", "/front-execute {경로}" 등.
---

# /front-execute — 프론트엔드 구현 + 검증 파이프라인

문서/지시를 입력으로 받아 **구현 → 타입체크/유닛테스트 → UI 검증 루프(자동 수정) → 최종 코드 리뷰 → 요약** 까지 한 번에 진행한다. 프론트엔드 전용 스킬이다.

## 전제

- `react-code-reviewer`, `ui-validator` 서브에이전트가 사용 가능해야 한다 (`~/.claude/agents/` 또는 프로젝트 `.claude/agents/`)
- 산출물은 `.claude/front-execute/` 아래에 저장 (없으면 생성)
- 프론트엔드 변경이 전제. 백엔드 only 변경에는 이 스킬을 호출하지 말 것

## 페이즈

### Phase 1: 입력 해석

**1-a. 인자 우선 탐색**

1. `$ARGUMENTS` 에 문서 경로가 있으면 → 그 파일 Read
2. 없으면 `ide_opened_file` 에 `.md`/`.txt` 류의 플랜/스펙 파일이 열려있는지 확인 → 있으면 "이 파일을 기반으로 진행할까요?" 1회 확인 후 사용
3. 둘 다 없으면 → **AskUserQuestion 으로 입력 소스를 직접 물어본다**:
   - 옵션 1: "문서 경로를 직접 입력" (사용자가 경로 텍스트로 답변)
   - 옵션 2: "대화 맥락에서 자동 추출" (지금까지의 대화에서 의도 추출)
   - 옵션 3: "지금 IDE에 열린 파일 사용" (코드 파일이라도 컨텍스트로 활용)

**1-b. 의도 확정**

- 선택된 소스에서 구현 의도를 1~2문장으로 추출
- 사용자에게 한 줄로 보여주고 진행 확인

### Phase 2: 구현 + 정적 검증

- Phase 1 의 의도를 바탕으로 코드 변경 수행
- TodoWrite 로 작업 단계 추적
- 구현 직후 검증 (**빌드는 생략** — Phase 3 의 ui-validator 가 실제로 앱을 띄우므로 빌드 깨짐은 거기서 잡힘):
  - **타입체크 — 항상 실행**
    - `package.json` 의 `typecheck` / `type-check` / `tsc` 스크립트가 있으면 그것을, 없으면 `npx tsc --noEmit`
  - **유닛테스트 — 휴리스틱 실행**
    - 조건: `package.json` 의 `scripts.test` 존재 **AND** 변경한 코드를 참조하는 테스트 파일 실재 (`**/*.{test,spec}.{ts,tsx,js,jsx}` 또는 `__tests__/`)
    - 둘 다 충족 시 패키지 매니저 추론 (lock 파일 기준) 후 `npm test` / `yarn test` / `pnpm test` 실행
    - 한쪽이라도 없으면 스킵, 그 사실을 Phase 5 요약에 기록
- 실패 시 즉시 수정 (이 시점 수정은 Phase 3 루프와 별개, 명백한 타입/테스트 에러 처리용)

### Phase 3: UI 검증 루프 (최대 5회)

```
for attempt in 1..5:
  ui-validator 서브에이전트 호출
  결과를 .claude/front-execute/ui-validation-{attempt}.md 에 저장
  if STATUS == PASS:
    break
  if STATUS == FAIL:
    실패 시나리오 분석 → 코드 자동 수정 → 다음 시도
else:  # 5회 초과
  멈춤. 사용자에게 실패 시나리오 보고 후 의사결정 요청 (계속 수정 / 종료)
```

- 5회까지 **사용자 개입 없이 자동 수정** 한다
- 스크린샷 증거는 `.claude/front-execute/ui-evidence/` 에 누적
- ui-validator 가 `N/A` 를 반환하면 잘못된 호출(프론트 변경 없음) 가능성 — 사용자에게 확인 요청

### Phase 4: 최종 코드 리뷰 (1회, 병렬 아님)

Task 도구로 `react-code-reviewer` 서브에이전트 호출.

- base branch 와 변경 요약 전달
- 결과 전문을 `.claude/front-execute/review-summary.md` 에 저장
- `STATUS` 분기:

| STATUS | 동작 |
|---|---|
| `PASS` | Phase 5 진행 |
| `ADVISORY` | Minor 이슈를 사용자에게 보여주고 "진행할까요?" 묻기 |
| `NEEDS_FIX` | **멈춤**. Critical/Major 이슈 출력 후 "지금 수정할까요?" 묻기. 동의 시 수정하고 **Phase 3 부터 재시작** |

### Phase 5: 최종 요약

```markdown
# /front-execute 결과

## 입력 소스
- (문서 경로 / IDE 열린 파일 / 대화 의도) 중 무엇이었는지
- 구현 의도: (한 줄 요약)

## ✅ 진행 단계
- Phase 2: 구현 — N개 파일 변경, 타입체크 ✓, 유닛테스트 (실행 / 스킵 사유)
- Phase 3: UI 검증 루프 — N회 시도, STATUS
- Phase 4: 코드 리뷰 — STATUS, 발견 N건

## 📎 산출물
- UI 검증: .claude/front-execute/ui-validation-*.md
- 스크린샷: .claude/front-execute/ui-evidence/
- 리뷰: .claude/front-execute/review-summary.md

## 다음 액션 제안
- (커밋 / PR 생성 / 추가 수정 중 적절한 것)
```

## 운영 규칙

- **사람이 control 에 있다.** Phase 3 루프 5회 초과, Phase 4 NEEDS_FIX 시 반드시 사용자 결정을 받는다.
- Phase 3 루프 안에서의 자동 수정(최대 5회)은 사용자 개입 없이 진행한다.
- 서브에이전트 호출 시 description 에 phase 번호와 base branch 를 명시한다.
- `.claude/front-execute/` 가 없으면 생성한다.
- 사용자가 인자로 추가 컨텍스트를 줬으면 Phase 1-b 의 의도 요약에 반영한다.

## 호출 예시

- "프론트 구현하고 검증해줘"
- "/front-execute docs/dev-process/SPEC.md"
- "UI 스펙대로 구현하고 마무리"
- "이 플랜 파일대로 구현 시작" (IDE 에 플랜 파일이 열린 상태)
