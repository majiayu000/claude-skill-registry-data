---
name: project-status
description: |
  GitHub Projects Status 변경. Use when (1) "상태 변경해줘", "Status 바꿔줘",
  (2) "작업중으로 변경", "완료 처리", (3) Epic/태스크 상태 일괄 변경.
tools: [Bash, Read]
model: inherit
---

> **🔔 호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: project-status` 시스템 메시지를 첫 줄에 출력하세요.

# project-status Skill

> GitHub Projects Status 필드 변경

## 🔴 필수 참조 파일

**반드시 먼저 읽을 파일**: `.claude/memory/projects.md`

이 파일에서 다음 정보를 확인합니다:
- GitHub Projects 설정 (Project ID, Number)
- Status 옵션 및 Option ID
- **상태값 Alias** (사용자 입력 → Status 값 매핑)

## 권한 요구사항

```bash
# project scope 필요 (최초 1회)
gh auth refresh -s project
```

## Workflow

### 1. Status 필드 정보 조회

```bash
# Status 필드 ID와 옵션 목록 조회
gh api graphql -f query='
query {
  organization(login: "semicolon-devteam") {
    projectV2(number: 1) {
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options { id name }
        }
      }
    }
  }
}' --jq '.data.organization.projectV2.field'
```

### 2. Issue의 Project Item ID 조회

```bash
REPO="semicolon-devteam/docs"
ISSUE_NUMBER=123

# Issue node_id 조회
ISSUE_NODE_ID=$(gh api repos/$REPO/issues/$ISSUE_NUMBER --jq '.node_id')

# Project Item ID 조회
ITEM_ID=$(gh api graphql -f query='
  query($nodeId: ID!) {
    node(id: $nodeId) {
      ... on Issue {
        projectItems(first: 10) {
          nodes {
            id
            project { id }
          }
        }
      }
    }
  }
' -f nodeId="$ISSUE_NODE_ID" \
  --jq '.data.node.projectItems.nodes[] | select(.project.id == "PVT_kwDOC01-Rc4AtDz2") | .id')
```

### 3. Status 변경 실행

```bash
# Status 변경
gh api graphql -f query='
  mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) {
      projectV2Item { id }
    }
  }
' -f projectId="PVT_kwDOC01-Rc4AtDz2" \
  -f itemId="$ITEM_ID" \
  -f fieldId="$STATUS_FIELD_ID" \
  -f optionId="$STATUS_OPTION_ID"
```

## Status 옵션

| Status | 설명 |
|--------|------|
| 백로그 | 초기 상태 |
| 검수대기 | Epic 생성 시 기본값 |
| 작업중 | 개발 진행 중 |
| 리뷰요청 | 코드 리뷰 대기 |
| 테스트중 | QA 테스트 단계 |
| 완료 | 작업 완료 |

> **Note**: Status Option ID는 동적으로 조회합니다.

## 출력 포맷

```
[SEMO] project-status: 상태 변경 완료

✅ Status 변경 완료

**Issue**: #123
**이전 상태**: 검수대기
**변경 상태**: 작업중
```

## 에러 처리

### 권한 오류

```
⚠️ project scope 권한이 필요합니다.

다음 명령을 실행해주세요:
gh auth refresh -s project
```

### Item 미발견

```
⚠️ Issue #123이 '이슈관리' Project에 없습니다.

먼저 Issue를 Project에 추가해주세요.
```

## 일괄 변경 지원

여러 Issue의 Status를 한 번에 변경:

```bash
# 라벨로 필터링하여 일괄 변경
ISSUES=$(gh issue list --repo semicolon-devteam/docs \
  --label "project:차곡" --json number --jq '.[].number')

for ISSUE in $ISSUES; do
  # Status 변경 로직 실행
done
```

## Configuration

> **⚠️ 아래 값은 예시입니다. 실제 값은 `.claude/memory/projects.md`에서 확인하세요.**

```
Project ID: .claude/memory/projects.md 참조
Organization: .claude/memory/projects.md 참조
Project Number: .claude/memory/projects.md 참조
```

## 상태값 Alias 사용

사용자가 "리뷰요청", "테스트중" 등의 한글/영문 키워드를 사용하면,
`.claude/memory/projects.md`의 **상태값 Alias** 테이블을 참조하여
실제 Status 필드값으로 매핑합니다.

**예시:**
```
입력: "리뷰요청 이슈들 테스트중으로 바꿔줘"

1. projects.md 읽기
2. "리뷰요청" → Status "리뷰요청" 매핑
3. "테스트중" → Status "테스트중" 매핑
4. 해당 Status의 이슈들 조회
5. Status 변경 실행
```

## References

- [set-project-field Skill](../../packages/core/skills/set-project-field/SKILL.md)
- [GitHub Projects GraphQL API](https://docs.github.com/en/graphql/reference/mutations#updateprojectv2itemfieldvalue)
