---
name: auto-validate
description: |
  Next.js 코드 작성 후 자동 검증 (tsc, lint, build). Use when (1) 코드 구현 완료 후,
  (2) PR 생성 전, (3) 커밋 전 검증 필요 시. 모든 검증 통과 시에만 다음 단계 진행.
tools: [Bash, Read]
model: inherit
---

> **시스템 메시지**: `[SEMO] Skill: auto-validate 호출`

# auto-validate Skill

> Next.js 코드 작성 후 자동 검증 (tsc, lint, build)

## Purpose

코드 구현 완료 후 CI/CD 파이프라인 실패를 방지하기 위해 로컬에서 미리 검증합니다.

## Trigger

- `implement` 스킬 완료 후 자동 호출
- 커밋 전
- PR 생성 전
- 사용자 명시적 요청: "검증해줘", "빌드 체크해줘"

## Workflow

### Step 1: TypeScript 컴파일 검사

```bash
# tsc --noEmit 실행
pnpm tsc --noEmit 2>&1 || npm run type-check 2>&1
```

**실패 시**: 타입 오류 목록 출력 → 자동 수정 시도 → 재검증

### Step 2: ESLint 검사

```bash
# lint 실행
pnpm lint 2>&1 || npm run lint 2>&1
```

**실패 시**: lint 오류 목록 출력 → 자동 수정 (`--fix`) → 재검증

### Step 3: 빌드 테스트

```bash
# build 실행
pnpm build 2>&1 || npm run build 2>&1
```

**실패 시**: 빌드 오류 분석 → 수정 제안

### Step 4: 결과 리포트

```markdown
## 검증 결과

| 항목 | 결과 | 소요 시간 |
|------|------|----------|
| TypeScript | ✅ Pass | 2.3s |
| ESLint | ✅ Pass | 1.5s |
| Build | ✅ Pass | 45s |

✅ 모든 검증 통과. 커밋/PR 진행 가능합니다.
```

## Auto-Fix Flow

```text
검증 실패
    ↓
오류 분석
    ↓
자동 수정 시도 (최대 3회)
    ↓
재검증
    ↓
성공 → 계속 진행
실패 → 사용자에게 수동 수정 요청
```

## Quality Gates

### Production Mode (기본값)

| 단계 | 검증 항목 | 필수 |
|------|----------|------|
| Pre-Commit | tsc, lint | ✅ |
| Pre-PR | tsc, lint, build | ✅ |
| Pre-Merge | tsc, lint, build, test | ✅ |

### MVP Mode

| 단계 | 검증 항목 | 필수 |
|------|----------|------|
| Pre-Commit | lint | ⚠️ 권장 |
| Pre-PR | tsc, lint | ⚠️ 권장 |
| Pre-Merge | tsc, lint, build | ✅ |

## Expected Output

```markdown
[SEMO] Skill: auto-validate 호출

=== Next.js 코드 검증 ===

### 1. TypeScript 컴파일 검사
```bash
$ pnpm tsc --noEmit
```
✅ 타입 오류 없음

### 2. ESLint 검사
```bash
$ pnpm lint
```
✅ lint 오류 없음

### 3. 빌드 테스트
```bash
$ pnpm build
```
✅ 빌드 성공 (45.2s)

---

## 검증 결과

| 항목 | 결과 |
|------|------|
| TypeScript | ✅ Pass |
| ESLint | ✅ Pass |
| Build | ✅ Pass |

✅ **모든 검증 통과**

[SEMO] Skill: auto-validate 완료
```

## Error Handling

### 타입 오류 시

```markdown
❌ TypeScript 오류 발견 (3건)

| 파일 | 라인 | 오류 |
|------|------|------|
| src/app/login/page.tsx | 15 | Type 'string' is not assignable to type 'number' |

🔧 자동 수정 시도 중...
```

### Lint 오류 시

```markdown
❌ ESLint 오류 발견 (2건)

| 파일 | 규칙 | 오류 |
|------|------|------|
| src/components/Button.tsx | react-hooks/exhaustive-deps | Missing dependency |

🔧 pnpm lint --fix 실행 중...
✅ 자동 수정 완료. 재검증 중...
```

### 빌드 오류 시

```markdown
❌ 빌드 실패

오류 내용:
- Module not found: Can't resolve '@/lib/utils'

💡 수정 제안:
- 파일 경로 확인: src/lib/utils.ts 존재 여부
- import 경로 수정 필요
```

## Integration

### implement 스킬 연동

```text
implement 스킬 완료
    ↓
auto-validate 자동 호출
    ↓
검증 통과 → 커밋 안내
검증 실패 → 수정 후 재검증
```

### git-workflow 스킬 연동

```text
커밋 요청
    ↓
auto-validate 호출
    ↓
검증 통과 → git commit 실행
검증 실패 → 커밋 차단, 수정 요청
```

## References

- [eng/nextjs CLAUDE.md](../../CLAUDE.md) - Quality Gates 정의
- [implement Skill](../implement/SKILL.md) - 구현 스킬
- [git-workflow Skill](../git-workflow/SKILL.md) - Git 워크플로우
