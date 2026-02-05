---
name: list-bugs
description: |
  GitHub Issue Type 기반 버그 이슈 조회. Use when (1) "버그 이슈 목록",
  (2) "버그 확인", (3) "버그 조회", (4) type:Bug 이슈 필터링.
tools: [Bash]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: list-bugs 호출` 시스템 메시지를 첫 줄에 출력하세요.

# list-bugs Skill

> GitHub Issue Type 기반 버그 이슈 조회

## Purpose

GitHub 라벨 대신 GitHub Issue Type (`type:Bug`)을 기준으로 버그 이슈를 조회합니다.

### 기존 방식의 문제점

```bash
# 기존: 라벨 기반 (레포마다 naming이 다름)
gh issue list --label "bug" --state open
gh issue list --label "BugFix" --state open
gh issue list --label "🐛" --state open
```

- 레포마다 라벨 naming이 다름 (bug, BugFix, 🐛, fix 등)
- 일부 레포는 bug 라벨이 없음
- 일관된 조회 불가

### 새 방식: GitHub Issue Type 기준

```bash
# GitHub Issue Type으로 버그 필터 조회
gh issue list --repo semicolon-devteam/semo --state open --json number,title,issueType --jq '.[] | select(.issueType.name == "Bug")'
```

## Configuration

### GitHub Issue Type 정보

> **Projects 커스텀 필드 '타입' 대신 GitHub Issue Type을 사용합니다.**

| Issue Type | ID | 용도 |
|------------|-----|------|
| Task | `IT_kwDOC01-Rc4BdOub` | 일반 태스크 |
| Bug | `IT_kwDOC01-Rc4BdOuc` | 버그 리포트 |
| Feature | `IT_kwDOC01-Rc4BdOud` | 기능 요청 |
| Epic | `IT_kwDOC01-Rc4BvVz5` | 에픽 |

## Workflow

### 1. GitHub Issue Type으로 버그 조회

```bash
# GitHub Issue Type (type:Bug)으로 버그 이슈 조회
gh issue list --repo semicolon-devteam/semo --state open \
  --json number,title,issueType,createdAt,assignees,repository \
  --jq '.[] | select(.issueType.name == "Bug")'
```

### 2. 전체 조직 레포지토리 버그 조회

```bash
# 조직 내 모든 레포지토리에서 Bug 타입 이슈 조회
REPOS="semo docs core-backend community-web"

for repo in $REPOS; do
  gh issue list --repo "semicolon-devteam/$repo" --state open \
    --json number,title,issueType,createdAt,assignees \
    --jq '.[] | select(.issueType.name == "Bug") | "| #\(.number) | '"$repo"' | \(.title) |"'
done
```

### 3. 결과 포맷팅

```bash
# 테이블 형식으로 출력
gh issue list --repo semicolon-devteam/semo --state open \
  --json number,title,issueType,createdAt,assignees \
  --jq '.[] | select(.issueType.name == "Bug") | "| #\(.number) | \(.title) | \(.createdAt | split("T")[0]) |"'
```

## Output Format

```markdown
## 🐛 버그 이슈 현황 (GitHub Issue Type 기준)

| # | 레포 | 제목 | 담당자 | 생성일 |
|---|------|------|--------|--------|
| #123 | core-backend | API 응답 지연 | kyago | 2025-12-01 |
| #456 | community-web | 버튼 클릭 안됨 | Reus | 2025-12-05 |

---
**총 2개의 Open 버그 이슈**
```

## 전체 스크립트

```bash
#!/bin/bash

# 조회할 레포지토리 목록
REPOS="semo docs core-backend community-web"

echo "## 🐛 버그 이슈 현황 (GitHub Issue Type 기준)"
echo ""
echo "| # | 레포 | 제목 | 담당자 | 생성일 |"
echo "|---|------|------|--------|--------|"

COUNT=0

for repo in $REPOS; do
  # GitHub Issue Type이 Bug인 이슈만 조회
  RESULT=$(gh issue list --repo "semicolon-devteam/$repo" --state open \
    --json number,title,issueType,createdAt,assignees \
    --jq '.[] | select(.issueType.name == "Bug")')

  if [ -n "$RESULT" ]; then
    echo "$RESULT" | jq -r '"| #\(.number) | '"$repo"' | \(.title) | \(.assignees | map(.login) | join(\", \") | if . == \"\" then \"-\" else . end) | \(.createdAt | split(\"T\")[0]) |"'
    REPO_COUNT=$(echo "$RESULT" | jq -s 'length')
    COUNT=$((COUNT + REPO_COUNT))
  fi
done

if [ "$COUNT" -eq 0 ]; then
  echo "| - | - | 버그 이슈 없음 | - | - |"
fi

echo ""
echo "---"
echo "**총 ${COUNT}개의 Open 버그 이슈**"
```

## No Bugs Case

```markdown
## 🐛 버그 이슈 현황 (GitHub Issue Type 기준)

✅ 현재 Open 상태의 버그 이슈가 없습니다.
```

## Error Handling

### GitHub CLI 인증 오류

```markdown
⚠️ **인증 오류**

GitHub CLI 인증이 필요합니다.
인증 상태를 확인해주세요: `gh auth status`
```

### 레포지토리 접근 권한 없음

```markdown
⚠️ **레포지토리 접근 오류**

해당 레포지토리에 접근할 수 없습니다.
- 조직 멤버십을 확인해주세요.
```

## SEMO Message Format

```markdown
[SEMO] Skill: list-bugs 호출

[SEMO] Skill: list-bugs 완료 - {N}개 버그 이슈 발견
```

## 라벨 기반 조회 (Fallback)

GitHub Issue Type 조회가 실패할 경우 라벨 기반으로 폴백:

```bash
# Fallback: 라벨 기반 조회
for repo in $(gh repo list semicolon-devteam --json name --jq '.[].name'); do
  gh issue list --repo "semicolon-devteam/$repo" --label "bug" --state open 2>/dev/null
done
```

## Related

- [이슈 #6](https://github.com/semicolon-devteam/semo-core/issues/6) - 버그 이슈 조회 시 GitHub Issue Type 기준 조회 지원
- [check-feedback Skill](../check-feedback/SKILL.md) - 피드백 이슈 수집
