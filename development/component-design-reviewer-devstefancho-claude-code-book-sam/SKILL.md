---
name: component-design-reviewer
description: Reviews React components and provides improvement suggestions. Use when you need code review, component review, structure improvement, refactoring, or component separation.
allowed-tools: Read, Grep, Glob
---

# Component Design Reviewer

React 컴포넌트 설계 원칙에 따른 전문적인 코드 리뷰를 제공하는 Skill입니다. Claude가 직접 코드를 분석하여 5가지 핵심 원칙을 중심으로 상세한 리포트를 생성합니다.

## 검사 원칙 요약

1. **SRP** - 하나의 컴포넌트, 하나의 역할
2. **Props** - drilling 최소화, 명확한 interface
3. **Composition** - 상속보다 합성
4. **Reusability** - 공통 요소 추출
5. **Custom Hooks** - UI/비즈니스 로직 분리

## Instructions

1. Read로 대상 컴포넌트 파일 읽기
2. 5가지 원칙별로 체크리스트 기반 분석
3. Grep으로 props drilling, hooks 패턴 검색
4. 컴포넌트별 리포트 생성 (Critical/Warning/Suggestion)
5. 문제마다 "문제 코드" vs "개선 코드" 예시 제공

## 리뷰 체크리스트

### 단일 책임 원칙 검사
- [ ] 컴포넌트가 하나의 역할만 수행하는가? (위반 신호: 이름에 "And" 포함)
- [ ] UI 렌더링과 비즈니스 로직이 분리되어 있는가? (위반 신호: 여러 API 호출)
- [ ] 컴포넌트 크기가 적절한가? (권장: 150줄 이하)
- [ ] 조건부 렌더링이 복잡하지 않은가? (권장: 3단계 이내)

### Props 설계 검사
- [ ] Props drilling이 3단계 이상인가?
- [ ] Props interface가 명확하게 정의되어 있는가?
- [ ] Default props가 적절히 활용되고 있는가?
- [ ] Props 개수가 적절한가? (권장: 7개 이하)

### 합성 패턴 검사
- [ ] 상속 대신 합성을 사용했는가?
- [ ] children props를 적절히 활용했는가?
- [ ] 컴포넌트 합성이 유연한가?
- [ ] Render props / Compound components가 필요한 상황인가?

### 재사용성 검사
- [ ] 공통 UI 요소가 추출되어 있는가?
- [ ] 범용 vs 특화 컴포넌트가 적절히 구분되어 있는가?
- [ ] 컴포넌트가 다른 곳에서 재사용 가능한가?
- [ ] 하드코딩된 값이 없는가?

### Custom Hooks 검사
- [ ] 비즈니스 로직이 custom hooks로 분리되어 있는가?
- [ ] useState/useEffect 로직이 컴포넌트 내에 과도하게 있지 않은가?
- [ ] 재사용 가능한 로직이 hooks로 추출되어 있는가?
- [ ] Hooks 명명이 use로 시작하고 명확한가?

## 출력 형식

[examples.md](examples.md)의 "리뷰 출력 형식" 섹션을 따를 것
