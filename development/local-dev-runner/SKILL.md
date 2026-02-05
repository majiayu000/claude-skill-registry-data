---
name: Local Dev Runner
description: Provide local debugging scripts for Docker including build, run, and environment setup for development workflow.
---

# Local Dev Runner

## Instructions

1. Generate local development scripts:
   - Create build.sh for building Docker images
   - Create run.sh for running containers locally
   - Generate .env.example with required variables
   - Include compose files if multi-service needed

2. Implement build script functionality:
   - Build Docker image with proper tagging
   - Handle dependency installation
   - Include caching for faster builds
   - Add error handling for build failures

3. Create run script with development features:
   - Run container with proper port mapping
   - Mount volumes for live code updates
   - Include environment variable loading
   - Add cleanup and stop functionality

4. Configure development environment:
   - Generate .env.example with all required variables
   - Include default values where appropriate
   - Add validation for required variables
   - Document development-specific settings

5. Follow Context7 MCP standards:
   - Support local development workflow
   - Follow deterministic script patterns
   - Include proper error handling
   - Document all script options and parameters

## Examples

Input: "Create local development runner scripts"
Output: Creates build.sh, run.sh, and .env.example for local development workflow.