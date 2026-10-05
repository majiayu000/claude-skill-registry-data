---




name: backstage
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides Backstage in Cloud-Native Engineering - Developer Portal for
  Microservices"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: null
  role: reference
  scope: infrastructure
  triggers: backstage, cloud-native, developer, engineering
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




# Backstage in Cloud-Native Engineering

**Category:** portal  
**Status:** Active  
**Stars:** 30,000  
**Last Updated:** 2026-04-22  
**Primary Language:** TypeScript  
**Documentation:** [https://backstage.io/](https://backstage.io/)  

---

## Purpose and Use Cases

Backstage is an open-source developer portal that provides a unified experience for developers to discover, consume, and manage internal services, tools, and infrastructure.

### What Problem Does It Solve?

The fragmentation of developer tools and services across organizations, creating discovery, documentation, and management chaos. It centralizes service discovery, documentation, and tool integration.

### When to Use This Project

Use Backstage when you have multiple microservices, need centralized service discovery, want to improve developer experience, manage technical documentation, or integrate development tools into a unified portal.

### Key Use Cases


- **Service Catalog**: Central registry of all services and components
- **Documentation Portal**: Unified technical documentation
- **CI/CD Integration**: Build and deployment status display
- **Tool Integration**: Jenkins, GitHub, Kubernetes, Prometheus integrations
- **API Documentation**: OpenAPI/Swagger integration
- **Resource Management**: Kubernetes resource management
- **Security Governance**: RBAC and policy enforcement


---

## Architecture Design Patterns

### Core Components

- **Backend Server**: Node.js server providing API endpoints
- **Frontend**: React-based web application
- **Entity Registry**: Catalog of services, components, and resources
- **Scaffolder**: Template-based application generation
- **Search**: Distributed search across entities
- **Permissions**: RBAC and access control
- **Plugins**: Extensible feature modules

### Component Interactions

1. **User → Frontend**: Web interface interaction
2. **Frontend → Backend API**: API calls for data
3. **Backend → Plugins**: Plugin execution and data aggregation
4. **Plugins → External Systems**: GitHub, Kubernetes, CI/CD tools
5. **Entity Registry → Search**: Indexed entity search
6. **Permissions → Plugins**: Access control enforcement

### Data Flow Patterns

1. **Entity Ingestion**: External systems → Catalog model → Entity registry → Search index
2. **User Request**: Frontend → Backend → Plugin → External system → Response
3. **Scaffolding**: Template → User input → Generated code → Repository
4. **Search Query**: User input → Search index → Results → Frontend display

### Design Principles

- **Developer-Centric**: Focus on developer experience
- **Extensible**: Plugin architecture for customization
- **Agile**: Rapid iteration and improvement
- **Open-First**: Open-source with community governance
- **Type-Safe**: TypeScript for type safety
- **Modular**: Separation of concerns with plugins

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Resource management and cluster integration
- **Prometheus**: Metrics and monitoring integration
- **OpenTelemetry**: Tracing and observability
- **Tekton**: CI/CD pipeline integration
- **Helm**: Chart management and deployment
- **CoreDNS**: Service discovery integration

### API Patterns

- **REST API**: Backend server API endpoints
- **GraphQL**: Internal data querying
- **Webhook API**: External system notifications
- **Plugin API**: Plugin registration and execution

### Configuration Patterns

- **app-config.yaml**: Main configuration file
- **catalog-model.yaml**: Entity definitions
- **plugin-config.yaml**: Plugin-specific configuration
- **k8s.yaml**: Kubernetes integration configuration

### Extension Mechanisms

- **Plugins**: Add new features and integrations
- **API Entities**: Custom catalog entities
- **Theme Extensions**: UI customization
- **Sidebar Extensions**: Navigation customization
- **Search Extensions**: Custom search providers

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **Plugin Dependencies**: Missing or incorrect plugin configurations
- **Authentication Setup**: OAuth and SSO misconfiguration
- **Catalog Ingestion**: Incorrect entity format or access credentials
- **Search Index**: Missing or corrupted search index
- **CORS Configuration**: Frontend-backend communication issues

### Performance Issues

- **Catalog Size**: Large catalogs causing slow queries
- **Plugin Load**: Too many plugins affecting startup time
- **Search Performance**: Unoptimized search queries
- **Database Bottlenecks**: Backend database performance

### Operational Challenges

- **Version Updates**: Breaking changes between versions
- **Plugin Compatibility**: Plugin version mismatches
- **Backup and Recovery**: Catalog state management
- **Multi-Tenancy**: Organization-level isolation

### Security Pitfalls

- **Authentication**: Missing or weak authentication
- **Authorization**: Overly permissive access controls
- **Secrets Management**: Credentials in configuration files
- **API Security**: Missing rate limiting and protection

---

## Coding Practices

### Idiomatic Configuration

- **YAML Configuration**: Declarative configuration
- **Environment Variables**: Environment-specific settings
- **Git-Based Catalog**: Version control for catalog
- **Plugin Registry**: Centralized plugin management

### API Usage Patterns

- **Backend API**: Plugin API endpoints
- **Frontend API**: Component API integration
- **External API**: Integration with third-party systems
- **GraphQL API**: Internal data querying

### Observability Best Practices

- **Metrics**: Prometheus metrics collection
- **Logging**: Centralized logging integration
- **Tracing**: OpenTelemetry distributed tracing
- **Health Checks**: Application health monitoring

### Development Workflow

- **Local Development**: docker-compose for backend and frontend
- **Plugin Development**: Plugin scaffolding and testing
- **Testing**: Jest and React Testing Library
- **CI/CD**: Automated testing and deployment
- **Tools**: Node.js, Docker, Git

---

## Fundamentals

### Essential Concepts

- **Entity**: Any object in the catalog (service, component, resource)
- **Kind**: Entity type (Component, System, API, Resource)
- **Relation**: Connection between entities
- **Location**: Source of entity definition
- **Plugin**: Extensible feature module
- **API**: Backend service interface
- **Theme**: UI customization configuration

### Terminology Glossary

- **Catalog**: Central registry of entities
- **Component**: Software component or service
- **System**: Logical grouping of components
- **API**: Interface definition
- **Resource**: Infrastructure resource
- **Location**: Git repository or file containing entity definitions
- **Template**: Scaffolding template for new components

### Data Models and Types

- **Catalog Entity**: Entity definition and metadata
- **Component Spec**: Component specification
- **System Spec**: System specification
- **API Spec**: API specification
- **Resource Spec**: Resource specification
- **Location Spec**: Location definition
- **Relation Spec**: Relation between entities

### Lifecycle Management

- **Entity Lifecycle**: Create → Ingest → Catalog → Search → Display
- **Plugin Lifecycle**: Install → Configure → Register → Execute
- **Theme Lifecycle**: Load → Apply → Update → Remove

### State Management

- **Entity State**: Current catalog state
- **Search Index**: Searchable entity state
- **Session State**: User session management
- **Plugin State**: Plugin-specific state

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Backend Scaling**: Multiple backend server instances
- **Cache Layer**: Redis or Memcached for caching
- **Search Scaling**: Distributed search index
- **Database Scaling**: Read replicas and connection pooling

### High Availability

- **Backend HA**: Multiple backend instances behind load balancer
- **Database HA**: PostgreSQL or MySQL HA
- **Cache HA**: Redis cluster or sentinel
- **Service Discovery**: Kubernetes service discovery

### Production Deployments

- **Docker Deployment**: Containerized backend and frontend
- **Kubernetes Deployment**: Native Kubernetes manifests
- **Authentication**: OAuth, SSO, or basic auth
- **SSL/TLS**: HTTPS termination
- **Monitoring**: Prometheus and Grafana integration

### Upgrade Strategies

- **Configuration Migration**: Handle config file changes
- **Database Migration**: Schema updates
- **Plugin Updates**: Version compatibility checks
- **Rolling Update**: Zero-downtime deployment

### Resource Management

- **CPU/Memory Limits**: Appropriate resource requests
- **Storage**: Catalog database storage
- **Cache Size**: Appropriate cache configuration
- **Network**: API and plugin communication

---

## Additional Resources

- **Official Documentation:** [https://backstage.io/](https://backstage.io/)
- **GitHub Repository:** [github.com/backstage/backstage](https://github.com/backstage/backstage)
- **CNCF Project Page:** [cncf.io/projects/backstage/](https://www.cncf.io/projects/backstage/)
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

### Basic Configuration


```yaml
# Basic configuration example
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{project_name}}-config
  namespace: default
data:
  # Configuration goes here
  config.yaml: |
    # Base configuration
    # Add your settings here
```

### Kubernetes Deployment


```yaml
# Kubernetes deployment for {{project_name}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{project_name}}
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{project_name}}
  template:
    metadata:
      labels:
        app: {{project_name}}
    spec:
      containers:
      - name: {{project_name}}
        image: {{project_name}}:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Kubernetes Service


```yaml
# Kubernetes service for {{project_name}}
apiVersion: v1
kind: Service
metadata:
  name: {{project_name}}
  namespace: default
spec:
  selector:
    app: {{project_name}}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
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
