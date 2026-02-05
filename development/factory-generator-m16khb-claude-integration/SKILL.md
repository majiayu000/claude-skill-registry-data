---
name: factory-generator
description: '컴포넌트 생성의 핵심 로직을 처리하는 스킬'
license: MIT
triggers:
  - component generation
  - argument parsing
  - file creation
  - user input collection
  - kebab-case validation
  - path building
---

# Factory Generator Skill

## ROLE

컴포넌트 생성의 핵심 로직을 담당하며, 인자 파싱, 사용자 입력 수집, 파일 생성을 처리합니다.

## GUIDELINES

### 1. 인자 파싱 규칙
- 빈 인자: 타입 선택 TUI 표시
- command [name]: 타입=command, 이름 추출
- skill [name]: 타입=skill, 이름 추출
- agent [name]: 타입=agent, 이름 추출
- 그외: 오류 메시지와 유효한 형식 제시

### 2. 이름 검증
- kebab-case 형식 (소문자, 하이픈)
- 3-30자 길이
- 공백이나 특수문자 불가
- 유효하지 않으면 다시 입력 요청

### 3. 경로 생성 규칙
- command: {base_path}/commands/{name}.md
- skill: {base_path}/skills/{name}/SKILL.md
- agent: {base_path}/agents/{name}.md

### 4. 사용자 정보 수집
- 목적 (purpose) 명확히 수집
- 설치 위치 (프로젝트/사용자/플러그인)
- 모델 선택 (Command/Agent만)
- 도구 선택 (Command/Agent만)

## EXAMPLES

### Input
```
Type: agent
Name: typescript-validator
Purpose: TypeScript 코드 유효성 검사 자동화
Location: project
Model: Sonnet
Tools: Read, Grep, Write
```

### Output
```markdown
---
name: typescript-validator
description: 'TypeScript 코드 유효성 검사 자동화 에이전트'
model: claude-sonnet-4-20250414
allowed-tools:
  - Read
  - Grep
  - Write
---

# TypeScript Validator
...
```

## TRIGGER CONDITIONS

- 컴포넌트 생성 요청 시
- 사용자 입력 수집 필요 시
- 파일 경로 결정 필요 시
- 유효성 검사 필요 시