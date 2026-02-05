---
name: vagrant-config-generator
description: Generate Vagrant configuration files for local development environments. Triggers on "create vagrantfile", "generate vagrant config", "vagrant setup", "local vm config".
---

# Vagrant Config Generator

Generate Vagrant configuration files for reproducible development environments.

## Output Requirements

**File Output:** `Vagrantfile`
**Format:** Valid Ruby Vagrantfile
**Standards:** Vagrant 2.x

## When Invoked

Immediately generate a complete Vagrantfile for the development environment.

## Example Invocations

**Prompt:** "Create Vagrantfile for Node.js development"
**Output:** Complete `Vagrantfile` with Ubuntu, Node.js, and port forwarding.
