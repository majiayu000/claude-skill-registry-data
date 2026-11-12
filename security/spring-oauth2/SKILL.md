---
name: spring-oauth2
description: "Spring JWT 와 OAuth2 — JWT 발급·검증, JWT Filter, Auth Controller, Resource Server 설정, Token TTL. Use when Spring 서비스에 JWT 로그인을 구현하거나 OAuth2 Resource Server 로 API 를 보호할 때."
---

# Spring OAuth2 & JWT Patterns

JWT 토큰 발급/검증 및 OAuth2 Resource Server 설정

## Quick Reference (결정 트리)

```
JWT 구현 방식
    │
    ├─ 직접 발급 ────> JwtProvider + AuthService
    │                  (이 문서)
    │
    └─ 외부 IdP ─────> OAuth2 Resource Server
                       (이 문서 하단)
```

---

## CRITICAL: JWT Provider

**IMPORTANT**: Access Token 15분, Refresh Token 7일 권장

```java
@Component
public class JwtProvider {
    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.access-token-validity}")
    private long accessTokenValidity;  // 15분 (900000ms)

    @Value("${jwt.refresh-token-validity}")
    private long refreshTokenValidity;  // 7일 (604800000ms)

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(secretKey.getBytes(StandardCharsets.UTF_8));
    }

    public String createAccessToken(Long userId, String email, List<String> roles) {
        return Jwts.builder()
            .subject(String.valueOf(userId))
            .claim("email", email)
            .claim("roles", roles)
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + accessTokenValidity))
            .signWith(getSigningKey())
            .compact();
    }

    public String createRefreshToken(Long userId) {
        return Jwts.builder()
            .subject(String.valueOf(userId))
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + refreshTokenValidity))
            .signWith(getSigningKey())
            .compact();
    }

    public Claims parseToken(String token) {
        return Jwts.parser()
            .verifyWith(getSigningKey())
            .build()
            .parseSignedClaims(token)
            .getPayload();
    }

    public boolean validateToken(String token) {
        try {
            parseToken(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}
```

---

## JWT Filter

```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    private final JwtProvider jwtProvider;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        String token = extractToken(request);

        if (token != null && jwtProvider.validateToken(token)) {
            Claims claims = jwtProvider.parseToken(token);
            String userId = claims.getSubject();

            UserDetails userDetails = userDetailsService.loadUserByUsername(userId);
            UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
            auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

            SecurityContextHolder.getContext().setAuthentication(auth);
        }

        chain.doFilter(request, response);
    }

    private String extractToken(HttpServletRequest request) {
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            return header.substring(7);
        }
        return null;
    }
}
```

---

## Auth Controller & Service

```java
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;

    @PostMapping("/signup")
    public ResponseEntity<UserResponse> signup(@Valid @RequestBody SignupRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(authService.signup(request));
    }

    @PostMapping("/login")
    public ResponseEntity<TokenResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @PostMapping("/refresh")
    public ResponseEntity<TokenResponse> refresh(@RequestBody RefreshTokenRequest request) {
        return ResponseEntity.ok(authService.refresh(request.getRefreshToken()));
    }

    @PostMapping("/logout")
    public ResponseEntity<Void> logout(@AuthenticationPrincipal CustomUserDetails user) {
        authService.logout(user.getId());
        return ResponseEntity.noContent().build();
    }
}
```

### Auth Service

```java
@Service
@RequiredArgsConstructor
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;
    private final RefreshTokenRepository refreshTokenRepository;

    @Transactional
    public TokenResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
            .orElseThrow(() -> new UnauthorizedException("Invalid credentials"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new UnauthorizedException("Invalid credentials");
        }

        String accessToken = jwtProvider.createAccessToken(
            user.getId(), user.getEmail(), user.getRoles());
        String refreshToken = jwtProvider.createRefreshToken(user.getId());

        // Refresh Token 저장 (Redis 또는 DB)
        refreshTokenRepository.save(new RefreshToken(user.getId(), refreshToken));

        return new TokenResponse(accessToken, refreshToken);
    }

    @Transactional
    public TokenResponse refresh(String refreshToken) {
        if (!jwtProvider.validateToken(refreshToken)) {
            throw new UnauthorizedException("Invalid refresh token");
        }

        Claims claims = jwtProvider.parseToken(refreshToken);
        Long userId = Long.parseLong(claims.getSubject());

        RefreshToken stored = refreshTokenRepository.findByUserId(userId)
            .orElseThrow(() -> new UnauthorizedException("Refresh token not found"));

        if (!stored.getToken().equals(refreshToken)) {
            throw new UnauthorizedException("Refresh token mismatch");
        }

        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UnauthorizedException("User not found"));

        String newAccessToken = jwtProvider.createAccessToken(
            user.getId(), user.getEmail(), user.getRoles());

        return new TokenResponse(newAccessToken, refreshToken);
    }
}
```

---

## OAuth2 Resource Server

### application.yml

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com
          # 또는 직접 jwk-set-uri 지정
          # jwk-set-uri: https://auth.example.com/.well-known/jwks.json
```

### 설정

```java
@Configuration
@EnableWebSecurity
public class OAuth2ResourceServerConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 ->
                oauth2.jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter()))
            )
            .build();
    }

    // JWT claims를 Spring Security authorities로 변환
    @Bean
    public JwtAuthenticationConverter jwtAuthConverter() {
        JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
        grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");
        grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");

        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
        return converter;
    }
}
```

---

## Token TTL 권장값

| 토큰 타입 | 권장 TTL | 이유 |
|----------|---------|------|
| Access Token | 15분 | 탈취 시 피해 최소화 |
| Refresh Token | 7일 | 사용자 경험 유지 |
| Remember Me | 30일 | 명시적 동의 시 |

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| Access Token 만료 너무 김 | 15분 이하 권장 |
| Refresh Token DB 미저장 | Redis/DB에 저장하여 무효화 가능하게 |
| 토큰 로그 출력 | 절대 금지 |
| Secret 코드에 하드코딩 | 환경변수 또는 Vault |

---

## 체크리스트

- [ ] JWT Secret 환경변수화 (최소 256bit)
- [ ] Access Token TTL 15분 이하
- [ ] Refresh Token 저장소 (Redis/DB)
- [ ] Refresh Token 무효화 로직 (로그아웃)
- [ ] 토큰 갱신 API 구현
- [ ] HTTPS 필수 적용
