---
name: monggle-code-qa
version: 1.0.0
description: |
  QA testing - Run tests and auto-fix issues (monggle)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - /qa
  - /qa-only
  - /test
  - monggle qa
---

# qa (monggle)

QA 테스트 실행 및 자동 수정

**Usage:** `/code-qa [options] [target]`

**특정 스킬 테스트:** `/code-qa [스킬|스킬]` - 여러 스킬을 대상으로 QA 테스트 실행

```bash
/code-qa                           # 전체 테스트 + 자동 수정
/code-qa debug review              # debug와 review 스킬 테스트
/code-qa [pipeline|stats|trace]    # pipeline, stats, trace 스킬 테스트
```

**Examples:**
```bash
/code-qa                    # 전체 테스트 + 수정
/code-qa --report           # 보고서만 (수정 없음)
/code-qa --quick            # 빠른 스모크 테스트
/code-qa src/auth.ts        # 특정 파일 테스트
```

## 옵션

| 옵션 | 설명 |
|-----|------|
| `--report` | 보고서만 생성 (수정 안함) |
| `--quick` | 빠른 스모크 테스트 |
| `--format <fmt>` | 출력 형식: json\|text\|markdown |
| `--verbose, -v` | 상세 출력 |

## 테스트 항목

1. **Syntax Check** - Shell, Python, JavaScript/TypeScript 문법
2. **Code Quality** - TODO/FIXME 주문 확인
3. **Debug Statements** - console.log/print 문 확인
4. **Git Status** - 커밋되지 않은 파일 확인

## 자동 수정

기본 모드에서는 다음 문제를 자동 수정:
- Shell script 문법 오류
- Python import 정리
- Debug statement 제거 (선택)

## 사용법 요약

```bash
/code-qa                           # 전체 테스트 + 자동 수정
/code-qa --report                  # 보고서만 출력
/code-qa --quick                   # 빠른 테스트
/code-qa --format json             # JSON 형식 출력
/code-qa path/to/file.ts           # 특정 파일 테스트
```
