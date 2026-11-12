---
name: spring-security
description: "Spring Security 기본 설정 — SecurityFilterChain, Method Security(@PreAuthorize), CORS, 설정 우선순위, Authorization Server. Use when Spring 앱의 인증·인가 필터와 CORS 를 구성하거나 메서드 단위 권한을 걸 때."
---

# Spring Security Patterns

Spring Security 기본 설정 및 Method Security 패턴

## Quick Reference (결정 트리)

```
인증 방식 선택
    │
    ├─ JWT 직접 발급 ────> JwtProvider + Filter
    │                      (상세: /java:spring-oauth2 참조)
    │
    ├─ OAuth2 Authorization Server 구축
    │   └─ Spring Authorization Server (신규 프로젝트)
    │
    ├─ OAuth2 Provider ──> Resource Server 설정
    │                      (상세: /java:spring-oauth2 참조)
    │
    └─ Session 기반 ─────> 기본 formLogin()
```

---

## 의존성

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-oauth2-resource-server'
    // JWT 직접 발급 시
    implementation 'io.jsonwebtoken:jjwt-api:0.12.3'
    runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.12.3'
    runtimeOnly 'io.jsonwebtoken:jjwt-jackson:0.12.3'
}
```

---

## CRITICAL: Security 설정

**IMPORTANT**: CSRF 비활성화는 Stateless API에서만 사용

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    private final JwtAuthenticationFilter jwtFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())  // Stateless API만
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

---

## Method Security

### 기본 어노테이션

```java
@Service
public class UserService {

    // 역할 기반
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long id) { }

    // 권한 기반
    @PreAuthorize("hasAuthority('USER_WRITE')")
    public User updateUser(Long id, UpdateUserRequest request) { }

    // 복합 조건: 관리자이거나 본인
    @PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
    public User getUser(Long id) { }

    // 반환값 필터링
    @PostAuthorize("returnObject.ownerId == authentication.principal.id")
    public Resource getResource(Long id) { }

    // 컬렉션 필터링
    @PostFilter("filterObject.ownerId == authentication.principal.id")
    public List<Resource> getAllResources() { }
}
```

### 커스텀 Security Expression

```java
@Component("authz")
@RequiredArgsConstructor
public class AuthorizationService {
    private final ResourceRepository resourceRepository;

    public boolean isOwner(Long resourceId) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        Long userId = ((CustomUserDetails) auth.getPrincipal()).getId();

        return resourceRepository.findById(resourceId)
            .map(r -> r.getOwnerId().equals(userId))
            .orElse(false);
    }
}

// 사용
@PreAuthorize("@authz.isOwner(#resourceId)")
public void updateResource(Long resourceId, UpdateRequest request) { }
```

---

## CORS 설정

```java
@Configuration
public class CorsConfig {

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("https://example.com", "http://localhost:3000"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "PATCH"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return source;
    }
}
```

---

## 보안 설정 우선순위

| 순서 | 방식 | 용도 |
|------|------|------|
| 1 | `requestMatchers()` | URL 패턴 기반 |
| 2 | `@PreAuthorize` | 메서드 진입 전 |
| 3 | `@PostAuthorize` | 메서드 실행 후 |
| 4 | `@PostFilter` | 반환 컬렉션 필터링 |

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| JWT Secret 하드코딩 | 환경변수 또는 Vault 사용 |
| HTTPS 미사용 | 프로덕션에서 필수 |
| 비밀번호 평문 저장 | BCrypt 해시 필수 |
| 권한 체크 컨트롤러에만 | @PreAuthorize로 서비스에도 적용 |
| Actuator 노출 | 엔드포인트 보호 필수 |

---

## Spring Authorization Server (자체 OAuth2 서버)

Spring Security 6.x와 함께 사용하는 OAuth2 Authorization Server:

```groovy
implementation 'org.springframework.boot:spring-boot-starter-oauth2-authorization-server'
```

```java
@Configuration
public class AuthServerConfig {
    @Bean
    public RegisteredClientRepository registeredClientRepository() {
        RegisteredClient client = RegisteredClient.withId(UUID.randomUUID().toString())
            .clientId("my-client")
            .clientSecret("{noop}secret")
            .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
            .authorizationGrantType(AuthorizationGrantType.REFRESH_TOKEN)
            .redirectUri("http://localhost:8080/callback")
            .scope(OidcScopes.OPENID)
            .scope("read")
            .build();
        return new InMemoryRegisteredClientRepository(client);
    }
}
```

**권장**: JWT 서명에는 RSA 키 기반 사용 (HMAC보다 안전)

---

## 체크리스트

- [ ] HTTPS 적용
- [ ] 비밀번호 BCrypt 해시
- [ ] CORS 적절히 설정
- [ ] Method Security 적용
- [ ] Actuator 엔드포인트 보호
- [ ] JWT 상세 설정: `/java:spring-oauth2` 참조
- [ ] RSA 키 기반 JWT 서명 (HMAC 대신)
