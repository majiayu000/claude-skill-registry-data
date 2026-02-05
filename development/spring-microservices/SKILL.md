---
name: spring-microservices
description: Build cloud-native microservices - service discovery, config server, API gateway, resilience patterns
sasmp_version: "1.3.0"
bonded_agent: 05-spring-cloud
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2024-12-30"
---

# Spring Microservices Skill

Master building cloud-native microservices with Spring Cloud including service discovery, centralized configuration, API gateway, and resilience patterns.

## Overview

This skill covers the complete Spring Cloud ecosystem for production-grade microservices architecture.

## Parameters

| Name | Type | Required | Default | Validation |
|------|------|----------|---------|------------|
| `discovery` | enum | ✗ | eureka | eureka \| consul \| kubernetes |
| `gateway` | enum | ✗ | spring-cloud-gateway | spring-cloud-gateway \| zuul |
| `resilience` | enum | ✗ | resilience4j | resilience4j \| hystrix |

## Topics Covered

### Core (Must Know)
- **Service Discovery**: Eureka Server/Client, service registration
- **API Gateway**: Spring Cloud Gateway, routing, filters
- **Configuration**: Spring Cloud Config Server/Client
- **Load Balancing**: Spring Cloud LoadBalancer

### Intermediate
- **Resilience**: Circuit breaker, retry, timeout, bulkhead
- **Distributed Tracing**: Micrometer Tracing, Zipkin
- **Inter-Service Communication**: RestClient, Feign

### Advanced
- **Event-Driven**: Spring Cloud Stream, Kafka, RabbitMQ
- **Service Mesh**: Kubernetes integration
- **Multi-Region**: Cross-region deployment patterns

## Code Examples

### Eureka Server
```java
@SpringBootApplication
@EnableEurekaServer
public class DiscoveryServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(DiscoveryServerApplication.class, args);
    }
}
```

```yaml
# application.yml
server:
  port: 8761
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
```

### Spring Cloud Gateway
```java
@Configuration
public class GatewayConfig {

    @Bean
    public RouteLocator routes(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r
                .path("/api/users/**")
                .filters(f -> f
                    .stripPrefix(1)
                    .circuitBreaker(c -> c.setName("userCB").setFallbackUri("forward:/fallback"))
                    .retry(retryConfig -> retryConfig.setRetries(3)))
                .uri("lb://USER-SERVICE"))
            .build();
    }
}
```

### Resilience4j Circuit Breaker
```java
@Service
public class OrderClient {

    @CircuitBreaker(name = "orderService", fallbackMethod = "fallback")
    @Retry(name = "orderService")
    public List<Order> getOrders(Long userId) {
        return restClient.get()
            .uri("/orders?userId={userId}", userId)
            .retrieve()
            .body(new ParameterizedTypeReference<>() {});
    }

    public List<Order> fallback(Long userId, Throwable t) {
        log.warn("Fallback for userId: {}", userId);
        return Collections.emptyList();
    }
}
```

```yaml
# resilience4j configuration
resilience4j:
  circuitbreaker:
    instances:
      orderService:
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
        sliding-window-size: 10
  retry:
    instances:
      orderService:
        max-attempts: 3
        wait-duration: 1s
```

### Distributed Tracing
```yaml
management:
  tracing:
    sampling:
      probability: 1.0
  zipkin:
    tracing:
      endpoint: http://localhost:9411/api/v2/spans

logging:
  pattern:
    level: "%5p [${spring.application.name},%X{traceId:-},%X{spanId:-}]"
```

## Troubleshooting

### Failure Modes

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Service not registered | Wrong Eureka URL | Check `eureka.client.serviceUrl` |
| Gateway 503 | No instances | Check service health |
| Circuit always open | Threshold too low | Adjust failure rate |

### Debug Checklist

```
□ Check Eureka dashboard: http://localhost:8761
□ Verify gateway routes: /actuator/gateway/routes
□ Check circuit breaker state: /actuator/circuitbreakers
□ Test config refresh: POST /actuator/refresh
```

## Unit Test Template

```java
@SpringBootTest
@WireMockTest(httpPort = 8089)
class OrderClientTest {

    @Autowired
    private OrderClient orderClient;

    @Test
    void shouldReturnOrdersWhenServiceAvailable() {
        stubFor(get(urlPathEqualTo("/orders"))
            .willReturn(aResponse()
                .withStatus(200)
                .withBody("[]")));

        List<Order> orders = orderClient.getOrders(1L);
        assertThat(orders).isEmpty();
    }

    @Test
    void shouldUseFallbackWhenServiceDown() {
        stubFor(get(urlPathEqualTo("/orders"))
            .willReturn(aResponse().withStatus(503)));

        List<Order> orders = orderClient.getOrders(1L);
        assertThat(orders).isEmpty(); // fallback
    }
}
```

## Usage

```
Skill("spring-microservices")
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12-30 | Resilience4j, Micrometer Tracing, gateway patterns |
| 1.0.0 | 2024-01-01 | Initial release |
