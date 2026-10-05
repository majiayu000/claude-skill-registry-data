---




name: contour
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Contour in Service Proxy - cloud native architecture, patterns, pitfalls"
  and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: calico, cilium, kuma, linkerd
  role: reference
  scope: infrastructure
  triggers: cdn, contour, infrastructure as code, k8s service, kubernetes service,
    monitoring, proxy, service
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




# Contour in Cloud-Native Engineering

**Category:** ingress  
**Status:** Active  
**Stars:** 4,800  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://projectcontour.io/](https://projectcontour.io/)  

---

## Purpose and Use Cases

Contour is a CNCF incubating project that provides a Kubernetes ingress controller using Envoy proxy for load balancing and traffic routing.

### What Problem Does It Solve?

Complex ingress management in Kubernetes. Before Contour, users had to use Kubernetes Ingress resources with limited functionality or deploy individual Envoy instances manually. Contour provides a native Kubernetes integration with advanced routing, TLS termination, and HTTP/2 support.

### When to Use This Project

Use Contour when you need:
- Advanced HTTP routing beyond basic Kubernetes Ingress
- HTTP/2 and gRPC support out of the box
- Complex routing rules with weighted traffic splitting
- TLS termination with certificate management
- Integration with external services and upstream policies

### Key Use Cases

- **Kubernetes Ingress**: Primary use case - route external traffic to services
- **Traffic Management**: Weighted traffic splitting, canary deployments
- **TLS Termination**: HTTPS termination with automatic certificate management
- **API Gateway**: Front door for microservices with advanced routing
- **Multi-tenant Ingress**: Isolated ingress for different teams/tenants

---

## Architecture Design Patterns

### Contour Components

#### 1. Contour (Control Plane)

```bash
# Contour control plane components
contour server \
  --incluster \
  --xds-address=0.0.0.0 \
  --xds-port=8001 \
  --config-path=/config/contour.yaml
```

**Responsibilities:**
- Reads Kubernetes resources (Ingress, Gateway, HTTPProxy)
- Generates Envoy configuration
- Communicates with Envoy via XDS API
- Manages certificate secrets

#### 2. Envoy (Data Plane)

```bash
# Envoy data plane
envoy -c /config/envoy.yaml --service-cluster contour
```

**Responsibilities:**
- Handles actual traffic routing
- TLS termination
- Load balancing
- Rate limiting
- Circuit breaking

### XDS API Architecture

Contour uses Envoy's XDS (x Discovery Service) protocol:

```yaml
# Contour generates XDS resources
resources:
  - "@type": type.googleapis.com/envoy.config.listener.v3.Listener
    name: ingress
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
  - "@type": type.googleapis.com/envoy.config.route.v3.RouteConfiguration
    name: ingress
    virtual_hosts:
      - name: ingress
        domains: ["*"]
        routes:
          - match:
              prefix: "/api"
            route:
              cluster: api-service
```

### Resource Hierarchy

Contour uses a resource hierarchy:

```yaml
# HTTPProxy - Contour's custom resource
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: example
  namespace: default
spec:
  virtualhost:
    fqdn: example.com
    tls:
      secretName: example-tls
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: frontend
          port: 80
    - conditions:
        - prefix: "/api"
      services:
        - name: api
          port: 8080
```

### Certificate Management

#### 1. Standard Kubernetes Secrets

```yaml
# TLS certificate from Kubernetes Secret
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: secure
spec:
  virtualhost:
    fqdn: secure.example.com
    tls:
      secretName: secure-example-com-tls  # Kubernetes Secret
```

#### 2. ACME Certificate Management

```yaml
# ACME certificate via cert-manager
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: acme
spec:
  virtualhost:
    fqdn: acme.example.com
    tls:
      secretName: acme-example-com-tls
      minimumProtocolVersion: "1.2"
      passthrough: false
```

### Gateway API Integration

Contour supports the Gateway API for modern ingress management:

```yaml
# Gateway API resource
apiVersion: gateway.networking.k8s.io/v1beta1
kind: GatewayClass
metadata:
  name: contour
spec:
  controllerName: projectcontour.io/contour-gateway-controller
  parametersRef:
    group: projectcontour.io
    kind: GatewayParameters
    name: contour-params
---
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: example
spec:
  gatewayClassName: contour
  listeners:
    - name: http
      port: 80
      protocol: HTTP
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - name: example-tls
```

### Upstream Policy

```yaml
# Upstream policy for backend services
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: policy-example
spec:
  routes:
    - services:
        - name: backend
          port: 80
      policy:
        loadBalancer:
          policy: RingHash
          requestHashPolicies:
            - header:
                headerName: "x-request-id"
        retryPolicy:
          count: 3
          perTryTimeout: 2s
        connectionPool:
          tcp:
            maxConnections: 100
          http:
            h2ProtocolSettings:
              maxConcurrentStreams: 100
```

---

## Integration Approaches

### Kubernetes Native Integration

#### 1. Ingress Resource

```yaml
# Standard Kubernetes Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example
  annotations:
    kubernetes.io/ingress.class: contour
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 8080
```

#### 2. HTTPProxy Resource

```yaml
# Contour's HTTPProxy with advanced features
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: advanced
spec:
  virtualhost:
    fqdn: advanced.example.com
    tls:
      secretName: advanced-tls
      minimumProtocolVersion: "1.2"
  routes:
    - conditions:
        - prefix: "/v1"
      services:
        - name: api-v1
          port: 8080
      timeoutPolicy:
        response: 30s
        idle: 5m
      retryPolicy:
        count: 3
        perTryTimeout: 2s
    - conditions:
        - prefix: "/v2"
      services:
        - name: api-v2
          port: 8080
      rewritePolicy:
        prefix: "/api"
```

#### 3. Gateway API Resource

```yaml
# Gateway API with Contour
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: main-gateway
spec:
  gatewayClassName: contour
  listeners:
    - name: http
      port: 80
      protocol: HTTP
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - name: main-cert
---
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: main-route
spec:
  parentRefs:
    - name: main-gateway
  hostnames:
    - example.com
  rules:
    - matches:
        - path:
            type: Prefix
            value: /
      backendRefs:
        - name: frontend
          port: 80
    - matches:
        - path:
            type: Prefix
            value: /api
      backendRefs:
        - name: api
          port: 8080
```

### External Services Integration

#### 1. External Service Reference

```yaml
# Reference external service
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: external
spec:
  routes:
    - conditions:
        - prefix: "/external"
      services:
        - name: external-service
          port: 443
          protocol: https
          urlScheme: https
      # External service load balancing
      loadBalancer:
        policy: RoundRobin
```

#### 2. Weighted Services

```yaml
# Traffic splitting between services
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: canary
spec:
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: primary
          port: 80
          weight: 90
        - name: canary
          port: 80
          weight: 10
      # Percent-based traffic splitting
      policy:
        loadBalancer:
          policy: RoundRobin
```

### Load Balancer Integration

#### 1. NLB Integration (AWS)

```yaml
# AWS NLB with Contour
apiVersion: v1
kind: Service
metadata:
  name: contour-envoy
  namespace: projectcontour
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "external"
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "instance"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      targetPort: 8080
    - name: https
      port: 443
      targetPort: 8443
  selector:
    app: contour-envoy
```

#### 2. Service Mesh Integration

```yaml
# Istio integration with Contour
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: mesh-integration
spec:
  routes:
    - conditions:
        - prefix: "/api"
      services:
        - name: api
          port: 8080
      # Service mesh integration
      policy:
        loadBalancer:
          policy: Maglev
```

### Monitoring Integration

#### 1. Prometheus Metrics

```yaml
# Enable Prometheus metrics
apiVersion: v1
kind: ConfigMap
metadata:
  name: contour
  namespace: projectcontour
data:
  contour.yaml: |
    xds-address: "0.0.0.0"
    xds-port: 8001
    debug: true
    # Contour metrics
    metrics:
      address: "0.0.0.0"
      port: 8002
```

#### 2. Tracing Integration

```yaml
# Jaeger/Zipkin tracing
apiVersion: v1
kind: ConfigMap
metadata:
  name: contour
  namespace: projectcontour
data:
  contour.yaml: |
    xds-address: "0.0.0.0"
    xds-port: 8001
    tracing:
      type: zipkin
      service-name: contour
      sampling-rate: 0.0001
      config:
        collector-host: zipkin.observability.svc.cluster.local
        collector-port: 9411
```

---

## Common Pitfalls and How to Avoid Them

### 1. TLS Configuration

**Pitfall:** Missing TLS configuration for HTTPS traffic.

```yaml
# ❌ Incorrect - no TLS configuration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: insecure
spec:
  routes:
    - services:
        - name: backend
          port: 8080

# ✅ Correct - with TLS configuration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: secure
spec:
  virtualhost:
    fqdn: secure.example.com
    tls:
      secretName: secure-tls
      minimumProtocolVersion: "1.2"
  routes:
    - services:
        - name: backend
          port: 8080
```

### 2. Route Conditions

**Pitfall:** Incorrect route condition matching.

```yaml
# ❌ Incorrect - conflicting routes
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: conflicting
spec:
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: default
          port: 80
    - conditions:
        - prefix: "/"  # Conflicts with first!
      services:
        - name: other
          port: 80

# ✅ Correct - specific routes
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: correct
spec:
  routes:
    - conditions:
        - prefix: "/api"
      services:
        - name: api
          port: 80
    - conditions:
        - prefix: "/web"
      services:
        - name: web
          port: 80
```

### 3. Service Discovery

**Pitfall:** Backend service not in same namespace.

```yaml
# ❌ Incorrect - cross-namespace service reference
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: cross-namespace
  namespace: ingress
spec:
  routes:
    - services:
        - name: backend
          namespace: production  # Must specify namespace
          port: 8080

# ✅ Correct - explicit namespace
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: same-namespace
  namespace: default
spec:
  routes:
    - services:
        - name: backend
          port: 8080  # Same namespace as HTTPProxy
```

### 4. HTTP/2 Configuration

**Pitfall:** HTTP/2 not properly configured.

```yaml
# ❌ Incorrect - HTTP/2 misconfiguration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: http2-missing
spec:
  routes:
    - services:
        - name: backend
          port: 8080
      # Missing HTTP/2 configuration

# ✅ Correct - HTTP/2 enabled
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: http2-enabled
spec:
  routes:
    - services:
        - name: backend
          port: 8080
      # HTTP/2 automatically enabled for gRPC
      policy:
        loadBalancer:
          policy: Maglev
```

### 5. Certificate Expiration

**Pitfall:** TLS certificates not rotated.

```bash
# ❌ Incorrect - manual certificate management
# Certificates expire and cause outages

# ✅ Correct - automatic rotation
# Use cert-manager with ACME
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-com
spec:
  secretName: example-com-tls
  duration: 2160h  # 90 days
  renewBefore: 360h  # 15 days before expiration
  commonName: example.com
  dnsNames:
    - example.com
    - "*.example.com"
  issuerRef:
    name: letsencrypt
    kind: ClusterIssuer
```

### 6. Timeout Configuration

**Pitfall:** Missing timeout configuration.

```yaml
# ❌ Incorrect - no timeouts
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: no-timeouts
spec:
  routes:
    - services:
        - name: slow-backend
          port: 8080

# ✅ Correct - with timeouts
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: with-timeouts
spec:
  routes:
    - services:
        - name: slow-backend
          port: 8080
      timeoutPolicy:
        response: 30s
        idle: 5m
```

---

## Coding Practices

### HTTPProxy Templates

```go
// HTTPProxy template generation
package ingress

import (
    projectcontouriov1 "github.com/projectcontour/contour/api/projectcontour/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// GenerateHTTPProxy creates a standard HTTPProxy
func GenerateHTTPProxy(name, namespace, fqdn string, routes []Route) *projectcontouriov1.HTTPProxy {
    proxy := &projectcontouriov1.HTTPProxy{
        TypeMeta: metav1.TypeMeta{
            APIVersion: "projectcontour.io/v1",
            Kind:       "HTTPProxy",
        },
        ObjectMeta: metav1.ObjectMeta{
            Name:      name,
            Namespace: namespace,
            Labels: map[string]string{
                "app": name,
            },
        },
        Spec: projectcontouriov1.HTTPProxySpec{
            VirtualHost: &projectcontouriov1.VirtualHost{
                Fqdn: fqdn,
                TLS: &projectcontouriov1.TLS{
                    SecretName: fqdnToSecretName(fqdn),
                },
            },
            Routes: convertRoutes(routes),
        },
    }
    
    return proxy
}

// Route represents an HTTP route
type Route struct {
    Path       string
    Service    string
    Port       int32
    Timeout    string
    Retries    int
    Weight     int32
}

func convertRoutes(routes []Route) []projectcontouriov1.Route {
    var result []projectcontouriov1.Route
    
    for _, r := range routes {
        route := projectcontouriov1.Route{
            Conditions: []projectcontouriov1.Condition{
                {
                    Prefix: r.Path,
                },
            },
            Services: []projectcontouriov1.Service{
                {
                    Name: r.Service,
                    Port: r.Port,
                },
            },
        }
        
        if r.Timeout != "" {
            route.TimeoutPolicy = &projectcontouriov1.TimeoutPolicy{
                Response: r.Timeout,
            }
        }
        
        if r.Retries > 0 {
            route.RetryPolicy = &projectcontouriov1.RetryPolicy{
                Count: uint32(r.Retries),
            }
        }
        
        if r.Weight > 0 {
            route.Services[0].Weight = r.Weight
        }
        
        result = append(result, route)
    }
    
    return result
}

func fqdnToSecretName(fqdn string) string {
    // Convert FQDN to secret name
    // example.com -> example-com-tls
    return fqdn + "-tls"
}
```

### Ingress Controller Integration

```go
// Contour Ingress Controller
package controller

import (
    "context"
    "fmt"
    
    projectcontouriov1 "github.com/projectcontour/contour/api/projectcontour/v1"
    networkingv1 "k8s.io/api/networking/v1"
    apierrors "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/watch"
    "k8s.io/client-go/tools/cache"
)

// IngressHandler handles Kubernetes Ingress resources
type IngressHandler struct {
    client       clientset.Interface
    proxyInformer cache.SharedIndexInformer
}

// HandleIngress converts Ingress to HTTPProxy
func (h *IngressHandler) HandleIngress(ing *networkingv1.Ingress) error {
    // Convert Ingress to HTTPProxy
    proxy := h.convertIngressToHTTPProxy(ing)
    
    // Create or update HTTPProxy
    _, err := h.client.ProjectcontourV1().HTTPProxies(ing.Namespace).Create(
        context.Background(),
        proxy,
        metav1.CreateOptions{},
    )
    
    if apierrors.IsAlreadyExists(err) {
        // Update existing HTTPProxy
        _, err = h.client.ProjectcontourV1().HTTPProxies(ing.Namespace).Update(
            context.Background(),
            proxy,
            metav1.UpdateOptions{},
        )
    }
    
    return err
}

func (h *IngressHandler) convertIngressToHTTPProxy(ing *networkingv1.Ingress) *projectcontouriov1.HTTPProxy {
    routes := make([]projectcontouriov1.Route, 0)
    
    for _, rule := range ing.Spec.Rules {
        if rule.IngressRuleValue.HTTP == nil {
            continue
        }
        
        for _, path := range rule.IngressRuleValue.HTTP.Paths {
            route := projectcontouriov1.Route{
                Conditions: []projectcontouriov1.Condition{
                    {
                        Prefix: path.Path,
                    },
                },
                Services: []projectcontouriov1.Service{
                    {
                        Name: path.Backend.Service.Name,
                        Port: path.Backend.Service.Port.Number,
                    },
                },
            }
            routes = append(routes, route)
        }
    }
    
    return &projectcontouriov1.HTTPProxy{
        TypeMeta: metav1.TypeMeta{
            APIVersion: "projectcontour.io/v1",
            Kind:       "HTTPProxy",
        },
        ObjectMeta: metav1.ObjectMeta{
            Name:      ing.Name + "-proxy",
            Namespace: ing.Namespace,
            Labels:    ing.Labels,
        },
        Spec: projectcontouriov1.HTTPProxySpec{
            Routes: routes,
        },
    }
}
```

### Testing

```go
// HTTPProxy testing
package ingress

import (
    "testing"
    
    projectcontouriov1 "github.com/projectcontour/contour/api/projectcontour/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func TestGenerateHTTPProxy(t *testing.T) {
    routes := []Route{
        {
            Path:    "/api",
            Service: "api-service",
            Port:    8080,
            Timeout: "30s",
        },
        {
            Path:    "/",
            Service: "web-service",
            Port:    80,
        },
    }
    
    proxy := GenerateHTTPProxy("test", "default", "example.com", routes)
    
    // Validate HTTPProxy
    if proxy.Name != "test" {
        t.Errorf("expected name 'test', got '%s'", proxy.Name)
    }
    
    if proxy.Namespace != "default" {
        t.Errorf("expected namespace 'default', got '%s'", proxy.Namespace)
    }
    
    if proxy.Spec.VirtualHost.Fqdn != "example.com" {
        t.Errorf("expected FQDN 'example.com', got '%s'", proxy.Spec.VirtualHost.Fqdn)
    }
    
    if proxy.Spec.VirtualHost.TLS.SecretName != "example.com-tls" {
        t.Errorf("expected TLS secret 'example.com-tls', got '%s'", proxy.Spec.VirtualHost.TLS.SecretName)
    }
    
    if len(proxy.Spec.Routes) != 2 {
        t.Errorf("expected 2 routes, got %d", len(proxy.Spec.Routes))
    }
    
    // Validate routes
    if proxy.Spec.Routes[0].Conditions[0].Prefix != "/api" {
        t.Errorf("expected prefix '/api', got '%s'", proxy.Spec.Routes[0].Conditions[0].Prefix)
    }
    
    if proxy.Spec.Routes[0].Services[0].Name != "api-service" {
        t.Errorf("expected service 'api-service', got '%s'", proxy.Spec.Routes[0].Services[0].Name)
    }
}
```

---

## Fundamentals

### Contour Architecture

#### 1. Control Plane

- **Contour**: Reads Kubernetes resources and generates Envoy config
- **XDS API**: Communicates with Envoy data plane
- **Certificate Manager**: Manages TLS certificates

#### 2. Data Plane

- **Envoy**: Handles traffic routing and load balancing
- **XDS Client**: Connects to Contour control plane
- **Listeners**: HTTP/HTTPS listeners on configured ports

### Contour Deployment

```bash
# Contour deployment
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml

# Verify deployment
kubectl -n projectcontour get pods

# Check Envoy pods
kubectl -n projectcontour get pods -l app=contour-envoy
```

### Resource Types

#### 1. HTTPProxy

```yaml
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: example
spec:
  virtualhost:
    fqdn: example.com
  routes:
    - services:
        - name: service
          port: 80
```

#### 2. TLSService

```yaml
apiVersion: projectcontour.io/v1
kind: TLSService
metadata:
  name: tls-service
spec:
  secretName: tls-secret
  minProtocolVersion: "1.2"
```

#### 3. GatewayClass

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: GatewayClass
metadata:
  name: contour
spec:
  controllerName: projectcontour.io/contour-gateway-controller
```

### Configuration Options

#### 1. Contour Config

```yaml
# contour.yaml
xds-address: "0.0.0.0"
xds-port: 8001
debug: true
metrics:
  address: "0.0.0.0"
  port: 8002
tracing:
  type: zipkin
  service-name: contour
  sampling-rate: 0.0001
```

#### 2. Envoy Config

```yaml
# Envoy bootstrap config
static_resources:
  listeners:
    - name: ingress
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 8080
  clusters:
    - name: xds_cluster
      connect_timeout: 30s
      type: STRICT_DNS
      lb_policy: ROUND_ROBIN
      load_assignment:
        cluster_name: xds_cluster
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: contour
                      port_value: 8001
```

---

## Scaling and Deployment Patterns

### High Availability

```bash
# HA Contour deployment
# Multiple Contour instances with leader election
kubectl apply -f https://projectcontour.io/quickstart/contour-ha.yaml

# Scale Envoy pods
kubectl -n projectcontour scale deployment contour-envoy --replicas=3
```

### Auto-scaling

```bash
# Horizontal Pod Autoscaler for Envoy
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: contour-envoy
  namespace: projectcontour
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: contour-envoy
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### Load Balancing Strategies

```yaml
# Load balancing in HTTPProxy
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: lb-example
spec:
  routes:
    - services:
        - name: backend
          port: 8080
      policy:
        loadBalancer:
          policy: RoundRobin  # Random, RingHash,Maglev, WeightedLeastRequest
```

### Rate Limiting

```yaml
# Rate limiting configuration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: rate-limit
spec:
  routes:
    - services:
        - name: api
          port: 8080
      policy:
        ratelimit:
          local:
            requests: 100
            period: 1s
```

### Circuit Breaking

```yaml
# Circuit breaking configuration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: circuit-breaker
spec:
  routes:
    - services:
        - name: backend
          port: 8080
      policy:
        connectionPool:
          tcp:
            maxConnections: 100
          http:
            h2ProtocolSettings:
              maxConcurrentStreams: 100
            requestTimeout: 30s
            idleTimeout: 5m
        outlierDetection:
          consecutive5xxErrors: 5
          interval: 30s
          baseEjectionTime: 30s
          maxEjectionPercent: 50
```

---

## Additional Resources

### Official Documentation

- [Project Contour](https://projectcontour.io/) - Project website
- [Contour Documentation](https://projectcontour.io/docs/) - Complete documentation
- [Contour GitHub](https://github.com/projectcontour/contour) - Source code
- [Contour API Reference](https://projectcontour.io/docs/latest/config/api/) - API documentation

### Implementations

- [Kubernetes Ingress Contour](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/#contour) - Kubernetes integration
- [Contour Operator](https://github.com/projectcontour/operator) - Operator for Contour
- [Contour Helm Chart](https://github.com/projectcontour/contour/tree/main/contour) - Helm installation

### Community Resources

- [CNCF Contour](https://www.cncf.io/projects/contour/) - CNCF project page
- [Contour Slack](https://kubernetes.slack.com/archives/C015Y3PSQSD) - Community discussion
- [Contour Mailing List](https://lists.cncf.io/g/cncf-contour) - Announcements

### Learning Resources

- [Contour Getting Started](https://projectcontour.io/docs/latest/start/) - Tutorial
- [Contour Examples](https://github.com/projectcontour/contour/tree/main/examples) - Example configurations
- [Contour Webinars](https://www.cncf.io/contour-webinars/) - Video content

---

*This SKILL.md file was verified and last updated on 2026-04-22. Content based on CNCF Contour project and production usage patterns.*

---

## Tutorial

This tutorial covers installation, configuration, and basic usage of Contour for Kubernetes ingress management.

### Prerequisites

Before starting with Contour, ensure you have:

- A running Kubernetes cluster (1.23+)
- `kubectl` configured with cluster admin access
- Basic understanding of Kubernetes services and ingress concepts
- Helm 3.x (if using Helm installation)

### Installation

#### Method 1: Using kubectl apply (Quick Start)

```bash
# Download and apply the latest Contour manifest
curl -sL https://projectcontour.io/quickstart/contour.yaml > contour.yaml

# Apply the manifest
kubectl apply -f contour.yaml

# Verify the installation
kubectl -n projectcontour get pods

# Expected output:
# NAME                      READY   STATUS    RESTARTS   AGE
# contour-7d8f9c6b9-abc12   1/1     Running   0          2m
# contour-7d8f9c6b9-def34   1/1     Running   0          2m
# contour-envoy-xyz56       1/1     Running   0          2m
```

#### Method 2: Using Helm (Production Recommended)

```bash
# Add the Contour Helm repository
helm repo add projectcontour https://projectcontour.github.io/charts
helm repo update

# Install Contour
helm install contour projectcontour/contour \
  --create-namespace \
  --namespace projectcontour \
  --set contour.config.filePath=/config/contour.yaml

# Verify installation
helm -n projectcontour list
```

#### Method 3: Custom Configuration

```bash
# Create namespace
kubectl create namespace projectcontour

# Apply Contour with custom config
kubectl apply -f contour.yaml

# Create custom ConfigMap for Contour
kubectl create configmap contour-config \
  --from-file=contour.yaml=./my-contour-config.yaml \
  -n projectcontour

# Patch deployment to use custom config
kubectl patch deployment contour \
  --namespace projectcontour \
  --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/volumes/-", "value": {"name": "config", "configMap": {"name": "contour-config"}}}]'
```

### Basic Configuration

Contour is configured via a YAML file and Kubernetes ConfigMap.

#### Contour Config File

Create `contour.yaml`:

```yaml
# contour.yaml - Contour main configuration
xds-address: "0.0.0.0"
xds-port: 8001
debug:
  address: "0.0.0.0"
  port: 8000
metrics:
  address: "0.0.0.0"
  port: 8002
tracing:
  type: zipkin
  service-name: contour
  sampling-rate: 0.0001
  config:
    collector-host: zipkin.observability.svc.cluster.local
    collector-port: 9411
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

#### Enable Gateway API Support

```yaml
# contour.yaml - Enable Gateway API
gateway:
  apiVersion: gateway.networking.k8s.io/v1beta1
  enabled: true
```

#### Configure TLS Settings

```yaml
# contour.yaml - TLS configuration
tls:
  minimumProtocolVersion: "1.2"
  cipherSuites:
    - TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
    - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

### Usage Examples

#### Creating Your First HTTPProxy

```yaml
# hello-world.yaml
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: hello-world
  namespace: default
spec:
  virtualhost:
    fqdn: hello-world.example.com
    tls:
      secretName: hello-world-tls
      minimumProtocolVersion: "1.2"
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: hello
          port: 80
```

Apply the configuration:

```bash
# Create a simple hello service first
kubectl create deployment hello --image=nginx --port=80
kubectl expose deployment hello --port=80 --target-port=80 --type=ClusterIP

# Apply HTTPProxy
kubectl apply -f hello-world.yaml

# Check status
kubectl get httpproxy hello-world -o yaml
```

#### Configure Path-Based Routing

```yaml
# multi-path.yaml
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: multi-path
  namespace: default
spec:
  virtualhost:
    fqdn: app.example.com
    tls:
      secretName: app-tls
  routes:
    - conditions:
        - prefix: "/api"
      services:
        - name: api-service
          port: 8080
      timeoutPolicy:
        response: 30s
        idle: 5m
    - conditions:
        - prefix: "/web"
      services:
        - name: web-service
          port: 80
    - conditions:
        - prefix: "/admin"
      services:
        - name: admin-service
          port: 8080
```

#### Enable gRPC Support

```yaml
# grpc-service.yaml
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: grpc-service
  namespace: default
spec:
  virtualhost:
    fqdn: grpc.example.com
    tls:
      secretName: grpc-tls
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: grpc-backend
          port: 50051
        # gRPC is automatically enabled when using HTTP/2
```

### Common Operations

#### Checking Contour Status

```bash
# Check Contour pod status
kubectl -n projectcontour get pods -l app=contour

# Check Envoy pod status
kubectl -n projectcontour get pods -l app=contour-envoy

# View Contour logs
kubectl -n projectcontour logs -l app=contour -f

# View Envoy logs
kubectl -n projectcontour logs -l app=contour-envoy -f
```

#### Debugging Configuration Issues

```bash
# Validate HTTPProxy syntax
kubectl apply -f my-proxy.yaml --dry-run=client

# Check Contour XDS status
kubectl -n projectcontour exec -l app=contour -- contour status

# Check Envoy configuration
kubectl -n projectcontour exec -l app=contour-envoy -- envoy config dump
```

#### Monitoring with Prometheus

```yaml
# Enable Prometheus scraping
apiVersion: v1
kind: ConfigMap
metadata:
  name: contour
  namespace: projectcontour
data:
  contour.yaml: |
    xds-address: "0.0.0.0"
    xds-port: 8001
    debug: true
    metrics:
      address: "0.0.0.0"
      port: 8002
---
# Prometheus scrape configuration
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: contour
  namespace: projectcontour
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: contour
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
```

#### Viewing TLS Certificate Status

```bash
# List certificates in secret
kubectl get secret -n projectcontour contour-envoy -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout

# Check certificate expiration
kubectl get secret -n projectcontour contour-envoy -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout

# View Contour TLS configuration
kubectl -n projectcontour get secret contour-envoy -o yaml
```

#### Traffic Management Examples

```yaml
# Canary deployment with weighted routing
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: canary
  namespace: default
spec:
  virtualhost:
    fqdn: myapp.example.com
    tls:
      secretName: myapp-tls
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: myapp-primary
          port: 80
          weight: 90
        - name: myapp-canary
          port: 80
          weight: 10
```

```yaml
# Retry configuration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: with-retries
  namespace: default
spec:
  routes:
    - conditions:
        - prefix: "/api"
      services:
        - name: api
          port: 8080
      retryPolicy:
        count: 3
        perTryTimeout: 2s
        retryOn:
          - 5xx
          - reset
          - connect-failure
```

### Best Practices for Contour

#### 1. Use Namespace Isolation

```yaml
# HTTPProxy in different namespaces
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: frontend
  namespace: web
spec:
  virtualhost:
    fqdn: frontend.example.com
    tls:
      secretName: frontend-tls
  routes:
    - services:
        - name: frontend
          port: 80
---
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: backend
  namespace: api
spec:
  virtualhost:
    fqdn: api.example.com
    tls:
      secretName: api-tls
  routes:
    - services:
        - name: backend
          port: 8080
```

#### 2. Implement Timeout and Retry Policies

```yaml
# Production-ready timeout and retry configuration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: production
  namespace: default
spec:
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: backend
          port: 8080
      timeoutPolicy:
        response: 30s           # Response timeout
        idle: 5m                # Idle timeout
        reconnect: 3            # Number of retries
        perTryTimeout: 5s       # Per-try timeout
      retryPolicy:
        count: 3                # Retry count
        perTryTimeout: 2s       # Per-try timeout
        retryOn:
          - 5xx                 # Retry on 5xx errors
          - reset               # Retry on connection reset
          - connect-failure     # Retry on connection failures
```

#### 3. Use Resource Limits

```yaml
# Contour deployment with resource limits
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contour
  namespace: projectcontour
spec:
  template:
    spec:
      containers:
        - name: contour
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

#### 4. Enable Access Logging

```yaml
# Enable Envoy access logging
apiVersion: v1
kind: ConfigMap
metadata:
  name: contour
  namespace: projectcontour
data:
  contour.yaml: |
    xds-address: "0.0.0.0"
    xds-port: 8001
    debug: true
    accessLog:
      - type: file
        path: /var/log/contour/envoy.log
        format: "%LOCAL_PORT% %PROTOCOL% %STATUS% %STATUS_CODE% %RESPONSE_FLAGS% %UPSTREAM_HOST% %UPSTREAM_CLUSTER% %UPSTREAM_SERVICE_TIME% %REQUEST_SIZE% %RESPONSE_SIZE% %DOWNSTREAM_REMOTE_ADDRESS% %DOWNSTREAM_LOCAL_ADDRESS% %REQUEST_METHOD% %REQUEST_PATH% %REQUEST_HEADERS% %RESPONSE_HEADERS% %UPSTREAM_STREAM_RESPONSE_FLAGS%"
```

#### 5. Certificate Management with cert-manager

```yaml
# Certificate from cert-manager
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-com
  namespace: default
spec:
  secretName: example-com-tls
  duration: 2160h  # 90 days
  renewBefore: 360h  # 15 days before expiration
  commonName: example.com
  dnsNames:
    - example.com
    - "*.example.com"
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
---
# Reference in HTTPProxy
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: secure
  namespace: default
spec:
  virtualhost:
    fqdn: example.com
    tls:
      secretName: example-com-tls
      minimumProtocolVersion: "1.2"
```

#### 6. Health Check Endpoints

```bash
# Contour health endpoint
curl http://localhost:8000/healthz

# Contour metrics endpoint
curl http://localhost:8002/metrics

# Check Contour status
kubectl -n projectcontour exec -l app=contour -- contour status
```

#### 7. Circuit Breaking Configuration

```yaml
# Circuit breaker for backend services
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: circuit-breaker
  namespace: default
spec:
  routes:
    - conditions:
        - prefix: "/api"
      services:
        - name: api
          port: 8080
      policy:
        loadBalancer:
          policy: RingHash
          requestHashPolicies:
            - header:
                headerName: "x-request-id"
        connectionPool:
          tcp:
            maxConnections: 100
          http:
            h2ProtocolSettings:
              maxConcurrentStreams: 100
            requestTimeout: 30s
            idleTimeout: 5m
        outlierDetection:
          consecutive5xxErrors: 5
          interval: 30s
          baseEjectionTime: 30s
          maxEjectionPercent: 50
```

---

*This SKILL.md file was verified and last updated on 2026-04-22. Content based on CNCF Contour project and production usage patterns.*

## Examples

### Basic HTTPProxy Configuration

```yaml
# Basic HTTPProxy for a single service
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: simple
  namespace: default
spec:
  virtualhost:
    fqdn: simple.example.com
    tls:
      secretName: simple-tls
      minimumProtocolVersion: "1.2"
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: my-service
          port: 80
```

### TLS Passthrough

```yaml
# TLS passthrough configuration
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: tls-passthrough
  namespace: default
spec:
  virtualhost:
    fqdn: secure.example.com
    tls:
      passthrough: true
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: my-service
          port: 443
```

### Weighted Traffic Splitting

```yaml
# Traffic splitting between versions
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: canary
  namespace: default
spec:
  virtualhost:
    fqdn: app.example.com
    tls:
      secretName: app-tls
  routes:
    - conditions:
        - prefix: "/"
      services:
        - name: app-v1
          port: 80
          weight: 95
        - name: app-v2
          port: 80
          weight: 5
```

### External Service

```yaml
# Route to external service
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: external
  namespace: default
spec:
  routes:
    - conditions:
        - prefix: "/external"
      services:
        - name: external-service
          port: 443
          protocol: https
          urlScheme: https
      policy:
        loadBalancer:
          policy: RoundRobin
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
