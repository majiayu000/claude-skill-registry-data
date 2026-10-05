---
name: skill-guide
description: >
  이 레포에서 새 스킬을 작성하거나 기존 스킬을 수정할 때 사용하는 가이드.
  "스킬 만들어줘", "새 skill 추가", "SKILL.md 작성", "스킬 구조",
  "스킬 수정해줘", "스킬 가이드", "description 다듬기",
  "frontmatter 작성", "스킬 검증" 등의 요청에서 트리거.
  스킬 스펙(frontmatter, description, Progressive Disclosure),
  디렉토리 구조 패턴, 작성 원칙을 제공한다.
---

# Skill Guide

이 레포에서 스킬을 만들거나 수정할 때 따르는 가이드.
상세 스펙은 `references/guide.md` 참조.

## 이 레포 컨벤션

- 경로: `skills/<kebab-case-name>/SKILL.md`
- 기본은 shallow layout (SKILL.md 단독). 참조 문서가 필요하면 `references/` 추가.
- 한국어 위주, 명령형 톤. 기존 스킬(trace-change-why, session-history)과 톤 일관성 유지.
- README.md 스킬 테이블에 행 추가.

## 어떤 스킬을 만들까

스킬 아이디어가 있으면 아래 유형에 매핑해 본다. 좋은 스킬은 여러 유형의 교차점에 있다.

| 유형 | 핵심 | 이 레포 예시 |
|------|------|-------------|
| **라이브러리/API 레퍼런스** | 내부 라이브러리, CLI, SDK의 엣지케이스와 footgun | — |
| **제품 검증** | 유저 플로우를 브라우저/CLI로 직접 구동하여 동작 확인 | — |
| **데이터 수집/분석** | 데이터 소스 연결, 쿼리 패턴, 대시보드 매핑 | video-subtitle-dl |
| **업무 자동화** | 반복 워크플로우를 하나의 커맨드로 | session-history, commit-msg |
| **코드 스캐폴딩** | 프레임워크 보일러플레이트 + 프로젝트 설정 자동 생성 | — |
| **코드 품질/리뷰** | 스타일 강제, 테스트 관행, 적대적 리뷰 | self-feedback-loop |
| **CI/CD & 배포** | PR 모니터링, 빌드→테스트→배포 파이프라인 | — |
| **런북** | 증상 → 진단 → 소견 다단계 분석 | trace-change-why |
| **인프라 운영** | 프로세스 관리, 리소스 정리, 비용 조사 | tmux |

스킬 가치를 높이는 질문:
- Claude가 이 작업을 **기본적으로 잘 못하는 부분**이 있는가? (있으면 스킬로 만들 가치가 높다)
- 이 작업을 할 때 **매번 같은 설명을 반복**하고 있는가?
- **실패한 적이 있는** 엣지케이스가 있는가? (→ Gotchas 섹션의 씨앗)

## 작성 체크리스트

### 1. Frontmatter

```yaml
---
name: kebab-case-name # 필수. 디렉토리명과 일치, 1-64자
description: > # 필수. 1-1024자, < > 금지
  스킬이 하는 일 + 구체적 트리거 문구.
  사용자가 실제로 말할 법한 표현 포함.
  "언더트리거" 방지를 위해 약간 pushy하게.
---
```

### 2. Description — 트리거의 핵심

- description은 에이전트가 스킬 활성화를 결정하는 **유일한 기준**
- 스킬 기능 + 트리거 컨텍스트 모두 포함
- 추상적 설명("PDF 도구") 대신 구체적 행동("PDF 읽기, 병합, OCR…")
- **한국어 + 영어 트리거 문구 병기** — 이 레포 스킬은 전부 이중 언어 트리거를 사용. 사용자가 어느 언어로 말해도 활성화되도록.

### 3. 본문 구조

- 스킬 목적 1-2줄 요약
- 절차/워크플로우를 번호 매긴 단계로
- 명령형 사용 ("Run…", "Save…" — "You should…" 금지)
- ALWAYS/NEVER 대신 **이유 설명**
- 출력 포맷이 있으면 템플릿 명시
- **Gotchas 섹션 필수** — 실제 실패/엣지케이스에서 빌드업. 스킬에서 가장 가치 높은 콘텐츠.
- **Don't State the Obvious** — Claude가 이미 아는 것(일반적 코딩 패턴, 프레임워크 기본)은 쓰지 말 것. Claude가 잘 못하는 부분만 집중.
- **Avoid Railroading** — 모든 단계를 과도하게 지정하면 엣지케이스에서 유연성이 떨어진다. 핵심 제약만 명시하고 판단 여지를 남길 것.

### 4. 크기 관리 (Progressive Disclosure)

| 단계                  | 로드 시점      | 크기 권장 |
| --------------------- | -------------- | --------- |
| name + description    | 항상           | ~100 단어 |
| SKILL.md 본문         | 트리거 시      | < 500줄   |
| references/, scripts/ | 명시적 필요 시 | 무제한    |

- 500줄 초과 → `references/`로 분리
- 300줄 초과 참조 파일 → 목차 포함
- `scripts/`는 실행만 되고 컨텍스트 소비 없음

### 5. 디렉토리 구조 패턴

| 패턴          | 구조                                                        |
| ------------- | ----------------------------------------------------------- |
| 단순          | `SKILL.md` 단독                                             |
| 참조 포함     | `SKILL.md` + `references/`                                  |
| 스크립트 포함 | `SKILL.md` + `scripts/` (실행 코드, 컨텍스트 소비 없음)     |
| 규칙 기반     | `SKILL.md` + `AGENTS.md` + `rules/`                         |
| 커맨드 포함   | `SKILL.md` + `command/`                                     |
| 도메인 분기   | `SKILL.md` + `references/{domain}.md`                       |
| 복합 플러그인 | `SKILL.md` + `skills/` + `hooks/` + `commands/` + `agents/` |

### 6. 검증

- frontmatter 파싱: `rg -n '^name:|^description:' skills/<name>/SKILL.md`
- 설치 테스트: `npx skills add ./`
- 트리거 확인: 2-3개 현실적 프롬프트로 스킬이 활성화되는지 확인

## Gotchas

- description에 `<` 또는 `>` 문자가 포함되면 frontmatter 파싱이 깨진다. YAML 블록 스칼라(`>` 또는 `|`)를 사용하고, 본문 내 꺾쇠는 피할 것.
- 500줄 기준은 references 분리를 고려하는 시점이지, SKILL.md가 501줄이면 안 되는 것이 아니다. 분리의 판단 기준은 "이 내용이 매번 필요한가?"
- `npx skills add ./` 테스트는 skills CLI가 설치된 환경에서만 동작한다. CI가 없는 이 레포에서는 frontmatter 파싱(`rg`)과 트리거 확인이 실질적 검증.
- description을 사람이 읽기 좋게 쓰면 모델이 트리거를 놓친다. description은 모델용 — 사용자의 실제 발화 패턴을 포함해야 함.
- 기존 스킬의 톤/스타일과 불일치하면 사용자 경험이 어색해진다. 새 스킬 작성 전 기존 스킬 1-2개를 반드시 읽고 톤을 맞출 것.

## 설계 패턴

### Scripts — 실행 코드 번들링

반복되는 bash 명령 조합이나 복잡한 옵션을 `scripts/`에 추출한다. Claude가 스크립트를 직접 실행하므로 안정성이 높아지고, 컨텍스트도 소비하지 않는다.

- 스크립트에 `#!/usr/bin/env bash`와 `set -euo pipefail` 포함
- SKILL.md에서 `bash scripts/<name>.sh`로 호출
- **Fallback 절차 병기** — 스크립트가 실패하거나 의존 도구가 없을 때의 수동 대안을 SKILL.md에 함께 적는다. video-subtitle-dl은 yt-dlp 부재 시 수동 절차를, trace-change-why는 세션 파일 부재 시 git blame fallback을 제공.
- **조합 가능한 코드 제공** — 단순 명령 래퍼 외에, Claude가 즉석에서 조합할 수 있는 함수 라이브러리를 `scripts/`에 포함하는 것도 효과적. 예: 데이터 분석 스킬에서 warehouse 접속 함수 모음을 제공하면 Claude가 이를 조합해 고급 쿼리를 생성.
- ref: `trace-change-why/scripts/find-session.sh`, `video-subtitle-dl/scripts/fetch-subs.sh`

### Mode 선언 — 스킬 활성 중 제약

스킬의 목적에 맞지 않는 도구 사용을 본문 지시로 차단한다. 조사 전용 스킬이 코드를 수정하거나, 리뷰 스킬이 범위 밖 코드를 건드리는 것을 방지.

- 본문 상단에 제약 명시 (예: "이 스킬 활성 중 Edit, Write 사용 금지")
- 도구 차단 외에 **범위 제약**도 포함 — self-feedback-loop는 "플랜에 포함된 변경만" 수정하도록 범위를 제한.
- ref: `trace-change-why`의 읽기 전용 제약, `self-feedback-loop`의 플랜 기반 범위 제한

### 종료 조건 — 루프형 스킬의 탈출 기준

반복 수행하는 스킬에는 명시적 종료 조건이 필수. 없으면 무한 루프에 빠지거나 사용자가 수동으로 중단해야 한다.

- **정량적 기준** 권장 — self-feedback-loop: "material finding 없는 리뷰가 2회 연속이면 종료"
- 트리거 조건과 쌍으로 — session-history: "이 조건에서 트리거하고, 이 조건에서는 트리거하지 말 것"
- 최대 반복 횟수 상한도 고려 — 무한 루프 안전장치

### Setup — 사용자 설정 수집

복잡한 스킬이 사용자별 설정을 필요로 할 때(Slack 채널, API 키 경로, 프로젝트별 옵션 등):

- `config.json`을 스킬 디렉토리에 저장하는 패턴 사용
- 구조화된 선택이 필요하면 `AskUserQuestion` 도구로 질문
- 플러그인 환경에서는 `${CLAUDE_PLUGIN_DATA}/`에 설정 저장 (업그레이드에 안전)

### Memory — 데이터 저장

스킬이 실행 이력이나 설정을 기억해야 할 때, 파일 기반 저장소를 활용한다.

- 업그레이드 시 삭제될 수 있는 스킬 디렉토리 대신 안정적 경로 사용
  - 플러그인: `${CLAUDE_PLUGIN_DATA}/`
  - 단독 스킬: `~/history/` 등 사용자 홈 하위
- JSONL, JSON, markdown 등 자유 포맷
- ref: `session-history/SKILL.md`의 "이력 관리" 섹션

## 상세 참조

다음 항목의 상세 스펙은 `references/guide.md` 참조:

- Frontmatter 전체 필드 (선택 필드 포함)
- Description 최적화 (trigger eval 프로세스)
- AGENTS.md vs Skills 사용 기준
- Skill 생성 워크플로우 (skill-creator 코어 루프)
- 설치/검색 메커니즘, 플러그인 매니페스트
- CLI 명령어, 컬렉션 레포 요건
- 멀티 에이전트 지원 파일 규칙
- 생태계 참조 링크
