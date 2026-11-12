---
name: spring-jooq
description: "Spring Boot + jOOQ — 타입 세이프 SQL 빌더, 코드 생성(Flyway·Testcontainers), MULTISET, Window Function·CTE, Keyset Pagination. Use when JPA 대신 SQL 중심으로 jOOQ 쿼리를 작성하거나 설정할 때."
---

# Spring Boot + jOOQ Patterns

jOOQ (Java Object Oriented Querying) — 타입 세이프 SQL 빌더 + 코드 생성. JPA 대신 SQL 중심 개발.

## Quick Reference

```
데이터 액세스 기술 선택
    │
    ├─ 단순 CRUD ──────────> Spring Data JPA (/java:spring-data)
    │
    ├─ 복잡한 SQL/분석 쿼리 ──> jOOQ (이 스킬)
    │
    ├─ SQL 완전 제어 + 타입 세이프 ──> jOOQ
    │
    └─ JPA + 복잡한 쿼리 혼용 ──> JPA + jOOQ 조합

jOOQ vs JPA/QueryDSL
    ├─ jOOQ: SQL 중심, DB-first, Window Function/CTE/MULTISET 지원
    ├─ JPA:  객체 중심, Code-first, 1차 캐시/Lazy Loading
    └─ QueryDSL: JPA 보조, JPQL 빌더 (SQL 직접 제어 불가)
```

---

## Spring Boot 설정

### Gradle (build.gradle.kts)

```kotlin
plugins {
    id("org.jooq.jooq-codegen-gradle") version "3.19.15"
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-jooq")
    jooqCodegen("org.postgresql:postgresql")
    jooqCodegen("org.testcontainers:postgresql")
    jooqCodegen("org.flywaydb:flyway-database-postgresql")
}
```

### Maven (testcontainers-jooq-codegen 플러그인)

```xml
<plugin>
    <groupId>org.testcontainers</groupId>
    <artifactId>jooq-testcontainers-codegen-maven-plugin</artifactId>
    <version>0.0.4</version>
    <configuration>
        <database><type>POSTGRES</type>
            <containerImage>postgres:16-alpine</containerImage></database>
        <flyway><locations>filesystem:src/main/resources/db/migration</locations></flyway>
        <jooq><generator><database>
            <inputSchema>public</inputSchema>
        </database><target>
            <packageName>com.example.jooq</packageName>
            <directory>target/generated-sources/jooq</directory>
        </target></generator></jooq>
    </configuration>
</plugin>
```

### application.yml

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: app
    password: ${DB_PASSWORD}
  jooq:
    sql-dialect: postgres
```

---

## 코드 생성 (Flyway + Testcontainers)

```
워크플로우: DB 마이그레이션 → Testcontainers로 임시 DB → jOOQ 코드 생성 → 컴파일
  1. Flyway가 마이그레이션 스크립트 실행
  2. Testcontainers가 PostgreSQL 컨테이너 자동 시작
  3. jOOQ가 스키마에서 Java 클래스 생성
  4. 빌드 시 항상 DB 스키마와 동기화 보장
```

### Gradle 코드 생성 설정

```kotlin
jooq {
    configuration {
        jdbc {
            driver = "org.testcontainers.jdbc.ContainerDatabaseDriver"
            url = "jdbc:tc:postgresql:16-alpine:///test?TC_TMPFS=/testtmpfs:rw"
        }
        generator {
            database {
                name = "org.jooq.meta.postgres.PostgresDatabase"
                inputSchema = "public"
                includes = ".*"
                excludes = "flyway_schema_history"
            }
            generate {
                isRecords = true
                isPojos = true
                isPojosAsJavaRecordClasses = true  // Java 16+ record 생성
                isFluentSetters = true
            }
            target {
                packageName = "com.example.jooq"
                directory = "build/generated-sources/jooq"
            }
        }
    }
}
```

---

## Repository 패턴 (권장)

```java
@Repository
@RequiredArgsConstructor
public class UserRepository {
    private final DSLContext dsl;

    // CREATE
    public UserRecord insert(String name, String email) {
        return dsl.insertInto(USERS, USERS.NAME, USERS.EMAIL)
            .values(name, email)
            .returning()
            .fetchOne();
    }

    // READ (단건)
    public Optional<UserRecord> findById(Long id) {
        return dsl.selectFrom(USERS)
            .where(USERS.ID.eq(id))
            .fetchOptional();
    }

    // READ (목록 + 동적 조건)
    public List<UserRecord> search(String name, Status status, int limit) {
        return dsl.selectFrom(USERS)
            .where(trueCondition()
                .and(name != null ? USERS.NAME.containsIgnoreCase(name) : noCondition())
                .and(status != null ? USERS.STATUS.eq(status) : noCondition()))
            .orderBy(USERS.CREATED_AT.desc())
            .limit(limit)
            .fetch();
    }

    // UPDATE
    public int update(Long id, String name) {
        return dsl.update(USERS)
            .set(USERS.NAME, name)
            .set(USERS.UPDATED_AT, LocalDateTime.now())
            .where(USERS.ID.eq(id))
            .execute();
    }

    // DELETE
    public int delete(Long id) {
        return dsl.deleteFrom(USERS)
            .where(USERS.ID.eq(id))
            .execute();
    }

    // UPSERT (INSERT ... ON CONFLICT)
    public UserRecord upsert(String email, String name) {
        return dsl.insertInto(USERS, USERS.EMAIL, USERS.NAME)
            .values(email, name)
            .onConflict(USERS.EMAIL)
            .doUpdate()
            .set(USERS.NAME, name)
            .returning()
            .fetchOne();
    }
}
```

---

## MULTISET (N+1 없는 중첩 컬렉션, jOOQ 3.15+)

```java
// JPA의 @OneToMany + fetch join 대체 — 단일 쿼리로 중첩 컬렉션 조회
record AuthorDto(String name, List<BookDto> books, List<String> tags) {}
record BookDto(String title, int year) {}

List<AuthorDto> result = dsl
    .select(
        AUTHOR.NAME,
        multiset(
            select(BOOK.TITLE, BOOK.PUBLISHED_YEAR)
            .from(BOOK)
            .where(BOOK.AUTHOR_ID.eq(AUTHOR.ID))
        ).as("books").convertFrom(r -> r.map(mapping(BookDto::new))),
        multiset(
            select(TAG.NAME)
            .from(AUTHOR_TAG).join(TAG).on(AUTHOR_TAG.TAG_ID.eq(TAG.ID))
            .where(AUTHOR_TAG.AUTHOR_ID.eq(AUTHOR.ID))
        ).as("tags").convertFrom(r -> r.map(Record1::value1))
    )
    .from(AUTHOR)
    .fetch(mapping(AuthorDto::new));
```

---

## Window Functions & CTE

```java
// Window Function — 부서별 급여 순위
dsl.select(
        EMPLOYEE.NAME,
        EMPLOYEE.SALARY,
        EMPLOYEE.DEPARTMENT_ID,
        rowNumber().over(partitionBy(EMPLOYEE.DEPARTMENT_ID)
            .orderBy(EMPLOYEE.SALARY.desc())).as("rank")
    )
    .from(EMPLOYEE)
    .fetch();

// CTE (Common Table Expression)
var monthlySales = name("monthly_sales").fields("month", "total")
    .as(select(ORDERS.ORDER_DATE.cast(SQLDataType.DATE), sum(ORDERS.AMOUNT))
        .from(ORDERS)
        .groupBy(ORDERS.ORDER_DATE.cast(SQLDataType.DATE)));

dsl.with(monthlySales)
    .select()
    .from(monthlySales)
    .where(field(name("total"), BigDecimal.class).gt(BigDecimal.valueOf(10000)))
    .fetch();
```

---

## Batch Operations

```java
// 방법 1: Batch with bind (JDBC batch)
dsl.batch(
    dsl.insertInto(USERS, USERS.NAME, USERS.EMAIL)
        .values((String) null, null))
    .bind("Alice", "alice@test.com")
    .bind("Bob", "bob@test.com")
    .bind("Charlie", "charlie@test.com")
    .execute();

// 방법 2: Bulk INSERT (multi-row VALUES)
var insert = dsl.insertInto(USERS, USERS.NAME, USERS.EMAIL);
for (var u : userList) {
    insert = insert.values(u.name(), u.email());
}
insert.execute();

// 방법 3: COPY API (PostgreSQL, 대량 적재 시 가장 빠름)
dsl.loadInto(USERS)
    .loadCSV(csvInputStream, StandardCharsets.UTF_8)
    .fields(USERS.NAME, USERS.EMAIL)
    .execute();
```

---

## Keyset Pagination (Seek Method)

```java
// OFFSET 방식 대비 상수 시간 성능 — 대용량 데이터 필수
public List<ProductRecord> fetchPage(Long lastId, int size) {
    var query = dsl.selectFrom(PRODUCT)
        .orderBy(PRODUCT.ID.asc())
        .limit(size);

    if (lastId != null) {
        query = dsl.selectFrom(PRODUCT)
            .orderBy(PRODUCT.ID.asc())
            .seek(lastId)
            .limit(size);
    }
    return query.fetch();
}

// 복합 정렬 Seek
dsl.selectFrom(PRODUCT)
    .orderBy(PRODUCT.SCORE.desc(), PRODUCT.ID.asc())
    .seek(949, 15)  // 마지막으로 본 score=949, id=15
    .limit(20)
    .fetch();
```

---

## Transaction Management

```java
// Spring @Transactional 사용 (권장)
@Service
@RequiredArgsConstructor
public class OrderService {
    private final DSLContext dsl;

    @Transactional
    public void placeOrder(Long userId, List<OrderItem> items) {
        var order = dsl.insertInto(ORDERS, ORDERS.USER_ID, ORDERS.STATUS)
            .values(userId, "PENDING")
            .returning().fetchOne();

        for (var item : items) {
            dsl.insertInto(ORDER_ITEMS, ORDER_ITEMS.ORDER_ID,
                    ORDER_ITEMS.PRODUCT_ID, ORDER_ITEMS.QUANTITY)
                .values(order.getId(), item.productId(), item.quantity())
                .execute();
        }

        dsl.update(PRODUCTS)
            .set(PRODUCTS.STOCK, PRODUCTS.STOCK.minus(
                select(ORDER_ITEMS.QUANTITY).from(ORDER_ITEMS)
                    .where(ORDER_ITEMS.ORDER_ID.eq(order.getId()))
                    .and(ORDER_ITEMS.PRODUCT_ID.eq(PRODUCTS.ID))))
            .where(PRODUCTS.ID.in(items.stream().map(OrderItem::productId).toList()))
            .execute();
    }

    @Transactional(readOnly = true)
    public List<OrderRecord> findByUser(Long userId) {
        return dsl.selectFrom(ORDERS)
            .where(ORDERS.USER_ID.eq(userId))
            .fetch();
    }
}
```

---

## R2DBC Reactive (jOOQ 3.17+)

```java
// Spring WebFlux + jOOQ R2DBC
@Bean
public DSLContext reactiveDsl(ConnectionFactory cf) {
    return DSL.using(cf, SQLDialect.POSTGRES);
}

Flux<UserRecord> users = Flux.from(
    dsl.selectFrom(USERS).where(USERS.STATUS.eq("ACTIVE")));

// Reactive 트랜잭션
Flux<?> result = Flux.from(dsl.transactionPublisher(trx ->
    Flux.from(trx.dsl()
        .insertInto(ORDERS).columns(ORDERS.USER_ID).values(userId))
    .thenMany(trx.dsl()
        .update(USERS).set(USERS.ORDER_COUNT, USERS.ORDER_COUNT.plus(1))
        .where(USERS.ID.eq(userId)))
));
```

---

## ExecuteListener (슬로우 쿼리 감지)

```java
@Bean
public DefaultConfigurationCustomizer jooqCustomizer() {
    return c -> c.set(new DefaultExecuteListenerProvider(new SlowQueryListener()));
}

public class SlowQueryListener extends DefaultExecuteListener {
    private StopWatch watch;

    @Override
    public void executeStart(ExecuteContext ctx) { watch = new StopWatch(); }

    @Override
    public void executeEnd(ExecuteContext ctx) {
        long millis = watch.split();
        if (millis > 3000) {
            log.warn("Slow query ({}ms): {}", millis, ctx.query());
        }
    }
}
```

---

## Multitenancy (스키마 기반)

```java
@Bean
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public DSLContext tenantDsl(DataSource ds, TenantContext tenantCtx) {
    var settings = new Settings()
        .withRenderMapping(new RenderMapping()
            .withSchemata(new MappedSchema()
                .withInput("public")
                .withOutput(tenantCtx.getSchema())));  // tenant_abc
    return DSL.using(ds, SQLDialect.POSTGRES, settings);
}
```

---

## Custom Converter

```java
// Converter: DB jsonb ↔ Java Object
public class JsonbConverter implements Converter<JSONB, UserProfile> {
    private static final ObjectMapper mapper = new ObjectMapper();
    @Override public UserProfile from(JSONB db) {
        return db == null ? null : mapper.readValue(db.data(), UserProfile.class);
    }
    @Override public JSONB to(UserProfile obj) {
        return obj == null ? null : JSONB.valueOf(mapper.writeValueAsString(obj));
    }
    @Override public Class<JSONB> fromType() { return JSONB.class; }
    @Override public Class<UserProfile> toType() { return UserProfile.class; }
}

// 코드 생성에 등록 (forcedType)
// generator > database > forcedTypes:
//   - userType: com.example.UserProfile
//     converter: com.example.JsonbConverter
//     includeExpression: ".*\.profile"
```

---

## Testing

```java
// @JooqTest 슬라이스 테스트 (Spring Boot)
@JooqTest
@AutoConfigureTestDatabase(replace = NONE)
@Testcontainers
class UserRepositoryTest {
    @Container
    static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine")
        .withInitScript("schema.sql");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", pg::getJdbcUrl);
        r.add("spring.datasource.username", pg::getUsername);
        r.add("spring.datasource.password", pg::getPassword);
    }

    @Autowired DSLContext dsl;

    @Test
    void insertAndFind() {
        dsl.insertInto(USERS, USERS.NAME, USERS.EMAIL)
            .values("Test", "test@test.com").execute();

        var user = dsl.selectFrom(USERS)
            .where(USERS.EMAIL.eq("test@test.com")).fetchOne();
        assertThat(user.getName()).isEqualTo("Test");
    }
}

// MockDataProvider (유닛 테스트, DB 불필요)
var provider = ctx -> new MockResult[]{
    new MockResult(1, dsl.newResult(USERS.ID, USERS.NAME))
};
var mockDsl = DSL.using(new MockConnection(provider), SQLDialect.POSTGRES);
```

---

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| Generated DAO만 사용 | DSLContext 직접 사용 Repository | DAO는 단순 CRUD만 지원 |
| `fetchOne()` null 미처리 | `fetchOptional()` 사용 | NPE 방지 |
| OFFSET 페이징 대량 데이터 | Seek/Keyset 페이징 | OFFSET은 깊은 페이지에서 성능 저하 |
| 동적 조건에 문자열 연결 | `Condition` 조합 | SQL injection 방지 |
| 모든 필드 SELECT | 필요한 필드만 select | 네트워크/메모리 절약 |
| N+1 루프 쿼리 | MULTISET 또는 JOIN | 쿼리 수 최소화 |
| codegen 없이 문자열 SQL | 코드 생성 사용 | 컴파일 타임 검증 |

---

## 선택 기준

```
JPA가 적합한 경우              jOOQ가 적합한 경우
─────────────────            ─────────────────
단순 CRUD 위주                복잡한 분석 쿼리
객체 그래프 탐색 많음          SQL 완전 제어 필요
1차 캐시 활용                 Window Function, CTE, MULTISET
Hibernate 생태계 활용         DB 벤더 특화 기능 (PostgreSQL jsonb 등)
```

**관련 skill**: `/java:spring-data`, `/java:spring-testcontainers`, `/infra:database`, `/infra:database-migration`
