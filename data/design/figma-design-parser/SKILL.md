---
name: figma-design-parser
description: Parse Figma design files into structured screen hierarchies. Use when working with Figma API, extracting text/labels from design nodes, traversing node trees, detecting cover frames, or parsing screen IDs (AUTO_0001, PSET_0002, etc.).
---

# Figma Design Parser

Figma 디자인 파일을 구조화된 스크린 계층으로 파싱하는 전문 스킬입니다.

## Quick Reference

### 스크린 ID 규칙
- 형식: `{PREFIX}_{4자리숫자}[_suffix]`
- 예: `AUTO_0001`, `PSET_0002_1`, `LINK_0003_ㅅ`
- 접두사: AUTO, PSET, LINK, MENU 등

### 핵심 노드 타입
```
FRAME → 스크린 컨테이너
TEXT → 텍스트 콘텐츠
GROUP → 그룹화된 요소
COMPONENT → 재사용 컴포넌트
INSTANCE → 컴포넌트 인스턴스
```

## Contents

- [reference.md](reference.md) - Figma API 노드 순회 및 최적화 가이드
- [guide.md](guide.md) - 텍스트 추출 및 라벨-값 파싱 패턴
- [scripts/extract_figma_data.py](scripts/extract_figma_data.py) - 결정론적 Figma 데이터 추출
- [scripts/parse_screen_id.py](scripts/parse_screen_id.py) - 스크린 ID 파싱 유틸리티

## When to Use

- Figma 파일에서 스크린 데이터 추출 시
- 노드 트리 재귀 순회 로직 작성 시
- Cover 프레임 감지 및 썸네일 데이터 추출 시
- 텍스트 노드에서 라벨-값 쌍 추출 시
