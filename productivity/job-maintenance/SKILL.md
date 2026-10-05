---
name: job-maintenance
description: Maintain the VisaJobs.xyz job board by checking for dead links, removing expired jobs, and cleaning up data. Use when the user asks to check jobs, clean up listings, remove dead links, validate URLs, or maintain the job board.
---

# Job Board Maintenance

## Existing Automation

### Dead link checker: `scripts/check-jobs.js`

Reads `src/_data/jobs.json`, sends HEAD requests to each job's `description` URL, and removes dead entries.

```bash
# Dry run (shows what would be removed, no changes)
node scripts/check-jobs.js --dry-run

# Check first 100 jobs
node scripts/check-jobs.js --batch=100

# Check all jobs
node scripts/check-jobs.js
```

**Detection rules:**
- HTTP 404, 410, 403 → dead
- DNS resolution failure → dead
- Follows one redirect before checking
- Logs removals to `scripts/removed-jobs.log`

### GitHub Actions: `.github/workflows/check-jobs.yml`

Runs automatically:
- **Schedule**: Monday and Thursday at 06:00 UTC
- **Batch**: 100 jobs per run
- Auto-commits and pushes removals if changes found

## Manual Maintenance Tasks

### Check total job count
```bash
python3 -c "import json; jobs=json.load(open('src/_data/jobs.json')); print(f'Total: {len(jobs)}')"
```

### Find jobs older than N days
```bash
python3 -c "
import json
from datetime import datetime, timedelta
jobs = json.load(open('src/_data/jobs.json'))
cutoff = datetime.now() - timedelta(days=90)
for j in jobs:
    try:
        d = datetime.strptime(j['post_date'], '%B %d, %Y')
        if d < cutoff:
            print(f'{j[\"post_date\"]} | {j[\"company\"]} | {j[\"position\"]}')
    except: pass
"
```

### Find duplicate entries
```bash
python3 -c "
import json
from collections import Counter
jobs = json.load(open('src/_data/jobs.json'))
dupes = Counter((j['company'], j['position']) for j in jobs)
for (c, p), count in dupes.items():
    if count > 1:
        print(f'{count}x | {c} | {p}')
"
```

### List companies with job counts
```bash
python3 -c "
import json
from collections import Counter
jobs = json.load(open('src/_data/jobs.json'))
for company, count in Counter(j['company'] for j in jobs).most_common():
    print(f'{count:3d} | {company}')
"
```

### Find entries missing fields
```bash
python3 -c "
import json
REQUIRED = ['company','position','location','contract','reloc','visa','post_date','logo','description']
jobs = json.load(open('src/_data/jobs.json'))
for i, j in enumerate(jobs):
    missing = [f for f in REQUIRED if f not in j]
    if missing:
        print(f'Job {i}: {j.get(\"company\",\"?\")} missing {missing}')
"
```

### Verify all logos exist
```bash
python3 -c "
import json, os
jobs = json.load(open('src/_data/jobs.json'))
logos = set(j['logo'] for j in jobs)
for logo in sorted(logos):
    path = logo.lstrip('/')
    if not os.path.exists(path):
        print(f'MISSING: {logo}')
"
```

## Maintenance Checklist

- [ ] Run dead link checker (`--dry-run` first)
- [ ] Remove jobs older than 6 months
- [ ] Remove duplicates
- [ ] Verify all logos exist
- [ ] Validate JSON structure
- [ ] Check for missing fields
- [ ] Commit and push changes
