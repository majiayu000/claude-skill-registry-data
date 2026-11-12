---
name: spring-testing
description: "Spring 단위·슬라이스 테스트 — JUnit 5, Mockito, @WebMvcTest, @DataJpaTest, 테스트 픽스처, 네이밍 규칙, 테스트 피라미드. Use when Spring 서비스·컨트롤러·리포지토리 테스트를 작성하거나 mock 범위를 정할 때."
---

# Spring Testing Patterns

JUnit 5, Mockito를 활용한 테스트 패턴

## Quick Reference (결정 트리)

```
테스트 타입 선택
    │
    ├─ 비즈니스 로직 ────> Unit Test (@ExtendWith(MockitoExtension))
    │
    ├─ Controller ───────> @WebMvcTest
    │
    ├─ Repository ───────> @DataJpaTest
    │
    └─ 전체 통합 ────────> @SpringBootTest + Testcontainers
                          (상세: /java:spring-testcontainers 참조)
```

---

## 테스트 피라미드

```
        /\
       /  \      E2E Tests (적게)
      /----\
     /      \    Integration Tests (적당히)
    /--------\
   /          \  Unit Tests (많이)
  --------------
```

---

## CRITICAL: Unit Tests (Mockito)

### Service 테스트

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    @DisplayName("사용자 생성 성공")
    void createUser_Success() {
        // Given
        CreateUserRequest request = new CreateUserRequest("test@example.com", "password");
        when(userRepository.existsByEmail(request.getEmail())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // When
        UserResponse response = userService.createUser(request);

        // Then
        assertThat(response.getEmail()).isEqualTo("test@example.com");
        verify(userRepository).save(any(User.class));
    }

    @Test
    @DisplayName("중복 이메일로 예외")
    void createUser_DuplicateEmail_ThrowsException() {
        when(userRepository.existsByEmail(anyString())).thenReturn(true);

        assertThatThrownBy(() -> userService.createUser(request))
            .isInstanceOf(DuplicateException.class);

        verify(userRepository, never()).save(any());
    }
}
```

### Parameterized Tests

```java
@ParameterizedTest
@CsvSource({
    "test@example.com, true",
    "invalid-email, false",
    "'', false"
})
void validateEmail(String email, boolean expected) {
    assertThat(EmailValidator.isValid(email)).isEqualTo(expected);
}

@ParameterizedTest
@MethodSource("provideUserCreationData")
void createUser_MultipleScenarios(CreateUserRequest request, Class<? extends Exception> expected) {
    if (expected == null) {
        assertThatNoException().isThrownBy(() -> userService.createUser(request));
    } else {
        assertThatThrownBy(() -> userService.createUser(request)).isInstanceOf(expected);
    }
}
```

---

## @WebMvcTest (Controller)

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void getUser_Success() throws Exception {
        when(userService.getUser(1L)).thenReturn(new UserResponse(1L, "test@example.com"));

        mockMvc.perform(get("/api/users/{id}", 1L)
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.email").value("test@example.com"));
    }

    @Test
    void createUser_ValidationFailed() throws Exception {
        CreateUserRequest request = new CreateUserRequest("invalid", "");

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isBadRequest());
    }
}
```

---

## @DataJpaTest (Repository)

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void findByEmail_Success() {
        // Given
        User user = User.builder().email("test@example.com").build();
        entityManager.persistAndFlush(user);

        // When
        Optional<User> found = userRepository.findByEmail("test@example.com");

        // Then
        assertThat(found).isPresent();
    }
}
```

**Testcontainers 사용**: `/java:spring-testcontainers` 참조

---

## 테스트 픽스처

```java
public class UserFixture {
    public static User createUser() {
        return User.builder()
            .email("test@example.com")
            .password("password")
            .status(UserStatus.ACTIVE)
            .build();
    }

    public static User createUser(String email) {
        return User.builder().email(email).password("password").build();
    }
}
```

---

## 테스트 네이밍 규칙

```java
// Given-When-Then 패턴
@Test
void createUser_WithDuplicateEmail_ThrowsException() { }

// @DisplayName으로 한글 설명
@Test
@DisplayName("유효한 ID로 사용자 조회 시 사용자 반환")
void getUser_ValidId_ReturnsUser() { }
```

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| @SpringBootTest 남용 | 필요한 슬라이스만 사용 |
| 테스트 간 상태 공유 | @BeforeEach로 초기화 |
| 실제 외부 서비스 호출 | Mock 또는 Testcontainers |
| 테스트 순서 의존 | 독립적인 테스트 작성 |

---

## 체크리스트

- [ ] Unit Test: 핵심 비즈니스 로직
- [ ] @WebMvcTest: Controller
- [ ] @DataJpaTest: Repository
- [ ] 경계값, 예외 케이스 포함
- [ ] 테스트 격리 (독립 실행)
- [ ] CI에서 자동 실행
