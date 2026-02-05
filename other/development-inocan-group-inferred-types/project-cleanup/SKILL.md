---
name: project-cleanup
description: 프로젝트 문서 정리 및 폴더 구조 최적화. 정리, cleanup, organize, 문서 관리 키워드에 자동 활성화.
allowed-tools: Read, Bash, Grep, Glob, Write, Edit
---

# Project Cleanup Skill

## SSDD 정리 원칙

### 문서 크기 기준

| 문서 | 권장 크기 | 초과 시 조치 |
|------|-----------|--------------|
| CLAUDE.md | 300줄 이하 | 히스토리 → archive |
| roadmap.md | 800줄 이하 | 이전 버전 → archive |
| changelog.md | 1000줄 이하 | 월별 분할 → archive |
| project-todo.md | 200줄 이하 | 완료 항목 → archive |

### 아카이브 경로

```
docs/archive/
├── CLAUDE-history-YYYY-MM.md     # CLAUDE.md 히스토리
├── roadmap-vX.X.X.md             # 이전 버전 로드맵
├── changelog-YYYY-MM.md          # 월별 변경 로그
├── completed-todos-vX.X.X.md     # 완료된 TODO
├── phase-plans/                  # Phase 계획 문서
└── daily-summaries/              # 일일 요약
```

### 정리 대상

#### 삭제 대상

- 빈 폴더
- `*.bak`, `*.backup` 파일
- `*.tmp`, `*-temp.*` 파일
- `nul` 파일 (Windows 잔여)

#### 아카이브 대상

- 3개월 이상 지난 daily-summaries
- 완료된 phase 계획
- 오래된 리포트

#### 통합 대상

- 중복 PDF/PPTX 파일
- 분산된 동일 주제 문서

## 분석 명령어

### 대용량 파일 찾기 (Windows/Git Bash)

```bash
find docs/ -name "*.md" -exec wc -l {} + 2>/dev/null | sort -rn | head -20
```

### 빈 폴더 찾기

```bash
find docs/ -type d -empty 2>/dev/null
```

### 백업/임시 파일 찾기

```bash
find . -name "*.bak" -o -name "*-backup.*" -o -name "*.tmp" 2>/dev/null
```

### 버전 확인

```bash
echo "package.json:" && grep '"version"' package.json
echo "CLAUDE.md:" && grep -E "현재 버전|버전:" CLAUDE.md
echo "docs/INDEX.md:" && grep -E "버전|Version" docs/INDEX.md
```

## 정리 워크플로우

### 1. 분석

```bash
# 전체 현황
echo "=== 대용량 파일 ===" && find docs/ -name "*.md" -exec wc -l {} + | sort -rn | head -10
echo "=== 빈 폴더 ===" && find docs/ -type d -empty
echo "=== 백업 파일 ===" && find . -name "*.bak"
```

### 2. 계획

정리 대상 목록 작성:
- [ ] 분할할 대용량 문서
- [ ] 삭제할 빈 폴더/백업 파일
- [ ] 동기화할 버전

### 3. 실행

```bash
# 빈 폴더 삭제
find docs/ -type d -empty -delete

# 백업 파일 삭제
find . -name "*.bak" -delete
```

### 4. 검증

```bash
# 버전 동기화 확인
grep '"version"' package.json
grep "현재 버전" CLAUDE.md
```

### 5. 보고

정리 결과 요약 테이블 작성

## 주의사항

- 삭제 전 반드시 확인
- 대용량 문서 분할 시 링크 업데이트
- 버전 동기화는 package.json 기준
