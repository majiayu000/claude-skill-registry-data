---
name: factory-researcher
description: '웹 문서 및 GitHub 예제 분석 전문 스킬'
license: MIT
triggers:
  - documentation research
  - github examples
  - webfetch
  - websearch
  - best practices
  - code examples
---

# Factory Researcher Skill

## ROLE

컴포넌트 생성에 필요한 최신 정보와 예제를 웹에서 수집하여 최적의 결과물을 생성하도록 지원합니다.

## GUIDELINES

### 1. 리서치 전략
- 공식문서 우선 (anthropic.com, claude.ai)
- GitHub 예제 분석 (anthropic-ai, claude-ai 관련)
- 기술 블로그 (Medium, Dev.to)
- Stack Overflow 참고

### 2. 검색 쿼리 패턴
- "{keyword} official documentation 2025"
- "{keyword} best practices tutorial"
- "{keyword} NestJS/React/etc integration"
- "Claude Code {type} {keyword} example"

### 3. 콘텐츠 추출 규칙
- 설치 명령어
- 설정 예제
- API 패턴과 코드 스니펫
- 일반적인 문제점과 해결책
- 버전별 주의사항

### 4. 품질 평가 기준
- 2024년 이후 발행
- 코드 예제 포함
- Claude Code 특정 언급
- 명확하고 실행 가능한 내용

### 5. 연구 결과 구조
```json
{
  "sources": ["URL 목록"],
  "key_findings": {
    "installation": ["설치 명령어"],
    "configuration": ["설정 예제"],
    "best_practices": ["모범 사례"],
    "common_issues": ["일반적인 문제"]
  },
  "code_examples": [
    {
      "language": "typescript",
      "code": "코드",
      "source": "URL",
      "description": "설명"
    }
  ]
}
```

## EXAMPLES

### Input
```
Component: typescript-linter
Research preference: 공식문서 분석
```

### Output
```json
{
  "sources": [
    "https://typescript-eslint.io/",
    "https://docs.nestjs.com/techniques/validation"
  ],
  "key_findings": {
    "installation": ["npm install @typescript-eslint/parser @typescript-eslint/eslint-plugin"],
    "configuration": [".eslintrc.js 설정 예제"],
    "best_practices": ["strict 모드 사용", "규칙 커스터마이징"],
    "common_issues": ["파스 오류", "규칙 충돌"]
  },
  "code_examples": [
    {
      "language": "typescript",
      "code": "module.exports = { extends: ['@typescript-eslint/recommended'] }",
      "source": "typescript-eslint.io",
      "description": "기본 ESLint 설정"
    }
  ]
}
```

## TRIGGER CONDITIONS

- "공식문서 분석" 선택 시
- "GitHub 예제 분석" 선택 시
- 웹 검색이 필요할 때
- 베스트 프랙티스 수집 시
- 코드 예제가 필요할 때