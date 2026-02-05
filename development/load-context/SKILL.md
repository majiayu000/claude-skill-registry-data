---
name: load-context
description: |
  도메인/기능의 컨텍스트 빠른 파악. Use when:
  (1) 특정 도메인 이해 필요, (2) 기존 기능 수정 전 파악,
  (3) 세션 시작 시 컨텍스트 로드.
tools: [Read, Glob, Grep, Bash]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: load-context 호출 - {대상}` 시스템 메시지를 첫 줄에 출력하세요.

# Load Context Skill

> 도메인/기능의 빠른 컨텍스트 파악

## When to Use

- 특정 도메인/기능 이해가 필요할 때
- 기존 기능 수정 전 컨텍스트 파악
- 세션 시작 시 작업 컨텍스트 로드
- 버그 수정 전 관련 코드 파악 (`debug-master`와 연계)

## Context Sources

### 1. Spec Documents (specs/)

```bash
# 도메인 스펙 문서 확인
ls specs/{domain}/
# spec.md, plan.md, tasks.md

# 스펙 내용 요약
cat specs/{domain}/spec.md
```

**수집 정보**:
- 요구사항 정의
- 기술 계획
- 작업 항목

### 2. Source Code (domain/)

```bash
# 도메인 코드 구조 확인
ls -la domain/{domain}/

# 주요 파일 목록
find domain/{domain} -name "*.kt" -type f
```

**수집 정보**:
- Entity 구조
- Service 로직
- Controller 엔드포인트
- 예외 처리

### 3. Git History

```bash
# 최근 변경 이력
git log --oneline -10 -- domain/{domain}/

# 최근 변경 내용
git diff HEAD~5 -- domain/{domain}/
```

**수집 정보**:
- 최근 변경 사항
- 변경 이유 (커밋 메시지)
- 담당자

### 4. Related Issues

```bash
# 관련 이슈 확인
gh issue list --label "{domain}" --state all --limit 5
```

**수집 정보**:
- 진행 중인 이슈
- 완료된 이슈
- 알려진 문제

### 5. Test Files

```bash
# 테스트 파일 확인
ls src/test/**/*{Domain}*.kt
```

**수집 정보**:
- 테스트 커버리지
- 테스트 시나리오

> 📚 **상세 소스 목록**: [references/context-sources.md](references/context-sources.md)

## Workflow

```text
1. 대상 식별
   ├── 도메인명 추출
   └── 관련 경로 매핑

2. Spec 문서 수집
   ├── specs/{domain}/ 존재 확인
   └── spec.md, plan.md 요약

3. 코드 구조 분석
   ├── domain/{domain}/ 파일 목록
   ├── 주요 클래스/함수 식별
   └── 의존성 파악

4. 이력 확인
   ├── git log 최근 변경
   └── 관련 이슈/PR

5. 컨텍스트 요약 출력
```

## Output Format

```markdown
[SEMO] Skill: load-context 호출 - {domain}

## 📋 컨텍스트 요약: {Domain}

### 📄 Spec 상태
| 파일 | 상태 | 요약 |
|------|------|------|
| spec.md | ✅/❌ | {brief_summary} |
| plan.md | ✅/❌ | {brief_summary} |
| tasks.md | ✅/❌ | {progress} |

### 📁 코드 구조
```text
domain/{domain}/
├── entity/{Domain}.kt         # {entity_fields_count} fields
├── repository/{Domain}Repository.kt
├── service/
│   ├── {Domain}CommandService.kt  # {command_methods}
│   └── {Domain}QueryService.kt    # {query_methods}
├── web/{Domain}Controller.kt      # {endpoints_count} endpoints
└── exception/{Domain}Exception.kt
```

### 🔄 최근 변경
| 날짜 | 커밋 | 내용 |
|------|------|------|
| {date} | {hash} | {message} |

### 🎫 관련 이슈
- #{issue_number}: {issue_title} ({state})

### 📊 테스트 현황
- 테스트 파일: {test_file_count}개
- 주요 테스트: {test_classes}

### 🔗 연관 도메인
- {related_domain_1}
- {related_domain_2}

---

**다음 작업 제안**:
1. {suggestion_1}
2. {suggestion_2}
```

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--deep` | 상세 분석 (코드 내용 포함) | `load-context posts --deep` |
| `--spec-only` | Spec 문서만 확인 | `load-context posts --spec-only` |
| `--code-only` | 코드 구조만 확인 | `load-context posts --code-only` |
| `--history` | Git 이력 중심 | `load-context posts --history` |

## Usage Examples

### 기본 사용

```
"posts 도메인 컨텍스트 파악해"
→ skill:load-context posts

# Spec, 코드 구조, 최근 변경, 이슈 모두 확인
```

### 상세 분석

```
"채팅 기능 자세히 분석해줘"
→ skill:load-context chat --deep

# 코드 내용까지 포함한 상세 분석
```

### 수정 전 파악

```
"알림 기능 수정하려는데 먼저 파악해줘"
→ skill:load-context notification

# 컨텍스트 파악 후 debug-master로 연계 가능
```

## Integration Points

| Tool/Agent | When |
|------------|------|
| `debug-master` | 컨텍스트 파악 후 버그 수정 |
| `spec-master` | Spec 누락 시 작성 제안 |
| `implementation-master` | 구현 전 컨텍스트 확인 |

## Critical Rules

1. **읽기 전용**: 코드 수정하지 않음
2. **요약 중심**: 핵심 정보만 추출
3. **연계 제안**: 다음 작업 자동 제안
4. **최신 정보**: Git 이력으로 최신 상태 확인

## References

- [Context Sources](references/context-sources.md)
- [Output Format](references/output-format.md)
