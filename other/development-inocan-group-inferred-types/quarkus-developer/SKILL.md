---
name: quarkus-developer
description: "[Extends backend-developer] Quarkus specialist for cloud-native Java. Use for Quarkus apps, Panache ORM, native builds with GraalVM, RESTEasy Reactive, Dev Services. Invoke alongside backend-developer for Quarkus projects."
---

# Quarkus Developer

> **Extends:** backend-developer
> **Type:** Specialized Skill

## Trigger

Use this skill alongside `backend-developer` when:
- Building Quarkus applications
- Creating REST APIs with RESTEasy Reactive
- Working with Panache (ORM/MongoDB)
- Configuring native builds (GraalVM)
- Setting up reactive messaging (Kafka, AMQP)
- Using Dev Services for testing
- Implementing CDI beans
- Optimizing for cloud-native deployment

## Context

You are a Senior Quarkus Developer with 5+ years of experience building cloud-native Java applications. You have deep expertise in reactive programming, native compilation, and Kubernetes deployments. You understand Quarkus's build-time optimization philosophy and use it to create fast, memory-efficient applications.

## Expertise

### Versions

| Technology | Version | Notes |
|------------|---------|-------|
| Quarkus | 3.30+ | Latest stable |
| Quarkus LTS | 3.20 | Long-term support |
| Java | 21+ | Virtual threads supported |
| GraalVM | 23+ | Native compilation |
| Hibernate ORM | 7.x | With Panache |

### Core Concepts

#### Project Setup

```bash
# Create new project
quarkus create app com.example:my-app \
  --extension='resteasy-reactive-jackson,hibernate-orm-panache,jdbc-postgresql'

# Or with Maven
mvn io.quarkus.platform:quarkus-maven-plugin:3.30.0:create \
  -DprojectGroupId=com.example \
  -DprojectArtifactId=my-app \
  -Dextensions="resteasy-reactive-jackson,hibernate-orm-panache"
```

#### RESTEasy Reactive Endpoints

```java
@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserResource {

    @Inject
    UserService userService;

    @GET
    public List<User> list() {
        return userService.findAll();
    }

    @GET
    @Path("/{id}")
    public User get(@PathParam("id") Long id) {
        return userService.findById(id)
            .orElseThrow(() -> new NotFoundException("User not found"));
    }

    @POST
    @Transactional
    public Response create(@Valid CreateUserRequest request) {
        User user = userService.create(request);
        return Response.created(URI.create("/users/" + user.id)).entity(user).build();
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public User update(@PathParam("id") Long id, @Valid UpdateUserRequest request) {
        return userService.update(id, request);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        userService.delete(id);
    }
}
```

#### Panache ORM (Active Record Pattern)

```java
@Entity
public class User extends PanacheEntity {
    public String name;
    public String email;
    public LocalDateTime createdAt;

    // Custom queries
    public static User findByEmail(String email) {
        return find("email", email).firstResult();
    }

    public static List<User> findActive() {
        return list("active", true);
    }

    public static long countByName(String name) {
        return count("name like ?1", "%" + name + "%");
    }
}

// Usage
User user = new User();
user.name = "John";
user.email = "john@example.com";
user.persist();

User found = User.findById(1L);
List<User> users = User.listAll();
User.deleteById(1L);
```

#### Panache Repository Pattern

```java
@ApplicationScoped
public class UserRepository implements PanacheRepository<User> {

    public User findByEmail(String email) {
        return find("email", email).firstResult();
    }

    public List<User> findActive() {
        return list("active", true);
    }
}

// Usage in service
@ApplicationScoped
public class UserService {
    @Inject
    UserRepository userRepository;

    public List<User> findAll() {
        return userRepository.listAll();
    }
}
```

#### Reactive with Mutiny

```java
@Path("/users")
public class ReactiveUserResource {

    @Inject
    UserRepository userRepository;

    @GET
    public Uni<List<User>> list() {
        return userRepository.listAll();
    }

    @GET
    @Path("/{id}")
    public Uni<User> get(@PathParam("id") Long id) {
        return userRepository.findById(id)
            .onItem().ifNull().failWith(() -> new NotFoundException());
    }

    @POST
    @Transactional
    public Uni<Response> create(@Valid CreateUserRequest request) {
        return userRepository.persist(User.from(request))
            .map(user -> Response.created(URI.create("/users/" + user.id)).build());
    }
}
```

#### WebSocket Next (3.20+)

```java
@WebSocket(path = "/chat/{room}")
public class ChatWebSocket {

    @Inject
    ChatService chatService;

    @OnOpen
    public void onOpen(WebSocketConnection connection, @PathParam("room") String room) {
        chatService.join(room, connection);
    }

    @OnTextMessage
    public void onMessage(WebSocketConnection connection, String message) {
        chatService.broadcast(connection, message);
    }

    @OnClose
    public void onClose(WebSocketConnection connection) {
        chatService.leave(connection);
    }
}
```

#### Configuration

```properties
# application.properties

# Database
quarkus.datasource.db-kind=postgresql
quarkus.datasource.username=${DB_USER:postgres}
quarkus.datasource.password=${DB_PASSWORD:postgres}
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/mydb

# Hibernate
quarkus.hibernate-orm.database.generation=update
quarkus.hibernate-orm.log.sql=true

# HTTP
quarkus.http.port=8080
quarkus.http.cors=true

# Native build
quarkus.native.container-build=true
quarkus.native.builder-image=quay.io/quarkus/ubi-quarkus-mandrel-builder-image:jdk-21
```

#### Dev Services

```properties
# Automatically starts containers for testing
%dev.quarkus.datasource.devservices.enabled=true
%test.quarkus.datasource.devservices.enabled=true

# Kafka Dev Service
quarkus.kafka.devservices.enabled=true

# Redis Dev Service
quarkus.redis.devservices.enabled=true
```

### Native Compilation

```bash
# Build native executable
./mvnw package -Pnative

# Build native in container (no GraalVM needed locally)
./mvnw package -Pnative -Dquarkus.native.container-build=true

# Build native container image
./mvnw package -Pnative -Dquarkus.container-image.build=true
```

#### Native Build Configuration

```java
@RegisterForReflection
public class MyDTO {
    public String name;
    public int value;
}

// For resources
@RegisterForReflection(targets = {Resource.class})
```

### Testing

```java
@QuarkusTest
class UserResourceTest {

    @Test
    void testListUsers() {
        given()
            .when().get("/users")
            .then()
            .statusCode(200)
            .body("$.size()", greaterThan(0));
    }

    @Test
    void testCreateUser() {
        given()
            .contentType(ContentType.JSON)
            .body(new CreateUserRequest("John", "john@example.com"))
            .when().post("/users")
            .then()
            .statusCode(201)
            .header("Location", containsString("/users/"));
    }
}

@QuarkusTest
@TestProfile(TestProfile.class)
class UserServiceTest {

    @Inject
    UserService userService;

    @Test
    @Transactional
    void testCreateUser() {
        User user = userService.create(new CreateUserRequest("Test", "test@example.com"));
        assertNotNull(user.id);
    }
}
```

#### Native Testing

```java
@QuarkusIntegrationTest
class UserResourceIT {

    @Test
    void testNativeEndpoint() {
        given()
            .when().get("/users")
            .then()
            .statusCode(200);
    }
}
```

### Messaging with Kafka

```java
@ApplicationScoped
public class OrderEventProducer {

    @Inject
    @Channel("orders-out")
    Emitter<OrderEvent> emitter;

    public void sendOrderEvent(OrderEvent event) {
        emitter.send(event);
    }
}

@ApplicationScoped
public class OrderEventConsumer {

    @Incoming("orders-in")
    public void consume(OrderEvent event) {
        // Process event
    }

    @Incoming("orders-in")
    @Outgoing("processed-orders")
    public ProcessedOrder processAndForward(OrderEvent event) {
        return new ProcessedOrder(event);
    }
}
```

```properties
# application.properties
mp.messaging.outgoing.orders-out.connector=smallrye-kafka
mp.messaging.outgoing.orders-out.topic=orders
mp.messaging.outgoing.orders-out.value.serializer=io.quarkus.kafka.client.serialization.JsonbSerializer

mp.messaging.incoming.orders-in.connector=smallrye-kafka
mp.messaging.incoming.orders-in.topic=orders
mp.messaging.incoming.orders-in.value.deserializer=com.example.OrderEventDeserializer
```

### Project Structure

```
src/
├── main/
│   ├── java/com/example/
│   │   ├── domain/           # Entities
│   │   ├── repository/       # Panache repositories
│   │   ├── service/          # Business logic
│   │   ├── resource/         # REST endpoints
│   │   ├── dto/              # DTOs
│   │   └── config/           # Configuration
│   ├── resources/
│   │   ├── application.properties
│   │   └── META-INF/resources/  # Static files
│   └── docker/
│       ├── Dockerfile.jvm
│       └── Dockerfile.native
└── test/
    └── java/com/example/
```

## Parent & Related Skills

| Skill | Relationship |
|-------|--------------|
| **backend-developer** | Parent skill - invoke for general backend patterns |
| **spring-kafka-integration** | For SmallRye Kafka messaging, reactive streams |
| **devops-engineer** | For native builds, GraalVM, Kubernetes deployment |
| **database-architect** | For Panache entities, PostgreSQL optimization |

## Standards

- **Dev mode**: Use `quarkus dev` for hot reload
- **Dev Services**: Use for local development
- **Panache**: Prefer repository pattern for complex apps
- **Native builds**: Test native builds in CI
- **Virtual threads**: Use with Java 21+
- **Configuration profiles**: Use %dev, %test, %prod

## Checklist

### Before Implementing
- [ ] Extensions selected (quarkus ext list)
- [ ] Database configured
- [ ] Dev Services enabled for testing

### Before Deploying
- [ ] Native build tested
- [ ] Health checks configured
- [ ] Metrics enabled
- [ ] Container image built

## Anti-Patterns to Avoid

1. **Blocking in reactive**: Don't block Uni/Multi
2. **Missing @RegisterForReflection**: Native builds fail
3. **No Dev Services**: Manual container setup
4. **Large native images**: Minimize dependencies
5. **No health checks**: Container orchestration needs them
