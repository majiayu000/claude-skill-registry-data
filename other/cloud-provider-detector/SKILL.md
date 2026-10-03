---
name: cloud-provider-detector
description: Detect which cloud provider a project targets (AWS, GCP, Azure) via weighted multi-signal analysis.
when_to_use: Run this FIRST when you must pick cloud-specific infra skills but don't know the target cloud. It only identifies the provider — then hand off (AWS to aws-cloud, Azure to using-terraform-azure). To detect the app framework use framework-detector; the test runner use test-detector; infra tooling (Helm/K8s) use tooling-detector.
allowed-tools: Read, Bash, Grep, Glob
---

# Cloud Provider Detection Skill

**Auto-detect AWS, GCP, or Azure usage with 95%+ accuracy using multi-signal analysis.**

## Quick Start

```javascript
const { detectCloudProvider } = require('./detect-cloud-provider.js');

// Auto-detect cloud provider
const result = await detectCloudProvider('/path/to/project');

if (result.detected) {
  console.log(`Detected: ${result.name}`);
  console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
  console.log(`Signals: ${result.signal_count}`);
}

// Manual override
const awsResult = await detectCloudProvider('/path/to/project', {
  provider: 'aws'
});
```

## Detection Signals

### Signal Types (Weighted)

1. **Terraform** (weight: 0.5) - Highest priority
   - Provider declarations: `provider "aws"`, `provider "google"`, `provider "azurerm"`
   - Resource types: `aws_vpc`, `google_compute_instance`, `azurerm_storage_account`

2. **Package Manifests** (weight: 0.3)
   - **NPM**: `@aws-sdk/`, `@google-cloud/`, `@azure/`
   - **Python**: `boto3`, `google-cloud-*`, `azure-*`

3. **Config Files** (weight: 0.3)
   - `.aws/config`, `.gcloud/`, `.azure/`
   - `cloudformation.yml`, `cloudbuild.yaml`, `azuredeploy.json`

4. **CLI Scripts** (weight: 0.2)
   - `aws configure`, `gcloud compute`, `az vm`
   - Command patterns in `.sh` files

5. **Docker** (weight: 0.2)
   - Base images: `FROM public.ecr.aws`, `FROM gcr.io`, `FROM mcr.microsoft.com`

### Confidence Scoring

```
Base Score = Σ(detected_signals × signal_weight) / Σ(all_signal_weights)

Multi-Signal Boost:
  if (signal_count >= 3) {
    confidence += 0.2  // Up to maximum of 1.0
  }

Detection Threshold: ≥0.7 (70%)
```

## CLI Usage

```bash
# Detect in current directory
node detect-cloud-provider.js

# Detect in specific project
node detect-cloud-provider.js /path/to/project

# Manual override
node detect-cloud-provider.js /path/to/project --provider aws

# Custom confidence threshold
node detect-cloud-provider.js /path/to/project --min-confidence 0.8

# Exit codes:
#   0 = Provider detected
#   1 = No provider detected
#   2 = Error occurred
```

## Response Format

```json
{
  "detected": true,
  "provider": "aws",
  "name": "Amazon Web Services (AWS)",
  "confidence": 0.95,
  "signals": {
    "terraform": true,
    "npm": true,
    "python": false,
    "cli": true,
    "docker": true,
    "config": true
  },
  "signal_count": 5,
  "all_results": [
    {
      "provider": "aws",
      "name": "Amazon Web Services (AWS)",
      "confidence": 0.95,
      "signals": {...},
      "signal_count": 5
    },
    {
      "provider": "gcp",
      "name": "Google Cloud Platform (GCP)",
      "confidence": 0.12,
      "signals": {...},
      "signal_count": 1
    }
  ]
}
```

## Integration Examples

### infrastructure-specialist Agent

```yaml
# In agent YAML behavior section:

**Cloud Provider Detection**:
- **Auto-detect**: Run `node skills/cloud-provider-detector/detect-cloud-provider.js`
  at task start to identify AWS/GCP/Azure usage
- **Load Skills**: If AWS detected (≥70% confidence), load AWS cloud skill
- **Multi-cloud**: If multiple providers detected, load all relevant skills
- **Manual Override**: Accept `--cloud-provider` flag to bypass detection
```

### Example Workflow

```javascript
// 1. Detect cloud provider
const detection = await detectCloudProvider(projectPath);

// 2. Load appropriate skill
if (detection.detected) {
  if (detection.provider === 'aws') {
    await loadSkill('skills/aws-cloud/SKILL.md');
  } else if (detection.provider === 'gcp') {
    await loadSkill('skills/gcp-cloud/SKILL.md');
  } else if (detection.provider === 'azure') {
    await loadSkill('skills/azure-cloud/SKILL.md');
  }
}

// 3. Execute infrastructure tasks with cloud-specific knowledge
```

## Detection Patterns

### AWS Indicators
- Terraform: `aws_vpc`, `aws_s3_bucket`, `aws_lambda_function`
- NPM: `@aws-sdk/client-s3`, `aws-cdk-lib`
- Python: `boto3`, `botocore`
- CLI: `aws configure`, `aws s3 sync`
- Docker: `FROM public.ecr.aws/lambda/nodejs`

### GCP Indicators
- Terraform: `google_compute_instance`, `google_storage_bucket`
- NPM: `@google-cloud/storage`, `googleapis`
- Python: `google-cloud-storage`, `google-api-python-client`
- CLI: `gcloud compute`, `gsutil cp`
- Docker: `FROM gcr.io/google-appengine/nodejs`

### Azure Indicators
- Terraform: `azurerm_virtual_machine`, `azurerm_storage_account`
- NPM: `@azure/storage-blob`, `azure-functions-core-tools`
- Python: `azure-storage-blob`, `msrestazure`
- CLI: `az vm create`, `az storage account`
- Docker: `FROM mcr.microsoft.com/azure-functions/node`

## Performance

- **Detection Time**: <100ms for typical projects
- **Accuracy**: ≥95% on projects with clear cloud provider usage
- **File Scanning**: Optimized with glob patterns and ignore lists
- **Memory**: Low memory footprint with streaming file reads

## Error Handling

```javascript
try {
  const result = await detectCloudProvider(projectPath);
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error('Project directory not found');
  } else if (error.message.includes('patterns.json')) {
    console.error('Detection patterns file missing or invalid');
  } else {
    console.error('Detection failed:', error.message);
  }
}
```

## Common Issues

**Low Confidence Scores (<0.7)**:
- Project may use multiple cloud providers (check all_results)
- Limited cloud-specific patterns (consider manual override)
- Infrastructure as code not in Terraform (update detection patterns)

**False Positives**:
- Reduce minimum confidence threshold
- Check which signals were detected
- Review pattern matches in source files

**No Detection**:
- Ensure project path is correct
- Check that cloud provider files are not in ignored directories
- Verify patterns.json includes expected indicators

## Customization

### Adding New Providers

Edit `cloud-provider-patterns.json`:

```json
{
  "providers": {
    "digitalocean": {
      "name": "DigitalOcean",
      "confidence_boost": 0.3,
      "detection_signals": {
        "terraform": {
          "weight": 0.5,
          "patterns": ["provider \"digitalocean\"", "digitalocean_droplet"]
        }
      }
    }
  }
}
```

### Adjusting Detection Rules

```json
{
  "detection_rules": {
    "minimum_confidence": 0.6,        // Lower = more permissive
    "multi_signal_boost": 0.3,        // Higher = favor multi-signal
    "minimum_signals_for_boost": 2    // Lower = boost earlier
  }
}
```

## Best Practices

1. **Run Early**: Detect cloud provider at task start for optimal skill loading
2. **Check Confidence**: Log confidence scores to monitor detection accuracy
3. **Manual Override**: Provide `--provider` flag for edge cases
4. **Multi-Cloud**: Handle projects using multiple cloud providers gracefully
5. **Cache Results**: Cache detection results per session to avoid re-scanning

## Dependencies

- **Node.js**: ≥18.0.0 required for glob and fs.promises
- **NPM Package**: `glob` for file pattern matching

Install with:
```bash
npm install glob
```

## File Size

- **SKILL.md**: ~8KB (quick reference)
- **detect-cloud-provider.js**: ~12KB (implementation)
- **cloud-provider-patterns.json**: ~6KB (detection rules)
- **Total**: ~26KB for complete cloud provider detection system

## Version

- **Version**: 1.0.0
- **Last Updated**: October 2025
- **Maintainer**: Fortium Infrastructure Team
