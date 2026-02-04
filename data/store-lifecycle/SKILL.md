---
name: store-lifecycle
description: Best practices for creating, indexing, and managing Bluera Knowledge stores. Covers when to use clone vs crawl vs folder, naming conventions, indexing strategies, storage management, background job monitoring, and handling indexing failures.
---

# Bluera Knowledge Store Lifecycle Management

Master the lifecycle of knowledge stores from creation to deletion, including best practices for naming, indexing, and maintenance.

## Choosing the Right Source Type

Bluera Knowledge supports three source types. Choose based on your content:

### Git Repositories (`add-repo` / `create_store` with git URL)

**✅ Use for:**
- Public library source code (React, Vue, Pydantic, etc.)
- Private repositories with auth
- Code you want to track and update
- Multi-file projects with git history

**Advantages:**
- Preserves git history
- Can pull updates (`git pull` in repo directory)
- Standard structure recognized by analyzers
- Automatic language detection

**Example:**
```
/bluera-knowledge:add-repo https://github.com/vuejs/core --name=vue

# Or via MCP:
create_store(
  source='https://github.com/vuejs/core',
  name='vue',
  type='repo'
)
```

**Best practices:**
- Use package/library name for consistency: `vue`, `fastapi`, `pydantic`
- For monorepos: `org-project` format: `microsoft-typescript`, `vercel-next`
- Include version if tracking specific release: `vue-3.4`, `python-3.11`

### Local Folders (`add-folder`)

**✅ Use for:**
- Private codebases not in git
- Work-in-progress code
- Local documentation
- Specific subdirectories of larger projects

**Advantages:**
- No git required
- Fast indexing (no clone step)
- Perfect for proprietary code
- Can index subset of larger repo

**Example:**
```
/bluera-knowledge:add-folder /path/to/my-project/api --name=my-api

# Or via MCP:
create_store(
  source='/Users/me/projects/my-app/backend',
  name='my-backend',
  type='folder'
)
```

**Best practices:**
- Use descriptive names: `my-api`, `auth-service`, `shared-utils`
- Index focused directories (not entire ~/ )
- Update by re-indexing: `/bluera-knowledge:index my-api`

### Web Documentation (`crawl`)

**✅ Use for:**
- Official documentation sites
- API references hosted online
- Tutorials and guides
- Content only available via web

**Advantages:**
- Access web-only content
- Handles JavaScript-rendered sites (headless mode)
- Follows links automatically
- Converts HTML to searchable text

**Example:**
```
/bluera-knowledge:crawl https://fastapi.tiangolo.com --name=fastapi-docs --max-pages=100

# Or via MCP:
create_store(
  source='https://fastapi.tiangolo.com',
  name='fastapi-docs',
  type='web',
  max_pages=100
)
```

**Best practices:**
- Append `-docs` to library name: `fastapi-docs`, `vue-docs`
- Set `max-pages` to avoid crawling entire internet
- Use `--headless` for JavaScript-heavy sites
- Crawl specific documentation paths, not marketing pages

## Naming Conventions

Good names make stores easy to find and filter.

### Recommended Patterns

**Library source code:**
```
vue          # Official package name
react
fastapi
pydantic
```

**Documentation sites:**
```
vue-docs
fastapi-docs
python-3.11-docs
```

**Organization/project format:**
```
microsoft-typescript
vercel-next
acme-payment-api      # Your company's code
```

**Versioned stores:**
```
vue-3.4
python-3.11
react-18
```

**Specialized content:**
```
coding-standards      # Company standards
api-spec-v2          # API specification
architecture-docs    # Design docs
```

### Naming Anti-Patterns

❌ Avoid:
- Generic names: `docs`, `code`, `library`
- Unclear abbreviations: `fp`, `lib1`, `proj`
- Dates without context: `2024-01-15`
- Redundant words: `my-project-library-code`

✅ Prefer:
- Specific, descriptive: `fastapi-docs`, `vue-source`
- Standard package names: `pydantic`, `lodash`
- Clear context: `api-spec-v2`, `coding-standards`

## Indexing Strategies

### Initial Indexing

When creating a store, indexing happens automatically in the background:

```
create_store(url, name)
→ Returns: job_id
→ Background: clone/download → analyze → index
→ Status: pending → running → completed

# Monitor progress
check_job_status(job_id)
→ Progress: 45% (processing src/core.ts)
→ Estimated: ~2 minutes remaining
```

**Indexing time estimates:**
- Small library (<1k files): 30-60 seconds
- Medium library (1k-5k files): 1-3 minutes
- Large library (>5k files): 3-10 minutes
- Documentation crawl (100 pages): 1-2 minutes

### Re-indexing (Updates)

When library code changes or you modify indexed content:

```
# For git repos: pull latest changes
cd .bluera/bluera-knowledge/repos/vue
git pull origin main
cd -

# Re-index
/bluera-knowledge:index vue

# Or via MCP:
index_store(store='vue')
→ Re-processes all files
→ Updates vector embeddings
→ Rebuilds search index
```

**When to re-index:**
- Library released new version
- You modified local folder content
- Search results seem outdated
- After significant codebase changes

**Re-indexing is incremental** - only changed files are re-processed.

### Selective Indexing

For large repos, you might want to index specific directories:

```
# Clone full repo manually
git clone https://github.com/microsoft/vscode
cd vscode

# Index only specific dirs
/bluera-knowledge:add-folder ./src/vs/editor --name=vscode-editor
/bluera-knowledge:add-folder ./src/vs/workbench --name=vscode-workbench

# Result: Multiple focused stores instead of one massive store
```

## Storage Management

### Monitoring Storage

Check what's using space:

```
list_stores()
→ vue: 487 files, 2.3 MB
→ react: 312 files, 1.8 MB
→ fastapi-docs: 156 pages, 0.9 MB
→ my-api: 89 files, 0.4 MB

Total storage: ~5.4 MB

# Detailed info
get_store_info('vue')
→ Location: .bluera/bluera-knowledge/repos/vue/
→ Indexed: 487 files
→ Size: 2.3 MB (source) + 4.1 MB (vectors)
→ Last indexed: 2 hours ago
```

### When to Delete Stores

**✅ Delete when:**
- Library no longer relevant to your project
- Documentation outdated (re-crawl instead)
- Testing/experimental stores no longer needed
- Running low on disk space
- Duplicate stores exist

**How to delete:**
```
/bluera-knowledge:remove-store old-library

# Or via MCP:
delete_store(store='old-library')
→ Removes: source files, vector index, metadata
→ Frees: ~6-8 MB per store (varies by size)
```

**⚠️ Cannot undo!** Make sure you don't need the store before deleting.

## Background Job Monitoring

All expensive operations run as background jobs: cloning, indexing, crawling.

### Job Lifecycle

```
1. create_store() or index_store() → Returns job_id

2. Job states:
   - pending: In queue, not started
   - running: Actively processing
   - completed: Finished successfully
   - failed: Error occurred

3. Monitor progress:
   check_job_status(job_id)
   → Current state, percentage, current file

4. List all jobs:
   list_jobs()
   → See pending, running, completed jobs

5. Cancel if needed:
   cancel_job(job_id)
   → Stops running job, cleans up
```

### Best Practices for Job Monitoring

**Do poll, but not too frequently:**
```
# ❌ Too frequent - wastes resources
while status != 'completed':
    check_job_status(job_id)  # Every second!
    sleep(1)

# ✅ Reasonable polling interval
while status != 'completed':
    check_job_status(job_id)
    sleep(15)  # Every 15 seconds is fine
```

**Do handle failures gracefully:**
```
status = check_job_status(job_id)

if status['state'] == 'failed':
    error = status['error']

    if 'auth' in error.lower():
        print("Authentication required - try SSH URL or provide credentials")
    elif 'not found' in error.lower():
        print("Repository/URL not found - check the source")
    elif 'disk' in error.lower():
        print("Disk space issue - delete unused stores")
    else:
        print(f"Unexpected error: {error}")
```

**Do list jobs to avoid duplicates:**
```
# Before creating new store
jobs = list_jobs()
existing = [j for j in jobs if j['store'] == 'vue' and j['state'] in ['pending', 'running']]

if existing:
    print(f"Job already running for 'vue': {existing[0]['id']}")
    # Wait for it instead of creating duplicate
else:
    create_store(...)
```

## Handling Indexing Failures

### Common Failure Scenarios

**1. Authentication Required (Private Repos)**
```
Error: "Authentication required"

Fix options:
  - Use SSH URL: git@github.com:org/repo.git
  - Use HTTPS with token: https://token@github.com/org/repo.git
  - Make repo public (if appropriate)
```

**2. Invalid URL/Path**
```
Error: "Repository not found" or "Path does not exist"

Fix:
  - Verify URL is correct (typos common!)
  - Check path exists and is accessible
  - Ensure network connectivity
```

**3. Disk Space**
```
Error: "No space left on device"

Fix:
  - Check available space: df -h
  - Delete unused stores: delete_store(old_store)
  - Clear .bluera/bluera-knowledge/repos/ manually if needed
```

**4. Network Timeout**
```
Error: "Connection timeout" or "Failed to fetch"

Fix:
  - Retry after checking network
  - Use --shallow for large repos
  - Clone manually then add-folder
```

**5. Unsupported File Types**
```
Warning: "Skipped 45 binary files"

This is normal!
  - Binary files (images, compiled code) are skipped
  - Only text files are indexed
  - Check indexed count vs total to see ratio
```

### Recovery Workflow

```
1. Attempt fails:
   create_store(url, name) → job fails

2. Check error:
   job_status = check_job_status(job_id)
   error_msg = job_status['error']

3. Determine fix based on error type (see above)

4. Retry with fix:
   create_store(corrected_url, name)

5. Verify success:
   check_job_status(new_job_id)
   → Status: completed

   list_stores()
   → Store appears in list

6. Test search:
   search(test_query, stores=[name], limit=3)
   → Returns results: ✅ Ready to use!
```

## Store Lifecycle Checklist

**Creating a Store:**
- [ ] Choose appropriate source type (repo/folder/crawl)
- [ ] Use descriptive, consistent naming
- [ ] Start indexing job
- [ ] Monitor job status until complete
- [ ] Verify with list_stores()
- [ ] Test with sample search

**Maintaining a Store:**
- [ ] Re-index after significant changes
- [ ] Pull git updates periodically for repo stores
- [ ] Monitor storage usage
- [ ] Check search relevance quality

**Deleting a Store:**
- [ ] Confirm no longer needed
- [ ] Note storage freed
- [ ] Remove from any documentation referencing it

## Quick Reference Commands

```
# Create
/bluera-knowledge:add-repo <url> --name=<name>
/bluera-knowledge:add-folder <path> --name=<name>
/bluera-knowledge:crawl <url> --name=<name>

# Monitor
/bluera-knowledge:check-status <job-id>

# Maintain
/bluera-knowledge:index <name>
/bluera-knowledge:stores

# Remove
/bluera-knowledge:remove-store <name>
```

Master these lifecycle management practices to maintain a clean, efficient, and useful knowledge base.
