---
name: aws-amplify
description: Deploys and hosts full-stack web applications on AWS Amplify with SSR support, CI/CD, and backend services. Use when deploying Next.js apps to AWS, setting up Amplify hosting, or configuring Amplify backends.
---

# AWS Amplify Hosting

Full-stack deployment platform for web applications with automatic CI/CD, SSR support, and integrated AWS services.

## Quick Start

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Configure AWS credentials
amplify configure

# Initialize Amplify in project
amplify init

# Deploy via Console
# 1. Go to AWS Amplify Console
# 2. Connect your Git repository
# 3. Amplify auto-detects framework
```

## Supported Frameworks

- Next.js (SSR, SSG, ISR)
- React (CRA, Vite)
- Vue.js / Nuxt
- Angular
- Gatsby
- Astro
- SvelteKit
- Static sites

## Git-Based Deployment

### Connect Repository

1. AWS Console > Amplify > Create new app
2. Choose Git provider (GitHub, GitLab, Bitbucket, CodeCommit)
3. Select repository and branch
4. Review build settings
5. Deploy

### amplify.yml (Build Spec)

```yaml
version: 1
applications:
  - frontend:
      phases:
        preBuild:
          commands:
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: .next
        files:
          - '**/*'
      cache:
        paths:
          - node_modules/**/*
          - .next/cache/**/*
```

## Next.js Configuration

### Next.js 14+ (App Router)

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

### Environment Variables

```yaml
version: 1
frontend:
  phases:
    build:
      commands:
        - echo "NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL" >> .env.production
        - npm run build
```

### Custom Headers

```yaml
# amplify.yml
customHeaders:
  - pattern: '**/*'
    headers:
      - key: Strict-Transport-Security
        value: max-age=31536000; includeSubDomains
      - key: X-Content-Type-Options
        value: nosniff
      - key: X-Frame-Options
        value: DENY
  - pattern: '*.js'
    headers:
      - key: Cache-Control
        value: public, max-age=31536000, immutable
```

## Environment Variables

### Console Setup

1. App settings > Environment variables
2. Add key-value pairs
3. Choose branch scope (all or specific)

### In amplify.yml

```yaml
frontend:
  phases:
    build:
      commands:
        - printenv | grep -E '^(NEXT_|REACT_APP_)' >> .env.production
        - npm run build
```

### Secrets

Store sensitive values securely:

```yaml
frontend:
  phases:
    preBuild:
      commands:
        - aws secretsmanager get-secret-value --secret-id prod/api-key --query SecretString --output text > .env.local
```

## Custom Domains

### Add Domain

1. App settings > Domain management
2. Add domain
3. Configure DNS (Route 53 or external)
4. Wait for SSL certificate

### Subdomains

```
# Branch subdomains
main    -> example.com
develop -> dev.example.com
feature -> feature.example.com
```

## Redirects & Rewrites

### amplify.yml

```yaml
customRules:
  # Redirect
  - source: /old-path
    target: /new-path
    status: '301'

  # Rewrite (proxy)
  - source: /api/<*>
    target: https://api.example.com/<*>
    status: '200'

  # SPA fallback
  - source: </^[^.]+$|\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|ttf|map|json)$)([^.]+$)/>
    target: /index.html
    status: '200'
```

## Branch Deployments

### Auto Branch Detection

```yaml
# amplify.yml (root)
version: 1
backend:
  phases:
    build:
      commands:
        - amplifyPush --simple
frontend:
  phases:
    build:
      commands:
        - npm run build
```

### Branch-Specific Builds

```yaml
frontend:
  phases:
    build:
      commands:
        - if [ "$AWS_BRANCH" = "main" ]; then npm run build:prod; else npm run build:dev; fi
```

## Monorepo Setup

### Select App Directory

1. During setup, enable "My app is a monorepo"
2. Specify app root: `apps/web`

### amplify.yml

```yaml
version: 1
applications:
  - appRoot: apps/web
    frontend:
      phases:
        preBuild:
          commands:
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: .next
        files:
          - '**/*'
```

## Build Performance

### Caching

```yaml
cache:
  paths:
    - node_modules/**/*
    - .next/cache/**/*
    - ~/.npm/**/*
```

### Build Image

```yaml
frontend:
  phases:
    preBuild:
      commands:
        - nvm use 20
        - npm ci
```

## Preview Deployments

### Pull Request Previews

1. App settings > Previews
2. Enable previews
3. Configure:
   - Preview branches
   - Access control (password/Cognito)

```yaml
# Branch patterns
# feature/** -> Preview deployment
# main -> Production
```

## IAM Service Role

### Required Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "amplify:*",
        "s3:*",
        "cloudfront:*",
        "route53:*",
        "acm:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

## Troubleshooting

### Build Fails

```yaml
frontend:
  phases:
    build:
      commands:
        - npm run build 2>&1 | tee build.log
```

### Memory Issues

```yaml
frontend:
  phases:
    build:
      commands:
        - NODE_OPTIONS="--max-old-space-size=8192" npm run build
```

### Image Optimization

Next.js image optimization works automatically. Amplify deploys Sharp internally.

See [references/configuration.md](references/configuration.md) for complete build spec and [references/backends.md](references/backends.md) for Amplify backend setup.
