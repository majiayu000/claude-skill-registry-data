---
name: env-var-manager
description: Manages environment variable additions and updates across all project files. Use when adding new environment variables, updating PORT configuration, modifying deployment configurations, or documenting configuration requirements.
---

# Environment Variable Manager

This skill ensures environment variables are properly added, documented, and configured across all project files and deployment platforms.

## Files to Update When Adding Environment Variables

When adding a new environment variable, the following files must be updated in this order:

### 1. `.env.example` (Required)
Add the variable with a descriptive comment explaining its purpose and expected format.

**Format**:
```bash
# Description of what this variable does
# Options: value1, value2, value3 (if applicable)
# Default: default_value (if applicable)
VARIABLE_NAME=example_value
```

**Example**:
```bash
# Server port - useful for local development or platform-specific configs
# Default: 3000
PORT=3000

# Node environment - affects Express server optimization
# Options: development, production, test
# Default: (unset)
NODE_ENV=production
```

### 2. `server.js` (Required)
Implement the variable usage in the application code.

**Pattern**:
```javascript
// Read from environment with fallback default
const variableName = process.env.VARIABLE_NAME || 'default_value';

// For required variables (no default)
const requiredVar = process.env.REQUIRED_VAR;
if (!requiredVar) {
  console.error('ERROR: REQUIRED_VAR environment variable is not set');
  process.exit(1);
}
```

**Examples**:
```javascript
// Optional with default
const port = process.env.PORT || 3000;

// Optional with default
const nodeEnv = process.env.NODE_ENV || 'development';

// Required variable
const apiKey = process.env.API_KEY;
if (!apiKey) {
  console.error('ERROR: API_KEY environment variable must be set');
  process.exit(1);
}
```

### 3. `docs/ENVIRONMENT-VARIABLES.md` (Required)
Add comprehensive documentation in the "Currently Supported Variables" section.

**Format**:
```markdown
### VARIABLE_NAME

**Purpose**: Brief description of what this variable controls

**Required**: Yes/No

**Default**: `default_value` (or "None - must be set" for required vars)

**Valid Values**:
- `value1`: Description
- `value2`: Description

**Example**:
```bash
VARIABLE_NAME=example_value
```

**Platform Notes**:
- AWS Elastic Beanstalk: [specific notes if applicable]
- Google Cloud Run: [specific notes if applicable]
- Docker: [specific notes if applicable]
```

### 4. `CLAUDE.md` (Required)
Update the "Environment Variables" section to include the new variable in the list.

**Format**:
```markdown
**Currently Supported Variables:**
- `PORT` (optional, defaults to 3000) - Server port. Useful for local development or platform-specific configurations
- `NODE_ENV` (optional) - Node environment: `development`, `production`, or `test`
- `NEW_VARIABLE` (required/optional, defaults to X) - Brief description
```

### 5. `docker-compose.yml` (If Applicable)
Add to the environment section if the variable should be set in Docker containers.

**Format**:
```yaml
services:
  usa-spending-app:
    environment:
      - NODE_ENV=production
      - PORT=3000
      - NEW_VARIABLE=value
```

### 6. `Dockerfile` (If Applicable)
Add ENV directive if the variable needs a build-time or runtime default.

**Format**:
```dockerfile
# For build-time variables
ARG VARIABLE_NAME=default_value

# For runtime variables with defaults
ENV VARIABLE_NAME=default_value
```

**Note**: Only add to Dockerfile if a default is truly needed. Prefer runtime configuration via docker-compose.yml or deployment platform.

### 7. Deployment Documentation (If Platform-Specific)
Update `docs/DEPLOYMENT.md` if the variable requires special handling on specific platforms.

## Complete Checklist for Adding Environment Variables

Use this checklist to ensure all steps are completed:

- [ ] Add to `.env.example` with descriptive comment and example value
- [ ] Implement in `server.js` with appropriate default or required check
- [ ] Document in `docs/ENVIRONMENT-VARIABLES.md` with full details
- [ ] Update variable list in `CLAUDE.md` "Environment Variables" section
- [ ] Add to `docker-compose.yml` environment section (if applicable)
- [ ] Add to `Dockerfile` ENV/ARG (if applicable)
- [ ] Update `docs/DEPLOYMENT.md` with platform-specific instructions (if needed)
- [ ] Test locally without `.env` file (verify defaults work)
- [ ] Test locally with `.env` file (verify variable is read correctly)
- [ ] Verify `.env` is in `.gitignore` (should already be there)
- [ ] Never commit actual `.env` file to repository
- [ ] Update `CHANGELOG.md` under [Unreleased] > Added section

## Security Rules

### Sensitive Values
**API Keys, Passwords, Secrets, Tokens**:
- NEVER hardcode in source code
- NEVER commit to `.env.example` with real values (use placeholders)
- MUST use platform-specific secret managers in production:
  - AWS: AWS Secrets Manager or Parameter Store
  - Google Cloud: Secret Manager
  - Heroku: Config Vars (encrypted at rest)
  - Docker: Docker Secrets or external secret management

### Non-Sensitive Values
**Port numbers, feature flags, public URLs**:
- Safe to include in `.env.example`
- Can have defaults in source code

### Required vs Optional Variables

**Required Variables** (no safe default):
```javascript
const apiKey = process.env.API_KEY;
if (!apiKey) {
  console.error('ERROR: API_KEY is required but not set');
  process.exit(1);
}
```

**Optional Variables** (with safe defaults):
```javascript
const port = process.env.PORT || 3000;
const logLevel = process.env.LOG_LEVEL || 'info';
```

## Platform-Specific Considerations

### Google Cloud Run
- **PORT**: Automatically assigned by Cloud Run (typically 8080). DO NOT hardcode. Application must read from `process.env.PORT`.
- **Secrets**: Use Secret Manager, reference in `gcloud run deploy` with `--set-secrets`

### AWS Elastic Beanstalk
- **PORT**: Can be set via environment properties, but application must read from `process.env.PORT`
- **Secrets**: Use AWS Secrets Manager, reference in `.ebextensions` or set via console

### AWS ECS/Fargate
- **Environment Variables**: Set in task definition under `containerDefinitions[].environment`
- **Secrets**: Use `secrets` field in task definition to pull from Secrets Manager or Parameter Store

### Heroku
- **PORT**: Automatically assigned by Heroku. Application must read from `process.env.PORT`
- **Config Vars**: Set via `heroku config:set VARIABLE=value` or dashboard

### Docker / Docker Compose
- **Environment Variables**: Set in `docker-compose.yml` under `environment` or via `.env` file
- **Secrets**: Use Docker Secrets for swarm mode, or mount secret files as volumes

## Common Patterns

### Feature Flags
```javascript
const featureEnabled = process.env.FEATURE_NAME === 'true';
if (featureEnabled) {
  // Feature-specific code
}
```

### API Configuration
```javascript
const apiBaseUrl = process.env.API_BASE_URL || 'https://api.example.com';
const apiTimeout = parseInt(process.env.API_TIMEOUT || '5000', 10);
```

### Database Configuration
```javascript
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432', 10),
  database: process.env.DB_NAME || 'myapp',
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
};

// Validate required fields
if (!dbConfig.user || !dbConfig.password) {
  console.error('ERROR: DB_USER and DB_PASSWORD must be set');
  process.exit(1);
}
```

### Multi-Environment Configuration
```javascript
const isDevelopment = process.env.NODE_ENV === 'development';
const isProduction = process.env.NODE_ENV === 'production';
const isTest = process.env.NODE_ENV === 'test';

if (isDevelopment) {
  // Development-specific settings
}
```

## Testing Environment Variables

### Local Testing Without .env
```bash
# Test that defaults work
npm start

# Verify application starts successfully
# Check that default values are used
```

### Local Testing With .env
```bash
# Create .env file
cp .env.example .env

# Edit .env with test values
# Run application
npm start

# Verify variables are read correctly
```

### Testing Required Variables
```bash
# Test that application fails gracefully when required var is missing
# Remove required variable from .env
npm start

# Should see error message and exit with code 1
```

## Documentation Standards

### .env.example Format
```bash
# ============================================
# Server Configuration
# ============================================

# Server port
# Default: 3000
PORT=3000

# ============================================
# Application Settings
# ============================================

# Node environment (development, production, test)
# Default: (unset)
NODE_ENV=production

# ============================================
# API Configuration
# ============================================

# External API base URL
# Required: Yes
API_BASE_URL=https://api.example.com

# API timeout in milliseconds
# Default: 5000
API_TIMEOUT=5000
```

### ENVIRONMENT-VARIABLES.md Format
Follow the existing structure in `docs/ENVIRONMENT-VARIABLES.md`:
1. Currently Supported Variables (list with descriptions)
2. Local Development Setup (how to set variables)
3. Platform-Specific Setup (AWS, GCP, Heroku, Docker)
4. Security Best Practices
5. Troubleshooting

## Troubleshooting

### Variable Not Being Read
1. Check spelling in `.env` file matches code exactly
2. Verify `.env` file is in project root (same directory as `server.js`)
3. Restart server after changing `.env` file
4. Check for syntax errors in `.env` (no quotes needed, no spaces around `=`)
5. Verify `dotenv` package is installed if using: `npm install dotenv`

### Variable Not Available in Docker
1. Check variable is defined in `docker-compose.yml` environment section
2. Rebuild container: `docker compose up --build`
3. Check variable in running container: `docker exec container_name env | grep VARIABLE`

### Wrong Default Value Used
1. Verify fallback logic: `process.env.VAR || 'default'`
2. Check for empty string: `process.env.VAR || 'default'` (empty string is falsy)
3. For numbers, use: `parseInt(process.env.VAR || '100', 10)`

## Current Environment Variables

**Reference**: See `docs/ENVIRONMENT-VARIABLES.md` for the authoritative list.

**Currently Configured**:
- `PORT` - Server port (default: 3000)
- `NODE_ENV` - Node environment (default: unset)

## Best Practices Summary

1. **Always update `.env.example`** - Never commit actual `.env`
2. **Document everything** - Update docs/ENVIRONMENT-VARIABLES.md with full details
3. **Use descriptive names** - `API_TIMEOUT` not `TIMEOUT`, `DB_HOST` not `HOST`
4. **Provide safe defaults** - Unless the variable is truly required
5. **Validate required variables** - Exit with clear error message if missing
6. **Never hardcode secrets** - Use environment variables and secret managers
7. **Test both scenarios** - With and without `.env` file
8. **Keep documentation in sync** - Update all files when adding variables
9. **Use platform secrets** - Don't put sensitive data in environment variables in production
10. **Follow naming conventions** - UPPER_CASE_WITH_UNDERSCORES

## Quick Reference Commands

```bash
# Create .env from example
cp .env.example .env

# View current environment variables (local)
printenv | grep -E '(PORT|NODE_ENV)'

# Set variable temporarily (bash/zsh)
export VARIABLE_NAME=value
npm start

# Set variable inline (bash/zsh)
VARIABLE_NAME=value npm start

# Docker Compose with custom env file
docker compose --env-file .env.production up

# Check variable in Docker container
docker exec usa-spending-search env | grep VARIABLE_NAME

# AWS EB set variable
eb setenv VARIABLE_NAME=value

# Heroku set variable
heroku config:set VARIABLE_NAME=value

# GCP Cloud Run set variable
gcloud run services update SERVICE_NAME --set-env-vars="VARIABLE_NAME=value"
```

## Resources

- Project Documentation: `docs/ENVIRONMENT-VARIABLES.md`
- Deployment Guide: `docs/DEPLOYMENT.md`
- Quick Start Guide: `docs/quick-start-guide.md`
- Example Template: `.env.example`
