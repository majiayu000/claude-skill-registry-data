---
name: obsidian-writer
description: Obsidian Vault에 문서를 업로드하는 스킬. 현재 프로젝트의 컨텍스트 문서를 workspace/{프로젝트명}/context/ 경로에 저장합니다. 'obsidian 업로드', 'obsidian에 저장', '옵시디언 문서', 'vault에 업로드' 요청 시 활성화됩니다.
---

# Obsidian Writer - 프로젝트 문서 업로드

## Overview

현재 작업 중인 프로젝트의 문서를 Obsidian Vault에 업로드하는 스킬입니다.

**핵심 기능:**
- 현재 디렉토리(pwd) 기반 프로젝트명 자동 감지
- `workspace/{프로젝트명}/context/` 경로에 문서 저장 (기본값)
- **경로 매핑 지원**: `~/.agents/OBSIDIAN.md`의 "프로젝트 경로 매핑" 테이블에서 커스텀 경로 사용
- 프로젝트별 문서 체계적 관리
- 프론트매터(YAML) 자동 생성

**저장 구조:**
```
Vault/
├── workspace/                    # ~/workspace/* 프로젝트
│   ├── agent-skills/
│   │   └── context/
│   └── other-project/
│       └── context/
└── workspace-vibe/               # ~/workspace-vibe/* 프로젝트
    ├── colorpal/
    │   └── context/
    ├── memory-ai/
    │   └── context/
    ├── GoalTracker/
    │   └── context/
    └── shared_services/
        └── context/
```

## 경로 매핑 (Path Mapping)

`~/.agents/OBSIDIAN.md`의 "프로젝트 경로 매핑"에 따라 경로가 결정됩니다:

| 로컬 경로 | Obsidian 경로 |
|----------|--------------|
| `~/workspace/{project}/` | `workspace/{project}/context/` |
| `~/workspace-vibe/{service}/` | `workspace-vibe/{service}/context/` |

예시:
- `~/workspace/agent-skills/` → `workspace/agent-skills/context/`
- `~/workspace-vibe/colorpal/` → `workspace-vibe/colorpal/context/`

## Prerequisites

### Static 파일 설정 (필수)

`~/.agents/OBSIDIAN.md` 파일에 Vault 경로 설정:

```markdown
# Obsidian 설정

## Vault 경로
- **경로**: /Users/username/Documents/ObsidianVault

## 문서 설정
- **프론트매터 생성**: true
- **태그 자동 생성**: true
```

## Workflow

### Step 1: 프로젝트 감지

스킬 실행 시 현재 작업 디렉토리에서 프로젝트명을 자동으로 감지합니다:

```bash
# 현재 디렉토리: ~/workspace/agent-skills
# 감지된 프로젝트명: agent-skills
# 저장 경로: Vault/workspace/agent-skills/context/
```

### Step 2: 문서 업로드

```bash
# 기본 업로드 (프로젝트 자동 감지)
./scripts/obsidian-write.py \
  --title "API 설계 문서" \
  --content "마크다운 내용"

# 프로젝트 명시
./scripts/obsidian-write.py \
  --title "문서 제목" \
  --content "내용" \
  --project "custom-project"

# 하위 폴더 지정
./scripts/obsidian-write.py \
  --title "회의록" \
  --content "내용" \
  --subfolder "meetings"
# 결과: workspace/agent-skills/context/meetings/회의록.md
```

## Examples

### 예시 1: 문서 업로드

```
사용자: 이 API 설계 문서 옵시디언에 업로드해줘

Claude: Obsidian에 업로드를 준비합니다.

## 업로드 정보

- **프로젝트**: agent-skills (자동 감지)
- **저장 경로**: workspace/agent-skills/context/api-design.md

### 문서 미리보기
---
created: 2025-01-15T14:30:00
project: agent-skills
tags: [claude, api, design]
---

# API 설계 문서

[문서 내용...]

이대로 업로드할까요? (Y/n)
```

### 예시 2: 하위 폴더에 저장

```
사용자: 오늘 회의 내용 옵시디언 meetings 폴더에 저장해줘

Claude: 업로드합니다.

✅ 업로드 완료
- 경로: workspace/agent-skills/context/meetings/2025-01-15-meeting.md
- Vault: ~/Documents/ObsidianVault
```

### 예시 3: 설정 없을 때

```
사용자: 옵시디언 업로드해줘

Claude: ⚠️ Obsidian 설정이 필요합니다.

~/.agents/OBSIDIAN.md 파일을 생성해주세요:

# Obsidian 설정

## Vault 경로
- **경로**: [여기에 Vault 경로 입력]

설정 파일을 자동으로 생성할까요? (Y/n)
```

## Configuration

### ~/.agents/OBSIDIAN.md 구조

```markdown
# Obsidian 설정

## Vault 경로
- **경로**: /Users/username/Documents/ObsidianVault

## 문서 설정
- **프론트매터 생성**: true
- **태그 자동 생성**: true
- **기본 태그**: claude, context
```

## 프론트매터 템플릿

```yaml
---
created: 2025-01-15T14:30:00
project: agent-skills
tags: [claude, context, documentation]
---
```

## Best Practices

**DO:**
- Vault 경로는 절대 경로로 설정
- 프론트매터로 메타데이터 관리
- 일관된 폴더 구조 유지
- 저장 전 내용 미리보기 확인

**DON'T:**
- 민감 정보(API 키, 비밀번호) 저장하지 않기
- 기존 파일 덮어쓰기 주의 (확인 필요)
- Obsidian 잠금 파일(.obsidian) 수정하지 않기

## Troubleshooting

### 문제 1: Vault 경로 없음

```
Error: Vault path not found
```

해결:
1. `~/.agents/OBSIDIAN.md`에 올바른 경로 설정
2. 폴더가 실제로 존재하는지 확인
3. 경로에 공백이 있으면 따옴표로 감싸기

### 문제 2: 권한 오류

```
Error: Permission denied
```

해결:
1. Vault 폴더 쓰기 권한 확인
2. `chmod 755 /path/to/vault` 실행

### 문제 3: 파일명 충돌

```
Warning: File already exists
```

해결:
- 덮어쓰기 확인 프롬프트 표시
- 또는 `--suffix` 옵션으로 번호 추가

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/obsidian-write.py` | 문서 생성 스크립트 |
| `~/.agents/OBSIDIAN.md` | 사용자 설정 (static-index 참조) |

## Integration with Other Skills

| 스킬 | 연동 방식 |
|------|----------|
| static-index | OBSIDIAN.md 파일 경로 조회 |
| security-auditor | 저장 전 민감 정보 검사 |
| mindcontext | 프로젝트별 컨텍스트와 연동 |
