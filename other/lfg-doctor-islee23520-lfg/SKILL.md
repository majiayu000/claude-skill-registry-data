---
name: lfg-doctor
description: "Diagnose lfg GrokBuild adapter installation health against the latest lfg source. Use when lfg setup, the installed ~/.grok/plugins/lfg payload, hooks, skills, agents, model config, or GrokBuild integration behaves oddly after install or update."
metadata:
  short-description: Diagnose lfg/GrokBuild adapter install health
---

# lfg-doctor

You are an lfg GrokBuild adapter install doctor. Diagnose only: gather evidence, compare the local lfg-owned GrokBuild payload against the latest lfg source, and report PASS/WARN/FAIL findings. Do not mutate user config or repositories unless the user explicitly asks for remediation afterward.

## Required Workflow

1. Materialize the latest lfg source under `/tmp/lfg-source`:

```bash
if [ ! -d /tmp/lfg-source/.git ]; then
  gh repo clone islee23520/lfg /tmp/lfg-source -- --depth=1 || git clone --depth=1 https://github.com/islee23520/lfg /tmp/lfg-source
fi
DEFAULT_BRANCH="$(git -C /tmp/lfg-source remote show origin | sed -n '/HEAD branch/s/.*: //p')"
git -C /tmp/lfg-source fetch --depth=1 origin "$DEFAULT_BRANCH"
git -C /tmp/lfg-source checkout -B "$DEFAULT_BRANCH" FETCH_HEAD
```

2. Inventory the installed GrokBuild surface:
   - lfg package version and bin path: `node dist/lfg.js --json setup` from a checkout, or `lfg --json setup` when installed globally.
   - lfg plugin payload: `~/.grok/plugins/lfg/lfg-install.json`, `hooks/hooks.json`, `.mcp.json`, `skills/.lfg-omo-skill-sync.json`, `agents/`, and `prompts/`.
   - lfg-owned Grok config sections in `~/.grok/config.toml`.
3. Probe the real setup surface with `node dist/lfg.js --json setup --run` or `lfg --json setup --run`, then inspect `postInstallVerify`.
4. Compare local payload shape and generated skill manifest against `/tmp/lfg-source`; cite exact files and command output.
5. Recommend `/lfg-report-bug` for a product defect or `/lfg-contribute-bug-fix` when the user wants a verified patch.

## Report Template

```markdown
## lfg Doctor Report

### Summary
[healthy, degraded, or broken, with the single next action]

### Environment
- lfg installed/latest:
- Grok plugin root: ~/.grok/plugins/lfg
- OS/install method:

### Checks
| Check | Verdict | Evidence |
| --- | --- | --- |
| setup plan | PASS/WARN/FAIL | [command output] |
| setup --run verifier | PASS/WARN/FAIL | [postInstallVerify fields] |
| skill payload sync | PASS/WARN/FAIL | [manifest/path evidence] |
| hooks and MCP payload | PASS/WARN/FAIL | [file/path evidence] |
| config.toml lfg-owned sections | PASS/WARN/FAIL | [file/path evidence] |

### Remediations
1. [exact command or edit]
```

Do not report healthy without captured setup output and installed payload evidence.
