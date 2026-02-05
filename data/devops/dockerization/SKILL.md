---
name: dockerization
description: |
  Official Stakpak application containerization standard operating procedure, a step-by-step guidline to properly dockerize applications. This is a rule book curated by the Stakpak Team.
license: MIT
tags:
  - dockerization
  - containerization
  - docker
  - compose
  - cloud-native
  - container
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

# Application Dockerization RuleBook

## Core Principles

* **Analysis First**: Thoroughly examine application before starting work
* **User Collaboration**: Involve users in decisions, avoid assumptions, confirm critical choices
* **Documentation**: Record all configurations, generated values, and requirements
* **Efficiency**: Use available tools and information before requesting input
* **Error Analysis**: Identify root causes before retrying failed operations

## Mandatory 9-Phase Workflow

### 1. Application Analysis

* Examine directory structure and key files
* Identify programming language, framework, and dependencies
* Document external services (databases, cache, message queues)
* Create file/purpose mapping table
* Accumulate findings progressively

### 2. Base Image Selection

* Prefer official Docker Hub images
* Choose Alpine/slim variants for smaller size
* Consider security update frequency
* Create comparison table with pros/cons
* Document selection rationale

### 3. Dockerfile Creation

* Use multi-stage builds when applicable
* Configure non-root user for security
* Optimize layer caching and minimize size
* Implement health checks
* Address security concerns explicitly

### 4. Docker Compose Configuration

* Include application and dependent services
* Configure networks and volumes properly
* Set environment variables and secrets
* Omit obsolete 'version' attribute
* Enable service dependencies and restart policies

### 5. Build Process

* Use `docker compose build` (preferred method)
* Tag images with human-readable names
* Implement comprehensive .dockerignore file
* Document build commands and process
* Handle build errors systematically

### 6. Container Execution

* Start with `docker compose up -d`
* Verify all services start successfully
* Apply database migrations if required
* Check container status and logs
* Ensure port mappings work correctly

### 7. Health Verification

* Check container status and logs
* Test application endpoints (expect 200 status)
* Verify dependent service connectivity
* Monitor resource usage
* Consider network accessibility (avoid localhost assumptions)

### 8. Resource Cleanup

* Stop containers with `docker compose down`
* Remove unnecessary volumes and images
* Clean build cache and temporary files
* Document cleanup procedures
* Verify complete resource removal

### 9. Documentation

* List all required environment variables
* Identify secrets and sensitive configurations
* Document deployment and migration steps
* Provide troubleshooting guidance
* Create final summary report

## Security Requirements

* **Never run as root user**
* Use specific image tags (avoid 'latest')
* Implement proper .dockerignore
* Store secrets securely (not in image layers)
* Scan for vulnerabilities regularly
* Set resource limits appropriately
* Use minimal base images

## Error Handling Guidelines

* **Build Failures**: Analyze error messages, check Dockerfile syntax, verify base image availability
* **Runtime Failures**: Check logs immediately, verify environment variables, test dependencies
* **Performance Issues**: Monitor resources, check for leaks, optimize layers
* Never repeat failed commands more than twice without changing approach

## Tool Usage (For Agents)

* State objectives before each tool call
* Use `generate_code` for Dockerfile creation when available
* Leverage persistent scratchpad for state management
* Invoke multiple independent operations simultaneously
* Provide regular progress updates via todo lists

## Best Practices Summary

**DO:**

* Use official base images and specific tags
* Implement health checks and resource limits
* Document thoroughly and test systematically
* Cache dependencies effectively
* Monitor container health continuously

**DON'T:**

* Run containers as root
* Store secrets in Dockerfiles
* Use 'latest' tags in production
* Skip security scanning
* Ignore error root causes

## Success Criteria Checklist

* [ ] Container builds successfully
* [ ] Application runs without errors
* [ ] All health checks pass
* [ ] Dependencies properly configured
* [ ] Environment variables documented
* [ ] Security measures implemented
* [ ] Resources cleaned up
* [ ] Complete documentation provided
* [ ] Build images for the deployment target architecture (most likely amd64, unless the deployment target is arm-based) 

## Critical Workflow Rules

1. **Analysis before action** - understand the application first
2. **User involvement** - confirm decisions and tradeoffs
3. **Progressive documentation** - record findings at each step
4. **Error analysis** - identify causes before retry attempts
5. **Security by design** - implement security measures throughout
6. **Health verification** - test thoroughly before completion
7. **Clean completion** - remove unnecessary resources and document fully

***

*Adapt based on specific application requirements and organizational policies. Always prioritize security and maintainability.*
