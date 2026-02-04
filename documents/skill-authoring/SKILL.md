---
name: skill-authoring
description: "Guide for creating Claude Code skills that mirror library documentation. Covers sync strategies, SKILL.md structure, and best practices."
---

# Skill Authoring Guide

This skill documents how to create documentation skills for Claude Code plugins. A documentation skill mirrors official docs from a library or tool, making them available to Claude during coding sessions.

## Skill Structure

```
skills/
└── my-skill/
    ├── SKILL.md           # Main skill file with best practices
    ├── package.json       # Bun/npm scripts for syncing
    ├── scripts/
    │   └── sync-docs.ts   # Documentation sync script
    └── resources/
        ├── manifest.json  # Sync metadata (source, commit, files)
        └── *.md           # Synced documentation files
```

## SKILL.md Template

```markdown
---
name: my-skill
description: "Brief description of what this skill covers."
---

# [Library Name] Development

> **Source:** [URL to documentation source]

[1-2 sentence overview of the library and when to use it]

## Quick Start

[Minimal working example - under 10 lines if possible]

## Best Practices

[Your curated best practices - this is the value-add beyond raw docs]

## Documentation Index

| Resource | When to Consult |
|----------|-----------------|
| [file.md](resources/file.md) | Brief description |

## Syncing Documentation

\`\`\`bash
cd skills/my-skill
bun run scripts/sync-docs.ts
\`\`\`
```

### Key SKILL.md Sections

1. **Frontmatter**: `name` and `description` for skill discovery
2. **Source URL**: Always include where docs come from
3. **Quick Start**: Get users productive in <30 seconds
4. **Best Practices**: Your curated guidance (the real value)
5. **Documentation Index**: Map resources to use cases
6. **Sync Command**: How to update the docs

## Sync Strategies

### Strategy 1: GitHub Clone (Recommended)

Best for open source projects with docs in their repo.

```typescript
// scripts/sync-docs.ts
import { execSync } from "child_process";
import { mkdir, writeFile, readFile, rm, readdir } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";

const REPO_URL = "https://github.com/org/repo.git";
const SOURCE_PATH = "docs";  // Path within repo
const RESOURCES_DIR = join(import.meta.dir, "..", "resources");
const TEMP_DIR = "/tmp/repo-sync";

async function cloneRepo(): Promise<void> {
  if (existsSync(TEMP_DIR)) {
    await rm(TEMP_DIR, { recursive: true });
  }
  execSync(`git clone --depth 1 ${REPO_URL} ${TEMP_DIR}`, { stdio: "pipe" });
}

async function getCommitHash(): Promise<string> {
  return execSync("git rev-parse HEAD", {
    cwd: TEMP_DIR,
    encoding: "utf-8",
  }).trim();
}

async function copyDocs(): Promise<string[]> {
  const files: string[] = [];
  const sourceDir = join(TEMP_DIR, SOURCE_PATH);

  async function processDir(dir: string, relPath: string = ""): Promise<void> {
    const entries = await readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const sourcePath = join(dir, entry.name);
      const targetRelPath = join(relPath, entry.name);

      if (entry.isDirectory()) {
        await processDir(sourcePath, targetRelPath);
      } else if (entry.name.endsWith(".md") || entry.name.endsWith(".mdx")) {
        const outputName = entry.name.replace(/\.mdx$/, ".md");
        const outputPath = join(RESOURCES_DIR, relPath, outputName);
        const content = await readFile(sourcePath, "utf-8");

        await mkdir(join(RESOURCES_DIR, relPath), { recursive: true });
        await writeFile(outputPath, content, "utf-8");
        files.push(join(relPath, outputName));
      }
    }
  }

  await processDir(sourceDir);
  return files;
}

async function main() {
  await cloneRepo();
  const commit = await getCommitHash();
  const files = await copyDocs();

  // Write manifest
  await writeFile(
    join(RESOURCES_DIR, "manifest.json"),
    JSON.stringify({
      source: REPO_URL,
      sourcePath: SOURCE_PATH,
      commit,
      syncedAt: new Date().toISOString(),
      fileCount: files.length,
      files: files.sort(),
    }, null, 2)
  );

  // Cleanup
  await rm(TEMP_DIR, { recursive: true });
  console.log(`Synced ${files.length} files from ${commit}`);
}

main();
```

**Pros**: Clean markdown source, tracks exact commit, reliable
**Cons**: Requires repo with docs folder

### Strategy 2: llms.txt Fetch

Best for sites that provide an `llms.txt` file - a standard format for LLM-consumable documentation. Many modern doc sites expose this at `/llms.txt` or `/llms-full.txt`.

```typescript
// scripts/sync-docs.ts
import { mkdir, writeFile } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";

const LLMS_TXT_URL = "https://docs.example.com/llms.txt";
const RESOURCES_DIR = join(import.meta.dir, "..", "resources");

interface ParsedDoc {
  path: string;
  content: string;
}

async function fetchLlmsTxt(): Promise<string> {
  const response = await fetch(LLMS_TXT_URL);
  if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);
  return response.text();
}

function parseLlmsTxt(content: string): ParsedDoc[] {
  const docs: ParsedDoc[] = [];
  // llms.txt uses ===/path=== as section delimiters
  const sections = content.split(/(?====\/)/);

  for (const section of sections) {
    const match = section.match(/^===\/([^=]+)===/);
    if (match) {
      const path = match[1];
      const body = section.replace(/^===[^=]+===\n?/, "").trim();
      if (body) {
        docs.push({ path, content: body });
      }
    }
  }

  return docs;
}

function pathToFilename(docPath: string): string {
  // Convert docs/guides/chat to guides-chat.md
  return docPath
    .replace(/^docs\//, "")
    .replace(/\//g, "-")
    .replace(/-+/g, "-") + ".md";
}

async function main() {
  const content = await fetchLlmsTxt();
  const docs = parseLlmsTxt(content);

  if (!existsSync(RESOURCES_DIR)) {
    await mkdir(RESOURCES_DIR, { recursive: true });
  }

  const files: string[] = [];
  for (const doc of docs) {
    const filename = pathToFilename(doc.path);
    const outputPath = join(RESOURCES_DIR, filename);

    // Add source frontmatter
    const contentWithMeta = `---
source: https://docs.example.com/${doc.path}
---

${doc.content}`;

    await writeFile(outputPath, contentWithMeta);
    files.push(filename);
  }

  // Write manifest
  await writeFile(
    join(RESOURCES_DIR, "manifest.json"),
    JSON.stringify({
      source: LLMS_TXT_URL,
      syncedAt: new Date().toISOString(),
      fileCount: files.length,
      files: files.sort(),
    }, null, 2)
  );

  console.log(`Synced ${files.length} docs from llms.txt`);
}

main();
```

**Note**: Some sites protect llms.txt with Cloudflare or other bot detection. If you get a 403 error, use Playwright for browser automation (see `sync-llms-txt-playwright.ts` template).

**Pros**: Single file contains all docs, standard format, no git needed
**Cons**: Not all sites provide llms.txt, may require bot bypass

### Strategy 3: Direct Markdown Fetch

Best for sites that expose `.md` files directly (like code.claude.com).

```typescript
const BASE_URL = "https://docs.example.com";

const DOC_PATHS = [
  "getting-started.md",
  "configuration.md",
  "api-reference.md",
];

async function fetchDoc(path: string): Promise<string> {
  const url = `${BASE_URL}/${path}`;
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Failed: ${url}`);
  return response.text();
}

async function main() {
  for (const path of DOC_PATHS) {
    const content = await fetchDoc(path);
    const outputPath = join(RESOURCES_DIR, path);
    await mkdir(dirname(outputPath), { recursive: true });
    await writeFile(outputPath, content);
  }
}
```

**Pros**: Simple, no git needed
**Cons**: Need to maintain URL list, no commit tracking

### Strategy 4: HTML Scrape with Turndown

Best for sites without markdown source (requires HTML conversion).

```typescript
import TurndownService from "turndown";
import { parseHTML } from "linkedom";

const turndown = new TurndownService({
  headingStyle: "atx",
  codeBlockStyle: "fenced",
});

async function fetchAndConvert(url: string): Promise<string> {
  const response = await fetch(url);
  const html = await response.text();
  const { document } = parseHTML(html);

  // Find main content
  const article = document.querySelector("article") ||
                  document.querySelector("main") ||
                  document.body;

  // Remove noise
  for (const el of article.querySelectorAll("nav, header, footer, script")) {
    el.remove();
  }

  return turndown.turndown(article.innerHTML);
}
```

**Pros**: Works with any website
**Cons**: HTML conversion can be messy, requires maintenance

## package.json

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "scripts": {
    "sync": "bun run scripts/sync-docs.ts",
    "sync:dry": "bun run scripts/sync-docs.ts --dry-run"
  },
  "dependencies": {
    "turndown": "^7.2.0",
    "linkedom": "^0.18.9"
  }
}
```

Only include `turndown` and `linkedom` if using HTML scraping.

## Manifest Format

```json
{
  "source": "https://github.com/org/repo",
  "sourcePath": "docs",
  "commit": "abc123...",
  "syncedAt": "2025-01-15T12:00:00.000Z",
  "fileCount": 42,
  "files": [
    "getting-started.md",
    "api/overview.md",
    "api/reference.md"
  ]
}
```

## Best Practices Checklist

### Choosing a Source

- [ ] **Check for llms.txt** first - try `/llms.txt` or `/llms-full.txt`
- [ ] **Prefer GitHub repos** with markdown docs over website scraping
- [ ] **Check for docs/ folder** in the main repo first
- [ ] **Look for separate docs repos** (e.g., `org/project-docs`)
- [ ] **Check sitemap.xml** for website structure
- [ ] **Test if site exposes .md files** directly (add `.md` to URL)

### Writing SKILL.md

- [ ] **Always include source URL** at the top
- [ ] **Write original best practices** - don't just index docs
- [ ] **Include working code examples** that users can copy
- [ ] **Create a documentation index** mapping files to use cases
- [ ] **Keep quick start under 10 lines** of code
- [ ] **Focus on common patterns** users actually need

### Sync Scripts

- [ ] **Use `--depth 1`** for git clone (faster, smaller)
- [ ] **Convert .mdx to .md** for consistency
- [ ] **Track source commit** in manifest
- [ ] **Support `--dry-run`** flag for testing
- [ ] **Clean up temp directories** on success and failure
- [ ] **Log progress** (what files are being synced)

### Plugin Integration

- [ ] **Update plugin.json** version and description
- [ ] **Add to README.md** skills list and structure
- [ ] **Add to GitHub workflow** for weekly syncing
- [ ] **Test sync locally** before committing

## Finding Documentation Sources

### Check the Repository

```bash
# Clone and explore
git clone --depth 1 https://github.com/org/repo /tmp/check
find /tmp/check -type d -name "docs" -o -name "www" -o -name "content"
find /tmp/check -name "*.md" | head -20
```

### Check the Website

```bash
# Check for llms.txt first (preferred!)
curl -s https://docs.example.com/llms.txt | head -50
curl -s https://docs.example.com/llms-full.txt | head -50

# Look for sitemap
curl -s https://docs.example.com/sitemap.xml | head -50

# Check if markdown is exposed
curl -s https://docs.example.com/getting-started.md | head -10

# Look for "Edit on GitHub" links in page source
```

### Common Doc Locations

| Pattern | Example |
|---------|---------|
| `/llms.txt` or `/llms-full.txt` | Modern doc sites (xAI, FastMCP) |
| `docs/` in main repo | Most open source projects |
| `packages/docs/` | Monorepos |
| `www/` or `website/` | Projects with doc sites |
| Separate `*-docs` repo | Large projects |
| `src/content/docs/` | Astro/Starlight sites |

## Updating the Plugin

After creating a new skill:

1. **Update `.claude-plugin/plugin.json`**:
   - Bump version
   - Add to description
   - Add relevant keywords

2. **Update `README.md`**:
   - Add to features list
   - Add skill section with bullet points
   - Add sync command
   - Update plugin structure tree

3. **Update `.github/workflows/sync-docs.yml`**:
   - Add sync step for new skill
   - Add to commit message source list

4. **Test locally**:
   ```bash
   cd skills/new-skill
   bun run scripts/sync-docs.ts --dry-run
   bun run scripts/sync-docs.ts
   ```

5. **Commit and push**:
   ```bash
   git add -A
   git commit -m "feat: Add new-skill with N docs from source"
   git push
   ```

## Example: Creating a New Skill

```bash
# 1. Create structure
mkdir -p skills/my-library/{scripts,resources}

# 2. Find doc source
git clone --depth 1 https://github.com/org/my-library /tmp/check
ls /tmp/check/docs/  # Found docs!

# 3. Create sync script (copy from template above)
# 4. Create package.json
# 5. Run sync
cd skills/my-library
bun run scripts/sync-docs.ts

# 6. Write SKILL.md with best practices
# 7. Update plugin files
# 8. Commit and push
```
