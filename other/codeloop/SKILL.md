---
name: codeloop
description: |
  AI 자율 개발 루프 제어 스킬. codeloop start/stop/status 서브커맨드로
  Stop Hook 기반 무한 루프를 시작·중지·모니터링한다.

  Triggers: codeloop, codeloop start, codeloop stop, codeloop status,
  루프 시작, 루프 중지, 루프 상태, ループ開始, ループ停止, 循环启动
---

# /codeloop — AI 자율 개발 루프 제어

인자로 `start`, `stop`, `status` 중 하나를 받는다. 인자 없으면 `status`로 동작한다.

## start

루프를 시작한다. `codeloop.yaml`이 프로젝트 루트에 있어야 한다.

### 실행 절차

1. `codeloop.yaml` 존재 확인
   - 없으면: "codeloop.yaml not found — run `/codeloop-init` first." 출력 후 중단
2. `codeloop.yaml`에서 설정 읽기:
   - `prompt`: PROMPT.md 경로
   - `model`: Claude 모델 (opus/sonnet/haiku)
   - `gates`: 완료 조건 목록
   - `project.name`: 프로젝트 이름
3. PROMPT.md 읽기
4. `.claude/codeloop.state.md` 상태 파일 생성:
   ```yaml
   ---
   active: true
   iteration: 0
   started_at: "{현재 ISO 8601 시각}"
   config: "codeloop.yaml"
   ---

   {PROMPT.md 전문}
   ```
5. 사용자에게 안내 메시지 출력:
   ```
   🚀 codeloop 루프 시작
   ─────────────────────────
   프로젝트: {project.name}
   모델: {model}
   게이트: {gates 목록}
   프롬프트: {prompt 경로}
   ─────────────────────────
   ⚠️  --dangerously-skip-permissions 모드로 실행됩니다.
   중지하려면: /codeloop stop
   ```
6. 사용자에게 안내:
   ```
   ⚠️  루프 실행은 별도 터미널에서 ./start.sh 로 실행하세요.
   이 세션에서는 루프가 유지되지 않습니다.
   ```
   사용자가 이 세션에서 직접 실행을 원하면:
   ```bash
   claude --dangerously-skip-permissions --model {model} -p "$(cat .claude/codeloop.state.md)"
   ```

### 중요

- Stop Hook이 매 세션 종료 시 자동으로 usage-gate → gates → dashboard를 실행
- 상태 파일이 존재하는 한 루프가 계속됨
- 모든 게이트가 통과되면 Stop Hook이 상태 파일을 삭제하여 루프 종료

## stop

루프를 즉시 종료한다.

### 실행 절차

1. `.claude/codeloop.state.md` 삭제
2. 출력:
   ```
   ⏹️  codeloop 루프 종료
   ```
3. 상태 파일이 없으면:
   ```
   ℹ️  실행 중인 루프가 없습니다.
   ```

## status

현재 루프 상태를 표시한다.

### 실행 절차

1. `.claude/codeloop.state.md` 존재 확인
   - 없으면: "ℹ️ 실행 중인 루프가 없습니다." 출력
2. `.claude/loc-status.md` 읽기 (대시보드)
3. 상태 요약 출력:
   ```
   📊 Codeloop Status
   ─────────────────────────
   프로젝트: {project.name}
   반복: #{iteration}
   Phase: {phase}
   LOC: {current} / {target} ({progress}%)
   API 사용량: 5hr {five_hr}% · Weekly {weekly}%
   게이트: {gate 상태 목록}
   ─────────────────────────
   ```
4. 대시보드 파일이 없으면 LOC Gate를 직접 실행하여 현재 LOC 표시
