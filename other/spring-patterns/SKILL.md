---
name: spring-patterns
description: "Spring Boot 핵심 설계 규칙 — 계층 구조, @Transactional 규칙, DTO vs Entity 분리, 예외 처리, 의존성 주입, API 설계. Use when Spring Boot 에 새 API 엔드포인트를 추가하거나 계층·트랜잭션 경계를 정할 때."
---

# Spring Boot Core Patterns

Spring Boot 프로젝트에서 반복되는 설계 결정 가이드. "이 상황에서는 이렇게 한다".

## Quick Reference — 계층 구조 결정

```
어디에 로직을 넣을까?
    │
    ├─ HTTP 파싱, 입력 검증, 응답 변환 ──> Controller
    │
    ├─ 비즈니스 로직, 트랜잭션, 조율 ────> Service
    │
    ├─ DB 접근, 쿼리 ─────────────────> Repository
    │
    └─ 순수 도메인 로직 (상태 변경, 규칙) ──> Domain Entity

Controller가 Service를 건너뛰고 Repository 호출? → 금지
Service가 HttpServletRequest 참조? → 금지 (Controller 책임)
Entity에 비즈니스 로직? → 상태 변경/규칙 검증만 허용
```

---

## CRITICAL: @Transactional 규칙

### 핵심 원칙

| 규칙 | 이유 |
|------|------|
| Service 레이어에만 선언 | Controller/Repository에 선언 시 계층 침범 |
| 클래스: `@Transactional(readOnly=true)` | 기본 읽기 전용으로 안전하게 시작 |
| 쓰기 메서드: `@Transactional` 오버라이드 | 명시적으로 쓰기 트랜잭션 열기 |
| private 메서드에 절대 금지 | AOP 프록시가 private 호출을 가로채지 못함 |
| 같은 클래스 내 호출 금지 | self-invocation은 프록시를 우회 |
| `readOnly=true` 효과 | DB 레플리카 라우팅 + Hibernate dirty checking 비활성화 |

### Bad: 흔한 실수

```java
@Service
public class OrderService {
    // BAD: private 메서드에 @Transactional — 작동 안 함
    @Transactional
    private void updateStock(Long productId, int qty) {
        // 프록시가 가로채지 못해 트랜잭션 무시됨
    }

    // BAD: 같은 클래스 내 호출 — self-invocation
    public void processOrder(Order order) {
        saveOrder(order);  // 프록시 우회 → 트랜잭션 미적용
    }

    @Transactional
    public void saveOrder(Order order) {
        orderRepository.save(order);
    }
}
```

### Good: 올바른 패턴

```java
@Service
@Transactional(readOnly = true)  // 클래스 기본: 읽기 전용
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final StockService stockService;  // self-invocation 방지: 별도 서비스

    public Order findById(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Order", id));
    }

    @Transactional  // 쓰기: readOnly 오버라이드
    public Order createOrder(CreateOrderCommand cmd) {
        stockService.decreaseStock(cmd.productId(), cmd.quantity());
        return orderRepository.save(Order.create(cmd));
    }
}

@Service
@RequiredArgsConstructor
public class StockService {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void decreaseStock(Long productId, int qty) {
        // 독립 트랜잭션: 메인 롤백과 무관하게 커밋
    }
}
```

---

## CRITICAL: DTO vs Entity 분리

### 원칙

- Controller는 Entity 절대 노출 금지
- 흐름: `Request DTO → Service → Response DTO`
- 이유: API 스펙 ≠ DB 스키마, LazyInitializationException 방지, 보안

### Bad: Entity 직접 노출

```java
// BAD: Entity 그대로 반환 — 보안 위험 + API-DB 결합
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userService.findById(id);  // password 등 민감 정보 노출
}
```

### Good: Record DTO 패턴 (Java 16+)

```java
// Request DTO
public record CreateOrderRequest(
    @NotNull Long productId,
    @Positive int quantity,
    @NotBlank String shippingAddress
) {}

// Response DTO — static factory로 Entity → DTO 변환
public record OrderResponse(
    Long id, String productName, int quantity,
    BigDecimal totalPrice, String status, LocalDateTime createdAt
) {
    public static OrderResponse from(Order order) {
        return new OrderResponse(
            order.getId(), order.getProduct().getName(),
            order.getQuantity(), order.getTotalPrice(),
            order.getStatus().name(), order.getCreatedAt()
        );
    }
}

// Controller
@GetMapping("/orders/{id}")
public ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
    Order order = orderService.findById(id);
    return ResponseEntity.ok(OrderResponse.from(order));
}
```

---

## 예외 처리 전략

### 도메인 예외 계층

```java
// 기본 비즈니스 예외
public abstract class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;
    protected BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
    public ErrorCode getErrorCode() { return errorCode; }
}

// 구체 예외 — HTTP 상태 코드와 1:1 매핑
public class NotFoundException extends BusinessException {    // 404
    public NotFoundException(String resource, Object id) {
        super(ErrorCode.NOT_FOUND);
    }
}
public class ConflictException extends BusinessException {    // 409
    public ConflictException(String message) { super(ErrorCode.CONFLICT); }
}
public class ForbiddenException extends BusinessException {   // 403
    public ForbiddenException() { super(ErrorCode.FORBIDDEN); }
}
```

### 에러 응답 표준화

```java
public record ErrorResponse(String code, String message, LocalDateTime timestamp) {
    public static ErrorResponse of(ErrorCode errorCode) {
        return new ErrorResponse(errorCode.getCode(), errorCode.getMessage(), LocalDateTime.now());
    }
}
```

### @RestControllerAdvice 글로벌 핸들러

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(NotFoundException e) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse.of(e.getErrorCode()));
    }

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusiness(BusinessException e) {
        log.warn("Business error: {}", e.getMessage());
        return ResponseEntity.badRequest().body(ErrorResponse.of(e.getErrorCode()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
            .map(f -> f.getField() + ": " + f.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("VALIDATION_ERROR", msg, LocalDateTime.now()));
    }

    // 프로덕션: 스택트레이스 절대 노출 금지
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(Exception e) {
        log.error("Unexpected error", e);
        return ResponseEntity.internalServerError()
            .body(new ErrorResponse("INTERNAL_ERROR", "서버 오류", LocalDateTime.now()));
    }
}
```

**IMPORTANT**: Controller에서 try-catch 금지. 모든 예외는 글로벌 핸들러가 처리.

---

## 의존성 주입 규칙

### 생성자 주입만 사용

```java
// GOOD: 생성자 주입 (Lombok)
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;  // 불변, 컴파일 타임 검증
    private final PaymentService paymentService;
    private final EventPublisher eventPublisher;
}

// BAD: 필드 주입 — 테스트 어렵고, 불변성 미보장
@Service
public class OrderService {
    @Autowired private OrderRepository orderRepository;  // 금지
}
```

### 순환 참조 해결

```
순환 참조 발생 시
    │
    ├─ ServiceA ↔ ServiceB 직접 참조
    │   └─ 해결: 이벤트 기반 분리 (ApplicationEventPublisher)
    │
    ├─ 공통 로직 존재
    │   └─ 해결: 공통 서비스 추출
    │
    └─ 인터페이스로 의존성 역전 (DIP)
        └─ ServiceA → InterfaceB ← ServiceB
```

**IMPORTANT**: `@Lazy`로 순환 참조 해결은 근본 원인 회피. 설계를 고쳐야 함.

---

## API 설계 패턴

### RESTful 규칙

| HTTP 메서드 | URI 패턴 | 용도 |
|-------------|----------|------|
| POST | `/api/v1/orders` | 주문 생성 |
| GET | `/api/v1/orders/{id}` | 주문 단건 조회 |
| GET | `/api/v1/orders` | 주문 목록 (+ 페이징) |
| PUT | `/api/v1/orders/{id}` | 전체 수정 |
| PATCH | `/api/v1/orders/{id}` | 부분 수정 |
| DELETE | `/api/v1/orders/{id}` | 삭제 |

### 페이징 + 검증 예시

```java
@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
public class OrderController {
    private final OrderService orderService;

    @PostMapping
    public ResponseEntity<OrderResponse> create(
            @Valid @RequestBody CreateOrderRequest request) {
        Order order = orderService.createOrder(request);
        return ResponseEntity
            .created(URI.create("/api/v1/orders/" + order.getId()))
            .body(OrderResponse.from(order));
    }

    @GetMapping
    public ResponseEntity<PageResponse<OrderResponse>> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        Page<OrderResponse> result = orderService.findAll(pageable).map(OrderResponse::from);
        return ResponseEntity.ok(PageResponse.from(result));
    }
}
```

### 버전 관리

| 전략 | 예시 | 적합성 |
|------|------|--------|
| URI 방식 | `/api/v1/orders` | 단순 명확, 대부분 추천 |
| Header 방식 | `Accept: application/vnd.myapp.v1+json` | 깔끔하지만 테스트 불편 |
| Query 방식 | `/api/orders?version=1` | 비추천 (캐싱 문제) |

---

## 설정 관리

### @ConfigurationProperties (추천)

```java
// @Value 대신 타입 세이프한 설정 바인딩
@ConfigurationProperties(prefix = "app.payment")
public record PaymentProperties(
    @NotBlank String apiKey,
    @NotNull Duration timeout,
    @Positive int maxRetries,
    String callbackUrl
) {}

@SpringBootApplication
@ConfigurationPropertiesScan  // Record 기반 설정 활성화
public class Application { }
```

```yaml
# application.yml — 공통
app:
  payment:
    timeout: 5s
    max-retries: 3

# application-prod.yml — 프로덕션
app:
  payment:
    api-key: ${PAYMENT_API_KEY}  # 시크릿은 환경변수
    callback-url: https://api.prod.example.com/callback
```

### 환경별 프로필

| 프로필 | 용도 | 데이터소스 |
|--------|------|-----------|
| `local` | 로컬 개발 | H2 / Docker Compose |
| `dev` | 개발 서버 | 개발 DB |
| `staging` | 스테이징 | 프로덕션 유사 |
| `prod` | 프로덕션 | RDS / CloudSQL |

**IMPORTANT**: 시크릿(API 키, DB 비밀번호)은 yml에 평문 금지. 환경변수 또는 Vault 사용.

---

## 테스트 패턴

### 테스트 종류 선택

```
무엇을 테스트할까?
    │
    ├─ Controller (HTTP) ──────> @WebMvcTest + MockMvc + @MockBean
    │
    ├─ Service (비즈니스) ─────> 순수 단위 테스트 (Mockito)
    │
    ├─ Repository (쿼리) ──────> @DataJpaTest + TestEntityManager
    │
    └─ 전체 통합 (E2E) ────────> @SpringBootTest + TestRestTemplate
```

### 슬라이스 테스트 예시

```java
// Controller 슬라이스
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @Autowired MockMvc mockMvc;
    @MockBean OrderService orderService;

    @Test
    void 주문_생성_성공() throws Exception {
        given(orderService.createOrder(any())).willReturn(testOrder());

        mockMvc.perform(post("/api/v1/orders")
                .contentType(APPLICATION_JSON)
                .content("""
                    {"productId": 1, "quantity": 2, "shippingAddress": "서울시"}
                    """))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1L));
    }
}

// Repository 슬라이스
@DataJpaTest
class OrderRepositoryTest {
    @Autowired OrderRepository orderRepository;
    @Autowired TestEntityManager em;

    @Test
    void 사용자별_주문_조회() {
        em.persist(testOrder());
        em.flush(); em.clear();
        assertThat(orderRepository.findByUserId(1L)).hasSize(1);
    }
}
```

### @MockBean vs @SpyBean

| 어노테이션 | 용도 | 동작 |
|-----------|------|------|
| `@MockBean` | 완전 대체 | 모든 메서드 stub 필요, 기본 null/0 반환 |
| `@SpyBean` | 부분 대체 | 실제 동작 유지 + 특정 메서드만 오버라이드 |

```java
@SpyBean PaymentService paymentService;

@Test
void 결제_실패_시_롤백() {
    doThrow(new PaymentException("timeout")).when(paymentService).process(any());
    // 나머지 메서드는 실제 동작 유지
}
```

---

## Anti-Patterns 표

| 실수 | 문제 | 해결 |
|------|------|------|
| Entity 직접 반환 | API-DB 결합, 보안 위험 | DTO 분리 + `from()` factory |
| @Transactional on private | 프록시 미작동 | public 메서드로 변경 |
| 필드 @Autowired | 테스트 어려움, 불변성 없음 | 생성자 주입 + final |
| Controller에서 try-catch | 예외 처리 분산 | @RestControllerAdvice |
| @Value 남용 | 타입 안전하지 않음 | @ConfigurationProperties |
| God Service (500줄+) | 단일 책임 위반 | 도메인별 서비스 분리 |
| 비즈니스 로직 in Controller | 계층 혼재 | Service로 이동 |
| yml에 시크릿 평문 | 보안 위험 | 환경변수 / Vault |
| @SpringBootTest 남용 | 느린 테스트 | 슬라이스 테스트 활용 |
| 순환 참조 @Lazy 해결 | 근본 원인 미해결 | 이벤트/인터페이스 분리 |
| Repository에서 비즈니스 로직 | 계층 침범 | Service로 이동 |
| N+1 무시 | 성능 저하 | @EntityGraph / Fetch Join |

---

## Checklist: 새 API 엔드포인트 추가 시

```
□ Request/Response DTO 생성 (Record)
□ Bean Validation 어노테이션 (@NotNull, @Valid)
□ Service에 @Transactional 적절히 설정
□ 도메인 예외 정의 + GlobalExceptionHandler 매핑
□ Controller → Service → Repository 계층 준수
□ 단위 테스트 + @WebMvcTest 작성
□ API 버전 경로 확인 (/api/v1/...)
```

---

## 관련 스킬

| 스킬 | 용도 |
|------|------|
| `/java:spring-data` | JPA + QueryDSL 데이터 액세스 패턴 |
| `/java:spring-security` | 인증/인가, JWT, OAuth2 |
| `/java:spring-testing` | 테스트 전략 심화 (Testcontainers 등) |
| `/java:spring-cache` | Redis 캐싱 패턴 |
| `/java:spring-jooq` | jOOQ SQL 중심 개발 |
| `/java:effective-java` | Java 코드 품질 패턴 |
| `/java:refactoring-spring` | Spring 리팩토링 패턴 |
