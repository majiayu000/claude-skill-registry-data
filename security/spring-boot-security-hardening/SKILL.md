---
name: spring-boot-security-hardening
description: >
  Security hardening for Spring Boot: SecurityFilterChain, CORS/CSRF,
  rate limiting (resilience4j), password hashing (Argon2), OWASP top 10
  applied to Spring, JWT authentication + refresh tokens, secrets handling,
  and a prevention checklist. Use when asked to improve security, review
  auth, run an audit, or address pentest findings.
---

# Security hardening

## Choose an authentication scenario before changing security

Identify credential transport, trust boundary, issuer/audience, session behavior and affected endpoints. Record the observed threat and evidence before proposing a mitigation.

| Scenario | Required decision |
|---|---|
| Header-only bearer API | Validate issuer, audience, signature and expiry; stateless chain; CSRF exception only for endpoints that cannot authenticate via cookies/browser credentials. |
| Browser session or cookie token | Preserve CSRF protection, secure/HttpOnly/SameSite cookies and session lifecycle; CORS alone does not prevent CSRF. |
| OAuth2 login/client | Separate client/login configuration from resource-server validation; do not replace external identity with a custom token issuer. |
| Application-owned passwords | Adaptive hashing, migration of existing hashes and measured resource cost; resource servers alone do not need a password store. |
| Service-to-service | Scope/audience boundaries and key rotation; mTLS or token design depends on the deployed trust model. |

Match the existing design. Test unauthenticated, wrong-scope, wrong-audience, expired-token and ownership outcomes relevant to that design. Do not disable CSRF globally to repair a mixed cookie/bearer application.

## SecurityFilterChain (Spring Security 7+)

This chain is for an API authenticated exclusively by a bearer token in the Authorization header. Provide `spring.security.oauth2.resourceserver.jwt.issuer-uri` and the OAuth2 resource-server starter. Cookie-based endpoints, including refresh endpoints, require CSRF protection; use a separate protected chain if combined with this API.

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {
    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .cors(Customizer.withDefaults()) // uses the bean named "corsConfigurationSource"
            .csrf(csrf -> csrf.disable()) // header-only bearer authentication
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health", "/actuator/health/liveness", "/actuator/health/readiness").permitAll()
                .requestMatchers("/api/v1/admin/**").hasAuthority("SCOPE_admin")
                .anyRequest().authenticated())
            .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
    }
}
```

For opaque tokens instead, use `oauth2.opaqueToken(token -> token.introspector(introspector))` with an `OpaqueTokenIntrospector` bean. JWT scopes map to `SCOPE_` authorities by default; custom role claims need a `JwtAuthenticationConverter`.

### CORS

```java
@Bean
CorsConfigurationSource corsConfigurationSource() { // Spring Security looks this bean up by name
    var source = new UrlBasedCorsConfigurationSource();
    var config = new CorsConfiguration();
    config.setAllowedOrigins(List.of(
        "https://app.mycompany.com",
        "http://localhost:4200"
    ));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "PATCH"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type", "X-Correlation-Id"));
    config.setExposedHeaders(List.of("X-Correlation-Id"));
    config.setMaxAge(3600L);
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

**Never** use `allowedOrigins: ["*"]` with credentials. If you need many dynamic origins, use a `CorsConfigurationSource` that reads from DB/config.

Use framework-supported MDC/context propagation for correlation IDs, including async boundaries. Scoped Values can carry application-owned immutable context but do not replace MDC automatically.

### Password hashing

```java
import org.springframework.security.crypto.argon2.Argon2PasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

public final class PasswordHashing {
    public static PasswordEncoder encoder() {
        return Argon2PasswordEncoder.defaultsForSpringSecurity_v5_8();
    }
}
```

Argon2 requires Bouncy Castle (`org.bouncycastle:bcprov-jdk18on`) with an explicit reviewed version; Boot does not manage it. Benchmark parameters against the application's latency and resource budget. `PasswordEncoderFactories.createDelegatingPasswordEncoder()` supports prefixed hashes and gradual algorithm migration. Never store plaintext passwords or use fast unsalted hashes.

### Rate limiting (Resilience4j)

Framework retry support is not a distributed request rate limiter. Add `io.github.resilience4j:resilience4j-ratelimiter` with a verified version (not automatically managed by Boot). This example limits one JVM; per-client/distributed limits require a gateway or appropriately configured distributed implementation.

```java
import io.github.resilience4j.ratelimiter.RateLimiter;
import io.github.resilience4j.ratelimiter.RateLimiterConfig;
import java.time.Duration;
import java.util.function.Supplier;

public final class ApiRateLimit {
    private final RateLimiter limiter = RateLimiter.of("api", RateLimiterConfig.custom()
        .limitForPeriod(100)
        .limitRefreshPeriod(Duration.ofSeconds(1))
        .timeoutDuration(Duration.ZERO)
        .build());

    public <T> T call(Supplier<T> action) {
        return RateLimiter.decorateSupplier(limiter, action).get();
    }
}
```

Map `RequestNotPermitted` to HTTP 429 and apply a client-aware policy to login and refresh endpoints.

### JWT + refresh tokens

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: ${JWT_ISSUER_URI}
          audiences: ${JWT_AUDIENCE}
```

The encoder must be configured with appropriate signing keys and algorithm. Example token creation:

```java
import java.time.Instant;
import java.util.List;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;

public final class AccessTokens {
    private final JwtEncoder encoder;
    private final String issuer;
    private final String audience;

    public AccessTokens(JwtEncoder encoder, String issuer, String audience) {
        this.encoder = encoder;
        this.issuer = issuer;
        this.audience = audience;
    }

    public String issue(String subject) {
        Instant now = Instant.now();
        JwtClaimsSet claims = JwtClaimsSet.builder()
            .issuer(issuer).subject(subject)
            .audience(List.of(audience))
            .issuedAt(now).expiresAt(now.plusSeconds(900))
            .claim("scope", "users.read")
            .build();
        return encoder.encode(JwtEncoderParameters.from(claims)).getTokenValue();
    }
}
```

Configure the issuer's `audience` with the same intended resource identifier as `JWT_AUDIENCE` above. Validate issuer, audience, algorithm and expiry on consumption. Use short-lived access tokens and rotate/revoke refresh tokens with reuse detection. A refresh token in an HttpOnly, Secure, SameSite cookie is still browser-supplied authentication: enforce CSRF tokens and origin checks on the refresh endpoint. SameSite is defense in depth, not a replacement for CSRF protection.

## Hardening checklist

- [ ] CORS configured with concrete origins (no `*`).
- [ ] `Content-Type: application/json` on POST/PUT — reject if missing (JSON bypass).
- [ ] Rate limiting on login and account creation.
- [ ] HSTS header (`Strict-Transport-Security: max-age=31536000; includeSubDomains`).
- [ ] `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.
- [ ] Bearer-token API: stateless sessions (JWT), no session cookie for the API. Browser-session or cookie-token application: secure session lifecycle (fixation protection, timeouts, invalidation on logout) and CSRF protection instead.
- [ ] Secrets in environment variables / Vault, never in committed YAML.
- [ ] DDL-auto = none on all profiles except dev.
- [ ] Preserve security filtering for relevant servlet dispatches; do not override dispatcher types without testing error and async requests.
- [ ] Input validation on every endpoint (Bean Validation).
- [ ] Log failed auth attempts (login, refresh) with user and timestamp.
- [ ] Audit changes to sensitive entities (role changes, email changes).

## References

- [Resource server JWT](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html)
- [CSRF and stateless browser applications](https://docs.spring.io/spring-security/reference/features/exploits/csrf.html)
- [Argon2PasswordEncoder API](https://docs.spring.io/spring-security/reference/api/java/org/springframework/security/crypto/argon2/Argon2PasswordEncoder.html)
- [Resilience4j RateLimiter](https://resilience4j.readme.io/docs/ratelimiter)
