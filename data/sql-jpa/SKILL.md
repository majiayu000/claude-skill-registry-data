---
name: sql-jpa
description: Write optimized JPA queries, JPQL, Spring Data specifications, and raw SQL for Spring Boot applications. Use this skill whenever the user needs to write database queries, optimize slow queries, design JPA entities with relationships, write Criteria API or Specifications, or says things like "write a query for X", "how do I join these entities", "optimize this query", "create a JPA repository method", "write a Specification for filtering", "design the entity relationships", "fix this N+1 problem". Always use this skill for any database/JPA/SQL task in Spring Boot.
---

# SQL & JPA Queries Skill

Write correct, efficient JPA mappings, JPQL queries, and Spring Data patterns for Spring Boot applications.

## Entity Relationship Mapping

### One-to-Many (most common)

```java
// Parent (One side)
@Entity
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    // Helper methods to maintain bidirectional consistency
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);
    }
    public void removeItem(OrderItem item) {
        items.remove(item);
        item.setOrder(null);
    }
}

// Child (Many side)
@Entity
public class OrderItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)  // Always LAZY on @ManyToOne
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;
}
```

### Many-to-Many

```java
@Entity
public class Student {
    @ManyToMany
    @JoinTable(
        name = "student_course",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private Set<Course> courses = new HashSet<>();
}
```

### Fetch Strategy Rules
- `@ManyToOne` → always `FetchType.LAZY` (EAGER causes performance issues)
- `@OneToMany` → default is LAZY, keep it
- `@ManyToMany` → always LAZY
- Load eagerly only via `JOIN FETCH` in specific queries where needed

## Spring Data Repository Patterns

### Derived Query Methods
```java
// Simple conditions
Optional<User> findByEmail(String email);
List<User> findByStatus(UserStatus status);
boolean existsByEmail(String email);
long countByStatus(UserStatus status);

// Combined conditions
List<User> findByStatusAndCreatedAtAfter(UserStatus status, LocalDateTime date);
List<User> findByNameContainingIgnoreCase(String name);

// Ordering
List<Product> findByCategory_IdOrderByPriceAsc(Long categoryId);

// Pagination
Page<Product> findByStatus(ProductStatus status, Pageable pageable);
```

### JPQL Queries
```java
// Fetch join to avoid N+1
@Query("SELECT o FROM Order o LEFT JOIN FETCH o.items WHERE o.customer.id = :customerId")
List<Order> findByCustomerWithItems(@Param("customerId") Long customerId);

// Projection (DTO constructor)
@Query("SELECT new com.example.dto.OrderSummary(o.id, o.total, o.status, c.name) " +
       "FROM Order o JOIN o.customer c WHERE o.status = :status")
List<OrderSummary> findOrderSummaries(@Param("status") OrderStatus status);

// Count with condition
@Query("SELECT COUNT(o) FROM Order o WHERE o.customer.id = :customerId AND o.status = 'PENDING'")
long countPendingOrdersByCustomer(@Param("customerId") Long customerId);

// Exists check (more efficient than findBy)
@Query("SELECT CASE WHEN COUNT(u) > 0 THEN true ELSE false END FROM User u WHERE u.email = :email")
boolean existsByEmailCustom(@Param("email") String email);
```

### Native SQL (when JPQL isn't enough)
```java
@Query(value = """
    SELECT p.*, c.name as category_name
    FROM products p
    INNER JOIN categories c ON p.category_id = c.id
    WHERE p.price BETWEEN :minPrice AND :maxPrice
    ORDER BY p.price ASC
    LIMIT :limit
    """, nativeQuery = true)
List<Object[]> findProductsInPriceRange(
    @Param("minPrice") BigDecimal min,
    @Param("maxPrice") BigDecimal max,
    @Param("limit") int limit);
```

## Spring Data Specifications (Dynamic Filtering)

Best pattern for complex, dynamic queries:

```java
// Specification class
public class ProductSpecification {

    public static Specification<Product> hasCategory(Long categoryId) {
        return (root, query, cb) ->
            categoryId == null ? null : cb.equal(root.get("category").get("id"), categoryId);
    }

    public static Specification<Product> priceBetween(BigDecimal min, BigDecimal max) {
        return (root, query, cb) -> {
            if (min == null && max == null) return null;
            if (min == null) return cb.lessThanOrEqualTo(root.get("price"), max);
            if (max == null) return cb.greaterThanOrEqualTo(root.get("price"), min);
            return cb.between(root.get("price"), min, max);
        };
    }

    public static Specification<Product> nameContains(String name) {
        return (root, query, cb) ->
            name == null ? null : cb.like(cb.lower(root.get("name")), "%" + name.toLowerCase() + "%");
    }
}

// Repository — extend JpaSpecificationExecutor
public interface ProductRepository extends JpaRepository<Product, Long>,
    JpaSpecificationExecutor<Product> { }

// Usage in service
public Page<ProductResponse> search(ProductFilterRequest filter, Pageable pageable) {
    Specification<Product> spec = Specification
        .where(ProductSpecification.hasCategory(filter.getCategoryId()))
        .and(ProductSpecification.priceBetween(filter.getMinPrice(), filter.getMaxPrice()))
        .and(ProductSpecification.nameContains(filter.getName()));

    return productRepository.findAll(spec, pageable).map(mapper::toResponse);
}
```

## Solving N+1 Problems

**Detect**: Multiple identical queries in Hibernate logs (`spring.jpa.show-sql=true`)

**Fix Strategy**:
```java
// ❌ N+1: loads order items in a loop
List<Order> orders = orderRepository.findAll();
orders.forEach(o -> o.getItems().size()); // N queries

// ✅ Option 1: JOIN FETCH for small datasets
@Query("SELECT DISTINCT o FROM Order o LEFT JOIN FETCH o.items")
List<Order> findAllWithItems();

// ✅ Option 2: @EntityGraph for repository methods
@EntityGraph(attributePaths = {"items", "customer"})
List<Order> findByStatus(OrderStatus status);

// ✅ Option 3: Batch loading (for large datasets)
@BatchSize(size = 30)
@OneToMany(mappedBy = "order")
private List<OrderItem> items;
```

## Pagination with Fetch Join (Common Pitfall)

```java
// ❌ Hibernate warning: HHH90003004 - paginates in memory
@Query("SELECT o FROM Order o LEFT JOIN FETCH o.items")
Page<Order> findAllWithItems(Pageable pageable);

// ✅ Correct approach: two queries
@Query(value = "SELECT o FROM Order o LEFT JOIN FETCH o.items WHERE o.status = :status",
       countQuery = "SELECT COUNT(o) FROM Order o WHERE o.status = :status")
Page<Order> findByStatusWithItems(@Param("status") OrderStatus status, Pageable pageable);
```

## Useful Hibernate/JPA Configuration

```yaml
spring:
  jpa:
    show-sql: true              # Dev only
    properties:
      hibernate:
        format_sql: true        # Pretty print SQL
        generate_statistics: true  # Query performance stats
        default_batch_fetch_size: 30  # Global batch loading
    open-in-view: false         # Disable OSIV (anti-pattern in APIs)
```
