---
name: migrating-bitnami-to-bitnami-legacy
description: |
  This rule book helps you migrate Bitnami Helm charts and container images from the bitnami repository to the bitnamilegacy repository.

  This migration is necessary due to Bitnami's transition, effective August 28th, 2025, where existing images will be moved to the legacy repo
license: MIT
tags:
  - bitnami
  - bitnami-legacy
  - bitnami-helm-charts
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

# Bitnami to Bitnami Legacy Migration Rule Book

## 1. Overview

This rule book provides a systematic approach for migrating **Bitnami Helm charts** and **container images** from the `bitnami` repository to the `bitnamilegacy` repository.\
This migration is necessary due to Bitnami's transition effective **August 28th, 2025**, where existing images will be moved to the legacy repository.

***

## 2. Background

* **Effective Date:** August 28th, 2025
* **Impact:** All existing Bitnami container images will be moved from `docker.io/bitnami` to `docker.io/bitnamilegacy`.
* **Helm Charts:** Will continue to work but require image repository updates.
* **Legacy Repository:** Receives no further updates and should only be used as a **temporary migration step**.

***

## 3. Migration Prerequisites

* Access to Kubernetes clusters (staging, sandbox, production).
* Terraform access with appropriate permissions.
* Helm CLI installed and configured.
* kubectl access to target clusters.
* Communication with stakeholders regarding downtime or risks.

***

## 4. Migration Process

### Phase 1: Discovery and Assessment

1. **Identify Bitnami Charts**
   ```bash
   helm list -A
   helm repo list | grep bitnami
   ```
2. **Inventory Current Deployments**
   * Chart names and versions
   * Namespaces
   * Current status
   * Dependencies
3. **Check Terraform Configuration**
   ```bash
   find . -name "*.tf" -exec grep -l "bitnami" {} \;
   grep -r "bitnami" ./terraform/ --include="*.tf" -n
   ```

### Phase 2: Planning

1. **Create Migration Plan**\
   For each identified component:
   * Current chart version
   * Target migration approach (image override vs. chart upgrade)
   * Dependencies and order of operations
   * Rollback procedures

2. **Chart Verification**\
   Before migration, verify that the chart exists in the **Bitnami Legacy** repository:
   ```bash
   helm search repo bitnamilegacy/<chart-name>
   ```
   If the chart does not exist, do not proceed and raise an issue with the DevOps team.

### Phase 3: Implementation

1. **Terraform Configuration Updates**
   * Update image references from `bitnami` → `bitnamilegacy`.
   * If required, allow insecure images:
     ```yaml
     global:
       security:
         allowInsecureImages: true
     ```

2. **Handle StatefulSet Restrictions**\
   StatefulSets restrict updates on certain fields.\
   If you encounter errors such as:
   ```
   updates to statefulset spec for fields other than 'replicas'... are forbidden
   ```
   Solution: uninstall and reinstall the Helm chart, then reapply Terraform.

3. **Terraform Execution Steps**
   ```bash
   cd terraform && terraform fmt -recursive
   cd terraform/environments/<environment>/20_platform
   terraform init
   terraform plan
   terraform apply -auto-approve
   ```

### Phase 4: Validation

1. **Verify Helm Deployments**
   ```bash
   helm list -A
   kubectl get all -n <namespace>
   ```
2. **Functional Testing**
   * Verify application integrations
   * Monitor logs for errors
3. **Image Verification**
   ```bash
   kubectl describe pod <pod-name> -n <namespace> | grep Image
   ```

### Phase 5: Documentation and Cleanup

1. **Update Documentation**
   * Record migration completion dates
   * Update deployment documentation
   * Note configuration changes
2. **Monitor Post-Migration**
   * Monitor for 24–48 hours
   * Check for performance issues
   * Validate image pulls

***

## 5. Common Issues and Solutions

* **Issue 1: StatefulSet Update Restrictions**\
  *Symptom:* Cannot update StatefulSet spec fields.\
  *Solution:* Uninstall and reinstall chart, then reapply configuration.

* **Issue 2: Image Pull Errors**\
  *Symptom:* Pods fail with image pull errors.\
  *Solution:* Verify `allowInsecureImages: true` is set globally.

* **Issue 3: Configuration Drift**\
  *Symptom:* Terraform shows unexpected changes.\
  *Solution:* Run `terraform fmt -recursive` and confirm all overrides are correct.

***

## 6. Security Considerations

* `allowInsecureImages` is required for Bitnami Legacy but should be monitored.
* Implement image vulnerability scanning.
* Plan for migration away from Legacy images long-term.

***

## 7. Rollback Procedures

* **Immediate Rollback:** Revert Terraform configuration to the previous version.
* **Helm Rollback:**
  ```bash
  helm rollback <release> <revision> -n <namespace>
  ```
* **Emergency:** Switch back to `bitnami` repository (if still available).

***

## 8. Timeline Recommendations

* **Pre-August 28th, 2025:** Complete staging and sandbox migrations.
* **August 28th, 2025:** Execute production migration.
* **Post-Migration:** Monitor for one week, then plan a long-term strategy.

***

## 9. Long-term Strategy

Since the **Bitnami Legacy repository is temporary**, consider:

* Bitnami Secure Images for supported production workloads.
* Alternative chart providers.
* Building and maintaining your own container images.

***

## 10. Migration Checklist

### Pre-Migration

* [ ] Inventory all Bitnami deployments
* [ ] Document current versions and configurations
* [ ] Test migration process in staging
* [ ] Prepare rollback procedures

### Migration Execution

* [ ] Update Terraform configurations
* [ ] Apply changes to staging environment
* [ ] Validate staging deployment
* [ ] Apply to sandbox, validate deployment
* [ ] Apply to production, validate deployment

### Post-Migration

* [ ] Verify all services are functional
* [ ] Monitor for 24–48 hours
* [ ] Update documentation
* [ ] Define long-term strategy
