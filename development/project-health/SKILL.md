---
name: project-health
description: 프로젝트 상태 점검 및 건강 진단. 상태, 점검, health, check, inspect 키워드에 자동 활성화.
allowed-tools: Read, Bash, Grep, Glob
---

# Project Health Skill

## SDD 점검 기준

### 필수 디렉토리 구조

```
idea-on-action/
├── spec/           # Stage 1: 명세
│   ├── requirements.md
│   ├── acceptance-criteria.md
│   └── constraints.md
├── plan/           # Stage 2: 계획
│   ├── architecture.md
│   ├── tech-stack.md
│   └── implementation-strategy.md
├── tasks/          # Stage 3: 작업
│   ├── sprint-N.md
│   └── backlog.md
└── src/            # Stage 4: 구현
```

---

## 점검 명령어

### SDD 구조 확인

```bash
ls -la spec/ plan/ tasks/ 2>/dev/null
```

### 빌드 점검

```bash
npm run build 2>&1 | tail -5
```

### 린트 점검

```bash
npm run lint 2>&1 | grep -E "warning|error" | wc -l
```

### 테스트 점검

```bash
npm run test 2>&1 | tail -10
```

### 버전 동기화 확인

```bash
grep '"version"' package.json
grep "현재 버전" CLAUDE.md
grep "프로젝트 버전" docs/INDEX.md
```

### 대용량 문서 확인

```bash
find docs/ -name "*.md" -exec wc -l {} + 2>/dev/null | sort -rn | head -10
```

### TypeScript 에러

```bash
npx tsc --noEmit 2>&1 | grep -c "error" || echo "0"
```

### 의존성 취약점

```bash
npm audit 2>&1 | grep -E "vulnerabilities|found"
```

### TODO/FIXME 수

```bash
grep -r "TODO\|FIXME" src/ --include="*.ts" --include="*.tsx" | wc -l
```

---

## 상태 분류 기준

### 🔴 즉시 조치 (Critical)

| 항목 | 조건 | 조치 |
|------|------|------|
| 빌드 실패 | exit code != 0 | debugger Agent 호출 |
| 보안 취약점 | high/critical 존재 | npm audit fix |
| 버전 불일치 | package.json ≠ CLAUDE.md | project-organizer Agent 호출 |
| 필수 디렉토리 누락 | spec/plan/tasks 없음 | 디렉토리 생성 |

### 🟡 개선 권장 (Warning)

| 항목 | 조건 | 권장 조치 |
|------|------|----------|
| 린트 경고 | 10개 이상 | npm run lint --fix |
| 테스트 실패 | 1개 이상 실패 | test-runner Agent 호출 |
| 대용량 문서 | 1000줄 초과 | 분할/아카이브 |
| TODO/FIXME | 20개 이상 | 정리 필요 |

### 🟢 양호 (Good)

| 항목 | 조건 |
|------|------|
| 빌드 성공 | exit code = 0 |
| 린트 경고 | 0개 |
| 테스트 통과 | 전체 통과 |
| 버전 동기화 | 모두 일치 |

---

## 병렬 조치 트리거

즉시 조치 항목 발견 시 자동으로 병렬 Agent 호출:

```
점검 결과 분석
    │
    ├── 빌드 실패 ──────→ debugger Agent
    │
    ├── 테스트 실패 ────→ test-runner Agent
    │
    ├── 버전 불일치 ────→ project-organizer Agent
    │
    └── 코드 품질 이슈 ──→ code-reviewer Agent
```

### 병렬 호출 예시

```
🔴 즉시 조치 필요:
1. 빌드 실패 (TypeScript 에러)
2. 테스트 3개 실패

→ [병렬 실행]
  - debugger Agent: TypeScript 에러 분석
  - test-runner Agent: 실패 테스트 분석

→ [결과 종합]
  - 수정 사항 통합
  - 최종 상태 재점검
```

---

## 점검 워크플로우

### 1. 전체 점검 실행

```bash
# 한 번에 실행
echo "=== SDD 구조 ===" && ls -la spec/ plan/ tasks/ 2>/dev/null
echo "=== 버전 동기화 ===" && grep '"version"' package.json && grep "현재 버전" CLAUDE.md
echo "=== 빌드 ===" && npm run build 2>&1 | tail -3
echo "=== 린트 ===" && npm run lint 2>&1 | tail -3
```

### 2. 상태 보고서 생성

점검 결과를 테이블 형식으로 정리:

```markdown
| 항목 | 상태 | 수치/비고 |
|------|------|----------|
| SDD 구조 | ✅ | spec, plan, tasks 존재 |
| 빌드 | ✅ | 성공 |
| 린트 | ⚠️ | 경고 5개 |
| 테스트 | ✅ | 100% 통과 |
| 버전 동기화 | ✅ | 2.39.0 |
```

### 3. 조치 실행

- 🔴 즉시 조치: 병렬 Agent 자동 호출
- 🟡 개선 권장: 사용자 확인 후 조치
- 🟢 양호: 보고만

---

## 주의사항

1. **읽기 전용** - 이 Skill은 상태 점검만 수행
2. **수정 필요 시** - project-organizer Agent 또는 해당 Agent 호출
3. **KST 시간대** 기준으로 점검 일시 표기
4. **모든 출력은 한글**로 작성
