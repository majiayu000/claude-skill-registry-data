---
name: developing-reactflow-ui
description: React Flow 라이브러리를 사용한 노드 기반 UI 개발 지원. 노드/엣지 생성, 커스터마이징, 레이아웃, 상호작용 구현 시 사용. 항상 최신 문서를 WebFetch로 참조하여 정확한 정보 제공.
---

# React Flow Development Support

React Flow(@xyflow/react)를 사용한 노드 기반 인터페이스 개발을 지원합니다.

## 핵심 원칙

1. **항상 최신 문서 참조**: WebFetch 도구로 r.jina.ai를 통해 공식 문서 확인
2. **타입 안전성**: TypeScript 타입을 항상 명시
3. **베스트 프랙티스**: 성능 최적화 패턴 적용

## 문서 참조 방법

문서가 필요할 때 WebFetch 도구를 사용하여 다음 URL 형식으로 접근:

```
WebFetch(url: "https://r.jina.ai/https://reactflow.dev/{path}", prompt: "필요한 정보 요청")
```

### 기본 문서 URL
| 주제 | URL |
|------|-----|
| 학습 가이드 | `https://r.jina.ai/https://reactflow.dev/learn` |
| API 레퍼런스 | `https://r.jina.ai/https://reactflow.dev/api-reference` |
| 예제 | `https://r.jina.ai/https://reactflow.dev/examples` |
| UI 컴포넌트 | `https://r.jina.ai/https://reactflow.dev/ui` |

### 세부 문서 URL 패턴
- 특정 컴포넌트: `https://r.jina.ai/https://reactflow.dev/api-reference/components/{component-name}`
- 특정 훅: `https://r.jina.ai/https://reactflow.dev/api-reference/hooks/{hook-name}`
- 특정 예제: `https://r.jina.ai/https://reactflow.dev/examples/{category}/{example-name}`

## 주요 기능 영역

### 1. 노드 (Nodes)
- 기본 노드 타입: default, input, output
- 커스텀 노드 생성
- 노드 리사이징, 툴바, 드래그 핸들

### 2. 엣지 (Edges)
- 엣지 타입: bezier, smoothstep, step, straight
- 커스텀 엣지 생성
- 애니메이션 엣지, 마커

### 3. 상호작용 (Interaction)
- 연결/선택/드래그 이벤트
- 컨텍스트 메뉴
- 키보드 단축키

### 4. 레이아웃 (Layout)
- Dagre, Elkjs를 이용한 자동 레이아웃
- 계층적 레이아웃
- 수동 배치

### 5. 스타일링
- 다크 모드
- Tailwind CSS 통합
- CSS 변수 활용

## 사용 예시

### 문서 조회
```
사용자: useReactFlow 훅 사용법 알려줘
-> WebFetch로 https://r.jina.ai/https://reactflow.dev/api-reference/hooks/use-react-flow 조회
```

### 커스텀 노드 생성
```
사용자: 데이터베이스 테이블을 표현하는 노드 만들어줘
-> 최신 커스텀 노드 패턴 확인 후 코드 생성
```

## 참고 문서
- [문서 URL 목록](references/documentation-urls.md)
- [노드 패턴](references/node-patterns.md)
- [엣지 패턴](references/edge-patterns.md)
- [레이아웃 패턴](references/layout-patterns.md)
- [TypeScript 타입](references/typescript-types.md)
