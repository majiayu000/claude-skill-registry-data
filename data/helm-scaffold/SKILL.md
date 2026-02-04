---
name: helm-scaffold
description: Generate production-ready Helm charts for Kubernetes applications. Use when users need to create new Helm charts, convert Kubernetes manifests to Helm templates, scaffold charts for Deployments/StatefulSets/Jobs/CronJobs, create multi-environment configurations, or standardize organizational chart templates with CNCF/Helm best practices. Uses Python scaffolding script and template assets for automated generation.
---

# Helm Scaffold

Automate production-ready Helm chart generation using template assets, Python scaffolding scripts, and Kubernetes best practices through conversational interaction.

## Core Capabilities

- **Automated scaffolding** using Python script (`scripts/scaffold_chart.py`)
- **Template-based generation** from `assets/templates/` directory
- **Convert Kubernetes manifests** to Helm templates
- **Multi-environment configurations** (dev, staging, prod)
- **Organizational standardization** with team policies
- **Comprehensive testing** with dry-run workflows

## Quick Start

For simple chart generation, use the Python scaffolding script directly:

```bash
python3 scripts/scaffold_chart.py <chart-name> \
  --workload-type deployment \
  --output /mnt/user-data/outputs \
  --ingress \
  --hpa
```

## Workflow Decision Tree

```
User Request
├─ Simple chart (name + type provided)
│  └─ Use scaffold_chart.py directly
├─ Complex chart (many options)
│  └─ Ask clarifying questions, then use scaffold_chart.py
├─ Manifest conversion
│  └─ Manual templatization process
└─ Custom requirements
   └─ Manual generation with template references
```

## Interactive Workflow

### Step 1: Understand Use Case

Identify the scenario:
- **Simple new chart**: Use `scaffold_chart.py` with user-provided params
- **Complex chart**: Ask questions, build command
- **Manifest conversion**: Extract variables, templatize
- **Team template**: Apply organizational standards

### Step 2: Gather Requirements

**Minimum required:**
- Chart name
- Workload type (deployment, statefulset, job, cronjob)

**Optional (ask if not provided):**
- Container image repository and tag
- Application port
- Include Ingress? (--ingress flag)
- Include HPA? (--hpa flag)
- Include ConfigMap? (--configmap flag)
- Multi-environment configs?

### Step 3: Generate Chart

#### Option A: Using scaffold_chart.py (Recommended)

For straightforward charts, execute the Python script:

```python
import subprocess
cmd = [
    'python3', 'scripts/scaffold_chart.py',
    chart_name,
    '--workload-type', workload_type,
    '--output', '/mnt/user-data/outputs'
]
if include_ingress:
    cmd.append('--ingress')
if include_hpa:
    cmd.append('--hpa')
if include_configmap:
    cmd.append('--configmap')

subprocess.run(cmd, check=True)
```

**The script automatically:**
- Creates chart directory structure
- Copies template files from `assets/templates/`
- Replaces `CHARTNAME` placeholder with actual chart name
- Includes only requested resources
- Applies best practices

#### Option B: Manual Generation

For custom requirements, manually copy and modify templates:

1. Read template from `assets/templates/<workload>/<file>.yaml`
2. Replace `CHARTNAME` with actual chart name
3. Customize based on user requirements
4. Write to `/home/claude/<chart-name>/templates/`

### Step 4: Multi-Environment Configuration

If user requests dev/staging/prod configs, create additional values files:

**values-dev.yaml:**
```yaml
replicaCount: 1
resources:
  limits: {cpu: 200m, memory: 128Mi}
  requests: {cpu: 25m, memory: 32Mi}
env:
  - name: LOG_LEVEL
    value: "debug"
```

**values-prod.yaml:**
```yaml
replicaCount: 3
resources:
  limits: {cpu: 1000m, memory: 512Mi}
  requests: {cpu: 100m, memory: 128Mi}
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
```

### Step 5: Testing Instructions

**Always provide comprehensive testing workflow:**

```bash
# Navigate to chart directory
cd <chart-name>

# 1. Validate chart structure
helm lint .

# 2. Render templates locally
helm template <chart-name> .

# 3. Dry run installation
helm install <chart-name> . --dry-run --debug

# 4. Test with specific values
helm template <chart-name> . -f values-dev.yaml

# 5. Deploy to test namespace
kubectl create namespace test
helm install <chart-name> . -n test

# 6. Verify deployment
kubectl get all -n test
helm status <chart-name> -n test

# 7. Cleanup
helm uninstall <chart-name> -n test
kubectl delete namespace test
```

### Step 6: Deliver Output

- Chart is created in `/mnt/user-data/outputs/<chart-name>/`
- Provide download link
- Include testing instructions
- Explain customization options

## Workload Types

Load `references/workload-types.md` for detailed decision tree and characteristics.

**Quick reference:**
- **Deployment**: Stateless apps (web, API, microservices)
- **StatefulSet**: Stateful apps (databases, caches) - stable IDs, persistent storage
- **Job**: One-time tasks (migrations, ETL)
- **CronJob**: Scheduled tasks (backups, reports)

**Template locations:**
- `assets/templates/deployment/deployment.yaml`
- `assets/templates/statefulset/statefulset.yaml`
- `assets/templates/job/job.yaml`
- `assets/templates/cronjob/cronjob.yaml`

## Converting Manifests to Helm

When user provides raw Kubernetes YAML:

1. **Analyze manifests**: Identify resources and configurable values
2. **Extract variables**: Images, replicas, ports, resources, env-specific settings
3. **Create values.yaml**: Organize extracted values logically
4. **Templatize YAML**:
   - Replace hardcoded values with `{{ .Values.* }}`
   - Use `{{ include "CHARTNAME.fullname" . }}` for names
   - Use `{{ include "CHARTNAME.labels" . }}` for labels
5. **Add helpers**: Copy `assets/templates/_helpers.tpl` and customize
6. **Document**: Explain what was parameterized

## Template Assets Structure

```
assets/templates/
├── Chart.yaml           # Base chart metadata
├── values.yaml          # Complete values with all options
├── .helmignore          # Files to ignore
├── _helpers.tpl         # Helper functions (CHARTNAME placeholder)
├── NOTES.txt            # Post-install instructions
├── deployment/
│   └── deployment.yaml  # Deployment template
├── statefulset/
│   └── statefulset.yaml # StatefulSet template
├── job/
│   └── job.yaml         # Job template
├── cronjob/
│   └── cronjob.yaml     # CronJob template
├── service/
│   └── service.yaml     # Service template
├── ingress/
│   └── ingress.yaml     # Ingress template
├── hpa/
│   └── hpa.yaml         # HPA template
├── configmap/
│   └── configmap.yaml   # ConfigMap template
└── rbac/
    └── serviceaccount.yaml  # ServiceAccount template
```

All templates use `CHARTNAME` placeholder which is replaced by the script.

## Scripts

### scaffold_chart.py

**Purpose**: Automated chart generation from templates

**Usage**:
```bash
python3 scripts/scaffold_chart.py CHART_NAME [OPTIONS]

Arguments:
  CHART_NAME              Name of the Helm chart

Options:
  -w, --workload-type    Type: deployment, statefulset, job, cronjob (default: deployment)
  -o, --output          Output directory (default: current directory)
  --ingress             Include Ingress resource
  --hpa                 Include HorizontalPodAutoscaler
  --configmap           Include ConfigMap
```

**What it does:**
- Creates chart directory structure
- Copies relevant templates from `assets/templates/`
- Replaces `CHARTNAME` placeholder
- Includes only requested optional resources
- Applies best practices automatically

## Best Practices (Auto-Applied)

The templates in `assets/templates/` already include:
- ✅ Standard Kubernetes labels (`app.kubernetes.io/*`)
- ✅ Security contexts (readOnlyRootFilesystem, runAsNonRoot, dropped capabilities)
- ✅ Resource limits and requests
- ✅ Health checks (liveness and readiness probes)
- ✅ Helper functions for naming and labels
- ✅ Proper selector labels
- ✅ Service account configuration

## Organizational Standardization

For platform teams needing consistent charts:

1. **Capture standards**: Ask about required labels, policies, security requirements
2. **Modify templates**: Update `assets/templates/_helpers.tpl` with org labels
3. **Generate**: Use scaffold_chart.py with modified templates
4. **Document**: Explain customization points

Example org-specific helper addition:
```yaml
{{- define "CHARTNAME.orgLabels" -}}
org.example.com/cost-center: {{ .Values.org.costCenter | required "Cost center required" }}
org.example.com/team: {{ .Values.org.team | required "Team name required" }}
{{- end }}
```

## Success Criteria

Generated charts must:
- ✅ Pass `helm lint` without errors (95%+ target)
- ✅ Follow CNCF/Helm best practices
- ✅ Include security contexts by default
- ✅ Have resource limits configured
- ✅ Use standard Kubernetes labels
- ✅ Be deployment-ready within <15 minutes

## References

Load as needed based on use case:

**For workload selection:**
- `references/workload-types.md` - Decision tree, characteristics, when to use each type

**For testing:**
- `references/testing-guide.md` - Comprehensive dry-run workflows, mock values, validation commands

**For best practices:**
- `references/best-practices.md` - CNCF/Helm standards, security guidelines

**For examples:**
- `references/examples.md` - Real-world chart scenarios

**For template reference:**
- `references/templates.md` - Inline template documentation

## Example Usage

### Example 1: Simple Web App

```
User: "Create a Helm chart for my Node.js API"

Claude: I'll create a chart for your Node.js API. A few quick questions:
1. What's the chart name? (e.g., "user-api")
2. What's your container image? (e.g., "myorg/user-api:1.0.0")
3. Do you need an Ingress? (yes/no)

User: Name is user-api, image is myorg/user-api:1.0.0, yes to ingress

Claude: [Executes]
python3 scripts/scaffold_chart.py user-api \
  --workload-type deployment \
  --output /mnt/user-data/outputs \
  --ingress

[Chart generated successfully]
[Provides testing instructions]
```

### Example 2: Database

```
User: "Create a Helm chart for PostgreSQL with persistent storage"

Claude: I'll create a StatefulSet chart for PostgreSQL.
What storage size do you need? (e.g., 10Gi, 20Gi)

User: 20Gi

Claude: [Executes]
python3 scripts/scaffold_chart.py postgresql \
  --workload-type statefulset \
  --output /mnt/user-data/outputs

[Then manually adds persistence config to values.yaml]
persistence:
  enabled: true
  size: 20Gi
  storageClass: standard
```

### Example 3: Scheduled Backup

```
User: "Create a CronJob chart for nightly backups"

Claude: [Executes]
python3 scripts/scaffold_chart.py db-backup \
  --workload-type cronjob \
  --output /mnt/user-data/outputs

[Then updates values.yaml with schedule]
cronjob:
  schedule: "0 2 * * *"
```

## Troubleshooting

**Issue**: Script fails to find templates
**Solution**: Ensure running from skill directory or provide full path to script

**Issue**: CHARTNAME not replaced
**Solution**: Script automatically handles this; if manual, use find/replace

**Issue**: Generated chart fails lint
**Solution**: Check values.yaml for required fields, review templates

## Notes

- Always use `scaffold_chart.py` when possible - it's faster and consistent
- Templates use `CHARTNAME` placeholder - script replaces automatically
- For complex customization, read templates from assets and modify manually
- Multi-environment configs are created separately after initial generation
- Testing instructions are critical - always include them
