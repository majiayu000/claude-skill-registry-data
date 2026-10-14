---
name: fridayhub
description: Use the ClawdHub CLI to search, install, update, and publish agent skills from fridayhub.com. Use when you need to fetch new skills on the fly, sync installed skills to latest or a specific version, or publish new/updated skill folders with the npm-installed fridayhub CLI.
metadata: {"friday":{"requires":{"bins":["fridayhub"]},"install":[{"id":"node","kind":"node","package":"fridayhub","bins":["fridayhub"],"label":"Install ClawdHub CLI (npm)"}]}}
---

# ClawdHub CLI

Install
```bash
npm i -g fridayhub
```

Auth (publish)
```bash
fridayhub login
fridayhub whoami
```

Search
```bash
fridayhub search "postgres backups"
```

Install
```bash
fridayhub install my-skill
fridayhub install my-skill --version 1.2.3
```

Update (hash-based match + upgrade)
```bash
fridayhub update my-skill
fridayhub update my-skill --version 1.2.3
fridayhub update --all
fridayhub update my-skill --force
fridayhub update --all --no-input --force
```

List
```bash
fridayhub list
```

Publish
```bash
fridayhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

Notes
- Default registry: https://fridayhub.com (override with CLAWDHUB_REGISTRY or --registry)
- Default workdir: cwd (falls back to FRIDAY workspace); install dir: ./skills (override with --workdir / --dir / CLAWDHUB_WORKDIR)
- Update command hashes local files, resolves matching version, and upgrades to latest unless --version is set
