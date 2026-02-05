---
name: data-model-reviewer
description: Analyze and Refactor TypeScript data models. Detect duplication, improve type safety, and validate relationships in interfaces/types.
allowed-tools: Read, Grep, Glob
---

# Data Model Reviewer

TypeScript 타입 정의를 검토하여 SSOT, 타입 안전성, 데이터 관계의 품질을 확인합니다.

## 검사 원칙

1. **SSOT** - 데이터 정의 중복 제거
2. **Type Safety** - any 지양, Union/Enum 활용
3. **Relationship** - 데이터 간 관계 명확성

## Instructions

1. **대상 확인**: 사용자가 특정 파일/디렉토리를 지정한 경우 해당 대상에서 검토, 미지정 시 프로젝트 전체 탐색
2. **타입 파일 탐색**: `Glob`으로 `**/types/**/*.ts`, `**/*.d.ts` 등 타입 정의 파일 찾기
3. **타입 정의 분석**: `Read`로 파일 읽고 interface/type 정의 확인
4. **문제 패턴 검색**: `Grep`으로 `any`, 매직 스트링, 중복 정의 탐지
5. **체크리스트 기반 검토**: 아래 체크리스트 항목별로 검증
6. **결과 출력**: examples.md의 출력 형식에 따라 리뷰 결과 제시

## 체크리스트

### 타입 안전성

- [ ] `any` 타입 미사용
- [ ] 매직 스트링 대신 Literal Union/Enum 사용
- [ ] Optional(`?`) 필요한 곳에만 사용

### 구조 및 관계

- [ ] 중복 데이터 정의 없음 (SSOT)
- [ ] ID 필드 타입 일관성
- [ ] 중첩 깊이 3단계 이하

## 출력 형식

[examples.md](examples.md)의 "리뷰 출력 형식" 섹션을 따를 것
