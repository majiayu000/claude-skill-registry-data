---
name: helm
description: Charts (Chart.yaml, values.yaml, templates), helm install/upgrade, values inheritance, hooks, dependencies, testing, repos.
---

## helm

Package and deploy Kubernetes applications with Helm.

### Chart structure
- Chart.yaml: metadata, version, dependencies
- values.yaml: default configuration values
- templates/: Go templates for K8s manifests
- NOTES.txt: post-install usage instructions

### Commands
- helm create, lint, package, install, upgrade
- helm rollback, uninstall, list, history
- helm repo add, update, search
- helm get values, get manifest

### Values and templates
- Values inheritance: --values, --set, --set-string
- Sprig template functions
- Control flow: range, if, with, define
- Named templates with template and include

### Advanced
- Hooks: pre/post install, upgrade, delete
- Chart dependencies and subcharts
- Chart testing with helm test
- OCI-based registry storage
