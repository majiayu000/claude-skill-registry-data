---
name: deployment
description: Deploy applications, configure cloud hosting targets (Vercel, Netlify,
  GitHub Pages, S3), manage build pipelines, and verify post-deployment health. Trigger
  with "deploy app", "publish release", "setup hosting", or when configuring production
  rollout workflows.
argument-hint: <target platform or service>
---

<!-- Generated from skills/deployment.md by tools/generate_integrations.py. Edit the source file, not this one. -->

# Skill: Deployment

## Purpose
Deploy applications, expose services, and manage release workflows. _Source: Factory (Category O)_

## Tools Required
- Deployment CLI tools (Netlify, Vercel, gh-pages, etc.) _Source: Factory (Category O)_
- Shell commands _Source: Manus (Category F)_
- Port exposure tools _Source: Manus (Category P)_

## General Principles
- Read deployment config before attempting to deploy _Source: Cursor (Category E)_
- Ensure all required files exist before deployment _Source: Factory (Category P)_
- Verify build succeeds before deploy _Source: Factory (Category O)_
- Check deployment status after deploying _Source: Factory (Category O)_
- NEVER auto-deploy to production without user confirmation _Source: Cursor (Category G)_

## Deployment Workflow

### Pre-Deployment Checklist
- [ ] Read deployment configuration (if exists) _Source: Cursor (Category E)_
- [ ] Verify all source files are present _Source: Factory (Category P)_
- [ ] Build succeeds locally _Source: Factory (Category O)_
- [ ] Environment variables configured _Source: Factory (Category P)_
- [ ] Required service accounts / API keys available _Source: Factory (Category P)_

### Common Platforms

| Platform | Tool | Setup |
|----------|------|-------|
| GitHub Pages | `gh-pages` package or Actions | Push to gh-pages branch _Source: Factory (Category O)_ |
| Netlify | Netlify CLI / manual | Connect repo + configure build _Source: Factory (Category O)_ |
| Vercel | Vercel CLI | `vercel` for project setup _Source: V0 (Category A)_ |
| Static hosting | rsync / scp / s3 | Copy build output to host _Source: Factory (Category O)_ |

### Deployment Steps
1. Build the project _Source: Factory (Category O)_
2. If deploying new site: use project_id empty _Source: Factory (Category O)_
3. If updating existing site: use existing project_id _Source: Factory (Category O)_
4. Run deploy command _Source: Factory (Category O)_
5. Check deployment status _Source: Factory (Category O)_
6. Provide access URL to user _Source: Factory (Category O)_

## Service Exposure (Manus pattern)
- For temporary services: expose local ports _Source: Manus (Category P)_
- For permanent services: deploy to cloud hosting _Source: Factory (Category O)_
- Provide access links after deployment _Source: Factory (Category O)_
- Monitor deployed applications _Source: Factory (Category O)_

## PR/MR Workflow (Factory pattern)
For implementation tasks in collaborative projects: _Source: Factory (Category O)_
1. Create feature branch from updated main _Source: Factory (Category O)_
2. Make changes _Source: Factory (Category O)_
3. Commit with descriptive message _Source: Factory (Category O)_
4. Push branch _Source: Factory (Category O)_
5. Create Pull/Merge Request _Source: Factory (Category O)_
6. Include summary of changes in PR description _Source: Factory (Category O)_

## Environment Configuration
- Use environment variables for config _Source: Factory (Category P)_
- Provide .env.example file with placeholder values _Source: Factory (Category P)_
- Document required environment variables _Source: Factory (Category P)_
- Never commit real secrets to version control _Source: Kiro (Category E)_

## Rollback
- Know how to roll back a deployment _Source: Factory (Category O)_
- For git-based deploys: revert commit and redeploy _Source: Factory (Category O)_
- For platform deploys: use platform's rollback feature _Source: Factory (Category O)_
- Always keep previous deployment artifacts _Source: Factory (Category O)_
