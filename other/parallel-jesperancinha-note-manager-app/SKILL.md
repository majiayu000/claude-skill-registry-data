---
name: parallelization
description: Conventions for using parallelization in all tests using Jupiter
---

# Add a JUnit properties file to all modules to make sure parallelization is enabled

Filename should be: `junit-platform.properties` and it should be placed in `src/test/resources` of each module.

Its content should be:

```properties
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.config.fixed.parallelism = 4
junit.jupiter.execution.parallel.config.dynamic.factor = 4.0
junit.jupiter.execution.parallel.mode.default = concurrent
junit.jupiter.execution.parallel.mode.classes.default = concurrent
```

Only add this file, and if the file doesn't exist. Do not override existing files.

Check if tests run successfully for every module where you add this file. If it fails, then remove the file.

In case they fail, the following should be tried

1. Add `@TestMethodOrder(OrderAnnotation::class)` to the test class
2. Add `@Execution(SAME_THREAD)` to the test methods that are failing
3. Add `@Order(1)` to the test methods that are failing. The number should be sequential for all failing tests

## Example 1

```kotlin

@SpringBootTest(webEnvironment = RANDOM_PORT)
@TestMethodOrder(OrderAnnotation::class)
class NarwhalsShopControllerTest @Autowired constructor(
    private val narwhalsWebShopDao: NarwhalsWebShopDao,
    private val testRestTemplate: TestRestTemplate,
) {
    val xmlHeaders = HttpHeaders().apply {
        add("Content-Type", APPLICATION_XML_VALUE)
    }
    val jsonHeaders = HttpHeaders().apply {
        add("Content-Type", APPLICATION_JSON_VALUE)
    }

    @Test
    fun `should load narwhals`() {
    }

    @Test
    fun `should make full purchase when stocks are available`() {
    }

    @Test
    @Execution(SAME_THREAD)
    fun `should make multiple purchase request but only one succeeds when stocks are available`(): Unit = runBlocking {
    }

    @Test
    @Execution(SAME_THREAD)
    fun `should make partial purchase when stocks are not available`() {
    }

    @Test
    fun `should make no purchase when stocks are not available and show predictions`() {
    }

    @Test
    @Execution(SAME_THREAD)
    @Order(1)
    fun `should return not found failed when nothing is available`() {
    }

}
```

If it still fails. Only here revert the changes made to the test class and remove the `junit-platform.properties` file.