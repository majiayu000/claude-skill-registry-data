---
name: spring-boot-contract-testing
description: >
  Guides contract testing between Spring Boot services: consumer-driven
  contracts with Pact (pact-jvm consumer tests, pact file publishing, broker
  verification) and provider-side contracts with Spring Cloud Contract
  (contracts in Groovy/YAML, stub publishing, consumer stub runner). Use when
  asked about contract tests, Pact, Spring Cloud Contract, consumer-driven
  contracts, or verifying inter-service API compatibility.
---

# Contract Testing in Spring Boot

Guides setting up contract testing between separately deployed Spring Boot services.

## When contract testing applies

Use contract testing when one service calls another over HTTP (or messaging) and the two are deployed and released independently. Unit tests and integration tests each validate one side in isolation; they do not catch contract drift — a field renamed, a status code changed, a content type narrowed — until both services are running together in a shared environment, which is usually too late. A contract test pins the interaction so a breaking change fails the *provider's* build, not the consumer's production deployment.

## Choose the tool

| Situation | Tool |
|---|---|
| The consumer defines what it needs; the provider is another team | Pact (consumer-driven) |
| The provider owns the API specification and wants to publish verifiable stubs to consumers | Spring Cloud Contract |

**Decision rule:** Pact when the consumer drives the expectations — each consumer publishes what it uses, and the provider verifies against all of them. Spring Cloud Contract when the provider is the source of truth: contracts live with the provider, and consumers get generated stubs without ever writing a contract test. Neither Pact nor Spring Cloud Contract is automatically managed by Boot. Select a Pact JVM version compatible with the test platform, or a Spring Cloud release train explicitly compatible with the project Boot version.

Do not state specific version numbers unless verified; for Spring Cloud Contract, rely on the version managed by the Spring Cloud release train BOM ("latest managed by the BOM").

## Option 1: Pact (consumer-driven)

### Consumer test

The consumer test should drive the **real application HTTP client** against a Pact mock server, so it exercises the exact serialization path the consumer uses in production. It generates a pact file (JSON) describing the interaction.

Add test dependency `au.com.dius.pact.consumer:junit5` at a verified Pact JVM version.

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;
import au.com.dius.pact.consumer.MockServer;
import au.com.dius.pact.consumer.dsl.PactDslJsonBody;
import au.com.dius.pact.consumer.dsl.PactDslWithProvider;
import au.com.dius.pact.consumer.junit5.PactConsumerTestExt;
import au.com.dius.pact.consumer.junit5.PactTestFor;
import au.com.dius.pact.core.model.RequestResponsePact;
import au.com.dius.pact.core.model.PactSpecVersion;
import au.com.dius.pact.core.model.annotations.Pact;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.assertEquals;

@ExtendWith(PactConsumerTestExt.class)
public class UserClientPactTest {
    @Pact(consumer = "order-service", provider = "user-service")
    public RequestResponsePact usersExist(PactDslWithProvider builder) {
        return builder.given("user 42 exists")
            .uponReceiving("a request for user 42")
            .path("/api/v1/users/42").method("GET")
            .willRespondWith().status(200)
            .headers(Map.of("Content-Type", "application/json"))
            .body(new PactDslJsonBody().numberType("id", 42L)
                .stringType("email", "user@example.com"))
            .toPact();
    }

    @Test
    @PactTestFor(pactMethod = "usersExist", pactVersion = PactSpecVersion.V3)
    void fetchUser(MockServer server) throws Exception {
        // Replace with the application's production client and assert deserialization.
        var request = HttpRequest.newBuilder(
            URI.create(server.getUrl() + "/api/v1/users/42")).GET().build();
        var response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode());
        var user = tools.jackson.databind.json.JsonMapper.builder().build()
            .readTree(response.body());
        assertEquals(42, user.get("id").asInt());
        assertEquals("user@example.com", user.get("email").asString());
    }
}
```

Key fields to always set explicitly: provider name, a human-readable request description ("a request for user 42"), provider state ("user 42 exists"), expected status, and content type. Matching rules: `stringType`/`numberType` match by type, not by exact value — do not over-constrain the provider.

### Publishing and provider verification

- Publish pacts from CI to a **Pact Broker** (or Pactflow) tagged with the branch/version. Gate the consumer's deploy on `can-i-deploy` so it only ships against a verified provider version.
- The provider verifies with `@PactBroker` (fetches pacts from the broker) or `@PactFolder` for local pact files:

Add test dependency `au.com.dius.pact.provider:junit5` at the same verified Pact JVM version. Local verification example (start and seed the actual provider before running):

```java
import au.com.dius.pact.provider.junit5.HttpTestTarget;
import au.com.dius.pact.provider.junit5.PactVerificationContext;
import au.com.dius.pact.provider.junit5.PactVerificationInvocationContextProvider;
import au.com.dius.pact.provider.junitsupport.Provider;
import au.com.dius.pact.provider.junitsupport.State;
import au.com.dius.pact.provider.junitsupport.loader.PactFolder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestTemplate;
import org.junit.jupiter.api.extension.ExtendWith;

@Provider("user-service")
@PactFolder("target/pacts")
public class UserServiceProviderTest {
    @BeforeEach
    void target(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", Integer.getInteger("provider.port", 8080)));
    }

    @State("user 42 exists")
    void seedUser() {
        // Implement with the provider's repository/test fixture before enabling in CI.
        // An empty state method is valid only when an external fixture already seeded user 42.
    }

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void verify(PactVerificationContext context) {
        context.verifyInteraction();
    }
}
```

For CI replace `@PactFolder` with `@PactBroker` and configure broker URL/auth and consumer selectors using protected CI settings. The provider target must be the running application, not a Pact mock server.

- Wire provider verification into CI and enable broker webhooks so a breaking consumer change re-triggers provider verification (and vice versa).

### Reproducible release cycle

1. Run the consumer against its local mock and assert the deserialized fields it uses. Keep the generated pact and consumer revision as artifacts.
2. Start the real provider in an isolated test environment, implement/reset every declared provider state and run verification against that exact pact. An independently implemented local HTTP fixture demonstrates the pipeline; it does not certify the production provider.
3. Publish only from an authorized trusted CI job. The following commands are templates, not actions performed by loading this skill. Supply protected broker settings and immutable revisions; never embed broker tokens in source or logs.

```bash
# Consumer publication (requires explicit publication scope and broker credentials)
pact-broker publish target/pacts --consumer-app-version "$CONSUMER_REVISION" \
  --branch "$CI_BRANCH" --broker-base-url "$PACT_BROKER_BASE_URL"
# Before either application deploys, using its own immutable revision:
pact-broker can-i-deploy --pacticipant "$APPLICATION" --version "$REVISION" \
  --to-environment "$DEPLOY_ENVIRONMENT" --broker-base-url "$PACT_BROKER_BASE_URL"
# Only AFTER the authorized deployment succeeds:
pact-broker record-deployment --pacticipant "$APPLICATION" --version "$REVISION" \
  --environment "$DEPLOY_ENVIRONMENT" --broker-base-url "$PACT_BROKER_BASE_URL"
```

4. Provider CI records verification results with its exact provider revision and branch; select relevant consumer branches and deployed/released versions. Enable publication explicitly only in that trusted job (`pact.verifier.publishResults=true` and provider-version configuration for the selected Pact JVM release). Do not silently accept missing/pending verification as compatibility.
5. A renamed required field, narrowed type or changed status must fail verification. Keep an additive-field case that passes, a breaking-field case that fails, and an unimplemented-state case that fails. An empty pact directory must not count as successful verification.

The repository `tests/examples/check.sh` runs the extracted consumer and provider examples locally with a seeded independent HTTP fixture, then deliberately returns a broken response and checks verification rejects it. It never contacts or publishes to a broker.

## Option 2: Spring Cloud Contract (provider-side)

Contracts live in the provider's repo under `src/test/resources/contracts`, written in Groovy DSL or YAML. The `spring-cloud-contract-verifier` plugin/dependency generates provider verification tests from them, and produces stub JARs for consumers. Version comes from the Spring Cloud release train BOM — do not pin manually.

### YAML contract

```yaml
# src/test/resources/contracts/user/shouldReturnUser.yaml
request:
  method: GET
  url: /api/v1/users/42
  headers:
    Content-Type: application/json
response:
  status: 200
  headers:
    Content-Type: application/json
  body:
    id: 42
    email: "user@example.com"
  matchers:
    body:
      - path: $.id
        type: by_type
      - path: $.email
        type: by_regex
        value: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-z]{2,}"
```

The generated provider test uses a base test class that you configure with the application context and MockMvc/RestAssured test target. WireMock stubs are produced for consumers; WireMock is not automatically placed in front of the provider. Keep `matchers` loose where values vary, strict where the consumer depends on shape.

### Publishing stubs and consuming them

Configure the Spring Cloud Contract Maven/Gradle plugin to install/publish the stubs artifact (local Maven repo for development, remote repository or a local stub storage directory for CI). Consumers depend on the stub artifact with the `stubs` classifier.

Consumer side — let the **Stub Runner** boot WireMock instances from the published stubs; for local development, use local mode:

Add the test-scoped `org.springframework.cloud:spring-cloud-starter-contract-stub-runner` managed by the selected compatible Spring Cloud BOM. Resolve an exact published provider stub version:

```java
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cloud.contract.stubrunner.spring.AutoConfigureStubRunner;
import org.springframework.cloud.contract.stubrunner.spring.StubRunnerProperties;

@SpringBootTest
@AutoConfigureStubRunner(
    ids = "com.example:user-service:1.0.0:stubs:9090",
    stubsMode = StubRunnerProperties.StubsMode.LOCAL)
class UserClientStubTest {
    // Configure the application's user client base URL to http://localhost:9090,
    // call it and assert the deserialized result in an actual @Test method.
}
```

For remote artifacts use `REMOTE` with a configured repository. Avoid floating versions in reproducible CI.

`ids` supports `groupId:artifactId:version:classifier`; `+` means latest available.

## Rules

- Always set provider state (`given`) and implement its setup on the provider side — unfulfilled states make verification meaningless.
- Keep contracts minimal: match on type/regex, not exact values, to avoid brittle provider builds.
- Run contract verification on every provider build; wire broker webhooks (Pact) or stub publishing (SCC) into CI so both sides are gated.
- Never test business logic through contracts — they pin the interface, not behavior beyond the interaction.

## References

- [Pact Broker publication and deployment CLI](https://docs.pact.io/pact_broker/client_cli/readme)
- [Pact JVM consumer JUnit 5](https://docs.pact.io/implementation_guides/jvm/consumer/junit5)
- [Pact JVM provider JUnit 5](https://docs.pact.io/implementation_guides/jvm/provider/junit5)
- [Spring Cloud Contract Stub Runner](https://docs.spring.io/spring-cloud-contract/reference/project-features-stubrunner.html)
