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

## 3. The `toByteBuffer()` function with no params has been deprecated.

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
            val bytes = ByteArray(it.readableByteCount())
            it.read(bytes)
            s3AsyncClient.putObject(
                putObjectRequest,
                AsyncRequestBody.fromBytes(bytes)
            )
        }.then()
    }
}
```

Essentially, this means replacing calls to it.asByteBuffer().array() with a more explicit way of creating a ByteBuffer, writing the data into it, and then flipping it before getting the byte array.

## 4. Follow OAuth2 Guidelines for dependencies coming from deprecated `org.springframework.security.oauth2` package

`OAuth2` from dependencies `org.springframework.security.oauth2` has been deprecated. There is a guideline manual located at: https://github.com/spring-projects/spring-security/wiki/OAuth-2.0-Migration-Guide
Please make sure that the new code follows the guidelines. Make the eventual necessary changes to the `pom.xml` files, code, en what may be necessary.

## 5. `ApplicationArguments` cannot be null anymore and `args` has to be a list of non-null Strings

please replace `override fun run(args: ApplicationArguments?)` with `override fun run(args: ApplicationArguments?)`
please replace `return CommandLineRunner { args: Array<String?>?` with `return CommandLineRunner { args: Array<String>`

## 6. `import org.springframework.boot.env.EnvironmentPostProcessor` needs to be replaced by `import org.springframework.boot.EnvironmentPostProcessor`

The `EnvironmentPostProcessor` is now part of the `import org.springframework.boot` package.

## 7. Make sure to use classes for `@Entity` with primary constructor

Good practices mean that classes for entities should be created by declaring a primary constructor with all of the properties.

### Example 1

Replace this:

```kotlin
@Entity
@Table(name = "users")
@Profile("localprod && !test")
class ApplicationUser {
    @Id
    @Column(unique = true)
    @GeneratedValue(strategy = GenerationType.UUID)
    var uuid: UUID? = null

    @Column
    var email: String? = null

    @Column
    var name: String? = null

    @Column
    var password: String? = null

    @Column
    var role: String? = null

    @get:Nullable
    @Column
    @Nullable
    var date: Timestamp? = null
}
```

with this:

```kotlin
@Entity
@Table(name = "users")
@Profile("localprod && !test")
class ApplicationUser(
    @Id
    @Column(unique = true)
    @GeneratedValue(strategy = GenerationType.UUID)
    var uuid: UUID? = null,

    @Column
    val email: String? = null,

    @Column
    var name: String? = null,

    @Column
    var password: String? = null,

    @Column
    val role: String? = null,

    @get:Nullable
    @Column
    @Nullable
    var date: Timestamp? = null
)
```

## 8. `@Nullable` needs to be used from another package

The `org.springframework.lang.Nullable` is deprecated, please use `org.jspecify.annotations.Nullable` instead.

## 9. management.metrics.export.statsd.host does not exist

Replace all usages of `management.metrics.export.statsd.host` with `management.statsd.metrics.export.host`

## 10. There should be no `open` use when the spring kotlin plugin is being used

Since the `spring`, or the `all-open` plugins make methods, functions, and classes open by default, the `open` keyword should not be used.

## 11. Migrate to the latest version of spring-boot

In maven projects, there should be a node called `spring-boot-starter-parent.version` in the `pom.xml` or something similar that indicates the parent version of `spring-boot` it is being used.
That version should match the latest stable version.
Make sure to follow the migration rules to migrate to the latest version of spring-boot.
If the axon framework is being used, make sure to migrate it to be compatible with the latest spring version.

For reference, please follow the following documents:

1. https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.5-Release-Notes
2. https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide
3. https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.1-Release-Notes
4. https://docs.axoniq.io/axon-framework-reference/5.2/migration/

## 12. Checklist

[ ] All old security configurations have been updated to the new style.
[ ] All usages of `NestedServletException` have been replaced with `ServletException`.
[ ] All usages of `DataBuffer.toByteBuffer` have been replaced with a more explicit ay of creating a ByteBuffer and getting the byte array.
[ ] There should be no `override fun run(args: ApplicationArguments?)` left
[ ] There should be no `import org.springframework.boot.env.EnvironmentPostProcessor` left
[ ] There should be no usage of the keyword `open`, when using plugins `spring` or `all-open`
