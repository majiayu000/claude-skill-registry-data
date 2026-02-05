---
name: context-worktree
description: 새 작업 요청 시 기존 작업과의 맥락 유사성을 판단하고, 비유사한 경우 자동으로 git worktree를 생성하여 새 브랜치에서 작업합니다. 작업 시작, 새 기능 구현, 다른 이슈 작업 시 자동 활성화됩니다.
---

# Context Worktree 스킬

## Overview

새로운 작업 요청이 기존 작업과 맥락상 유사한지 판단하고, 비유사한 경우 git worktree를 통해 독립된 브랜치에서 작업하도록 자동 분리하는 스킬입니다.

**핵심 기능:**
- **맥락 유사성 판단**: 파일 경로, 커밋 히스토리, LLM 의미 분석을 통한 종합 판단
- **자동 worktree 생성**: 비유사 판단 시 자동으로 새 worktree 및 브랜치 생성
- **작업 컨텍스트 분리**: 독립적인 작업을 별도 공간에서 진행하여 충돌 방지
- **Git repo 검증**: Git 저장소가 아닌 경우 자동 스킵

**중요**: Git 저장소가 아닌 디렉토리에서는 이 스킬이 적용되지 않습니다.

## When to Use

이 스킬은 다음 상황에서 **자동으로** 활성화됩니다:

**명시적 요청:**
- "새로운 기능 만들어줘"
- "다른 이슈 작업해줘"
- "이 버그 수정해줘" (현재 작업과 무관한 버그)
- "worktree로 분리해줘"

**자동 활성화:**
- 사용자가 구현 요청을 할 때
- 기존 작업 브랜치에서 새로운 작업 시작 시
- 긴급 핫픽스가 필요할 때

**스킵 조건:**
- 현재 디렉토리가 Git 저장소가 아닌 경우
- 이미 해당 작업을 위한 worktree가 존재하는 경우

## Prerequisites

### 도구 요구사항

```bash
# Git 버전 확인 (worktree는 Git 2.5+ 필요)
git --version
```

### 스크립트 설치

```bash
# 스크립트 경로를 PATH에 추가하거나 직접 실행
chmod +x /path/to/agent-skills/development/context-worktree/scripts/context-worktree.sh

# 또는 alias 설정
alias cw='/path/to/agent-skills/development/context-worktree/scripts/context-worktree.sh'
```

### 환경 조건

```bash
# Git 저장소인지 확인
git rev-parse --is-inside-work-tree
```

## Workflow

### 전체 흐름도 (스크립트 사용)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 컨텍스트 수집 (1회 스크립트 호출)                          │
│    └─ context-worktree.sh collect                           │
│       → 구조화된 컨텍스트 정보 반환                          │
├─────────────────────────────────────────────────────────────┤
│ 2. LLM 유사성 판단                                           │
│    └─ 수집된 정보 + 새 요청 비교                             │
├─────────────────────────────────────────────────────────────┤
│ 3. 분기 결정                                                 │
│    ├─ 유사 → 현재 브랜치에서 작업 계속                       │
│    └─ 비유사 → Step 4로                                      │
├─────────────────────────────────────────────────────────────┤
│ 4. Worktree 생성 (1회 스크립트 호출)                          │
│    └─ context-worktree.sh create -b <branch> -d <desc>      │
└─────────────────────────────────────────────────────────────┘

토큰 절약: 6+ 도구 호출 → 1~2회 호출
```

### Step 1: 컨텍스트 수집 (스크립트)

```bash
# 한 번의 호출로 모든 컨텍스트 수집
context-worktree.sh collect
```

**출력 예시:**
```markdown
## Context Summary

| 항목 | 값 |
|------|-----|
| Repository | my-app |
| Current Branch | feature/user-auth |
| Default Branch | main |
| Has Uncommitted | false |
| Active Worktrees | 1 |

### Recent Commits (last 5)
feat(auth): JWT 토큰 생성 로직 추가
feat(auth): 로그인 API 엔드포인트 구현

### Changed Directories
`src/auth,src/middleware`

### Recent Scopes
`auth`
```

수집 정보:
| 항목 | 용도 |
|------|------|
| 브랜치명 | 현재 작업 맥락 파악 (feature/, fix/, hotfix/ 등) |
| 최근 커밋 | scope, type 분석 |
| Changed Directories | 작업 영역 파악 |
| Recent Scopes | Conventional commit scope 패턴 |
| Has Uncommitted | 진행 중 작업 확인 |

### Step 2: LLM 맥락 유사성 판단

#### 2.1 파일 경로 패턴 분석

```
유사 판단 기준:
- 같은 최상위 디렉토리 (src/auth/* ↔ src/auth/*)
- 같은 모듈/기능 영역
- 관련 테스트 파일 (src/auth/* ↔ tests/auth/*)

비유사 판단 기준:
- 완전히 다른 디렉토리 (src/auth/* ↔ src/payment/*)
- 인프라 vs 애플리케이션 (infra/* ↔ src/*)
- 프론트엔드 vs 백엔드 (frontend/* ↔ backend/*)
```

#### 2.2 커밋 히스토리 scope/type 분석

```
유사 판단:
- 같은 scope: feat(auth) ↔ fix(auth)
- 관련 type: feat(auth) ↔ test(auth)

비유사 판단:
- 다른 scope: feat(auth) ↔ feat(payment)
- hotfix vs feature: hotfix/* ↔ feature/*
```

#### 2.3 LLM 의미적 유사성 판단

다음 요소를 종합하여 LLM이 판단:

```markdown
## 현재 작업 컨텍스트
- 브랜치: feature/user-authentication
- 최근 커밋:
  - feat(auth): JWT 토큰 생성 로직 추가
  - feat(auth): 로그인 API 엔드포인트 구현
- 변경 파일: src/auth/*, src/middleware/auth.ts

## 새 요청
"결제 시스템에 카드 결제 기능을 추가해줘"

## 판단
비유사 - 결제 시스템은 인증 시스템과 독립적인 기능 영역
```

#### 2.4 종합 유사성 점수

```
유사성 점수 = (파일 경로 점수 × 0.3) + (커밋 히스토리 점수 × 0.3) + (LLM 판단 점수 × 0.4)

- 0.7 이상: 유사 → 현재 브랜치 유지
- 0.7 미만: 비유사 → 새 worktree 생성
```

### Step 3: Worktree 생성 (스크립트)

비유사로 판단된 경우 스크립트로 worktree 생성:

```bash
# 새 worktree 생성
context-worktree.sh create -b feat/payment-card -d "카드 결제 기능 구현"

# 핫픽스 (main 기반)
context-worktree.sh create -b hotfix/login-bug -d "로그인 버그 수정" -base main
```

**출력 예시:**
```markdown
## Worktree Created

| 항목 | 값 |
|------|-----|
| Branch | feat/payment-card |
| Path | /home/user/projects/my-app-worktrees/feat-payment-card |
| Base | main |

### Next Steps
cd /home/user/projects/my-app-worktrees/feat-payment-card

**Description**: 카드 결제 기능 구현
```

#### 브랜치명 생성 규칙

```
패턴: <type>/<short-description>

예시:
- feat/payment-card-integration
- fix/login-timeout-issue
- hotfix/security-patch
- refactor/database-connection
```

#### Worktree 경로 규칙

```
기본 경로: ../<repo-name>-worktrees/<branch-name>

예시:
- 현재: /home/user/projects/my-app
- worktree: /home/user/projects/my-app-worktrees/feat-payment-card
```

### Step 4: 작업 환경 안내

worktree 생성 후 사용자에게 안내:

```markdown
## 새 Worktree 생성됨

새 작업은 기존 작업과 맥락이 다르므로 별도 worktree를 생성했습니다.

| 항목 | 값 |
|------|-----|
| 브랜치 | feat/payment-card-integration |
| 경로 | /home/user/projects/my-app-worktrees/feat-payment-card-integration |
| 기반 브랜치 | main |

### 다음 단계

해당 worktree에서 작업을 계속하려면:
\`\`\`bash
cd /home/user/projects/my-app-worktrees/feat-payment-card-integration
\`\`\`

또는 현재 세션에서 작업하려면 경로를 변경합니다.
```

---

## Examples

### 예시 1: 유사한 작업 (분리 불필요)

```
현재 상태:
- 브랜치: feature/user-authentication
- 최근 커밋: feat(auth): JWT 토큰 생성 로직
- 변경 파일: src/auth/jwt.ts, src/auth/login.ts

사용자: 로그아웃 기능도 추가해줘

Claude: 맥락 유사성을 판단합니다...

## 유사성 분석 결과

| 기준 | 점수 | 이유 |
|------|------|------|
| 파일 경로 | 1.0 | 같은 src/auth/ 영역 |
| 커밋 히스토리 | 1.0 | 동일 scope (auth) |
| LLM 판단 | 0.9 | 인증 기능의 일부 |
| **종합** | **0.96** | |

→ 유사: 현재 브랜치(feature/user-authentication)에서 작업 계속

[로그아웃 기능 구현 시작...]
```

### 예시 2: 비유사한 작업 (worktree 생성)

```
현재 상태:
- 브랜치: feature/user-authentication
- 최근 커밋: feat(auth): JWT 토큰 생성 로직
- 변경 파일: src/auth/jwt.ts

사용자: 결제 시스템에 카드 결제 기능 추가해줘

Claude: 맥락 유사성을 판단합니다...

## 유사성 분석 결과

| 기준 | 점수 | 이유 |
|------|------|------|
| 파일 경로 | 0.1 | src/payment/ ≠ src/auth/ |
| 커밋 히스토리 | 0.1 | 다른 scope (payment ≠ auth) |
| LLM 판단 | 0.2 | 독립적인 기능 영역 |
| **종합** | **0.14** | |

→ 비유사: 새 worktree 생성

## 새 Worktree 생성됨

| 항목 | 값 |
|------|-----|
| 브랜치 | feat/payment-card-integration |
| 경로 | ../my-app-worktrees/feat-payment-card-integration |
| 기반 브랜치 | main |

worktree로 이동하여 작업을 시작합니다...

[결제 기능 구현 시작...]
```

### 예시 3: 긴급 핫픽스

```
현재 상태:
- 브랜치: feature/dashboard-redesign
- 변경 파일: src/components/Dashboard.tsx (uncommitted)

사용자: 프로덕션에서 로그인이 안 되는 긴급 버그가 있어. 빨리 수정해줘!

Claude: 긴급 핫픽스 요청을 감지했습니다. 맥락 유사성을 판단합니다...

## 유사성 분석 결과

| 기준 | 점수 | 이유 |
|------|------|------|
| 파일 경로 | 0.0 | Dashboard ≠ Auth |
| 커밋 히스토리 | 0.0 | 다른 scope |
| LLM 판단 | 0.1 | 긴급 핫픽스는 별도 처리 필요 |
| **종합** | **0.04** | |

→ 비유사: 새 worktree 생성 (hotfix)

## 새 Worktree 생성됨

| 항목 | 값 |
|------|-----|
| 브랜치 | hotfix/login-critical-bug |
| 경로 | ../my-app-worktrees/hotfix-login-critical-bug |
| 기반 브랜치 | main |

**주의**: 현재 브랜치에 uncommitted 변경사항이 있습니다.
핫픽스 완료 후 원래 브랜치로 돌아가서 작업을 계속하세요.

[핫픽스 작업 시작...]
```

### 예시 4: Git 저장소가 아닌 경우

```
사용자: 새로운 API 엔드포인트 만들어줘

Claude: Git 저장소 확인 중...

⚠️ 현재 디렉토리는 Git 저장소가 아닙니다.
context-worktree 스킬을 스킵하고 일반 작업을 진행합니다.

[API 엔드포인트 구현 시작...]
```

---

## Configuration

### Worktree 경로 커스터마이징

기본 경로 패턴을 변경하려면:

```bash
# 환경 변수로 설정
export WORKTREE_BASE_PATH="/custom/path/worktrees"
```

### 유사성 임계값 조정

```yaml
# ~/.agents/config/context-worktree.yaml (선택적)
similarity:
  threshold: 0.7  # 0.0 ~ 1.0, 높을수록 엄격
  weights:
    file_path: 0.3
    commit_history: 0.3
    llm_judgment: 0.4
```

### 브랜치 네이밍 규칙

```yaml
branch_naming:
  prefix_map:
    feature: "feat"
    bugfix: "fix"
    hotfix: "hotfix"
    refactor: "refactor"
  separator: "/"
  word_separator: "-"
```

---

## Best Practices

**DO:**
- 새로운 독립적 작업 시작 전 맥락 확인
- uncommitted 변경사항이 있으면 먼저 stash 또는 commit
- worktree 작업 완료 후 정리 (`git worktree remove`)
- 브랜치명에 작업 내용을 명확히 표현
- 긴급 핫픽스는 항상 main/master 기반으로 생성

**DON'T:**
- 같은 브랜치를 여러 worktree에서 체크아웃
- worktree 내부에서 다시 worktree 생성
- 완료된 worktree를 정리하지 않고 방치
- uncommitted 변경사항을 무시하고 다른 작업 시작
- 기반 브랜치를 잘못 선택하여 충돌 유발

---

## Troubleshooting

### Worktree 생성 실패

```bash
# 이미 해당 브랜치가 다른 worktree에서 체크아웃된 경우
git worktree list

# 해결: 기존 worktree 제거 또는 다른 브랜치명 사용
git worktree remove /path/to/existing/worktree
```

### Worktree 정리

```bash
# 사용하지 않는 worktree 확인
git worktree list

# worktree 제거
git worktree remove /path/to/worktree

# 또는 강제 제거
git worktree remove --force /path/to/worktree

# 정리 (삭제된 worktree 참조 제거)
git worktree prune
```

### 브랜치 충돌

```bash
# 같은 이름의 브랜치가 이미 존재하는 경우
# 해결: 다른 브랜치명 사용 또는 기존 브랜치 삭제

git branch -d existing-branch  # 머지된 경우
git branch -D existing-branch  # 강제 삭제
```

### uncommitted 변경사항 처리

```bash
# 변경사항 임시 저장
git stash push -m "WIP: 현재 작업"

# 다른 작업 완료 후 복원
git stash pop
```

---

## Integration

이 스킬은 다음 스킬과 연동됩니다:

| 스킬 | 연동 방식 |
|------|-----------|
| git-commit-pr | worktree에서 작업 완료 후 커밋/PR 생성 시 |
| context-manager | 새 worktree에서 컨텍스트 재로드 |

---

## Script Commands

### 스크립트 명령어 요약

```bash
# 컨텍스트 수집 (구조화된 출력)
context-worktree.sh collect

# worktree 생성
context-worktree.sh create -b <branch> [-d <description>] [-base <branch>]

# worktree 목록
context-worktree.sh list

# 정리 (stale 참조 제거)
context-worktree.sh clean

# 도움말
context-worktree.sh help
```

### Git Worktree 네이티브 명령어 참고

```bash
# worktree 목록 확인
git worktree list

# worktree 추가 (새 브랜치)
git worktree add -b <branch> <path> <base-branch>

# worktree 추가 (기존 브랜치)
git worktree add <path> <existing-branch>

# worktree 제거
git worktree remove <path>

# worktree 이동
git worktree move <old-path> <new-path>

# 정리 (prune)
git worktree prune
```

---

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/context-worktree.sh` | 메인 자동화 스크립트 (컨텍스트 수집, worktree 생성) |
