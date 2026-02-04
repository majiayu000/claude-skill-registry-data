---
name: command-analytics
description: >
  커맨드, 스킬, 에이전트 사용 빈도 측정 및 리포트 생성.
  미사용 항목 식별, 최적화 제안 제공.
version: 2.0.0

triggers:
  keywords:
    - "analytics"
    - "사용량"
    - "미사용"
    - "통계"
  file_patterns:
    - ".claude/analytics/**/*"
  context:
    - "커맨드 사용 빈도 분석"
    - "미사용 항목 정리"

capabilities:
  - generate_report
  - identify_unused
  - usage_trend

model_preference: haiku

auto_trigger: false
---

# Command Analytics

커맨드, 스킬, 에이전트의 사용 빈도를 측정하고 최적화 제안을 제공합니다.

> **주의**: `/usage`는 Claude Code **내장 명령어** (토큰/비용 표시)입니다.
> 이 스킬은 `/analytics` 명령어를 사용합니다.

## Quick Start

```bash
# 커맨드 사용 빈도 리포트
/analytics                    # 전체 요약
/analytics top 10             # 상위 10개
/analytics unused             # 미사용 항목
/analytics report --weekly    # 주간 보고서

# Claude Code 내장 (토큰 사용량) - 별도
/usage                        # 토큰, 비용 표시
```

## 데이터 저장 구조

```
.claude/analytics/
├── commands.jsonl        # 커맨드 사용 로그
├── skills.jsonl          # 스킬 사용 로그
├── agents.jsonl          # 에이전트 사용 로그
└── reports/              # 생성된 보고서
    └── 2025-W50.md
```

## 로그 스키마

```jsonl
// commands.jsonl
{"ts": "2025-12-10T10:30:00", "cmd": "/work", "args": "API 개선", "duration_ms": 45000, "status": "success", "project": "wsoptv"}
{"ts": "2025-12-10T11:00:00", "cmd": "/commit", "args": "", "duration_ms": 5000, "status": "success", "project": "wsoptv"}

// skills.jsonl
{"ts": "2025-12-10T10:30:00", "skill": "tdd-workflow", "trigger": "auto", "duration_ms": 30000, "status": "success"}

// agents.jsonl
{"ts": "2025-12-10T10:30:00", "agent": "Explore", "task": "코드베이스 분석", "duration_ms": 15000, "status": "success"}
```

## 수동 로깅 (Hook 미사용 시)

세션 시작 시:
```bash
# .claude/analytics/commands.jsonl에 직접 추가
echo '{"ts":"'$(date -Iseconds)'","cmd":"/work","args":"...",..."status":"success"}' >> .claude/analytics/commands.jsonl
```

## 리포트 형식

### /analytics (전체 요약)

```markdown
# 사용량 요약 (최근 30일)

## 커맨드 TOP 5
| 순위 | 커맨드 | 횟수 | 평균 시간 |
|------|--------|------|-----------|
| 1 | /work | 45 | 2분 30초 |
| 2 | /commit | 38 | 5초 |
| 3 | /check | 25 | 15초 |
| 4 | /issue | 18 | 30초 |
| 5 | /tdd | 12 | 3분 |

## 미사용 커맨드 (30일+)
- /changelog (마지막: 45일 전)
- /optimize (마지막: 60일 전)
- /journey (사용 없음)

## 권장 조치
1. `/journey` 삭제 검토 (전혀 사용 안됨)
2. `/changelog`를 `/commit`에 통합 검토
```

### /analytics unused

```markdown
# 미사용 항목 (30일 기준)

## 커맨드 (6개)
| 커맨드 | 마지막 사용 | 권장 |
|--------|------------|------|
| /journey | 없음 | 삭제 |
| /compact | 없음 | 삭제 |
| /changelog | 45일 전 | 유지 |
| /optimize | 60일 전 | 유지 |
| /api-test | 없음 | /check 통합 |
| /final-check | 30일 전 | 유지 |

## 스킬 (2개)
| 스킬 | 마지막 사용 | 권장 |
|------|------------|------|
| journey-sharing | 없음 | 삭제 |
| phase-validation | 45일 전 | 유지 |

## 에이전트 (0개)
모든 에이전트 활발히 사용 중
```

### /analytics report --weekly

```markdown
# 주간 사용량 보고서
**기간**: 2025-12-02 ~ 2025-12-08

## Executive Summary
- 총 커맨드 실행: 127회
- 총 에이전트 호출: 89회
- 평균 세션 시간: 45분
- 가장 활발한 프로젝트: wsoptv (52%)

## 일별 트렌드
```
Mon ████████████████ 28
Tue ██████████████ 24
Wed ████████████ 20
Thu ██████████████████ 30
Fri ████████████ 20
Sat ██ 3
Sun ██ 2
```

## 프로젝트별 분포
- wsoptv: 52%
- archive-statistics: 28%
- db_architecture: 15%
- 기타: 5%

## 권장 사항
1. 주말 사용량 낮음 - 자동화 스크립트 검토
2. /work 사용률 높음 - 효율적
3. /parallel 사용률 낮음 - 활용도 개선 필요
```

## 자동 수집 (향후 Hook 연동)

```python
# .claude/hooks/post-command.py (향후 구현)
import json
from datetime import datetime

def log_command(cmd, args, duration_ms, status):
    entry = {
        "ts": datetime.now().isoformat(),
        "cmd": cmd,
        "args": args,
        "duration_ms": duration_ms,
        "status": status,
        "project": get_current_project()
    }
    with open(".claude/analytics/commands.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
```

## 정리 권장 기준

| 미사용 기간 | 권장 조치 |
|------------|-----------|
| 30일 미만 | 유지 |
| 30-60일 | 검토 |
| 60-90일 | 통합/축소 검토 |
| 90일+ | 삭제 검토 |

## 관련

- `/check` - 코드 품질 검사
- `docs/SUBREPO_ANALYSIS_REPORT.md` - 서브레포 분석
