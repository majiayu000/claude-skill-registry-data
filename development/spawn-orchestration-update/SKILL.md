---
name: spawn-orchestration-update
description: 오케스트레이션 업데이트가 필요할 때 orchestration-update-agent 활용 가이드
allowed-tools: Task, Read, Bash
---

# Orchestration Update Agent 활용 가이드

/orchestration-update 명령 실행 시 orchestration-update-agent를 활용하는 방법입니다.

## 언제 사용하나?

- 사용자가 `/orchestration-update` 명령 실행 시
- 오케스트레이션 시스템 업데이트가 필요할 때
- 서브모듈 최신화가 필요할 때

## Spawn 방법

### 1. 명령어 파싱

사용자 입력에서 옵션 추출:
- `--version {ver}`: 특정 버전
- `--dry-run`: 미리보기
- `--force`: 강제 실행

### 2. Spawn 실행

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

```
Task tool 호출:
  subagent_type: "orchestration-update-agent"
  run_in_background: true
  prompt: |

옵션:
- version: {지정된 버전 또는 'latest'}
- dry_run: {true/false}
- force: {true/false}

.claude/agents/orchestration-update-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 3. 결과 확인

orchestration-update-agent 결과 확인:
- COMPLETED: 업데이트 성공
- FAILED: 업데이트 실패 (롤백됨)
- DRY_RUN: 미리보기 결과

## 결과 처리

### 성공 시

```markdown
## orchestration-update-agent 결과
- 상태: COMPLETED
- 버전 변경: v1.0.0 → v1.1.0
- 업데이트된 파일: [목록]
```

→ 사용자에게 결과 보고

### 실패 시

```markdown
## orchestration-update-agent 결과
- 상태: FAILED
- 에러: [에러 내용]
- 복구 상태: 백업에서 복원됨
```

→ 에러 원인 분석 및 사용자에게 안내

### DRY_RUN 시

```markdown
## orchestration-update-agent 결과
- 상태: DRY_RUN
- 변경 예정: [목록]
```

→ 변경 예정 내용 사용자에게 표시, 실제 실행 여부 확인

## 주의사항

1. **서브모듈 확인**: `.claude-orchestration/` 없으면 안내 메시지 출력
2. **config.json 확인**: 없으면 `/orchestration-init` 안내
3. **결과 전달**: 성공/실패 결과를 사용자에게 명확히 전달

---
<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
