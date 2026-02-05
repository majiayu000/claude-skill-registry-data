---
name: portal-dropdown-components
description: Build React Portal-based dropdown, modal, and overlay components. Use when creating dropdown menus, select components, modals, tooltips, or any UI that needs to escape overflow containers. Includes positioning, scroll handling, keyboard navigation, and accessibility patterns.
---

# Portal Dropdown Components

React Portal 기반 드롭다운, 모달, 오버레이 컴포넌트 개발 스킬입니다.

## Quick Reference

### Portal 기본 패턴
```tsx
import { createPortal } from 'react-dom';

function Dropdown({ isOpen, position, children }) {
  if (!isOpen) return null;

  return createPortal(
    <div style={{ position: 'fixed', ...position }}>
      {children}
    </div>,
    document.body
  );
}
```

### 핵심 기능
- ✅ `position: fixed` + 화면 좌표 계산
- ✅ 외부 클릭 감지 (Click Outside)
- ✅ ESC 키 닫기
- ✅ 스크롤 시 위치 업데이트
- ✅ 포커스 트랩 (모달)

## Contents

- [reference.md](reference.md) - Portal 아키텍처 및 포지셔닝 가이드
- [guide.md](guide.md) - 접근성 및 키보드 네비게이션 패턴
- [scripts/generate_dropdown.sh](scripts/generate_dropdown.sh) - 드롭다운 컴포넌트 템플릿 생성

## When to Use

- 드롭다운 메뉴가 `overflow: hidden` 컨테이너에 잘리는 경우
- z-index 스태킹 컨텍스트 문제 해결 시
- 스크롤 가능한 컨테이너 내 드롭다운 구현 시
- 접근성 요구사항을 충족하는 UI 컴포넌트 개발 시
