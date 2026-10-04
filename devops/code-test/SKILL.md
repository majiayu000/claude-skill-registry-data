---
name: code-test
description: Test DevOps code including Terraform, Kubernetes, Docker, and shell scripts using unit tests, integration tests, and compliance tests. Use when creating test strategies, writing infrastructure tests, or validating infrastructure changes.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# DevOps Code Testing Skill

You are a Senior DevOps Engineer specializing in testing infrastructure code. You implement testing strategies for Terraform, Kubernetes, Docker, and shell scripts using unit tests, integration tests, and compliance validation.

## Core Testing Areas

1. **Terraform Testing**
   - Unit tests with Terraform Test Framework
   - Integration tests with Terratest
   - Plan validation
   - Cost estimation tests

2. **Kubernetes Testing**
   - YAML validation with kubeconform
   - Policy testing with OPA/Conftest
   - Helm chart testing
   - Dry-run validation

3. **Docker Testing**
   - Image structure tests
   - Container runtime tests
   - Security scanning
   - Multi-arch testing

4. **CI/CD Testing**
   - Workflow validation
   - Mock pipeline runs
   - Security gate testing

5. **Shell Script Testing**
   - Unit tests with Bats
   - Static analysis with ShellCheck
   - Integration testing

## Terraform Testing

### Terraform Test Framework

```hcl
# tests/unit.tftest.hcl
variables {
  environment = "test"
  project     = "test-project"
}

run "validate_vpc" {
  command = plan

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block should be 10.0.0.0/16"
  }

  assert {
    condition     = aws_vpc.main.enable_dns_hostnames == true
    error_message = "DNS hostnames should be enabled"
  }
}

run "validate_security_group_rules" {
  command = plan

  assert {
    condition     = length(aws_security_group.web.ingress) == 1
    error_message = "Web security group should have exactly one ingress rule"
  }

  assert {
    condition     = aws_security_group.web.ingress[0].from_port == 443
    error_message = "Web security group should only allow HTTPS"
  }
}

run "validate_tags" {
  command = plan

  variables {
    tags = {
      Environment = "test"
      Project     = "test-project"
    }
  }

  assert {
    condition     = aws_vpc.main.tags["Environment"] == "test"
    error_message = "VPC should have Environment tag"
  }
}
```

### Terratest (Go)

```go
// tests/vpc_test.go
package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/gruntwork-io/terratest/modules/aws"
	"github.com/stretchr/testify/assert"
)

func TestVpcCreation(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../terraform/modules/vpc",
		Vars: map[string]interface{}{
			"environment": "test",
			"vpc_cidr": "10.0.0.0/16",
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	vpcID := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcID)

	// Verify VPC exists
	vpc := aws.GetVpcById(t, vpcID, "us-east-1")
	assert.Equal(t, "10.0.0.0/16", vpc.CidrBlock)
	assert.Equal(t, "available", vpc.State)
}

func TestSecurityGroupRules(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../terraform/modules/security",
		Vars: map[string]interface{}{
			"allowed_cidr": []string{"10.0.0.0/8"},
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	// Test ingress rules
	ingressRules := terraform.OutputListOfObjects(t, terraformOptions, "ingress_rules")
	for _, rule := range ingressRules {
		cidrBlocks := rule["cidr_blocks"].([]interface{})
		assert.NotContains(t, cidrBlocks, "0.0.0.0/0")
	}
}
```

### Terraform Plan Validation

```yaml
# .github/workflows/terraform-test.yml
name: Terraform Tests

on:
  pull_request:
    paths:
      - 'terraform/**'

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.7.0"

      - name: Run Terraform Tests
        run: |
          cd terraform/modules/vpc
          terraform init
          terraform test

  integration-tests:
    runs-on: ubuntu-latest
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Run Terratest
        run: |
          cd tests
          go test -v -timeout 30m
```

## Kubernetes Testing

### Kubeconform

```yaml
# .github/workflows/k8s-test.yml
name: Kubernetes Tests

on:
  pull_request:
    paths:
      - 'k8s/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install kubeconform
        run: |
          curl -L -o kubeconform.tar.gz https://github.com/yannh/kubeconform/releases/download/v0.6.4/kubeconform-linux-amd64.tar.gz
          tar -xzf kubeconform.tar.gz
          sudo mv kubeconform /usr/local/bin/

      - name: Validate manifests
        run: |
          kubeconform -strict -schema-location default \
            -schema-location 'https://raw.githubusercontent.com/yannh/kubernetes-json-schema/master' \
            k8s/

      - name: Helm lint
        run: |
          helm lint charts/*
          helm template myapp charts/myapp | kubeconform -strict
```

### OPA/Conftest Tests

```rego
# tests/k8s/policy.rego
package main

deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot
  msg := "Deployment must run as non-root"
}

deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.resources.limits.memory
  msg := sprintf("Container %s must have memory limits", [container.name])
}

deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  container.image
  contains(container.image, ":latest")
  msg := sprintf("Container %s must not use 'latest' tag", [container.name])
}

deny[msg] {
  input.kind == "Service"
  input.spec.type == "LoadBalancer"
  not input.metadata.annotations["service.beta.kubernetes.io/aws-load-balancer-internal"]
  msg := "LoadBalancer service must be internal"
}

warn[msg] {
  input.kind == "Deployment"
  input.spec.replicas < 2
  msg := "Deployment should have at least 2 replicas for HA"
}
```

### Helm Testing

```yaml
# charts/myapp/templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "myapp.fullname" . }}-test-connection"
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args:
        - '--spider'
        - '{{ include "myapp.fullname" . }}:{{ .Values.service.port }}/health'
  restartPolicy: Never
```

```yaml
# test-helm.yml
name: Helm Tests
on:
  pull_request:
    paths:
      - 'charts/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Helm
        uses: azure/setup-helm@v3

      - name: Setup Kind
        uses: helm/kind-action@v1

      - name: Run Helm tests
        run: |
          helm install myapp charts/myapp --wait
          helm test myapp
```

## Docker Testing

### Container Structure Tests

```yaml
# tests/container-structure.yaml
schemaVersion: "2.0.0"

commandTests:
  - name: "node version"
    command: "node"
    args: ["--version"]
    expectedOutput: ["v20."]

  - name: "npm version"
    command: "npm"
    args: ["--version"]
    expectedOutput: ["10."]

  - name: "health check endpoint"
    command: "curl"
    args: ["-f", "http://localhost:8080/health"]
    expectedOutput: ["ok"]

fileExistenceTests:
  - name: "app directory exists"
    path: "/app"
    shouldExist: true

  - name: "tmp directory exists"
    path: "/tmp"
    shouldExist: true

fileContentTests:
  - name: "package.json contains app name"
    path: "/app/package.json"
    expectedContents: ["myapp"]

metadataTest:
  env:
    - key: NODE_ENV
      value: production
  labels:
    - key: maintainer
      value: platform-team
  exposedPorts: ["8080"]
  user: "nodejs"
```

```yaml
name: Docker Tests
on:
  pull_request:
    paths:
      - 'Dockerfile'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t app:test .

      - name: Container Structure Test
        uses: brpaz/structure-tests-action@v1
        with:
          image: app:test
          config: tests/container-structure.yaml
```

### Docker Compose Testing

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=test
    depends_on:
      - db
      - redis
    command: npm test

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test

  redis:
    image: redis:7-alpine
```

```yaml
name: Docker Compose Tests
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Shell Script Testing

### Bats Tests

```bash
#!/usr/bin/env bats
# tests/test_backup.bats

@test "backup script exists and is executable" {
  [ -x "./scripts/backup.sh" ]
}

@test "backup script requires database argument" {
  run ./scripts/backup.sh
  [ "$status" -eq 1 ]
  [[ "$output" == *"Usage:"* ]]
}

@test "backup script validates database name" {
  run ./scripts/backup.sh "invalid; rm -rf /"
  [ "$status" -eq 1 ]
  [[ "$output" == *"Invalid database name"* ]]
}

@test "backup script creates backup file" {
  run ./scripts/backup.sh "test_db" "test-bucket"
  [ "$status" -eq 0 ]
  [ -f "/tmp/backup-*/backup.sql" ]
}

@test "backup script cleans up on failure" {
  DB_HOST="invalid" run ./scripts/backup.sh "test_db" "test-bucket"
  [ "$status" -eq 1 ]
  [ ! -d "/tmp/backup-*" ]
}
```

```yaml
name: Shell Tests
on:
  pull_request:
    paths:
      - 'scripts/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bats
        run: |
          git clone https://github.com/bats-core/bats-core.git
          cd bats-core
          sudo ./install.sh /usr/local

      - name: Run tests
        run: bats tests/
```

## Ansible Testing

### Molecule

```yaml
# molecule/default/converge.yml
---
- name: Converge
  hosts: all
  tasks:
    - name: Include role
      ansible.builtin.include_role:
        name: common

# molecule/default/verify.yml
---
- name: Verify
  hosts: all
  gather_facts: false
  tasks:
    - name: Check SSH service
      ansible.builtin.service:
        name: ssh
        state: started
      register: ssh_status
      failed_when: not ssh_status.status.ActiveState == "active"

    - name: Verify timezone
      ansible.builtin.command: timedatectl
      register: timezone
      changed_when: false
      failed_when: "'UTC' not in timezone.stdout"

    - name: Check fail2ban
      ansible.builtin.service:
        name: fail2ban
        state: started
```

```yaml
name: Ansible Tests
on:
  pull_request:
    paths:
      - 'ansible/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ansible molecule molecule-docker

      - name: Run Molecule tests
        run: |
          cd ansible/roles/common
          molecule test
```

## Compliance Testing

```yaml
name: Compliance Tests
on:
  schedule:
    - cron: '0 0 * * 0'
  workflow_dispatch:

jobs:
  cis-benchmarks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run CIS Benchmark
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'
          format: 'sarif'
          output: 'compliance-results.sarif'

      - name: Check compliance
        run: |
          if [ $(grep -c "CRITICAL" compliance-results.sarif) -gt 0 ]; then
            echo "Compliance violations found"
            exit 1
          fi
```

## Test Organization

```
tests/
├── terraform/
│   ├── unit/
│   │   ├── vpc_test.go
│   │   └── security_test.go
│   └── integration/
│       └── full_stack_test.go
├── kubernetes/
│   ├── policy/
│   │   └── security.rego
│   └── helm/
│       └── values-test.yaml
├── docker/
│   └── container-structure.yaml
├── shell/
│   ├── test_backup.bats
│   └── test_deploy.bats
└── ansible/
    └── molecule/
        └── default/
            ├── converge.yml
            ├── molecule.yml
            └── verify.yml
```

## Test Guidelines

1. **Unit Tests**: Fast, isolated, test single components
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Compliance Tests**: Verify security/policy adherence

## Test Metrics

- Coverage: Minimum 80% for Terraform modules
- Execution Time: < 10 minutes for PR validation
- Reliability: < 1% flaky test rate
- Documentation: Every test has clear purpose documented