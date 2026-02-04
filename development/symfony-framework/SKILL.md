---
name: symfony-framework
description: Comprehensive Symfony 6.4 development skill for web applications, APIs, and microservices.
license: MIT
version: 1.0.0
---

# Symfony Framework Development Skill

## Quick Start

```bash
# Full web app
symfony new project_name --version="6.4.*" --webapp

# API/Microservice
symfony new project_name --version="6.4.*"

# Without CLI
composer create-project symfony/skeleton:"6.4.*" project_name
```

## Core Patterns

### Controller
- Extend `AbstractController`
- Use attributes for routing: `#[Route('/path', name: 'route_name')]`
- Automatic entity parameter conversion

### Services
- Autowiring by default
- Configure in `config/services.yaml`

### Doctrine
- Create entity: `php bin/console make:entity`
- Create migration: `php bin/console make:migration`
- Execute: `php bin/console doctrine:migrations:migrate`

### Forms
- Dedicated `FormType` classes
- Handle in controller: `createForm()`, `handleRequest()`, `isSubmitted()`, `isValid()`

### Security
- Configure in `config/packages/security.yaml`
- Use Voters for authorization

## Essential Commands

```bash
php bin/console cache:clear
php bin/console debug:router
php bin/console debug:container
php bin/console make:controller
php bin/console make:crud Product
```

## Best Practices

1. Use dependency injection
2. Prefer composition over inheritance
3. Keep controllers thin
4. Use DTOs for API input/output
5. Repository pattern for queries
6. Voters for authorization
7. Cache expensive operations
8. TDD for critical features

## Deployment Checklist

1. `APP_ENV=prod`, `APP_DEBUG=0`
2. `composer install --no-dev --optimize-autoloader`
3. `php bin/console cache:clear --env=prod`
4. `npm run build`
5. `php bin/console doctrine:migrations:migrate --env=prod`

## References

Pour détails avancés :
- `references/doctrine-advanced.md` - ORM patterns
- `references/security-detailed.md` - Security configs
- `references/api-platform.md` - API Platform
- `references/testing-complete.md` - Testing strategies
- `references/performance-tuning.md` - Optimization
