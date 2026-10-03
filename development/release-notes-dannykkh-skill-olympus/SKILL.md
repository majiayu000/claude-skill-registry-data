---
name: release-notes
description: >
  Conventional Commits 기반 릴리즈 노트 자동 생성. 버전 결정 + CHANGELOG.md + Git 태그 + GitHub Release.
  /release, release, 릴리즈, release-notes, 릴리즈 노트, 버전 올려, changelog 요청에 사용한다.
---

# Release Notes — 릴리즈 노트 자동화

> Conventional Commits에서 버전을 결정하고, CHANGELOG를 생성하고, 태그를 찍는다.
> `commit-work` 스킬로 커밋한 뒤, 릴리즈할 때 사용.

## Quick Start

```
/release                    # 자동 버전 결정 + CHANGELOG + 태그
/release patch              # patch 버전 강제 (0.1.0 → 0.1.1)
/release minor              # minor 버전 강제 (0.1.0 → 0.2.0)
/release major              # major 버전 강제 (0.1.0 → 1.0.0)
/release --dry-run          # 미리보기만 (변경 없음)
/release --no-tag           # CHANGELOG만 생성 (태그 안 찍음)
/release --github           # GitHub Release도 생성
```

**공식 호출명:** `/release` (별칭: `릴리즈`, `릴리즈 노트`, `버전 올려`)

## 파이프라인 위치

```
/commit-work → /release
  커밋 작성      릴리즈 노트 + 버전 + 태그
```

**독립 실행 가능** — 파이프라인 밖에서 단독으로 사용.

---

## CRITICAL: First Actions

### 1. Print Intro

```
Release Notes — 릴리즈 노트 생성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
순서: Analyze → Version → CHANGELOG → Tag → (GitHub Release)
```

### 2. 현재 상태 확인

```bash
# 마지막 태그 확인
git describe --tags --abbrev=0 2>/dev/null || echo "태그 없음 (첫 릴리즈)"

# 마지막 태그 이후 커밋 목록
git log $(git describe --tags --abbrev=0 2>/dev/null)..HEAD --oneline

# 또는 태그 없으면 전체 커밋
git log --oneline
```

상태 출력:

```
📋 현재 상태:
  마지막 버전: v{X.Y.Z} (또는 "없음 — 첫 릴리즈")
  새 커밋: {N}개
  브랜치: {branch}
```

**새 커밋이 0개면:**
```
⚠️ 마지막 태그 이후 새 커밋이 없습니다. 릴리즈할 내용이 없습니다.
```
→ 종료

---

## Phase 1: 커밋 분석

마지막 태그 이후의 모든 커밋을 Conventional Commits 형식으로 파싱합니다.

### 파싱 규칙

```
type(scope): description    →  type, scope, description 추출
```

| Type | 분류 | 버전 영향 |
|------|------|-----------|
| `feat` | Features (새 기능) | **minor** |
| `fix` | Bug Fixes | **patch** |
| `docs` | Documentation | patch |
| `style` | Code Style | patch |
| `refactor` | Refactoring | patch |
| `perf` | Performance | patch |
| `test` | Tests | patch |
| `build` | Build System | patch |
| `ci` | CI/CD | patch |
| `chore` | Miscellaneous | patch |
| `revert` | Reverts | patch |
| `BREAKING CHANGE` | (footer 또는 `!` suffix) | **major** |

### Conventional Commits가 아닌 커밋

Conventional Commits 형식이 아닌 커밋도 수집합니다:
- `Other Changes` 섹션에 포함
- 버전 영향: patch

### 분석 결과 출력

```
📊 커밋 분석:
  feat:     {N}개
  fix:      {N}개
  docs:     {N}개
  refactor: {N}개
  기타:     {N}개
  BREAKING: {N}개
```

---

## Phase 2: 버전 결정

### 자동 결정 (인수 없을 때)

Semantic Versioning (major.minor.patch) 규칙:

| 조건 | 버전 변경 |
|------|-----------|
| `BREAKING CHANGE` 또는 `!` suffix 있음 | **major** (1.0.0 → 2.0.0) |
| `feat` 커밋 있음 | **minor** (1.0.0 → 1.1.0) |
| 그 외 (fix, docs, refactor 등) | **patch** (1.0.0 → 1.0.1) |

### 수동 결정 (인수 있을 때)

```
/release major    →  major 강제
/release minor    →  minor 강제
/release patch    →  patch 강제
/release v2.0.0   →  특정 버전 강제
```

### 첫 릴리즈

태그가 없으면 기본 `v0.1.0`으로 시작. 단, `feat`가 있으면 `v1.0.0`.

### 버전 소스 파일 업데이트

프로젝트에 버전을 관리하는 파일이 있으면 자동 업데이트:

| 파일 | 필드 |
|------|------|
| `VERSION` | 파일 전체를 `X.Y.Z`로 교체 (줄바꿈 포함) |
| `package.json` | `"version": "X.Y.Z"` |
| `pyproject.toml` | `version = "X.Y.Z"` |
| `setup.py` | `version="X.Y.Z"` |
| `*.csproj` | `<Version>X.Y.Z</Version>` |
| `Cargo.toml` | `version = "X.Y.Z"` |
| `build.gradle` | `version = 'X.Y.Z'` |

**없으면 건너뜀** — 에러 아님.

**중요**: `VERSION` 파일은 업데이트 체크 시스템(`scripts/update-check.ps1|sh`)이 참조합니다. 반드시 릴리즈 시 업데이트해야 합니다.

### 버전 확인

```
📌 다음 버전: v{X.Y.Z}
  이유: {feat N개 → minor / BREAKING CHANGE → major / fix만 → patch}
```

현재 CLI의 질문 방식으로 확인:
- "v{X.Y.Z}로 릴리즈합니다. 진행할까요?"
- 옵션: "진행" / "버전 변경" / "취소"

---

## Phase 3: CHANGELOG 생성

### CHANGELOG.md 형식

[Keep a Changelog](https://keepachangelog.com/) 규격을 따릅니다.

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [X.Y.Z] - YYYY-MM-DD

### Breaking Changes
- **scope**: description ([commit-hash])

### Features
- **scope**: description ([commit-hash])

### Bug Fixes
- **scope**: description ([commit-hash])

### Performance
- **scope**: description ([commit-hash])

### Documentation
- **scope**: description ([commit-hash])

### Refactoring
- **scope**: description ([commit-hash])

### Other Changes
- description ([commit-hash])
```

### 생성 규칙

1. **기존 CHANGELOG.md가 있으면**: 맨 위에 새 섹션 추가 (기존 내용 유지)
2. **없으면**: 새로 생성
3. **빈 섹션 제거**: 해당 type의 커밋이 없으면 섹션 자체를 생략
4. **커밋 해시**: 7자리 short hash로 표시
5. **scope**: 있으면 **bold**로 표시, 없으면 생략
6. **날짜**: 오늘 날짜 (YYYY-MM-DD)

### CHANGELOG 출력 미리보기

생성된 내용을 사용자에게 보여줍니다:

```
📝 CHANGELOG.md 미리보기:

## [1.2.0] - 2026-03-16

### Features
- **auth**: JWT 리프레시 토큰 지원 추가 (a1b2c3d)
- **ui**: 다크모드 토글 구현 (e4f5g6h)

### Bug Fixes
- **api**: 페이지네이션 오프셋 계산 오류 수정 (i7j8k9l)

---
{N}개 커밋, {M}개 섹션
```

---

## Phase 4: Git 태그

`--no-tag` 옵션이 아닌 경우 실행.

### 태그 생성

```bash
# 버전 소스 파일이 업데이트되었으면 커밋
git add -A
git commit -m "chore(release): v{X.Y.Z}"

# annotated tag 생성
git tag -a v{X.Y.Z} -m "Release v{X.Y.Z}

{CHANGELOG의 이번 버전 섹션 내용}"
```

### 태그 확인

```
🏷️ 태그 생성: v{X.Y.Z}
  커밋: {short-hash}
  푸시: git push origin v{X.Y.Z} (수동)
```

**자동 push 안 함** — 사용자가 직접 push.

---

## Phase 5: GitHub Release (선택)

`--github` 옵션일 때만 실행. `gh` CLI가 설치되어 있어야 합니다.

### gh CLI 확인

```bash
gh --version 2>/dev/null || echo "gh CLI 미설치"
```

미설치면:
```
⚠️ gh CLI가 설치되어 있지 않습니다. GitHub Release를 건너뜁니다.
  설치: https://cli.github.com/
  또는: --no-github 옵션으로 실행
```

### GitHub Release 생성

```bash
# 태그 먼저 push
git push origin v{X.Y.Z}

# Release 생성
gh release create v{X.Y.Z} \
  --title "v{X.Y.Z}" \
  --notes "$(cat <<'EOF'
{CHANGELOG의 이번 버전 섹션 내용}
EOF
)"
```

---

## Phase 6: 완료 안내

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 릴리즈 v{X.Y.Z} 완료!

📝 산출물:
  CHANGELOG.md    — 업데이트 완료
  Git Tag         — v{X.Y.Z} 생성
  버전 파일       — {package.json 등} 업데이트 (해당 시)

👉 다음 단계:
  git push origin master       → 코드 푸시
  git push origin v{X.Y.Z}     → 태그 푸시
  /release --github             → GitHub Release 생성 (선택)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `patch` / `minor` / `major` | 버전 범프 강제 | 자동 결정 |
| `v{X.Y.Z}` | 특정 버전 강제 | 자동 결정 |
| `--dry-run` | 미리보기만 (파일 변경 없음) | false |
| `--no-tag` | CHANGELOG만 생성 (태그 안 찍음) | false |
| `--github` | GitHub Release도 생성 | false |
| `--no-verify` | 버전 확인 질문 건너뜀 | false |

---

## 예외사항

다음은 **문제가 아닙니다**:

1. **Conventional Commits가 아닌 커밋** — "Other Changes"로 분류, 정상 처리
2. **태그가 하나도 없음** — 첫 릴리즈로 처리 (v0.1.0 또는 v1.0.0)
3. **버전 파일 없음** — 건너뜀, 태그만 생성
4. **gh CLI 미설치** — GitHub Release만 건너뜀, 나머지 정상

---

## 연관 스킬

| 스킬 | 역할 | 연결 |
|------|------|------|
| commit-work | Conventional Commits 작성 | 선행 — 커밋 형식 보장 |
| closer | 최종 산출물 (PRD, 기술문서) | 병렬 — closer 후 release 가능 |
| docker-deploy | Docker 배포 환경 구성 | 후행 — 릴리즈 후 Docker 이미지 빌드 |
| deploymonitor | 배포 실행 (내부용) | 후행 — push 시 자동 배포 |

## Related Files

| 파일 | 역할 |
|------|------|
| `skills/commit-work/SKILL.md` | Conventional Commits 작성 워크플로우 |
| 이 스킬의 `CHANGELOG.md` 형식 | CHANGELOG 생성 계약 |
