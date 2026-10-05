---
name: feature-dev
description: Comprehensive feature development workflow management with branching strategies, code reviews, testing automation, and deployment coordination.
license: MIT
---

# Feature Development Workflow

## Overview

Complete feature development toolkit providing structured workflows, branching strategies, automated testing, code review processes, and deployment coordination for modern software development teams.

## Quick Start

### Installation
```bash
npm install -g @feature-dev/cli
# or
npx @feature-dev/cli init
```

### Initialize Feature Development
```bash
# Initialize in existing project
feature-dev init

# Create new project with feature workflow
feature-dev create my-project --template=feature-driven
```

## Feature Workflow Management

### Feature Creation
```bash
# Start new feature
feature-dev start user-authentication

# Start feature with specific type
feature-dev start user-authentication --type=feature --epic=EPIC-123

# Start feature with template
feature-dev start user-authentication --template=api-endpoint

# List active features
feature-dev list --status=active
```

**Feature Configuration**
```javascript
// feature.config.js
module.exports = {
  name: 'user-authentication',
  type: 'feature',
  epic: 'EPIC-123',
  assignee: 'john.doe@company.com',
  
  branches: {
    main: 'main',
    develop: 'develop',
    feature: 'feature/user-authentication',
    release: 'release/user-authentication'
  },
  
  tasks: [
    {
      id: 'TASK-001',
      title: 'Design authentication flow',
      type: 'design',
      status: 'todo'
    },
    {
      id: 'TASK-002', 
      title: 'Implement login endpoint',
      type: 'development',
      status: 'todo'
    },
    {
      id: 'TASK-003',
      title: 'Write authentication tests',
      type: 'testing',
      status: 'todo'
    }
  ],
  
  definition: {
    acceptanceCriteria: [
      'User can login with valid credentials',
      'User receives error for invalid credentials',
      'Session management works correctly',
      'Password reset functionality available'
    ],
    
    technicalRequirements: [
      'JWT token authentication',
      'Password hashing with bcrypt',
      'Rate limiting on login attempts',
      'Session timeout after 1 hour'
    ]
  }
};
```

### Branch Management
```bash
# Create feature branch
feature-dev branch create user-authentication --from=develop

# Switch between branches
feature-dev branch switch user-authentication

# Sync with main branch
feature-dev branch sync user-authentication --with=main

# Merge feature branch
feature-dev branch merge user-authentication --into=develop --strategy= squash
```

**Branch Strategy Configuration**
```javascript
// branch-strategy.config.js
module.exports = {
  strategy: 'gitflow', // or 'github-flow', 'gitlab-flow'
  
  branches: {
    main: {
      name: 'main',
      protection: {
        requireReviews: true,
        requiredReviewers: 2,
        requireUpToDate: true,
        requireStatusChecks: ['ci/ci', 'security/scan']
      }
    },
    
    develop: {
      name: 'develop',
      protection: {
        requireReviews: true,
        requiredReviewers: 1,
        requireUpToDate: true
      }
    },
    
    feature: {
      prefix: 'feature/',
      from: 'develop',
      autoDelete: true
    },
    
    release: {
      prefix: 'release/',
      from: 'develop',
      into: ['main', 'develop']
    },
    
    hotfix: {
      prefix: 'hotfix/',
      from: 'main',
      into: ['main', 'develop']
    }
  },
  
  mergeStrategies: {
    feature: 'squash',
    release: 'merge-commit',
    hotfix: 'merge-commit'
  }
};
```

## Code Development

### Task Management
```bash
# Create task
feature-dev task create "Implement login endpoint" --type=development --assignee=john

# Update task status
feature-dev task update TASK-002 --status=in-progress

# Link task to commit
feature-dev task link TASK-002 --commit=abc123

# View task board
feature-dev board --sprint=current
```

**Task Templates**
```javascript
// task-templates.config.js
module.exports = {
  templates: {
    'api-endpoint': {
      title: 'Implement {endpoint} endpoint',
      description: 'Create REST API endpoint for {feature}',
      checklist: [
        'Define API contract',
        'Implement endpoint logic',
        'Add input validation',
        'Write unit tests',
        'Update API documentation'
      ],
      estimatedHours: 8,
      labels: ['backend', 'api']
    },
    
    'ui-component': {
      title: 'Create {component} component',
      description: 'Build React component for {feature}',
      checklist: [
        'Design component structure',
        'Implement component logic',
        'Add styling',
        'Write component tests',
        'Add accessibility features'
      ],
      estimatedHours: 6,
      labels: ['frontend', 'react']
    },
    
    'test-coverage': {
      title: 'Add tests for {module}',
      description: 'Write comprehensive tests for {module}',
      checklist: [
        'Unit tests',
        'Integration tests',
        'Edge case testing',
        'Performance tests',
        'Coverage report'
      ],
      estimatedHours: 4,
      labels: ['testing', 'quality']
    }
  }
};
```

### Code Quality Gates
```bash
# Run quality checks
feature-dev quality check

# Run specific checks
feature-dev quality check --lint --test --security

# Set quality gates
feature-dev quality gate --coverage=80 --complexity=10 --duplicates=5
```

**Quality Configuration**
```javascript
// quality.config.js
module.exports = {
  gates: {
    coverage: {
      minimum: 80,
      exclude: ['**/*.test.js', '**/*.spec.js'],
      reportFormats: ['html', 'lcov']
    },
    
    complexity: {
      maximum: 10,
      ignorePatterns: ['**/node_modules/**', '**/dist/**']
    },
    
    duplicates: {
      maximum: 5,
      minTokens: 50,
      ignoreAnnotations: true
    },
    
    security: {
      enabled: true,
      rules: ['owasp-top-ten', 'bandit'],
      failOnHigh: true
    },
    
    performance: {
      enabled: true,
      budgets: {
        javascript: 250, // KB
        css: 50, // KB
        images: 500 // KB
      }
    }
  },
  
  tools: {
    linter: 'eslint',
    formatter: 'prettier',
    testRunner: 'jest',
    coverageTool: 'istanbul',
    securityScanner: 'snyk'
  }
};
```

## Testing Automation

### Test Strategy
```bash
# Generate test plan
feature-dev test plan --feature=user-authentication

# Run test suite
feature-dev test run --suite=all

# Run specific test types
feature-dev test run --unit --integration --e2e

# Generate test report
feature-dev test report --format=html --output=./reports
```

**Test Configuration**
```javascript
// test.config.js
module.exports = {
  strategy: 'pyramid', // or 'diamond', 'inverted'
  
  suites: {
    unit: {
      framework: 'jest',
      coverage: {
        minimum: 80,
        thresholds: {
          statements: 80,
          branches: 75,
          functions: 80,
          lines: 80
        }
      },
      timeout: 5000,
      parallel: true
    },
    
    integration: {
      framework: 'jest',
      setup: './test/integration/setup.js',
      teardown: './test/integration/teardown.js',
      timeout: 30000,
      parallel: false
    },
    
    e2e: {
      framework: 'playwright',
      browsers: ['chromium', 'firefox', 'webkit'],
      timeout: 60000,
      retries: 2,
      video: true,
      screenshots: 'on-failure'
    },
    
    performance: {
      framework: 'lighthouse',
      budgets: {
        performance: 90,
        accessibility: 95,
        bestPractices: 90,
        seo: 85
      },
      urls: ['/', '/login', '/dashboard']
    }
  },
  
  data: {
    fixtures: './test/fixtures',
    mocks: './test/mocks',
    factories: './test/factories'
  }
};
```

### Test Data Management
```bash
# Generate test data
feature-dev test data generate --model=user --count=100

# Reset test database
feature-dev test db reset --env=test

# Seed test data
feature-dev test db seed --fixtures=users,posts
```

**Test Data Factory**
```javascript
// test/factories/user-factory.js
const { Factory } = require('@feature-dev/testing');

class UserFactory extends Factory {
  static definition() {
    return {
      id: this.sequence(),
      name: this.faker.name.findName(),
      email: this.faker.internet.email(),
      password: this.crypt('password123'),
      role: this.choice(['user', 'admin'], [0.9, 0.1]),
      createdAt: this.past(),
      updatedAt: this.now()
    };
  }
  
  static admin() {
    return this.state({
      role: 'admin',
      permissions: ['read', 'write', 'delete']
    });
  }
  
  static withPosts(count = 3) {
    return this.afterCreate(async (user) => {
      const posts = await PostFactory.createMany(count, { userId: user.id });
      user.posts = posts;
      return user;
    });
  }
}

module.exports = UserFactory;
```

## Code Review Process

### Review Workflow
```bash
# Create pull request
feature-dev pr create --title="Add user authentication" --draft=false

# Request reviewers
feature-dev pr review request --reviewers=jane.doe,bob.smith --team=backend

# Auto-review with AI
feature-dev pr review ai --focus=security,performance

# Merge PR after approval
feature-dev pr merge --strategy=squash --delete-branch
```

**Review Configuration**
```javascript
// review.config.js
module.exports = {
  autoAssign: {
    enabled: true,
    rules: [
      {
        when: { files: ['**/*.js'] },
        assign: ['backend-team']
      },
      {
        when: { files: ['**/*.css', '**/*.scss'] },
        assign: ['frontend-team']
      },
      {
        when: { labels: ['security'] },
        assign: ['security-team']
      }
    ]
  },
  
  requiredReviewers: {
    minimum: 2,
    maximum: 4,
    excludeAuthor: true,
    excludeCommitters: false
  },
  
  checks: {
    required: [
      'ci/ci',
      'security/scan',
      'coverage/coverage',
      'lint/lint'
    ],
    
    optional: [
      'performance/lighthouse',
      'accessibility/a11y',
      'docs/docs'
    ]
  },
  
  aiReview: {
    enabled: true,
    model: 'gpt-4',
    focus: ['security', 'performance', 'maintainability'],
    maxSuggestions: 10,
    autoComment: true
  },
  
  mergeMethods: {
    default: 'squash',
    allowRebase: false,
    allowMergeCommit: false,
    autoDelete: true
  }
};
```

### Review Templates
```javascript
// review-templates.config.js
module.exports = {
  templates: {
    'feature-review': {
      title: 'Feature Review: {feature}',
      description: `
## Overview
{description}

## Changes Made
{changes}

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass  
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Security
- [ ] Security review completed
- [ ] No sensitive data exposed
- [ ] Authentication/authorization verified

## Documentation
- [ ] API documentation updated
- [ ] User documentation updated
- [ ] Code comments added where needed

## Deployment
- [ ] Migration scripts tested
- [ ] Rollback plan documented
- [ ] Monitoring configured
      `
    },
    
    'bugfix-review': {
      title: 'Bugfix: {issue}',
      description: `
## Issue
{issueDescription}

## Root Cause
{rootCause}

## Fix
{fixDescription}

## Testing
- [ ] Bug reproduction verified
- [ ] Fix resolves issue
- [ ] Regression tests pass
- [ ] Edge cases covered

## Impact Assessment
- [ ] Breaking changes identified
- [ ] Migration requirements documented
- [ ] Performance impact measured
      `
    }
  }
};
```

## Deployment Management

### Deployment Pipeline
```bash
# Deploy to staging
feature-dev deploy staging --feature=user-authentication

# Deploy to production
feature-dev deploy production --version=v1.2.0 --confirm

# Rollback deployment
feature-dev deploy rollback --environment=production --to=v1.1.0

# Monitor deployment
feature-dev deploy monitor --environment=production --duration=30m
```

**Deployment Configuration**
```javascript
// deploy.config.js
module.exports = {
  environments: {
    development: {
      type: 'local',
      autoDeploy: true,
      healthCheck: '/health',
      rollbackOnFailure: false
    },
    
    staging: {
      type: 'kubernetes',
      namespace: 'staging',
      autoDeploy: true,
      healthCheck: '/health',
      rollbackOnFailure: true,
      approvalRequired: false
    },
    
    production: {
      type: 'kubernetes',
      namespace: 'production',
      autoDeploy: false,
      healthCheck: '/health',
      rollbackOnFailure: true,
      approvalRequired: true,
      approvers: ['tech-lead', 'product-manager'],
      deploymentWindow: {
        start: '22:00',
        end: '06:00',
        timezone: 'UTC',
        weekends: false
      }
    }
  },
  
  pipeline: {
    stages: [
      {
        name: 'build',
        parallel: false,
        steps: ['install', 'test', 'lint', 'security-scan']
      },
      {
        name: 'package',
        parallel: false,
        steps: ['build-image', 'push-registry']
      },
      {
        name: 'deploy-staging',
        parallel: false,
        steps: ['deploy-staging', 'health-check', 'integration-tests']
      },
      {
        name: 'approve-production',
        parallel: false,
        steps: ['manual-approval']
      },
      {
        name: 'deploy-production',
        parallel: false,
        steps: ['deploy-production', 'health-check', 'smoke-tests']
      }
    ]
  },
  
  monitoring: {
    metrics: ['response-time', 'error-rate', 'throughput'],
    alerts: [
      {
        metric: 'error-rate',
        threshold: 5, // percentage
        duration: '5m',
        action: 'rollback'
      },
      {
        metric: 'response-time',
        threshold: 2000, // milliseconds
        duration: '10m',
        action: 'alert'
      }
    ]
  }
};
```

### Feature Flags
```bash
# Create feature flag
feature-dev flag create user-authentication --type=boolean --default=false

# Update flag configuration
feature-dev flag update user-authentication --enabled=true --percentage=50

# Target specific users
feature-dev flag target user-authentication --users=john.doe,jane.smith

# Gradual rollout
feature-dev flag rollout user-authentication --strategy=gradual --duration=7d
```

**Feature Flag Configuration**
```javascript
// feature-flags.config.js
module.exports = {
  provider: 'launchdarkly', // or 'unleash', 'custom'
  
  flags: {
    'user-authentication': {
      type: 'boolean',
      defaultValue: false,
      description: 'Enable new user authentication system',
      
      targeting: {
        rules: [
          {
            name: 'beta-users',
            condition: {
              attribute: 'email',
              operator: 'endsWith',
              value: '@beta.company.com'
            },
            variation: true
          },
          {
            name: 'percentage-rollout',
            condition: {
              attribute: 'random',
              operator: 'lessThan',
              value: 0.1 // 10%
            },
            variation: true
          }
        ]
      },
      
      rollout: {
        strategy: 'gradual',
        schedule: {
          start: '2024-01-15T00:00:00Z',
          duration: '7d',
          steps: [
            { percentage: 10, duration: '1d' },
            { percentage: 25, duration: '2d' },
            { percentage: 50, duration: '2d' },
            { percentage: 100, duration: '2d' }
          ]
        }
      }
    }
  },
  
  analytics: {
    trackEvents: true,
    trackExposures: true,
    trackGoals: ['conversion-rate', 'user-satisfaction']
  }
};
```

## Monitoring & Analytics

### Feature Analytics
```bash
# Track feature usage
feature-dev analytics track --feature=user-authentication --event=login

# Generate feature report
feature-dev analytics report --feature=user-authentication --period=30d

# Compare feature performance
feature-dev analytics compare --features=old-auth,new-auth --metrics=conversion,time-to-complete
```

**Analytics Configuration**
```javascript
// analytics.config.js
module.exports = {
  provider: 'mixpanel', // or 'amplitude', 'segment', 'custom'
  
  tracking: {
    events: [
      {
        name: 'feature_used',
        properties: ['feature_name', 'user_id', 'timestamp', 'context']
      },
      {
        name: 'feature_completed',
        properties: ['feature_name', 'user_id', 'completion_time', 'success']
      },
      {
        name: 'feature_error',
        properties: ['feature_name', 'user_id', 'error_type', 'error_message']
      }
    ],
    
    goals: [
      {
        name: 'user-authentication-success',
        event: 'feature_completed',
        filters: { feature_name: 'user-authentication', success: true }
      },
      {
        name: 'user-authentication-failure',
        event: 'feature_error',
        filters: { feature_name: 'user-authentication' }
      }
    ]
  },
  
  reporting: {
    dashboards: [
      {
        name: 'Feature Performance',
        widgets: [
          {
            type: 'line-chart',
            metric: 'feature_usage',
            groupBy: 'feature_name',
            timeRange: '30d'
          },
          {
            type: 'funnel',
            steps: ['feature_started', 'feature_completed'],
            filter: { feature_name: 'user-authentication' }
          }
        ]
      }
    ],
    
    alerts: [
      {
        name: 'High Error Rate',
        condition: {
          metric: 'feature_error_rate',
          operator: '>',
          value: 0.05 // 5%
        },
        notification: ['slack', 'email']
      }
    ]
  }
};
```

## Integration

### CI/CD Integration
```yaml
# .github/workflows/feature-development.yml
name: Feature Development

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Feature Dev
        run: |
          npm install -g @feature-dev/cli
          feature-dev init --ci
      
      - name: Quality Gates
        run: |
          feature-dev quality check --coverage --security --performance
      
      - name: Test Suite
        run: |
          feature-dev test run --unit --integration
      
      - name: AI Review
        run: |
          feature-dev pr review ai --focus=security,performance
```

### IDE Integration
```bash
# VS Code extension
code --install-extension feature-dev.vscode

# JetBrains plugin
# Install from marketplace: Feature Development

# Vim/Neovim plugin
git clone https://github.com/feature-dev/vim-plugin ~/.vim/pack/feature/start/
```

## API Reference

### Core Classes

**FeatureManager**
```javascript
const { FeatureManager } = require('@feature-dev/core');

const featureManager = new FeatureManager({
  repository: './',
  branchStrategy: 'gitflow'
});

const feature = await featureManager.start('user-authentication');
await featureManager.complete(feature.id);
```

**TaskManager**
```javascript
const { TaskManager } = require('@feature-dev/tasks');

const taskManager = new TaskManager();
const task = await taskManager.create({
  title: 'Implement login endpoint',
  type: 'development',
  assignee: 'john.doe'
});
```

**DeploymentManager**
```javascript
const { DeploymentManager } = require('@feature-dev/deploy');

const deployManager = new DeploymentManager();
const deployment = await deployManager.deploy('staging', {
  version: 'v1.2.0',
  feature: 'user-authentication'
});
```

## Contributing

1. Fork repository
2. Create feature branch
3. Follow development workflow
4. Add comprehensive tests
5. Submit pull request

## License

MIT License - see LICENSE file for details.