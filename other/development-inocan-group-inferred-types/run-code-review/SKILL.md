---
name: run-code-review
description: |
  Next.js 프로젝트 통합 리뷰. review-task 6단계 + semicolon-reviewer 코드 리뷰를
  하나의 워크플로우로 통합 실행합니다. PR에 리뷰 코멘트를 자동 등록합니다.
  Use when (1) "/SEMO:review", (2) "리뷰해줘", "PR 리뷰", (3) "태스크 리뷰", "코드 리뷰".
tools: [Bash, Read, Grep, Glob, Edit]
model: inherit
---

> **호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: run-code-review` 시스템 메시지를 첫 줄에 출력하세요.

# run-code-review Skill

> review-task + semicolon-reviewer 통합 워크플로우

## 워크플로우

### Phase 1-5: 태스크 리뷰 (review-task 기반)

> 📖 상세 검증 로직: [review-task references](../review-task/references/review-phases.md)

#### Phase 1: 메타데이터 검증

```bash
# 이슈 상태 확인
gh issue view {issue} --json title,labels,body

# 브랜치명 규칙 확인: {이슈번호}-{영문-기능명}
BRANCH=$(git branch --show-current)
```

**검증 항목**:
- [ ] Draft 라벨/접두사 제거됨
- [ ] 브랜치명 규칙 준수 (`{issue}-{feature-name}`)
- [ ] 이슈 연결됨

#### Phase 2: 테스트 구조 검증

**검증 항목**:
- [ ] 개발자 테스트와 QA 테스트 분리
- [ ] 테스트 파일 존재 (`*.test.ts`, `*.spec.ts`)
- [ ] 테스트 커버리지 기준 충족

#### Phase 3: 아키텍처 검증 (DDD)

```bash
# DDD 4-layer 구조 확인
ls -la app/{domain}/_{repositories,api-clients,hooks,components}

# 레이어 위반 검색
grep -r "'use client'" app/*/_repositories/  # Repository에 use client 금지
```

**검증 항목**:
- [ ] 4-layer 구조 준수 (`_repositories`, `_api-clients`, `_hooks`, `_components`)
- [ ] 레이어 의존성 위반 없음
- [ ] Server/Client Components 분리

#### Phase 4: 기능 구현 확인 (AC 매칭)

**검증 항목**:
- [ ] Acceptance Criteria 추출
- [ ] 각 AC에 대응하는 구현 확인
- [ ] 누락된 AC 없음

#### Phase 5: 품질 게이트

```bash
npm run lint           # ESLint 검사
npx tsc --noEmit       # TypeScript 타입 체크
npm test               # 테스트 실행
```

**검증 항목**:
- [ ] ESLint 통과
- [ ] TypeScript 컴파일 에러 없음
- [ ] 테스트 통과

---

### Phase 6: 코드 리뷰 (semicolon-reviewer 기반)

> 📖 상세 검증 로직: [semicolon-reviewer references](../../agents/semicolon-reviewer/references/review-phases.md)

#### 6.1 Team Codex Compliance

**검증 항목**:
- [ ] Commit convention 준수
- [ ] ESLint 규칙 준수
- [ ] TypeScript strict mode

#### 6.2 DDD Architecture

**검증 항목**:
- [ ] 4-layer 구조 준수
- [ ] Domain isolation
- [ ] Repository pattern

#### 6.3 Supabase Integration

**검증 항목**:
- [ ] Server client 사용 (SSR)
- [ ] RPC 네이밍 규칙 (`fn_domain_action`)
- [ ] Type safety

#### 6.4 Performance & Best Practices

**검증 항목**:
- [ ] Server Components 우선
- [ ] React Query 캐싱
- [ ] Code splitting

#### 6.5 Security & Accessibility

**검증 항목**:
- [ ] XSS 방지
- [ ] WCAG 2.1 AA 준수
- [ ] 인증/인가 검증

---

### Phase 7: PR 리뷰 등록

#### 7.1 리뷰 결과 종합

| Severity | 조건 | 판정 |
|----------|------|------|
| ✅ APPROVE | Critical 0건 | 승인 |
| 🟡 COMMENT | Critical 0건, Warning 1건+ | 코멘트 |
| 🔴 REQUEST_CHANGES | Critical 1건+ | 변경 요청 |

#### 7.2 PR 리뷰 코멘트 등록

```bash
# PR 번호 조회
PR_NUMBER=$(gh pr list --head $(git branch --show-current) --json number -q '.[0].number')

# 리뷰 등록
gh pr review $PR_NUMBER --{approve|comment|request-changes} --body "$(cat <<'EOF'
## 🔍 SEMO Review: #{issue_number}

### {verdict}

{phase_results_table}

{details}

---
🤖 *SEMO review Skill (eng/nextjs)*
EOF
)"
```

## 출력 포맷

### 리뷰 진행 중

```markdown
[SEMO] Skill: review (nextjs)

📋 이슈: #{issue_number} "{title}"
🔍 PR: #{pr_number}

=== Phase 1-5: 태스크 리뷰 ===

| Phase | 상태 | 요약 |
|-------|------|------|
| 1. 메타데이터 | ✅ | Draft 제거됨 |
| 2. 테스트 구조 | ✅ | 개발자/QA 분리됨 |
| 3. 아키텍처 | ✅ | DDD 준수 |
| 4. 기능 구현 | ✅ | AC 5/5 충족 |
| 5. 품질 게이트 | ✅ | 모두 통과 |

=== Phase 6: 코드 리뷰 ===

| 항목 | 상태 |
|------|------|
| Team Codex | ✅ |
| DDD Architecture | ✅ |
| Supabase | ✅ |
| Performance | ✅ |
| Security | ✅ |
```

### 리뷰 완료

```markdown
## 최종 결과: ✅ APPROVE

모든 검증 항목을 통과했습니다.

PR #{pr_number}에 리뷰 코멘트를 등록합니다...
✅ 리뷰 등록 완료

**다음 단계**:
> PR 머지 후 "테스트 요청" 또는 `/SEMO:change-to-testing`으로 QA에 넘기세요.
```

### 수정 필요 시

```markdown
## 최종 결과: 🔴 REQUEST_CHANGES

다음 Critical 이슈를 해결해야 합니다:

**차단 사유**:
- 🔴 [Phase 3] DDD 레이어 위반: `_repositories/`에 'use client' 사용
- 🔴 [Phase 5] TypeScript 에러 3건

**Warning**:
- 🟡 [Phase 6.4] React Query 캐싱 미적용

PR #{pr_number}에 리뷰 코멘트를 등록합니다...
✅ 리뷰 등록 완료 (REQUEST_CHANGES)
```

## Severity 분류

### Critical (PR 차단)

- Security vulnerabilities
- DDD 아키텍처 위반
- TypeScript/ESLint 에러
- 테스트 실패

### Warning (수정 권장)

- Team Codex 경미한 위반
- 테스트 누락
- Code smell
- 패턴 일탈

### Suggestion (선택적 개선)

- Performance 최적화
- 코드 스타일 개선
- 문서화 보강

## 인자 처리

| 인자 | 설명 | 예시 |
|------|------|------|
| (없음) | 현재 브랜치 PR 리뷰 | `/SEMO:review` |
| `#123` | 특정 이슈 기반 리뷰 | `/SEMO:review #123` |
| `--pr 456` | 특정 PR 리뷰 | `/SEMO:review --pr 456` |
| `--skip-register` | PR 리뷰 등록 생략 | `/SEMO:review --skip-register` |

## References

- [review-task Skill](../review-task/SKILL.md) - 태스크 리뷰 상세 로직
- [semicolon-reviewer Agent](../../agents/semicolon-reviewer/semicolon-reviewer.md) - 코드 리뷰 상세 로직
- [review-phases.md](../review-task/references/review-phases.md) - Phase별 검증 상세
