---
name: deployment-kamal
description: This skill should be used when the user asks about deploying Rails applications, Kamal deployment, Docker containers, production configuration, environment variables, secrets management, CI/CD pipelines, server provisioning, zero-downtime deploys, Kamal Proxy, Thruster, or infrastructure setup. Also use when discussing production optimization, deployment strategies, or hosting options. Examples:

<example>
Context: User wants to deploy their Rails 8 app
user: "How do I deploy my Rails app to production?"
assistant: "Rails 8 includes Kamal for deployment. Let me show you the setup."
<commentary>
This relates to Kamal deployment workflow and configuration.
</commentary>
</example>

<example>
Context: User asks about zero-downtime deploys
user: "How can I deploy without taking my app offline?"
assistant: "Kamal provides zero-downtime deploys by default. Let me explain how it works."
<commentary>
This involves Kamal's rolling deployment strategy.
</commentary>
</example>

<example>
Context: User needs environment-specific configuration
user: "How do I configure different settings for staging vs production?"
assistant: "I'll show you Rails environment configuration and Kamal deployment targets."
<commentary>
This relates to Rails environments and Kamal configuration.
</commentary>
</example>
---

# Deployment & Infrastructure: Kamal and Rails 8

## Overview

Rails 8 ships with **Kamal 2** for zero-downtime deployments to any Linux server. Kamal eliminates PaaS lock-in and Kubernetes complexity, giving you full control with simple tools.

**Kamal philosophy:**
- Deploy to any server (VPS, cloud, on-premise)
- Docker-based containers
- Zero-downtime deploys
- No vendor lock-in
- Simple configuration
- One command to deploy

Rails 8 also includes:
- **Thruster**: Rust-based proxy for asset serving and compression
- **Kamal Proxy**: Traffic routing and SSL termination
- **Dockerfile**: Production-ready container configuration

## Kamal Basics

### What Kamal Does

Kamal turns a fresh Linux server into a production Rails host with a single command:

```bash
kamal setup
```

This:
1. Installs Docker
2. Configures the server
3. Pulls your application image
4. Starts containers
5. Configures proxy
6. Sets up SSL (via Let's Encrypt)

Subsequent deploys are just:

```bash
kamal deploy
```

### Zero-Downtime Deploys

Kamal performs rolling deploys:

1. Builds new Docker image
2. Pushes to registry
3. Pulls image on servers
4. Starts new containers
5. Waits for health check
6. Shifts traffic to new containers
7. Stops old containers

Users never see downtime.

### Configuration

Kamal is configured in `config/deploy.yml`:

```yaml
service: myapp
image: username/myapp

servers:
  web:
    hosts:
      - 192.168.1.1
      - 192.168.1.2

proxy:
  ssl: true
  host: myapp.com

registry:
  username: username
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  secret:
    - RAILS_MASTER_KEY

healthcheck:
  path: /up
  interval: 10s
```

## Kamal 2 Features

### Kamal Proxy

Rails 8 includes Kamal Proxy (replaces Traefik):

- Simpler configuration
- Better performance
- Integrated health checks
- Automatic SSL via Let's Encrypt
- Traffic routing
- Request buffering

### Registry-Free Deploys (Rails 8.1+)

Kamal 2.8+ supports local registry for simple deploys:

```yaml
# config/deploy.yml
registry:
  local: true  # No Docker Hub/GHCR needed
```

Perfect for getting started. Use remote registry for larger deployments.

### Accessories

Deploy supporting services alongside your app:

```yaml
accessories:
  db:
    image: postgres:16
    host: 192.168.1.1
    env:
      POSTGRES_PASSWORD: secret
    volumes:
      - /var/lib/postgresql/data:/var/lib/postgresql/data

  redis:
    image: redis:7
    host: 192.168.1.1
```

## Rails 8 Dockerfile

Generated Dockerfile is production-ready:

```dockerfile
FROM ruby:3.2-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Install gems
COPY Gemfile* ./
RUN bundle install

# Copy application
COPY . .

# Precompile assets
RUN bundle exec rails assets:precompile

# Start Thruster
CMD ["bin/thruster", "bin/rails", "server"]
```

## Thruster

Rust-based proxy that sits in front of Puma:

**Features:**
- X-Sendfile acceleration (serve files efficiently)
- Asset caching (immutable assets cached forever)
- Compression (gzip/brotli)
- HTTP/2 support

**Configuration:**

```bash
# bin/thruster
thruster \
  --http-port=80 \
  --https-port=443 \
  --storage-path=/var/thruster \
  bin/rails server
```

Thruster handles all the performance optimizations you'd normally configure in Nginx.

## Environment Configuration

### Rails Environments

Rails has three default environments:

- **development**: Local development (verbose logs, code reloading)
- **test**: Running tests (separate database, fixtures)
- **production**: Live application (caching, optimized, secure)

Configure in `config/environments/`:

```ruby
# config/environments/production.rb
Rails.application.configure do
  config.cache_classes = true
  config.eager_load = true
  config.consider_all_requests_local = false
  config.public_file_server.enabled = true
  config.assets.compile = false
  config.assets.digest = true
  config.log_level = :info
  config.force_ssl = true
end
```

### Secrets and Credentials

Rails 8 uses encrypted credentials:

```bash
# Edit credentials
rails credentials:edit

# Edit environment-specific credentials
rails credentials:edit --environment production
```

```yaml
# config/credentials/production.yml.enc
secret_key_base: abc123...
database:
  password: dbpass
aws:
  access_key_id: AKIAIOSFODNN7EXAMPLE
  secret_access_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Access in code:

```ruby
Rails.application.credentials.aws[:access_key_id]
Rails.application.credentials.database[:password]
```

Kamal can fetch secrets from credentials:

```bash
# .kamal/secrets
KAMAL_REGISTRY_PASSWORD=$(rails credentials:fetch kamal.registry_password)
```

See `references/kamal-setup.md` for complete deployment guide.

## CI/CD with Rails 8

### Local CI (Rails 8.1+)

> **Note**: This feature is available in Rails 8.1+. Verify your Rails version
> supports `config/ci.rb` before using.

Rails 8.1 includes built-in CI configuration:

```ruby
# config/ci.rb
CI.run do
  step "Setup", "bin/setup --skip-server"
  step "Style: Ruby", "bin/rubocop"
  step "Security: Gem audit", "bin/bundler-audit"
  step "Tests: Rails", "bin/rails test"

  if success?
    step "Signoff: All systems go", "gh signoff"
  else
    failure "CI failed. Fix issues and try again."
  end
end
```

Run locally:

```bash
bin/ci
```

Perfect for fast feedback without cloud CI.

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres

    steps:
      - uses: actions/checkout@v3
      - uses: ruby/setup-ruby@v1
        with:
          bundler-cache: true
      - run: bin/rails db:setup
      - run: bin/rails test
      - run: bin/rails test:system

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: webfactory/ssh-agent@v0.8.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
      - run: gem install kamal
      - run: kamal deploy
```

## Production Best Practices

1. **Use production environment** with proper config
2. **Enable SSL/TLS** (force_ssl = true)
3. **Set SECRET_KEY_BASE** via credentials
4. **Use environment variables** for secrets
5. **Enable caching** (Solid Cache in Rails 8)
6. **Configure logging** appropriately
7. **Set up monitoring** (error tracking, metrics)
8. **Use CDN** for assets
9. **Configure database** connection pooling
10. **Set up backups** (database, credentials)

See `references/production-checklist.md` for complete checklist.

## Further Reading

For deeper exploration:

- **`references/kamal-setup.md`**: Complete Kamal deployment guide
- **`references/production-checklist.md`**: Production readiness checklist

For code examples:

- **`examples/basic-config.yml`**: Minimal single-server setup
- **`examples/registry-free-config.yml`**: No Docker Hub needed (Kamal 2.8+)
- **`examples/multi-server-config.yml`**: Multiple web servers with workers
- **`examples/with-accessories-config.yml`**: PostgreSQL and Redis setup
- **`examples/staging-production-config.yml`**: Environment-specific deploys
- **`examples/custom-healthcheck-config.yml`**: Detailed health checks
- **`examples/advanced-services-config.yml`**: Resource limits and scaling
- **`examples/deployment-hooks.sh`**: Pre/post deploy automation

## Summary

Rails 8 deployment provides:
- **Kamal 2**: Zero-downtime deploys to any server
- **Thruster**: Performance proxy
- **Kamal Proxy**: Traffic routing
- **Dockerfile**: Production-ready containers
- **Credentials**: Encrypted secrets
- **Local CI**: Fast feedback
- **Self-hosting**: No vendor lock-in

Master Kamal and deploy with confidence to any infrastructure.
