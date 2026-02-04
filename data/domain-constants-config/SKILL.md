---
name: domain-constants-config
description: Manage centralized domain constants and configuration in the project. Use when adding new status types, modifying UI labels, updating color schemes, or creating configuration objects for domain entities.
---

# Domain Constants Config

프로젝트의 도메인 상수 및 설정을 중앙 관리하는 스킬입니다.

## Quick Reference

### 상수 위치
```
app/screen/[prefix]/config/constants.ts  ← 메인 상수 파일
```

### 상태 설정 구조
```typescript
const STATUS_CONFIG = {
  'Reviewing': {
    label: '검토중',
    color: 'text-yellow-700',
    bgColor: 'bg-yellow-100'
  }
  // ...
};
```

## Contents

- [reference.md](reference.md) - 도메인 상수 전체 목록 및 가이드
- [guide.md](guide.md) - 새 상수 추가 및 수정 패턴

## When to Use

- 새 상태(Status) 또는 진행 단계(Progress) 추가 시
- UI 라벨 또는 색상 수정 시
- 스크린 접두사(Prefix) 추가 시
- 설정 객체가 여러 파일에 분산되어 있을 때 통합 시
