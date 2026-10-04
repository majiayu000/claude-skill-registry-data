---
name: whmcs-gitlab-ci
description: GitLab CI/CD for WHMCS
category: Automation & DevOps
version: 1.0.0
---

# WHMCS GitLab CI/CD Skill

## Overview
This skill provides patterns for configuring GitLab CI/CD for WHMCS.

## Implementation Patterns

### GitLab CI Manager
```php
<?php
/**
 * WHMCS GitLab CI/CD
 * Manages GitLab CI configuration
 */

namespace WHMCS\Module\DevOps\GitLab;

class GitLabCIManager {
    /**
     * Generate .gitlab-ci.yml
     */
    public function generateCIConfig(): string {
        return <<<YAML
stages:
  - lint
  - test
  - build
  - deploy

lint:
  stage: lint
  script:
    - composer install
    - vendor/bin/phpcs

test:
  stage: test
  services:
    - mysql:8.0
  script:
    - cp .env.example .env
    - composer install
    - vendor/bin/phpunit

build:
  stage: build
  script:
    - docker build -t whmcs:\$CI_COMMIT_SHA .

deploy:
  stage: deploy
  only:
    - main
  script:
    - echo "Deploying..."
YAML;
    }
}
```

## Best Practices

1. **Pipeline Stages**: Clear pipeline stages
2. **Caching**: Use dependency caching
3. **Artifacts**: Pass build artifacts between jobs
4. **Environment**: Use GitLab environments
5. **Review Apps**: Auto-create review apps

## Related Skills

- whmcs-github-actions
- whmcs-jenkins-pipeline
- whmcs-cicd-integration
- whmcs-gitops-workflow