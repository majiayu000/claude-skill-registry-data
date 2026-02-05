---
name: python-runner
description: Python 프로젝트 실행, 테스트, 문법 검사, 임포트 검증을 위한 스킬. `scripts/python-runner.sh`를 사용합니다.
allowed-tools: Bash
---

# Python Runner - 파이썬 실행 및 검증 스킬

이 스킬은 `scripts/python-runner.sh` 래퍼 스크립트를 사용하여 `.venv` 가상환경에서 Python 프로젝트를 실행, 테스트 및 검증합니다.

모든 명령어는 `.katarc` 파일에 정의된 현재 `kata` 프로젝트의 컨텍스트에서 실행됩니다.

## 주요 명령어

모든 기능은 `./scripts/python-runner.sh`를 통해 접근합니다.

| 작업 | 명령어 | 설명 |
|---|---|---|
| **테스트 실행** | `./scripts/python-runner.sh test [test_path]` | 모든 테스트 또는 특정 테스트 실행 |
| **프로젝트 실행** | `./scripts/python-runner.sh run [module]` | Python 모듈 실행 (기본값: `{CURRENT_KATA}.main`) |
| **문법 검사** | `./scripts/python-runner.sh syntax-check <file_path>` | Python 파일 문법 검사 |
| **임포트 검증** | `./scripts/python-runner.sh import-check` | 임포트 전략 검증 (절대 임포트) |
| **정리** | `./scripts/python-runner.sh clean` | 빌드 아티팩트 삭제 (`__pycache__`, `.pyc` 등) |
| **도움말** | `./scripts/python-runner.sh help` | 사용 가능한 모든 명령어 확인 |

---

## 사용 예시

### 예시 1: 전체 테스트 실행

**사용자 요청:**
> "테스트 돌려줘"

**스킬 동작:**
```bash
./scripts/python-runner.sh test
```

### 예시 2: 특정 테스트 실행

**사용자 요청:**
> "게임 테스트만 실행해줘"

**스킬 동작:**
```bash
./scripts/python-runner.sh test hidden-number/tests/test_game.py
```

### 예시 3: main.py 실행

**사용자 요청:**
> "main.py 실행해줘"

**스킬 동작:**
```bash
./scripts/python-runner.sh run
```

### 예시 4: 특정 파일 문법 검사

**사용자 요청:**
> "game.py 파일 문법 검사해줘"

**스킬 동작:**
```bash
./scripts/python-runner.sh syntax-check hidden-number/domain/game.py
```

### 예시 5: 임포트 검증

**사용자 요청:**
> "임포트 제대로 됐는지 확인해줘"

**스킬 동작:**
```bash
./scripts/python-runner.sh import-check
```

**출력 예시:**
```text
==> Executing in venv for kata 'hidden-number': ...

1. Searching for relative imports (should be none):
✅ No relative imports found

2. Searching for imports without package name (should be none):
✅ No imports without package name found

3. Testing pytest collection (validates all imports):
collected 10 items
```

### 예시 6: 빌드 아티팩트 정리

**사용자 요청:**
> "캐시 파일 정리해줘"

**스킬 동작:**
```bash
./scripts/python-runner.sh clean
```

---

## 임포트 전략 규칙

이 프로젝트는 다음 임포트 전략을 따릅니다:

### 절대 임포트 (Absolute Import) - 권장

```python
# ✅ 올바른 임포트
from hidden-number.domain.game import Game
from hidden-number.app.game_service import GameService
from hidden-number.infra.random_generator import RandomGenerator
```

### 상대 임포트 (Relative Import) - 비권장

```python
# ❌ 잘못된 임포트 (같은 패키지 내에서도 절대 임포트 권장)
from .game import Game
from ..domain.game import Game
```

### 임포트 오류 수정 예시

**Case 1: 상대 임포트 → 절대 임포트**

```python
# Before (잘못됨)
from .game import Game

# After (올바름)
from hidden-number.domain.game import Game
```

**Case 2: 패키지명 누락**

```python
# Before (잘못됨)
from domain.game import Game

# After (올바름)
from hidden-number.domain.game import Game
```

**Case 3: 순환 임포트 문제**

```python
# 해결 방법 1: TYPE_CHECKING 사용
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hidden-number.domain.game import Game

# 해결 방법 2: 늦은 임포트 (함수 내부)
def some_function():
    from hidden-number.domain.game import Game
    # ...
```

---

## 주의사항

- `.venv` 가상환경이 존재해야 합니다
- 모든 명령어는 `.katarc`에서 `CURRENT_KATA` 값을 읽어 작업 대상 결정
- 스크립트 내부에서 자동으로 가상환경 활성화
- UTF-8 인코딩 자동 설정

## 트러블슈팅

**문제: .venv not found**

```bash
# 가상환경 생성
uv venv
uv sync
```

**문제: ModuleNotFoundError**

```bash
# 프로젝트 재설치
uv pip install -e .
```

**문제: pytest 찾을 수 없음**

```bash
# pytest 설치
uv pip install pytest
```
