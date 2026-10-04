---
name: epci:java-springboot
description: >-
  Patterns and conventions for Java/Spring Boot. Includes Spring Data JPA,
  Spring Security, JUnit 5, Lombok. Use when: Spring Boot Java development,
  gradle maven build detected with spring dependencies.
  Not for: Jakarta enterprise edition, Quarkus framework.
user-invocable: false
---

# Java/Spring Boot Development Patterns

## Overview

Patterns and conventions for modern Spring Boot development.

## Auto-detection

Automatically loaded if detection of:
- `pom.xml` containing `spring-boot`
- `build.gradle` containing `spring-boot`
- Files `@SpringBootApplication`, `application.yml`

## Spring Boot Architecture

### Standard Structure

```
project/
├── src/
│   ├── main/
│   │   ├── java/com/example/app/
│   │   │   ├── Application.java
│   │   │   ├── config/           # Configuration beans
│   │   │   ├── controller/       # REST controllers
│   │   │   ├── service/          # Business logic
│   │   │   ├── repository/       # Data access
│   │   │   ├── entity/           # JPA entities
│   │   │   ├── dto/              # Data Transfer Objects
│   │   │   ├── exception/        # Custom exceptions
│   │   │   └── security/         # Security config
│   │   └── resources/
│   │       ├── application.yml
│   │       └── application-dev.yml
│   └── test/
│       └── java/com/example/app/
│           ├── controller/
│           ├── service/
│           └── repository/
├── pom.xml
└── README.md
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Controllers | `*Controller` | `UserController` |
| Services | `*Service` | `UserService` |
| Repositories | `*Repository` | `UserRepository` |
| Entities | Singular, PascalCase | `User` |
| DTOs | `*Request`, `*Response` | `CreateUserRequest` |
| Tests | `*Test` | `UserServiceTest` |

## Entity Patterns

### JPA Entity with Lombok

```java
@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private Boolean active = true;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}
```

### Repository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    List<User> findByActiveTrue();

    @Query("SELECT u FROM User u WHERE u.name LIKE %:name%")
    List<User> searchByName(@Param("name") String name);

    boolean existsByEmail(String email);
}
```

## Service Patterns

### Service with Transactions

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public User createUser(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new UserAlreadyExistsException(request.getEmail());
        }

        User user = User.builder()
                .email(request.getEmail())
                .name(request.getName())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();

        User savedUser = userRepository.save(user);

        eventPublisher.publishEvent(new UserCreatedEvent(savedUser));

        log.info("Created user with id: {}", savedUser.getId());

        return savedUser;
    }

    @Transactional(readOnly = true)
    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
    }

    @Transactional(readOnly = true)
    public Page<User> getActiveUsers(Pageable pageable) {
        return userRepository.findAll(
            (root, query, cb) -> cb.equal(root.get("active"), true),
            pageable
        );
    }
}
```

## Controller Patterns

### REST Controller

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
public class UserController {

    private final UserService userService;
    private final UserMapper userMapper;

    @GetMapping
    public ResponseEntity<Page<UserResponse>> getAllUsers(
            @PageableDefault(size = 20) Pageable pageable) {
        Page<User> users = userService.getActiveUsers(pageable);
        Page<UserResponse> response = users.map(userMapper::toResponse);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) {
        User user = userService.getUserById(id);
        return ResponseEntity.ok(userMapper.toResponse(user));
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody CreateUserRequest request) {
        User user = userService.createUser(request);
        UserResponse response = userMapper.toResponse(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
}
```

### DTO with Validation

```java
@Data
@Builder
public class CreateUserRequest {

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100)
    private String name;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;
}

@Data
@Builder
public class UserResponse {
    private Long id;
    private String email;
    private String name;
    private LocalDateTime createdAt;
}
```

## Exception Handling

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        log.warn("User not found: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(new ErrorResponse("USER_NOT_FOUND", ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors().stream()
                .map(e -> e.getField() + ": " + e.getDefaultMessage())
                .collect(Collectors.joining(", "));
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(new ErrorResponse("VALIDATION_ERROR", message));
    }
}
```

## Testing Patterns (JUnit 5)

### Unit Test

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Test
    void createUser_shouldCreateUserSuccessfully() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
                .email("test@example.com")
                .name("Test User")
                .password("password123")
                .build();

        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(passwordEncoder.encode(anyString())).thenReturn("encoded");
        when(userRepository.save(any(User.class))).thenAnswer(i -> {
            User u = i.getArgument(0);
            u.setId(1L);
            return u;
        });

        // When
        User result = userService.createUser(request);

        // Then
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getEmail()).isEqualTo("test@example.com");
        verify(userRepository).save(any(User.class));
    }

    @Test
    void createUser_shouldThrowWhenEmailExists() {
        CreateUserRequest request = CreateUserRequest.builder()
                .email("existing@example.com")
                .build();

        when(userRepository.existsByEmail(anyString())).thenReturn(true);

        assertThatThrownBy(() -> userService.createUser(request))
                .isInstanceOf(UserAlreadyExistsException.class);
    }
}
```

### Integration Test

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    @Test
    void createUser_shouldReturn201() throws Exception {
        CreateUserRequest request = CreateUserRequest.builder()
                .email("new@example.com")
                .name("New User")
                .password("password123")
                .build();

        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.email").value("new@example.com"))
                .andExpect(jsonPath("$.id").exists());
    }

    @Test
    void getUserById_shouldReturn404WhenNotFound() throws Exception {
        mockMvc.perform(get("/api/v1/users/999"))
                .andExpect(status().isNotFound());
    }
}
```

## Useful Commands

```bash
# Maven
mvn spring-boot:run
mvn clean install
mvn test
mvn test -Dtest=UserServiceTest

# Gradle
./gradlew bootRun
./gradlew build
./gradlew test
./gradlew test --tests UserServiceTest
```

## Spring Boot Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Injection | Constructor injection | @Autowired on fields |
| Transactions | @Transactional on service | Transaction on controller |
| DTO | Separate Request/Response | Entity in API |
| Validation | @Valid + annotations | Manual validation |
| Logs | SLF4J + parameters | String concatenation |

## Security Config

```java
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/public/**").permitAll()
                        .requestMatchers("/api/admin/**").hasRole("ADMIN")
                        .anyRequest().authenticated())
                .sessionManagement(session ->
                        session.sessionCreationPolicy(STATELESS))
                .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

## Deep Dive References

For detailed patterns and advanced usage, see:

| Topic | Reference | Description |
|-------|-----------|-------------|
| Architecture | @references/architecture.md | Clean/Hexagonal, CQRS, Modular monolith |
| JPA/Hibernate | @references/jpa-hibernate.md | Entity patterns, N+1, Specifications |
| Security | @references/security.md | Spring Security 6, JWT, OAuth2 |
| Testing | @references/testing.md | JUnit 5, TestContainers, ArchUnit |
| Reactive | @references/reactive.md | WebFlux, R2DBC, Backpressure |
