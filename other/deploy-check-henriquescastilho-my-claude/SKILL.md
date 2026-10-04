---
name: deploy-check
description: Pre-deploy validation checklist. Use automatically before any deploy, push to production, or when the user says "deploy", "publica", "manda pra prod". Run to catch issues before they reach production.
allowed-tools: Bash Read Grep Glob
context: fork
agent: deployer
---

Run the full deploy readiness check for this project.

1. Detect the deploy target (Railway/Vercel/GCP) from config files
2. Check git status for uncommitted files
3. Run type-check, lint, build, and tests
4. Check for security vulnerabilities in dependencies
5. Verify environment variables
6. Output a GO/NO-GO verdict with any blockers listed
