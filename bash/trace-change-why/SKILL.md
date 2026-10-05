---
name: trace-change-why
description: >
  코드 변경의 WHY(원인, 동기, 판단 근거)를 추적하는 스킬.
  세션 트랜스크립트, git blame, 커밋 히스토리에서 변경 의도를 찾아낸다.
  "왜 이렇게 바꿨어?", "이 변경 이유가 뭐야?", "이거 왜 바뀐거야?",
  "이 커밋 의도가 뭐야?", "누가 왜 바꿨어?",
  "이 코드 왜 이렇게 된거야?",
  "why was this changed?", "explain this commit"
  등 변경 의도를 묻는 질문에서 트리거.
  diff나 blame 결과를 보여주며 의도를 물을 때도 트리거.
---

# Trace Change Why

코드 변경의 WHY(원인, 동기, 판단 근거)를 추적하여 설명하는 스킬.
사용자는 diff를 이미 보고 있다. WHAT을 반복하지 말고 WHY를 말하라.

## 읽기 전용 제약 (On Demand)

이 스킬은 조사/분석 전용이다. **스킬 활성 중 Edit, Write 도구를 사용하지 말 것.** 코드를 "수정"하고 싶은 충동이 생겨도 조사 결과만 보고하고, 수정은 사용자가 별도 요청할 때 수행한다.

## 추적 절차

### 1. 현재 세션 확인

이 세션에서 만든 변경이면 이미 맥락을 알고 있다. 바로 설명.

### 2. 변경 대상 식별

- 특정 파일/라인을 지목한 경우: `git diff` 또는 `git diff --staged` 로 해당 변경 확인
- 이미 커밋된 변경인 경우: `git log -p -- <파일경로>` 또는 `git show <커밋>` 로 확인
- 대상이 불명확한 경우: 사용자에게 확인. 추측하지 말 것.
- 변경된 **파일 경로**와 **코드 패턴**(함수명, 변수명 등)을 기록

### 3. 세션 트랜스크립트에서 원인 찾기

세션 디렉토리에서 해당 변경을 만든 Edit/Write 호출을 검색한다.

**빠른 검색 — `scripts/find-session.sh` 사용:**
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/trace-change-why/scripts/find-session.sh" "<파일명 또는 경로 일부>"
```
`CLAUDE_PLUGIN_ROOT`가 없는 환경에서는 스킬 디렉토리의 절대 경로를 직접 사용한다.
스크립트가 세션 디렉토리 경로 변환, 후보 세션 탐색, tool/context match 출력까지 한 번에 수행한다.
`session-bridge`가 함께 설치되어 있으면 공통 locator의 `grep-file` 모드에 위임하고, 없으면 자체 fallback으로 동작한다.

**스크립트 실행 불가 시 수동 절차:**

세션 디렉토리 경로: 프로젝트 경로의 `/` → `-` 변환. 선행 `-` 유지. worktree나 dot path는 저장소에 따라 `.`도 `-`로 바뀔 수 있으므로 exact path 변환만 믿지 말 것.

1. 후보 세션 찾기: `rg -l -F '파일명' ~/.claude/projects ~/.claude/transcripts | head -10`
2. Edit/Write 호출 위치: `rg -n '"name":"(Edit|Write)"|"tool_name":"(Edit|Write)"|"type":"tool_use"' <session>.jsonl | rg -F '파일명'`
3. 맥락 역추적: 해당 라인 번호 직전의 `"role":"user"`, `"role":"assistant"` 메시지를 Read 도구로 확인

### 4. Fallback: 세션을 못 찾은 경우

1. `git log --all --oneline -- <파일경로>` 와 `git blame <파일경로> -L <줄>,<줄>` 로 단서 추출
2. 코드 컨텍스트에서 합리적 이유 추론
3. **추론임을 명시**하고, 확인된 사실과 구분하여 설명

### 5. WHY 중심으로 설명

1. **트리거**: 어떤 요청/문제가 이 변경을 유발했는지
2. **판단 근거**: 왜 이 방식을 선택했는지
3. **변경 요약**: 간략하게만

"이전 세션에서 한 것 같습니다" 같은 애매한 답변 금지. 구체적 맥락을 제시하거나 fallback을 따르라.

## Gotchas

- 프로젝트 경로에 공백, dot path, worktree alias가 있으면 `/ → -` 변환이 깨진다. 스크립트는 raw 변환, dot-normalized 변환, global content search 순으로 fallback한다.
- 대용량 jsonl(10MB+)에서 `grep`이 느리면 `rg`(ripgrep)으로 대체. 동일 문법.
- 여러 세션에 걸친 변경은 최신 세션만 보면 맥락이 누락된다. `grep -l`로 매칭되는 세션이 2개 이상이면 모두 확인.
- `git blame`은 rebase/squash 이후 원래 커밋 정보를 잃는다. `-C -C` 플래그로 코드 이동까지 추적하거나, `git log -p --follow`로 보완.
- 세션 파일이 아예 없을 때(다른 머신에서 작업, 수동 편집 등) 바로 fallback으로 전환. "세션에서 찾을 수 없습니다"를 반복하지 말 것.

## 응답 출력 규칙

모든 응답에서 **확인된 사실**과 **추론**을 명시적으로 분리한다.

- **확인됨**: 세션 트랜스크립트, 커밋 메시지, git blame 등에서 직접 확인한 근거
- **추론**: 코드 컨텍스트, 패턴, 타이밍 등에서 유추한 근거

출력 예시:
```
**확인됨** — 세션에서 사용자가 "N+1 쿼리 제거해줘"라고 요청 (2025-03-15 세션)
**추론** — eager loading 대신 batch loader를 선택한 이유는 기존 코드의 DataLoader 패턴과 일관성을 맞추기 위한 것으로 보임
```

세션에서 직접 확인한 경우에도 판단 근거 해석이 포함되면 해당 부분은 **추론**으로 표기한다.
