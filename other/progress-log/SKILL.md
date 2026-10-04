---
name: progress-log
description: 작업 청크 종료 시점의 .progress/날짜/주제.md 진행 기록
---

# Progress Log

`.claude/skills/progress-log/SKILL.md` 래퍼. 실제 기준 워크플로우는 해당 파일.

## 실행 순서

1. `.claude/skills/progress-log/SKILL.md` 선행 읽기
2. `$ARGUMENTS` 존재 시 주제 슬러그로 사용
3. `$ARGUMENTS` 부재 시 대화 컨텍스트에서 핵심 주제 1-3단어 kebab-case 추론
4. `date +%y%m%d` 기준 `.progress/YYMMDD/<주제>.md` 경로 결정
5. 기존 파일은 Edit 갱신, 신규 파일은 Write 생성
6. `AGENTS.md` 규칙과 `pnpm` 패키지 매니저 기준 적용
