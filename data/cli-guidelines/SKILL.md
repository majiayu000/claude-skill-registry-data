---
name: cli-guidelines
description: Provides CLI design guidelines and best practices. Use when developing command-line tools, designing flags, help text, or error messages.
---

# CLI Guidelines

clig.dev 기반의 CLI 설계 가이드라인과 베스트 프랙티스를 제공합니다.

**핵심 철학**:
- 인간 중심 설계: 사람이 주 사용자
- 상호 연동성: UNIX 관례 준수, 파이프 조합 가능
- 일관성: 기존 패턴 따라 직관성 확보
- 발견 용이성: 도움말, 예제, 오류 제안
- 공감: 사용자의 성공을 돕는 의도 표현

## Instructions

### 워크플로우: 요청 분석 및 리소스 선택

사용자 요청을 분석하여 필요한 리소스만 선택적으로 로드합니다.

#### 1. 키워드 매칭

**철학/원칙** (`resources/01-philosophy.md`)
- "철학", "원칙", "principle"
- "설계", "design"
- "UX", "사용자 경험"

**도움말/문서화** (`resources/02-help-documentation.md`)
- "help", "도움말", "--help"
- "man page", "문서"
- "usage", "사용법"

**출력** (`resources/03-output.md`)
- "output", "출력"
- "색상", "color"
- "JSON", "포맷"
- "stdout", "stderr"
- "로그", "log"

**오류 처리** (`resources/04-errors.md`)
- "error", "오류", "에러"
- "exit code", "종료 코드"
- "예외", "exception"
- "디버그", "debug"

**인자/플래그** (`resources/05-arguments-flags.md`)
- "argument", "인자"
- "flag", "플래그", "옵션"
- "-v", "--verbose"
- "파라미터", "parameter"

**상호작용** (`resources/06-interactivity.md`)
- "interactive", "대화형"
- "prompt", "프롬프트"
- "input", "입력"
- "TTY", "터미널"
- "확인", "confirm"

**서브커맨드** (`resources/07-subcommands.md`)
- "subcommand", "서브커맨드"
- "command", "명령어"
- "verb noun", "noun verb"

**견고성** (`resources/08-robustness.md`)
- "robust", "견고"
- "signal", "시그널"
- "Ctrl-C", "SIGINT"
- "timeout", "타임아웃"
- "진행률", "progress"

**설정** (`resources/09-configuration.md`)
- "config", "설정"
- "environment", "환경변수"
- ".env", "XDG"
- "우선순위", "priority"

**배포/명명** (`resources/10-distribution.md`)
- "배포", "distribution"
- "install", "설치"
- "이름", "naming"
- "바이너리", "binary"

#### 2. 리소스 로딩 전략

**단일 주제**
- User: "플래그 네이밍 규칙이 뭐야?"
- → Read resources/05-arguments-flags.md

**복합 요청**
- User: "CLI 도구 처음부터 만들어줘"
- → Read resources/01-philosophy.md (철학)
- → Read resources/05-arguments-flags.md (인자/플래그)
- → Read resources/02-help-documentation.md (도움말)
- → 필요 시 추가 리소스

**불명확한 요청**
- User: "CLI 잘 만들고 싶어"
- → REFERENCE.md 확인하여 선택지 제시

#### 3. 리소스 적용

1. **현재 CLI 구조 파악**
   - 기존 CLI 코드 확인
   - 사용 중인 CLI 라이브러리 확인 (Click, argparse, clap 등)

2. **리소스 Read**
   - 필요한 리소스만 Read
   - 언어별 CLI 라이브러리 패턴 고려

3. **패턴 적용**
   - 가이드라인에 맞게 CLI 구조 개선
   - 기존 인터페이스 호환성 유지
   - 사용자에게 변경 사항 설명

4. **검증**
   - `--help` 출력 확인
   - 종료 코드 동작 확인
   - 에러 메시지 품질 확인

### 예시

#### 예시 1: 새 CLI 도구 설계

User: "Python으로 파일 변환 CLI 만들어줘"

1. 키워드 매칭: CLI 설계 전반
2. Read resources/01-philosophy.md
3. Read resources/05-arguments-flags.md
4. Read resources/02-help-documentation.md
5. Click 또는 argparse 기반 구조 설계
6. 표준 플래그 적용 (-h, -v, -o, --quiet 등)
7. 도움말 텍스트 작성

#### 예시 2: 에러 처리 개선

User: "CLI 에러 메시지가 불친절해"

1. 키워드 매칭: "에러" → 오류 처리
2. Read resources/04-errors.md
3. 기존 에러 메시지 분석
4. 인간 친화적 메시지로 재작성
5. 해결 방법 제안 추가
6. 적절한 종료 코드 사용

#### 예시 3: 출력 포맷 추가

User: "JSON 출력 옵션 추가해줘"

1. 키워드 매칭: "JSON", "출력" → 출력
2. Read resources/03-output.md
3. --json 플래그 추가
4. 구조화된 출력 구현
5. TTY 감지 로직 확인
6. 기존 출력과 일관성 유지

## 중요 원칙

1. **인간 우선**: TTY에서는 사람 읽기용 출력, 파이프에서는 기계 처리용
2. **일관성**: 기존 UNIX/POSIX 관례 준수
3. **발견 가능**: 도움말, 예제, 오류 제안으로 사용법 안내
4. **견고함**: 빠른 응답, 진행률 표시, 정상 종료 처리
5. **호환성**: 가산적 변경, 비호환 변경 사전 경고

## Technical Details

상세한 가이드라인은 각 리소스 파일 참조:
- `REFERENCE.md`: 리소스 전체 개요
- `resources/01-philosophy.md`: 설계 철학
- `resources/02-help-documentation.md`: 도움말 작성
- `resources/03-output.md`: 출력 가이드라인
- `resources/04-errors.md`: 오류 처리
- `resources/05-arguments-flags.md`: 인자와 플래그
- `resources/06-interactivity.md`: 대화형 인터페이스
- `resources/07-subcommands.md`: 서브커맨드 설계
- `resources/08-robustness.md`: 견고성/시그널 처리
- `resources/09-configuration.md`: 설정 관리
- `resources/10-distribution.md`: 배포/명명 규칙
