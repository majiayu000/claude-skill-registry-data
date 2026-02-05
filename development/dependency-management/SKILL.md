---
name: dependency-management
description: 依存関係管理ガイド。Swift Package Manager、CocoaPods、npm、pip等のパッケージマネージャー運用、バージョン管理、セキュリティアップデート、ライセンス管理など、依存関係の効率的な管理方法。
status: high
completion: 100%
guides: 3
---

# Dependency Management Skill

## Status

🟢 **High** (100% completion, 3/3 comprehensive guides)

## Overview

依存関係管理は、現代のソフトウェア開発において最も重要な要素の一つです。適切な依存関係管理により、セキュリティリスクの最小化、予測可能なビルド、効率的なメンテナンスが実現します。

**Statistics:**
- 平均的なNode.jsプロジェクト: 1,200+ の依存関係
- セキュリティ脆弱性の70%: サードパーティ依存関係から発生
- 適切な依存関係管理により、年間$500K-$5Mのコスト削減が可能

## 📚 公式ドキュメント・参考リソース

**このガイドで学べること**: パッケージマネージャーの選定、バージョン管理戦略、セキュリティ脆弱性対応、自動化設定
**公式で確認すべきこと**: 最新のパッケージバージョン、セキュリティアップデート、新機能、非推奨機能

### 主要な公式ドキュメント

- **[npm Documentation](https://docs.npmjs.com/)** - Node.jsのデフォルトパッケージマネージャー
  - [package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)
  - [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)

- **[pnpm Documentation](https://pnpm.io/)** - 高速で効率的なパッケージマネージャー
  - [Workspaces](https://pnpm.io/workspaces)
  - [CLI Commands](https://pnpm.io/cli/install)

- **[Swift Package Manager Guide](https://www.swift.org/package-manager/)** - Swift公式パッケージマネージャー
  - [Package Manifest](https://www.swift.org/package-manager/)

- **[Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)** - 自動依存関係更新
  - [Configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)

### 関連リソース

- **[Snyk Learn](https://learn.snyk.io/)** - セキュリティ脆弱性対策
- **[Renovate Documentation](https://docs.renovatebot.com/)** - 自動依存関係更新ツール
- **[Semantic Versioning](https://semver.org/)** - バージョニング規約

---

## What This Skill Covers

### 1. Comprehensive Dependency Management
- Package manager comparison and selection (npm, yarn, pnpm, Poetry, SPM, CocoaPods)
- Lock file strategies and best practices
- Semantic Versioning deep dive
- Dependency resolution algorithms
- Monorepo dependency management
- Private package registries
- Dependency auditing workflows
- License compliance

### 2. Security & Vulnerability Management
- Understanding security vulnerabilities (CVE, CVSS)
- Vulnerability scanning tools (npm audit, Snyk, Dependabot, OWASP)
- Automated security updates
- Dependency pinning strategies
- Supply chain attack prevention
- SBOM (Software Bill of Materials)
- Security policies and workflows
- Incident response procedures
- Real-world security case studies

### 3. Dependency Optimization & Maintenance
- Bundle size optimization techniques
- Tree shaking and dead code elimination
- Dependency update strategies
- Breaking change management
- Automated dependency updates (Renovate, Dependabot)
- Deprecation handling
- Technical debt management
- Migration guides for major updates
- Performance monitoring

## Quick Start

### Daily Tasks (Automated)
```bash
# Security monitoring
npm audit
snyk test

# Review automated PRs
# - Dependabot security alerts
# - Renovate update PRs
```

### Weekly Tasks
```bash
# Update patch versions
npm update

# Review outdated packages
npm outdated

# Clean unused dependencies
npx depcheck
```

### Monthly Tasks
```bash
# Update minor versions
npm update --save

# Generate reports
npm audit --json > reports/audit.json
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# License compliance
npx license-checker --failOn "GPL;AGPL"
```

### Quarterly Tasks
```bash
# Major version updates (planned)
npm outdated
# Review migration guides
# Plan updates

# Technical debt assessment
# Dependency health report
```

## Comprehensive Guides

### [Guide 1: Comprehensive Dependency Management](./guides/01-comprehensive-dependency-management.md)
**38,206 characters** - Complete guide covering:
- Package manager deep dive (npm, yarn, pnpm, SPM, CocoaPods, Poetry, Go)
- Lock file strategies
- Semantic Versioning mastery
- Dependency resolution algorithms
- Monorepo dependency management
- Private package registries
- Dependency auditing
- License compliance
- Real-world case studies (left-pad, event-stream, etc.)

### [Guide 2: Security & Vulnerability Management](./guides/02-security-vulnerability-management.md)
**47,074 characters** - Security-focused guide covering:
- Understanding security vulnerabilities (RCE, XSS, Prototype Pollution, etc.)
- CVE scoring system (CVSS)
- Vulnerability scanning tools (npm audit, Snyk, GitHub Dependabot, OWASP)
- Automated security updates
- Dependency pinning strategies
- Supply chain attack prevention
- SBOM generation and management
- Security policies and workflows
- Incident response playbooks
- Real-world security case studies (Log4Shell, event-stream, colors/faker, ua-parser-js)

### [Guide 3: Dependency Optimization & Maintenance](./guides/03-dependency-optimization-maintenance.md)
**39,758 characters** - Optimization guide covering:
- Bundle size optimization (webpack-bundle-analyzer, code splitting)
- Tree shaking and dead code elimination
- Dependency update strategies
- Breaking change management
- Automated dependency updates (Renovate advanced configuration)
- Deprecation handling and migration
- Technical debt management
- Migration guides (React 17→18, Next.js 13→14, Webpack 4→5)
- Performance monitoring

## Templates & Configurations

### Automation Templates
- **[Dependabot Configuration](./templates/dependabot.yml)** - Complete `.github/dependabot.yml` template with all ecosystems
- **[Renovate Configuration](./templates/renovate.json)** - Advanced Renovate Bot configuration
- **[Auto-Merge Workflow](./templates/auto-merge-workflow.yml)** - GitHub Actions for automatic PR merging
- **[npm Configuration](./templates/.npmrc)** - Production-ready `.npmrc` with security settings

### Checklists
- **[Dependency Audit Checklist](./checklists/dependency-audit-checklist.md)** - Before adding dependencies, weekly/monthly/quarterly reviews
- **[Security Checklist](./checklists/security-checklist.md)** - Daily/weekly/monthly security tasks, incident response

## Best Practices Summary

### Package Manager Selection

**JavaScript/TypeScript:**
- 🥇 **pnpm** - Best performance, strict dependency resolution, disk efficiency
- 🥈 **npm** - Default, stable, widely supported
- 🥉 **yarn** - Good for monorepos, Plug'n'Play mode

**iOS/Swift:**
- 🥇 **Swift Package Manager** - Official, modern, Xcode integrated
- 🥈 **CocoaPods** - Mature, legacy support

**Python:**
- 🥇 **Poetry** - Modern, excellent dependency resolution
- 🥈 **pip** - Simple, traditional approach

### Version Pinning Strategy

```json
{
  "dependencies": {
    // Critical packages: exact versions
    "react": "18.2.0",

    // Important packages: patch updates only
    "lodash": "~4.17.21",

    // Low-risk packages: minor updates allowed
    "axios": "^1.6.0"
  },
  "devDependencies": {
    // Dev tools: flexible updates
    "typescript": "^5.3.0"
  }
}
```

### Security Best Practices

1. **Enable Automated Scanning**
   - GitHub Dependabot
   - Snyk
   - npm audit in CI/CD

2. **Response Times**
   - Critical vulnerabilities: < 24 hours
   - High vulnerabilities: < 48 hours
   - Medium vulnerabilities: < 1 week

3. **Supply Chain Protection**
   - Use lock files (always commit)
   - Private registry proxy
   - Package verification
   - SBOM generation

### Update Strategy

| Update Type | Frequency | Automation | Review |
|------------|-----------|------------|--------|
| Security patches | Immediate | ✅ Auto-merge | Minimal |
| Patch (x.x.PATCH) | Weekly | ✅ Auto-merge | CI only |
| Minor (x.MINOR.x) | Monthly | ⚠️ Manual merge | Code review |
| Major (MAJOR.x.x) | Quarterly | ❌ Manual | Full review |

## Essential Tools

### Security
- npm audit (built-in)
- Snyk (comprehensive)
- GitHub Dependabot (native)
- Socket.dev (supply chain)
- OWASP Dependency-Check

### Automation
- Renovate (advanced features)
- Dependabot (GitHub native)

### Analysis
- webpack-bundle-analyzer
- bundlephobia.com
- depcheck
- npm-check-updates

### Compliance
- license-checker
- SBOM generators (CycloneDX, SPDX)
- Dependency-Track

## Metrics & KPIs

Track these metrics for dependency health:

### Security Metrics
- Vulnerability count (Critical/High/Medium/Low)
- Mean time to detect (MTTD)
- Mean time to remediate (MTTR)
- Security scan success rate

**Target:** 0 critical/high vulnerabilities, MTTR < 7 days

### Dependency Metrics
- Total dependency count
- Outdated percentage
- Average dependency age
- Deprecated package count

**Target:** < 5% outdated, < 200 total dependencies

### Performance Metrics
- Bundle size (gzipped)
- Build time
- Install time

**Target:** < 200KB initial bundle, < 2min builds

### Process Metrics
- Automated update success rate
- Manual review time
- Breaking change incidents

**Target:** > 80% auto-merge, < 1 incident/month

## Common Patterns

### Pattern 1: Security-First Approach
```yaml
# Immediate security updates
- Daily vulnerability scans
- Auto-merge security patches
- 24-hour response for critical CVEs
- Monthly security audit reports
```

### Pattern 2: Stability-First Approach
```yaml
# Controlled updates
- Lock all production dependencies
- Manual review for all updates
- Staging deployment before production
- Quarterly update cycles
```

### Pattern 3: Innovation-First Approach
```yaml
# Stay current
- Daily dependency updates
- Auto-merge minor updates
- Beta testing of new versions
- Monthly major version evaluations
```

## Troubleshooting

### Problem: Build Failures After Update

**Symptoms:** Tests fail, TypeScript errors, runtime errors

**Solutions:**
1. Check breaking changes in changelog
2. Review migration guide
3. Use codemod tools for automated migration
4. Rollback and plan migration
5. Pin problematic dependency temporarily

### Problem: Security Vulnerabilities in Transitive Dependencies

**Symptoms:** npm audit shows vulnerabilities you don't directly use

**Solutions:**
1. Update parent dependency
2. Use `npm audit fix --force` (carefully)
3. Use `overrides` (npm 8.3+) or `resolutions` (yarn)
4. Contact package maintainer
5. Find alternative package

### Problem: Dependency Conflicts

**Symptoms:** "Cannot resolve dependency", version conflicts

**Solutions:**
1. Use `npm ls <package>` to see dependency tree
2. Use `overrides`/`resolutions` to force version
3. Update conflicting packages
4. Consider alternative packages

## Related Skills

- [ios-project-setup](../ios-project-setup/SKILL.md) - Project initialization
- [ci-cd-automation](../ci-cd-automation/SKILL.md) - CI/CD pipelines
- [ios-security](../ios-security/SKILL.md) - Security practices
- [web-development](../web-development/SKILL.md) - Web development
- [react-development](../react-development/SKILL.md) - React patterns
- [nextjs-development](../nextjs-development/SKILL.md) - Next.js patterns

## Quick Reference Commands

### npm
```bash
npm install              # Install dependencies
npm ci                   # Clean install (CI/CD)
npm update              # Update patch versions
npm outdated            # Show outdated packages
npm audit               # Security audit
npm audit fix           # Auto-fix vulnerabilities
npx depcheck           # Find unused dependencies
npx npm-check-updates   # Check all updates
```

### Yarn
```bash
yarn install                      # Install
yarn upgrade                      # Update
yarn audit                        # Security audit
yarn outdated                     # Check outdated
yarn install --frozen-lockfile    # CI/CD
```

### pnpm
```bash
pnpm install                      # Install
pnpm update                       # Update
pnpm audit                        # Security audit
pnpm outdated                     # Check outdated
pnpm install --frozen-lockfile    # CI/CD
```

### Security Tools
```bash
snyk test                         # Snyk security scan
npx socket-cli audit              # Socket.dev scan
npx @cyclonedx/cyclonedx-npm      # Generate SBOM
npx license-checker               # License check
```

## Version History

- **2025-01-03**: Complete overhaul to 🟢 High status
  - Added 3 comprehensive guides (125,000+ total characters)
  - Created automation templates (Dependabot, Renovate, CI/CD)
  - Added comprehensive checklists
  - Expanded to cover all major package managers
  - Added real-world case studies
  - Included security best practices
  - Added performance optimization techniques

- **2024-12-24**: Initial version (📝 Basic status)
  - Basic package manager coverage
  - Simple version management guidelines

---

**Maintained by:** Development Team
**Last Updated:** 2025-01-03
**Status:** 🟢 High (100% complete)
