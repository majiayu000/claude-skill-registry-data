---
name: trigger-deploy
description: |
  **GitHub Actions 기반** 프로젝트 배포 (Milestone Close → CI/CD 트리거).
  Use when:
  (1) 프로젝트 별칭 + 환경 (예: "랜드 stg 배포", "오피스 prd 배포"),
  (2) Milestone 기반 릴리즈 관리,
  (3) GitHub Actions CI/CD 배포,
  (4) "stg에 뭐 올라가있어?", "prd 최신 버전".
  ⚠️ Docker/SSH 직접 배포는 deploy-service 사용.
tools: [Read, Bash, mcp__github__*]
model: inherit
---

> **🔔 호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: trigger-deploy` 시스템 메시지를 첫 줄에 출력하세요.

# trigger-deploy Skill

> **GitHub Actions 기반** 프로젝트 별칭 기반 배포 및 상태 조회
>
> ⚠️ **deploy-service와 혼동 주의**: Docker/SSH 직접 배포가 필요하면 `deploy-service` 사용

## 🔴 trigger-deploy vs deploy-service 선택 기준

| 조건 | 선택 스킬 | 이유 |
|------|----------|------|
| 프로젝트 별칭 사용 (랜드, 오피스 등) | `deployer` | projects.md에 별칭 등록 |
| "Milestone", "릴리즈" 언급 | `deployer` | GitHub 릴리즈 워크플로우 |
| GitHub Actions 기반 배포 | `deployer` | CI/CD 자동 트리거 |
| "Docker 빌드", "PM2" 언급 | `deploy-service` | SSH 직접 제어 |
| SSH 접근 필요한 직접 배포 | `deploy-service` | 원격 서버 직접 접근 |
| ms-* 마이크로서비스 배포 | `deploy-service` | Docker + PM2 방식 |

## Semicolon 브랜치 전략

| 환경 | 브랜치/태그 | 트리거 | 설명 |
|------|-------------|--------|------|
| DEV | `dev` | push | 개발 환경 (기본 브랜치) |
| STG | `release-x.x.x` | Milestone Close | 마일스톤 기반 릴리즈 브랜치 |
| PRD | `vx.x.x` 태그 | Production Tagging | 릴리즈 태그 |

## 프로젝트 별칭 참조

**반드시 먼저 읽을 파일**: `.claude/memory/projects.md`

이 파일에서 프로젝트 별칭과 배포 방법을 확인합니다.

## Workflow

### 1. 프로젝트 식별

```
입력: "랜드 stg 배포해줘"

1. .claude/memory/projects.md 읽기
2. "랜드" → semicolon-devteam/cm-land 매핑
3. "stg" → Milestone close 방식 확인
```

### 2. 환경별 배포 절차

#### DEV 배포
```bash
# dev 브랜치 상태 확인 및 push
gh api repos/{owner}/{repo}/branches/dev
```

#### STG 배포
```bash
# 1. 열린 Milestone 목록 조회
gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.state=="open")'

# 2. 사용자에게 Milestone 선택 요청

# 3. Milestone Close
gh api repos/{owner}/{repo}/milestones/{number} -X PATCH -f state=closed
```

#### PRD 배포
```bash
# 1. 열린 Milestone 조회
gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.state=="open")'

# 2. source-tag 라벨 확인/추가
gh api repos/{owner}/{repo}/labels --jq '.[].name' | grep source-tag

# 3. Milestone에 라벨이 연결된 이슈가 있는지 확인 후 Close
gh api repos/{owner}/{repo}/milestones/{number} -X PATCH -f state=closed
```

## 출력 포맷

```
[SEMO] deployer: 프로젝트 식별 완료
  - 프로젝트: cm-land (semicolon-devteam/cm-land)
  - 환경: STG
  - 방법: Milestone Close

[SEMO] deployer: Milestone 목록 조회
  1. v1.2.0 (이슈 5개, PR 3개)
  2. v1.3.0 (이슈 2개, PR 1개)

배포할 Milestone을 선택해주세요: ___

[SEMO] deployer: Milestone 'v1.2.0' Close 완료
  → STG 배포가 자동으로 트리거됩니다.
  → GitHub Actions: https://github.com/semicolon-devteam/cm-land/actions
```

## 상태 조회 Workflow

### STG 현재 배포 버전 확인

```bash
# 최근 close된 Milestone 조회 (= STG에 배포된 버전)
gh api repos/{owner}/{repo}/milestones?state=closed --jq '.[0] | "v\(.title) - \(.closed_at | split("T")[0]) 배포"'

# release- 브랜치 목록 조회
gh api repos/{owner}/{repo}/branches --jq '.[] | select(.name | startswith("release-")) | .name'
```

### PRD 최신 버전 확인

```bash
# 최신 릴리즈 태그 조회
gh api repos/{owner}/{repo}/releases/latest --jq '"v\(.tag_name) - \(.published_at | split("T")[0]) 릴리즈"'

# 또는 태그 목록에서 조회
gh api repos/{owner}/{repo}/tags --jq '.[0].name'
```

### STG 반영 대기 항목 조회

```bash
# Open 상태 Milestone + 연결된 이슈/PR 조회
gh api repos/{owner}/{repo}/milestones?state=open --jq '.[] | {title, open_issues, html_url}'

# 특정 Milestone의 이슈 목록
gh api "repos/{owner}/{repo}/issues?milestone={number}&state=all" --jq '.[] | "- #\(.number) \(.title) [\(.state)]"'
```

### 상태 조회 출력 포맷

```
[SEMO] deployer: 배포 상태 조회

📦 cm-land (semicolon-devteam/cm-land)

🟢 PRD: v1.2.2 (2025-12-10 릴리즈)
🟡 STG: release-1.2.3 (2025-12-15 배포)
🔵 DEV: dev 브랜치

📋 STG 반영 대기:
  - release-1.3.0 (Milestone Open)
    - #45 [Feature] 새 기능 추가 [open]
    - #46 [Bug] 버그 수정 [closed]
```

## 주의사항

- PRD 배포 시 반드시 STG 검증 여부 확인
- Milestone Close 전 연결된 이슈/PR 상태 확인
- 배포 실패 시 GitHub Actions 로그 확인 안내

## References

- Milestones: `https://github.com/{owner}/{repo}/milestones`
- Releases: `https://github.com/{owner}/{repo}/releases`
- Actions: `https://github.com/{owner}/{repo}/actions`
