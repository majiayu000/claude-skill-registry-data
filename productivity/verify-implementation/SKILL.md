---
name: verify-implementation
description: 프로젝트의 모든 verify 스킬을 실행하여 통합 패턴 검증 보고서를 생성합니다. 기능 구현 후, PR 전, 코드 리뷰 시 사용.
disable-model-invocation: true
argument-hint: "[옵션: --fix | --report-only | --severity <level> | --category <name> | 특정 verify 스킬 이름]"
---

# 구현 검증

## 목적

프로젝트에 등록된 모든 `verify-*` 스킬을 실행하여 통합 패턴 검증을 수행합니다:

- 각 스킬의 Workflow에 정의된 검사를 실행
- 각 스킬의 Exceptions를 참조하여 false positive 방지
- 발견된 이슈에 severity 레벨 분류
- 사용자 승인 후 수정 적용 및 재검증

## verification-engine과의 역할 구분

| 항목 | verification-engine | verify-implementation (이 스킬) |
|------|-------------------|-------------------------------|
| 대상 | 기술 검증 (빌드, 타입, 린트, 테스트) | 패턴 검증 (코딩 규칙, 아키텍처 패턴, 프로젝트 규약) |
| 트리거 | `/handoff-verify` | `/verify-implementation` |
| 자동 수정 | Fixable 9종 즉시 수정 | 사용자 승인 후 수정 (기본) 또는 `--fix`로 자동 |

두 시스템은 **상호보완**입니다. 기술 검증은 verification-engine에, 패턴 검증은 이 스킬에 위임합니다.

## 실행 시점

- 새로운 기능을 구현한 후
- Pull Request를 생성하기 전
- 코드 리뷰 중
- 코드베이스 규칙 준수 여부를 감사할 때
- `/handoff-verify` 통과 후 패턴 준수 추가 확인 시

## 실행 플래그

| 플래그 | 설명 | 기본값 |
|--------|------|--------|
| `--fix` | 발견 이슈 자동 수정 (사용자 확인 없이) | OFF |
| `--report-only` | 보고서만 생성, 수정 제안 없음 | OFF |
| `--severity <level>` | 특정 심각도 이상만 보고 (CRITICAL/HIGH/MEDIUM/LOW) | LOW (전체) |
| `--category <name>` | 특정 verify-* 스킬만 실행 (예: `--category api`) | 전체 |

## 심각도 레벨

| 레벨 | 설명 | 예시 |
|------|------|------|
| CRITICAL | 즉시 수정 필수. 배포 차단 | 인증 없는 API 엔드포인트, 하드코딩된 시크릿 |
| HIGH | PR 전 수정 권장 | 패턴 위반, 누락된 유효성 검사 |
| MEDIUM | 수정 권장하나 긴급하지 않음 | 네이밍 규칙 불일치, 불필요한 코드 |
| LOW | 개선 제안 | 더 나은 패턴 존재, 문서 보강 필요 |

## 실행 대상 스킬

이 스킬이 실행하는 검증 스킬 목록입니다. `/manage-skills`가 스킬을 생성/삭제할 때 이 목록을 자동 업데이트합니다.

| # | 스킬 | 설명 |
|---|------|------|
| (프로젝트에서 `/manage-skills`로 생성됨) | (프로젝트별 verify-* 스킬은 각 프로젝트에서 동적으로 생성됩니다) | (프로젝트 지침을 참조하세요) |

## 워크플로우

### Step 1: 소개 및 실행 전략 결정

위의 **실행 대상 스킬** 섹션에 나열된 스킬을 확인합니다.

선택적 인수가 제공된 경우:
- 특정 스킬 이름 -> 해당 스킬만 필터링
- `--category <name>` -> `verify-<name>*` 패턴과 매칭되는 스킬만 필터링
- `--severity <level>` -> 모든 스킬 실행 후 해당 심각도 이상만 보고

**등록된 스킬이 0개인 경우:**

```markdown
## 구현 검증

검증 스킬이 없습니다. `/manage-skills`를 실행하여 프로젝트에 맞는 검증 스킬을 생성하세요.
```

이 경우 워크플로우를 종료합니다.

**등록된 스킬이 1개 이상인 경우:**

#### 적응형 실행 전략 결정

```
IF 실행 대상 스킬 수 <= 5:
    -> 순차 실행 (토큰 절약, 컨텍스트 내 직접 실행)
ELSE IF 실행 대상 스킬 수 >= 6:
    -> 병렬 실행 (Task 서브에이전트, fresh context)
```

실행 대상 스킬 테이블과 실행 전략을 표시합니다:

```markdown
## 구현 검증

다음 검증 스킬을 실행합니다:

| # | 스킬 | 설명 |
|---|------|------|
| 1 | verify-<name1> | <description1> |
| 2 | verify-<name2> | <description2> |

**실행 전략:** 순차 실행 (N개 스킬)
**플래그:** --fix / --report-only / --severity HIGH

검증 시작...
```

### Step 2: 스킬 실행

#### 순차 실행 모드 (스킬 5개 이하)

**실행 대상 스킬** 테이블에 나열된 각 스킬에 대해 다음을 수행합니다:

**2a. 스킬 SKILL.md 읽기**

해당 스킬의 `.claude/skills/verify-<name>/SKILL.md`를 읽고 다음 섹션을 파싱합니다:

- **Workflow** -- 실행할 검사 단계와 탐지 명령어
- **Exceptions** -- 위반이 아닌 것으로 간주되는 패턴
- **Related Files** -- 검사 대상 파일 목록

**2b. 검사 실행**

Workflow 섹션에 정의된 각 검사를 순서대로 실행합니다:

1. 검사에 명시된 도구(Grep, Glob, Read, Bash)를 사용하여 패턴 탐지
2. 탐지된 결과를 해당 스킬의 PASS/FAIL 기준에 대조
3. Exceptions 섹션에 해당하는 패턴은 면제 처리
4. FAIL인 경우 이슈를 기록:
   - 파일 경로 및 라인 번호
   - 문제 설명
   - 심각도 레벨 (CRITICAL / HIGH / MEDIUM / LOW)
   - 수정 권장 사항 (코드 예시 포함)

**2c. 스킬별 결과 기록**

각 스킬 실행 완료 후 진행 상황을 표시합니다:

```markdown
### verify-<name> 검증 완료

- 검사 항목: N개
- 통과: X개
- 이슈: Y개 (CRITICAL: a, HIGH: b, MEDIUM: c, LOW: d)
- 면제: Z개

[다음 스킬로 이동...]
```

#### 병렬 실행 모드 (스킬 6개 이상)

Task 도구로 서브에이전트를 생성하여 병렬 실행합니다:

```
각 verify-* 스킬에 대해 Task 서브에이전트 생성:
    - subagent_type: general-purpose
    - model: haiku (비용 최적화)
    - prompt: 해당 스킬의 SKILL.md 전체 내용 + 검사 지시
    - 결과: 이슈 목록 (파일, 라인, 심각도, 수정 방법)
```

모든 서브에이전트 완료 후 결과를 수집합니다.

### Step 3: 통합 보고서

모든 스킬 실행 완료 후, 결과를 하나의 보고서로 통합합니다:

```markdown
## 구현 검증 보고서

### 요약

| 검증 스킬 | 상태 | 이슈 수 | CRITICAL | HIGH | MEDIUM | LOW |
|-----------|------|---------|----------|------|--------|-----|
| verify-<name1> | PASS / FAIL | N | a | b | c | d |
| verify-<name2> | PASS / FAIL | N | a | b | c | d |

**발견된 총 이슈: X개** (CRITICAL: a, HIGH: b, MEDIUM: c, LOW: d)
```

**모든 검증 통과 시:**

```markdown
모든 검증을 통과했습니다!

구현이 프로젝트의 모든 패턴/규칙을 준수합니다:

- verify-<name1>: <통과 내용 요약>
- verify-<name2>: <통과 내용 요약>

코드 리뷰 준비가 완료되었습니다.
```

**이슈 발견 시:**

`--severity` 플래그에 따라 필터링된 이슈만 표시합니다:

```markdown
### 발견된 이슈

| # | 심각도 | 스킬 | 파일 | 문제 | 수정 방법 |
|---|--------|------|------|------|-----------|
| 1 | CRITICAL | verify-<name1> | `path/to/file.ts:42` | 문제 설명 | 수정 코드 예시 |
| 2 | HIGH | verify-<name2> | `path/to/file.tsx:15` | 문제 설명 | 수정 코드 예시 |
```

### Step 4: 사용자 액션 확인

`--fix` 플래그가 지정된 경우 -> Step 5로 바로 이동 (전체 수정)
`--report-only` 플래그가 지정된 경우 -> 보고서만 표시하고 종료

그 외의 경우, 이슈가 발견되면 `AskUserQuestion`을 사용하여 사용자에게 확인합니다:

```markdown
---

### 수정 옵션

**X개 이슈가 발견되었습니다. 어떻게 진행할까요?**

1. **전체 수정** - 모든 권장 수정사항을 자동으로 적용
2. **CRITICAL/HIGH만 수정** - 심각도 HIGH 이상만 자동 적용
3. **개별 수정** - 각 수정사항을 하나씩 검토 후 적용
4. **건너뛰기** - 변경 없이 종료
```

### Step 5: 수정 적용

사용자 선택에 따라 수정을 적용합니다.

**"전체 수정" 또는 `--fix` 선택 시:**

모든 수정을 순서대로 적용하며 진행 상황을 표시합니다:

```markdown
## 수정 적용 중...

- [1/X] verify-<name1>: `path/to/file.ts` 수정 완료 (CRITICAL)
- [2/X] verify-<name2>: `path/to/file.tsx` 수정 완료 (HIGH)

X개 수정 완료.
```

**"CRITICAL/HIGH만 수정" 선택 시:**

CRITICAL과 HIGH 심각도 이슈만 수정합니다.

**"개별 수정" 선택 시:**

각 이슈마다 수정 내용을 보여주고 `AskUserQuestion`으로 승인 여부를 확인합니다.

### Step 6: 수정 후 재검증

수정이 적용된 경우, 이슈가 있었던 스킬만 다시 실행하여 Before/After를 비교합니다:

```markdown
## 수정 후 재검증

이슈가 있었던 스킬을 다시 실행합니다...

| 검증 스킬 | 수정 전 | 수정 후 |
|-----------|---------|---------|
| verify-<name1> | X개 이슈 | PASS |
| verify-<name2> | Y개 이슈 | PASS |

모든 검증을 통과했습니다!
```

**여전히 이슈가 남은 경우:**

```markdown
### 잔여 이슈

| # | 심각도 | 스킬 | 파일 | 문제 |
|---|--------|------|------|------|
| 1 | HIGH | verify-<name> | `path/to/file.ts:42` | 자동 수정 불가 -- 수동 확인 필요 |

수동으로 해결한 후 `/verify-implementation`을 다시 실행하세요.
```

---

## 예외사항

다음은 **문제가 아닙니다**:

1. **등록된 스킬이 없는 프로젝트** -- 오류가 아닌 안내 메시지를 표시하고 종료
2. **스킬의 자체적 예외** -- 각 verify 스킬의 Exceptions 섹션에 정의된 패턴은 이슈로 보고하지 않음
3. **verify-implementation 자체** -- 실행 대상 스킬 목록에 자기 자신을 포함하지 않음
4. **manage-skills** -- `verify-`로 시작하지 않으므로 실행 대상에 포함되지 않음
5. **verification-engine 대상 항목** -- 빌드 오류, 타입 오류, 린트 오류, 테스트 실패는 verification-engine의 영역이며 이 스킬에서 중복 검사하지 않음

## Related Files

| File | Purpose |
|------|---------|
| `~/.claude/skills/manage-skills/SKILL.md` | 스킬 유지보수 (이 파일의 실행 대상 스킬 목록을 관리) |
| `~/.claude/skills/verification-engine/SKILL.md` | 기술 검증 엔진 (상호보완 - 빌드/타입/린트/테스트) |
| 프로젝트 `CLAUDE.md` | 프로젝트 지침 |
| 프로젝트 `.claude/skills/verify-*/SKILL.md` | 개별 검증 스킬 (이 스킬이 실행) |
