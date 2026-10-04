---
name: microservices
description: Microservices architecture expertise from Netflix. Build resilient, scalable distributed systems with Netflix OSS tools (Eureka, Hystrix, Zuul). Proven at 260M+ subscribers with 99.999% uptime.
expert_level: 10/10
source_company: Netflix
specialist: netflix-backend-architect
requires:
  - java-spring-expert
related:
  - chaos-engineering
  - aws-expert
  - kubernetes-expert
---

# Microservices Architecture - Netflix Expertise

**Expert**: Marcus Johnson (Netflix Principal Engineer, 15 years)
**Level**: 10/10 - Architected Netflix global streaming (260M+ subscribers)

## Overview

Microservices at Netflix scale - 100+ services, 15 billion API requests/day, 99.999% uptime. Netflix pioneered microservices and open-sourced the tools that power them.

## Netflix OSS Stack

### 1. Service Discovery - Eureka
```java
// Service registration
@SpringBootApplication
@EnableEurekaClient
public class OrderService {
    public static void main(String[] args) {
        SpringApplication.run(OrderService.class, args);
    }
}

// application.yml
eureka:
  client:
    serviceUrl:
      defaultZone: http://eureka-server:8761/eureka/
  instance:
    preferIpAddress: true
    leaseRenewalIntervalInSeconds: 10
```

### 2. Circuit Breaker - Hystrix
```java
@Service
public class UserService {

    @HystrixCommand(
        fallbackMethod = "getUserFallback",
        commandProperties = {
            @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "1000"),
            @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "10"),
            @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "50")
        }
    )
    public User getUser(String userId) {
        return restTemplate.getForObject(
            "http://user-service/users/" + userId,
            User.class
        );
    }

    public User getUserFallback(String userId, Throwable e) {
        // Return cached data or degraded response
        return cacheService.get(userId);
    }
}
```

### 3. API Gateway - Zuul
```java
@SpringBootApplication
@EnableZuulProxy
public class ApiGateway {
    public static void main(String[] args) {
        SpringApplication.run(ApiGateway.class, args);
    }
}

// Routes configuration
zuul:
  routes:
    user-service:
      path: /api/users/**
      serviceId: user-service
    order-service:
      path: /api/orders/**
      serviceId: order-service
```

## Netflix Patterns

### 1. Resilience
- Circuit breakers (Hystrix)
- Timeouts on every call
- Fallback responses
- Bulkhead isolation
- Retry with exponential backoff

### 2. Observability
- Distributed tracing (Zipkin)
- Metrics (Atlas)
- Centralized logging (ELK)
- Service mesh (future: Istio)

### 3. Deployment
- Blue-green deployments
- Canary releases
- Automated rollback
- Feature flags

## Related Skills

- **[java-spring-expert](../java-spring-expert/SKILL.md)** - Spring Boot/Cloud
- **[chaos-engineering](../chaos-engineering/SKILL.md)** - Chaos Monkey
- **[video-streaming](../video-streaming/SKILL.md)** - Netflix streaming

---

**Last Updated**: 2026-02-03
**Expert**: Marcus Johnson (Netflix, 15 years) - 99.999% uptime
