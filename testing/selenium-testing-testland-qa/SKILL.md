---
name: selenium-testing
description: "Authors Selenium WebDriver tests in any of its 6+ supported languages (Java, Python, JavaScript, C#, Ruby, Kotlin, PHP) - picks the appropriate language binding, configures WebDriver per browser, uses `By.*` locators with the team's accessibility-first preference where supported, runs locally + via Selenium Grid for distributed execution, parses results to JUnit XML. Use for legacy Selenium-locked stacks; new projects pick Playwright or Cypress."
---

# selenium-testing

## Overview

Selenium WebDriver is a W3C-standard browser automation protocol with
the broadest language support: Java, Python, JavaScript, C#, Ruby,
Kotlin, PHP - all official.

## When to use

- The team has substantial existing Selenium investment; migration
  cost is prohibitive.
- The codebase is in a language with limited modern E2E support
  (e.g., older C# / Ruby / PHP projects).
- W3C standard adherence is contractually required.
- Cross-browser including IE11 is required (rare; deprecated).

For new projects in 2026+: pick Playwright or Cypress unless
constraints dictate Selenium.

## How to use

1. Pick the language binding that matches the stack (Java, Python, C#, Ruby, Kotlin, PHP) and add the Selenium dependency plus WebDriverManager.
2. Instantiate a driver in setup and `quit()` it in teardown so no browser process leaks.
3. Prefer stable `By.cssSelector` / `data-testid` locators; keep XPath for relationship queries only.
4. Replace every `Thread.sleep()` with `WebDriverWait` + `ExpectedConditions` so the test waits on a condition, not a clock.
5. Author one test per user flow with fresh per-test setup rather than one giant flow.
6. For breadth, point a `RemoteWebDriver` at Selenium Grid (or a managed grid) to fan out across browsers.
7. Emit JUnit XML in CI (`target/surefire-reports/`) and feed it to `junit-xml-analysis`.

## Step 1 - Install (Java + JUnit example)

```xml
<!-- pom.xml -->
<dependency>
  <groupId>org.seleniumhq.selenium</groupId>
  <artifactId>selenium-java</artifactId>
  <version>4.27.0</version>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>io.github.bonigarcia</groupId>
  <artifactId>webdrivermanager</artifactId>
  <version>5.9.2</version>
  <scope>test</scope>
</dependency>
```

WebDriverManager handles browser-driver download (saves the
"download chromedriver.exe" step).

## Step 2 - Author a test (Java)

```java
import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.*;
import io.github.bonigarcia.wdm.WebDriverManager;

import java.time.Duration;

class CheckoutTest {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeAll
    static void setupClass() {
        WebDriverManager.chromedriver().setup();
    }

    @BeforeEach
    void setup() {
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @AfterEach
    void teardown() {
        driver.quit();
    }

    @Test
    void completeCheckout() {
        driver.get("http://localhost:3000/login");

        driver.findElement(By.cssSelector("[data-testid=email]"))
              .sendKeys("user@example.com");
        driver.findElement(By.cssSelector("[data-testid=password]"))
              .sendKeys("test-password");
        driver.findElement(By.cssSelector("button[type=submit]")).click();

        wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.xpath("//h1[contains(text(), 'Welcome')]")));

        driver.get("http://localhost:3000/products/BOOK-001");
        driver.findElement(By.cssSelector("[data-testid=add-to-cart]")).click();

        WebElement cartCount = driver.findElement(By.cssSelector("[data-testid=cart-count]"));
        Assertions.assertEquals("1", cartCount.getText());
    }
}
```

## Step 3 - Locator strategies

| Strategy             | When                                         |
|----------------------|----------------------------------------------|
| `By.id`               | Element has stable `id`                       |
| `By.name`             | Form field with `name` attribute              |
| `By.cssSelector`      | Most cases (preferred over XPath)             |
| `By.xpath`            | Complex relationship queries (avoid otherwise) |
| `By.linkText`         | Anchor by text                                 |
| `By.partialLinkText`  | Anchor by partial text                          |
| `By.tagName`          | Generic (e.g., all `input` elements)           |
| `By.className`        | Single CSS class (brittle)                      |

Prefer `data-testid` selectors; avoid XPath / classes.

For accessibility-first equivalents (Selenium doesn't ship
`getByRole` natively), evaluate **selenium-axe-core** for a11y
testing and consider Selenium 4's relative locators:

```java
// Selenium 4 relative locators
import static org.openqa.selenium.support.locators.RelativeLocator.*;

driver.findElement(with(By.tagName("button")).near(By.id("password-field")));
```

## Step 4 - Explicit waits

```java
// WebDriverWait with ExpectedConditions
WebElement element = wait.until(
    ExpectedConditions.elementToBeClickable(By.cssSelector("button.submit"))
);
element.click();
```

**Never use `Thread.sleep()`** - `WebDriverWait` polls until the
condition is met. Sleep is the most common Selenium flake source.

## Step 5 - Selenium Grid for distributed execution

```yaml
# docker-compose.grid.yml
services:
  selenium-hub:
    image: selenium/hub:4.27.0
    ports: ["4444:4444"]

  chrome-node:
    image: selenium/node-chrome:4.27.0
    depends_on: [selenium-hub]
    environment:
      SE_EVENT_BUS_HOST: selenium-hub
      SE_EVENT_BUS_PUBLISH_PORT: 4442
      SE_EVENT_BUS_SUBSCRIBE_PORT: 4443

  firefox-node:
    image: selenium/node-firefox:4.27.0
    # ... same env
```

Connect from tests:

```java
WebDriver driver = new RemoteWebDriver(
    new URL("http://localhost:4444"),
    new ChromeOptions()
);
```

Grid distributes tests across nodes - handles parallelism. For
managed grids, see commercial: BrowserStack, Sauce Labs,
LambdaTest.

Verify: `curl http://localhost:4444/status` reports `"ready": true`
before pointing `RemoteWebDriver` at the grid; if not, the hub or nodes
haven't registered - check `docker compose -f docker-compose.grid.yml ps`
and the node container logs.

## Step 6 - Other language bindings

The Java spine above ports 1:1 to Selenium's other official bindings.
Python (pytest) and C# (xUnit) worked examples:
[references/language-bindings.md](references/language-bindings.md).

## Step 7 - CI integration

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21' }
      - run: mvn test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: surefire-reports
          path: target/surefire-reports/
```

JUnit XML lands at `target/surefire-reports/`; feeds
`junit-xml-analysis` (in the qa-test-reporting plugin).

Verify: confirm `target/surefire-reports/*.xml` exists after `mvn test`
before handing off to `junit-xml-analysis`; if the directory is empty the
run emitted no reports - check that tests compiled and actually ran rather
than being skipped.

## Worked example

A legacy Java suite has one `CheckoutTest` method that drives login,
add-to-cart, and checkout in a single flow, synchronizing with
`Thread.sleep(2000)` between steps and never calling `driver.quit()`.
Browser processes leak on CI and the test flakes when the runner is
slow.

1. The single method is split into per-behavior `@Test` methods, each
   with `@BeforeEach` creating a fresh `ChromeDriver` and `@AfterEach`
   calling `driver.quit()`.
2. Every `Thread.sleep(2000)` is replaced with
   `wait.until(ExpectedConditions.elementToBeClickable(...))` so the
   step blocks only until the element is ready.
3. Class-name selectors move to `By.cssSelector("[data-testid=...]")`,
   and the hardcoded chromedriver path is dropped for
   `WebDriverManager.chromedriver().setup()`.
4. A Dockerized Selenium Grid is added and tests connect via
   `RemoteWebDriver`, so Chrome and Firefox run on parallel nodes.
5. `mvn test` writes JUnit XML to `target/surefire-reports/`, which
   `junit-xml-analysis` ingests for the flake trend.

Result: browsers no longer leak (every test quits its driver), the
fixed sleeps are gone, and the flow runs across two browsers on the
grid.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Single test class with one giant flow                                 | Failure mid-test obscures cause.                                         | Per-flow tests with `@BeforeEach` setup. |
| Skipping `driver.quit()`                                              | Browser instance leaks; CI runner OOM.                                  | Always `quit()` in `@AfterEach` (Step 2). |
| Hardcoded ChromeDriver path                                           | Drift; brittle to Chrome updates.                                        | WebDriverManager (Step 1). |

## Limitations

- **Slower than Playwright / Cypress.** WebDriver protocol overhead;
  per-action HTTP round-trips.
- **Async / Promise handling weaker.** Per-language; some
  frameworks better than others.
- **No native mobile.** Mobile via Appium (uses Selenium WebDriver
  protocol underneath) per `appium-testing` (in the qa-mobile plugin).
- **Per-language idioms vary.** A Python pytest test looks
  different from a Java JUnit test.

## References

- Selenium project at `selenium.dev`.
- W3C WebDriver spec.
- `playwright-testing`,
  `cypress-testing` - modern
  alternatives.
- `appium-testing` - mobile via WebDriver protocol.
