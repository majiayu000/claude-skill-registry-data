---
name: tech-stack-config
description: Spring Boot 3.4.4 and Java 17 tech stack configuration, package structure conventions, and coding patterns for consistent API development. Use this when generating designs, implementing features, or reviewing code to ensure alignment with the project's established tech stack and conventions.
allowed-tools: Read(*), Glob(*), Grep(*)
---

# Tech Stack Configuration Skill

This skill provides comprehensive configuration context for the hello-spring-boot project. All new features should follow this established tech stack and architectural patterns.

---

## Technology Stack

**Core Framework:**
- **Spring Boot**: 3.4.4 (current version)
- **Java**: 17 (LTS, required)
- **Gradle**: 8.13
- **Build Tool**: Gradle with Spring Boot plugin

**Database Layer:**
- **Database**: PostgreSQL 15 (Docker container on port 5432)
- **Database Name**: hello-spring-db
- **Username**: postgres
- **Password**: datpt
- **Connection Pool**: HikariCP (max 10 connections)
- **ORM**: Spring Data JPA with Hibernate
- **Migration Tool**: Flyway for database version control
- **JDBC Driver**: PostgreSQL 42.x

**Testing:**
- **Framework**: JUnit 5
- **Mocking**: Mockito
- **Spring Test**: @SpringBootTest, @WebMvcTest, @DataJpaTest
- **Integration Testing**: MockMvc for controller tests

**Build & Utilities:**
- **Lombok**: For boilerplate reduction (@Data, @RequiredArgsConstructor, @Slf4j, etc.)
- **Config Format**: application.properties (not YAML)

**Containerization:**
- **Docker & Docker Compose**: For PostgreSQL + pgAdmin setup
- **pgAdmin 4**: Port 5050 for database administration (email: admin@admin.com, password: admin)

---

## Package Structure Pattern

**Base Package:** `com.example.hellospringboot`

**Organization Style:** Layer-based structure (NOT feature-based)

```
src/main/java/com/example/hellospringboot/
├── controller/                       # REST API controllers
├── service/                          # Business logic layer
├── repository/                       # Spring Data JPA repositories
├── entity/                           # JPA entities (@Entity)
├── dto/                             # Data Transfer Objects (request/response)
├── exception/                        # Custom exception classes
└── HelloSpringBootApplication.java   # Main application entry point

src/main/resources/
├── application.properties            # Configuration
└── db/migration/                     # Flyway migration scripts
    └── V{n}__{description}.sql
```

**Important:** The project uses a flat, layer-based package structure (NOT feature-based like `com.example.app.student.controller`).

---

## Naming Conventions

### Entity Naming
- **Entities**: Singular noun (e.g., `Student.java`, `Program.java`)
- **Table names**: Lowercase, singular (e.g., `@Table(name="student")`, `@Table(name="program")`)
- **Field names**: camelCase in Java (e.g., `firstName`, `lastName`)
- **Column names**: Lowercase in database, mapped via `@Column(name="first_name")`

### Service Layer
- **Interface**: `[Entity]Service.java` (e.g., `StudentService.java`)
- **Implementation**: `[Entity]ServiceImpl.java` (e.g., `StudentServiceImpl.java`)
- **Annotation**: `@Service`
- **Lombok**: `@Slf4j` and `@RequiredArgsConstructor` for constructor injection

### Repository Layer
- **Class name**: `[Entity]Repository.java` (e.g., `StudentRepository.java`)
- **Extension**: `extends JpaRepository<[Entity], ID_Type>`
- **Annotation**: `@Repository` (optional, Spring auto-detects interfaces extending JpaRepository)

### Controller Layer
- **Class name**: `[Entity]Controller.java` (e.g., `StudentController.java`)
- **Annotation**: `@RestController`
- **Base path annotation**: `@RequestMapping("/api/[plural-entity]")` (e.g., `/api/students`)
- **Lombok**: `@RequiredArgsConstructor` for constructor injection

### Exception Classes
- **Pattern**: `[Entity]NotFoundException.java`, `Invalid[Entity]Exception.java`
- **Example**: `StudentNotFoundException.java`
- **Parent class**: Extend `RuntimeException`
- **Global Handler**: Use `@ControllerAdvice` with `@ExceptionHandler`

### DTOs
- **Response**: `[Entity]NameResponse.java` or `[Entity]Response.java` (e.g., `StudentNameResponse.java`)
- **Request**: `[Entity]Request.java` (e.g., `CreateStudentRequest.java`)
- **Error**: `ErrorResponse.java` (global error response DTO)

---

## Code Patterns & Annotations

### Service Layer Pattern

```java
package com.example.hellospringboot.service;

import com.example.hellospringboot.dto.StudentResponse;
import com.example.hellospringboot.entity.Student;
import com.example.hellospringboot.exception.StudentNotFoundException;
import com.example.hellospringboot.repository.StudentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
@RequiredArgsConstructor
public class StudentServiceImpl implements StudentService {

    private final StudentRepository studentRepository;

    @Override
    @Transactional(readOnly = true)
    public StudentResponse getStudentById(Integer id) {
        log.info("Getting student with ID: {}", id);

        Student student = studentRepository.findById(id)
            .orElseThrow(() -> new StudentNotFoundException("Student with ID " + id + " not found"));

        log.info("Student retrieved successfully: ID={}", id);
        return StudentResponse.from(student);
    }

    @Override
    @Transactional
    public StudentResponse createStudent(CreateStudentRequest request) {
        log.info("Creating new student: {}", request.getName());

        Student student = new Student();
        student.setName(request.getName());

        Student saved = studentRepository.save(student);
        log.info("Student created successfully: ID={}", saved.getId());

        return StudentResponse.from(saved);
    }
}
```

**Key patterns to follow:**
- Constructor injection with `@RequiredArgsConstructor` (Lombok)
- `@Slf4j` for logging (Lombok annotation)
- Service interface with implementation class
- `@Transactional(readOnly=true)` for read operations
- `@Transactional` (without params) for write operations
- Log important events (requests, successes, failures)

### Controller Layer Pattern

```java
package com.example.hellospringboot.controller;

import com.example.hellospringboot.dto.StudentResponse;
import com.example.hellospringboot.service.StudentService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/students")
@RequiredArgsConstructor
@Slf4j
public class StudentController {

    private final StudentService studentService;

    @GetMapping("/{id}")
    public ResponseEntity<StudentResponse> getStudent(@PathVariable Integer id) {
        log.info("Received request to get student: ID={}", id);
        StudentResponse response = studentService.getStudentById(id);
        return ResponseEntity.ok(response);
    }

    @PostMapping
    public ResponseEntity<StudentResponse> createStudent(@Valid @RequestBody CreateStudentRequest request) {
        log.info("Received request to create student");
        StudentResponse response = studentService.createStudent(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteStudent(@PathVariable Integer id) {
        log.info("Received request to delete student: ID={}", id);
        studentService.deleteStudent(id);
        return ResponseEntity.noContent().build();
    }
}
```

**Key patterns:**
- `@RestController` annotation
- Constructor injection for services (`@RequiredArgsConstructor`)
- `@RequestMapping` for base path
- `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` for endpoints
- `@PathVariable` for URL parameters
- `@RequestBody` with `@Valid` for request validation
- `ResponseEntity` for HTTP responses with proper status codes
- Logging at controller level

### Repository Pattern

```java
package com.example.hellospringboot.repository;

import com.example.hellospringboot.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.List;

@Repository
public interface StudentRepository extends JpaRepository<Student, Integer> {

    // Spring Data JPA auto-implements findById(Integer id)

    // Custom query methods following Spring Data naming conventions
    Optional<Student> findByName(String name);
    List<Student> findByNameContaining(String keyword);
    boolean existsByName(String name);
}
```

**Key patterns:**
- Extend `JpaRepository<Entity, ID_Type>`
- Method naming follows Spring Data conventions
- Return `Optional<T>` for single results that might not exist
- Return `List<T>` for multiple results
- Use `boolean` for existence checks (`existsBy...`)

### Entity Pattern

```java
package com.example.hellospringboot.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "student")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Student {

    @Id
    @Column(name = "id")
    private Integer id;

    @Column(name = "name", length = 255, nullable = false)
    private String name;
}
```

**Key patterns:**
- `@Entity` and `@Table` annotations
- `@Data` from Lombok for getters/setters/toString/equals/hashCode
- `@NoArgsConstructor` and `@AllArgsConstructor` from Lombok
- `@Id` for primary key
- `@Column` annotations with constraints (length, nullable, unique)
- Use `@GeneratedValue(strategy = GenerationType.IDENTITY)` for auto-increment IDs

### Exception Handling Pattern

**Custom Exception:**
```java
package com.example.hellospringboot.exception;

public class StudentNotFoundException extends RuntimeException {
    public StudentNotFoundException(String message) {
        super(message);
    }
}
```

**Global Exception Handler:**
```java
package com.example.hellospringboot.exception;

import com.example.hellospringboot.dto.ErrorResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(StudentNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleStudentNotFound(StudentNotFoundException ex) {
        log.warn("Student not found: {}", ex.getMessage());

        ErrorResponse error = ErrorResponse.of(
            "STUDENT_NOT_FOUND",
            ex.getMessage()
        );

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(DataAccessException.class)
    public ResponseEntity<ErrorResponse> handleDatabaseError(DataAccessException ex) {
        log.error("Database error: {}", ex.getMessage(), ex);

        ErrorResponse error = ErrorResponse.of(
            "DATABASE_ERROR",
            "Unable to process request due to database error"
        );

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericError(Exception ex) {
        log.error("Unexpected error: {}", ex.getMessage(), ex);

        ErrorResponse error = ErrorResponse.of(
            "INTERNAL_ERROR",
            "An unexpected error occurred"
        );

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### DTO Pattern

```java
package com.example.hellospringboot.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class StudentResponse {
    private String id;
    private String name;

    public static StudentResponse from(Integer id, String name) {
        return new StudentResponse(String.valueOf(id), name);
    }
}
```

### Validation Annotations

Used on DTO request classes:
```java
import jakarta.validation.constraints.*;

@NotNull(message = "Name is required")
@NotBlank(message = "Name cannot be blank")
@Size(min = 1, max = 255, message = "Name must be between 1 and 255 characters")
@Pattern(regexp = "^[a-zA-Z0-9 ]+$", message = "Name can only contain letters, numbers, and spaces")
@Email(message = "Email must be valid")
```

---

## Database Migration with Flyway

**Migration File Location:** `src/main/resources/db/migration/`

**Naming Convention:** `V{version}__{description}.sql`

**Examples:**
- `V1__Create_student_table.sql`
- `V2__Add_program_table.sql`
- `V3__Add_foreign_keys.sql`

**Migration Example:**
```sql
-- V1__Create_student_table.sql
CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
```

**Configuration in application.properties:**
```properties
spring.flyway.enabled=true
spring.flyway.baseline-on-migrate=true
spring.flyway.locations=classpath:db/migration
spring.jpa.hibernate.ddl-auto=validate
```

**Important Rules:**
- **Never modify** existing migration files after they've been applied
- **Always create new migrations** for schema changes
- Hibernate uses `validate` mode - it validates but doesn't auto-create/alter tables
- Use Flyway for all DDL changes (CREATE, ALTER, DROP)

---

## HTTP Status Codes

Use these standard HTTP status codes in controllers:

| Code | Meaning | When to Use |
|------|---------|-------------|
| **200 OK** | Success | Successful GET, PUT (update) |
| **201 Created** | Resource created | Successful POST (new resource) |
| **204 No Content** | Success, no body | Successful DELETE |
| **400 Bad Request** | Validation error | Invalid input, failed validation |
| **404 Not Found** | Resource not found | Entity doesn't exist |
| **409 Conflict** | Conflict | Duplicate entries, constraint violations |
| **500 Internal Server Error** | Server error | Unexpected errors, database failures |

**Example:**
```java
return ResponseEntity.ok(response);                    // 200
return ResponseEntity.status(HttpStatus.CREATED).body(response); // 201
return ResponseEntity.noContent().build();             // 204
return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);  // 404
```

---

## Development Workflow

### Build Commands
```bash
./gradlew build              # Build the project
./gradlew bootRun           # Run the application
./gradlew clean             # Clean build artifacts
./gradlew build -x test     # Build without tests
```

### Testing
```bash
./gradlew test                                          # Run all tests
./gradlew test --tests HelloSpringBootApplicationTests # Single test
./gradlew test --tests "*ControllerTests"             # Pattern match
```

### Database (Docker)
```bash
cd docker
docker-compose up -d        # Start PostgreSQL + pgAdmin
docker-compose down         # Stop services
docker-compose logs -f      # View logs
docker-compose restart      # Restart services
```

**Access Information:**
- PostgreSQL: `localhost:5432` (user: postgres, password: datpt, database: hello-spring-db)
- pgAdmin: `http://localhost:5050` (email: admin@admin.com, password: admin)

### Flyway Commands
```bash
./gradlew flywayInfo        # Check migration status
./gradlew flywayValidate    # Validate migrations
./gradlew flywayRepair      # Repair migration history (use with caution)
./gradlew flywayClean       # Clean database (WARNING: deletes all data)
```

---

## Important Notes

### Database Credentials
**Development Only** - Hardcoded in application.properties:
- Host: localhost:5432
- User: postgres
- Password: datpt
- Database: hello-spring-db

⚠️ **Production**: Use environment variables or secure credential management

### Connection Pool Configuration
```properties
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.auto-commit=true
spring.datasource.hikari.max-lifetime=300000
```

### Known Issues
- Existing `Program` entity may have legacy code or typos
- Table naming: Use singular, lowercase (e.g., `student`, not `students`)
- Field naming in entities should be camelCase (e.g., `firstName`, not `first_name`)

---

## When to Use This Skill

Claude will automatically reference this skill when:
- Generating technical design documents (`/generate-design`)
- Implementing new features (`/implement-database`, `/implement-service`, `/implement-api`)
- Reviewing code for consistency
- Creating new entities, services, controllers, or repositories
- Planning database migrations
- Setting up error handling patterns

---

## Example: Creating a New Feature (Course Management)

When implementing a new "Course" feature:

1. **Entity**: `Course.java` (singular)
   - Package: `com.example.hellospringboot.entity`
   - Table: `@Table(name="course")` (singular, lowercase)
   - Lombok: `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

2. **Repository**: `CourseRepository.java`
   - Package: `com.example.hellospringboot.repository`
   - Extends: `JpaRepository<Course, Long>`

3. **Service**: `CourseService.java` (interface) + `CourseServiceImpl.java`
   - Package: `com.example.hellospringboot.service`
   - Annotations: `@Service`, `@Slf4j`, `@RequiredArgsConstructor`
   - Use `@Transactional` appropriately

4. **Controller**: `CourseController.java`
   - Package: `com.example.hellospringboot.controller`
   - Annotations: `@RestController`, `@RequestMapping("/api/courses")`
   - Lombok: `@RequiredArgsConstructor`, `@Slf4j`

5. **DTOs**: `CourseResponse.java`, `CreateCourseRequest.java`
   - Package: `com.example.hellospringboot.dto`

6. **Exceptions**: `CourseNotFoundException.java`
   - Package: `com.example.hellospringboot.exception`

7. **Migration**: `V{n}__Add_course_table.sql`
   - Location: `src/main/resources/db/migration/`

---

## Summary

This skill ensures that all generated code and documentation follows:
- ✅ Spring Boot 3.4.4 + Java 17
- ✅ PostgreSQL 15 with Flyway migrations
- ✅ Layer-based package structure
- ✅ Consistent naming conventions
- ✅ Lombok for boilerplate reduction
- ✅ Constructor injection with `@RequiredArgsConstructor`
- ✅ Proper transaction management
- ✅ Comprehensive logging with `@Slf4j`
- ✅ Global exception handling
- ✅ Proper HTTP status codes
