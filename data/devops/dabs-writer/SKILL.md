---
name: dabs-writer
description: "Create and configure Databricks Asset Bundles (DABs) with best practices for multi-environment deployments. Use when working with: (1) Creating new DAB projects, (2) Adding resources (dashboards, pipelines, jobs, alerts), (3) Configuring multi-environment deployments, (4) Setting up permissions, (5) Deploying or running bundle resources"
---

# Databricks Asset Bundle (DABs) Writer

## Overview
Create DABs for multi-environment deployment (dev/staging/prod).

## Reference Files

- **[SDP_guidance.md](SDP_guidance.md)** - Spark Declarative Pipeline configurations
- **[alerts_guidance.md](alerts_guidance.md)** - SQL Alert schemas (critical - API differs)

## Bundle Structure

```
project/
├── databricks.yml           # Main config + targets
├── resources/*.yml          # Resource definitions
└── src/                     # Code/dashboard files
```

### Main Configuration (databricks.yml)

```yaml
bundle:
  name: project-name

include:
  - resources/*.yml

variables:
  catalog:
    default: "default_catalog"
  schema:
    default: "default_schema"
  warehouse_id:
    lookup:
      warehouse: "Shared SQL Warehouse"

targets:
  dev:
    default: true
    mode: development
    workspace:
      profile: dev-profile
    variables:
      catalog: "dev_catalog"
      schema: "dev_schema"

  prod:
    mode: production
    workspace:
      profile: prod-profile
    variables:
      catalog: "prod_catalog"
      schema: "prod_schema"
```

### Dashboard Resources

```yaml
resources:
  dashboards:
    dashboard_name:
      display_name: "[${bundle.target}] Dashboard Title"
      file_path: ../src/dashboards/dashboard.lvdash.json  # Relative to resources/
      warehouse_id: ${var.warehouse_id}
      permissions:
        - level: CAN_RUN
          group_name: "users"
```

**Permission levels**: `CAN_READ`, `CAN_RUN`, `CAN_EDIT`, `CAN_MANAGE`

### Pipelines

**See [SDP_guidance.md](SDP_guidance.md)** for pipeline configuration

### SQL Alerts

**See [alerts_guidance.md](alerts_guidance.md)** - Alert schema differs significantly from other resources

### Jobs Resources

```yaml
resources:
  jobs:
    job_name:
      name: "[${bundle.target}] Job Name"
      tasks:
        - task_key: "main_task"
          notebook_task:
            notebook_path: ../src/notebooks/main.py  # Relative to resources/
          new_cluster:
            spark_version: "13.3.x-scala2.12"
            node_type_id: "i3.xlarge"
            num_workers: 2
      schedule:
        quartz_cron_expression: "0 0 9 * * ?"
        timezone_id: "America/Los_Angeles"
      permissions:
        - level: CAN_VIEW
          group_name: "users"
```

**Permission levels**: `CAN_VIEW`, `CAN_MANAGE_RUN`, `CAN_MANAGE`

⚠️ **Cannot modify "admins" group permissions** on jobs - verify custom groups exist before use

### Path Resolution

⚠️ **Critical**: Paths depend on file location:

| File Location | Path Format | Example |
|--------------|-------------|---------|
| `resources/*.yml` | `../src/...` | `../src/dashboards/file.json` |
| `databricks.yml` targets | `./src/...` | `./src/dashboards/file.json` |

**Why**: `resources/` files are one level deep, so use `../` to reach bundle root. `databricks.yml` is at root, so use `./`

### Volume Resources

```yaml
resources:
  volumes:
    my_volume:
      catalog_name: ${var.catalog}
      schema_name: ${var.schema}
      name: "volume_name"
      volume_type: "MANAGED"
```

⚠️ **Volumes use `grants` not `permissions`** - different format from other resources

### Other Resources

DABs supports schemas, models, experiments, clusters, warehouses, apps, etc. Use `databricks bundle schema` to inspect schemas.

**Reference**: [DABs Resource Types](https://docs.databricks.com/dev-tools/bundles/resources)

## Common Commands

### Validation
```bash
databricks bundle validate                    # Validate default target
databricks bundle validate -t prod           # Validate specific target
```

### Deployment
```bash
databricks bundle deploy                      # Deploy to default target
databricks bundle deploy -t prod             # Deploy to specific target
databricks bundle deploy --auto-approve      # Skip confirmation prompts
databricks bundle deploy --force             # Force overwrite remote changes
```

### Running Resources
```bash
databricks bundle run resource_name          # Run a pipeline or job
databricks bundle run pipeline_name -t prod  # Run in specific environment
```

### Cleanup
```bash
databricks bundle destroy -t dev
databricks bundle destroy -t prod --auto-approve
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| **Wrong permission level** | Dashboards: CAN_READ/RUN/EDIT/MANAGE; Jobs: CAN_VIEW/MANAGE_RUN/MANAGE |
| **Path resolution fails** | Use `../src/` in resources/*.yml, `./src/` in databricks.yml |
| **Catalog doesn't exist** | Create catalog first or update variable |
| **"admins" group error on jobs** | Cannot modify admins permissions on jobs |
| **Volume permissions** | Use `grants` not `permissions` for volumes |
| **Hardcoded catalog in dashboard** | Create environment-specific files or parameterize JSON |

## Key Principles

1. **Path resolution**: `../src/` in resources/*.yml, `./src/` in databricks.yml
2. **Variables**: Parameterize catalog, schema, warehouse
3. **Mode**: `development` for dev/staging, `production` for prod
4. **Groups**: Use `"users"` for all workspace users
5. **Job permissions**: Verify custom groups exist; can't modify "admins"

## Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/)
- [Bundle Resources Reference](https://docs.databricks.com/dev-tools/bundles/resources)
- [Bundle Configuration Reference](https://docs.databricks.com/dev-tools/bundles/settings)
- [Supported Resource Types](https://docs.databricks.com/aws/en/dev-tools/bundles/resources#resource-types)
- [Examples Repository 1](https://github.com/databricks-solutions/databricks-dab-examples)
- [Example Repository 2](https://github.com/databricks/bundle-examples)