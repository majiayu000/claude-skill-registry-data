---
name: dependency-manager
version: "2.0"
trigger: dependency management, vulnerability scan, package audit, npm audit
description: Dependency management, vulnerability scanning, license compliance, package updates, and monorepo tooling. Use when updating dependencies, auditing packages, managing licenses, or configuring package managers.
---

# Dependency Manager

## Package Management

### Monorepo with pnpm
```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'

# .npmrc
shamefully-hoist=true
strict-peer-dependencies=false
auto-install-peers=true
```

### Dependency Updates
```bash
# Check for updates
pnpm outdated

# Update all dependencies
pnpm update --latest

# Update specific package
pnpm update react@latest

# Interactive update
pnpm update --interactive
```

## Security Auditing

### Automated Scanning
```typescript
// scripts/security-audit.ts
import { execSync } from 'child_process';

async function securityAudit() {
  try {
    const result = execSync('pnpm audit --json', { encoding: 'utf-8' });
    const audit = JSON.parse(result);
    
    const critical = audit.advisories.filter(a => a.severity === 'critical');
    const high = audit.advisories.filter(a => a.severity === 'high');
    
    if (critical.length > 0) {
      console.error(`❌ ${critical.length} critical vulnerabilities found`);
      process.exit(1);
    }
    
    if (high.length > 0) {
      console.warn(`⚠️ ${high.length} high severity vulnerabilities`);
    }
  } catch (error) {
    console.error('Audit failed:', error);
    process.exit(1);
  }
}
```

### Lock File Integrity
```bash
# Verify lock file
pnpm install --frozen-lockfile

# Check for lock file drift
pnpm install && git diff --exit-code pnpm-lock.yaml
```

## License Compliance

```typescript
// scripts/check-licenses.ts
import checker from 'license-checker';

const ALLOWED_LICENSES = [
  'MIT',
  'Apache-2.0',
  'BSD-3-Clause',
  'ISC',
  'CC0-1.0'
];

const FORBIDDEN_LICENSES = [
  'GPL-2.0',
  'GPL-3.0',
  'AGPL-3.0'
];

checker.init({ start: '.' }, (err, packages) => {
  if (err) process.exit(1);
  
  for (const [name, info] of Object.entries(packages)) {
    const licenses = Array.isArray(info.licenses) 
      ? info.licenses 
      : [info.licenses];
    
    for (const license of licenses) {
      if (FORBIDDEN_LICENSES.includes(license)) {
        console.error(`❌ Forbidden license ${license} in ${name}`);
        process.exit(1);
      }
    }
  }
  
  console.log('✅ All licenses compliant');
});
```

## Bundle Size Analysis

```typescript
// scripts/analyze-bundle.ts
import { analyze } from 'webpack-bundle-analyzer';

async function analyzeBundle() {
  const stats = await import('./dist/stats.json');
  
  const largeModules = stats.modules
    .filter(m => m.size > 100000)
    .sort((a, b) => b.size - a.size);
  
  console.log('Large modules (>100KB):');
  largeModules.forEach(m => {
    console.log(`  ${m.name}: ${(m.size / 1024).toFixed(2)}KB`);
  });
}
```

## Dependency Graph

```bash
# Visualize dependencies
pnpm list --depth=10 --json | jq '.'

# Find why a package is installed
pnpm why lodash

# Find duplicate packages
pnpm dedupe --check
pnpm dedupe
```
