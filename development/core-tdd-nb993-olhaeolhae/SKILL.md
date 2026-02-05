---
name: core-tdd
description: 코어 계층(Domain, UseCase, Service, Command/Query) TDD 개발 지침. Red-Green-Refactor 사이클을 통해 테스트 주도 개발을 수행합니다. 테스트를 먼저 작성하고, 테스트가 통과하는 최소한의 코드를 구현합니다.
---

# 코어 계층 TDD 지침

## TDD 순서

1. **Command/Query** - 테스트 → 구현 → 리팩토링
2. **Domain** - 테스트 → 구현 → 리팩토링
3. **UseCase** - 인터페이스 정의 (테스트 불필요)
4. **Service** - 테스트 → 구현 → 리팩토링

## Red-Green-Refactor 사이클

### Red (테스트 작성)
1. 실패하는 테스트 먼저 작성
2. 컴파일 에러 해결을 위한 최소 stub만 생성
3. 테스트 실행하여 의도한 실패 확인

### Green (구현)
1. 테스트를 통과시키는 최소한의 코드 작성
2. 명명 규칙 준수 (Find/Save/Modify/Delete)
3. 정적 팩토리 메서드 패턴 (newXxx/withId)

### Refactor (개선)
1. 테스트 통과 상태 유지
2. 중복 제거, 가독성 개선
3. 아키텍처/코딩 규칙 준수

## 핵심 규칙

### 필수 명명 규칙
| 동작 | 접두사 | 금지 |
|------|--------|------|
| 조회 | **Find** | Get, Query, Retrieve |
| 등록 | **Save** | Create, Add, Insert |
| 수정 | **Modify** | Update, Edit, Change |
| 삭제 | **Delete** | Remove, Erase |

### 정적 팩토리 메서드
- 신규 생성: `newXxx()` (예: `Family.newFamily(...)`)
- 복원: `withId()` (예: `Family.withId(...)`)
- 금지: `of()`, `create()`, `from()`

### 테스트 패턴
- 클래스: `@ExtendWith(MockitoExtension.class)`
- Service: `@InjectMocks` + `@Mock`
- 메서드명: snake_case (`{행동}_{결과}_{조건}`)

## 상세 지침

**[필수] 아래 참조 문서를 모두 읽은 후 작업을 시작하세요:**

- **TDD 사이클**: [tdd-cycle.md](tdd-cycle.md)
- **명명 규칙**: [naming.md](naming.md)
- **아키텍처**: [architecture.md](architecture.md)
- **코딩 스타일**: [coding.md](coding.md)
