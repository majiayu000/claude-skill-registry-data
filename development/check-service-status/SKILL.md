---
name: check-service-status
description: |
  서비스 상태 확인. Use when (1) "현황 알려줘", (2) "서비스 상태 확인",
  (3) "cm-* 상태 체크". GitHub 레포 상태 및 최근 배포 정보 조회.
tools: [Bash, Read]
model: inherit
---

> **시스템 메시지**: `[SEMO] Skill: check-service-status 호출`

# check-service-status Skill

> 서비스 상태 확인

## Purpose

운영 중인 서비스의 현재 상태를 확인합니다.

## Workflow

### Step 1: 서비스 목록 조회

```bash
# cm-* 서비스 레포 목록
gh repo list semicolon-devteam --json name,updatedAt,pushedAt \
  --jq '.[] | select(.name | startswith("cm-")) | {name, updatedAt, pushedAt}'
```

### Step 2: 최근 배포 확인

```bash
# 각 서비스의 최근 배포 (main 브랜치 마지막 커밋)
gh api repos/semicolon-devteam/{repo}/commits/main \
  --jq '{sha: .sha[:7], message: .commit.message, date: .commit.author.date}'
```

### Step 3: 활성 이슈 카운트

```bash
# 레포별 open 이슈 수
gh api repos/semicolon-devteam/{repo}/issues \
  --jq '[.[] | select(.state == "open")] | length'
```

### Step 4: 상태 리포트 생성

```markdown
## 서비스 현황 리포트

### 운영 서비스
| 서비스 | 상태 | 마지막 배포 | Open 이슈 |
|--------|------|------------|----------|
| cm-office | 🟢 정상 | 2025-12-15 | 0 |
| cm-land | 🟡 이슈 있음 | 2025-12-14 | 2 |

### 상태 기준
- 🟢 정상: Open 이슈 0건
- 🟡 이슈 있음: Open 이슈 1-3건
- 🔴 주의 필요: Open 이슈 4건 이상 또는 critical 라벨
```

## Expected Output

```markdown
[SEMO] Skill: check-service-status 호출

## 서비스 현황 리포트

| 서비스 | 상태 | 마지막 배포 | Open 이슈 |
|--------|------|------------|----------|
| cm-office | 🟢 정상 | 2025-12-15 | 0 |
| cm-land | 🟡 이슈 있음 | 2025-12-14 | 2 |
| core-backend | 🟢 정상 | 2025-12-14 | 0 |

**총 서비스**: 3개
**정상**: 2개 | **이슈 있음**: 1개 | **주의 필요**: 0개

[SEMO] Skill: check-service-status 완료
```

## References

- [ops/monitor CLAUDE.md](../../CLAUDE.md)
- [list-active-issues Skill](../list-active-issues/SKILL.md)
