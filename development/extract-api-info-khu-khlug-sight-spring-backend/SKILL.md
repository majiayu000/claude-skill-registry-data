---
name: extract-api-info
description: Spring Boot 백엔드의 REST API 엔드포인트 정보를 추출합니다. API 명세, 엔드포인트 목록, API 문서, 프론트엔드 연동 정보가 필요할 때 사용하세요.
---

# REST API 정보 추출

이 Skill은 Spring Boot 백엔드 프로젝트에서 REST API 엔드포인트 정보를 자동으로 추출하여 프론트엔드 개발자에게 전달할 수 있는 형태로 정리합니다.

## Instructions

다음 단계를 따라 API 정보를 추출하세요:

### 1. Controller 파일 찾기
- `src/main/kotlin/com/sight/controllers/http/` 디렉토리에서 모든 `*Controller.kt` 파일을 찾습니다
- `InternalApiController`나 `TestController` 같은 내부용 API는 제외할 수 있습니다
- 찾은 컨트롤러 파일 중 주어진 프롬프트와 관련된 컨트롤러만 추출합니다

### 2. 각 Controller 분석
각 Controller 파일에서 다음 정보를 추출합니다:

- **HTTP 메서드**: `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`
- **경로**: 매핑 어노테이션의 값 (예: `@GetMapping("/users/@me")`)
- **권한**: `@Auth` 어노테이션의 UserRole 배열
- **요청 DTO**: `@RequestBody`, `@ModelAttribute`, `@PathVariable`, `@RequestParam`이 붙은 파라미터
- **응답 DTO**: 메서드의 반환 타입
- **상태 코드**: `@ResponseStatus` 어노테이션 또는 `ResponseEntity` 사용 여부

### 3. DTO 정보 수집
Request/Response DTO가 있는 경우:
- `src/main/kotlin/com/sight/controllers/http/dto/` 디렉토리에서 해당 DTO 파일을 찾습니다
- DTO의 필드 이름과 타입을 추출합니다

### 4. 출력 형식
다음과 같은 형식으로 API 정보를 정리합니다:

```markdown
# API 엔드포인트 목록

## [Controller 이름]

### [HTTP METHOD] [경로]
- **권한**: [필요한 권한 목록]
- **설명**: [엔드포인트 설명]
- **요청 파라미터**:
  - [파라미터명] ([타입]): [설명]
- **요청 본문** (있는 경우):
  ```typescript
  {
    필드명: 타입,
  }
  ```
- **응답**:
  ```typescript
  {
    필드명: 타입,
  }
  ```
- **상태 코드**: [HTTP 상태 코드]
- **파일 참조**: `[파일경로]:[라인번호]`
```

### 5. TypeScript 타입 변환
Kotlin 타입을 TypeScript 타입으로 변환:
- `String` → `string`
- `Int`, `Long` → `number`
- `Boolean` → `boolean`
- `LocalDateTime`, `Instant` → `string` (ISO 8601 형식)
- `List<T>` → `T[]`
- `Map<K, V>` → `Record<K, V>`
- nullable 타입 (`T?`) → `T | null`

## Examples

### 예시 1: 단순 GET 엔드포인트
```kotlin
@Auth([UserRole.USER, UserRole.MANAGER])
@GetMapping("/users/@me")
fun getCurrentUser(requester: Requester): GetCurrentUserResponse
```

**출력:**
```markdown
### GET /users/@me
- **권한**: USER, MANAGER
- **설명**: 현재 로그인한 사용자 정보 조회
- **응답**:
  ```typescript
  {
    id: string,
    name: string,
    manager: boolean,
    status: string,
    studentStatus: string,
    createdAt: string,
    updatedAt: string
  }
  ```
- **파일 참조**: `src/main/kotlin/com/sight/controllers/http/UserController.kt:28`
```

### 예시 2: POST 엔드포인트 (Request Body 포함)
```kotlin
@Auth([UserRole.MANAGER])
@PostMapping("/transactions")
@ResponseStatus(HttpStatus.CREATED)
fun createTransaction(
    @Valid @RequestBody request: CreateTransactionRequest,
    requester: Requester,
): CreateTransactionResponse
```

**출력:**
```markdown
### POST /transactions
- **권한**: MANAGER
- **설명**: 새 거래 내역 생성
- **요청 본문**:
  ```typescript
  {
    item: string,
    price: number,
    quantity: number,
    place: string | null,
    note: string | null,
    usedAt: string  // ISO 8601 datetime
  }
  ```
- **응답**:
  ```typescript
  {
    id: string,
    author: string,
    item: string,
    price: number,
    quantity: number,
    total: number,
    cumulative: number,
    place: string | null,
    note: string | null,
    usedAt: string,
    createdAt: string
  }
  ```
- **상태 코드**: 201 Created
- **파일 참조**: `src/main/kotlin/com/sight/controllers/http/TransactionController.kt:72`
```

### 예시 3: Query Parameters 포함
```kotlin
@Auth([UserRole.USER, UserRole.MANAGER])
@GetMapping("/transactions")
fun getTransactions(
    @RequestParam year: Int,
    @RequestParam(defaultValue = "0") @Min(0) offset: Int,
    @RequestParam(defaultValue = "20") @Min(1) @Max(50) limit: Int,
): ListTransactionsResponse
```

**출력:**
```markdown
### GET /transactions
- **권한**: USER, MANAGER
- **설명**: 거래 내역 목록 조회
- **요청 파라미터**:
  - year (number): 조회할 연도 (필수)
  - offset (number): 페이지 오프셋 (기본값: 0)
  - limit (number): 페이지 크기 (기본값: 20)
- **응답**:
  ```typescript
  {
    count: number,
    transactions: Array<{
      id: string,
      author: string,
      item: string,
      price: number,
      quantity: number,
      total: number,
      cumulative: number,
      place: string | null,
      note: string | null,
      usedAt: string,
      createdAt: string,
      updatedAt: string
    }>
  }
  ```
- **파일 참조**: `src/main/kotlin/com/sight/controllers/http/TransactionController.kt:32`
```

## Tips

1. **그룹화**: Controller별로 엔드포인트를 그룹화하여 가독성을 높입니다
2. **정렬**: 각 그룹 내에서 경로 알파벳 순으로 정렬합니다
3. **상세 수준**: 사용자가 "간단하게" 또는 "상세하게"를 요청하면 DTO 필드 포함 여부를 조정합니다
4. **필터링**: 특정 Controller나 경로 패턴만 추출하고 싶다면 사용자에게 확인합니다
5. **OpenAPI**: 가능하다면 OpenAPI/Swagger 형식으로도 출력할 수 있습니다
