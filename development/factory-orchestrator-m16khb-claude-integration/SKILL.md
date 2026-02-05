---
name: factory-orchestrator
description: '오케스트레이터 에이전트 생성 및 전문가 조합 전문 스킬'
license: MIT
triggers:
  - orchestrator creation
  - expert composition
  - multi-agent coordination
  - task delegation
  - agent routing
---

# Factory Orchestrator Skill

## ROLE

복잡한 다영역 작업을 위해 여러 전문가 에이전트를 조합하는 오케스트레이터를 생성합니다.

## GUIDELINES

### 1. 구성 전략
- 단독 에이전트: 독립적 전문가
- 오케스트레이터: 여러 전문가 조합
- 전문가 확장: 기존 에이전트 기반 확장
- 하이브리드: 직접 작업 + 위임 혼합

### 2. 오케스트레이션 패턴
- SINGLE_EXPERT: 하나의 전문가가 전체 처리
- SEQUENTIAL_CHAIN: 의존성 있는 순차적 처리
- PARALLEL_EXECUTION: 독립적 병렬 처리
- HIERARCHICAL_DELEGATION: 다계층 위임
- DYNAMIC_ROUTING: 동적 라우팅

### 3. 전문가 분류
- Backend Development: DB, API, Messaging, Frameworks
- Frontend Development: Frameworks, State, Styling
- DevOps & Infrastructure: Cloud, Containers, CI/CD
- Quality & Testing: Unit, Integration, Review
- Documentation: API Docs, Guides, Writing

### 4. 라우팅 로직
- 키워드 기반 매칭
- 컨텍스트 기반 분석
- 워크플로우 기반 실행
- 복합 라우팅

### 5. 오케스트레이션 구조
```yaml
SPECIALIZED EXPERTS:
- 전문가 목록과 역할

ORCHESTRATION LOGIC:
- 요청 분석
- 전문가 선택
- 작업 위임

DELEGATION EXAMPLES:
- Task tool 호출 패턴
- 컨텍스트 전달 방식
```

## EXAMPLES

### Input
```
Agent name: fullstack-reviewer
Composition: 오케스트레이터
Selected experts: code-reviewer, testing-expert
Pattern: sequential
```

### Output
```markdown
## 전문가 에이전트

| 전문가 | 전문 분야 | 트리거 키워드 | 경로 |
|--------|----------|--------------|------|
| code-reviewer | 코드 리뷰 | 리뷰, 검토 | backend |
| testing-expert | 테스트 | 테스트, 검증 | backend |

## 오케스트레이션 로직

1. 코드 리뷰 실행
2. 리뷰 결과 기반 테스트 케이스 생성
3. 최종 보고서 통합
```

## TRIGGER CONDITIONS

- agent 생성 시 조합 옵션 선택
- 여러 전문가 필요한 작업
- 복잡한 워크플로우 필요 시
- 기존 전문가 확장 시
- 하이브리드 아키텍처 필요 시