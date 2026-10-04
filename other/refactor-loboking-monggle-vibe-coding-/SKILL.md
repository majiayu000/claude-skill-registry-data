---
name: refactor
description: Function 단위 리팩토링 검토를 수행합니다.
---

# refactor - Function-level Refactoring Review

Function 단위 리팩토링 검토를 수행합니다.

## Usage

```bash
/refactor [file] [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--threshold N` | 복잡도 임계값 설정 (기본값: 10) |
| `--length N` | 최대 함수 길이 설정 (기본값: 50 라인) |
| `--all` | 모든 함수 표시 (문제 있는 함수만 아니고) |
| `--fix` | 리팩토링 제안 표시 |
| `-v, --verbose` | 상세 출력 |

## Examples

```bash
# 기본 분석
/refactor src/main.ts

# 임계값 변경
/refactor --threshold 15 --length 100 app.py

# 리팩토링 제안 포함
/refactor --fix file.go

# 모든 함수 표시
/refactor --all file.sh
```

## 분석 항목

- **함수 길이**: 너무 긴 함수 탐지
- **복잡도**: Cyclomatic Complexity 분석
- **명명 규칙**: 함수 이름 검사

## 지원 언어

- TypeScript/JavaScript
- Python
- Kotlin
- Java
- Go
- Rust
- Ruby
- PHP
- Bash
