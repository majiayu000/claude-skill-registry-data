---




name: in-toto
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"in-toto in Supply Chain Security - cloud native architecture, patterns"
  pitfalls, and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-kms, aws-s3, aws-secrets-manager, azure-key-vault
  role: reference
  scope: infrastructure
  triggers: chain, in toto, in-toto, supply
  archetypes:
  - educational
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: medium
    directive_strength: low
    abstraction_level: strategic
version: "1.0.0"




---




# in-toto in Cloud-Native Engineering

## Purpose and Use Cases

### What Problem Does It Solve?
- **Software supply chain security**: in-toto provides end-to-end integrity for software artifacts throughout their lifecycle
- **Provenance verification**: Cryptographically verify that artifacts were built according to defined supply chain steps
- **Build pipeline assurance**: Ensure no unauthorized changes occurred during build, test, or deployment processes
- **Attack surface reduction**: Prevent supply chain attacks like compromised build tools or malicious code injection

### When to Use
- **High-security applications**: Financial systems, healthcare, government, or critical infrastructure
- **Compliance requirements**: Auditable software development for SOC2, PCI-DSS, HIPAA, or FedRAMP
- **Multi-vendor supply chains**: When multiple organizations contribute to software delivery
- **Open source governance**: Verify third-party dependencies haven't been tampered with
- **Regulatory compliance**: When you need to prove software integrity to auditors

### Key Use Cases
- **Build pipeline verification**: Confirm all build steps executed as defined
- **Artifact provenance**: Track origin and transformation history of software artifacts
- **Release integrity**: Ensure release artifacts haven't been modified after signing
- **Continuous verification**: Integrate in-toto checks into CI/CD pipelines
- **Attack detection**: Detect compromised build tools or malicious code injection

## Architecture Design Patterns

### Core Components

#### In-toto Layout
```
{
  "_type": "layout",
  "expires": "2025-12-31T23:59:59Z",
  "keys": {
    "alice-key-id": {
      "keytype": "rsa",
      "keyid_hash_algorithms": ["sha256"],
      "keyval": {
        "public": "-----BEGIN PUBLIC KEY-----..."
      }
    }
  },
  "roles": [
    {
      "name": "root",
      "threshold": 1,
      "keyids": ["alice-key-id"]
    },
    {
      "name": "staging",
      "threshold": 2,
      "keyids": ["alice-key-id", "bob-key-id"]
    },
    {
      "name": "production",
      "threshold": 3,
      "keyids": ["alice-key-id", "bob-key-id", "carol-key-id"]
    }
  ],
  "steps": [
    {
      "name": "build",
      "expected_artifact": "app-image.tar.gz",
      "expected_command": ["make", "build"],
      "pubkeys": ["alice-key-id"],
      "threshold": 1
    },
    {
      "name": "test",
      "expected_artifact": "app-image.tar.gz",
      "expected_command": ["make", "test"],
      "pubkeys": ["bob-key-id"],
      "threshold": 1
    }
  ],
  "inspect": [
    {
      "name": "verify-integrity",
      "command": ["in-toto-run", "--", "sha256sum", "app-image.tar.gz"],
      "expected_materials": [["MATCH", "app-image.tar.gz", "WITH", "PATH", "app-image.tar.gz"]],
      "expected_products": []
    }
  ]
}
```
- **Layout definition**: Root policy for supply chain verification
- **Roles and thresholds**: Multiple signatures required for critical steps
- **Steps definition**: Build steps with expected artifacts and commands
- **Inspections**: Post-build verification commands

#### Link Metadata
```json
{
  "_type": "link",
  "name": "build",
  "material": {
    "source-code.tar.gz": {
      "sha256": "abc123..."
    }
  },
  "product": {
    "app-image.tar.gz": {
      "sha256": "def456..."
    }
  },
  "command": ["make", "build"],
  "byproducts": {},
  "duration": 42
}
```
- **Step execution record**: Documents a single supply chain step
- **Materials**: Input artifacts with cryptographic hashes
- **Products**: Output artifacts with cryptographic hashes
- **Evidence**: Commands executed and timing information

#### Verification Tool (in-toto-verifier)
- **Layout validation**: Verify layout file structure and signatures
- **Link verification**: Check all link files exist and are valid
- **Hash matching**: Verify product hashes match materials through the pipeline
- **Signature verification**: Ensure all required roles signed

### Component Interactions
```
Builder (Alice)
    ↓ (builds artifact + creates link)
Link Metadata
    ↓ (signed with Alice's key)
In-toto Layout
    ↓ (defines verification policy)
Verifier (CI/CD)
    ↓ (validates all steps)
Artifact Release
```

### Data Flow Patterns

#### Build Pipeline Flow
```
1. Developer pushes code
2. CI system triggers build
3. Build step creates link with materials/products
4. Link signed by build role key
5. Next step reads link as input material
6. Repeat for each pipeline step
7. Final artifact verified against layout
8. Signed metadata included with release
```

#### Verification Flow
```
1. Download artifact + in-toto metadata
2. Load layout policy
3. Verify all link signatures
4. Verify link chain: products of step N = materials of step N+1
5. Execute inspections
6. Report verification result
```

### Design Principles

#### Non-Repudiation
- All supply chain steps must be signed by designated roles
- Key compromise detection through multiple signature requirements
- Immutable link metadata prevents post-hoc modifications

#### Least Privilege
- Each role signs only for authorized steps
- Key separation limits blast radius of compromise
- Threshold signatures prevent single-point failures

#### Verifiability
- All cryptographic material publicly auditable
- Self-contained metadata with no external dependencies
- Standard format enables interoperability

## Integration Approaches

### Integration with Other CNCF Projects

#### Grafeas Integration
```yaml
# Grafeas Note for in-toto policy
apiVersion: grafeas.io/v1
kind: Note
metadata:
  name: projects/myproject/notes/in-toto-policy
spec:
  in_toto: {
    "step": {
      "name": "build",
      "threshold": 1
    }
  }
```
- **Provenance tracking**: Grafeas stores in-toto metadata
- **Policy enforcement**: Grafeas policies validate in-toto signatures
- **Compliance reporting**: Audit trail of software provenance

#### Tekton Chains Integration
```yaml
apiVersion: chains.tekton.dev/v1beta1
kind: Configuration
metadata:
  name: chains
spec:
  artifacts:
    in_toto:
      predicate_type: in-toto.io/Link
      enabled: true
      keyless:
        subject: "https://tkn.dev/chains"
```
- **Automatic link generation**: Tekton pipelines create in-toto links
- **Keyless signing**: Use Fulcio for certificate-based signing
- **Metadata storage**: Store in-toto metadata in artifact registry

#### Cosign Integration
```bash
# Sign in-toto metadata with cosign
cosign sign-blob --output-signature=link.sig link.json

# Verify in-toto policy
cosign verify-blob --signature=link.sig \
  --certificate=link.pem \
  --certificate-identity=build@example.com \
  link.json
```
- **Cryptographic signing**: Cosign signs in-toto metadata
- **Certificate-based signing**: Use Fulcio for keyless signing
- **Policy enforcement**: Rekor provides transparency log verification

#### Kyverno Integration
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-in-toto
spec:
  rules:
    - name: check-in-toto
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Container images must have in-toto attestation"
        deny:
          conditions:
            - key: "{{ request.object.spec.containers[].image }}"
              operator: AnyNotIn
              value: "{{ 'images' | length(@) > 0 }}"
```
- **Policy enforcement**: Kyverno policies require in-toto attestation
- **Admission control**: Block pods without valid in-toto metadata
- **Automated remediation**: Policies can automatically add missing metadata

### API Patterns

#### Layout API
- **Layout definition**: JSON Schema for supply chain policy
- **Key management**: RSA, ECDSA, Ed25519 key support
- **Role management**: Define roles with signature thresholds

#### Link API
- **Link creation**: Generate link metadata for each step
- **Link signing**: Sign links with cryptographic keys
- **Link verification**: Verify links against layout policy

### Configuration Patterns

#### Layout Configuration
```json
{
  "expires": "2025-12-31T00:00:00Z",
  "keys": {},
  "roles": {
    "root": {
      "threshold": 1,
      "keyids": []
    }
  },
  "steps": [
    {
      "name": "checkout",
      "pubkeys": [],
      "threshold": 1,
      "expected_artifacts": [],
      "expected_command": []
    }
  ]
}
```

#### Key Generation
```bash
# Generate in-toto key
in-toto-keygen -t ed25519 -u alice

# Export public key
cat alice.pub

# Import public key into layout
in-toto-sign -f layout.json -p alice.pub
```

### Extension Mechanisms

#### Custom Predicate Types
- **SLSA Provenance**: Use in-toto with SLSA provenance predicate
- **Cosign Attestations**: Integrate with cosign for keyless signing
- **Custom predicates**: Define organization-specific predicates

#### Verification Integrations
- **CLI tool**: `in-toto-verify` for manual verification
- **Library support**: Go, Python, JavaScript libraries
- **CI/CD integration**: GitHub Actions, GitLab CI, Tekton

## Common Pitfalls and How to Avoid Them

### Configuration Issues

#### Expired Layout
**Problem**: Layout file expires and verification fails.

**Solution**:
- Set long expiration dates (1+ years)
- Implement layout rotation process
- Monitor expiration dates
- Use continuous delivery for layout updates

#### Missing Keys
**Problem**: Keys used in layout not available for verification.

**Solution**:
- Distribute public keys with layout
- Use keyless signing with certificate authorities
- Implement key backup and recovery
- Test verification with all keys available

#### Incorrect Thresholds
**Problem**: Threshold too high causes legitimate failures, too low reduces security.

**Solution**:
- Start with threshold of 1 for each role
- Increase thresholds as confidence grows
- Use separate keys for different purposes
- Document key rotation procedures

### Performance Issues

#### Large Metadata Files
**Problem**: Many links create large metadata files.

**Solutions**:
- Use link aggregation for batches
- Implement link expiration and cleanup
- Store links in separate storage
- Use link metadata inlining where appropriate

#### Verification Slowdown
**Problem**: Complex layouts with many steps slow verification.

**Solutions**:
- Cache verification results
- Parallelize independent step verification
- Use optimized implementations
- Profile verification for bottlenecks

### Operational Challenges

#### Key Compromise Recovery
**Problem**: Key compromise requires layout update and re-signing.

**Solutions**:
- Implement key rotation procedures
- Use multi-signature policies
- Document incident response procedures
- Test recovery procedures regularly

#### Build Tool Integration
**Problem**: Existing build tools don't naturally produce in-toto links.

**Solutions**:
- Wrap existing tools with in-toto runners
- Use in-toto plugins where available
- Implement build step instrumentation
- Gradual adoption strategy

#### Cross-Platform Compatibility
**Problem**: in-toto metadata format varies between implementations.

**Solutions**:
- Use standard in-toto specification
- Validate against JSON Schema
- Test with multiple verifier implementations
- Contribute improvements to standard

### Security Pitfalls

#### Weakened Signature Requirements
**Problem**: Reducing thresholds during emergencies creates security gaps.

**Solutions**:
- Document emergency procedures
- Require post-incident review
- Automatically revert threshold changes
- Alert on threshold modifications

#### Insecure Key Storage
**Problem**: Private keys stored in source control or accessible locations.

**Solutions**:
- Use hardware security modules (HSM)
- Store keys in secrets management systems
- Implement key access auditing
- Use keyless signing where possible

#### Incomplete Supply Chain Coverage
**Problem**: Only some steps covered, allowing bypass through uncovered steps.

**Solutions**:
- Map all supply chain steps
- Include all manual and automated steps
- Cover developer laptop builds
- Verify intermediate artifacts

## Coding Practices

### Idiomatic Configuration

#### Layout File Structure
```json
{
  "_type": "layout",
  "spec_version": "1.0",
  "expires": "2025-12-31T23:59:59Z",
  "keys": {
    "keyid1": {
      "keytype": "ed25519",
      "keyval": {
        "public": "publickeybase64"
      }
    }
  },
  "roles": {
    "root": {
      "threshold": 1,
      "keyids": ["keyid1"]
    }
  },
  "steps": [],
  "inspect": []
}
```

### API Usage Patterns

#### Layout Creation
```bash
# ✅ GOOD — in-toto layout creation via CLI
# Generate in-toto layout using in-toto-tool
in-toto-record start --name build --expected-products app.tar.gz

# Create initial layout file
cat > layout.json << 'EOF'
{
  "_type": "layout",
  "spec_version": "1.0",
  "expires": "2025-12-31T23:59:59Z",
  "keys": {},
  "roles": {
    "root": { "threshold": 1, "keyids": [] }
  },
  "steps": [],
  "inspect": []
}
EOF

# Add steps to layout
in-toto-layout --add-step build --pubkey alice.pub --threshold 1

# Sign layout with root key
in-toto-sign -f layout.json -k root.key
```

#### Link Generation
```go
// Go example
link := link.Link{
    Name:      "build",
    Materials: materials,
    Products:  products,
    Command:   command,
}

link.Sign(privateKey)
```

### Observability Best Practices

#### Logging Verification
- Log verification pass/fail with details
- Include artifact hashes in logs
- Record verification timestamps
- Correlate with build IDs

#### Metrics Collection
- Link creation count by step
- Verification success/failure rates
- Key rotation frequency
- Layout expiration monitoring

### Development Workflow

#### Layout Development
1. Define supply chain steps
2. Generate initial layout
3. Test with sample builds
4. Add signatures
5. Verify with sample artifacts
6. Deploy to CI/CD
7. Monitor verification results

#### CI/CD Integration
- Generate links during build
- Sign links with CI keys
- Store links with artifacts
- Verify before release
- Fail build on verification failure

## Fundamentals

### Essential Concepts

#### In-toto Metadata Format
- **Layout file**: Root policy defining supply chain
- **Link files**: Step execution records with artifacts and signatures
- **Metadata structure**: Standardized JSON format
- **Cryptographic signatures**: ECDSA, Ed25519, RSA support

#### Verification Process
- **Layout loading**: Parse policy from layout file
- **Link validation**: Check signatures and link chain
- **Artifact matching**: Verify materials flow to products
- **Inspection execution**: Run post-build verification commands

### Terminology Glossary

| Term | Definition |
|------|------------|
| **Layout** | Root policy file defining supply chain verification rules |
| **Link** | Metadata record for a single supply chain step execution |
| **Material** | Input artifact to a supply chain step |
| **Product** | Output artifact from a supply chain step |
| **Step** | A discrete action in the software supply chain |
| **Inspection** | Post-build verification command |
| **Threshold** | Number of signatures required for validity |
| **Key ID** | Unique identifier for a cryptographic key |
| **Signature** | Cryptographic proof of authorship |
| **Metadata** | Information about software artifacts and their history |

### Data Models and Types

#### Layout Schema
```json
{
  "_type": "layout",
  "spec_version": "string",
  "expires": "string (ISO 8601)",
  "keys": {
    "keyid": {
      "keytype": "string",
      "keyval": {
        "public": "string"
      }
    }
  },
  "roles": {
    "rolename": {
      "threshold": "number",
      "keyids": ["string"]
    }
  },
  "steps": [
    {
      "name": "string",
      "pubkeys": ["string"],
      "threshold": "number",
      "expected_materials": [],
      "expected_products": []
    }
  ],
  "inspect": [
    {
      "name": "string",
      "command": ["string"],
      "expected_materials": [],
      "expected_products": []
    }
  ]
}
```

#### Link Schema
```json
{
  "_type": "link",
  "name": "string",
  "material": {
    "artifact_path": {
      "sha256": "string"
    }
  },
  "product": {
    "artifact_path": {
      "sha256": "string"
    }
  },
  "command": ["string"],
  "byproducts": {},
  "duration": "number"
}
```

### Lifecycle Management

#### Layout Lifecycle
1. **Creation**: Initial layout with minimal roles
2. **Signing**: Root key signs initial layout
3. **Distribution**: Layout distributed to all verifiers
4. **Rotation**: Periodic key and layout updates
5. **Revocation**: Compromised keys removed from layout
6. **Expiration**: Layout expires and must be renewed

#### Link Lifecycle
1. **Creation**: Build step generates link
2. **Signing**: Step key signs link
3. **Storage**: Link stored with artifact
4. **Aggregation**: Multiple links combined
5. **Verification**: Link verified against layout
6. **Archival**: Old links archived or deleted

### State Management

#### Layout State
- **Expiration tracking**: Monitor layout expiration dates
- **Key status**: Active, revoked, rotated
- **Role membership**: Keys assigned to roles
- **Step definitions**: Current supply chain steps

#### Link State
- **Step completion**: Pending, complete, failed
- **Signature status**: Unsigned, signed, verified
- **Artifact status**: In material, in product
- **Chain state**: Connected to other links

## Scaling and Deployment Patterns

### Horizontal Scaling

#### Multiple Verifiers
- **Parallel verification**: Multiple verifiers check same artifact
- **Load distribution**: Distribute verification load
- **High availability**: Redundant verification services
- **Cache sharing**: Shared verification results

#### Link Aggregation
- **Batch signing**: Sign multiple links together
- **Link aggregation files**: Combine links for efficiency
- **Incremental updates**: Update only changed links

### High Availability

#### Verification Service Redundancy
- **Multiple verifier instances**: Run multiple verifiers
- **Load balancing**: Distribute verification requests
- **Failover verification**: Secondary verifier for failover
- **Caching**: Cache verification results

#### Layout Distribution
- **CDN distribution**: Deliver layout via CDN
- **Multiple sources**: Verify layout from multiple sources
- **Local caches**: Cache layouts for offline verification
- **Versioning**: Support multiple layout versions

### Production Deployments

#### CI/CD Pipeline Integration
1. Generate links during build
2. Sign links with appropriate keys
3. Store links with artifacts
4. Verify before deployment
5. Fail pipeline on verification failure

#### Deployment Gate
```yaml
# GitHub Actions example
- name: Verify in-toto
  uses: in-toto/verify-action@v1
  with:
    layout: layout.json
    artifact: app.tar.gz
```

### Upgrade Strategies

#### Layout Evolution
1. Create new layout with updated rules
2. Sign with new keys
3. Deploy new layout alongside old
4. Monitor verification results
5. Switch to new layout
6. Archive old layout

#### Key Rotation
1. Generate new keys
2. Update layout with new keys
3. Sign layout with old keys
4. Distribute updated layout
5. Stop using old keys
6. Securely delete old keys

### Resource Management

#### Storage Optimization
- **Compress links**: Use gzip for storage
- **Link expiration**: Delete old links
- **Aggregated storage**: Store multiple links together
- **Tiered storage**: Hot/warm/cold storage tiers

#### Memory Constraints
- **Streaming verification**: Process large link files incrementally
- **Memory limits**: Enforce verification memory limits
- **Link size limits**: Limit individual link sizes
- **Batch processing**: Process links in batches

## Additional Resources

### Official Documentation
- **in-toto GitHub**: https://github.com/in-toto
- **in-toto Specification**: https://github.com/in-toto/attestation
- **in-toto Python**: https://pypi.org/project/in-toto/
- **in-toto Go**: https://pkg.go.dev/github.com/in-toto/in-toto-golang
- **in-toto Ruby**: https://rubygems.org/gems/in_toto

### CNCF References
- **in-toto in CNCF Landscape**: https://landscape.cncf.io/?group=projects&filter=supply-chain
- **CNCF Security Technical Advisory Group**: https://github.com/cncf/sig-security

### Tools and Libraries
- **in-toto-rs**: Rust implementation
- **in-toto-golang**: Go implementation
- **in-toto-python**: Python implementation
- **in-toto-js**: JavaScript implementation
- **fulcio**: Keyless signing CA
- **cosign**: Container signing tool
- **slsa-generator**: SLSA provenance generator

### Tutorials and Guides
- **in-toto Getting Started**: https://in-toto.readthedocs.io/en/latest/
- **Build Secure Systems with in-toto**: https://www.usenix.org/conference/usenixsecurity20/presentation/melara
- **Software Supply Chain Security with in-toto**: https://arxiv.org/abs/2009.06734

### Community Resources
- **in-toto Mailing List**: https://groups.google.com/g/in-toto
- **in-toto Slack**: #in-toto channel
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/in-toto

### Related Standards
- **SLSA (Supply-chain Levels for Software Artifacts)**: https://slsa.dev/
- **OCI Images**: https://github.com/opencontainers/image-spec
- **CycloneDX**: https://cyclonedx.org/
- **SPDX**: https://spdx.dev/

### OpenTelemetry Integration
- **Tracing**: Trace verification steps
- **Metrics**: Count verification pass/fail rates
- **Logs**: Verify and audit verification results

## Troubleshooting

### Common Issues

1. **Deployment Failures**
   - Check pod logs for errors
   - Verify configuration values
   - Ensure network connectivity

2. **Performance Issues**
   - Monitor resource usage
   - Adjust resource limits
   - Check for bottlenecks

3. **Configuration Errors**
   - Validate YAML syntax
   - Check required fields
   - Verify environment-specific settings

4. **Integration Problems**
   - Verify API compatibility
   - Check dependency versions
   - Review integration documentation

### Getting Help

- Check official documentation
- Search GitHub issues
- Join community channels
- Review logs and metrics

## Examples

### Basic Configuration


```yaml
# Basic configuration example
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{project_name}}-config
  namespace: default
data:
  # Configuration goes here
  config.yaml: |
    # Base configuration
    # Add your settings here
```

### Kubernetes Deployment


```yaml
# Kubernetes deployment for {{project_name}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{project_name}}
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{project_name}}
  template:
    metadata:
      labels:
        app: {{project_name}}
    spec:
      containers:
      - name: {{project_name}}
        image: {{project_name}}:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Kubernetes Service


```yaml
# Kubernetes service for {{project_name}}
apiVersion: v1
kind: Service
metadata:
  name: {{project_name}}
  namespace: default
spec:
  selector:
    app: {{project_name}}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

---

## When to Use

Use this skill when:

- **Integrating a CNCF project into Kubernetes infrastructure** — You need to configure, deploy, or troubleshoot a cloud-native tool within a cluster
- **Designing cloud-native architecture** — You are selecting and integrating CNCF tools to solve specific infrastructure challenges
- **Resolving operational issues** — A CNCF component is misbehaving, underperforming, or needs configuration changes
---

## Core Workflow

1. **Assess Requirements** — Understand the use case, scale, integration needs, and existing infrastructure. **Checkpoint:** Document requirements, constraints, and success criteria.

2. **Design Architecture** — Plan component interactions, data flow, and deployment strategy using cloud-native best practices. **Checkpoint:** Verify the architecture addresses all requirements and follows CNCF conventions.

3. **Implement & Configure** — Create manifests, configurations, and deployment scripts. Include resource limits, health checks, and observability hooks. **Checkpoint:** Validate all YAML against schema and test in a staging environment.

4. **Deploy & Monitor** — Apply manifests to the cluster, verify component health, and confirm observability is working. **Checkpoint:** Confirm all pods/services are running, probes passing, and metrics/alerts configured.

---

## Constraints

### MUST DO
- Include at least one complete working YAML manifest example
- Note when content is auto-generated vs. manually verified
- Reference relevant CNCF project documentation

### MUST NOT DO
- Deploy manifests without testing in a staging environment first
- Use deprecated API versions (e.g., apps/v1beta1)
- Omit resource limits and requests in Kubernetes manifests
