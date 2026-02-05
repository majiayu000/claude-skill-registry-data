---
name: generate-mockup
description: Generate UI mockups using Magic MCP (21st.dev). Use when (1) creating new UI components, (2) prototyping interfaces, (3) building design system components.
tools: [mcp_magic, Write]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: generate-mockup 호출 - UI 목업 생성` 시스템 메시지를 첫 줄에 출력하세요.

# generate-mockup Skill

> Magic MCP (21st.dev)를 활용한 UI 목업 생성

## 역할

디자이너의 요구사항을 분석하여 현대적인 UI 컴포넌트 목업을 생성합니다.

## 트리거

- `/SEMO:mockup` 명령어
- "목업", "mockup", "UI 만들어" 키워드

## Process

### Step 1: 요구사항 분석

컴포넌트 유형, 필요 요소, 스타일 요구사항 분석

### Step 2: Magic MCP 호출

21st_magic_component_builder 함수 호출

### Step 3: 결과 제공

생성된 컴포넌트 코드와 사용 방법 제공

## Magic MCP Functions

| Function | 용도 |
|----------|------|
| 21st_magic_component_builder | 새 컴포넌트 생성 |
| 21st_magic_component_inspiration | 참고 검색 |
| 21st_magic_component_refiner | 기존 개선 |

## References

- [Component Types](references/component-types.md)
- [Design Principles](references/design-principles.md)
