---
name: claude
description: Delegate prompts to Claude Code CLI
---

# Claude Code CLI Skill

Claude Code CLI를 사용하여 작업을 수행합니다.

## 1. 사용 가능한 모델

### 1.1. CLI가 제공하는 모델

- `claude-4.5-sonnet` **기본 모델**
- `claude-4.5-opus`
- `claude-4.5-haiku`

## 2. 사용 방법

CLI를 비대화형 모드(`-p`)로 실행하며, 권한 검사를 건너뛰는 모드(`--dangerously-skip-permissions`)를 사용할 수 있습니다.

### 예시

```bash
# 기본 사용
claude -p "여기에 프롬프트 입력" --dangerously-skip-permissions

# 모델 지정 사용
claude -p "여기에 프롬프트 입력" --model "claude-3-opus-20240229" --dangerously-skip-permissions