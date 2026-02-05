---
name: github-actions-ci-workflow
description: Sets up comprehensive GitHub Actions CI/CD workflows for modern web applications. This skill should be used when configuring automated lint, test, build, and deploy pipelines, adding preview URL comments on pull requests, or optimizing workflow caching. Use when setting up continuous integration, deployment automation, GitHub Actions, CI/CD pipeline, preview deployments, or workflow optimization.
---

# GitHub Actions CI Workflow

Set up complete GitHub Actions workflows for continuous integration and deployment of worldbuilding applications.

## Overview

To configure comprehensive CI/CD pipelines with GitHub Actions:

1. Analyze the project structure and dependencies
2. Generate workflow files for lint, test, build, and deploy stages
3. Configure caching strategies for node_modules, Next.js cache, and build artifacts
4. Add preview deployment with automatic URL comments on pull requests
5. Set up environment-specific deployment targets

## Workflow Structure

Create the following workflow files in `.github/workflows/`:

### CI Workflow (`ci.yml`)

To set up continuous integration:

1. Configure triggers for push to main/master and pull requests
2. Set up job matrix for multiple Node.js versions if needed
3. Add checkout, dependency installation with caching
4. Run linting (ESLint, Prettier, type checking)
5. Execute test suites with coverage reporting
6. Build the application to verify no build errors
7. Upload build artifacts for deployment jobs

### Deploy Workflow (`deploy.yml`)

To set up continuous deployment:

1. Trigger on push to main/master branch
2. Download build artifacts from CI workflow
3. Deploy to target environment (Vercel, Netlify, AWS, etc.)
4. Set environment variables and secrets
5. Notify on deployment success/failure

### Preview Deployment (`preview.yml`)

To set up preview deployments for pull requests:

1. Trigger on pull_request events
2. Build and deploy to preview environment
3. Generate unique preview URL
4. Comment preview URL on pull request using GitHub API
5. Clean up preview deployments when PR is closed

## Caching Strategy

To optimize workflow performance:

1. Cache `node_modules` with dependency lock file as cache key
2. Cache Next.js build cache (`.next/cache`) for faster builds
3. Cache testing artifacts and coverage reports
4. Use `actions/cache@v3` with appropriate cache keys
5. Implement cache restoration fallbacks for partial matches

## Resources

Consult `references/github-actions-best-practices.md` for workflow optimization patterns and security best practices.

Use `scripts/generate_ci_workflow.py` to scaffold workflow files based on detected project configuration.

Reference `assets/workflow-templates/` for starter templates for common frameworks (Next.js, React, Node.js).

## Implementation Steps

To implement complete CI/CD with GitHub Actions:

1. **Detect Project Configuration**
   - Identify framework (Next.js, Vite, CRA, etc.)
   - Detect package manager (npm, yarn, pnpm)
   - Find test runner (Jest, Vitest, Playwright)
   - Check for linting configuration

2. **Generate Workflow Files**
   - Use `scripts/generate_ci_workflow.py` with detected configuration
   - Customize jobs based on project requirements
   - Add matrix builds if testing multiple environments

3. **Configure Secrets and Variables**
   - Document required secrets in README or workflow comments
   - Set up environment-specific variables
   - Configure deployment credentials

4. **Add Preview Deployments**
   - Generate preview workflow with URL commenting
   - Configure preview environment provider
   - Set up cleanup automation

5. **Optimize Caching**
   - Implement multi-level caching strategy
   - Use cache keys based on lock files
   - Add cache restoration logic

6. **Test and Validate**
   - Push workflows to repository
   - Create test PR to verify preview deployments
   - Check workflow execution times and optimize

## Advanced Features

To add advanced CI/CD capabilities:

- **Parallel Jobs**: Split test suites across multiple jobs for faster execution
- **Conditional Deployments**: Deploy only specific paths or when conditions are met
- **Status Checks**: Require CI passing before merge
- **Deployment Gates**: Add manual approval steps for production deployments
- **Performance Monitoring**: Integrate Lighthouse CI or bundle analysis
- **Dependency Updates**: Automate dependency updates with Dependabot integration

## Framework-Specific Configuration

### Next.js Applications

To optimize for Next.js:

1. Cache `.next/cache` directory for faster builds
2. Set `NEXT_TELEMETRY_DISABLED=1` to disable telemetry
3. Use `next build` and `next export` for static exports
4. Configure ISR revalidation for preview deployments

### Full-Stack Applications

To handle full-stack deployments:

1. Set up separate jobs for frontend and backend
2. Configure database migrations in deployment workflow
3. Run integration tests against preview environment
4. Coordinate deployment order (backend first, then frontend)

## Deployment Providers

Consult `references/deployment-providers.md` for platform-specific configuration:

- **Vercel**: Use vercel-action with project configuration
- **Netlify**: Use netlify-cli with site ID and auth token
- **AWS**: Configure S3/CloudFront or ECS deployment
- **Docker**: Build and push container images to registry
- **Self-Hosted**: SSH deployment with rsync or git pull

## Monitoring and Notifications

To add monitoring and notifications:

1. Configure Slack/Discord webhooks for deployment notifications
2. Add GitHub status checks for required CI jobs
3. Set up error tracking integration (Sentry, etc.)
4. Monitor workflow execution times and optimize slow jobs
5. Track deployment frequency and failure rates

## Troubleshooting

Common issues and solutions:

- **Cache Misses**: Verify cache key includes all dependency files
- **Timeout Errors**: Increase timeout or split into parallel jobs
- **Permission Errors**: Check repository secrets and permissions
- **Build Failures**: Ensure environment variables are set correctly
- **Preview URL Not Commented**: Verify PR comment permissions and token scope
