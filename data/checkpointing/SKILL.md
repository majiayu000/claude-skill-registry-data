---
name: checkpointing
description: |
  Save session context to agent configuration files or create full checkpoint files.
  Supports three modes: session history (default), full checkpoint (--full),
  and skill analysis (--full --analyze) for extracting reusable patterns.
metadata:
  short-description: Checkpoint session context with skill extraction support
---

# Checkpointing — 세션 컨텍스트 지속성

**세션 중 작업 기록을 저장하고 재사용 가능한 스킬 패턴을 찾는다.**

## 모드

### Mode 1: Session History(기본값)

CLI 상담 이력을 각 에이전트의 구성 파일에 추가한다.

```
┌─────────────────────────────────────────────────────────────┐
│  .claude/logs/cli-tools.jsonl                               │
│                      ↓                                      │
│  /checkpointing                                             │
│                      ↓                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │  CLAUDE.md   │ │ AGENTS.md    │ │ GEMINI.md            │ │
│  │ ## Session   │ │ ## Session   │ │ ## Session           │ │
│  │ History      │ │ History      │ │ History              │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Mode 2: Full Checkpoint（--full）

전체 작업의 포괄적인 스냅 샷을 만든다.

```
┌─────────────────────────────────────────────────────────────┐
│  Data Sources:                                              │
│  ├─ git log (commits)                                       │
│  ├─ git diff (file changes)                                 │
│  └─ cli-tools.jsonl (Codex/Gemini logs)                     │
│                      ↓                                      │
│  /checkpointing --full                                      │
│                      ↓                                      │
│  .claude/checkpoints/2026-01-28-153000.md                   │
│  ├─ Summary (commits, files, consultations)                 │
│  ├─ Git History (commits list)                              │
│  ├─ File Changes (created, modified, deleted)               │
│  └─ CLI Consultations (Codex/Gemini)                        │
└─────────────────────────────────────────────────────────────┘
```

### Mode 3: Skill Analysis（--full --analyze）

체크포인트에서 스킬화할 수 있는 패턴을 발견한다.

```
┌─────────────────────────────────────────────────────────────┐
│  /checkpointing --full --analyze                            │
│                      ↓                                      │
│  1. Full Checkpoint 생성                                   │
│  2. 분석용 프롬프트 생성                                    │
│     → .claude/checkpoints/YYYY-MM-DD-HHMMSS.analyze-prompt.md│
│                      ↓                                      │
│  3. 서브에이전트에서 AI 분석 수행                            │
│     → 작업 패턴 발견                                      │
│     → 스킬 후보 제안                                        │
│                      ↓                                      │
│  4. 새로운 스킬을 .claude/skills/에 추가                         │
└─────────────────────────────────────────────────────────────┘
```

**발견할 패턴 예시:**
- 테스트 → 구현 반복(TDD 워크플로우)
- 연구 → 설계 → 실장 흐름
- 특정 파일 세트의 동시 변경
- CLI 상담 → 코드 변경 순서

## 사용법

```bash
# Session History 모드(기본값)
/checkpointing

# Full Checkpoint 모드
/checkpointing --full

# Skill Analysis 모드(권장)
/checkpointing --full --analyze

# 기간 지정
/checkpointing --since "2026-01-26"
/checkpointing --full --analyze --since "2026-01-26"
```

### Skill Analysis 실행 흐름

```bash
# Step 1: 체크포인트 + 분석 프롬프트 생성
python checkpoint.py --full --analyze

# Step 2: 서브에이전트에서 분석(Claude 자동 실행)
# → 분석 프롬프트 로드
# → 스킬 후보 제안
# → 사용자가 승인하면 스킬 생성
```

## 처리 내용

### Session History 모드

1. `.claude/logs/cli-tools.jsonl` 구문 분석
2. Codex/Gemini에 상담 내용을 날짜별로 정리
3. 각 에이전트 구성 파일에 `## Session History` 추가

### Full Checkpoint 모드

1. **Git 정보 수집**
   - `git log`로 커밋 내역
   - `git diff --name-status`로 파일 변경
   - `git diff --numstat`로 행 수 변경

2. **CLI 상담 로그 분석**
   - Codex상담 내용 및 상태
   - Gemini조사 내용 및 상태

3. **체크포인트 파일 생성**
   - `.claude/checkpoints/YYYY-MM-DD-HHMMSS.md`

## Full Checkpoint 형식

```markdown
# Checkpoint: 2026-01-28 15:30:00 UTC

## Summary
- **Commits**: 5
- **Files changed**: 12 (8 modified, 3 created, 1 deleted)
- **Codex consultations**: 3
- **Gemini researches**: 2

## Git History

### Commits
- `abc1234` Add checkpointing enhancement
- `def5678` Update documentation

### File Changes

**Created:**
- `new_feature.py` (+120)

**Modified:**
- `checkpoint.py` (+80, -20)
- `SKILL.md` (+45, -10)

**Deleted:**
- `old_script.py`

## CLI Tool Consultations

### Codex (3 consultations)
- ✓ 설계: 체크포인트 확장 아키텍처
- ✓ 디버깅: Git log parsing issue

### Gemini (2 researches)
- ✓ 조사: Git integration best practices
```

## Session History 형식

```markdown
## Session History

### 2026-01-26

**Codex상담:**
- ✓ 하위 에이전트 패턴으로 Codex / Gemini 호출 권장...

**Gemini조사:**
- ✓ MCP vs CLI 비교 조사...
```

## 실행 타이밍

| 타이밍 | 권장 모드 |
|-----------|-----------|
| 세션 종료 전 | `--full --analyze` |
| 중요한 설계 결정 후 | `--full` |
| 큰 기능 구현 완료 후 | `--full --analyze` |
| 장시간 작업 구분 |`--full` |
| 반복 패턴을 느꼈을 때 | `--full --analyze` |
| 일일 가벼운 기록 | 기본 |

## 주의사항

- 로그가 비어 있으면 아무 것도 추가되지 않는다.
- 기존 '## Session History'섹션은 덮어 쓴다.
- 로그 파일 자체는 변경되지 않는다 (읽기 전용)
- Full Checkpoint는 `.claude/checkpoints/`에 축적된다.
- Git 초기화되지 않은 프로젝트에서도 CLI 로그 부분이 작동한다.
-`--analyze` 로 생성된 스킬 제안은 인간이 검토하고 나서 채용하는 것이다.
- 스킬 분석은 패턴을 고정하지 않고 AI가 자유롭게 발견하는 설계를 한다.
