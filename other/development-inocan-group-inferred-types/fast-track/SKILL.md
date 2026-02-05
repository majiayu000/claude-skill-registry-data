---
name: fast-track
description: 경미한 수정사항 빠른 처리 및 사후 이슈 생성. Use when (1) 오타/문구 수정, (2) 스타일 미세조정, (3) 버그 핫픽스, (4) 코드 정리 (3파일 이하, 30분 이내).
tools: [Read, Write, Edit, Bash, GitHub CLI]
triggers:
  - 패스트트랙
  - fast-track
  - 빠른수정
  - 긴급수정
  - 핫픽스
  - hotfix
  - 오타수정
  - typo
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: fast-track 호출 - {작업 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# fast-track Skill

> 개발자 주도의 경미한 수정사항을 Epic→Task 프로세스 없이 빠르게 처리

## Purpose

PO의 Epic→Task 생성 프로세스를 거치지 않고, 개발자가 발견한 경미한 수정사항을 **즉시 처리**하고 **사후 보고**하는 워크플로우를 제공합니다.

### 대상 작업

| 카테고리 | 예시 | 적격 여부 |
|----------|------|-----------|
| 오타/문구 수정 | 버튼 텍스트 오타, 에러 메시지 수정 | ✅ 적격 |
| 스타일 미세조정 | 간격/패딩 1-2px 조정, 색상 미세 수정 | ✅ 적격 |
| 버그 핫픽스 | 명확한 원인의 단순 버그 | ✅ 적격 |
| 코드 정리 | 사용하지 않는 import 제거, lint 수정 | ✅ 적격 |
| 새 기능 추가 | 신규 컴포넌트, 페이지 추가 | ❌ 부적격 |
| 아키텍처 변경 | 폴더 구조 변경, 상태관리 수정 | ❌ 부적격 |
| 데이터 모델 변경 | DB 스키마 수정, API 변경 | ❌ 부적격 |

> 📖 상세 적격성 기준: [references/eligibility-check.md](references/eligibility-check.md)

## Workflow

### Step 1: 적격성 확인

```
[SEMO] Skill 호출: fast-track (적격성 확인)

작업 내용: {사용자가 설명한 작업}

🔍 적격성 체크:
- [ ] 영향 범위 3개 파일 이하
- [ ] 기능 변경 없음 (동작 유지)
- [ ] 테스트 변경 불필요
- [ ] 30분 이내 완료 가능

✅ 패스트트랙 적격 / ❌ 일반 프로세스 필요
```

**적격 판정 시**: Step 2로 진행
**부적격 판정 시**: 일반 Epic→Task 프로세스 안내

### Step 2: 즉시 수정 실행

```
[SEMO] fast-track 실행: {작업 설명}

📝 변경 사항:
- {파일1}: {변경 내용}
- {파일2}: {변경 내용}

⏱️ 예상 소요: {n}분
```

수정 작업 완료 후 Step 3으로 진행

### Step 3: 사후 이슈 생성

작업 완료 후 **반드시** GitHub Issue 생성:

```
[SEMO] fast-track 완료 → 이슈 생성

📋 생성할 이슈:
- 제목: [Fast-Track] {작업 요약}
- 라벨: fast-track, {카테고리}
- 본문: (템플릿 기반)

이슈를 생성할까요? (Y/n)
```

> 📖 이슈 템플릿: [references/issue-template.md](references/issue-template.md)

### Step 4: 프로젝트 보드 연동

이슈 생성 후 **반드시** 프로젝트 보드에 연동하고 상태 설정:

```
[SEMO] fast-track → 프로젝트 보드 연동

📋 생성된 이슈: {repo}#{issue_number}
📊 프로젝트: 이슈관리 (#1)

🔄 작업 진행 중...
1. ✅ 프로젝트 보드에 이슈 추가
2. ✅ 상태를 "리뷰요청"으로 설정

✅ 완료: {repo}#{issue_number} → 리뷰요청
```

**자동 실행 명령**:

```bash
# 1. 프로젝트에 이슈 추가
gh project item-add 1 --owner semicolon-devteam --url "https://github.com/semicolon-devteam/{repo}/issues/{issue_number}"

# 2. 상태를 "리뷰요청"으로 변경
# skill: project-board 호출
```

> 📖 상세 API: [../project-board/references/api-commands.md](../project-board/references/api-commands.md)

## Issue Template

```markdown
## Fast-Track 수정 보고

### 카테고리
- [ ] 오타/문구 수정
- [ ] 스타일 미세조정
- [ ] 버그 핫픽스
- [ ] 코드 정리
- [ ] 기타: ___

### 변경 내용
{변경 사항 요약}

### 수정 파일
- `{파일 경로}`: {변경 내용}

### 스크린샷 (해당시)
{변경 전/후 스크린샷}

### 관련 커밋
{커밋 해시 또는 PR 링크}

---
> 🏃 이 이슈는 Fast-Track 프로세스로 사후 생성되었습니다.
> Epic 연결 없이 개발자 주도로 처리된 경미한 수정입니다.
```

## Routing Integration

### Orchestrator 라우팅 조건

```yaml
triggers:
  keywords:
    - 패스트트랙
    - fast-track
    - 빠른수정
    - 긴급수정
    - 핫픽스
    - hotfix
    - 간단한 수정
    - 오타 수정
  patterns:
    - "{경미한|간단한|사소한} {수정|변경|고침}"
    - "빠르게 {고치|수정}"
    - "바로 {처리|수정}"
```

### 일반 작업과의 구분

| 키워드 | 라우팅 |
|--------|--------|
| "기능 구현해줘" | implementer Agent |
| "오타 수정해줘" | fast-track Skill |
| "버그 고쳐줘" | 맥락에 따라 판단 |
| "핫픽스 필요해" | fast-track Skill |

## 🔄 테스트 정책: Fast-Track 예외

> **Fast-Track은 테스트 작성 의무에서 제외됩니다.**

### 테스트 생략 허용 조건

Fast-Track 작업은 다음 조건을 만족하므로 **Unit Test 생략 허용**:

| 조건 | Fast-Track 충족 |
|------|-----------------|
| 3개 파일 이하 | ✅ 필수 조건 |
| 기능 변경 없음 | ✅ 동작 유지 |
| 기존 테스트 통과 | ✅ 필수 확인 |

### 필수 검증

테스트 작성은 생략하되, 다음은 **필수 확인**:

```bash
# 기존 테스트 통과 확인
npm test

# Lint 확인
npm run lint

# TypeScript 확인
npx tsc --noEmit
```

### 테스트 생략 출력

```markdown
[SEMO] 테스트 정책: Unit Test 생략 (Fast-Track)

**사유**: 경미한 수정 (기능 변경 없음)
**검증**: 기존 테스트 통과 ✅

⚠️ 기능 변경이 포함된 경우 일반 프로세스 사용
```

> 📖 전체 테스트 정책: [_shared/test-policy.md](../_shared/test-policy.md)

---

## Constraints

### 필수 조건

1. **적격성 확인 필수**: Step 1 생략 불가
2. **이슈 생성 필수**: Step 3 생략 불가 (PO 가시성 확보)
3. **프로젝트 보드 연동 필수**: Step 4 생략 불가 (상태 추적)
4. **라벨 필수**: `fast-track` 라벨 반드시 포함
5. **커밋 메시지**: `🏃 [Fast-Track]` 접두사 사용
6. **기존 테스트 통과 필수**: 새 테스트 작성은 생략 가능

### 금지 사항

- ❌ 적격성 체크 없이 바로 수정
- ❌ 이슈 생성 없이 작업 종료
- ❌ 프로젝트 보드 연동 없이 작업 종료
- ❌ 부적격 작업을 패스트트랙으로 처리
- ❌ 3개 파일 초과 수정
- ❌ 기존 테스트 실패 상태로 커밋

## Examples

### Example 1: 오타 수정

**사용자**: "버튼에 오타가 있어서 수정하고 싶어"

```
[SEMO] Skill 호출: fast-track (적격성 확인)

작업 내용: 버튼 텍스트 오타 수정

🔍 적격성 체크:
- [x] 영향 범위 3개 파일 이하 (1개)
- [x] 기능 변경 없음
- [x] 테스트 변경 불필요
- [x] 30분 이내 완료 가능

✅ 패스트트랙 적격

---

[SEMO] fast-track 실행: 버튼 오타 수정

📝 변경 사항:
- components/Button.tsx: "제출하기" → "제출하기" (오타 없음 확인)
  실제: "제출 하기" → "제출하기" (띄어쓰기 수정)

⏱️ 예상 소요: 5분
```

### Example 2: 부적격 케이스

**사용자**: "새 페이지 추가 빠르게 해줘"

```
[SEMO] Skill 호출: fast-track (적격성 확인)

작업 내용: 새 페이지 추가

🔍 적격성 체크:
- [ ] 영향 범위 3개 파일 이하 → ❌ 5+ 파일 예상
- [ ] 기능 변경 없음 → ❌ 새 기능 추가
- [ ] 테스트 변경 불필요 → ❌ 새 테스트 필요
- [ ] 30분 이내 완료 가능 → ❌ 2시간+ 예상

❌ 패스트트랙 부적격

💡 권장: PO에게 Epic 생성 요청 후 일반 프로세스 진행
   → "새 페이지 Epic 요청" 또는 task-progress로 기존 Epic 확인
```

## References

- [적격성 체크 가이드](references/eligibility-check.md)
- [이슈 템플릿](references/issue-template.md)
- [카테고리 가이드](references/category-guide.md)
- [SEMO Core - Message Rules](../../.claude/semo-core/MESSAGE_RULES.md)
