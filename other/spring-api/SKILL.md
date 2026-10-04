---
name: spring-api
description: >
  Spring Boot REST API 엔드포인트를 프로젝트 컨벤션에 맞게 생성하는 스킬.
  "/spring-api"를 입력하거나, "API 만들어줘", "엔드포인트 추가해줘",
  "컨트롤러 생성해줘" 같은 요청에 트리거된다.
  Controller → Service → Repository → Entity → DTO 전체 레이어를 일관된 패턴으로 생성한다.
---

# Spring API 엔드포인트 생성

프로젝트 컨벤션(`.ai/rules/common-rule.md`)과 기존 코드 패턴을 따라 REST API 엔드포인트를 생성하는 스킬이다.

## 사전 확인

스킬 실행 전 반드시 다음을 확인한다:

1. `.ai/rules/common-rule.md` 읽기 — 코드 컨벤션 숙지
2. `doc/ERD.md` / `doc/ERD_NON_STANDARD_TABLES.md` 읽기 — 테이블 구조 확인
3. 기존 유사 코드 참조 — `MedicalController.java`, `ChatController.java` 패턴 확인

## 생성 순서

### Step 1: Entity 생성

```java
@Entity
@Table(name = "{테이블명}")
@Getter
@Setter
@NoArgsConstructor
public class {Domain} {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // FK는 @ManyToOne(fetch = FetchType.LAZY)
    // 생성일은 LocalDateTime createdAt = LocalDateTime.now()
}
```

**체크리스트:**
- [ ] `@Table(name = "...")` 이 ERD 테이블명과 일치
- [ ] FK 관계는 `FetchType.LAZY`
- [ ] `@NoArgsConstructor` 필수

### Step 2: Repository 생성

```java
public interface {Domain}Repository extends JpaRepository<{Domain}, Long> {
    // 페이징 조회 시: Page<{Domain}> findBy{FK}_IdOrderByCreatedAtDesc(Long id, Pageable pageable);
}
```

### Step 3: DTO 생성

```java
@Getter
@AllArgsConstructor
public class {Domain}Response {
    // 필드
    public static {Domain}Response from({Domain} entity) {
        return new {Domain}Response(...);
    }
}
```

**규칙:**
- Entity → DTO 변환은 `static from()` 팩토리 메서드
- Controller에 Entity를 절대 노출하지 않는다

### Step 4: Service 생성

```java
@Transactional(readOnly = true)
@RequiredArgsConstructor
@Service
@Slf4j
public class {Domain}Service {

    private final WebClient llmWebClient;  // LLM 호출 시
    private final {Domain}Repository {domain}Repository;

    // 쓰기 메서드에는 개별 @Transactional
    @Transactional
    public {Domain} save{Domain}(...) { ... }
}
```

**LLM 호출 패턴:**
- `llmWebClient.post().uri("/infer/{endpoint}").bodyValue(Map.of(...)).retrieve().bodyToMono(LlmResponse.class)`
- 에러 매핑: `WebClientRequestException` → `LlmServiceUnavailableException`, `TimeoutException` → `LlmTimeoutException`

### Step 5: Controller 생성

```java
@RequiredArgsConstructor
@RestController
@RequestMapping("/api/{domain}")
@Slf4j
public class {Domain}Controller {

    // POST: Mono<> 반환 (비동기 LLM 호출)
    // GET: Page<{Domain}Response> 반환 (히스토리 조회)
}
```

**헤더 패턴:**
- 사용자 식별: `@RequestHeader(value = "X-Staff-Id", required = true) Long staffId`
- 선택적 식별: `@RequestHeader(value = "X-User-Id", required = false) Long userId`

### Step 6: 테스트 생성

```java
@WebMvcTest({Domain}Controller.class)
class {Domain}ControllerTest {
    @Autowired MockMvc mockMvc;
    @MockitoBean {Domain}Service service;
    // asyncDispatch 패턴으로 Mono 응답 테스트
}
```

**필수 테스트 케이스:**
- 정상 응답
- LLM 서버 연결 실패 (503)
- LLM 타임아웃 (504)
- 히스토리 조회 (빈 결과 포함)

## Python 엔드포인트 연동

Spring에서 새 API를 추가하면, 대응하는 Python FastAPI 엔드포인트가 필요한지 확인한다:

- LLM 추론이 필요하면 `python-llm/app.py`에 `/infer/{endpoint}` 추가
- 시스템 프롬프트는 `app.py` 상단에 상수로 정의
- Ollama Chat API 호출 패턴은 기존 `infer_medical`, `infer_rule` 참조

## 주의사항

- 어노테이션 순서: `@RequiredArgsConstructor` → `@RestController` → `@RequestMapping` → `@Slf4j`
- 모든 비동기 응답은 `Mono<>` 또는 `Flux<>` (WebClient 사용)
- SSE 스트리밍: `produces = MediaType.TEXT_EVENT_STREAM_VALUE` + `Flux<String>` 반환
