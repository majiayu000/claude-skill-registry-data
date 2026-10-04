---
name: skill-github-pblctn
description: >
  Clean and publish Hermes Agent skills to GitHub.
  Security checks, sensitive info removal, repo setup.
tags: [skills, github, publication, security]
---

## When to use
- User says "publish skills to GitHub"
- User says "整理 skill" or "清理 skill"
- Preparing skills for public release

## Security checks (MANDATORY before publish)

### Sensitive patterns to scan
```bash
cd ~/.hermes/skills
grep -r "thrill3r\|tabb_\|a3c2af53\|ghp_\|sk-" --include="SKILL.md" -l
```

### What to clean
1. **User paths**: `~/` → `~/` or `$(which hermes)`
2. **Partial API keys**: `tabb_3...3FWg` → remove entirely
3. **Agent IDs**: `a3c2af53-...` → remove
4. **GitHub tokens**: `ghp_...` → check if example or real
5. **OpenAI keys**: `sk-...` → check if example or real
6. **Feishu URLs**: `https://xxx.feishu.cn/docx/...` → replace with `<your-doc-url>`
7. **API response parsing**: Use `json.loads(text, strict=False)` or regex cleanup for control chars

### What's OK to keep
- `config.json` references (generic path)
- Example tokens like `sk-xxx...xxxx` or `ghp_xx...xxxx`
- Regex patterns that match tokens (for detection)

## Category-based organization (recommended for 50+ skills)

### Structure
```
repo/
├── README.md
├── categories/
│   ├── agent-automation/     # agent, cron, autonomous
│   ├── browser-automation/   # browser, computer-use
│   ├── crypto-security/      # security, blockchain
│   ├── data-pipeline/        # data, ETL, analytics
│   ├── development/          # code, debug, testing
│   └── research/             # paper, analysis, synthesis
└── .gitignore
```

### Category mapping
```python
CATEGORY_KEYWORDS = {
    "agent-automation": ["agent", "cron", "autonomous", "hermes"],
    "browser-automation": ["browser", "computer-use", "selenium", "playwright"],
    "crypto-security": ["security", "crypto", "blockchain", "cryptography"],
    "data-pipeline": ["data", "etl", "pipeline", "analytics", "database"],
    "development": ["code", "debug", "test", "git", "github", "python", "rust"],
    "research": ["paper", "research", "analysis", "synthesis", "academic"]
}
```

### Multi-repo strategy
For 100+ skills, consider separate repos per category:
- `hermes-skills-dev` → development, testing, CI/CD
- `hermes-skills-automation` → agents, cron, browser
- `hermes-skills-security` → crypto, pentest, forensics
- `hermes-skills-research` → papers, analysis, synthesis

## Publication steps

### 1. Decide: existing repo vs new repo
First inspect whether the asset already has a local git repo / remote.
```bash
git -C <repo> remote -v
git -C <repo> status --short --branch
```
If the repo already exists:
- do not re-init
- do not create a second public repo
- sync the live script/artifact into the repo tree first
- commit and push the existing repo

If no repo exists yet, create one:
```bash
gh repo create <name> --public --description "<description>"
```

### 2. Copy skills or live artifacts into the publish repo
```bash
cd /tmp/<repo>
mkdir -p skills
cp -r ~/.hermes/skills/* skills/
```
For script-pack repos, compare the live working script against the repo copy before publishing:
```bash
cmp -s /path/to/live.user.js /path/to/repo/scripts/tool.user.js || echo DIFF
```
If `DIFF`, update the repo copy before commit so the public repo matches the validated live script.

Also remove trivial macOS junk before commit:
```bash
find . -name '.DS_Store' -delete
```

### 3. Handle embedded git repos
```bash
# Check for nested repos
find skills -name ".git" -type d

# Remove from index and add to .gitignore
git rm --cached <path>
echo "<path>" >> .gitignore
git add .gitignore
```

### 4. Create README
Include:
- Installation instructions
- Category table with counts
- Skill format documentation
- License
- For bilingual public repos, default to English `README.md` and add `README.zh-CN.md` as the secondary document unless the user asks otherwise

### 4.5 Single-skill/script pack pattern
For a public repo that packages one polished script plus one reusable skill, prefer this minimal layout:
```text
repo/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── docs/plan.md
├── scripts/<tool>.user.js
└── skills/<skill-name>/SKILL.md
```
Use this when the goal is agent retrieval, copy-safe reuse, and one-shot publication rather than a large multi-skill catalog.

Before publish, also sanitize planning docs and examples so they do not leak local absolute paths even if the code is clean.

### 5. Push
```bash
git add .
git commit -m "Add skills"
git push origin main
```

## Pitfalls
- **Embedded git repos**: Skills may contain cloned repos (e.g., anthropic-cybersecurity-skills). Must remove from index and use .gitignore.
- **File permissions**: Skills are 600 (owner-only). GitHub doesn't preserve permissions.
- **Large repos**: 900+ skills can be large. Consider splitting by category if needed.
- **Real secrets**: Always scan before publish. Use `grep -r` with multiple patterns.