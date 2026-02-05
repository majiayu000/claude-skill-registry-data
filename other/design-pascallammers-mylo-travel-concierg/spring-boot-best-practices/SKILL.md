---
name: Spring Boot Best Practices
description: Generate Spring Boot components following modern Java best practices and team conventions
---

# Spring Boot Code Generation Guidelines

When generating or reviewing Spring Boot code, follow these best practices:

## Dependency Injection

- **Use constructor injection**, never field injection with @Autowired
- Mark injected fields as `private final`
- Let Lombok's `@RequiredArgsConstructor` generate constructors when appropriate

```java
// Good
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
}

// Avoid
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository; // Field injection - avoid
}
```

## Package Structure

Follow standard Spring Boot layering:
```
com.example.project/
├── controller/       # REST endpoints, @RestController
├── service/          # Business logic, @Service
├── repository/       # Data access, extends JpaRepository
├── model/            # JPA entities, @Entity
├── dto/              # Data transfer objects
├── config/           # Configuration classes, @Configuration
└── exception/        # Custom exceptions and @ControllerAdvice
```

## REST Controllers

- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Return `ResponseEntity<T>` for explicit status codes
- Use `@Valid` for request body validation
- Include API versioning in paths (e.g., `/api/v1/users`)

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<UserDto> createUser(@Valid @RequestBody CreateUserRequest request) {
        UserDto created = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

## Service Layer

- Keep services focused on business logic
- Use `Optional<T>` for potentially absent results
- Throw custom exceptions for business rule violations
- Add `@Transactional` where needed

```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Transactional
    public User create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new UserAlreadyExistsException(request.getEmail());
        }
        User user = new User(request.getName(), request.getEmail());
        return userRepository.save(user);
    }
}
```

## JPA Entities

- Use `@Entity` and `@Table` annotations
- Include `@Id` with generation strategy
- Use Lombok annotations: `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`
- Include proper relationships with `@OneToMany`, `@ManyToOne`, etc.

```java
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Order> orders = new ArrayList<>();
}
```

## Testing Requirements

For every component generated:

1. **Controller Tests** - Use `@WebMvcTest` and MockMvc
2. **Service Tests** - Use `@ExtendWith(MockitoExtension.class)` with mocks
3. **Repository Tests** - Use `@DataJpaTest` with test database
4. **Integration Tests** - Use `@SpringBootTest` for end-to-end scenarios

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void getUser_WhenExists_ReturnsUser() throws Exception {
        // Arrange
        UserDto user = new UserDto(1L, "John Doe", "john@example.com");
        when(userService.findById(1L)).thenReturn(Optional.of(user));

        // Act & Assert
        mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John Doe"));
    }
}
```

## Documentation

- Add comprehensive JavaDoc for public methods
- Include `@param`, `@return`, and `@throws` tags
- Document business rules and assumptions
- Use OpenAPI/Swagger annotations for REST endpoints

```java
/**
 * Creates a new user in the system.
 *
 * @param request the user creation request containing name and email
 * @return the created user with generated ID
 * @throws UserAlreadyExistsException if a user with the email already exists
 */
@Transactional
public User create(CreateUserRequest request) {
    // implementation
}
```

## Error Handling

- Create custom exceptions extending RuntimeException
- Use `@ControllerAdvice` for global exception handling
- Return proper HTTP status codes with error details

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
}
```

## Configuration

- Use `application.yml` over `application.properties`
- Externalize configuration values
- Use Spring profiles for environment-specific config

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
```

## When This Skill Activates

This skill automatically activates when:
- Generating Spring Boot controllers, services, or repositories
- Creating JPA entities or DTOs
- Writing Spring Boot tests
- Reviewing existing Spring Boot code
- Questions about Spring Boot best practices
