---
name: init-java-project
description: Initialize a complete Java project with Maven/Gradle build, testing framework, and standard structure. Use when starting Spring Boot applications, Maven.
---

# Initialize Java Project

Create a complete, production-ready Java project with Maven or Gradle build configuration, testing framework, and enterprise-standard structure.

## When to Use This Skill

Use this skill when you need to:

- Start a new Java project from scratch
- Create Spring Boot applications
- Build Maven/Gradle libraries
- Set up enterprise Java applications
- Configure JUnit testing framework
- Establish CI/CD pipelines for Java

**Trigger phrases**: "init java project", "new java project", "create spring boot project", "maven project setup", "gradle init", "java boilerplate"

## What This Skill Does

### Project Structure Created (Maven)

```
project-name/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           └── projectname/
│   │   │               ├── Application.java
│   │   │               ├── config/
│   │   │               ├── controller/
│   │   │               ├── service/
│   │   │               ├── repository/
│   │   │               └── model/
│   │   └── resources/
│   │       ├── application.yml
│   │       └── logback.xml
│   └── test/
│       ├── java/
│       │   └── com/
│       │       └── example/
│       │           └── projectname/
│       │               └── ApplicationTest.java
│       └── resources/
│           └── application-test.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── pom.xml
├── CHANGELOG.md
└── README.md
```

## Instructions

### Step 1: Gather Project Requirements

```
Project Details:
- Name: [project-name]
- Group ID: [com.example]
- Artifact ID: [project-name]
- Version: [0.1.0-SNAPSHOT]
- Java Version: [17 / 21]
- Build Tool: [Maven / Gradle]
- Type: [Spring Boot / Library / CLI]

Dependencies:
- Spring Boot version: [3.2.x]
- Database: [PostgreSQL / MySQL / H2]
- Additional: [Spring Security, Spring Data JPA]
```

### Step 2: Create Maven Project (pom.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>project-name</artifactId>
    <version>0.1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Project Name</name>
    <description>Project description</description>

    <properties>
        <java.version>17</java.version>
        <maven.compiler.source>${java.version}</maven.compiler.source>
        <maven.compiler.target>${java.version}</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

        <!-- Dependency versions -->
        <lombok.version>1.18.30</lombok.version>
        <mapstruct.version>1.5.5.Final</mapstruct.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Developer Tools -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>

            <!-- Compiler Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>${java.version}</source>
                    <target>${java.version}</target>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>

            <!-- Surefire Plugin for Tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.2</version>
            </plugin>

            <!-- JaCoCo for Code Coverage -->
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <version>0.8.11</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>prepare-agent</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>report</id>
                        <phase>test</phase>
                        <goals>
                            <goal>report</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### Step 3: Create Application Entry Point

```java
// src/main/java/com/example/projectname/Application.java
package com.example.projectname;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import lombok.extern.slf4j.Slf4j;

/**
 * Main application entry point.
 *
 * @author Your Name
 * @version 0.1.0
 */
@Slf4j
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
        log.info("Application started successfully!");
    }
}
```

### Step 4: Create Configuration

```yaml
# src/main/resources/application.yml
spring:
  application:
    name: project-name

  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:

  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        format_sql: true

  h2:
    console:
      enabled: true
      path: /h2-console

server:
  port: 8080
  servlet:
    context-path: /api

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: always

logging:
  level:
    root: INFO
    com.example.projectname: DEBUG
    org.springframework: INFO
    org.hibernate: WARN
```

### Step 5: Create Service Layer Example

```java
// src/main/java/com/example/projectname/service/GreetingService.java
package com.example.projectname.service;

import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

/**
 * Service for greeting operations.
 */
@Slf4j
@Service
public class GreetingService {

    /**
     * Generate a greeting message.
     *
     * @param name the name to greet
     * @return greeting message
     */
    public String greet(String name) {
        log.debug("Generating greeting for: {}", name);
        return String.format("Hello, %s!", name);
    }
}
```

### Step 6: Create Controller

```java
// src/main/java/com/example/projectname/controller/GreetingController.java
package com.example.projectname.controller;

import com.example.projectname.service.GreetingService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;

/**
 * REST controller for greeting endpoints.
 */
@RestController
@RequestMapping("/greetings")
@RequiredArgsConstructor
public class GreetingController {

    private final GreetingService greetingService;

    /**
     * Get a greeting for the specified name.
     *
     * @param name the name to greet
     * @return greeting response
     */
    @GetMapping("/{name}")
    public ResponseEntity<String> greet(@PathVariable String name) {
        String greeting = greetingService.greet(name);
        return ResponseEntity.ok(greeting);
    }

    /**
     * Health check endpoint.
     *
     * @return health status
     */
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("OK");
    }
}
```

### Step 7: Create Tests

```java
// src/test/java/com/example/projectname/ApplicationTest.java
package com.example.projectname;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ApplicationTest {

    @Test
    void contextLoads() {
        // Verifies that the Spring context loads successfully
    }
}
```

```java
// src/test/java/com/example/projectname/service/GreetingServiceTest.java
package com.example.projectname.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("GreetingService Tests")
class GreetingServiceTest {

    private GreetingService greetingService;

    @BeforeEach
    void setUp() {
        greetingService = new GreetingService();
    }

    @Test
    @DisplayName("Should return greeting with name")
    void greet_ShouldReturnGreetingWithName() {
        // Given
        String name = "World";

        // When
        String result = greetingService.greet(name);

        // Then
        assertEquals("Hello, World!", result);
    }

    @Test
    @DisplayName("Should handle empty name")
    void greet_ShouldHandleEmptyName() {
        // Given
        String name = "";

        // When
        String result = greetingService.greet(name);

        // Then
        assertEquals("Hello, !", result);
    }
}
```

```java
// src/test/java/com/example/projectname/controller/GreetingControllerTest.java
package com.example.projectname.controller;

import com.example.projectname.service.GreetingService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(GreetingController.class)
class GreetingControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private GreetingService greetingService;

    @Test
    void greet_ShouldReturnGreeting() throws Exception {
        // Given
        when(greetingService.greet("World")).thenReturn("Hello, World!");

        // When & Then
        mockMvc.perform(get("/greetings/World"))
                .andExpect(status().isOk())
                .andExpect(content().string("Hello, World!"));
    }

    @Test
    void health_ShouldReturnOk() throws Exception {
        mockMvc.perform(get("/greetings/health"))
                .andExpect(status().isOk())
                .andExpect(content().string("OK"));
    }
}
```

### Step 8: Create .gitignore

```
# Compiled class files
*.class

# Build directories
target/
build/
out/

# IDE
.idea/
*.iml
*.ipr
*.iws
.project
.classpath
.settings/
.vscode/

# Maven
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next

# Gradle
.gradle/
gradle-app.setting
!gradle-wrapper.jar

# Package files
*.jar
*.war
*.ear
*.nar

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Environment
.env
*.env.local
```

### Step 9: Create CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: maven

      - name: Build with Maven
        run: mvn clean verify

      - name: Run tests
        run: mvn test

      - name: Generate coverage report
        run: mvn jacoco:report

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: target/site/jacoco/jacoco.xml
```

### Step 10: Build and Run

```bash
# Build project
mvn clean package

# Run tests
mvn test

# Run application
mvn spring-boot:run

# Or run JAR directly
java -jar target/project-name-0.1.0-SNAPSHOT.jar
```

## Gradle Alternative

```groovy
// build.gradle
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
    id 'jacoco'
}

group = 'com.example'
version = '0.1.0-SNAPSHOT'

java {
    sourceCompatibility = '17'
}

configurations {
    compileOnly {
        extendsFrom annotationProcessor
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'

    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'

    runtimeOnly 'com.h2database:h2'

    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

tasks.named('test') {
    useJUnitPlatform()
    finalizedBy jacocoTestReport
}

jacocoTestReport {
    dependsOn test
    reports {
        xml.required = true
        html.required = true
    }
}
```

## Quality Checklist

- [ ] pom.xml/build.gradle configured
- [ ] Project compiles successfully
- [ ] Tests pass
- [ ] Application starts
- [ ] Actuator endpoints accessible
- [ ] Code coverage > 80%
- [ ] CI workflow configured
- [ ] Documentation complete
- [ ] Git initialized

## Related Skills

- `test-structure` - Set up comprehensive testing
- `java-cleanup` - Code cleanup
- `api-documentation` - Document APIs
- `security-review` - Security assessment

---

**Version**: 1.0.0
**Last Updated**: December 2025


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
