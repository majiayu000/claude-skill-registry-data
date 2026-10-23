---
name: restassured-testing
description: "Strengthens and speeds up JVM API test suites - assertions so loose that an empty `200 OK` passed for three days, a 220-test suite spending fourteen minutes mostly waiting on sequential HTTP calls, or endpoints exercised through a hand-rolled JDK HTTP client with JSON parsed by hand. Authors REST Assured (Java) tests in the given().when().then() BDD-style DSL: status code and JSON / XML path assertions, authentication (Basic, OAuth2, API key), Maven / Gradle dependencies, JUnit 5 execution, and Surefire / JaCoCo reports for CI gating. Use when the project is on the JVM and its API tests miss real assertions, run too slowly, or are written by hand."
---

# restassured-testing

## Overview

REST Assured is a Java DSL for HTTP API testing with a BDD-style
`given().when().then()` chain ([restassured-readme][readme]). It runs
inside any JUnit / TestNG suite and consumes JSON, XML, and other
content types via path expressions backed by Hamcrest matchers
([restassured-usage][usage]).

[readme]: https://github.com/rest-assured/rest-assured
[usage]: https://github.com/rest-assured/rest-assured/wiki/Usage

This is the JVM-native counterpart to
`postman-collections`. Use REST
Assured when the team's primary stack is Java / Kotlin / Scala and
type-safe authoring + same-language refactoring matter.

## When to use

- The project is a Maven or Gradle Java project.
- The team wants API tests in the same language as the application
  (refactor-safe, IDE-aware).
- Tests need to compose fluently with JUnit 5 / TestNG fixtures.
- Authentication patterns required: Basic (preemptive), OAuth2
  (bearer token), API key in header - all first-class.

If the team is non-JVM, evaluate
`postman-collections` (JSON-driven),
`tavern-testing` (Python YAML), or
`karate-testing` (cross-platform DSL).

## Install

### Maven

```xml
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <version>6.0.0</version>
    <scope>test</scope>
</dependency>
```

(Per [restassured-usage][usage].)

For JSON Schema validation, add `json-schema-validator` from the
same group; for path-style assertions on JSON, the core dependency
is enough.

### Gradle

```groovy
testImplementation 'io.rest-assured:rest-assured:6.0.0'
```

## Authoring

### Imports

The canonical static imports for fluent authoring
([restassured-usage][usage]):

```java
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;
import static io.restassured.matcher.RestAssuredMatchers.*;
```

These bring `given()`, `get()`, `post()`, etc. plus Hamcrest matchers
(`equalTo`, `hasItems`, `containsString`, `nullValue`, etc.) into
scope.

### given() / when() / then() chain

The basic shape ([restassured-readme][readme]):

```java
given().
    param("key1", "value1").
when().
    post("/somewhere").
then().
    body(containsString("OK"));
```

`given()` configures the request (params, headers, body, auth);
`when()` issues the HTTP verb; `then()` asserts the response.

### Status code assertion

```java
get("/x").then().assertThat().statusCode(200);
```

(Per [restassured-usage][usage].)

`statusCode(int)` is equivalent to `statusCode(equalTo(int))`. For
ranges, use `statusCode(allOf(greaterThanOrEqualTo(200), lessThan(300)))`.

### JSON path assertions

```java
get("/lotto").then().body("lotto.lottoId", equalTo(5));
get("/lotto").then().body("lotto.winners.winnerId", hasItems(23, 54));
```

(Per [restassured-usage][usage].)

The first argument is a Groovy-style JSON path
(`models[0].author.name`); the second is a Hamcrest matcher.

### XML path assertions

```java
given().parameters("firstName", "John", "lastName", "Doe").
when().post("/greetXML").
then().body("greeting.firstName", equalTo("John"));
```

(Per [restassured-usage][usage].)

### Combined status + body assertion

```java
given().header("Accept", "application/json").
when().get("/orders/42").
then().
    statusCode(200).
    body("order_id", equalTo(42)).
    body("status", equalTo("shipped")).
    body("items", hasSize(greaterThan(0)));
```

## Authentication

REST Assured ships first-class auth support
([restassured-usage][usage]):

### OAuth2 / Bearer token

```java
given().auth().oauth2(accessToken).when().get("/secured").then().statusCode(200);
```

### Preemptive Basic Auth

```java
given().auth().preemptive().basic("username", "password").
when().get("/secured/hello").
then().statusCode(200);
```

`preemptive()` sends the `Authorization` header on the first request
without waiting for a 401 challenge - required for most modern APIs
that don't issue WWW-Authenticate.

### API Key in header

```java
given().header("X-API-KEY", "your-api-key").when().get("/endpoint");
```

For any custom auth scheme, fall through to the `header()` form - 
REST Assured doesn't impose a structure beyond the standard Basic /
OAuth1/2 patterns.

## Worked example: full JUnit 5 test

```java
package com.example.api;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class OrdersApiIT {

  @BeforeAll
  static void setup() {
    RestAssured.baseURI = System.getProperty("api.baseURI", "http://localhost:8080");
  }

  @Test
  @DisplayName("GET /orders/42 returns the expected order")
  void getOrder() {
    given().
        auth().oauth2(System.getenv("API_TOKEN")).
        accept(ContentType.JSON).
    when().
        get("/orders/42").
    then().
        statusCode(200).
        contentType(ContentType.JSON).
        body("order_id",  equalTo(42)).
        body("status",    isOneOf("placed", "shipped", "completed", "returned")).
        body("items",     hasSize(greaterThan(0))).
        body("items[0].sku", matchesPattern("^[A-Z0-9]{8}$"));
  }
}
```

## CI integration

```yaml
# .github/workflows/api-tests.yml
name: api-tests

on:
  pull_request:
  push:
    branches: [main]

jobs:
  restassured:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
          cache: 'maven'

      - name: Run integration tests
        env:
          API_TOKEN: ${{ secrets.STAGING_API_TOKEN }}
        run: |
          mvn -B verify \
            -Dapi.baseURI=https://staging.example.com \
            -Dfailsafe.includes='**/*IT.java'

      - name: Surface JUnit results
        if: always()
        uses: dorny/test-reporter@v1
        with:
          name: REST Assured tests
          path: target/failsafe-reports/TEST-*.xml
          reporter: java-junit

      - name: Upload test reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: failsafe-reports
          path: target/failsafe-reports/
          retention-days: 14
```

The `*IT.java` suffix is the Maven Failsafe convention for
**integration tests** (separate from `*Test.java` unit tests). Failsafe
uploads JUnit XML to `target/failsafe-reports/` automatically - same
format as Newman's `--reporter-junit-export`.

## Anti-patterns

| Anti-pattern                                              | Why it fails                                                         | Fix |
|-----------------------------------------------------------|----------------------------------------------------------------------|-----|
| Hard-coded `RestAssured.baseURI` in source                 | Tests bind to one environment; can't run against staging vs local.   | Read from system property: `RestAssured.baseURI = System.getProperty("api.baseURI", default);`. |
| Inline tokens in source                                    | Secrets leak; PRs flag; rotation pain.                              | Read from env var: `System.getenv("API_TOKEN")`. |
| `.basic()` without `.preemptive()`                         | Sends an unauthorized request first; doubles round trips and may fail on APIs that don't issue WWW-Authenticate. | Use `auth().preemptive().basic(...)`. |
| Asserting only status code without body shape              | Status 200 with garbage body still passes. | Always assert at least one body field, ideally schema-validated. |
| One mega-assertion `body(equalTo(jsonString))`             | Diff is uninterpretable on failure.                                  | Multiple field-level `body(path, matcher)` calls; fail-fast naming surfaces which field is wrong. |
| Mixing unit-test (`*Test.java`) and integration (`*IT.java`) by name only | Maven Surefire vs Failsafe gets confused; integration tests run during the unit-test phase. | Strict naming: `*Test.java` for unit (`mvn test`); `*IT.java` for integration (`mvn verify`). |

## Limitations

- **Java-only.** Kotlin and Scala work but the syntax overhead is
  notable (especially Kotlin trailing-lambda style); the canonical
  examples are Java.
- **No native parallelism.** Use JUnit 5's `@Execution(CONCURRENT)`
  or TestNG's `parallel="methods"` to parallelize at the framework
  level.
- **Schema validation is a separate jar.** Add
  `io.rest-assured:json-schema-validator` if you want
  `body(matchesJsonSchema(file))` style assertions.

## References

- [restassured-readme][readme] - main repo README; basic given/when/then
  + Maven groupId.
- [restassured-usage][usage] - full DSL reference: Maven dep XML,
  imports, status code, JSON/XML path, OAuth2, preemptive Basic,
  API-key header.
- `postman-collections` - 
  JSON-driven counterpart for non-JVM teams.
- `schemathesis-fuzzing` - 
  property-based fuzzing complement (different approach to coverage).
