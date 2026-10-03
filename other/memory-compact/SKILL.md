---
name: memory-compact
description: >
  MEMORY.md 크기 점검 및 압축. 비대해진 메모리를 정리하여 성능 저하를 방지합니다. /memory-compact로 실행.
  대상은 프로젝트 루트 MEMORY.md 전용 — Claude 네이티브 auto-memory(~/.claude/projects/)의 MEMORY.md와 무관.
---

# Memory Compact - MEMORY.md 압축 스킬

MEMORY.md가 비대해져 성능에 영향을 줄 때 사용합니다.
상세 내용을 `memory/*.md`로 이동하고, MEMORY.md는 가벼운 인덱스로 복원합니다.

## 제한 기준

| 항목 | 제한 |
|------|------|
| MEMORY.md 최대 줄 수 | **100줄** |
| MEMORY.md 최대 크기 | **5KB** |
| 항목당 최대 줄 수 | 3줄 (인덱스에는 요약만) |

## 워크플로우

### Step 1: 진단

```
1. MEMORY.md 읽기
2. 줄 수, 바이트 수 측정
3. 100줄 / 5KB 이하면 → "이미 컴팩트합니다" 종료
4. 초과면 → Step 2 진행
```

### Step 2: 분석

각 섹션을 파싱하여 문제를 분류합니다:

| 문제 유형 | 설명 | 조치 |
|-----------|------|------|
| **쓰레기 데이터** | 로그 출력, 에러 메시지, 설치 로그 등 | 삭제 |
| **상세 내용 인라인** | 인덱스가 아닌 상세 설명이 MEMORY.md에 있음 | `memory/*.md`로 이동 |
| **중복 항목** | 같은 내용이 반복됨 | 병합 |
| **SUPERSEDED 누적** | 오래된 ❌ 항목이 쌓임 | `memory/archive.md`로 이동 |

### Step 3: 압축 실행

```
1. 쓰레기 데이터 삭제
2. 상세 내용을 적절한 memory/*.md로 이동
   - 설계 결정 → memory/architecture.md
   - 작업 패턴 → memory/patterns.md
   - 도구/라이브러리 → memory/tools.md
   - 주의사항 → memory/gotchas.md
3. MEMORY.md에는 키워드 인덱스 항목만 남김
4. SUPERSEDED 항목은 memory/archive.md로 이동
5. 빈 섹션 정리
```

### Step 4: 결과 보고

```markdown
## Memory Compact 결과

| 항목 | 압축 전 | 압축 후 |
|------|---------|---------|
| 줄 수 | {before_lines} | {after_lines} |
| 크기 | {before_kb}KB | {after_kb}KB |
| 삭제된 항목 | {deleted} |
| 이동된 항목 | {moved} |

### 이동 내역
| 내용 요약 | 이동 대상 |
|-----------|-----------|
| {summary} | memory/{file}.md |
```

## MEMORY.md 올바른 형태 (참고)

```markdown
# MEMORY.md - 프로젝트 장기기억

## 프로젝트 목표
| 목표 | 상태 |
|------|------|
| 핵심 기능 구현 | 🔄 진행중 |

---

## 키워드 인덱스
| 키워드 | 상세 파일 |
|--------|-----------|
| auth, jwt | [memory/architecture.md](memory/architecture.md) |
| hooks, 훅 | [memory/tools.md](memory/tools.md) |

---

## architecture/
→ [memory/architecture.md](memory/architecture.md)

## patterns/
→ [memory/patterns.md](memory/patterns.md)

## tools/
→ [memory/tools.md](memory/tools.md)

## gotchas/
→ [memory/gotchas.md](memory/gotchas.md)

---

## meta/
- **프로젝트**: my-project
- **마지막 업데이트**: 2026-03-08
```

## 금지 사항

- MEMORY.md에 로그 출력, 에러 메시지, 설치 결과를 절대 저장하지 않음
- MEMORY.md에 3줄 이상의 상세 설명을 넣지 않음
- 인덱스 역할이 아닌 내용은 반드시 memory/*.md로 분리

## 관련 파일

| 파일 | 역할 |
|------|------|
| `MEMORY.md` | 압축 대상 |
| `memory/*.md` | 상세 내용 이동 대상 |
| `skills/mnemo/SKILL.md` | 므네모 메모리 시스템 |
| `skills/mnemo/templates/claude-md-rules.md` | CLAUDE.md 규칙 템플릿 |
