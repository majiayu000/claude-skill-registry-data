---
name: ci-cd-helper
description: Generate CI/CD configurations and automation scripts for building, testing, and deploying
type: skill
language: bash
---

# CI/CD Helper

Generate continuous integration and deployment configurations.

## Capabilities
- Generate GitHub Actions workflows
- Create Fastlane configurations
- Build automation scripts
- Test automation
- Archive and export scripts
- TestFlight upload automation
- Release note generation
- Version bumping scripts

## Tools
- `generate_github_workflow.sh` - Create GitHub Actions YAML
- `setup_fastlane.sh` - Initialize Fastlane
- `build_script.sh` - Automated build script
- `test_script.sh` - Automated test runner

## Templates Included
- macOS app build workflow
- Test and coverage workflow
- Release workflow
- Dependency caching
- Artifact upload

## Usage
```bash
# Generate GitHub Actions
./generate_github_workflow.sh --platform macos --tests

# Setup Fastlane
./setup_fastlane.sh --appname PaleoRose
```
