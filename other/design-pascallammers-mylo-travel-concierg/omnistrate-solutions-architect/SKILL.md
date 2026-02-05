---
name: Omnistrate Solutions Architect
description: Guide users through designing application architectures from scratch for SaaS deployment on Omnistrate. Focuses on technology selection, domain-specific architecture patterns, compliance and SLA requirements, and iterative compose spec development. The output is a production-ready compose spec that can be handed off to the FDE skill for Omnistrate-native onboarding.
---

# Omnistrate Solutions Architect

## When to Use This Skill

**Use this skill when**:
- Designing new SaaS applications from scratch and choosing technology stacks
- Architecting microservices and selecting databases, caches, message queues
- Understanding domain-specific requirements (AI/ML, analytics, APIs, data platforms)
- Evaluating compliance needs (SOC2, HIPAA, GDPR, data residency)
- Determining customer SLA requirements and availability zones
- Making architectural decisions informed by Omnistrate's tenancy and deployment models
- Iteratively developing and refining a Docker Compose specification
- **User has a compose file with `build:` contexts** that only runs locally
- **Converting local development compose** (build contexts) to cloud-ready compose (image registries)
- **Setting up container image registries** and authentication for private images

**Do NOT use this skill when**:
- User already has a compose spec with ALL services using `image:` references (no `build:` contexts) AND images are accessible in registries → Use **FDE skill** instead
- User needs to debug failed deployments → Use **SRE skill** instead

## Relationship to Other Skills

```
SA Skill                    FDE Skill                   SRE Skill
┌─────────────────┐        ┌──────────────────┐       ┌──────────────┐
│ Design app from │   →    │ Transform compose│   →   │ Debug failed │
│ scratch         │        │ to Omnistrate    │       │ deployments  │
│                 │        │ native           │       │              │
│ • Tech choices  │        │ • x-omnistrate-* │       │ • Workflows  │
│ • Architecture  │        │   extensions     │       │ • Logs       │
│ • Compose spec  │        │ • API params     │       │ • kubectl    │
│ • Domain needs  │        │ • Service plans  │       │              │
└─────────────────┘        └──────────────────┘       └──────────────┘
     This skill            Handoff to FDE              If issues arise
```

**Output**: A vanilla Docker Compose spec optimized for Omnistrate's capabilities (tenancy, deployment models, scaling) but WITHOUT `x-omnistrate-*` extensions yet.

## Core Responsibilities

As a Solutions Architect, you will:

1. **Understand domain and requirements** - Ask questions about business model, target customers, compliance, SLAs
2. **Select appropriate technologies** - Choose databases, frameworks, languages, infrastructure components
3. **Design service architecture** - Define microservices, data flow, dependencies, state management
4. **Consider Omnistrate deployment models** - Design for SaaS, BYOC, BYOC Copilot, or On-Premise from the start
5. **Plan for tenancy** - Architecture decisions that support shared, siloed, or hybrid tenancy
6. **Build compose spec iteratively** - Start simple, validate, add complexity, refine
7. **Prepare for FDE handoff** - Ensure compose spec is ready for Omnistrate-native transformation

## Architectural Workflow

### Phase 1: Discovery & Requirements

**Ask clarifying questions** to understand the user's needs:

#### Business Context
- What problem does your SaaS solve? (domain: AI/ML, analytics, APIs, databases, etc.)
- Who are your target customers? (startups, mid-market, enterprise, developers)
- What is your pricing model? (freemium, usage-based, tiered plans)
- What customer segments need different deployment models? (SaaS, BYOC, On-Premise)

#### Technical Requirements
- What is your expected scale? (users, requests/sec, data volume)
- What are your performance requirements? (latency, throughput)
- Do you have existing infrastructure or starting from scratch?
- What programming languages/frameworks does your team know?
- Any existing codebases to integrate?

#### Compliance & Security
- What compliance certifications do you need? (SOC2, HIPAA, GDPR, ISO 27001)
- Any data residency requirements? (EU data in EU, etc.)
- What industries are you targeting? (healthcare, finance, etc.)
- Do customers need data isolation? (dedicated infrastructure, encryption)

#### SLA & Availability
- What uptime SLA do you promise? (99.9%, 99.99%)
- What is acceptable downtime? (planned maintenance windows)
- Need multi-region for disaster recovery?
- What is your RTO (Recovery Time Objective) and RPO (Recovery Point Objective)?

### Phase 2: Technology Selection

Based on requirements, recommend appropriate technology stack.

#### Application Framework Selection

**API/Web Services**:
- **Node.js/Express**: Fast I/O, JavaScript ecosystem, good for APIs
- **Python/FastAPI**: ML/AI workloads, data science, rapid development
- **Go**: High performance, concurrent workloads, system services
- **Java/Spring Boot**: Enterprise, complex business logic, banking/finance
- **.NET/ASP.NET**: Microsoft ecosystem, Windows integration, enterprise

**Considerations**:
- Team expertise (choose familiar stack for faster iteration)
- Performance requirements (Go/Rust for low latency, Python for ML)
- Ecosystem maturity (npm, PyPI, Maven availability)
- Containerization ease (Alpine base images, build times)

#### Database Selection

**Relational (ACID, structured data)**:
- **PostgreSQL**: General purpose, JSON support, extensions, most versatile
- **MySQL/MariaDB**: High read throughput, WordPress/PHP ecosystems
- **SQL Server**: Microsoft stack, enterprise features
- **CockroachDB**: Distributed SQL, global scale, Postgres-compatible

**Document/NoSQL**:
- **MongoDB**: Flexible schema, rapid iteration, JSON documents
- **DynamoDB**: Serverless, AWS-native, predictable performance
- **Cassandra**: Write-heavy, time-series, high availability

**Time-Series**:
- **TimescaleDB**: PostgreSQL extension, SQL interface
- **InfluxDB**: Purpose-built, high ingestion rates
- **Prometheus**: Metrics, monitoring data

**Graph**:
- **Neo4j**: Relationships, social networks, recommendations
- **ArangoDB**: Multi-model, graph + document

**Selection criteria**:
- Data model fit (relational vs document vs graph)
- Query patterns (complex joins vs key-value lookups)
- Consistency requirements (ACID vs eventual consistency)
- Scale expectations (GB vs TB vs PB)
- Operational complexity (managed vs self-hosted)

#### Cache/Session Store Selection

**In-Memory Cache**:
- **Redis**: Versatile, pub/sub, data structures, most common
- **Memcached**: Simple key-value, high performance, less features
- **Valkey**: Redis fork, open-source alternative

**Use cases**:
- Session storage (user login sessions)
- Database query caching (reduce DB load)
- Rate limiting (API throttling)
- Real-time leaderboards, counters

#### Message Queue/Streaming Selection

**Message Queues**:
- **RabbitMQ**: AMQP protocol, reliable, work queues
- **Apache Kafka**: High throughput, event streaming, log aggregation
- **NATS**: Lightweight, low latency, microservices
- **Amazon SQS**: Serverless, AWS-native

**Use cases**:
- Asynchronous processing (email sending, report generation)
- Event-driven architectures (microservices communication)
- Log aggregation (centralized logging)
- Real-time analytics (stream processing)

#### Storage Selection

**Object Storage**:
- **S3/GCS/Azure Blob**: Media files, backups, data lakes
- **MinIO**: Self-hosted S3-compatible

**File Storage**:
- **NFS**: Shared filesystems
- **EFS/Cloud Filestore**: Managed network filesystems

**Use cases**:
- User uploads (images, documents)
- Backups and archives
- ML model storage
- Static assets (CDN origin)

### Phase 3: Architecture Design

Design the service architecture based on domain patterns.

#### Pattern 1: Simple API Service
**Domain**: REST APIs, microservices, webhooks
```
Internet → API Server → Database
              ↓
            Cache (optional)
```

**Components**:
- API server (Node.js/Python/Go/Java)
- PostgreSQL/MySQL (relational data)
- Redis (optional: caching, rate limiting)

**Tenancy considerations**:
- Shared tenancy: One API service, logical tenant isolation in DB (tenant_id column)
- Siloed tenancy: Separate database per tenant, shared application tier

#### Pattern 2: Three-Tier Web Application
**Domain**: SaaS apps, dashboards, admin panels
```
Internet → Load Balancer → Web Tier (static) → App Tier (API) → Database
                                                     ↓
                                                  Cache
```

**Components**:
- Web tier: NGINX/Apache (static assets, reverse proxy)
- App tier: Backend API (Node.js/Python/Java)
- Database: PostgreSQL/MySQL
- Cache: Redis

**Tenancy considerations**:
- Shared: Shared app tier + database, tenant routing by subdomain
- Siloed: Separate app + DB per tenant (enterprise customers)

#### Pattern 3: Data Processing Pipeline
**Domain**: ETL, analytics, data warehousing
```
Data Sources → Ingestion API → Message Queue → Workers → Database/Data Warehouse
                                     ↓
                                 Object Storage
```

**Components**:
- Ingestion: FastAPI/Go service (data collection)
- Queue: Kafka/RabbitMQ (buffering, reliability)
- Workers: Python/Java (data transformation)
- Storage: PostgreSQL + S3 (structured + raw data)

**Tenancy considerations**:
- Shared queue with tenant partitioning
- Isolated workers per tenant for security

#### Pattern 4: AI/ML Service
**Domain**: Model serving, inference APIs, ML platforms
```
Internet → API Gateway → Inference Service (GPU) → Model Storage (S3)
                              ↓
                         Result Database
```

**Components**:
- API: FastAPI/Flask (REST endpoints)
- Inference: GPU-enabled containers (CUDA, TensorFlow, PyTorch)
- Storage: S3/GCS (model weights)
- Database: PostgreSQL (metadata, results)
- Cache: Redis (model caching, request dedup)

**Tenancy considerations**:
- GPU isolation per tenant (cost optimization)
- Shared inference tier with request queuing

#### Pattern 5: Real-Time Analytics
**Domain**: Dashboards, metrics, monitoring
```
Events → Stream Processor → Time-Series DB → Query API → Visualization
            ↓
         Object Storage (archives)
```

**Components**:
- Stream: Kafka/NATS
- Processor: Flink/custom workers
- Database: TimescaleDB/InfluxDB
- API: GraphQL/REST (query layer)

**Tenancy considerations**:
- Tenant data partitioning in time-series DB
- Shared stream with tenant tagging

### Phase 4: Deployment Model Planning

**Design for Omnistrate's deployment models from the start**.

#### SaaS Provider Account (Most Common)
**Architecture**:
- All infrastructure in provider's cloud accounts
- Shared or dedicated resources per tenant
- Provider manages everything

**Design decisions**:
- Use shared databases with tenant_id isolation (cost-effective)
- Load balancers for multi-tenant access
- Consider "Customer Networks" for enhanced security (VPC per customer)

**Best for**: Startups, mid-market, most B2B SaaS

#### BYOC (Bring Your Own Cloud)
**Architecture**:
- Deploy into customer's cloud account (AWS/GCP/Azure)
- Customer owns infrastructure, provider manages service
- Data stays in customer's environment

**Design decisions**:
- Minimize cross-account dependencies
- Use customer's IAM roles for permissions
- Plan for network connectivity (VPC peering, private links)
- Automate provisioning (Terraform/CloudFormation for customer account setup)

**Best for**: Enterprise customers, data sovereignty, regulated industries

#### BYOC Copilot (Maximum Security)
**Architecture**:
- Runs completely offline in customer environment
- Provider connects on-demand for support
- Temporary, secure connections only

**Design decisions**:
- Fully self-contained (no external dependencies)
- Local license management
- Support tooling for remote troubleshooting
- Offline documentation/runbooks

**Best for**: Government, defense, ultra-secure environments

#### On-Premise
**Architecture**:
- Customer's own data center/hardware
- Fully self-managed by customer

**Design decisions**:
- Simplify deployment (fewer moving parts)
- Clear hardware requirements
- Extensive documentation
- Update/patch mechanisms

**Best for**: Legacy enterprises, air-gapped environments

#### Multi-Model Strategy
Support multiple deployment models in same architecture:
```yaml
# Same compose spec, different plans
services:
  app:
    image: myapp:latest
    # Works for SaaS, BYOC, On-Premise
```

**Design principles**:
- Externalize configuration (12-factor app)
- No hard-coded cloud-specific logic
- Support air-gapped deployments (container registries)
- Identical functionality across models

### Phase 5: Tenancy Architecture

**Omnistrate supports multiple tenancy models** - design for flexibility.

#### Shared Tenancy
**Architecture**: Single infrastructure, logical isolation
```
Customer A ─┐
Customer B ─┤→ Shared App → Shared DB (tenant_id partitioning)
Customer C ─┘
```

**Pros**:
- Cost-effective (resource sharing)
- Simple operations (one deployment)
- Easy scaling (horizontal app scaling)

**Cons**:
- "Noisy neighbor" risks
- Limited customization per tenant
- Shared security boundary

**Best for**: Freemium, small/medium customers, standardized offerings

**Compose design**:
- Single database service
- App environment variables include tenant routing logic
- Shared cache (tenant key prefixes)

#### Siloed Tenancy
**Architecture**: Dedicated infrastructure per tenant
```
Customer A → App A → DB A
Customer B → App B → DB B
Customer C → App C → DB C
```

**Pros**:
- Complete isolation (security, performance)
- Per-tenant customization
- Easier compliance (HIPAA, PCI)

**Cons**:
- Higher cost (no sharing)
- More complex operations (many deployments)
- Scaling overhead

**Best for**: Enterprise, regulated industries, high-value customers

**Compose design**:
- Full stack per tenant instance
- Omnistrate manages multiple instances
- Each instance is isolated deployment

#### Hybrid Tenancy
**Architecture**: Shared app tier, isolated data tier
```
Customer A ─┐
Customer B ─┤→ Shared App → DB A, DB B, DB C (dedicated)
Customer C ─┘
```

**Pros**:
- Balance cost and isolation
- Shared compute, isolated data
- Flexible per-tier decisions

**Cons**:
- More complex architecture
- Connection pooling challenges

**Best for**: Mixed customer base (SMB + Enterprise)

**Compose design**:
- Shared app service (scales horizontally)
- Database connection routing to tenant-specific DB instances

### Phase 6: Compliance & Security Architecture

Design for compliance requirements from the start.

#### SOC2 (Security, Availability, Confidentiality)
**Requirements**:
- Encryption at rest and in transit
- Access logging and audit trails
- Multi-factor authentication
- Regular backups
- Incident response procedures

**Compose decisions**:
- Use TLS/SSL for all services
- Enable database encryption
- Log all API requests
- Backup volumes daily

#### HIPAA (Healthcare)
**Requirements**:
- PHI (Protected Health Information) encryption
- Access controls and audit logs
- Business Associate Agreements (BAA)
- Dedicated infrastructure (no shared tenancy for PHI)

**Compose decisions**:
- Siloed tenancy for healthcare customers
- Encrypted databases (PostgreSQL with encryption)
- No caching of PHI data
- Detailed access logging

#### GDPR (European Data Privacy)
**Requirements**:
- Data residency (EU data in EU regions)
- Right to deletion (data purging)
- Data portability
- Consent management

**Compose decisions**:
- Multi-region deployments (EU, US)
- Clear data retention policies
- Data export APIs
- Customer data deletion workflows

#### PCI DSS (Payment Card Data)
**Requirements**:
- No storage of CVV, full PAN
- Encrypted card data
- Network segmentation
- Regular security scans

**Compose decisions**:
- Use payment gateways (Stripe, no card storage)
- Isolate payment processing services
- TLS everywhere

### Phase 7: SLA & Availability Architecture

Design for target SLA from the start.

#### 99.9% Uptime (8.76 hours downtime/year)
**Architecture**:
- Single region, single zone
- Basic health checks
- Manual failover acceptable

**Compose design**:
- Single replica per service
- Database with persistent volumes
- Basic health endpoints

#### 99.95% Uptime (4.38 hours downtime/year)
**Architecture**:
- Single region, multi-zone
- Automated health checks
- Load balancing across zones

**Compose design**:
- Multiple replicas per service (2-3)
- Load balancer configuration ready
- Multi-zone volume replication (plan for it)

#### 99.99% Uptime (52.6 minutes downtime/year)
**Architecture**:
- Multi-region active-passive
- Automated failover
- Redundant databases

**Compose design**:
- Replicated services (3+ replicas)
- Database replication ready
- Health checks with quick failover

#### 99.999% Uptime (5.26 minutes downtime/year)
**Architecture**:
- Multi-region active-active
- Global load balancing
- Distributed databases

**Compose design**:
- Highly replicated services
- Distributed databases (CockroachDB, Cassandra)
- Multiple cloud providers

### Phase 8: Compose Spec Development (Iterative)

**Build the Docker Compose spec iteratively** - start simple, validate, add complexity.

#### Iteration 1: Core Services (MVP)
**Goal**: Get basic architecture working

```yaml
version: '3.8'
services:
  app:
    image: mycompany/api:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
    depends_on:
      - database

  database:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

**Validate**:
- Run `docker-compose up` locally
- Test API endpoints
- Verify database connectivity
- Check logs for errors

#### Iteration 2: Add Caching & Dependencies
**Goal**: Add performance and reliability layers

```yaml
services:
  app:
    image: mycompany/api:latest
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      - database
      - cache

  cache:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

  database:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - db_data:/var/lib/postgresql/data
```

**Validate**:
- Test cache hit/miss
- Verify performance improvement
- Check memory usage

#### Iteration 3: Add Health Checks & Readiness
**Goal**: Production-grade reliability

```yaml
services:
  app:
    image: mycompany/api:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_started

  database:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Validate**:
- Test startup order
- Verify health check responses
- Test graceful degradation

#### Iteration 4: Multi-Service (If Needed)
**Goal**: Microservices architecture

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api

  api:
    image: mycompany/api:latest
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
      - WORKER_URL=http://worker:8081
    depends_on:
      - database
      - cache

  worker:
    image: mycompany/worker:latest
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      - database
      - cache

  database:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
```

**Validate**:
- Test service-to-service communication
- Verify load balancing
- Check worker job processing

#### Iteration 5: Parameterization & Configuration
**Goal**: Prepare for Omnistrate's multi-tenancy

```yaml
services:
  app:
    image: mycompany/api:${APP_VERSION:-latest}
    environment:
      - DATABASE_URL=postgresql://${DB_USER:-postgres}:${DB_PASSWORD}@database:5432/${DB_NAME:-app}
      - REDIS_URL=redis://cache:6379
      - LOG_LEVEL=${LOG_LEVEL:-info}
      - MAX_CONNECTIONS=${MAX_CONNECTIONS:-100}
    depends_on:
      - database
      - cache

  database:
    image: postgres:${POSTGRES_VERSION:-15}
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-app}
      - POSTGRES_USER=${DB_USER:-postgres}
    volumes:
      - db_data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
    command: redis-server --maxmemory ${CACHE_SIZE:-256mb} --maxmemory-policy allkeys-lru
```

**Validate**:
- Test with different parameter values
- Verify `.env` file support
- Check parameter validation

#### Iteration 6: Container Image Registry Setup
**Goal**: Ensure all services have image references (not build contexts)

**Check for build contexts**:
```yaml
services:
  app:
    build: ./app  # ❌ Won't work on Omnistrate
    # OR
    build:
      context: ./backend
      dockerfile: Dockerfile  # ❌ Won't work on Omnistrate
```

**If build contexts exist**, you MUST work with customer to convert them:

1. **Build and push images to a registry**:
   ```bash
   # Option 1: Docker Hub
   docker build -t mycompany/api:v1.0.0 ./app
   docker push mycompany/api:v1.0.0

   # Option 2: GitHub Container Registry
   docker build -t ghcr.io/mycompany/api:v1.0.0 ./app
   docker push ghcr.io/mycompany/api:v1.0.0

   # Option 3: Private registry
   docker build -t registry.company.com/api:v1.0.0 ./app
   docker push registry.company.com/api:v1.0.0
   ```

2. **Replace build context with image reference**:
   ```yaml
   services:
     app:
       image: mycompany/api:v1.0.0  # ✅ Now cloud-deployable
       # build: ./app  # Remove this
   ```

3. **Add registry authentication** (if using private registry):

   Work with customer to create Omnistrate secrets in Dev and Prod environments, then add to compose:

   ```yaml
   # Add at top level of compose file
   x-omnistrate-image-registry-attributes:
     docker.io:
       auth:
         username: mycompany
         password: {{ $secret.DOCKERHUB_PASSWORD }}
     ghcr.io:
       auth:
         username: {{ $secret.GITHUB_USERNAME }}
         password: {{ $secret.GITHUB_TOKEN }}
     registry.company.com:
       auth:
         username: {{ $secret.PRIVATE_REGISTRY_USERNAME }}
         password: {{ $secret.PRIVATE_REGISTRY_PASSWORD }}
   ```

   **Customer must create secrets in Omnistrate**:
   - Navigate to Omnistrate console → Service → Environment Settings → Secrets
   - Create secrets: `DOCKERHUB_PASSWORD`, `GITHUB_TOKEN`, etc.
   - Secrets are environment-specific (Dev, Staging, Prod)

**Validate**: All services have `image:` field with registry reference

#### Iteration 7: Resource Sizing Hints
**Goal**: Guide Omnistrate resource allocation

```yaml
services:
  app:
    image: mycompany/api:v1.0.0  # Must have image reference
    deploy:
      replicas: ${APP_REPLICAS:-2}
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app

  database:
    image: postgres:15
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
    driver: local
    driver_opts:
      type: none
      device: /data/postgres
      o: bind
```

**Note**: These are hints for FDE transformation, not strict Omnistrate syntax yet.

### Phase 9: Container Image Registry Validation

**Critical**: Omnistrate cannot build images from source. All services must have `image:` references to pre-built container images.

**Check for build contexts**:
```bash
grep -r "build:" docker-compose.yaml
```

**If any service uses `build:` instead of `image:`**:

1. **Identify all services with build contexts**:
   ```yaml
   services:
     api:
       build: ./backend  # ❌ Not supported by Omnistrate
     worker:
       build:
         context: ./worker
         dockerfile: Dockerfile  # ❌ Not supported
   ```

2. **Ask customer where to host images**:

   **Question**: "I see these services need container images: [list services with build contexts]. Where would you like to host these images?"

   **Options to present**:
   - Docker Hub (docker.io) - public or private
   - GitHub Container Registry (ghcr.io) - public or private
   - AWS ECR (123456.dkr.ecr.region.amazonaws.com)
   - GCP Artifact Registry (region-docker.pkg.dev/project/repo)
   - Azure Container Registry (company.azurecr.io)
   - Custom private registry

3. **Guide customer to build and push images**:
   ```bash
   # Example: Docker Hub
   docker build -t mycompany/api:v1.0.0 ./backend
   docker push mycompany/api:v1.0.0

   # Example: GitHub Container Registry
   docker build -t ghcr.io/mycompany/worker:v1.0.0 ./worker
   docker push ghcr.io/mycompany/worker:v1.0.0
   ```

4. **Replace build contexts with image references in compose**:
   ```yaml
   services:
     api:
       image: mycompany/api:v1.0.0  # ✅ Now has registry reference
       # build: ./backend  # ❌ Remove build context entirely

     worker:
       image: ghcr.io/mycompany/worker:v1.0.0  # ✅ Registry reference
       # build:  # ❌ Remove build section
       #   context: ./worker
       #   dockerfile: Dockerfile
   ```

5. **Document registry information for FDE handoff**:

   Create a list for FDE skill:
   - Custom images: `mycompany/api:v1.0.0` (docker.io), `ghcr.io/mycompany/worker:v1.0.0` (ghcr.io)
   - Public images: `nginx:alpine`, `postgres:15`, `redis:7-alpine`
   - Registries used: docker.io, ghcr.io

   **Do NOT add `x-omnistrate-image-registry-attributes`** - FDE skill will:
   - Test if images are publicly accessible using docker pull
   - Guide customer through PAT/token creation for private registries
   - Collect credentials and create Omnistrate secrets
   - Add the `x-omnistrate-image-registry-attributes` section to the compose file

**Validate before moving to next phase**:
- ✅ Every service has `image:` field with valid registry reference
- ✅ NO `build:` contexts remain in compose file
- ✅ Customer has pushed all custom images to registries
- ✅ Registry information documented (image names, registry hostnames, public/private if known)

### Phase 10: Omnistrate-Aware Design Decisions

**While building the compose spec, consider Omnistrate features** (even though you won't add `x-omnistrate-*` extensions yet).

#### Design for Autoscaling
**Compose consideration**: Make app tier stateless
```yaml
services:
  app:
    # Stateless - no local file storage
    # Session in Redis, not in-memory
    image: mycompany/api:latest
    depends_on:
      - cache  # For session storage
```

#### Design for Multi-Zone HA
**Compose consideration**: Multiple replicas, load balancer ready
```yaml
services:
  app:
    deploy:
      replicas: 3  # Spread across zones later
```

#### Design for Backups
**Compose consideration**: Clear volume paths
```yaml
services:
  database:
    volumes:
      - db_data:/var/lib/postgresql/data  # FDE will add backup config here
```

#### Design for Observability
**Compose consideration**: Metrics endpoints, structured logging
```yaml
services:
  app:
    environment:
      - METRICS_PORT=9090  # Prometheus endpoint
      - LOG_FORMAT=json     # Structured logs
```

#### Design for Multi-Tenant Routing
**Compose consideration**: Tenant ID in requests
```yaml
services:
  app:
    environment:
      - TENANT_HEADER=X-Tenant-ID  # Header-based routing
```

### Phase 11: Handoff to FDE Skill

**Once the compose spec is validated and working**, prepare for FDE handoff.

#### Pre-Handoff Checklist
- [ ] Compose spec runs successfully with `docker-compose up`
- [ ] All services start in correct order (depends_on)
- [ ] Health checks pass
- [ ] Inter-service communication works
- [ ] Database migrations run successfully
- [ ] **All services have `image:` references (no `build:` contexts remain)**
- [ ] **Container images pushed to registry (customer completed this)**
- [ ] **Registry information documented** (which images, which registries, public/private)
- [ ] Environment variables parameterized
- [ ] Resource limits documented
- [ ] Volumes clearly defined
- [ ] Multi-service architecture decision finalized (single vs multi-service)
- [ ] Tenancy model documented (shared, siloed, hybrid)
- [ ] Deployment model preferences noted (SaaS, BYOC, etc.)
- [ ] SLA requirements documented
- [ ] Compliance requirements noted

#### Handoff Documentation
Provide to FDE skill:
1. **Compose spec file** (vanilla, WITHOUT `x-omnistrate-image-registry-attributes` - FDE will add if needed)
2. **Container image inventory**:
   - List all custom images with full registry URLs (e.g., `mycompany/api:v1.0.0`, `ghcr.io/myorg/worker:v1.0.0`)
   - Mark which are public vs private (if known)
   - List public images (postgres, redis, nginx, etc.) separately
3. **Registry information**: Hostnames of registries used (docker.io, ghcr.io, custom registries)
4. **Architecture diagram** (ASCII or description)
5. **Service plan requirements**:
   - Free tier: What features/limits?
   - Pro tier: What features/limits?
   - Enterprise tier: What features/limits?
6. **Deployment model preferences**:
   - SaaS only?
   - BYOC for enterprise?
7. **Compliance requirements**: SOC2, HIPAA, GDPR, etc.
8. **SLA targets**: 99.9%, 99.95%, 99.99%
9. **Scaling expectations**: Fixed replicas, manual, or autoscaling?
10. **Backup requirements**: Daily, retention period?
11. **Observability preferences**: NewRelic, Datadog, Omnistrate native?

#### Example Handoff Message
```
Ready for Omnistrate onboarding. Here's the summary:

Architecture: Three-tier web app (NGINX → API → PostgreSQL + Redis)
Tenancy: Hybrid (shared API, isolated databases for enterprise)
Deployment models: SaaS (starter/pro), BYOC (enterprise)
Compliance: SOC2, GDPR data residency
SLA: 99.95% (multi-zone)

Container Images:
Custom images (customer pushed):
- API: company/api:v1.0.0 (docker.io registry)
- Worker: company/worker:v1.0.0 (docker.io registry)

Public images (no auth needed):
- NGINX: nginx:alpine
- PostgreSQL: postgres:15
- Redis: redis:7-alpine

Registry Info:
- docker.io used for custom images (FDE will test if authentication needed)

Service plans:
- Starter: 1 API replica, 20GB DB, no backups
- Pro: 3 API replicas, 100GB DB, daily backups, autoscaling
- Enterprise: Custom sizing, BYOC option, multi-region

Compose spec attached with x-omnistrate-image-registry-attributes configured.
Ready for FDE transformation.
```

## Domain-Specific Guidance

### AI/ML Platforms
**Key decisions**:
- GPU requirements (inference: T4, training: A100)
- Model storage (S3/GCS for weights)
- Batch vs real-time inference
- Model versioning strategy

**Compose architecture**:
```yaml
services:
  api:
    image: fastapi-app
  inference:
    image: pytorch-gpu:latest
    # FDE will map to GPU instance types
  model-storage:
    # S3 bucket (external, not in compose)
```

### Data Analytics Platforms
**Key decisions**:
- Query engine (Presto, Spark, custom)
- Data lake architecture (S3 + metadata)
- Streaming vs batch processing
- Column storage (Parquet, ORC)

**Compose architecture**:
```yaml
services:
  query-api:
    image: query-engine
  workers:
    image: spark-workers
  metadata-db:
    image: postgres
```

### API Platforms
**Key decisions**:
- Gateway pattern (Kong, Envoy, custom)
- Rate limiting strategy
- API versioning
- Documentation (OpenAPI/Swagger)

**Compose architecture**:
```yaml
services:
  gateway:
    image: kong
  api-v1:
    image: api:v1
  api-v2:
    image: api:v2
```

### Database-as-a-Service
**Key decisions**:
- Which DB to offer (PostgreSQL, MySQL, MongoDB)
- Backup and restore strategy
- Replication topology (primary-replica, multi-primary)
- Connection pooling (PgBouncer)

**Compose architecture**:
```yaml
services:
  primary:
    image: postgres:15
  replica:
    image: postgres:15
  pooler:
    image: pgbouncer
```

## Iterative Refinement Workflow

```
1. Discovery → 2. Tech Selection → 3. Simple Compose → 4. Validate
                                            ↓
                                         Issues? → Refine
                                            ↓
                                           No issues
                                            ↓
5. Add Complexity → 6. Validate → 7. Image Registry Setup → 8. Omnistrate-Aware Adjustments
                        ↓
                     Issues? → Refine
                        ↓
                      No issues
                        ↓
9. Document → 10. Handoff to FDE
```

**Key principle**: Validate at each step before adding complexity.

## Success Criteria

- ✅ User's domain and requirements clearly understood
- ✅ Technology stack selected with clear rationale
- ✅ Service architecture designed (single vs multi-service)
- ✅ Tenancy model selected (shared, siloed, hybrid)
- ✅ Deployment models planned (SaaS, BYOC, etc.)
- ✅ Compliance requirements addressed in architecture
- ✅ SLA targets mapped to architecture decisions
- ✅ Docker Compose spec validated locally (`docker-compose up` works)
- ✅ All services start and communicate correctly
- ✅ Health checks defined and passing
- ✅ **All services have `image:` references (no `build:` contexts)**
- ✅ **Custom images pushed to registry (Docker Hub, GHCR, ECR, etc.)**
- ✅ **Registry information documented** (for FDE to test accessibility and configure auth if needed)
- ✅ Environment variables parameterized
- ✅ Resource sizing hints documented
- ✅ Omnistrate-aware design decisions made (autoscaling, backups, multi-zone)
- ✅ Handoff documentation prepared for FDE skill

## Reference
See SOLUTIONS_ARCHITECT_REFERENCE.md for:
- Technology comparison matrices
- Domain-specific architecture patterns
- Compliance requirement checklists
- SLA architecture guidelines
- Compose spec best practices
- Common architectural anti-patterns
