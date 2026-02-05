---
name: devops
description:
    Generates DevOps configurations and scripts for deploying and managing
    Laravel applications. Run local commands to debug and deploy.
---

# Devops

## Instructions

### Environment Setup

#### Option 1: Docker Development (Recommended)

```bash
# Copy environment file
cp .env.example .env

# Start all services
docker compose up -d

# Install PHP dependencies
docker compose exec app composer install

# Install Node dependencies
docker compose exec app yarn install

# Generate application key
docker compose exec app php artisan key:generate

# Run migrations
docker compose exec app php artisan migrate

# Build frontend assets
docker compose exec app yarn dev
```

#### Option 2: Local Development

Ensure PHP 8.4+ is installed, then:

```bash
# Install dependencies
composer install
yarn install

# Setup environment
cp .env.example .env
php artisan key:generate

# Configure database and run migrations
php artisan migrate

# Start development servers
composer run dev  # Starts Laravel Octane, queue worker, logs, and Vite
```

### Development Scripts

All commands should run from a Docker container. The project includes several
useful Composer scripts:

- `composer run dev` - Start all development services (Octane, queue, logs,
  Vite)
- `composer run ide-helper` - Generate IDE helper files
- `composer run phpstan` - Run static analysis
- `composer run pint` - Check code style
- `composer run pint:fix` - Fix code style issues
- `composer run rector` - Check for code modernization opportunities
- `composer run rector:fix` - Apply code modernization

### CI/CD Pipeline

The project uses GitHub Actions with:

- **Linting**: PHPStan, Laravel Pint, Rector
- **Testing**: Pest with coverage and mutation testing
- **Code Coverage**: Codecov integration
- **Parallel Execution**: Tests run in parallel for faster feedback

### Environment-Specific Notes

- **Local Development**: Use Docker Compose for consistent environment
- **Testing**: Separate PostgreSQL instance for tests
- **Production**: Optimized for Laravel Octane with FrankenPHP
- **Debugging**: Xdebug available in development, Telescope for application
  debugging
