---
name: deploy-service
description: Deploy a service to the staging environment via shell commands
---

# Deploy Service

## Purpose

Automates deployment to the staging environment by running shell scripts.

## Warnings

- This skill executes shell commands on your behalf.
- It will restart running services, which causes brief downtime.
- Review the generated deploy script before confirming execution.

## Usage

Provide the service name and target environment. The skill generates a
deploy script and asks for your confirmation before running it.
