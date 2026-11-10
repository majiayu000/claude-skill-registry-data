---
name: spring-boot-4
description: Build, review and upgrade Spring Boot 4 web services (checked against Boot 4.1.2, Spring Framework 7.0.10, Jackson 3.1.7). Covers the split starters and test starters, Jackson 3 (tools.jackson packages, @JacksonComponent, ValueSerializer, JsonMapperBuilderCustomizer, the ObjectMapper bean Boot 4 ignores, default changes that alter JSON silently), built-in method validation versus class-level @Validated, HandlerMethodValidationException and RFC 9457 problem details with per-field errors, Boot 4 test packages (@MockitoBean, RestTestClient, TestRestTemplate opt-in), RestTemplateBuilder and HTTP client moves, API versioning, core @Retryable and virtual threads. Use when a build uses spring-boot-starter-parent 4.x, when upgrading from Boot 3, when a build fails on com.fasterxml.jackson.databind, @MockBean, @WebMvcTest or TestRestTemplate, or when customizing JSON, validating requests, shaping error responses or writing Spring MVC tests.
license: MIT
---

# Spring Boot 4 web services

Spring Boot 4 is the current major (`4.1.2` as of November 2026, on Spring Framework `7.0.10`,
Jackson `3.1.7`, Hibernate Validator `9.1.5`, Tomcat `11.0.27`, JUnit `6.0.3`; Java 17+, 25 is the
current LTS). Most Spring code an agent has seen is Boot 2 or 3. Much of it no longer compiles on 4,
and the dangerous part is what still compiles and does something else. Every behaviour below was
measured on 4.1.2 unless it cites a document.

## 1. Know which Boot you are on

```sh
mvn help:evaluate -Dexpression=project.parent.version -q -DforceStdout   # Maven, parent POM
./gradlew dependencyInsight --dependency spring-boot                     # Gradle
```

| Boot | Framework | JSON | Notes |
| --- | --- | --- | --- |
| 3.5.x | 6.2 | Jackson 2 (`com.fasterxml.jackson`) | last 3.x line; `@MockitoBean` already exists, `@MockBean` deprecated |
| 4.0.x, 4.1.x | 7.0 | Jackson 3 (`tools.jackson`) | modular starters, Jackson 2 only as a deprecated module |

Builds in this kind of repo are often hermetic (`.mvn/maven.config` pointing at a repo-local
repository, `mvn -o`). Before adding a dependency, check it is already there
(`ls .m2/repository/org/springframework/boot/`); you cannot download in an offline build.

## 2. Starters are per technology now

Boot 4 split the auto-configuration into modules (`spring-boot-<tech>`, packages
`org.springframework.boot.<tech>`) with one starter and one test starter each.

| You need | Boot 4 dependency | Boot 3 habit that breaks |
| --- | --- | --- |
| Spring MVC + Tomcat + Jackson | `spring-boot-starter-webmvc` | `spring-boot-starter-web` still resolves but is deprecated |
| `@WebMvcTest`, `@AutoConfigureMockMvc` | `spring-boot-starter-webmvc-test` (test) | `spring-boot-starter-test` alone: those annotations don't exist |
| `RestTemplateBuilder`, `RestClient.Builder` bean, HTTP service clients | `spring-boot-starter-restclient` | came with the web starter in 3.x |
| `TestRestTemplate` | `spring-boot-resttestclient` (inside `-webmvc-test`) **and** `@AutoConfigureTestRestTemplate` | injected by `@SpringBootTest(RANDOM_PORT)` in 3.x |
| Bean Validation | `spring-boot-starter-validation` | unchanged |

`spring-boot-starter-test` still brings JUnit, AssertJ, Mockito, JSONPath and `spring-test`; each
technology test starter brings it transitively. The `*-classic` starters exist to get a big upgrade
compiling, not as a destination. Full map: [references/upgrade-from-3.md](references/upgrade-from-3.md).

## 3. Jackson 3: what changed under your JSON

### 3.1 Packages and types

Jackson 3 lives in `tools.jackson.*` (group `tools.jackson.core`). The annotations did **not** move:
`com.fasterxml.jackson.annotation.*` (`@JsonProperty`, `@JsonInclude`, `@JsonValue`, `@JsonCreator`)
is still right. Everything else did.

| Jackson 2 / Boot 3 | Jackson 3 / Boot 4 |
| --- | --- |
| `com.fasterxml.jackson.databind.ObjectMapper` | `tools.jackson.databind.json.JsonMapper` (immutable; `JsonMapper.builder()`, `mapper.rebuild()`) |
| `JsonSerializer<T>`, `JsonDeserializer<T>` | `ValueSerializer<T>`, `ValueDeserializer<T>` |
| `SerializerProvider` | `SerializationContext` |
| `JsonProcessingException` (checked) | `JacksonException` (unchecked); no `throws IOException` |
| `gen.writeStringField(name, v)` | `gen.writeStringProperty(name, v)` |
| `p.getCodec().readTree(p)`, `node.asText()`, `isTextual()` | `ctxt.readTree(p)`, `node.asString()`, `isString()` |
| `Module` beans | `JacksonModule` beans (still auto-registered) |
| `@JsonComponent`, `@JsonMixin` | `@JacksonComponent`, `@JacksonMixin` (`org.springframework.boot.jackson`) |
| `Jackson2ObjectMapperBuilderCustomizer` | `JsonMapperBuilderCustomizer` (`org.springframework.boot.jackson.autoconfigure`) |
| `SerializationFeature.WRITE_DATES_AS_TIMESTAMPS` | `DateTimeFeature.WRITE_DATES_AS_TIMESTAMPS` (`tools.jackson.databind.cfg`) |
| `SerializationFeature.WRITE_ENUMS_USING_TO_STRING` | `EnumFeature.WRITE_ENUMS_USING_TO_STRING` |
| `builder.serializationInclusion(NON_NULL)` | `builder.changeDefaultPropertyInclusion(v -> v.withValueInclusion(NON_NULL))` |

`@JsonSerialize`/`@JsonDeserialize`/`@JsonNaming` moved to `tools.jackson.databind.annotation`. If a
leftover `com.fasterxml.jackson.databind.annotation` import still compiles (Jackson 2 on the
classpath through some other library), Jackson 3 ignores it silently.

### 3.2 Configure the mapper Boot uses, not a second one

1. **Properties first**: `spring.jackson.property-naming-strategy=SNAKE_CASE`,
   `spring.jackson.default-property-inclusion=non_null`,
   `spring.jackson.deserialization.fail-on-unknown-properties=true`,
   `spring.jackson.datatype.enum.write-enums-using-to-string=false`,
   `spring.jackson.datatype.datetime.*`. JSON parser and generator features
   (`JsonReadFeature`/`JsonWriteFeature`) are `spring.jackson.json.read.*`/`json.write.*`;
   `spring.jackson.read.*`/`write.*` now take the format-neutral `StreamReadFeature`/`StreamWriteFeature`.
2. **Code**: a `JsonMapperBuilderCustomizer` bean.
3. **Replace entirely**: a `JsonMapper` bean (declared type `JsonMapper`).

**Never `@Bean ObjectMapper` in Boot 4.** Measured on 4.1.2: a bean declared as `ObjectMapper`
(even built with `JsonMapper.builder()`) leaves Boot's own `jacksonJsonMapper` in place, Spring MVC
keeps using Boot's, and your naming strategy, inclusion and modules silently do nothing. Add
`@Primary` and the context fails to start ("more than one 'primary' bean found among candidates:
[objectMapper, jacksonJsonMapper]").

`@WebMvcTest` slices pick up `@JacksonComponent` beans but not a `JsonMapperBuilderCustomizer` declared
in a `@Configuration` class (measured). Prefer properties for wire-format rules, or test the JSON
contract with `@SpringBootTest`.

### 3.3 Serializers for types you don't own

```java
@JacksonComponent
public class FareJsonComponent {
  public static class Serializer extends ValueSerializer<Fare> {
    @Override
    public void serialize(Fare fare, JsonGenerator gen, SerializationContext ctxt) {
      gen.writeStartObject();
      gen.writeStringProperty("value", fare.value().toPlainString());
      gen.writeStringProperty("currency", fare.currency().getCurrencyCode());
      gen.writeEndObject();
    }
  }

  public static class Deserializer extends ValueDeserializer<Fare> {
    @Override
    public Fare deserialize(JsonParser p, DeserializationContext ctxt) {
      JsonNode node = ctxt.readTree(p);
      JsonNode value = node.get("value");
      JsonNode currency = node.get("currency");
      if (value == null || !value.isString() || currency == null || !currency.isString()) {
        return ctxt.reportInputMismatch(Fare.class, "expected {\"value\": \"..\", \"currency\": \"..\"}");
      }
      try {
        return Fare.of(value.asString(), currency.asString());
      } catch (IllegalArgumentException e) {
        return ctxt.reportInputMismatch(Fare.class, "invalid fare: %s", e.getMessage());
      }
    }
  }
}
```

Imports: `tools.jackson.core.{JsonGenerator,JsonParser}`, `tools.jackson.databind.*`. An exception
thrown inside a deserializer becomes `HttpMessageNotReadableException` and a 400 (measured, even a
bare `IllegalArgumentException`), but reporting a mismatch gives a clear message. Money-like values
go out as strings so JavaScript clients don't lose cents. When you can annotate the type,
`@JsonValue`/`@JsonCreator` (or a `@JacksonMixin` for types you can't edit) is often enough.

### 3.4 Jackson 3 defaults that change the wire format silently

Measured on Boot 4.1.2, default settings versus the same app with
`spring.jackson.use-jackson2-defaults=true`; the enum and primitive rows were also confirmed on a
real Boot 3.5.16 build:

| Input or output | Jackson 2 behaviour (Boot 3.5) | Boot 4 / Jackson 3 defaults |
| --- | --- | --- |
| enum with an overridden `toString()`, written | `"DELAYED"` (name) | `"Running late"` (toString) |
| same enum, read | name accepted, label rejected | **name rejected (400)**, label accepted |
| record/POJO with `boolean`/`int` property missing from the body | `false`/`0` | **400** (`FAIL_ON_NULL_FOR_PRIMITIVES`) |
| explicit `null` for a primitive | `0` | **400** |
| trailing content after the JSON value | ignored | **400** (`FAIL_ON_TRAILING_TOKENS`) |
| property order of a getter-based class | declaration order | alphabetical (records keep component order) |
| `java.util.Date` | `"1970-01-01T00:00:00.000+00:00"` | `"1970-01-01T00:00:00.000Z"` |
| unknown properties | accepted (Boot default) | accepted (Boot default) |
| `Instant`, `LocalDate`, `Duration` | ISO strings (Boot disabled timestamps) | ISO strings, nanoseconds kept |

On an upgrade, either restore the old behaviour per feature (preferred, explicit):

```java
@Bean
JsonMapperBuilderCustomizer keepJackson2WireFormat() {
  return builder -> builder
      .disable(EnumFeature.WRITE_ENUMS_USING_TO_STRING)
      .disable(EnumFeature.READ_ENUMS_USING_TO_STRING)
      .disable(DeserializationFeature.FAIL_ON_NULL_FOR_PRIMITIVES);
}
```

or the same as properties (`spring.jackson.datatype.enum.write-enums-using-to-string=false`,
`spring.jackson.datatype.enum.read-enums-using-to-string=false`,
`spring.jackson.deserialization.fail-on-null-for-primitives=false`, all measured), or set
`spring.jackson.use-jackson2-defaults=true` and remove it once clients are checked. Do not
"fix" a toString-based enum by deleting the `toString()` override: other code uses it. Details and
the full rename table: [references/jackson-3.md](references/jackson-3.md).

## 4. Validation and error responses

### 4.1 Let Spring MVC validate; no class-level `@Validated` on controllers

Put constraints straight on handler parameters. Spring MVC (since Framework 6.1) validates them itself:

```java
@RestController
class JourneyController {
  @GetMapping("/journeys")
  JourneyPage search(@RequestParam(defaultValue = "0") @Min(0) int page,
                     @RequestParam(defaultValue = "25") @Min(1) @Max(200) int limit) { ... }

  @PostMapping("/stations/{stationCode}/departures")
  Departure add(@PathVariable @Pattern(regexp = "[A-Z]{3}") String stationCode,
                @Valid @RequestBody NewDeparture body) { ... }
}
```

| Situation (measured) | Exception | Default response |
| --- | --- | --- |
| constraint on `@RequestParam`/`@PathVariable`, no class `@Validated` | `HandlerMethodValidationException` | 400 |
| same method also has `@Valid @RequestBody`, both invalid | **one** `HandlerMethodValidationException` with parameter and body errors | 400 |
| `@Valid @RequestBody` on a method with no other constrained parameter | `MethodArgumentNotValidException` | 400 |
| body is a `List<@Valid Leg>` or `@Valid List<Leg>` | `HandlerMethodValidationException` | 400 |
| **class-level `@Validated`** + constrained parameter | `ConstraintViolationException` from the AOP proxy | **500** |
| class-level `@Validated`, invalid parameter and invalid body | `MethodArgumentNotValidException` only: **parameter errors lost** | 400 |
| non-numeric `limit=abc` | `MethodArgumentTypeMismatchException` | 400 |
| malformed JSON, missing primitive, wrong enum | `HttpMessageNotReadableException` | 400 |

The class-level `@Validated` answer is everywhere in older material. With it, Spring MVC skips its
own method validation, the AOP interceptor throws `ConstraintViolationException` (a 500 unless you
map it), and the body is validated first and alone. Keep `@Validated` for `@Service` beans and
`@ConfigurationProperties`, not controllers.

### 4.2 Problem details (RFC 9457)

- `spring.mvc.problemdetails.enabled=true` (default `false`) registers Boot's
  `ProblemDetailsExceptionHandler`: every Spring MVC exception becomes `application/problem+json`
  with `type`, `title`, `status`, `detail`, `instance`. The default details are terse
  (`"Validation failure"`, `"Invalid request content."`) and list no fields.
- To add fields, **extend `ResponseEntityExceptionHandler`** in a `@RestControllerAdvice` and
  override `handleMethodArgumentNotValid` and `handleHandlerMethodValidationException`. Boot's
  handler backs off when such a bean exists, and you keep problem details for all other exceptions.
- Trap (measured): with the property on, a plain `@RestControllerAdvice` with
  `@ExceptionHandler(MethodArgumentNotValidException.class)` never runs, because Boot's ordered
  handler answers first. Extend `ResponseEntityExceptionHandler`, or give your advice
  `@Order(Ordered.HIGHEST_PRECEDENCE)`.

```java
@RestControllerAdvice
class ApiProblems extends ResponseEntityExceptionHandler {
  @Override
  protected ResponseEntity<Object> handleHandlerMethodValidationException(
      HandlerMethodValidationException ex, HttpHeaders headers, HttpStatusCode status, WebRequest request) {
    List<Map<String, String>> errors = new ArrayList<>();
    for (ParameterValidationResult result : ex.getParameterValidationResults()) {
      if (result instanceof ParameterErrors body) {          // a @Valid @RequestBody / @ModelAttribute
        body.getFieldErrors().forEach(e -> errors.add(Map.of("field", e.getField(), "message", e.getDefaultMessage())));
      } else {                                                // @RequestParam, @PathVariable, @RequestHeader
        String name = result.getMethodParameter().getParameterName();
        result.getResolvableErrors().forEach(e -> errors.add(Map.of("field", name, "message", e.getDefaultMessage())));
      }
    }
    ProblemDetail problem = ex.getBody();
    problem.setProperty("errors", errors);
    return handleExceptionInternal(ex, problem, headers, status, request);
  }
  // handleMethodArgumentNotValid: same, from ex.getBindingResult().getFieldErrors()
}
```

`FieldError.getField()` is already a property path (`legs[1].fare`). `getParameterName()` needs
`-parameters`, which `spring-boot-starter-parent` turns on; with an explicit
`@RequestParam("max-results")` use the annotation's name (or `ex.visitResults(...)`). Full recipe,
ordering and message customization: [references/validation-and-problem-details.md](references/validation-and-problem-details.md).

## 5. Tests on Boot 4

| Need | Boot 4 |
| --- | --- |
| mock a bean | `@MockitoBean` / `@MockitoSpyBean` (`org.springframework.test.context.bean.override.mockito`); `@MockBean`/`@SpyBean` are removed |
| MVC slice | `@WebMvcTest` from `org.springframework.boot.webmvc.test.autoconfigure` |
| MockMvc in `@SpringBootTest` | add `@AutoConfigureMockMvc` (same package); no longer implicit |
| AssertJ-style MockMvc | `MockMvcTester` (`org.springframework.test.web.servlet.assertj`), autowirable where MockMvc is |
| real HTTP client in tests | `RestTestClient` (`org.springframework.test.web.servlet.client`) + `@AutoConfigureRestTestClient` |
| keep `TestRestTemplate` | `org.springframework.boot.resttestclient.TestRestTemplate` + `@AutoConfigureTestRestTemplate` |
| port | `@LocalServerPort` (`org.springframework.boot.test.web.server`, unchanged) |

Spring caches one context per configuration, so state written by one test class (an in-memory
store) is visible to the next. Don't assert global counts; assert on what the test created.
Mockito prints a self-attach warning on JDK 25; it is harmless today.
More in [references/testing.md](references/testing.md).

## 6. Clients, versioning, resilience, threads

- **`RestTemplateBuilder`** moved to `org.springframework.boot.restclient` (needs the restclient
  starter), and `setConnectTimeout`/`setReadTimeout` are gone: use `connectTimeout(Duration)` and
  `readTimeout(Duration)`. Prefer `RestClient` for new code.
- **HTTP service clients**: `@ImportHttpServices(group = "routing", types = RoutingApi.class)` on a
  `@Configuration`, interfaces with `@HttpExchange`/`@GetExchange`, settings per group under
  `spring.http.serviceclient.routing.*` (`base-url` measured; `connect-timeout`, `read-timeout`
  from the property metadata). Global client settings moved from `spring.http.client.*` to
  `spring.http.clients.*`.
- **API versioning** (`spring.mvc.apiversion.*`, `@GetMapping(path = "/x", version = "2.0")`):
  configuring `use.header` without `default` makes **every** request without the header a 400,
  including endpoints that are not versioned (measured). Set `spring.mvc.apiversion.default` or
  `required=false`. Versions parse semantically: `2` matches `2.0`.
- **Retries**: Framework 7 has `@Retryable` and `@ConcurrencyLimit`
  (`org.springframework.resilience.annotation`, enable with `@EnableResilientMethods`) and
  `RetryTemplate`/`RetryPolicy` in `org.springframework.core.retry`. Spring Retry has no managed
  version in Boot 4. `@Retryable(maxRetries = 3)` means up to 4 calls, then the last exception is
  rethrown (measured). It is proxy-based: self-invocation is not retried.
- **Virtual threads**: `spring.threads.virtual.enabled=true` runs requests on virtual threads
  (measured: `tomcat-handler-N`, `isVirtual()` true).

Details: [references/http-and-resilience.md](references/http-and-resilience.md).

## 7. Upgrading a 3.5 service to 4.x

1. Get to the latest 3.5.x first with no deprecation warnings; `@MockitoBean` works there already.
2. Bump the parent, then swap starters (section 2), adding each technology's test starter.
3. Fix compile errors package by package: Jackson (3.1), test annotations (section 5),
   `RestTemplateBuilder`, moved Boot classes. Use `javap`/`unzip -l` on jars in the local repository
   to find a moved class instead of guessing.
4. **Then diff behaviour, not just compilation.** Record a few real responses and requests on 3.5
   (enums, omitted booleans, dates, nulls, error bodies) and replay them on 4. Jackson 3 changes
   them without a single compile error (3.4).
5. Rename properties (`spring.http.client.*`, `spring.jackson.read/write.*`, others in the
   reference). Run with `spring-boot-properties-migrator` on the classpath once to list them.
6. Keep every existing test; port, don't delete.

Checklist with all renames: [references/upgrade-from-3.md](references/upgrade-from-3.md).

## Review checklist

- [ ] Starters match the technologies used, and each has its `-test` starter where tests need it.
- [ ] No `com.fasterxml.jackson.databind`/`core` imports; annotations stay `com.fasterxml.jackson.annotation`.
- [ ] JSON is configured through properties, `JsonMapperBuilderCustomizer` or a `JsonMapper` bean, never `@Bean ObjectMapper`.
- [ ] Enums with a custom `toString()`, primitive request fields and dates have been checked against the published contract.
- [ ] Controllers carry no class-level `@Validated`; constraints sit on parameters and `@Valid` bodies.
- [ ] Both `MethodArgumentNotValidException` and `HandlerMethodValidationException` produce the same error format, and a request with bad parameters and a bad body reports both.
- [ ] Error responses are `application/problem+json`, either via the property or a `ResponseEntityExceptionHandler` subclass, not both fighting.
- [ ] Tests use `@MockitoBean`, Boot 4 test packages, and opt in to MockMvc/TestRestTemplate/RestTestClient explicitly.
- [ ] API versioning, if enabled, has a default or is optional for unversioned endpoints.

## Anti-patterns

- `@Bean ObjectMapper objectMapper()` → ignored by MVC in Boot 4; with `@Primary`, startup failure.
- `@JsonComponent` + `extends JsonSerializer<T>` → doesn't compile on 4; use `@JacksonComponent` + `ValueSerializer<T>`.
- Adding `jackson-databind` 2.x or `spring-boot-jackson2` to make old code compile → two JSON stacks, deprecated support, and Spring MVC still uses Jackson 3.
- `@Validated` on a `@RestController` → 500s for invalid parameters, parameter errors dropped when the body is also invalid.
- Handling only `MethodArgumentNotValidException` → parameter violations come back without field details.
- A plain `@ExceptionHandler(MethodArgumentNotValidException.class)` plus `spring.mvc.problemdetails.enabled=true` → your handler never runs.
- `@MockBean` → removed. `@SpringBootTest` + `@Autowired MockMvc` without `@AutoConfigureMockMvc` → no bean.
- `spring-retry` with no version → unresolvable in Boot 4; use Framework 7 `@Retryable`.
- `spring.mvc.apiversion.use.header` without a default → every unversioned request is a 400.

## More

- [references/jackson-3.md](references/jackson-3.md): Jackson 2 to 3 renames, Boot properties, defaults, serializer recipes.
- [references/validation-and-problem-details.md](references/validation-and-problem-details.md): validation exceptions, the full error-format handler, messages.
- [references/testing.md](references/testing.md): Boot 4 test annotations, slices, MockMvcTester, RestTestClient.
- [references/upgrade-from-3.md](references/upgrade-from-3.md): starters, modules, packages and properties that moved.
- [references/http-and-resilience.md](references/http-and-resilience.md): RestClient, HTTP service groups, API versioning, retries, virtual threads.
- [references/sources.md](references/sources.md): documentation and measurements behind every claim.
