---
name: Redc-useage
description: Multi-cloud red team infrastructure automation. Deploy and manage cloud resources across AWS, Aliyun, Tencent Cloud with Terraform. Includes commands for init, deploy, manage, execute, and cleanup of infrastructure cases.
---

# Redc Skills - AI Operations Guide

Multi-cloud red team infrastructure automation tool built on Terraform.

## Quick Reference

**Config:** `~/redc/config.yaml` | **Templates:** `~/redc/redc-templates/` | **Docs:** https://github.com/wgpsec/redc

## Configuration

```yaml
providers:
  aws:
    AWS_ACCESS_KEY_ID: "KEY"
    AWS_SECRET_ACCESS_KEY: "SECRET"
    region: "us-east-1"
  aliyun:
    ALICLOUD_ACCESS_KEY: "KEY"
    ALICLOUD_SECRET_KEY: "SECRET"
    region: "cn-hangzhou"
  tencentcloud:
    TENCENTCLOUD_SECRET_ID: "ID"
    TENCENTCLOUD_SECRET_KEY: "KEY"
    region: "ap-guangzhou"
```

**Env vars:** Set `AWS_ACCESS_KEY_ID`, `ALICLOUD_ACCESS_KEY`, `TENCENTCLOUD_SECRET_ID`, etc. if config.yaml unavailable.

## Global Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--config` | `~/redc/config.yaml` | Config file path |
| `-u, --user` | `system` | User identifier |
| `--project` | `default` | Project name |
| `--debug` | `false` | Debug mode |

## Commands

### Setup
```bash
redc init                           # Initialize templates
redc pull <image>                   # Download template (e.g., aliyun/ecs)
redc image ls                       # List local templates
```

### Deploy
```bash
redc run <template> -n <name> -e key=val    # Plan & start (create infrastructure)
redc plan <template> -n <name>              # Plan only (preview without creating)
redc start <case-id>                        # Start case (create infrastructure)
```

### Manage
```bash
redc ps                             # List all cases
redc status <case-id>               # Check status
redc stop <case-id>                 # Stop infrastructure
redc kill <case-id>                 # Stop & remove
redc rm <case-id>                   # Remove case
```

### Execute
```bash
redc exec <case-id> <command>       # Run command
redc exec -t <case-id> bash         # Interactive shell
redc cp <src> <case-id>:<dest>      # Upload file
redc cp <case-id>:<src> <dest>      # Download file
```

## Workflows

**Quick Deploy:**
```bash
redc pull aliyun/ecs && redc init
redc run aliyun/ecs -n myserver -e password=Pass123
# Returns case-id (e.g., 8a57078ee856)
redc exec 8a57078ee856 whoami
```

**Controlled:**
```bash
redc plan aws/ec2 -n staging
# Review the planned resources, then:
redc start <case-id>
redc cp deploy.sh <case-id>:/root/
redc exec <case-id> "bash /root/deploy.sh"
```

**Cleanup:**
```bash
redc stop <case-id> && redc rm <case-id>
# Or: redc kill <case-id>
```

## Automation

```python
import subprocess, re

def redc_run(template, name, env=None):
    cmd = ["redc", "run", template, "-n", name]
    if env:
        for k, v in env.items():
            cmd.extend(["-e", f"{k}={v}"])
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    match = re.search(r'[a-f0-9]{12,64}', result.stdout)
    return match.group(0) if match else None

# Usage
case_id = redc_run("aliyun/ecs", "auto_deploy", {"password": "Secure123"})
```

## Output Patterns

- **Success:** `✅` in output
- **Error:** `❌` in output
- **Case ID:** `[a-f0-9]{64}` (use first 12 chars)
- **Status:** `running`, `stopped`, `created`, `error`

## Error Handling

| Error | Solution |
|-------|----------|
| Config not found | Create `~/redc/config.yaml` |
| Template not found | Run `redc pull <template>` |
| Case ID not found | Check `redc ps` |
| SSH timeout | Verify instance running, security groups |
| Init failed | Check network, configure Terraform mirror |

## JSON Schemas

**Case:**
```json
{
  "id": "string[64]",
  "name": "string",
  "template": "string",
  "status": "running|stopped|created|error",
  "outputs": {"public_ip": "string"}
}
```

**Config:**
```json
{
  "providers": {
    "aws": {"AWS_ACCESS_KEY_ID": "string", "region": "string"}
  }
}
```

## Best Practices

- Use short IDs (first 12 chars)
- Assign meaningful names: `<project>_<purpose>_<env>`
- Always cleanup: `redc stop` → `redc rm`
- Use `--debug` for troubleshooting
- Never commit config.yaml to version control
- Monitor costs with `redc ps`

## Resources

- Repo: https://github.com/wgpsec/redc
- Templates: https://github.com/wgpsec/redc-template
- Online: https://redc.wgpsec.org/