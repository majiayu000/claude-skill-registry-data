---
name: factory-validator
description: '생성된 컴포넌트 검증 및 품질 보증 스킬'
license: MIT
triggers:
  - schema validation
  - quality assessment
  - syntax checking
  - auto-fix
  - quality scoring
  - component validation
---

# Factory Validator Skill

## ROLE

생성된 컴포넌트의 품질을 보증하고 스키마 준수 여부, 모범 사례 적용 여부를 검증합니다.

## GUIDELINES

### 1. 스키마 검증
- 필수 필드 확인 (name, description)
- 필드 형식 검증
- 타입별 필수 섹션 확인
- Anthropic 2025 스키마 호환성

### 2. 내용 품질 평가
- 명확성 점수 (1-5)
- 완전성 점수 (1-5)
- 사용성 점수 (1-5)
- 종합 품질 점수 (100점 만점)

### 3. 기술적 정확성
- 도구 사용 정확성
- 코드 예시 유효성
- 오류 처리 완성도
- 모범 사례 준수

### 4. 자동 수정 대상
- Frontmatter 형식
- 마크다운 구조
- 링크 검증
- 스키마 호환성

### 5. 품질 등급
- 90-100: Excellent (A) - 즉시 사용 가능
- 80-89: Good (B) - 사소한 개선 필요
- 70-79: Acceptable (C) - 일부 개선 필요
- 60-69: Needs Work (D) - 수정 필요
- <60: Poor (F) - 전면 수정 필요

## EXAMPLES

### Input
```
Component: newly-created-agent.md
Validation type: full
```

### Output
```markdown
## 🔍 컴포넌트 검증 보고서

| 항목 | 점수 | 상태 |
|------|------|------|
| 구조 | 28/30 | ✅ |
| 내용 | 35/40 | ⚠️ |
| 기술 | 25/30 | ✅ |

### 발견된 문제
#### ⚠️ 주요 (Major)
- ERROR HANDLING 섹션이 누락되었습니다
- 예제 코드가 너무 적습니다

#### 💡 개선 (Minor)
- 일부 설명이 모호합니다
- 더 많은 사용 예시가 필요합니다

### 자동 수정 제안
- ERROR HANDLING 섹션 템플릿 추가
- 기본 예제 코드 삽입
```

## TRIGGER CONDITIONS

- 컴포넌트 생성 완료 후
- 스키마 검증 필요 시
- 품질 점수 확인 필요 시
- 자동 수정 적용 시
- 플러그인 등록 전 검증 시