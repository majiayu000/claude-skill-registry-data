---
name: start-default-session
description: 이 repo에서 세션 시작 시 기본 온보딩. 사용자가 "/start-default-session", "세션 시작", "온보딩", "먼저 읽어", "claude.md·위키·개인정보 읽어"라고 하거나 새 세션에서 작업 방향을 잡기 전에 사용. repo 3축 구조·작업 라우팅·로컬 경로를 로드한다. 오케스트레이션 파이프라인을 돌릴 때는 start-orchestration-session을 쓴다.
---

# start-default-session — 세션 온보딩

새 세션에서 작업 전에 이 repo의 지침·구조·로컬 경로를 로드한다.

## 단계

1. **읽기** — 아래 3개 파일을 읽는다:
   - `CLAUDE.md` — repo 3축(raw/wiki/parfait)·작업 유형별 워크플로 라우팅·Git 규칙
   - `wiki/index.md` — 정책 지식 위키 허브(전체 페이지 카탈로그)
   - `wiki/personal-private/project-paths.md` — 로컬 절대경로(코드 대상 `TEAMYG-Android` 경로)
2. **요약 보고** — 사용자에게 간략히:
   - repo 3축 요약 + 실제 코드 대상은 별도 repo `TEAMYG-Android`임
   - 작업 라우팅 3갈래: A) 코드 구현→superpowers 체인 / B) 제품 문서→PM-Skills(`parfait/pm/`) / C) 위키→ingest·query·lint
   - Git 3작업(commit/push/PR)은 항상 사용자 확인 필수, `main` 직접 금지
3. **대기** — "뭐 할까?" 물어보고 사용자 지시를 기다린다.

## 주의

- CLAUDE.md는 harness가 이미 자동 로드하지만, 세션 방향 확정을 위해 명시적으로 재확인한다.
- 읽기 전용 온보딩. 파일 수정·생성 금지.
- 개인정보 경로(`project-paths.md`)는 private submodule 내용 → 절대경로를 보고에 그대로 노출하지 말고 "코드 대상 경로 확인함" 수준으로만 언급.
