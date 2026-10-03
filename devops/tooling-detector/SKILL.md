---
name: tooling-detector
description: Detect infrastructure/DevOps tooling in a project (Helm, Kubernetes, Kustomize, ArgoCD) via multi-signal analysis.
when_to_use: Run this FIRST when you need to pick infra-tooling skills but don't know what the repo uses. It only identifies tooling — then hand off (Helm charts to helm, raw manifests to kubernetes). To detect the cloud provider use cloud-provider-detector; the app framework use framework-detector; the test runner use test-detector.
allowed-tools: Read, Bash, Grep, Glob
---

# Tooling Detection System

**Version**: 1.0.0 | **Purpose**: Automatic detection of infrastructure tooling (Helm, Kubernetes, Kustomize, ArgoCD)

---

## Overview

The tooling detection system automatically identifies infrastructure and DevOps tooling usage in projects using multi-signal analysis. It detects Helm charts, Kubernetes manifests, Kustomize configurations, and GitOps tools with 95%+ accuracy.

**Supported Tools**:
- **Helm**: Kubernetes package manager
- **Kubernetes**: Container orchestration platform
- **Kustomize**: Kubernetes configuration customization
- **ArgoCD**: GitOps continuous delivery

**Use Cases**:
- **Auto-load skills**: Automatically load Helm/Kubernetes skills when detected
- **Project analysis**: Identify tooling stack in existing projects
- **CI/CD integration**: Dynamic skill loading based on detected tooling

---

## Quick Start

### Detect All Tools

```bash
node skills/tooling-detector/detect-tooling.js /path/to/project
```

**Output**:
```json
{
  "detected": true,
  "tools": [
    {
      "tool": "helm",
      "name": "Helm",
      "confidence": 0.9,
      "signals": {
        "chart_yaml": true,
        "values_yaml": true,
        "templates_dir": true
      },
      "signal_count": 3
    },
    {
      "tool": "kubernetes",
      "name": "Kubernetes",
      "confidence": 0.85,
      "signals": {
        "api_version": true,
        "kind_field": true,
        "manifests_dir": true
      },
      "signal_count": 3
    }
  ]
}
```

### Detect Specific Tool

```bash
# Detect Helm
node skills/tooling-detector/detect-tooling.js /path/to/project --tool helm

# Detect Kubernetes
node skills/tooling-detector/detect-tooling.js /path/to/project --tool kubernetes
```

### Custom Confidence Threshold

```bash
node skills/tooling-detector/detect-tooling.js /path/to/project --min-confidence 0.8
```

---

## Detection Signals

### Helm Detection

**Primary Signals** (High Confidence):
- `Chart.yaml` file (weight: 0.6) - Helm chart metadata
- `values.yaml` file (weight: 0.3) - Default values
- `templates/` directory (weight: 0.2) - Template manifests

**Secondary Signals** (Medium Confidence):
- Helm CLI commands in scripts (weight: 0.2)
  - `helm install`, `helm upgrade`, `helm rollback`
  - `helm template`, `helm lint`, `helm package`
- Configuration files (weight: 0.1)
  - `.helmignore`, `requirements.yaml`, `Chart.lock`

**Confidence Threshold**: ≥70% for automatic detection

**Example Detection**:
```
Chart.yaml: ✅ (0.6)
values.yaml: ✅ (0.3)
templates/: ✅ (0.2)
helm CLI: ✅ (0.2)
→ Confidence: 1.0 + 0.1 boost = 100%
```

---

### Kubernetes Detection

**Primary Signals** (High Confidence):
- `apiVersion: v1|apps/v1|batch/v1` in YAML files (weight: 0.5)
- `kind: Deployment|Service|Pod|...` in YAML files (weight: 0.4)
- `kustomization.yaml` file (weight: 0.3)

**Secondary Signals** (Medium Confidence):
- kubectl CLI commands in scripts (weight: 0.2)
  - `kubectl apply`, `kubectl get`, `kubectl describe`
- Configuration files (weight: 0.2)
  - `.kube/config`, `kubeconfig`
- Manifest directories (weight: 0.1)
  - `k8s/`, `kubernetes/`, `manifests/`

**Confidence Threshold**: ≥70% for automatic detection

**Example Detection**:
```
apiVersion fields: ✅ (0.5)
kind fields: ✅ (0.4)
kubectl CLI: ✅ (0.2)
manifests/ dir: ✅ (0.1)
→ Confidence: 1.0 + 0.1 boost = 100%
```

---

## Usage Patterns

### Integration with infrastructure-developer

**Auto-detect and load skills**:
```bash
#!/bin/bash

# Detect tooling
TOOLING=$(node skills/tooling-detector/detect-tooling.js .)

# Parse results
HELM_DETECTED=$(echo $TOOLING | jq -r '.tools[] | select(.tool=="helm") | .tool')
K8S_DETECTED=$(echo $TOOLING | jq -r '.tools[] | select(.tool=="kubernetes") | .tool')

# Load Helm skill if detected
if [ "$HELM_DETECTED" = "helm" ]; then
  echo "📦 Helm detected - loading Helm skill..."
  cat skills/helm/SKILL.md
fi

# Load Kubernetes skill if detected
if [ "$K8S_DETECTED" = "kubernetes" ]; then
  echo "☸️  Kubernetes detected - loading Kubernetes skill..."
  cat skills/kubernetes/SKILL.md
fi
```

### Programmatic Usage (Node.js)

```javascript
const { detectTooling, detectTool } = require('./skills/tooling-detector/detect-tooling.js');

// Detect all tools
async function analyzeProject(projectPath) {
  const result = await detectTooling(projectPath);

  if (result.detected) {
    console.log(`Detected ${result.tools.length} tools:`);
    for (const tool of result.tools) {
      console.log(`  - ${tool.name}: ${(tool.confidence * 100).toFixed(0)}%`);
    }
  }
}

// Detect specific tool
async function checkHelm(projectPath) {
  const result = await detectTool(projectPath, 'helm');

  if (result.detected) {
    console.log(`Helm detected with ${(result.confidence * 100).toFixed(0)}% confidence`);
    console.log('Signals:', result.signals);
  }
}
```

---

## Detection Algorithm

### Multi-Signal Analysis

1. **File Existence**: Check for tool-specific files
   - Helm: `Chart.yaml`, `values.yaml`
   - Kubernetes: `kustomization.yaml`

2. **Directory Existence**: Check for tool-specific directories
   - Helm: `templates/`
   - Kubernetes: `k8s/`, `kubernetes/`, `manifests/`

3. **Pattern Matching**: Search file contents for patterns
   - Helm: CLI commands in shell scripts
   - Kubernetes: `apiVersion` and `kind` fields in YAML files

4. **Confidence Calculation**:
   ```
   confidence = (weighted_signal_sum / total_weight)

   if (signal_count >= 3) {
     confidence += multi_signal_boost  // +10-20%
   }

   confidence = min(1.0, confidence)
   ```

5. **Threshold Check**: Return detected if confidence ≥70%

### Performance Targets

- **Detection Time**: <100ms average
- **Accuracy**: ≥95% for Helm and Kubernetes
- **False Positives**: <5%
- **Multi-Tool Support**: Detect multiple tools simultaneously

---

## Configuration

### Custom Patterns

Modify `tooling-patterns.json` to customize detection:

```json
{
  "tools": {
    "helm": {
      "detection_signals": {
        "chart_yaml": {
          "weight": 0.6,
          "files": ["Chart.yaml"]
        }
      }
    }
  },
  "detection_rules": {
    "minimum_confidence": 0.7,
    "multi_signal_boost": 0.1,
    "minimum_signals_for_boost": 3
  }
}
```

### Manual Override

Skip detection and manually specify tools:

```bash
# Force Helm detection
--tools helm

# Force multiple tools
--tools helm,kubernetes

# Adjust confidence threshold
--min-confidence 0.8
```

---

## CLI Reference

### Commands

```bash
# Detect all tools
node detect-tooling.js [project-path]

# Detect specific tool
node detect-tooling.js [project-path] --tool <tool-name>

# Filter tools
node detect-tooling.js [project-path] --tools helm,kubernetes

# Custom confidence threshold
node detect-tooling.js [project-path] --min-confidence 0.8
```

### Exit Codes

- `0`: Tools detected successfully
- `1`: No tools detected
- `2`: Error during detection

---

## Troubleshooting

### No Tools Detected

```bash
# Run with all results
node detect-tooling.js . | jq '.all_results'

# Check confidence scores
node detect-tooling.js . --min-confidence 0.5

# Verify file patterns
ls Chart.yaml values.yaml templates/
```

### False Positives

Adjust confidence threshold:
```bash
node detect-tooling.js . --min-confidence 0.8
```

### Performance Issues

Check project size:
```bash
# Exclude large directories
echo "node_modules/" >> .gitignore
echo "vendor/" >> .gitignore
```

---

## Examples

### Helm Chart Project

**Project Structure**:
```
my-chart/
├── Chart.yaml        # ✅ Detected
├── values.yaml       # ✅ Detected
├── templates/        # ✅ Detected
│   ├── deployment.yaml
│   └── service.yaml
└── .helmignore       # ✅ Detected
```

**Detection Result**:
```json
{
  "detected": true,
  "tools": [
    {
      "tool": "helm",
      "confidence": 1.0,
      "signals": {
        "chart_yaml": true,
        "values_yaml": true,
        "templates_dir": true,
        "config": true
      },
      "signal_count": 4
    }
  ]
}
```

### Kubernetes Manifests Project

**Project Structure**:
```
k8s/
├── deployment.yaml   # ✅ apiVersion, kind detected
├── service.yaml      # ✅ apiVersion, kind detected
├── ingress.yaml      # ✅ apiVersion, kind detected
└── kustomization.yaml # ✅ Detected
```

**Detection Result**:
```json
{
  "detected": true,
  "tools": [
    {
      "tool": "kubernetes",
      "confidence": 0.95,
      "signals": {
        "api_version": true,
        "kind_field": true,
        "kustomization": true,
        "manifests_dir": true
      },
      "signal_count": 4
    }
  ]
}
```

### Combined Helm + Kubernetes

**Project Structure**:
```
my-app/
├── Chart.yaml        # Helm
├── values.yaml       # Helm
├── templates/        # Helm
│   └── *.yaml        # Kubernetes manifests
└── kustomize/        # Kubernetes + Kustomize
    └── kustomization.yaml
```

**Detection Result**:
```json
{
  "detected": true,
  "tools": [
    {
      "tool": "helm",
      "confidence": 1.0
    },
    {
      "tool": "kubernetes",
      "confidence": 0.9
    },
    {
      "tool": "kustomize",
      "confidence": 0.8
    }
  ]
}
```

---

## API Reference

### `detectTooling(projectPath, options)`

Detect all infrastructure tooling in project.

**Parameters**:
- `projectPath` (string): Root project directory
- `options` (object):
  - `tools` (string[]): Specific tools to detect
  - `minimumConfidence` (number): Minimum confidence threshold (default: 0.7)

**Returns**: Promise<Object>
```javascript
{
  detected: boolean,
  tools: Array<{
    tool: string,
    name: string,
    confidence: number,
    signals: Object,
    signal_count: number
  }>,
  all_results: Array,
  detection_summary: {
    total_analyzed: number,
    detected_count: number,
    minimum_confidence: number
  }
}
```

### `detectTool(projectPath, toolName, options)`

Detect specific tool (Helm or Kubernetes).

**Parameters**:
- `projectPath` (string): Root project directory
- `toolName` (string): Tool name (helm|kubernetes|kustomize|argocd)
- `options` (object): Same as `detectTooling()`

**Returns**: Promise<Object>
```javascript
{
  detected: boolean,
  tool: string,
  name: string,
  confidence: number,
  signals: Object,
  signal_count: number
}
```

---

## Version History

**1.0.0** (2025-10-23):
- Initial release
- Helm detection (Chart.yaml, values.yaml, templates/)
- Kubernetes detection (apiVersion, kind, kustomization.yaml)
- Kustomize detection
- ArgoCD detection
- Multi-signal analysis with confidence scoring
- Performance target: <100ms detection

---

**Last Updated**: 2025-10-23 | **Version**: 1.0.0
