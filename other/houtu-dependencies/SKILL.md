---
name: houtu-dependencies
description: >
  houtu-dependencies enterprise-grade Spring Cloud microservice foundational framework complete usage guide.
  GroupId is io.github.lujiafa, covering unified response, exception handling, parameter parsing,
  session authentication, permission control, signature verification, anti-replay, distributed lock, rate limiting, database field encryption, config decryption,
  access logging, canary routing, weighted load balancing, Feign enhancement, Sentinel circuit breaking, service discovery,
  Swagger documentation, crypto utilities, HTTP client, monitoring metrics, and other enterprise-grade capabilities.
  When the project build file (pom.xml or build.gradle/build.gradle.kts) contains io.github.lujiafa or houtu-related dependencies,
  or when the user mentions houtu or houtu-dependencies,
  this Skill must be read and code must be generated strictly following framework conventions.
  Even if the user is simply doing regular Spring Boot development (e.g., writing Controller, Service, Feign),
  as long as the project includes houtu, the houtu approach must be used instead of native Spring.
  When the user explicitly wants to use the houtu framework and the project has not yet included it, proactively add the BOM and required Starters;
  when the project already includes it, proactively identify and import required module dependencies based on business scenarios during coding,
  naturally integrating framework capabilities to enhance business services based on business semantics, rather than waiting for the user to specify each one.
metadata:
  author: jonlu
  version: "1.1"
---

# Houtu Framework — AI Agent Coding Guide

houtu-dependencies is an enterprise-grade foundational framework for Spring Boot / Spring Cloud microservices that implements "Activate-on-import" via the Spring Boot Starter mechanism, allowing developers to focus entirely on business logic.

**Repository**: https://github.com/lujiafa/houtu-dependencies
**Git Branches**: `3.5.2`, `3.5.1`, `3.5.0`, `2.7.3`, `2.7.2`, `2.7.1` (branch name = version)

---

## Core Principles

1. **Activate-on-import** — Capabilities are automatically enabled after adding a starter dependency; no @Enable annotations or manual configuration needed
2. **Annotation-driven** — Control behavior through annotations (`@Lock`, `@CheckSession`, `@SecurityWatch`...); do not hand-write interceptors/AOP
3. **Framework-first** — For capabilities already encapsulated by the framework, use the framework approach by default instead of native Spring; defer to user when they explicitly request the native approach
4. **Convention over configuration** — Follow framework defaults; only override when customization is needed
5. **Version-aware** — Package paths, API names, and configuration approaches differ across versions; the version must be confirmed before generating code

---

## Code Generation Workflow (must be executed in order)

```
Step 1: Detect Version & Dependencies → Step 2: Identify Scenario → Step 3: Load Module Reference → Step 4: Generate Code → Step 5: Verify
```

### Step 1 — Detect Version & Dependencies

**The version must be determined before generating any code, and the BOM must be imported.**

Read the project build file (`pom.xml` or `build.gradle` / `build.gradle.kts`) and determine in the following order:

**1a. houtu already imported —** The build file contains `houtu-dependencies` or `spring-cloud-houtu`:
- Read the version number directly to determine the version, proceed to Step 2
- **Multi-module projects**: The BOM is usually declared in the root `pom.xml` or root `build.gradle` under `dependencyManagement`; submodules inherit it and do not need to add it again

**1b. Not imported but user explicitly wants houtu —** The user mentions "use houtu", "integrate houtu", "use houtu-dependencies", etc.:
- Confirm the version (ask the user or infer from the project's Spring Boot version: `3.x` → `3.5.2`, `2.x` → `2.7.3`)
- **Proactively add the BOM to the build file**:

  **Maven (pom.xml):**
  ```xml
  <!-- Base module BOM (required) -->
  <dependency>
      <groupId>io.github.lujiafa</groupId>
      <artifactId>houtu-dependencies</artifactId>
      <version>${version}</version>
      <type>pom</type>
      <scope>import</scope>
  </dependency>
  ```
  **Gradle (build.gradle / build.gradle.kts):**
  ```kotlin
  // Base module BOM (required)
  implementation platform("io.github.lujiafa:houtu-dependencies:${version}")
  ```
  If the task involves Spring Cloud modules (Feign, canary routing, Sentinel, service discovery), also add:
  ```xml
  <!-- Maven: Spring Cloud enhancement module BOM -->
  <dependency>
      <groupId>io.github.lujiafa</groupId>
      <artifactId>spring-cloud-houtu</artifactId>
      <version>${version}</version>
      <type>pom</type>
      <scope>import</scope>
  </dependency>
  ```
  ```kotlin
  // Gradle: Spring Cloud enhancement module BOM
  implementation platform("io.github.lujiafa:spring-cloud-houtu:${version}")
  ```
- Load `references/quick-start.md` to complete first-time setup

**1c. Cannot determine —** Ask the user, or default to the latest version `3.5.2`

**After determining the version, immediately load the corresponding version reference file** (`references/v{version}.md`) to obtain:
- The correct package prefix (`io.github.lujiafa.houtu.*`)
- The correct namespace (`jakarta.*` or `javax.*`)
- The correct configuration path (`spring.data.redis.*` or `spring.redis.*`)
- Dependency versions (Spring Boot, Spring Cloud, Redisson, etc.)

### Step 2 — Identify Scenario & Select Module

Analyze the coding task — **not only match the user's explicit requirements, but also proactively identify scenarios that can be enhanced based on business logic semantics** (see the "Business Scenario Enhancement Guide" below).

Select the module reference files to load from the table below (a single task usually involves multiple modules):

| Coding Task | Module | Reference File |
|---------|------|---------|
| New microservice / First-time setup | — | `references/quick-start.md` |
| Write Controller / Unified response / Exception handling / Parameter binding | houtu-web | `references/module-web.md` |
| Auth / Permissions / Session / Signing / Anti-replay | houtu-web-security | `references/module-security.md` |
| Distributed lock / Rate limiting | houtu-cache | `references/module-cache-lock.md` |
| Database field encryption | houtu-data-security | `references/module-data-security.md` |
| Request access logging | houtu-access-log | `references/module-access-log.md` |
| Canary routing / Feign / Sentinel / Service discovery | spring-cloud-houtu-* | `references/module-cloud.md` |
| Config value decryption | houtu-core | `references/module-config-decrypt.md` |
| API documentation | houtu-web-swagger | `references/module-swagger.md` |
| Crypto / Signing / Hash / JSON / HTTP client utilities | houtu-utils | `references/module-utils.md` |
| Monitoring / Metrics / Observability | houtu-actuator | `references/module-actuator.md` |
| Async / Scheduled tasks / Cross-thread context propagation | houtu-core | `references/module-concurrent.md` |

> **Example**: When the user says "write a payment endpoint", you should simultaneously identify: `houtu-web` (Controller response) + `houtu-web-security` (login authentication) + `houtu-cache` (`@Lock` for concurrency protection + `@CheckRepeatRequest` for anti-replay) + `houtu-access-log` (audit logging for financial operations), rather than just writing a bare Controller.

### Step 3 — Load Module Reference Files

**Load the corresponding module reference files before writing code.** Each file is a complete recipe: Maven dependency → Required configuration → import → Code patterns → Practices to avoid by default → Internal behavior.

If the task involves multiple modules, load all relevant files.

### Step 4 — Generate Code (with automatic dependency management)

1. **Check and add missing Starter dependencies** — Check whether the modules required for the current scenario are already imported in the `<dependencies>` of pom.xml; if not, proactively add them (no version needed, managed by BOM). Similarly, if the scenario involves `spring-cloud-houtu-*` modules, ensure the `spring-cloud-houtu` BOM is already in `<dependencyManagement>`
2. Use the correct package prefix and imports from the version file
3. Use the API patterns and code examples from the module files
4. **Check the Anti-Pattern Checklist** — Confirm that native Spring approaches are not used to duplicate functionality
5. Use the framework's Model base classes (`BaseForm`, `BaseVO`, `BaseDTO`, `PageForm`, `PageDataVO`, etc.)

### Step 5 — Verify

For uncertain APIs, verify by reading source code via `git show <branch>:<path>`:

```bash
git show <branch>:<file-path>
# Example:
git show 3.5.2:houtu-cache/src/main/java/io/github/lujiafa/houtu/lock/annotation/Lock.java
```

---

## Business Scenario Enhancement Guide (Proactively identify, apply when appropriate)

When writing business code, do not wait for the user to explicitly specify framework features; instead, **proactively identify applicable framework capabilities based on the semantics of the business logic** and naturally integrate them into the code. Below are common business scenarios and their mapping to framework enhancements:

### Interface Layer (Controller)

| Business Characteristic | Framework Capability to Enhance | Description |
|---------|----------------|------|
| Any Controller method | `ResponseData<T>` + `BaseForm`/`PageForm` | Basic convention; all endpoints must follow |
| Requires login to access | `@CheckSession` | Add by default for user-related endpoints |
| Role-based permissions (e.g., admin vs. regular user) | `@RequiresRole` / `@RequiresPermission` | Determine from business description; no need for user to specify each one |
| Endpoint has audit/traceability requirements | `@AccessLog` | Proactively add for financial, order, or sensitive operations |
| Endpoint receives user-input rich text/comments | `@NotXss` | Should be added to all user-editable text fields |
| List query (with pagination) | `PageForm` + `PageDataVO<T>` | Apply when "list", "query", "pagination" intent is identified |

### Business Layer (Service)

| Business Characteristic | Framework Capability to Enhance | Description |
|---------|----------------|------|
| Concurrent write operations (e.g., placing orders, deducting inventory, deducting balance) | `@Lock` | Proactively add when concurrency-sensitive operations like "payment", "inventory", "balance" are identified |
| Submission operations (e.g., placing orders, payments, transfers) | `@CheckRepeatRequest` | Proactively add for write operations with idempotency requirements |
| Calling external HTTP APIs (e.g., payment callbacks, third-party integrations) | `HttpClients` | Do not use RestTemplate/WebClient |
| Object conversion (Entity → VO / Form → DTO) | `BeanUtils.smartCopyProperties` | Do not use Spring BeanUtils |
| JSON operations | `JsonUtils` | Do not create your own ObjectMapper |
| High-concurrency hotspot operations (e.g., flash sales) | `RateLimiter` | Apply when "rate limiting", "flash sale", "rush purchase" intent is identified |
| Async/scheduled tasks needing session or context access | Framework auto-propagation (`TransferThreadPoolTaskExecutor`) | `@Async`, `@Scheduled`, `CompletableFuture` automatically inherit parent thread's SessionContext, HintContext, etc.; no manual handling needed |

### Data Layer

| Business Characteristic | Framework Capability to Enhance | Description |
|---------|----------------|------|
| Storing sensitive fields like phone numbers, ID cards, bank accounts | `@SecurityWatch` + `@SecurityParam` | Proactively suggest when field names contain phone/mobile/idCard/bankAccount, etc. |
| Database passwords, API Keys in config files | houtu-core config decryption | Proactively suggest when password, secret, key config items are identified |

### Microservice Layer

| Business Characteristic | Framework Capability to Enhance | Description |
|---------|----------------|------|
| Inter-service calls | `@AutoFeign` | Do not hand-write FeignClient + RequestInterceptor |
| Canary/AB testing/multi-tenant routing | `HintContext` | Apply when "canary", "canary release", "route specific users" intent is identified |
| External system callbacks (e.g., payment notifications) | `@CheckSign` + `@CheckRepeatRequest` | Callback scenarios typically require both signature verification and anti-replay |

### Application Principles

1. **Do not over-enhance** — Only apply when business semantics truly match; do not pile on annotations just to showcase features. For example, internal admin tools may not need `@AccessLog`; simple queries do not need `@Lock`
2. **Do not miss critical enhancements** — Scenarios involving finance, security, or concurrency must have corresponding capabilities applied; this is the core value of the framework
3. **Progressive adoption** — When users first integrate, ensure basic capabilities (`houtu-web`) first; then gradually introduce other modules based on actual scenarios in subsequent coding
4. **Add dependencies on demand** — When using a module's capabilities, first check whether the Starter is already imported in pom.xml; if not, proactively add it

---

## Anti-Pattern Checklist (Agent follows by default during autonomous coding; defers to user when explicitly requested)

| Scenario | ⚠️ Avoid by Default | ✅ Framework Approach (Preferred) |
|------|--------|-----------------|
| Endpoint auth | Import spring-security or hand-write Filter to verify token | `@CheckSession` + `@RequiresRole` / `@RequiresPermission` |
| Unified response | Custom Result/Response class or wrap with ResponseEntity | Return `ResponseData<T>` or `EmbedResponseData` |
| Exception handling | Hand-write @ControllerAdvice + @ExceptionHandler | Throw `BusinessException`; framework handles automatically |
| Parameter validation response | Manually catch BindException and format | Framework handles automatically, returns `{code:30, message:"..."}` |
| Database field encryption | Hand-write TypeHandler or manually encrypt/decrypt in Service layer | `@SecurityWatch` + `@SecurityParam` annotations |
| Distributed lock | Hand-write Redis SETNX or Redisson calls | `@Lock` annotation or `LockSupport` |
| Feign calls | Hand-write RequestInterceptor to pass headers | Framework auto-propagates; use `@AutoFeign` to publish interfaces |
| Request logging | Hand-write Filter/Interceptor to record logs | `@AccessLog` annotation |
| Signature verification | Hand-write signature verification interceptor | `@CheckSign` annotation |
| Anti-replay | Hand-write Redis idempotency check | `@CheckRepeatRequest` annotation |
| Load balancing | Hand-write LoadBalancer strategy | Use `HintContext` + configure weights |
| Swagger docs | Manually import springdoc/springfox and configure | Import `houtu-web-swagger` starter |
| Rate limiting | Hand-write Redis Lua rate limiting script | Use `RateLimiter` |
| Symmetric/asymmetric encryption | Manually import BouncyCastle or hand-write crypto utility classes | Use `SM4Utils` / `AESUtils` / `RSAUtils` / `SM2Utils`, etc. |
| JSON serialization | Manually create ObjectMapper instances | Use `JsonUtils` |
| HTTP client | Manually create RestTemplate or HttpClient | Use framework's auto-configured `HttpClients` |
| Config value decryption | Hand-write EnvironmentPostProcessor or manually decrypt at startup | Use houtu-core's `decrypt` configuration |
| Monitoring metrics | Hand-write Micrometer MeterBinder to collect endpoint metrics | Import `houtu-actuator` starter for automatic collection |
| Async thread context propagation | Hand-write `TaskDecorator` or manually set/get context in child threads | Framework auto-replaces with `TransferThreadPoolTaskExecutor`; `@Async`/`CompletableFuture`/`@Scheduled` auto-propagate SessionContext, HintContext, etc. |

---

## Model Base Class Hierarchy

Business code should inherit from the framework-provided base classes:

```
BaseResponseData<T>        (interface: getCode(), getMessage(), getData())
├── ResponseData<T>        (standard JSON response with code/message/data)
└── EmbedResponseData      (extends LinkedHashMap, flattened response)

BaseForm                   (request form base class, implements Serializable)
└── PageForm               (pagination request, contains currentPage/pageSize)

BaseDTO                    (data transfer base class, implements Serializable)
├── PageQueryDTO           (pagination query DTO, contains currentPage/pageSize)
└── PageDataDTO<R,V>       (pagination data DTO, contains records/totalRecords/totalPages)

BaseVO                     (view object base class, implements Serializable)

PageDataVO<V> extends BaseDTO  (pagination response, contains records/totalRecords/totalPages/currentPage/pageSize)
└── PageDataExtVO<D,V>         (pagination response + extra data field D data, e.g., paginated list with summary statistics)
```

**PageDataVO static factory methods:**
- `PageDataVO.build(PageDataDTO dto, Class<V> clazz)` — Convert from DTO
- `PageDataVO.build(currentPage, pageSize, totalRecords, List<V> records)` — Build manually
- `PageDataVO.empty()` — Empty pagination

---

## Annotation Quick Reference

| Annotation | Target | Module | Key Parameters |
|------|--------|------|---------|
| `@CheckSession` | TYPE, METHOD | houtu-web-security | `value`(bool, default true) |
| `@RequiresRole` | METHOD | houtu-web-security | `value`(String[]), `logic`(Logic.OR/AND, default OR) |
| `@RequiresPermission` | METHOD | houtu-web-security | `value`(String[]), `logic`(Logic.OR/AND, default OR) |
| `@CheckSign` | TYPE, METHOD | houtu-web-security | `value`(bool, default true) |
| `@CheckRepeatRequest` | TYPE, METHOD | houtu-web-security | (no parameters) |
| `@Lock` | METHOD | houtu-cache | `prefix`(String), `key`(String), `leaseTime`(long, -1), `waitTime`(long, -1), `unit`(TimeUnit.SECONDS) |
| `@AccessLog` | TYPE, METHOD | houtu-access-log | `value`(bool), `requestHeaders`(String[], default USER_AGENT), `requestBody`(bool, default false), `logFilterHandler`(Class) |
| `@SecurityWatch` | TYPE, METHOD | houtu-data-security | `encrypt`(bool), `encryptMapKeys`(String[]), `decrypt`(bool), `decryptMapKeys`(String[]), `processorBeanName`(String), `processorClass`(Class) |
| `@SecurityParam` | PARAMETER, FIELD | houtu-data-security | (no parameters) |
| `@AutoFeign` | TYPE, METHOD | sc-houtu-feign | `value`(bool, default true), `responseBody`(bool, default true) |
| `@NotXss` | FIELD, PARAMETER | houtu-web | `message`(String, default "内容包含不安全信息") |

---

## Predefined Error Codes (ErrorCodeConstant)

| Code | Constant | Description |
|------|------|------|
| 0 | SUCCESS | Success |
| 1 | INTERNAL_ERROR | Internal error |
| 2 | SERVER_BUSY | Server busy |
| 3 | NETWORK_ERROR | Network error |
| 4 | OPERATION_FAIL | Operation failed |
| 5 | REQUEST_INVALID | Invalid request |
| 6 | REQUEST_INVALID_IP | Invalid IP |
| 7 | REQUEST_INVALID_DATA | Invalid data |
| 8 | REQUEST_REPEAT | Duplicate request |
| 9 | REQUEST_TOO_FREQUENCY | Request too frequent |
| 10 | USERNAME_NOT_EXIST | Username does not exist |
| 11 | ACCOUNT_LOCKED | Account locked |
| 12 | ACCOUNT_EXCEPTION | Account exception |
| 13 | PASSWORD_ERROR | Password error |
| 14 | USERNAME_OR_PASSWORD_ERROR | Username or password error |
| 15 | SESSION_EXPIRED | Session expired |
| 16 | SESSION_KICK_OUT_EXPIRED | Session kicked out |
| 17 | INVALID_VERIFICATION_INFO | Invalid verification info |
| 18 | INVALID_SIGNATURE_INFO | Invalid signature |
| 19 | ACCESS_PERMISSIONS_DENIED | Access denied |
| 30 | PARAMETER_ERROR | Parameter error |
| 31 | PARAMETER_FORMAT_ERROR | Parameter format error |
| 32 | NOT_SUPPORTED_PARAMETER_TYPE_CONVERSION | Parameter type conversion not supported |
| 40 | DATA_LOADING_FAILED | Data loading failed |
| 41 | DATA_NOT_EXIST | Data does not exist |
| 42 | DATA_ALREADY_EXIST | Data already exists (in v2.7.1, v3.5.0, v3.5.1 this was 41, same as DATA_NOT_EXIST — a bug fixed in v2.7.2+ and v3.5.2) |

Custom business error codes should start from **100**, built via `ErrorCode.build(code)`, with i18n support.

---

## Source Code Verification (Fallback)

When reference files do not cover a specific API or you need to confirm parameters, read framework source code via `git show`:

```bash
git show <branch>:<file-path>
```

| Module | Key Source Files (under `src/main/java/`) |
|------|--------------------------------------|
| houtu-core | `.../core/exception/BusinessException.java`, `.../core/exception/ErrorCode.java`, `.../core/constant/ErrorCodeConstant.java`, `.../core/context/SpringApplicationContext.java` |
| houtu-web | `.../web/model/ResponseData.java`, `.../web/model/EmbedResponseData.java`, `.../web/model/vo/PageDataVO.java`, `.../web/model/form/PageForm.java`, `.../web/handler/UnifiedHandlerExceptionResolver.java`, `.../web/validation/constroins/NotXss.java` |
| houtu-web-security | `.../websecurity/annotation/*.java`, `.../websecurity/session/SessionContext.java` |
| houtu-cache | `.../lock/annotation/Lock.java`, `.../lock/support/LockSupport.java`, `.../lock/support/BLock.java`, `.../limit/RateLimiter.java` |
| houtu-data-security | `.../data/security/annotation/SecurityWatch.java`, `.../data/security/handler/SecurityProcessor.java` |
| houtu-access-log | `.../accesslog/annotation/AccessLog.java`, `.../accesslog/handler/LogFilterHandler.java` |
| houtu-utils | `.../util/crypto/*.java`, `.../util/JsonUtils.java`, `.../util/HttpClients.java` |
| houtu-actuator | `.../actuator/metrics/*.java` |
| sc-houtu-loadbalancer | `.../loadbalancer/support/hint/HintContext.java` |
| sc-houtu-feign | `.../feign/anotation/AutoFeign.java` |
| sc-houtu-discovery | `.../discovery/context/ServiceContext.java` |

> Path prefix: `io/github/lujiafa/houtu`
> Note: The package name for `@AutoFeign` is `anotation` (not `annotation`); this is the framework's original spelling.

---

## Version Quick Comparison

| Feature | v3.5.2 | v3.5.1 | v3.5.0 | v2.7.3 | v2.7.2 | v2.7.1 |
|------|--------|--------|--------|--------|--------|--------|
| JDK | 17+ | 17+ | 17+ | 1.8+ | 1.8+ | 1.8+ |
| Spring Boot | 3.5.11 | 3.5.11 | 3.5.11 | 2.7.18 | 2.7.18 | 2.7.18 |
| Package prefix | `io.github.lujiafa.houtu` | Same | Same | Same | Same | Same |
| Namespace | `jakarta.*` | `jakarta.*` | `jakarta.*` | `javax.*` | `javax.*` | `javax.*` |
| Redis config | `spring.data.redis.*` | Same | Same | `spring.redis.*` | `spring.redis.*` | `spring.redis.*` |
| Nacos config | `spring.config.import` | Same | **bootstrap.yml** | bootstrap.yml | bootstrap.yml | bootstrap.yml |
| SCA version | 2025.0.0.0 | Same | **2023.0.1.2** | 2021.0.6.2 | 2021.0.6.2 | 2021.0.6.2 |
| @Lock SpEL | ✅ | ✗ | ✗ | ✅ | ✗ | ✗ |

> See version details at `references/v{version}.md`
