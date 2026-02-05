---
name: code-quality-checker
description: >
  코드 품질 검사 자동화. 린트, 포맷, 타입 체크, 보안 스캔 통합.
version: 2.0.0

triggers:
  keywords:
    - "린트"
    - "품질 검사"
    - "코드 체크"
    - "보안 스캔"
    - "ruff"
    - "mypy"
    - "eslint"
  file_patterns:
    - "src/**/*.py"
    - "src/**/*.ts"
    - "**/*.js"
  context:
    - "코드 품질 개선"
    - "린트 오류 수정"

capabilities:
  - run_quality_check
  - auto_fix_lint
  - security_scan

model_preference: haiku

phase: [2, 2.5]
auto_trigger: true
dependencies:
  - code-reviewer
  - security-auditor
token_budget: 1400
---

# Code Quality Checker

코드 품질 검사 자동화 워크플로우입니다.

## Quick Start

```bash
# 전체 품질 검사
python .claude/skills/code-quality-checker/scripts/run_quality_check.py

# Python만 검사
python scripts/run_quality_check.py --python-only

# 자동 수정 적용
python scripts/run_quality_check.py --fix
```

## 검사 항목

### Python

| 도구 | 용도 | 명령어 |
|------|------|--------|
| **ruff** | 린트 + 포맷 | `ruff check src/` |
| **black** | 포맷팅 | `black --check src/` |
| **mypy** | 타입 체크 | `mypy src/` |
| **pip-audit** | 보안 취약점 | `pip-audit` |

### TypeScript/JavaScript

| 도구 | 용도 | 명령어 |
|------|------|--------|
| **eslint** | 린트 | `npx eslint src/` |
| **prettier** | 포맷팅 | `npx prettier --check src/` |
| **tsc** | 타입 체크 | `npx tsc --noEmit` |
| **npm audit** | 보안 취약점 | `npm audit` |

## 검사 수준

### Level 1: 기본 (CI 필수)

```bash
# Python
ruff check src/
black --check src/

# TypeScript
npx eslint src/
npx prettier --check src/
```

### Level 2: 타입 검사 (권장)

```bash
# Python
mypy src/ --strict

# TypeScript
npx tsc --noEmit --strict
```

### Level 3: 보안 (배포 전 필수)

```bash
# Python
pip-audit --strict
bandit -r src/

# TypeScript
npm audit --audit-level=high
```

## 자동 수정

### 안전한 자동 수정

```bash
# Python 포맷팅
black src/
ruff check src/ --fix

# TypeScript 포맷팅
npx prettier --write src/
npx eslint src/ --fix
```

### 수동 확인 필요

| 이슈 | 이유 |
|------|------|
| 타입 오류 | 로직 변경 가능성 |
| 보안 취약점 | 의존성 호환성 |
| 복잡한 린트 규칙 | 의도적일 수 있음 |

## 설정 파일

### Python (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]

[tool.black]
line-length = 100

[tool.mypy]
python_version = "3.11"
strict = true
```

### TypeScript (eslint.config.js)

```javascript
export default [
  {
    rules: {
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/explicit-function-return-type": "warn",
    }
  }
];
```

## CI 통합

### GitHub Actions

```yaml
- name: Code Quality
  run: |
    ruff check src/
    black --check src/
    mypy src/
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
      - id: ruff-format
```

## 오류 해결 가이드

### 일반적인 ruff 오류

| 코드 | 설명 | 해결 |
|------|------|------|
| E501 | 줄 길이 초과 | 줄 분할 또는 무시 설정 |
| F401 | 미사용 import | import 제거 |
| F841 | 미사용 변수 | 변수 제거 또는 _ 사용 |

### mypy 오류

| 오류 | 설명 | 해결 |
|------|------|------|
| Missing return | 반환 타입 누락 | `-> Type` 추가 |
| Incompatible types | 타입 불일치 | 타입 수정 또는 캐스팅 |
| Module has no attribute | 모듈 속성 없음 | 타입 스텁 설치 |

## 관련 도구

| 도구 | 용도 |
|------|------|
| `scripts/run_quality_check.py` | 통합 검사 |
| `code-reviewer` 에이전트 | 코드 리뷰 |
| `security-auditor` 에이전트 | 보안 검사 |
| `/check` | 기존 Command (deprecated) |

---

> 참조: CLAUDE.md 섹션 2 Build & Test
