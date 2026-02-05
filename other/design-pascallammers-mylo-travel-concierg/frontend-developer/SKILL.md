---
name: frontend-developer
description: React/Vite 컴포넌트 빌드, 성능 최적화, Tailwind CSS 스타일링, shadcn/ui 컴포넌트 활용, 접근성 검토. 프론트엔드 기능 개발, UI 이슈 디버깅, 컴포넌트 코드 리뷰 시 사용.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Frontend Developer Skill

이 스킬은 Notion Clone 프로젝트의 React/Vite 프론트엔드 개발을 지원합니다.

## 주요 능력

### 1. React 컴포넌트 개발
- 함수형 컴포넌트 작성 및 최적화
- React Hooks 활용 (useState, useEffect, useContext, useCallback 등)
- 커스텀 훅 개발 및 로직 캡슐화
- 컴포넌트 재사용성 향상

### 2. 스타일링
- Tailwind CSS를 사용한 반응형 디자인
- 다크모드 지원
- 접근성 고려한 스타일

### 3. shadcn/ui 컴포넌트
- 버튼, 입력창, 모달, 드롭다운 등 UI 컴포넌트 활용
- 컴포넌트 커스터마이징 및 확장

### 4. 상태 관리
- React Context를 활용한 전역 상태 관리
- Zustand를 사용한 복잡한 상태 관리
- Custom Hooks로 도메인 로직 구현

### 5. 성능 최적화
- 번들 사이즈 최적화
- 렌더링 최적화 (useMemo, useCallback)
- 이미지 최적화 및 Cloudinary 활용

### 6. API 통신
- REST API 호출 및 에러 처리
- WebSocket(STOMP) 실시간 통신
- API 인터셉터 및 인증 처리

### 7. 접근성(A11y) 및 SEO
- 시맨틱 HTML 마크업
- ARIA 속성 활용
- 키보드 네비게이션 지원

### 8. 디버깅 및 테스트
- React DevTools 활용
- 콘솔 에러 및 경고 해결
- 컴포넌트 테스트 작성

## 프로젝트 구조

```
frontend/src/
├── App.jsx                 # 루트 컴포넌트
├── components/
│   ├── layout/            # 레이아웃 컴포넌트 (사이드바, 헤더 등)
│   ├── auth/              # 인증 관련 컴포넌트
│   ├── documents/         # 문서 관리 (페이지/테이블 뷰)
│   ├── editor/            # TipTap 리치 텍스트 에디터
│   ├── workspace/         # 워크스페이스 관리
│   ├── notifications/     # 알림 시스템
│   ├── error/             # 에러 바운더리
│   └── ui/                # shadcn/ui 컴포넌트
├── contexts/              # React Context (인증, 워크스페이스 등)
├── hooks/                 # 커스텀 훅 (API 호출, 상태 관리 등)
├── services/              # API 통신 서비스
└── lib/                   # 유틸리티 (색상, 로거, 에러 처리)
```

## 개발 가이드

### 1. 의존 관계 URL 앞에 @ 사용
```javascript
import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'
```

### 2. 컴포넌트 구조
```javascript
export function MyComponent({ prop1, prop2 }) {
  const [state, setState] = useState(null);

  return (
    <div className="...">
      {/* JSX */}
    </div>
  );
}
```

### 3. Provider 계층 구조
```
ErrorBoundary → AuthProvider → Router →
  NotificationProvider → WorkspaceProvider → DocumentProvider → MainLayout
```

### 4. 커스텀 훅 패턴
```javascript
export function useDocuments() {
  const { workspaceId } = useWorkspace();
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    // 로직
  }, [workspaceId]);

  return { documents, loading, error };
}
```

### 5. Context 패턴
```javascript
const MyContext = createContext();

export function MyProvider({ children }) {
  const [state, setState] = useState();

  return (
    <MyContext.Provider value={{ state, setState }}>
      {children}
    </MyContext.Provider>
  );
}

export function useMyContext() {
  return useContext(MyContext);
}
```

## 워크플로우

프론트엔드 개발 요청을 받으면:

1. **파일 구조 파악** - Glob으로 관련 파일 검색
2. **기존 코드 분석** - Read로 기존 컴포넌트/서비스 검토
3. **구현 계획** - 아키텍처 패턴 확인 후 개발 계획 수립
4. **코드 작성** - React 최적화 패턴 적용
5. **테스트** - 로컬 개발 서버로 동작 확인
6. **코드 리뷰** - 성능, 접근성, 일관성 검토

## 개발 명령어

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치
pnpm install

# 개발 서버 시작 (http://localhost:5173)
pnpm dev

# 빌드
pnpm build

# 린트 실행
pnpm lint

# 프로덕션 빌드 미리보기
pnpm preview
```

## 예시 작업

이 스킬이 자동으로 활성화되는 작업들:

- "반응형 네비게이션 컴포넌트 만들어줘"
- "이 컴포넌트의 성능을 최적화해줘"
- "CSS 레이아웃 이슈를 디버깅해줘"
- "shadcn/ui 모달 컴포넌트를 추가해줘"
- "WebSocket 실시간 업데이트 기능 구현해줘"
- "에러 핸들링 개선해줘"
- "접근성 이슈를 수정해줘"
