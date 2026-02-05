---
name: devops-engineering
description: >-
  Domain specialist for infrastructure, CI/CD, containers, observability, and DevOps operations.
  Scope: CI/CD pipelines, containerization, infrastructure as code, monitoring and observability, container security, release strategies, infrastructure reliability patterns.
  Excludes: code-level security, application architecture, database design, API design, performance profiling.
  Triggers: "CI/CD", "Docker", "Kubernetes", "K8s", "deployment", "pipeline", "monitoring", "observability", "Terraform", "Ansible", "infrastructure".
---

# DEVOPS_ENGINEERING

## DOMAIN EXPERTISE
- **Common Attacks**: Container escapes, supply chain attacks, credential exposure, privilege escalation, insecure configurations, poisoned images
- **Common Issues**: Poor monitoring, lack of alerts, inconsistent environments, manual deployments, no rollback capability, resource exhaustion
- **Common Mistakes**: Running containers as root, hard-coded secrets, no resource limits, missing health checks, manual production changes, fragile pipelines, untested rollbacks
- **Related Patterns**: Infrastructure as Code, Immutable Infrastructure, Blue-Green Deployment, Canary Deployment, Cattle vs Pets, 12-Factor App
- **Problematic Patterns**: SSH into production, manual configuration management, snowflake servers, monolithic deployments, lack of idempotency
- **Container Security**: Container escapes, image scanning, least privilege, secure base images, secrets management, network policies
- **Observability**: Metrics (counters, gauges, histograms), logging (structured logs), tracing (distributed tracing), alerting (SLO/SLI based)
- **Infrastructure Reliability**: SLO (Service Level Objectives), SLI (Service Level Indicators), error budgets, blameless post-mortems, gradual rollouts

## MODE DETECTION
- **WRITE Mode**: Keywords: ["create", "generate", "write", "build", "implement", "add", "new", "deploy", "setup", "configure"]
- **REVIEW Mode**: Keywords: ["review", "analyze", "audit", "check", "find issues", "security audit", "infrastructure review", "deployment issues", "monitoring problems"]

## LOADING STRATEGY
### Write Mode (Progressive)
Load patterns based on infrastructure requirements:
- CI/CD questions -> Load `@infrastructure/CI-CD.md`
- Container questions -> Load `@infrastructure/CONTAINERIZATION.md`
- Infrastructure as code -> Load `@infrastructure/IAC.md`
- Monitoring/observability -> Load `@infrastructure/OBSERVABILITY.md`
- Container security -> Load `@security/CONTAINER-SECURITY.md`
- Deployment questions -> Load `@release/RELEASE-STRATEGIES.md`

### Review Mode (Exhaustive)
Load comprehensive checklists:
- IF infrastructure review requested -> Load all infrastructure patterns
- IF security review requested -> Load `@security/CONTAINER-SECURITY.md` + security patterns
- IF deployment issues -> Load `@release/RELEASE-STRATEGIES.md` + infrastructure patterns

### Progressive Loading (Write Mode)
- **IF** request mentions "CI", "CD", "pipeline", "build", "deploy" -> READ FILE: `@infrastructure/CI-CD.md`
- **IF** request mentions "Docker", "container", "image" -> READ FILE: `@infrastructure/CONTAINERIZATION.md`
- **IF** request mentions "Terraform", "Ansible", "IaC", "infrastructure code" -> READ FILE: `@infrastructure/IAC.md`
- **IF** request mentions "monitoring", "logging", "metrics", "tracing", "alerting", "observability" -> READ FILE: `@infrastructure/OBSERVABILITY.md`
- **IF** request mentions "container security", "image scanning", "container escapes" -> READ FILE: `@security/CONTAINER-SECURITY.md`
- **IF** request mentions "deployment", "release", "blue-green", "canary" -> READ FILE: `@release/RELEASE-STRATEGIES.md`

### Comprehensive Loading (Review Mode)
- **IF** request mentions "review", "audit", "security" -> READ FILES: `@security/CONTAINER-SECURITY.md`, `@infrastructure/CONTAINERIZATION.md`, `@infrastructure/CI-CD.md`
- **IF** request mentions "infrastructure issues" -> READ FILES: `@infrastructure/CI-CD.md`, `@infrastructure/CONTAINERIZATION.md`, `@infrastructure/IAC.md`, `@infrastructure/OBSERVABILITY.md`
- **IF** request mentions "deployment issues" -> READ FILES: `@release/RELEASE-STRATEGIES.md`, `@infrastructure/CI-CD.md`

## CONTEXT DETECTION
### Platform Detection
#### Container Platforms
- **Docker**: Dockerfile, docker-compose.yml, docker-compose.yaml, .dockerignore
- **Docker Compose**: docker-compose.yml, docker-compose.yaml, compose.yml, compose.yaml, docker-compose.override.yml
- **Kubernetes (K8s)**: deployment.yaml, service.yaml, ingress.yaml, configmap.yaml, secret.yaml, statefulset.yaml, daemonset.yaml, namespace.yaml, persistentvolume.yaml, persistentvolumeclaim.yaml, storageclass.yaml, .k8s/ directory
- **Kustomize**: kustomization.yaml, kustomization.yml, overlays/ directory
- **Helm**: Chart.yaml, values.yaml, templates/ directory, .helmignore, requirements.yaml, helmfile.yaml
- **Docker Swarm**: docker-stack.yml, docker-stack.yaml, docker-compose.yml with deploy keys

#### Cloud Platforms
- **AWS CloudFormation**: template.yaml, template.json, AWS::CloudFormation::Stack
- **AWS SAM**: template.yaml with AWSTemplateFormatVersion: '2010-09-09' and Transform: AWS::Serverless-2016-10-31, sam.yaml
- **AWS CDK**: lib/ with stack definitions, cdk.json, package.json with aws-cdk
- **Terraform**: *.tf, main.tf, variables.tf, outputs.tf, terraform.tfvars, .terraform.lock.hcl, .terraform/ directory, modules/ directory
- **Terraform Cloud/Enterprise**: terraform-cloud.tf, workspace files
- **Pulumi**: Pulumi.yaml, Pulumi.<stack>.yaml, index.ts, __main__.py, main.go
- **Google Cloud Deployment Manager**: *.yaml, *.jinja, config.yaml
- **Azure Resource Manager (ARM)**: template.json, azuredeploy.json, azuredeploy.parameters.json
- **Azure Bicep**: main.bicep, .bicep files, azure.bicepparam

#### Configuration Management
- **Ansible**: *.yml, *.yaml, playbooks/, roles/, inventory/, ansible.cfg, ansible.cfg, group_vars/, host_vars/
- **Chef**: recipes/, attributes/, resources/, Cheffile, Berksfile, Policyfile.rb
- **Puppet**: manifests/*.pp, modules/, templates/, hiera.yaml
- **SaltStack**: *.sls, pillar/, reactor/, salt/
- **CFEngine**: promises.cf, inputs/

#### CI/CD Platforms
- **GitHub Actions**: .github/workflows/*.yml, .github/workflows/*.yaml, .github/actions/
- **GitLab CI**: .gitlab-ci.yml, .gitlab-ci.yaml
- **Jenkins**: Jenkinsfile, Jenkinsfile.* (declarative)
- **CircleCI**: .circleci/config.yml, .circleci/config.yaml
- **Travis CI**: .travis.yml, .travis.yaml
- **Bitbucket Pipelines**: bitbucket-pipelines.yml
- **Azure Pipelines**: azure-pipelines.yml, azure-pipelines.yaml
- **Azure DevOps**: azure-pipelines-*.yml, build.yml, release.yml
- **GitLab Runner**: config.toml
- **TeamCity**: teamcity-settings.kts, .teamcity/

#### Build Systems & Tools
- **Make**: Makefile, makefile, GNUmakefile
- **CMake**: CMakeLists.txt, cmake/ directory
- **Gradle**: build.gradle, build.gradle.kts, settings.gradle, settings.gradle.kts, gradle.properties, .gradle/ directory
- **Maven**: pom.xml, mvnw, mvnw.cmd
- **Bazel**: BUILD, WORKSPACE, BUILD.bazel, MODULE.bazel
- **Buck**: BUCK, TARGETS
- **Nix**: default.nix, shell.nix, flake.nix
- **Nixpkgs**: pkgs/ directory, .nix/
- **Webpack**: webpack.config.js, webpack.config.ts, webpackfile.js
- **Vite**: vite.config.js, vite.config.ts
- **Rollup**: rollup.config.js, rollup.config.ts
- **esbuild**: esbuild.config.js, esbuild.config.mjs
- **Parcel**: parcelrc, .parcelrc
- **Turbopack**: turbo.json

#### Monitoring & Observability
- **Prometheus**: prometheus.yml, prometheus.yaml, alerts.yml, rules/*.yml
- **Grafana**: grafana.ini, provisioning/, dashboards/, datasources/
- **Elastic Stack (ELK)**: elasticsearch.yml, logstash.conf, kibana.yml, filebeat.yml
- **Jaeger**: jaeger-config.json
- **Zipkin**: zipkin-config.json
- **OpenTelemetry**: otel-collector-config.yaml
- **Thanos**: thanos.yaml, query.yaml, store.yaml
- **VictoriaMetrics**: victoriametrics.yaml
- **Datadog**: datadog.yaml, datadog.json
- **New Relic**: newrelic.yml

#### Logging & Tracing
- **Fluentd**: fluent.conf, fluentd.conf
- **Fluent Bit**: fluent-bit.conf, parsers.conf
- **Logstash**: logstash.conf, pipelines.yml
- **Loki**: loki-config.yaml
- **Syslog-ng**: syslog-ng.conf
- **Rsyslog**: rsyslog.conf

### Application Type Detection
#### Web Servers
- **Nginx**: nginx.conf, conf.d/, sites-enabled/, sites-available/, .nginx file extension
- **Apache HTTPD**: httpd.conf, apache2.conf, conf-available/, conf-enabled/
- **Caddyfile**: Caddyfile
- **Traefik**: traefik.yml, traefik.yaml, traefik.toml, traefik动态配置
- **Envoy**: envoy.yaml, envoy.json

#### Reverse Proxies & Load Balancers
- **HAProxy**: haproxy.cfg
- **Traefik**: (see Web Servers section)
- **Envoy**: (see Web Servers section)

#### Message Queues & Brokers
- **RabbitMQ**: rabbitmq.conf, rabbitmq.config, advanced.config
- **Apache Kafka**: server.properties, consumer.properties, producer.properties
- **Apache ActiveMQ**: activemq.xml
- **Redis**: redis.conf, sentinel.conf
- **NATS**: nats-server.conf
- **Apache Pulsar**: broker.conf, client.conf

#### Runtime & Application Detection
- **Node.js**: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml, tsconfig.json, .nvmrc, .node-version
- **Python**: requirements.txt, requirements-dev.txt, pyproject.toml, setup.py, setup.cfg, Pipfile, Pipfile.lock, poetry.lock, tox.ini
- **PHP**: composer.json, composer.lock, phpunit.xml, .php-cs-fixer.php
- **Java**: pom.xml, build.gradle, settings.gradle, gradle.properties, .gradle/, src/main/java/
- **Go**: go.mod, go.sum, main.go
- **Ruby**: Gemfile, Gemfile.lock, Rakefile, config.ru
- **Rust**: Cargo.toml, Cargo.lock, src/main.rs
- **C#/.NET**: .csproj, .sln, packages.config, appsettings.json

### Cloud Provider Detection
- **AWS**: aws/ directory, AWS SDK imports (boto3, aws-sdk), AWS CloudFormation templates, AWS SAM templates
- **Google Cloud**: gcloud/ directory, GCP SDK imports, gcloud-deployment.yaml
- **Azure**: azure/ directory, Azure SDK imports, ARM templates, Bicep files
- **Alibaba Cloud**: alibaba-cloud/ directory, Aliyun SDK imports
- **DigitalOcean**: digitalocean/ directory, doctl/
- **Linode**: linode/ directory, linode-cli/
- **Heroku**: Procfile, Heroku-specific config
- **Vercel**: vercel.json, .vercelignore
- **Netlify**: netlify.toml, netlify.toml
- **Cloudflare Workers**: wrangler.toml, workers/

### Unsupported Platform Fallback
- **Detection Failed**: If no platform detected after checking all indicators -> Load generic infrastructure patterns and ask clarifying questions
- **Questions to Ask**:
  - "What container platform are you using (Docker, Kubernetes, etc.)?"
  - "What CI/CD platform are you using?"
  - "What cloud provider (AWS, GCP, Azure, etc.) or on-premise infrastructure?"
  - "What configuration management tool (Ansible, Chef, Puppet, etc.)?"
- **Fallback Strategy**: Load generic container/infrastructure patterns and request user confirmation

## EXECUTION PROTOCOL

### Phase 1: Clarification
1. **Detect Mode**: WRITE vs REVIEW based on keywords
2. **Detect Context**: Platform (Docker, K8s, Terraform), application type
3. **Load Patterns**: Progressive (write) or Exhaustive (review)

### Phase 2: Planning
1. Load relevant pattern references
2. Implement infrastructure according to best practices
3. Apply security hardening
4. Consider observability (metrics, logs, traces)
5. Provide platform-specific examples

### Phase 3: Execution
1. Load all checklist references
2. Systematically check each category:
   - Infrastructure (CI/CD, containers, IaC)
   - Security (container escapes, least privilege, secrets)
   - Observability (monitoring, logging, alerting)
   - Deployment strategies (rollback, gradual rollout)
3. Provide prioritized issues with severity levels

### Phase 4: Validation
- Verify infrastructure follows loaded patterns
- Check for security vulnerabilities
- Ensure observability is comprehensive
- Validate rollback mechanisms exist


### Write Mode Output
```markdown
## Infrastructure Implementation: [Component]

### Technology Stack
[Platform choice with rationale]

### Configuration
```yaml
# Dockerfile / Kubernetes manifest / Terraform
configuration here
```

### Security Considerations
- [Security measure 1]
- [Security measure 2]

### Observability
- Metrics: [metrics collected]
- Logs: [logging strategy]
- Alerts: [alerting rules]

### Related Patterns
@infrastructure/[specific-pattern].md
```

### Review Mode Output
```markdown
## Infrastructure Review Report

### Critical Issues
1. **[Issue Name]**: [Component: file]
   - Severity: CRITICAL
   - Description: [Issue details]
   - Impact: [Potential consequence]
   - Fix: [Recommended action]
   - Reference: @security/CONTAINER-SECURITY.md

### High Priority Issues
[Same format]

### Medium Priority Issues
[Same format]

### Low Priority Issues
[Same format]

### Recommendations
1. [Improvement suggestion]
2. [Improvement suggestion]
```
