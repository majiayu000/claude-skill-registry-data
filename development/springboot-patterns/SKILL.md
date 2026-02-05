---
name: springboot-patterns
description: Spring Boot and Java best practices for SpecFlux backend. Use when developing REST APIs, services, repositories, or any Java code. Applies DDD architecture, OpenAPI-first workflow, transaction management, and test-driven development.
---

# Spring Boot Development Patterns

Spring Boot and Java best practices for SpecFlux backend. Use when developing REST APIs, services, repositories, or any Java code.

## Development Workflow

**ALWAYS follow this order when implementing API features:**

### 1. OpenAPI First
- Update `src/main/resources/openapi/api.yaml` with endpoint definition
- Define request/response DTOs in the spec
- Run `./mvnw compile` to generate interfaces and DTOs

### 2. Write Controller Test First
- Create test in `src/test/java/.../interfaces/rest/{Domain}ControllerTest.java`
- Extend `AbstractControllerIntegrationTest`
- Test happy path + error cases + auth scenarios
- Run test to see it fail (red)

### 3. Implement Controller
- Create controller implementing generated `{Domain}Api` interface
- Use `@Override` on all interface methods
- Delegate all logic to application service

### 4. Implement Application Service
- Create service in `{domain}/application/{Domain}ApplicationService.java`
- Use `TransactionTemplate` for explicit transactions
- Handle validation, business logic, and DTO conversion

### 5. Run Tests
- `./mvnw test` - all tests must pass
- `./mvnw spotless:check` - code formatting

### 6. Commit
- One commit per logical change
- Use conventional commit format

## Project Structure (DDD)

```
src/main/java/com/specflux/
├── {domain}/                    # One package per domain
│   ├── application/             # Application services
│   │   └── {Domain}ApplicationService.java
│   ├── domain/                  # Domain models & repository interfaces
│   │   ├── {Entity}.java
│   │   └── {Entity}Repository.java
│   ├── infrastructure/          # JPA repository implementations
│   │   └── Jpa{Entity}Repository.java
│   └── interfaces/rest/         # Controllers & mappers
│       ├── {Domain}Controller.java
│       └── {Domain}Mapper.java
└── shared/                      # Cross-cutting concerns
    ├── domain/                  # Base classes (Entity, AggregateRoot)
    ├── application/             # Shared services (CurrentUserService, RefResolver)
    └── infrastructure/          # Security, config, web setup
```

## OpenAPI Patterns

### File Structure
```
src/main/resources/openapi/
├── api.yaml                     # Main spec (imports others)
├── projects.yaml                # Project endpoints
├── epics.yaml                   # Epic endpoints
├── tasks.yaml                   # Task endpoints
└── components/
    ├── schemas.yaml             # Shared DTOs
    └── responses.yaml           # Common error responses
```

### Endpoint Definition
```yaml
/projects/{projectRef}/tasks:
  get:
    operationId: listTasks
    tags: [tasks]
    parameters:
      - name: projectRef
        in: path
        required: true
        schema:
          type: string
      - name: cursor
        in: query
        schema:
          type: string
      - name: limit
        in: query
        schema:
          type: integer
          default: 20
    responses:
      '200':
        description: Task list
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskListResponse'
```

### DTO Naming
- Request: `Create{Entity}Request`, `Update{Entity}Request`
- Response: `{Entity}` (singular), `{Entity}ListResponse` (list)
- Generated with `Dto` suffix: `CreateTaskRequestDto`, `TaskDto`

## Controller Patterns

### Standard Controller
```java
@RestController
@RequiredArgsConstructor
public class TaskController implements TasksApi {

    private final TaskApplicationService taskApplicationService;

    @Override
    public ResponseEntity<TaskDto> createTask(
            String projectRef,
            CreateTaskRequestDto request) {
        TaskDto created = taskApplicationService.createTask(projectRef, request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @Override
    public ResponseEntity<TaskDto> getTask(String projectRef, String taskRef) {
        TaskDto task = taskApplicationService.getTask(projectRef, taskRef);
        return ResponseEntity.ok(task);
    }

    @Override
    public ResponseEntity<Void> deleteTask(String projectRef, String taskRef) {
        taskApplicationService.deleteTask(projectRef, taskRef);
        return ResponseEntity.noContent().build();
    }
}
```

### Key Points
- Always `implements {Domain}Api` (generated interface)
- Use `@Override` on all methods
- Use `@RequiredArgsConstructor` for injection
- Return appropriate HTTP status codes
- No business logic in controller

## Application Service Patterns

### Standard Service
```java
@Service
@RequiredArgsConstructor
public class TaskApplicationService {

    private final TaskRepository taskRepository;
    private final RefResolver refResolver;
    private final CurrentUserService currentUserService;
    private final TransactionTemplate transactionTemplate;

    public TaskDto createTask(String projectRef, CreateTaskRequestDto request) {
        return transactionTemplate.execute(status -> {
            // 1. Resolve references
            Project project = refResolver.resolveProject(projectRef);
            User currentUser = currentUserService.getCurrentUser();

            // 2. Validate
            if (taskRepository.existsByProjectIdAndTitle(project.getId(), request.getTitle())) {
                throw new ResourceConflictException("Task with title already exists");
            }

            // 3. Create domain object
            String publicId = PublicId.generate(EntityType.TASK).getValue();
            String displayKey = project.getProjectKey() + "-" + project.nextTaskSequence();

            Task task = new Task(publicId, displayKey, project, request.getTitle());
            task.setDescription(request.getDescription());
            task.setPriority(TaskPriority.fromValue(request.getPriority().getValue()));

            // 4. Persist
            Task saved = taskRepository.save(task);

            // 5. Return DTO
            return TaskMapper.toDto(saved);
        });
    }

    public void deleteTask(String projectRef, String taskRef) {
        transactionTemplate.executeWithoutResult(status -> {
            Project project = refResolver.resolveProject(projectRef);
            Task task = refResolver.resolveTask(project, taskRef);
            taskRepository.delete(task);
        });
    }
}
```

### Transaction Patterns
```java
// Return value
return transactionTemplate.execute(status -> {
    // ... operations
    return result;
});

// No return value
transactionTemplate.executeWithoutResult(status -> {
    // ... operations
});

// Manual rollback
transactionTemplate.execute(status -> {
    try {
        // ... operations
    } catch (Exception e) {
        status.setRollbackOnly();
        throw e;
    }
    return result;
});
```

## Repository Patterns

### Interface (Domain Layer)
```java
public interface TaskRepository extends JpaRepository<Task, Long> {

    Optional<Task> findByPublicId(String publicId);

    Optional<Task> findByProjectIdAndDisplayKey(Long projectId, String displayKey);

    List<Task> findByProjectId(Long projectId);

    List<Task> findByEpicId(Long epicId);

    boolean existsByProjectIdAndTitle(Long projectId, String title);

    @Query("SELECT t FROM Task t WHERE t.project.id = :projectId AND t.status = :status")
    List<Task> findByProjectIdAndStatus(
        @Param("projectId") Long projectId,
        @Param("status") TaskStatus status);
}
```

### Naming Conventions
- `findBy{Field}` - Returns `Optional<T>` for single result
- `findBy{Field}` - Returns `List<T>` for multiple results
- `existsBy{Field}` - Returns `boolean`
- `countBy{Field}` - Returns `long`
- Use `@Query` for complex queries

## Mapper Patterns

### Utility Class Mapper
```java
@UtilityClass
public class TaskMapper {

    public TaskDto toDto(Task domain) {
        TaskDto dto = new TaskDto();
        dto.setId(domain.getPublicId());
        dto.setDisplayKey(domain.getDisplayKey());
        dto.setProjectId(domain.getProject().getPublicId());
        dto.setTitle(domain.getTitle());
        dto.setDescription(domain.getDescription());
        dto.setStatus(TaskStatusDto.fromValue(domain.getStatus().getValue()));
        dto.setPriority(TaskPriorityDto.fromValue(domain.getPriority().getValue()));
        dto.setCreatedAt(toOffsetDateTime(domain.getCreatedAt()));
        dto.setUpdatedAt(toOffsetDateTime(domain.getUpdatedAt()));

        // Nested object (only if loaded)
        if (domain.getEpic() != null) {
            dto.setEpicId(domain.getEpic().getPublicId());
        }

        return dto;
    }

    public TaskDto toDtoSimple(Task domain) {
        // Simplified version without nested objects
        TaskDto dto = new TaskDto();
        dto.setId(domain.getPublicId());
        dto.setDisplayKey(domain.getDisplayKey());
        dto.setTitle(domain.getTitle());
        dto.setStatus(TaskStatusDto.fromValue(domain.getStatus().getValue()));
        return dto;
    }

    private OffsetDateTime toOffsetDateTime(Instant instant) {
        return instant != null ? instant.atOffset(ZoneOffset.UTC) : null;
    }
}
```

### Key Points
- Use `@UtilityClass` (Lombok) for static methods
- Always use `publicId` for external IDs, never internal `id`
- Handle null values gracefully
- Convert `Instant` to `OffsetDateTime` for API responses
- Create simplified versions for list responses

## Entity Patterns

### Standard Entity
```java
@Entity
@Table(name = "tasks")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Task extends AggregateRoot<Long> {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "public_id", nullable = false, unique = true, length = 24)
    private String publicId;

    @Column(name = "display_key", nullable = false, length = 20)
    private String displayKey;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "epic_id")
    private Epic epic;

    @Setter
    @Column(nullable = false)
    private String title;

    @Setter
    @Column(columnDefinition = "TEXT")
    private String description;

    @Setter
    @Column(nullable = false)
    private TaskStatus status = TaskStatus.BACKLOG;

    @Setter
    @Column(nullable = false)
    private TaskPriority priority = TaskPriority.MEDIUM;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    // Constructor for required fields
    public Task(String publicId, String displayKey, Project project, String title) {
        this.publicId = publicId;
        this.displayKey = displayKey;
        this.project = project;
        this.title = title;
        this.createdAt = Instant.now();
        this.updatedAt = Instant.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = Instant.now();
    }

    // Domain methods
    public void assignToEpic(Epic epic) {
        this.epic = epic;
    }

    public void markCompleted() {
        this.status = TaskStatus.COMPLETED;
    }
}
```

### Key Points
- `@NoArgsConstructor(access = AccessLevel.PROTECTED)` for JPA
- Use `FetchType.LAZY` for all relationships
- `@Setter` only on mutable fields
- `@PreUpdate` for automatic timestamp updates
- Domain methods encapsulate state changes

## Test Patterns

### Controller Test
```java
class TaskControllerTest extends AbstractControllerIntegrationTest {

    @DynamicPropertySource
    static void configureSchema(DynamicPropertyRegistry registry) {
        configureSchemaForClass(registry, TaskControllerTest.class);
    }

    private Project testProject;

    @BeforeEach
    void setUp() {
        testProject = projectRepository.save(createTestProject());
    }

    @Test
    void createTask_shouldReturnCreatedTask() throws Exception {
        CreateTaskRequestDto request = new CreateTaskRequestDto();
        request.setTitle("Implement feature");
        request.setPriority(TaskPriorityDto.HIGH);

        mockMvc.perform(
            post("/api/projects/{ref}/tasks", testProject.getPublicId())
                .with(user("testuser"))
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists())
            .andExpect(jsonPath("$.displayKey").exists())
            .andExpect(jsonPath("$.title").value("Implement feature"))
            .andExpect(jsonPath("$.priority").value("HIGH"))
            .andExpect(jsonPath("$.status").value("BACKLOG"));
    }

    @Test
    void createTask_withoutAuth_shouldReturn403() throws Exception {
        CreateTaskRequestDto request = new CreateTaskRequestDto();
        request.setTitle("Test task");

        mockMvc.perform(
            post("/api/projects/{ref}/tasks", testProject.getPublicId())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isForbidden());
    }

    @Test
    void createTask_withInvalidProject_shouldReturn404() throws Exception {
        CreateTaskRequestDto request = new CreateTaskRequestDto();
        request.setTitle("Test task");

        mockMvc.perform(
            post("/api/projects/{ref}/tasks", "invalid_ref")
                .with(user("testuser"))
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.code").value("NOT_FOUND"));
    }

    @Test
    void getTask_shouldReturnTask() throws Exception {
        Task task = taskRepository.save(createTestTask(testProject));

        mockMvc.perform(
            get("/api/projects/{projectRef}/tasks/{taskRef}",
                testProject.getPublicId(), task.getPublicId())
                .with(user("testuser")))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(task.getPublicId()))
            .andExpect(jsonPath("$.title").value(task.getTitle()));
    }

    @Test
    void deleteTask_shouldReturn204() throws Exception {
        Task task = taskRepository.save(createTestTask(testProject));

        mockMvc.perform(
            delete("/api/projects/{projectRef}/tasks/{taskRef}",
                testProject.getPublicId(), task.getPublicId())
                .with(user("testuser")))
            .andExpect(status().isNoContent());

        assertThat(taskRepository.findByPublicId(task.getPublicId())).isEmpty();
    }

    // Helper methods
    private Project createTestProject() {
        return new Project(
            PublicId.generate(EntityType.PROJECT).getValue(),
            "TEST",
            "Test Project",
            testUser);
    }

    private Task createTestTask(Project project) {
        return new Task(
            PublicId.generate(EntityType.TASK).getValue(),
            project.getProjectKey() + "-1",
            project,
            "Test Task");
    }
}
```

### Test Checklist
- [ ] Happy path (success case)
- [ ] Authentication required (403 without auth)
- [ ] Resource not found (404)
- [ ] Validation errors (400)
- [ ] Conflict errors (409)
- [ ] Authorization (403 for wrong user)

## Error Handling

### Custom Exceptions
```java
// In GlobalExceptionHandler or dedicated exceptions package
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

public class ResourceConflictException extends RuntimeException {
    public ResourceConflictException(String message) {
        super(message);
    }
}

public class AccessDeniedException extends RuntimeException {
    public AccessDeniedException(String message) {
        super(message);
    }
}
```

### Global Handler
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponseDto> handleNotFound(ResourceNotFoundException ex) {
        return buildErrorResponse(ex.getMessage(), "NOT_FOUND", HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(ResourceConflictException.class)
    public ResponseEntity<ErrorResponseDto> handleConflict(ResourceConflictException ex) {
        return buildErrorResponse(ex.getMessage(), "CONFLICT", HttpStatus.CONFLICT);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponseDto> handleValidation(
            MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult().getFieldErrors().stream()
            .map(fe -> fe.getField() + ": " + fe.getDefaultMessage())
            .toList();

        ErrorResponseDto error = new ErrorResponseDto();
        error.setMessage("Validation failed");
        error.setCode("VALIDATION_ERROR");
        error.setDetails(errors);
        return ResponseEntity.badRequest().body(error);
    }

    private ResponseEntity<ErrorResponseDto> buildErrorResponse(
            String message, String code, HttpStatus status) {
        ErrorResponseDto error = new ErrorResponseDto();
        error.setMessage(message);
        error.setCode(code);
        return ResponseEntity.status(status).body(error);
    }
}
```

## Database Migration

### Creating a Migration
```sql
-- V17__add_task_estimated_hours.sql
ALTER TABLE tasks ADD COLUMN estimated_hours INTEGER;

-- Add index if needed for queries
CREATE INDEX idx_tasks_estimated_hours ON tasks(estimated_hours)
    WHERE estimated_hours IS NOT NULL;
```

### Migration Checklist
- [ ] Use next version number (check existing migrations)
- [ ] Double underscore after version: `V{n}__{description}.sql`
- [ ] Test migration locally: `./mvnw flyway:migrate`
- [ ] Ensure migration is reversible (document rollback)
- [ ] Add indexes for frequently queried columns

## Common Commands

```bash
# Build and run
./mvnw clean compile                    # Compile (generates OpenAPI code)
./mvnw spring-boot:run                  # Run application
./mvnw test                             # Run all tests
./mvnw test -Dtest=TaskControllerTest   # Run specific test

# Code quality
./mvnw spotless:check                   # Check formatting
./mvnw spotless:apply                   # Fix formatting

# Database
./mvnw flyway:migrate                   # Run migrations
./mvnw flyway:info                      # Show migration status
```
