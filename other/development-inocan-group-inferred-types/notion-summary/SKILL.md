---
name: notion-summary
description: Claude 세션의 대화 요약과 작업 결과를 Notion 페이지 하위에 업로드합니다. '노션 업로드', '결과 저장', 'notion 정리' 요청 시 활성화됩니다.
---

# Notion Summary - 세션 결과 Notion 업로드

## Overview

Claude Code 세션의 작업 내용을 Notion 문서로 정리하여 업로드하는 스킬입니다.

**핵심 기능:**
- 대화 내용 요약 및 업로드
- 작업 결과물 (코드 변경, 생성 파일 등) 정리
- 지정된 Notion 페이지 하위에 자동 생성
- 날짜/프로젝트별 체계적 문서화

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:

**명시적 요청:**
- "노션에 업로드해줘"
- "결과 노션에 정리해줘"
- "오늘 작업 내용 저장해줘"
- "notion summary"

**자동 활성화:**
- 긴 작업 세션 완료 후
- 사용자가 세션 정리 요청 시

## Prerequisites

### 환경 변수 (필수)

```bash
# ~/.bashrc, ~/.zshrc, 또는 ~/.profile에 추가
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxx"
```

**토큰 발급 방법:**
1. https://www.notion.so/my-integrations 접속
2. "New integration" 클릭
3. 이름 지정 후 생성
4. "Internal Integration Token" 복사

### Static 파일 설정 (필수)

`~/.agents/NOTION.md` 파일에 페이지 설정:

```markdown
# Notion 설정

## 기본 페이지
- **페이지 ID**: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- **페이지 이름**: Claude 작업 기록

## 업로드 설정
- **날짜별 하위 페이지**: true
- **프로젝트별 분류**: true
```

### 의존성 설치

```bash
pip install notion-client
```

### Notion 페이지 권한 설정

1. 업로드할 Notion 페이지 열기
2. 우측 상단 `...` → "Connections" 클릭
3. 생성한 Integration 선택하여 연결

## Workflow

### Step 1: 설정 확인

스킬 실행 시 다음을 확인합니다:

1. `NOTION_TOKEN` 환경 변수 존재 확인
2. `~/.agents/NOTION.md`에서 페이지 ID 읽기 (static-index 활용)

```bash
# 환경 변수 확인
echo $NOTION_TOKEN

# static 파일 확인
./scripts/notion-upload.py --check-config
```

### Step 2: 세션 내용 수집

현재 세션에서 다음 정보를 수집합니다:

**대화 요약:**
- 사용자 요청 사항
- 주요 논의 내용
- 결정된 사항

**작업 결과물:**
- 생성/수정된 파일 목록
- 코드 변경 요약
- 실행된 명령어

### Step 3: Notion 페이지 생성

지정된 부모 페이지 하위에 새 페이지를 생성합니다:

```
Claude 작업 기록/
├── 2025-01-15 - project-name/
│   ├── 요약
│   ├── 작업 내용
│   └── 파일 변경 사항
└── 2025-01-14 - other-project/
```

### Step 4: 콘텐츠 업로드

```bash
# 스크립트 실행
./scripts/notion-upload.py \
  --summary "대화 요약 내용" \
  --changes "파일 변경 사항" \
  --project "프로젝트명"
```

## Examples

### 예시 1: 기본 업로드

```
사용자: 오늘 작업한 내용 노션에 정리해줘

Claude: 노션에 업로드를 준비합니다.

## 업로드 내용 미리보기

### 세션 요약
- 노션 업로드 스킬 개발
- SKILL.md 및 업로드 스크립트 작성

### 작업 결과
- 생성 파일: integrations/notion-summary/SKILL.md
- 생성 파일: integrations/notion-summary/scripts/notion-upload.py

이대로 업로드할까요? (Y/n)
```

### 예시 2: 프로젝트 지정 업로드

```
사용자: 이 작업 결과를 agent-skills 프로젝트로 노션에 저장해

Claude: 노션에 업로드합니다.

✅ 업로드 완료
- 페이지: Claude 작업 기록 / 2025-01-15 - agent-skills
- URL: https://notion.so/xxxxx
```

### 예시 3: 설정 없을 때

```
사용자: 노션 업로드해줘

Claude: ⚠️ 노션 설정이 필요합니다.

1. NOTION_TOKEN 환경 변수를 설정해주세요:
   export NOTION_TOKEN="secret_xxx"

2. ~/.agents/NOTION.md 파일을 생성해주세요:
   페이지 ID와 업로드 설정을 포함해야 합니다.

자세한 설정 방법을 안내해드릴까요?
```

## Configuration

### ~/.agents/NOTION.md 구조

```markdown
# Notion 설정

## 기본 페이지
- **페이지 ID**: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- **페이지 이름**: Claude 작업 기록

## 업로드 설정
- **날짜별 하위 페이지**: true
- **프로젝트별 분류**: true
- **기본 프로젝트명**: general

## 콘텐츠 템플릿
### 포함 항목
- 세션 요약: true
- 작업 결과물: true
- 파일 변경 사항: true
- 실행 명령어: false
```

### 환경 변수 옵션

| 변수 | 필수 | 설명 |
|------|------|------|
| `NOTION_TOKEN` | 필수 | Notion Integration 토큰 |
| `NOTION_PAGE_ID` | 선택 | 기본 페이지 ID (static 파일보다 우선) |

## Best Practices

**DO:**
- 토큰은 반드시 환경 변수로 관리
- 업로드 전 미리보기로 내용 확인
- 프로젝트별로 체계적으로 분류
- 민감 정보 제외 확인

**DON'T:**
- 토큰을 코드나 설정 파일에 하드코딩하지 않기
- API 키나 비밀번호가 포함된 내용 업로드하지 않기
- 너무 자주 업로드하여 API 한도 초과하지 않기

## Troubleshooting

### 문제 1: 인증 실패

```
Error: Invalid token
```

해결:
1. 토큰 유효성 확인: `echo $NOTION_TOKEN`
2. Integration이 페이지에 연결되었는지 확인
3. 토큰 재발급 필요 시 my-integrations에서 재생성

### 문제 2: 페이지 없음

```
Error: Page not found
```

해결:
1. 페이지 ID가 올바른지 확인
2. Integration이 해당 페이지에 접근 권한이 있는지 확인
3. Notion 페이지 → Connections에서 Integration 연결

### 문제 3: Static 파일 없음

```
Warning: NOTION.md not found
```

해결:
```bash
# 템플릿 생성
cat > ~/.agents/NOTION.md << 'EOF'
# Notion 설정

## 기본 페이지
- **페이지 ID**: [여기에 페이지 ID 입력]
- **페이지 이름**: Claude 작업 기록

## 업로드 설정
- **날짜별 하위 페이지**: true
- **프로젝트별 분류**: true
EOF
```

## Security

이 스킬은 다음 보안 규칙을 따릅니다:

1. **토큰 보호**: `NOTION_TOKEN`은 환경 변수로만 관리
2. **민감 정보 필터링**: 업로드 전 API 키, 비밀번호 패턴 검사
3. **static-index 연동**: `~/.agents/SECURITY.md` 규칙 적용
4. **업로드 확인**: 사용자 확인 후 업로드 (기본 동작)

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/notion-upload.py` | Notion API 업로드 스크립트 |
| `~/.agents/NOTION.md` | 사용자 노션 설정 (static-index 참조) |

## Integration with Other Skills

| 스킬 | 연동 방식 |
|------|----------|
| static-index | NOTION.md 파일 경로 조회 |
| security-auditor | 업로드 전 민감 정보 검사 |
| git-commit-pr | 커밋 후 자동 문서화 연동 가능 |
