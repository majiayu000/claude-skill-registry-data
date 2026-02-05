---
name: static-index
description: 글로벌 정적 컨텍스트 파일의 인덱스를 제공합니다. 다른 스킬이나 에이전트가 정보를 찾을 때 먼저 참조해야 할 파일을 자연어 쿼리로 찾아줍니다. "내 정보", "보안 규칙" 등의 요청에 적절한 static 파일 경로를 반환합니다.
---

# Static Index - 글로벌 컨텍스트 인덱스

## Overview

`~/.agents/` 디렉토리에 있는 정적 컨텍스트 파일들의 인덱스를 제공합니다. 다른 스킬이나 에이전트가 특정 정보를 찾을 때, 이 인덱스를 먼저 조회하여 적절한 파일을 찾을 수 있습니다.

## When to Use

이 스킬은 다음 상황에서 **자동으로** 활성화됩니다:

- 다른 스킬이 글로벌 컨텍스트 정보를 필요로 할 때
- 사용자가 "내 정보", "보안 규칙" 등 정적 데이터를 요청할 때
- 프로젝트 설정 전 기본 정보를 확인해야 할 때

**명시적 호출:**
- "static 파일 목록 보여줘"
- "글로벌 설정 확인"
- "에이전트 컨텍스트 파일들"

## Static File Index

### 쿼리-파일 매핑 테이블

| 자연어 쿼리 | 파일 | 설명 |
|------------|------|------|
| 내 정보, 내 프로필, 사용자 정보, whoami, 개발자 정보, 내 기술 스택 | `WHOAMI.md` | 사용자 개발 프로필 (기술 스택, 선호도, 경험) |
| 보안 규칙, 보안 정책, 민감 정보, 커밋 금지, security | `SECURITY.md` | 보안 검증 규칙 (커밋 금지 패턴, 민감 정보) |
| 코딩 스타일, 스타일 가이드, 코드 컨벤션, formatting | `STYLE.md` | 코딩 스타일 가이드 (포맷팅, 네이밍) |
| 노션 설정, notion, 노션 페이지, 업로드 설정 | `NOTION.md` | Notion 연동 설정 (페이지 ID, 업로드 옵션) |

### 파일 상세 정보

#### WHOAMI.md
- **경로**: `~/.agents/WHOAMI.md`
- **용도**: 사용자의 개발 프로필 저장
- **관리 스킬**: `whoami`
- **포함 정보**:
  - 기본 정보 (이름, 역할, 경력)
  - 프로그래밍 언어 (주력/부수)
  - 프레임워크 & 라이브러리
  - 개발 환경 (OS, 에디터, 셸)
  - 코딩 스타일 선호도
  - 아키텍처/테스트/DevOps 선호도

#### SECURITY.md
- **경로**: `~/.agents/SECURITY.md`
- **용도**: 보안 검증 규칙 정의
- **관리 스킬**: `git-commit-pr`
- **포함 정보**:
  - 커밋 금지 파일 패턴
  - 민감 정보 패턴 (API 키, 비밀번호 등)
  - 보안 체크리스트

#### STYLE.md
- **경로**: `~/.agents/STYLE.md`
- **용도**: 프로젝트 공통 코딩 스타일
- **관리 스킬**: 전역
- **포함 정보**:
  - 포맷팅 규칙 (들여쓰기, 줄 길이)
  - 네이밍 컨벤션
  - 주석 스타일

#### NOTION.md
- **경로**: `~/.agents/NOTION.md`
- **용도**: Notion 연동 설정
- **관리 스킬**: `notion-summary`
- **포함 정보**:
  - 업로드 대상 페이지 ID
  - 페이지 이름
  - 업로드 설정 (날짜별/프로젝트별 분류)
  - 콘텐츠 템플릿

## Prerequisites

### 스크립트 설치

```bash
# 스크립트 실행 권한 부여
chmod +x /path/to/agent-skills/context/static-index/scripts/static-index.sh

# alias 설정 (선택)
alias static-index='/path/to/agent-skills/context/static-index/scripts/static-index.sh'
```

## Workflow

### 스크립트 사용 (권장)

```bash
# 모든 정적 파일 목록
static-index.sh list

# 자연어 쿼리로 파일 검색
static-index.sh search "보안 규칙"
static-index.sh search "내 정보"

# 특정 타입 파일 경로 반환
static-index.sh get whoami
static-index.sh get security
```

**토큰 절약 효과:**
```
Before: 2-3회 도구 호출 (ls, find, grep 등)
After:  1회 스크립트 호출
절약률: 50-60%
```

### 수동 워크플로우 (참고용)

### Step 1: 쿼리 분석

사용자 또는 다른 스킬의 요청에서 키워드를 추출합니다.

```
입력: "API 만들기 전에 내 기술 스택 확인해줘"
키워드: "내 기술 스택" → WHOAMI.md
```

### Step 2: 인덱스 조회

매핑 테이블에서 일치하는 파일을 찾습니다.

```python
# 의사 코드
query_keywords = ["내 정보", "내 프로필", "사용자 정보", "whoami"]
if any(kw in user_query for kw in query_keywords):
    return "~/.agents/WHOAMI.md"
```

### Step 3: 파일 존재 확인

```bash
# 파일 존재 여부 확인
ls ~/.agents/WHOAMI.md 2>/dev/null
```

### Step 4: 결과 반환

- 파일이 존재하면: 파일 경로와 간단한 설명 반환
- 파일이 없으면: 해당 스킬을 통해 생성 안내

## Examples

### 예시 1: 다른 스킬에서 호출

```
context-manager 스킬: "프로젝트 설정 전 사용자 정보 필요"

static-index: WHOAMI.md 파일을 참조하세요.
경로: ~/.agents/WHOAMI.md
내용: 사용자 개발 프로필 (기술 스택, 선호도)
```

### 예시 2: 직접 조회

```
사용자: 글로벌 설정 파일들 뭐가 있어?

Claude: ~/.agents/ 디렉토리의 static 파일 목록:

| 파일 | 용도 | 상태 |
|------|------|------|
| WHOAMI.md | 사용자 프로필 | ✓ 존재 |
| SECURITY.md | 보안 규칙 | ✓ 존재 |
| STYLE.md | 코딩 스타일 | ✗ 없음 |
```

### 예시 3: 보안 규칙 조회

```
git-commit-pr 스킬: "커밋 전 보안 규칙 확인 필요"

static-index: SECURITY.md 파일을 참조하세요.
경로: ~/.agents/SECURITY.md
내용: 커밋 금지 패턴, 민감 정보 규칙
```

## 새 Static 파일 추가하기

새로운 글로벌 컨텍스트 파일을 추가하려면:

1. `~/.agents/` (또는 `agent-skills/static/`)에 파일 생성
2. 이 SKILL.md의 매핑 테이블에 항목 추가
3. 파일 상세 정보 섹션에 설명 추가

**예시: PROJECTS.md 추가**

```markdown
| 프로젝트 목록, 내 프로젝트, 진행 중인 작업 | `PROJECTS.md` | 활성 프로젝트 목록 |
```

## API for Other Skills

다른 스킬에서 static-index를 활용하는 방법:

```markdown
# 다른 스킬의 SKILL.md에서

## Prerequisites

작업 전 다음 static 파일을 확인합니다:
- `WHOAMI.md`: 사용자 프로필 (static-index 참조)
- `SECURITY.md`: 보안 규칙 (static-index 참조)
```

## File Locations

```
~/.agents/                    # 심링크 → agent-skills/static/
├── WHOAMI.md                # 사용자 프로필
├── SECURITY.md              # 보안 규칙
├── STYLE.md                 # 코딩 스타일 (선택)
├── NOTION.md                # Notion 연동 설정
└── README.md                # 디렉토리 설명

agent-skills/
├── static/                  # 실제 파일 위치 (Git 관리)
│   ├── WHOAMI.md
│   ├── SECURITY.md
│   ├── NOTION.md
│   └── README.md
└── context/
    └── static-index/
        └── SKILL.md         # 이 파일
```

## Integration with Other Skills

| 스킬 | 참조하는 Static 파일 | 용도 |
|------|---------------------|------|
| whoami | WHOAMI.md | 프로필 읽기/쓰기 |
| git-commit-pr | SECURITY.md | 커밋 전 보안 검증 |
| context-manager | WHOAMI.md, STYLE.md | 프로젝트 컨텍스트 구성 |
| planning-agents | WHOAMI.md | 사용자 역량 기반 기획 |
| notion-summary | NOTION.md | Notion 업로드 설정 |

## Best Practices

**DO:**
- 정보 검색 시 항상 static-index를 먼저 확인
- 새 글로벌 파일 추가 시 인덱스 업데이트
- 파일 존재 여부 확인 후 사용

**DON'T:**
- 민감한 정보를 static 파일에 저장하지 않기
- 프로젝트별 설정을 글로벌 static에 저장하지 않기
- 인덱스 없이 직접 파일 경로 하드코딩하지 않기

---

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/static-index.sh` | 정적 파일 인덱싱 및 검색 스크립트 |
