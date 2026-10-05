---
name: java-expert
description: Deep Java expertise for enterprise application development. Use when writing Java code, implementing concurrency patterns, designing with streams and.
---

# Java Expert

Specialized expertise in Java programming, providing deep guidance on modern language features, streams and functional programming, generics, concurrency with virtual threads, Spring Boot patterns, resilience strategies, and testing with JUnit 5.

## When to Use This Skill

Use this skill for:

- Writing modern Java (17+) with records, sealed classes, and pattern matching
- Designing stream pipelines and functional transformations
- Implementing type-safe generic APIs
- Building concurrent applications with virtual threads and CompletableFuture
- Developing Spring Boot microservices
- Designing resilient error handling and retry strategies
- Writing comprehensive JUnit 5 test suites

**Trigger phrases**: "java", "spring boot", "jvm", "java concurrency", "java streams", "java generics", "junit", "java records", "virtual threads"

## What This Skill Does

Provides Java expertise including:

- **Modern Java**: Records, sealed classes, pattern matching, text blocks, virtual threads
- **Streams**: Stream API, collectors, Optional, parallel streams
- **Generics**: Bounded types, wildcards, type erasure workarounds
- **Concurrency**: CompletableFuture, virtual threads, structured concurrency, locks
- **Spring Boot**: DI, REST controllers, security, configuration, profiles
- **Resilience**: Custom exceptions, circuit breakers, retry patterns
- **Testing**: JUnit 5, Mockito, AssertJ, TestContainers, MockMvc

## Instructions

### Step 1: Leverage Modern Java Features

**Records for Immutable Data**:

```java
// Records eliminate boilerplate for data carriers (Java 16+)
public record User(String name, String email, LocalDate joinDate) {

    // Compact constructor for validation
    public User {
        Objects.requireNonNull(name, "name must not be null");
        Objects.requireNonNull(email, "email must not be null");
        if (!email.contains("@")) {
            throw new IllegalArgumentException("invalid email: " + email);
        }
    }

    // Custom accessor
    public String displayName() {
        return name + " <" + email + ">";
    }
}

// Records work naturally with collections and streams
List<User> users = List.of(
    new User("Alice", "alice@example.com", LocalDate.of(2024, 1, 15)),
    new User("Bob", "bob@example.com", LocalDate.of(2024, 3, 22))
);

// Destructure in local variable declarations
var user = new User("Alice", "alice@example.com", LocalDate.now());
String name = user.name();   // accessor, not getName()
String email = user.email();
```

**Sealed Classes and Pattern Matching**:

```java
// Sealed classes restrict which classes can extend them (Java 17+)
public sealed interface Shape permits Circle, Rectangle, Triangle {
    double area();
}

public record Circle(double radius) implements Shape {
    public double area() { return Math.PI * radius * radius; }
}

public record Rectangle(double width, double height) implements Shape {
    public double area() { return width * height; }
}

public record Triangle(double base, double height) implements Shape {
    public double area() { return 0.5 * base * height; }
}

// Pattern matching for instanceof (Java 16+)
public static String describe(Object obj) {
    if (obj instanceof String s && s.length() > 5) {
        return "long string: " + s;
    } else if (obj instanceof Integer i && i > 0) {
        return "positive int: " + i;
    }
    return "unknown: " + obj;
}

// Pattern matching for switch (Java 21+)
public static String formatShape(Shape shape) {
    return switch (shape) {
        case Circle c when c.radius() > 100 -> "large circle, r=" + c.radius();
        case Circle c    -> "circle, r=" + c.radius();
        case Rectangle r -> "rectangle, %sx%s".formatted(r.width(), r.height());
        case Triangle t  -> "triangle, base=" + t.base();
    };
}
```

**Text Blocks and Virtual Threads**:

```java
// Text blocks for multi-line strings (Java 15+)
String json = """
        {
            "name": "%s",
            "email": "%s",
            "active": true
        }
        """.formatted(user.name(), user.email());

String sql = """
        SELECT u.id, u.name, u.email
        FROM users u
        JOIN orders o ON o.user_id = u.id
        WHERE o.status = 'ACTIVE'
        ORDER BY u.name
        """;

// Virtual threads (Java 21+, Project Loom)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = urls.stream()
        .map(url -> executor.submit(() -> fetchUrl(url)))
        .toList();

    List<String> results = new ArrayList<>();
    for (var future : futures) {
        results.add(future.get());
    }
}

// var for local type inference (Java 10+)
var users = new ArrayList<User>();           // ArrayList<User>
var counts = Map.of("a", 1, "b", 2);        // Map<String, Integer>
var stream = users.stream().filter(u -> u.name().startsWith("A")); // Stream<User>
```

### Step 2: Master Streams and Functional Programming

**Stream API Fundamentals**:

```java
// Transforming and filtering
List<String> activeEmails = users.stream()
    .filter(u -> u.joinDate().isAfter(LocalDate.of(2024, 1, 1)))
    .map(User::email)
    .sorted()
    .toList();   // Java 16+; use .collect(Collectors.toList()) for older versions

// FlatMap for nested structures
record Order(String id, List<LineItem> items) {}
record LineItem(String product, int quantity, BigDecimal price) {}

List<LineItem> allItems = orders.stream()
    .flatMap(order -> order.items().stream())
    .filter(item -> item.quantity() > 0)
    .toList();

// Reduce for aggregation
BigDecimal total = allItems.stream()
    .map(item -> item.price().multiply(BigDecimal.valueOf(item.quantity())))
    .reduce(BigDecimal.ZERO, BigDecimal::add);

// Grouping and partitioning with Collectors
Map<String, List<LineItem>> byProduct = allItems.stream()
    .collect(Collectors.groupingBy(LineItem::product));

Map<Boolean, List<LineItem>> partitioned = allItems.stream()
    .collect(Collectors.partitioningBy(item -> item.quantity() > 10));

// Downstream collectors
Map<String, Long> countByProduct = allItems.stream()
    .collect(Collectors.groupingBy(LineItem::product, Collectors.counting()));

Map<String, BigDecimal> revenueByProduct = allItems.stream()
    .collect(Collectors.groupingBy(
        LineItem::product,
        Collectors.reducing(
            BigDecimal.ZERO,
            item -> item.price().multiply(BigDecimal.valueOf(item.quantity())),
            BigDecimal::add
        )
    ));
```

**Optional and Method References**:

```java
// Optional as return type (never as field or parameter)
public Optional<User> findByEmail(String email) {
    return users.stream()
        .filter(u -> u.email().equalsIgnoreCase(email))
        .findFirst();
}

// Chaining Optional operations
String displayName = findByEmail("alice@example.com")
    .map(User::displayName)
    .orElse("Unknown User");

// Optional with flatMap for nested optionals
Optional<String> city = findByEmail("alice@example.com")
    .flatMap(this::findAddress)
    .map(Address::city);

// orElseThrow for mandatory values
User user = findByEmail(email)
    .orElseThrow(() -> new UserNotFoundException("no user with email: " + email));

// Method references in four forms
users.stream().map(User::name);                    // instance method via type
users.stream().forEach(System.out::println);       // instance method via object
users.stream().map(String::valueOf);               // static method
users.stream().map(UserDto::new);                  // constructor reference
```

**Custom Collectors and Parallel Streams**:

```java
// Custom collector: join strings with prefix, delimiter, suffix
Collector<CharSequence, ?, String> csvCollector =
    Collectors.joining(", ", "[", "]");

String csv = users.stream()
    .map(User::name)
    .collect(csvCollector);  // "[Alice, Bob, Charlie]"

// Custom collector: collecting to an immutable map
Collector<User, ?, Map<String, User>> toUserMap =
    Collectors.toUnmodifiableMap(User::email, Function.identity());

// Parallel streams (use only for CPU-bound work on large datasets)
long count = IntStream.range(0, 10_000_000)
    .parallel()
    .filter(n -> isPrime(n))
    .count();

// Avoid parallel streams when:
// - The data set is small (overhead outweighs benefit)
// - Operations have side effects or shared mutable state
// - The source is not efficiently splittable (e.g., LinkedList, Stream.iterate)
```

### Step 3: Design Type-Safe Generics

**Bounded Type Parameters and Wildcards**:

```java
// Upper bounded type parameter
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}

// Multiple bounds
public static <T extends Serializable & Comparable<T>> void process(T item) {
    // T must implement both Serializable and Comparable
}

// Wildcards: PECS (Producer Extends, Consumer Super)
// Use extends when you READ from a structure
public static double sum(List<? extends Number> numbers) {
    return numbers.stream()
        .mapToDouble(Number::doubleValue)
        .sum();
}

// Use super when you WRITE to a structure
public static void addIntegers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
    list.add(3);
}

// Unbounded wildcard for read-only generic operations
public static void printAll(List<?> items) {
    for (Object item : items) {
        System.out.println(item);
    }
}
```

**Generic Methods and Type Tokens**:

```java
// Generic method with inferred types
public static <K, V> Map<K, V> mapOf(K key, V value) {
    return Map.of(key, value);
}

// Type-safe heterogeneous container using type tokens
public class TypeSafeRegistry {
    private final Map<Class<?>, Object> map = new ConcurrentHashMap<>();

    public <T> void put(Class<T> type, T instance) {
        map.put(Objects.requireNonNull(type), instance);
    }

    public <T> T get(Class<T> type) {
        return type.cast(map.get(type));
    }
}

// Usage
var registry = new TypeSafeRegistry();
registry.put(String.class, "hello");
registry.put(Integer.class, 42);
String s = registry.get(String.class);  // type-safe, no cast needed

// Generic interface with self-referential bound (Comparable pattern)
public interface Builder<T extends Builder<T>> {
    T withName(String name);
    T withAge(int age);
}

public class PersonBuilder implements Builder<PersonBuilder> {
    private String name;
    private int age;

    @Override
    public PersonBuilder withName(String name) {
        this.name = name;
        return this;
    }

    @Override
    public PersonBuilder withAge(int age) {
        this.age = age;
        return this;
    }

    public Person build() {
        return new Person(name, age);
    }
}
```

**Type Erasure Workarounds**:

```java
// Problem: cannot do "new T()" or "T.class" due to erasure
// Solution 1: Pass Class<T> as a parameter
public static <T> T createInstance(Class<T> type) throws Exception {
    return type.getDeclaredConstructor().newInstance();
}

// Solution 2: Use a Supplier<T> factory
public static <T> List<T> createList(int size, Supplier<T> factory) {
    return IntStream.range(0, size)
        .mapToObj(i -> factory.get())
        .collect(Collectors.toList());
}

List<StringBuilder> builders = createList(5, StringBuilder::new);

// Solution 3: TypeReference pattern (used by Jackson, Spring)
public abstract class TypeReference<T> {
    private final Type type;

    protected TypeReference() {
        Type superclass = getClass().getGenericSuperclass();
        this.type = ((ParameterizedType) superclass).getActualTypeArguments()[0];
    }

    public Type getType() { return type; }
}

// Usage with Jackson
List<User> users = objectMapper.readValue(json,
    new TypeReference<List<User>>() {});
```

### Step 4: Build Concurrent Applications

**CompletableFuture Pipelines**:

```java
// Async computation with chaining
CompletableFuture<UserProfile> profileFuture = CompletableFuture
    .supplyAsync(() -> userService.findById(userId))
    .thenApply(user -> enrichWithPreferences(user))
    .thenApply(user -> buildProfile(user))
    .exceptionally(ex -> {
        logger.error("Failed to load profile for user {}", userId, ex);
        return UserProfile.defaultProfile();
    });

// Combining multiple futures
CompletableFuture<String> nameFuture = CompletableFuture.supplyAsync(() -> fetchName(id));
CompletableFuture<String> emailFuture = CompletableFuture.supplyAsync(() -> fetchEmail(id));
CompletableFuture<String> roleFuture = CompletableFuture.supplyAsync(() -> fetchRole(id));

CompletableFuture<UserSummary> combined = nameFuture
    .thenCombine(emailFuture, (name, email) -> new UserSummary(name, email, null))
    .thenCombine(roleFuture, (summary, role) -> new UserSummary(summary.name(), summary.email(), role));

// Wait for all futures
CompletableFuture<Void> allDone = CompletableFuture.allOf(nameFuture, emailFuture, roleFuture);
allDone.thenRun(() -> System.out.println("All lookups complete"));

// Wait for first to complete
CompletableFuture<Object> fastest = CompletableFuture.anyOf(
    fetchFromPrimary(id),
    fetchFromSecondary(id)
);
```

**Virtual Threads and Structured Concurrency**:

```java
// Virtual threads replace platform threads for I/O-bound work (Java 21+)
// Each virtual thread is lightweight (a few KB vs. ~1 MB for platform threads)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Response>> futures = requests.stream()
        .map(req -> executor.submit(() -> httpClient.send(req, BodyHandlers.ofString())))
        .toList();

    for (var future : futures) {
        Response response = future.get();
        process(response);
    }
}

// Structured concurrency (preview in Java 21+)
// Ensures child tasks are bounded by the parent scope
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User> userTask = scope.fork(() -> userService.findById(userId));
    Subtask<List<Order>> ordersTask = scope.fork(() -> orderService.findByUser(userId));

    scope.join();            // Wait for both tasks
    scope.throwIfFailed();   // Propagate any exception

    return new UserDashboard(userTask.get(), ordersTask.get());
}

// Synchronized vs ReentrantLock
// Use synchronized for simple mutual exclusion
public class Counter {
    private int count = 0;

    public synchronized void increment() { count++; }
    public synchronized int getCount() { return count; }
}

// Use ReentrantLock for advanced features (tryLock, timed lock, fairness)
public class FairCounter {
    private final ReentrantLock lock = new ReentrantLock(true); // fair ordering
    private int count = 0;

    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock(); // always unlock in finally
        }
    }

    public boolean tryIncrement(long timeout, TimeUnit unit) throws InterruptedException {
        if (lock.tryLock(timeout, unit)) {
            try {
                count++;
                return true;
            } finally {
                lock.unlock();
            }
        }
        return false;
    }
}
```

**Atomic Variables and ConcurrentHashMap**:

```java
// AtomicInteger, AtomicLong, AtomicReference for lock-free operations
private final AtomicLong requestCount = new AtomicLong(0);

public void handleRequest() {
    long count = requestCount.incrementAndGet();
    logger.info("Request #{}", count);
}

// ConcurrentHashMap for thread-safe map operations
private final ConcurrentHashMap<String, AtomicLong> metrics = new ConcurrentHashMap<>();

public void recordMetric(String name) {
    metrics.computeIfAbsent(name, k -> new AtomicLong(0)).incrementAndGet();
}

public Map<String, Long> getSnapshot() {
    return metrics.entrySet().stream()
        .collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().get()));
}
```

### Step 5: Apply Spring Boot Patterns

**Dependency Injection and Configuration**:

```java
// Constructor injection (preferred over field injection)
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
    private final NotificationService notificationService;

    // Single constructor: @Autowired is optional
    public OrderService(OrderRepository orderRepository,
                        PaymentGateway paymentGateway,
                        NotificationService notificationService) {
        this.orderRepository = orderRepository;
        this.paymentGateway = paymentGateway;
        this.notificationService = notificationService;
    }
}

// @Configuration class for third-party beans
@Configuration
public class HttpClientConfig {

    @Bean
    public HttpClient httpClient(@Value("${http.timeout:30}") int timeoutSeconds) {
        return HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(timeoutSeconds))
            .followRedirects(HttpClient.Redirect.NORMAL)
            .build();
    }

    @Bean
    @Profile("production")
    public HttpClient productionHttpClient() {
        return HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .sslContext(productionSslContext())
            .build();
    }
}

// Type-safe configuration properties
@ConfigurationProperties(prefix = "app.notification")
public record NotificationProperties(
    boolean enabled,
    String senderEmail,
    int maxRetries,
    Duration retryDelay
) {}

// application.yml
// app:
//   notification:
//     enabled: true
//     sender-email: noreply@example.com
//     max-retries: 3
//     retry-delay: 5s
```

**REST Controllers and Exception Handlers**:

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<UserDto> listUsers(@RequestParam(defaultValue = "0") int page,
                                   @RequestParam(defaultValue = "20") int size) {
        return userService.findAll(PageRequest.of(page, size))
            .map(UserDto::from)
            .getContent();
    }

    @GetMapping("/{id}")
    public UserDto getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(UserDto::from)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDto createUser(@Valid @RequestBody CreateUserRequest request) {
        User user = userService.create(request);
        return UserDto.from(user);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable Long id) {
        userService.delete(id);
    }
}

// Spring Security basic configuration (Java 21+ / Spring Security 6.x)
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .build();
    }
}
```

### Step 6: Implement Error Handling and Resilience

**Custom Exception Hierarchy**:

```java
// Base application exception
public abstract class ApplicationException extends RuntimeException {
    private final String errorCode;

    protected ApplicationException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    protected ApplicationException(String errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }

    public String getErrorCode() { return errorCode; }
}

// Specific exception types
public class ResourceNotFoundException extends ApplicationException {
    public ResourceNotFoundException(String resourceType, Object id) {
        super("NOT_FOUND", "%s not found with id: %s".formatted(resourceType, id));
    }
}

public class BusinessRuleException extends ApplicationException {
    public BusinessRuleException(String rule, String detail) {
        super("BUSINESS_RULE_VIOLATION", "Rule '%s' violated: %s".formatted(rule, detail));
    }
}

// Global exception handler with @ControllerAdvice
@RestControllerAdvice
public class GlobalExceptionHandler {

    record ErrorResponse(String code, String message, Instant timestamp) {}

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        return new ErrorResponse(ex.getErrorCode(), ex.getMessage(), Instant.now());
    }

    @ExceptionHandler(BusinessRuleException.class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    public ErrorResponse handleBusinessRule(BusinessRuleException ex) {
        return new ErrorResponse(ex.getErrorCode(), ex.getMessage(), Instant.now());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        String details = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return new ErrorResponse("VALIDATION_ERROR", details, Instant.now());
    }
}
```

**Result Pattern and Resilience4j**:

```java
// Result type (Either pattern) for explicit error handling without exceptions
public sealed interface Result<T> permits Result.Success, Result.Failure {

    record Success<T>(T value) implements Result<T> {}
    record Failure<T>(String error) implements Result<T> {}

    static <T> Result<T> success(T value) { return new Success<>(value); }
    static <T> Result<T> failure(String error) { return new Failure<>(error); }

    default <R> Result<R> map(Function<T, R> fn) {
        return switch (this) {
            case Success<T> s -> Result.success(fn.apply(s.value()));
            case Failure<T> f -> Result.failure(f.error());
        };
    }

    default <R> Result<R> flatMap(Function<T, Result<R>> fn) {
        return switch (this) {
            case Success<T> s -> fn.apply(s.value());
            case Failure<T> f -> Result.failure(f.error());
        };
    }

    default T orElse(T fallback) {
        return switch (this) {
            case Success<T> s -> s.value();
            case Failure<T> f -> fallback;
        };
    }
}

// Usage
Result<User> result = validateInput(request)
    .flatMap(this::findUser)
    .map(this::enrichProfile);

// Resilience4j: retry with exponential backoff
RetryConfig retryConfig = RetryConfig.custom()
    .maxAttempts(3)
    .waitDuration(Duration.ofMillis(500))
    .retryExceptions(IOException.class, TimeoutException.class)
    .ignoreExceptions(BusinessRuleException.class)
    .build();

Retry retry = Retry.of("paymentService", retryConfig);

Supplier<PaymentResult> supplier = Retry.decorateSupplier(retry,
    () -> paymentGateway.charge(amount));
PaymentResult result = supplier.get();

// Resilience4j: circuit breaker
CircuitBreakerConfig cbConfig = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)
    .waitDurationInOpenState(Duration.ofSeconds(30))
    .slidingWindowSize(10)
    .build();

CircuitBreaker circuitBreaker = CircuitBreaker.of("inventoryService", cbConfig);

Supplier<Inventory> decorated = CircuitBreaker.decorateSupplier(circuitBreaker,
    () -> inventoryService.check(productId));
```

### Step 7: Test Effectively with JUnit 5

**Parameterized and Nested Tests**:

```java
class UserValidatorTest {

    private final UserValidator validator = new UserValidator();

    @ParameterizedTest(name = "email \"{0}\" should be {1}")
    @CsvSource({
        "alice@example.com, true",
        "bob@test.org, true",
        "invalid, false",
        "'', false",
        "@missing-local.com, false"
    })
    void shouldValidateEmail(String email, boolean expected) {
        assertThat(validator.isValidEmail(email)).isEqualTo(expected);
    }

    @ParameterizedTest
    @MethodSource("userProvider")
    void shouldValidateUser(User user, boolean expected) {
        assertThat(validator.isValid(user)).isEqualTo(expected);
    }

    static Stream<Arguments> userProvider() {
        return Stream.of(
            Arguments.of(new User("Alice", "alice@example.com", LocalDate.now()), true),
            Arguments.of(new User("", "bob@example.com", LocalDate.now()), false),
            Arguments.of(new User("Charlie", "invalid", LocalDate.now()), false)
        );
    }

    @Nested
    class WhenUserIsNew {
        @Test
        void shouldRequireName() {
            var user = new User("", "test@example.com", LocalDate.now());
            assertThat(validator.isValid(user)).isFalse();
        }

        @Test
        void shouldRequireValidEmail() {
            var user = new User("Alice", "not-an-email", LocalDate.now());
            assertThat(validator.isValid(user)).isFalse();
        }
    }

    @Nested
    class WhenUserExists {
        @Test
        void shouldAllowEmailUpdate() {
            var user = new User("Alice", "new@example.com", LocalDate.of(2024, 1, 1));
            assertThat(validator.isValid(user)).isTrue();
        }
    }
}
```

**Mockito and AssertJ**:

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private OrderRepository orderRepository;
    @Mock private PaymentGateway paymentGateway;
    @Mock private NotificationService notificationService;
    @InjectMocks private OrderService orderService;

    @Test
    void shouldCreateOrderAndChargePayment() {
        // Arrange
        var request = new CreateOrderRequest("user-1", List.of(
            new OrderItem("product-a", 2, new BigDecimal("10.00"))
        ));
        var expectedOrder = new Order("order-1", "user-1", new BigDecimal("20.00"));

        when(orderRepository.save(any(Order.class))).thenReturn(expectedOrder);
        when(paymentGateway.charge(any(BigDecimal.class))).thenReturn(PaymentResult.success());

        // Act
        Order result = orderService.createOrder(request);

        // Assert
        assertThat(result.id()).isEqualTo("order-1");
        assertThat(result.total()).isEqualByComparingTo("20.00");

        verify(paymentGateway).charge(new BigDecimal("20.00"));
        verify(notificationService).sendOrderConfirmation(eq("user-1"), any());
        verifyNoMoreInteractions(paymentGateway);
    }

    @Test
    void shouldThrowWhenPaymentFails() {
        var request = new CreateOrderRequest("user-1", List.of(
            new OrderItem("product-a", 1, new BigDecimal("50.00"))
        ));

        when(orderRepository.save(any())).thenReturn(new Order("order-2", "user-1", new BigDecimal("50.00")));
        when(paymentGateway.charge(any())).thenReturn(PaymentResult.declined("insufficient funds"));

        assertThatThrownBy(() -> orderService.createOrder(request))
            .isInstanceOf(PaymentDeclinedException.class)
            .hasMessageContaining("insufficient funds");

        verify(notificationService, never()).sendOrderConfirmation(any(), any());
    }
}
```

**TestContainers and MockMvc**:

```java
// Integration test with TestContainers (real PostgreSQL)
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldPersistAndRetrieveUser() {
        var user = new UserEntity("Alice", "alice@example.com");
        userRepository.save(user);

        Optional<UserEntity> found = userRepository.findByEmail("alice@example.com");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Alice");
    }
}

// Web layer test with MockMvc (Spring Boot test slice)
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired private MockMvc mockMvc;
    @MockBean private UserService userService;

    @Test
    void shouldReturnUserById() throws Exception {
        var user = new User("user-1", "Alice", "alice@example.com");
        when(userService.findById("user-1")).thenReturn(Optional.of(user));

        mockMvc.perform(get("/api/v1/users/user-1")
                .accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("Alice"))
            .andExpect(jsonPath("$.email").value("alice@example.com"));
    }

    @Test
    void shouldReturn404WhenUserNotFound() throws Exception {
        when(userService.findById("missing")).thenReturn(Optional.empty());

        mockMvc.perform(get("/api/v1/users/missing")
                .accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.code").value("NOT_FOUND"));
    }

    @Test
    void shouldValidateCreateRequest() throws Exception {
        String invalidBody = """
                { "name": "", "email": "not-valid" }
                """;

        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidBody))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"));
    }
}
```

## Best Practices

- **Prefer records for data transfer** - Use records for DTOs, value objects, and event payloads
- **Use sealed types for domain modeling** - Sealed interfaces with records make invalid states unrepresentable
- **Choose virtual threads for I/O** - Virtual threads excel for I/O-bound workloads; platform threads remain better for CPU-bound computation
- **Favor Optional over null returns** - Return Optional from lookup methods; never use Optional as a field or parameter type
- **Inject dependencies through constructors** - Constructor injection makes dependencies explicit and supports immutability
- **Keep controllers thin** - Controllers should delegate to services; business logic never belongs in a controller
- **Handle exceptions globally** - Use @ControllerAdvice for consistent error responses across all endpoints
- **Test at the right level** - Use MockMvc for web layer, Mockito for unit tests, TestContainers for integration tests

## Common Patterns

### Pattern 1: Repository with Specification

```java
public interface UserRepository extends JpaRepository<UserEntity, Long>,
                                        JpaSpecificationExecutor<UserEntity> {}

// Dynamic queries with Specifications
public class UserSpecifications {

    public static Specification<UserEntity> hasName(String name) {
        return (root, query, cb) -> cb.equal(root.get("name"), name);
    }

    public static Specification<UserEntity> emailContains(String fragment) {
        return (root, query, cb) -> cb.like(
            cb.lower(root.get("email")),
            "%" + fragment.toLowerCase() + "%"
        );
    }

    public static Specification<UserEntity> joinedAfter(LocalDate date) {
        return (root, query, cb) -> cb.greaterThan(root.get("joinDate"), date);
    }
}

// Usage
List<UserEntity> results = userRepository.findAll(
    hasName("Alice").and(joinedAfter(LocalDate.of(2024, 1, 1)))
);
```

### Pattern 2: Event-Driven with Spring ApplicationEvent

```java
// Domain event
public record OrderPlacedEvent(String orderId, String userId, BigDecimal total) {}

// Publishing
@Service
public class OrderService {
    private final ApplicationEventPublisher eventPublisher;

    public OrderService(ApplicationEventPublisher eventPublisher) {
        this.eventPublisher = eventPublisher;
    }

    @Transactional
    public Order placeOrder(CreateOrderRequest request) {
        Order order = createAndSave(request);
        eventPublisher.publishEvent(new OrderPlacedEvent(order.id(), order.userId(), order.total()));
        return order;
    }
}

// Listening
@Component
public class OrderEventListener {

    @EventListener
    public void onOrderPlaced(OrderPlacedEvent event) {
        // Send confirmation email, update inventory, etc.
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void afterOrderCommitted(OrderPlacedEvent event) {
        // Only fires after the transaction commits successfully
    }
}
```

## Quality Checklist

- [ ] Records used for value types and DTOs
- [ ] Sealed interfaces used for closed type hierarchies
- [ ] Streams used instead of imperative loops for collection transformations
- [ ] Optional returned from lookup methods (never null)
- [ ] CompletableFuture or virtual threads for async I/O
- [ ] Custom exception hierarchy with @ControllerAdvice
- [ ] Constructor injection throughout (no @Autowired on fields)
- [ ] Tests cover unit, integration, and web layers
- [ ] Parameterized tests for functions with multiple input/output combinations

## Related Skills

- `spring-boot-expert` - Advanced Spring Boot patterns
- `performance-testing` - JMH benchmarks, load testing
- `cicd-architect` - Maven/Gradle CI/CD pipelines
- `kubernetes-expert` - Java microservices on K8s
- `code-quality` - SonarQube, Checkstyle, SpotBugs

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Effective Java (Bloch), Spring Boot Reference, JDK 21+ documentation


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
