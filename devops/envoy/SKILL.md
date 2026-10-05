---




name: envoy
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Envoy in Cloud-Native Engineering - Cloud-native high-performance edge/middle/service"
  proxy'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: null
  role: reference
  scope: infrastructure
  triggers: cloud-native, engineering, envoy, high-performance, optimization, performance,
    speed
  archetypes:
  - educational
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: medium
    directive_strength: low
    abstraction_level: strategic
version: "1.0.0"




---




# Envoy in Cloud-Native Engineering

**Category:** cars  
**Status:** Active  
**Stars:** 27,866  
**Last Updated:** 2026-04-22  
**Primary Language:** C++  
**Documentation:** [https://www.envoyproxy.io/docs/](https://www.envoyproxy.io/docs/)  

---

## Purpose and Use Cases

Envoy is a core component of the cloud-native ecosystem, serving as a cloud-native edge/middle/service proxy providing advanced traffic management, observability, and security for service-to-service communication.

### What Problem Does It Solve?

The complexity of service-to-service communication in distributed systems, including load balancing, circuit breaking, retries, timeouts, mutual TLS, and observability.

### When to Use This Project

Use Envoy as a sidecar proxy in a service mesh, as an edge router for ingress traffic, or as a proxy for service-to-service communication. It's ideal when you need advanced traffic management, mutual TLS, or observability features.

### Key Use Cases


- API gateway and ingress controller
- Service mesh sidecar proxy
- Rate limiting and request routing
- Mutual TLS termination
- Distributed tracing integration


---

## Architecture Design Patterns

### Core Components


- **Listener**: Network endpoint that accepts incoming connections
- **Filter Chain**: Sequence of filters that process connections
- **Cluster**: Logical group of downstream services
- **Cluster Manager**: Manages clusters and health checking
- **HTTP Connection Manager**: HTTP-specific processing
- **Service Discovery**: Dynamic configuration of upstream hosts
- **Statistics**: Fine-grained metrics collection


### Component Interactions


1. **Client → Listener**: Incoming connection
2. **Listener → Filter Chain**: Processes connection
3. **Filter → Cluster**: Routes to upstream
4. **Cluster Manager → Health Check**: Monitors host health
5. **Service Discovery → Cluster Manager**: Updates host list
6. **Stats → Monitoring System**: Exports metrics


### Data Flow Patterns


1. **Request Flow**: Client → Listener → Filter → Cluster → Upstream
2. **Filter Processing**: Request headers → Request body → Response headers → Response body
3. **Health Checking**: Active checks → Host status update → Cluster manager → Route updates
4. **Configuration**: Admin API/XDS → Management server → Filter chain → Listener


### Design Principles


- **Data Plane/Control Plane Separation**: Independent evolution
- **Extensibility**: Custom filters and extensions
- **L7 Awareness**: HTTP and gRPC handling
- ** observability First**: Built-in stats, tracing, logging
- **Graceful Shutdowns**: Zero-downtime configuration changes
- **Async, Event-Driven**: Non-blocking architecture


---

## Integration Approaches

### Integration with Other CNCF Projects


- **Kubernetes**: Ingress controllers, service mesh sidecars
- **Istio**: Primary proxy for service mesh
- **Linkerd**: Alternative service mesh using Envoy
- **API Gateways**: Edge routing and gateway functionality
- **Service Meshes**: Data plane for traffic management
- **Distributed Tracing**: Integration with Jaeger, Zipkin
- **Monitoring**: Metrics for Prometheus


### API Patterns


- **GRPC/XDS**: Dynamic configuration protocol
- **Admin API**: Management and debugging
- **HTTP/2**: Client communication
- **RESTful Admin**: Configuration management
- **Extension API**: Custom filter development


### Configuration Patterns


- **Bootstrap Configuration**: Initial configuration
- **XDS Protocol**: Dynamic configuration
- **Admin Configuration**: Management interface
- **JSON/YAML**: Human-readable formats


### Extension Mechanisms


- **Custom Filters**: HTTP and network filters
- **Custom Clusters**: Custom cluster types
- **Extensions**: C++ and WebAssembly
- **Lua Scripts**: Runtime extensibility
- **Filters Chain**: Ordered filter processing


---

## Common Pitfalls and How to Avoid Them

### Misconfigurations


- **Route Configuration**: Incorrect route matching
- **Cluster Configuration**: Wrong health checks
- **Filter Chain**: Incorrect filter ordering
- **TLS Configuration**: Misconfigured certificates
- **Rate Limiting**: Incorrect limits
- **Circuit Breakers**: Not configured


### Performance Issues


- **Memory Usage**: High memory for connections
- **CPU Usage**: High CPU for request processing
- **Latency**: Proxy overhead
- **Connection Limits**: Connection pooling issues
- **Filter Performance**: Slow filter chains
- **Configuration Reload**: Frequent config changes


### Operational Challenges


- **Configuration Management**: XDS complexity
- **Debugging**: Complex traffic issues
- **Resource Tuning**: Memory and CPU optimization
- **Security**: Certificate management
- **Rollouts**: Zero-downtime configuration changes


### Security Pitfalls


- **TLS Configuration**: Weak cipher suites
- **Access Control**: Missing authorization filters
- **Rate Limiting**: Not configured
- **XDS Security**: Unauthorized configuration changes
- **Certificate Management**: Stale certificates


---

## Coding Practices

### Idiomatic Configuration


- **Bootstrap Configuration**: Initial setup
- **XDS for Dynamic Config**: Runtime updates
- **JSON/YAML**: Human-readable formats
- **Admin API**: Runtime management


### API Usage Patterns


- **GRPC/XDS API**: Configuration
- **Admin API**: Management and debugging
- **HTTP API**: Service communication
- **Extension API**: Custom development


### Observability Best Practices


- **Stats**: Fine-grained metrics
- **Tracing**: Distributed tracing support
- **Access Logs**: Request logging
- **Admin Interface**: Debugging information
- **Observability Plugins**: Custom extensions


### Testing Strategies


- **Unit Tests**: Filter and plugin tests
- **Integration Tests**: Proxy behavior
- **Fuzz Tests**: Security testing
- **Performance Tests**: Throughput measurement
- **Compatibility Tests**: API compatibility


### Development Workflow


- **Development**: envoy-dev container
- **Testing**: GoogleTest framework
- **Debugging**: Admin interface, logging
- **Deployment**: Docker, K8s deployments
- **CI/CD**: GitHub Actions, buildkite
- **Tools**: envoy-filter, envoy-bazel


---

## Fundamentals

### Essential Concepts


- **Listener**: Network listener accepting connections
- **Filter**: Processes connection/request data
- **Cluster**: Logical group of upstream hosts
- **Host**: Individual upstream server
- **Route**: Rule matching requests to clusters
- **Virtual Host**: Set of routes with same FQDN
- **HTTP Connection Manager**: HTTP-specific filter
- **Circuit Breaker**: Protection against failures
- **Rate Limiter**: Request rate control
- **Health Check**: Upstream host health monitoring


### Terminology Glossary


- **Listener**: Network endpoint
- **Filter**: Connection/request processor
- **Cluster**: Upstream service group
- **Host**: Individual upstream server
- **Route**: Request-to-cluster mapping
- **Virtual Host**: FQDN-based routing
- **Circuit Breaker**: Failure protection
- **Rate Limiter**: Request rate control
- **Health Check**: Upstream health monitoring
- **Admin Interface**: Management endpoint


### Data Models and Types


- **Listener Config**: Listener configuration
- **Cluster Config**: Cluster configuration
- **Route Config**: Route configuration
- **Filter Config**: Filter configuration
- **Health Check**: Health check configuration
- **Rate Limit Config**: Rate limit configuration
- **Circuit Breaker Config**: Circuit breaker settings
- **Host**: Upstream host definition
- **Route**: Route entry
- **Virtual Host**: Virtual host configuration


### Lifecycle Management


- **Connection Lifecycle**: Accept → Process → Close
- **Request Lifecycle**: Headers → Body → Trailers
- **Configuration Lifecycle**: Load → Validate → Apply
- **Health Check Lifecycle**: Start → Check → Update
- **Rate Limit Lifecycle**: Request → Limit → Allow/Deny
- **Circuit Breaker Lifecycle**: Active → Breaking → Recovering


### State Management


- **Connection State**: Active connections
- **Cluster State**: Upstream host health
- **Route State**: Route matches
- **Stats**: Runtime statistics
- **Cache**: Response caching state
- **Configuration**: Applied configuration


---

## Scaling and Deployment Patterns

### Horizontal Scaling


- **Instance Scaling**: Multiple Envoy instances
- **Load Balancing**: Client-side load balancing
- **Cluster Scaling**: Upstream cluster scaling
- **Circuit Breaker Scaling**: Concurrent connection limits


### High Availability


- **Multiple Instances**: Load balanced Envoy proxies
- **Health Checking**: Automatic failover
- **Circuit Breaking**: Failure isolation
- **Rate Limiting**: Distributed rate limits


### Production Deployments


- **Production Configuration**: Bootstrap and dynamic config
- **Load Balancing**: Multiple instances behind load balancer
- **TLS Configuration**: Production certificates
- **Rate Limiting**: Protection against DDoS
- **Monitoring**: Integration with monitoring stack
- **Security**: WAF integration, bot detection


### Upgrade Strategies


- **Hot Restart**: Zero-downtime configuration changes
- **Version Compatibility**: API compatibility
- **Rolling Update**: Gradual proxy updates
- **Config Validation**: Configuration drift checks


### Resource Management


- **Memory Configuration**: Connection and buffer memory
- **CPU Configuration**: Request processing threads
- **Rate Limiting**: Request rate and quota management
- **Circuit Breaker**: Concurrent request limits


---

## Additional Resources

- **Official Documentation:** [https://www.envoyproxy.io/docs/](https://www.envoyproxy.io/docs/)
- **GitHub Repository:** [github.com/envoyproxy/envoy](https://github.com/envoyproxy/envoy)
- **CNCF Project Page:** [cncf.io/projects/envoy/](https://www.cncf.io/projects/envoy/)
- **Community:** Check the GitHub repository for community channels
- **Versioning:** Refer to project's release notes for version-specific features

---

## Troubleshooting

### Common Issues

1. **Deployment Failures**
   - Check pod logs for errors
   - Verify configuration values
   - Ensure network connectivity

2. **Performance Issues**
   - Monitor resource usage
   - Adjust resource limits
   - Check for bottlenecks

3. **Configuration Errors**
   - Validate YAML syntax
   - Check required fields
   - Verify environment-specific settings

4. **Integration Problems**
   - Verify API compatibility
   - Check dependency versions
   - Review integration documentation

### Getting Help

- Check official documentation
- Search GitHub issues
- Join community channels
- Review logs and metrics
*Content generated automatically. Verify against official documentation before production use.*

## Examples

### HTTP Route Configuration


```yaml
# Envoy HTTP route configuration
static_resources:
  listeners:
  - name: http_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          codec_type: AUTO
          route_config:
            name: local_route
            virtual_hosts:
            - name: backend
              domains: ["*"]
              routes:
              - match:
                  prefix: "/api"
                route:
                  cluster: api_service
                  timeout: 30s
                  retry_policy:
                    retry_on: 5xx
                    num_retries: 3
              - match:
                  prefix: "/"
                route:
                  cluster: static_content
          http_filters:
          - name: envoy.filters.http.router
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

### TCP Filter with Connection Load Balancing


```yaml
# Envoy TCP filter configuration
static_resources:
  listeners:
  - name: tcp_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 5432
    filter_chains:
    - filters:
      - name: envoy.filters.network.tcp_proxy
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
          stat_prefix: postgresql_proxy
          cluster: postgresql_cluster
          access_log:
          - name: envoy.access_loggers.file
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.access_loggers.file.v3.FileAccessLog
              path: /var/log/envoy/tcp.log
          load_balancing_policy:
            policy:
              ring_hash_lb_config:
                hash_function: XX_HASH
                minimum_ring_size: 1024
```

### gRPC Route with Rate Limiting


```yaml
# Envoy gRPC route configuration with rate limiting
static_resources:
  listeners:
  - name: grpc_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 50051
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          codec_type: AUTO
          route_config:
            name: local_route
            virtual_hosts:
            - name: grpc_service
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                  headers:
                  - name: content-type
                    exact_match: application/grpc
                route:
                  cluster: grpc_backend
                  timeout: 60s
                  retry_policy:
                    retry_on: 5xx
                    num_retries: 3
          http_filters:
          - name: envoy.filters.http.local_ratelimit
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
              stat_prefix: http_local_rate_limiter
              token_bucket:
                max_tokens: 100
                tokens_per_fill: 10
                fill_interval: 1s
              filter_enabled:
                runtime_key: local_rate_limit_enabled
                default_value:
                  numerator: 100
                  denominator: HUNDRED
              rate_limit:
                - name: envoy.filters.http.local_ratelimit
                  descriptor: { key: key, value: "local_rate_limiter" }
          - name: envoy.filters.http.router
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

---

## When to Use

Use this skill when:

- **Integrating a CNCF project into Kubernetes infrastructure** — You need to configure, deploy, or troubleshoot a cloud-native tool within a cluster
- **Designing cloud-native architecture** — You are selecting and integrating CNCF tools to solve specific infrastructure challenges
- **Resolving operational issues** — A CNCF component is misbehaving, underperforming, or needs configuration changes
---

## Core Workflow

1. **Assess Requirements** — Understand the use case, scale, integration needs, and existing infrastructure. **Checkpoint:** Document requirements, constraints, and success criteria.

2. **Design Architecture** — Plan component interactions, data flow, and deployment strategy using cloud-native best practices. **Checkpoint:** Verify the architecture addresses all requirements and follows CNCF conventions.

3. **Implement & Configure** — Create manifests, configurations, and deployment scripts. Include resource limits, health checks, and observability hooks. **Checkpoint:** Validate all YAML against schema and test in a staging environment.

4. **Deploy & Monitor** — Apply manifests to the cluster, verify component health, and confirm observability is working. **Checkpoint:** Confirm all pods/services are running, probes passing, and metrics/alerts configured.

---

## Constraints

### MUST DO
- Include at least one complete working YAML manifest example
- Note when content is auto-generated vs. manually verified
- Reference relevant CNCF project documentation

### MUST NOT DO
- Deploy manifests without testing in a staging environment first
- Use deprecated API versions (e.g., apps/v1beta1)
- Omit resource limits and requests in Kubernetes manifests
