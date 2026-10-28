---
name: spring
description: Conventions for dependency injection and mocking in Spring Boot in this project. Use this whenever writing, reviewing, or refactoring integration test classes (anything annotated @SpringBootTest, or under src/test that talks to a real Spring context), especially when deciding how to wire dependencies or mock collaborators. Also consult this before adding @Autowired, @MockBean, @MockitoBean, or field injection in any test class.
---

## 1. Spring Configuration improvements

All old security configurations need to be updated

For java this means that we should migrate as en example from something like this:

### Example 1

```java
public class Flash16ConfigurationAdapter {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http.authenticationProvider(new Flash16AuthenticationProvider())
                .authorizeRequests()
                .requestMatchers(new AntPathRequestMatcher("/**")).hasRole("ADMIN")
                .anyRequest()
                .authenticated()
                .and()
                .formLogin().and().build();
    }
}
```

to this

```java
public class Flash16ConfigurationAdapter {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .authenticationProvider(new Flash16AuthenticationProvider())
                .authorizeHttpRequests(auth -> auth
                        .anyRequest().hasRole("ADMIN")
                )
                .formLogin(Customizer.withDefaults())
                .build();
    }
}
```

### Example 2

Migrate from this:

```java
public class Flash17ConfigurationAdapter {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .userDetailsService(jdbcUserDetailsManager)
                .authorizeRequests()
                .requestMatchers(new AntPathRequestMatcher("/open/**"))
                .permitAll()
                .requestMatchers(new AntPathRequestMatcher("/**")).hasRole("ADMIN")
                .anyRequest()
                .authenticated()
                .and()
                .formLogin()
                .and().csrf().disable().build();
    }
}
```

to this

```shell
public class Flash17ConfigurationAdapter {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http.userDetailsService(jdbcUserDetailsManager)
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/open/**").permitAll()
                        .requestMatchers("/**").hasRole("ADMIN")
                        .anyRequest().authenticated()
                )
                .formLogin(Customizer.withDefaults())
                .csrf(AbstractHttpConfigurer::disable)
                .build();
}
```

## 2. Replace usage of `NestedServletException` with `ServletException`

NestedServletException has been deprecated.
This means that all usages of `org.springframework.web.util.NestedServletException` should be replaced with `jakarta.servlet.ServletException` in all test classes.

## 3. The `toByteBuffer` function has been deprecated.

This means that all usages of `org.springframework.core.io.buffer.DataBuffer.toByteBuffer` should be replaced with another way to get the byte array.

### Example 1


Replace this:

```kotlin
@RestController
@RequestMapping("images")
internal class StaCoImageController(
    val s3AsyncClient: S3AsyncClient
) {
    @PostMapping("/save/{id}")
    fun saveUser(
        @RequestPart(value = "image", required = false) filePartMono: Mono<FilePart>,
        @PathVariable("id") uuid: UUID
    ): Mono<Void> {
        return filePartMono.flatMapMany {
            it.content()
        }.map {
            val putObjectRequest =
                PutObjectRequest.builder().bucket(IMAGES_BUCKET).key("staco-image-$uuid.png").build()
            s3AsyncClient.putObject(
                putObjectRequest,
                AsyncRequestBody.fromBytes(it.asByteBuffer().array())
            )
        }.then()
    }
}
```

with this:


```kotlin
@RestController
@RequestMapping("images")
internal class StaCoImageController(
    val s3AsyncClient: S3AsyncClient
) {
    @PostMapping("/save/{id}")
    fun saveUser(
        @RequestPart(value = "image", required = false) filePartMono: Mono<FilePart>,
        @PathVariable("id") uuid: UUID
    ): Mono<Void> {
        return filePartMono.flatMapMany {
            it.content()
        }.map {
            val putObjectRequest =
                PutObjectRequest.builder().bucket(IMAGES_BUCKET).key("staco-image-$uuid.png").build()
            val buffer = ByteBuffer.allocate(it.readableByteCount())
            it.toByteBuffer(buffer)
            buffer.flip()
            s3AsyncClient.putObject(
                putObjectRequest,
                AsyncRequestBody.fromBytes(buffer.array())
            )
        }.then()
    }
}
```

Essentially, this means replacing calls to it.asByteBuffer().array() with a more explicit way of creating a ByteBuffer, writing the data into it, and then flipping it before getting the byte array.

## 4. Checklist

[ ] All old security configurations have been updated to the new style. 
[ ] All usages of `NestedServletException` have been replaced with `ServletException`.
[ ] All usages of `DataBuffer.toByteBuffer` have been replaced with a more explicit way of creating a ByteBuffer and getting the byte array.
