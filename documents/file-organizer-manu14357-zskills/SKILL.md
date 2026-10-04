---
name: file-organizer
description: Intelligently organize files across your computer by understanding context, detecting duplicates, suggesting folder structures, and automating cleanup. Maintain a clean digital workspace without manual effort.
compatibility:
  use-case: File management, organization, cleanup, deduplication
  frameworks: File system utilities, automation scripts
---

# File Organizer

## Use This Skill When

- Downloads folder has become chaotic and disorganized
- Can't find files because they're scattered everywhere
- Duplicate files taking up unnecessary space
- Current folder structure no longer makes sense
- Starting a new project and need initial organization
- Cleaning up before archiving old projects
- Want to establish better organization habits
- Disk space running low and need to identify waste

## When NOT to Use

- Working with highly sensitive/confidential files (consider security implications)
- Automated organization before manual backup
- Files requiring specific regulatory/compliance structure (consult policies first)
- Active projects in flux (wait until work stabilizes)

## Context: File Organization Maturity

**Undeveloped**: Files scattered, no structure, duplicates unknown, chaos.

**Target**: Identified duplicates, suggested folder hierarchy, automated sorting by type/date.

**Optimized**: Context-aware organization, automated archival, periodic maintenance scripts, tagging system.

## Core Principle

**File organization reduces cognitive load.** Clear structure means you find things quickly, spot duplicates easily, and maintain less clutter — enabling you to focus on work, not hunting for files.

## Instructions

### Step 1: Understand Your Organization Goals

**Ask clarifying questions:**

| Question | Why It Matters |
|----------|----------------|
| Which directory needs help? | Scope: Downloads vs. Documents vs. entire home? |
| What's the main pain point? | Can't find things? Too much duplication? Outdated structure? |
| Files to exclude/protect? | Current projects, sensitive data, external links? |
| Aggressiveness level? | Conservative (keep structure intact) vs. comprehensive (restructure completely)? |
| Timeline preferences? | What files should move (old files after 6 months?)? |

**Document scope:**
```markdown
# File Organization Project

**Target Directory**: ~/Downloads
**Main Problem**: "Can't find things, everything is mixed together"
**Scope**: Downloads only (protect ~/Projects, ~/Work)
**Aggressiveness**: Moderate (organize but don't delete)
**Archive Timeline**: Files not touched in 6+ months → Archive folder
```

### Step 2: Analyze Current State

**Get overview of directory:**
```bash
# Total files and folders
find [target] -type f | wc -l
find [target] -type d | wc -l

# File type breakdown
find [target] -type f -exec file {} \; | \
  awk '{print $NF}' | sort | uniq -c | sort -rn

# Size breakdown (top 20 largest)
du -ah [target]/* 2>/dev/null | sort -rh | head -20

# Age breakdown (modified dates)
find [target] -type f -printf '%T@\n' | \
  awk '{if(NR==1 || $1<min) min=$1; if(NR==1 || $1>max) max=$1} END {print "Oldest:", min, "Newest:", max}'

# File extensions count
find [target] -type f -name '*.*' -exec basename {} \; | \
  sed 's/.*\.//' | sort | uniq -c | sort -rn
```

**Summarize findings:**
```markdown
## Current State Analysis

**Total**: 1,247 files in 89 folders
**Storage**: 45.3 GB total

**File Type Breakdown**:
- Images (JPG, PNG, GIF): 312 files (28 GB) — 61%
- Documents (PDF, DOCX): 178 files (3.2 GB) — 7%
- Archives (ZIP, RAR): 95 files (8.1 GB) — 18%
- Videos (MP4, MOV): 23 files (5.2 GB) — 11%
- Other: 639 files (702 MB) — 2%

**Age**: 
- Created in last 30 days: 145 files
- Last 3 months: 312 files
- Over 6 months old: 790 files (64% of total)

**Issues Identified**:
- 3 duplicate images (scan-1.jpg, scan-1 copy.jpg, scan_1.jpg)
- Random naming (Screenshot_2026-04-25.png, IMG_20220315_091745.jpg)
- Mixed projects in root (no subfolder structure)
```

### Step 3: Identify Duplicates

**Find exact duplicates:**
```bash
# Method 1: Hash-based duplicate detection
find [target] -type f -exec md5sum {} \; | \
  sort | uniq -d -w 32 | awk '{print $2}' | xargs ls -lh

# Method 2: By name + size (potential duplicates)
find [target] -type f -exec basename {} \; | \
  sort | uniq -d | while read name; do
    find [target] -name "$name" -exec ls -lh {} \;
  done
```

**Categorize duplicates:**

```markdown
## Duplicates Found

### Exact Duplicates (identical files)
| File | Size | Copies | Age Range | Action |
|------|------|--------|-----------|--------|
| presentation-v1.pdf | 2.1 MB | 3 | Apr 2026 | Keep latest, archive others |
| logo.png | 145 KB | 2 | Feb 2026 | Keep 1, delete 1 |
| archive.zip | 456 MB | 2 | Dec 2025 | Delete 1 (confirm contents match) |

### Likely Duplicates (similar names/sizes)
| Pattern | Examples | Recommendation |
|---------|----------|-----------------|
| scan copies | scan-1.jpg, scan_1.jpg, scan (copy).jpg | Manual check; likely same file with versioning |

**Total duplicate space**: ~890 MB
```

### Step 4: Suggest New Folder Structure

**Propose organized hierarchy:**

```markdown
## Recommended Folder Structure

### Option A: By File Type (Simple)
```
Downloads/
├── Documents/
│   ├── 2026/
│   ├── 2025/
│   └── Templates/
├── Images/
│   ├── Screenshots/
│   ├── Photos/
│   └── Design/
├── Videos/
├── Archives/
└── Archive/  [older files, infrequent access]
```

### Option B: By Project + Type (Complex but useful)
```
Downloads/
├── Projects/
│   ├── Website-Redesign/
│   │   ├── Assets/
│   │   ├── Designs/
│   │   └── Archive/
│   ├── Marketing-Campaign/
│   │   ├── Photos/
│   │   ├── Copywriting/
│   │   └── Archive/
├── Personal/
│   ├── Finances/
│   ├── Travel/
│   └── Archive/
├── Quick-Refs/  [single files, references]
└── Archive/  [old projects, 6+ months]
```

### Option C: Hybrid (By Type + Date for large folders)
```
Downloads/
├── Documents/
│   ├── 2026-Q2/
│   ├── 2026-Q1/
│   └── Archive/
├── Images/
│   ├── 2026-Recent/
│   ├── 2025/
│   └── Archive/
├── Projects/  [active work]
└── Archive/  [6+ months old]
```

**Recommendation**: Option C (hybrid) balances simplicity with discovery
```

### Step 5: Plan File Migration

**Create migration strategy:**

```markdown
## Migration Plan

**Phase 1: Backup (Safety)**
[ ] Create backup: `cp -r ~/Downloads ~/Downloads-backup-$(date +%Y%m%d)`
[ ] Verify backup exists and is readable

**Phase 2: Duplicate Cleanup**
[ ] Delete confirmed duplicates: [list 3 files]
[ ] Expected recovery: ~890 MB

**Phase 3: Create New Folders**
[ ] mkdir -p ~/Downloads/Documents/2026
[ ] mkdir -p ~/Downloads/Documents/2025
[ ] mkdir -p ~/Downloads/Images/Screenshots
[ ] mkdir -p ~/Downloads/Images/Photos
[ ] mkdir -p ~/Downloads/Projects
[ ] mkdir -p ~/Downloads/Archive

**Phase 4: Move by Type**
[ ] Move *.pdf, *.docx, *.txt → Documents/
[ ] Move *.jpg, *.png, *.gif → Images/
[ ] Move *.mp4, *.mov → Videos/
[ ] Move *.zip, *.rar → Archives/

**Phase 5: Organize by Date**
[ ] In Documents/: Rename files with date prefixes if missing
[ ] In Images/: Sort into 2026-Recent vs. 2025

**Phase 6: Archive Old Files**
[ ] Move files untouched >6 months → Archive/
[ ] Compress: tar -czf ~/Downloads/Archive-backup-$(date +%Y%m%d).tar.gz Archive/

**Phase 7: Verify**
[ ] Check all files moved correctly
[ ] No files lost (compare file counts)
[ ] Can find key files quickly (spot check 5 files)

**Phase 8: Cleanup**
[ ] Delete backup-backup if verification passes
[ ] Document new structure in README.txt
```

### Step 6: Execute with Scripts

**Safe migration script:**

```bash
#!/bin/bash
# organized-downloads.sh — Safe file organization

TARGET=${1:-.}
BACKUP="${TARGET}-backup-$(date +%Y%m%d-%H%M%S)"

echo "🔄 Backing up $TARGET → $BACKUP"
cp -r "$TARGET" "$BACKUP"
echo "✓ Backup complete"

echo "📁 Creating folder structure..."
mkdir -p "$TARGET"/{Documents/{2026,2025},Images/{Screenshots,Photos},Videos,Projects,Archive}

echo "🔍 Detecting and removing exact duplicates..."
find "$TARGET" -type f -exec md5sum {} + | \
  awk '{print $1, $2}' | \
  sort | uniq -d -w 32 | \
  awk '{print $2}' | \
  while read file; do
    echo "  Removing duplicate: $file"
    rm "$file"
  done

echo "📄 Moving documents..."
find "$TARGET" -maxdepth 1 -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.txt" \) \
  -exec mv {} "$TARGET/Documents/2026/" \;

echo "🖼️ Moving images..."
find "$TARGET" -maxdepth 1 -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \) \
  -exec mv {} "$TARGET/Images/Photos/" \;

echo "🎬 Moving videos..."
find "$TARGET" -maxdepth 1 -type f \( -name "*.mp4" -o -name "*.mov" \) \
  -exec mv {} "$TARGET/Videos/" \;

echo "📦 Moving archives..."
find "$TARGET" -maxdepth 1 -type f \( -name "*.zip" -o -name "*.rar" \) \
  -exec mv {} "$TARGET/Archives/" \;

echo "✅ Organization complete!"
echo "📊 Summary:"
echo "  Backup: $BACKUP"
du -sh "$TARGET" | awk '{print "  Total size: " $1}'
echo "  Structure: $(ls -d $TARGET/*/ | wc -l) folders"
```

**Run safely:**
```bash
chmod +x organized-downloads.sh
./organized-downloads.sh ~/Downloads
```

### Step 7: Establish Maintenance Routine

**Weekly habits:**
```markdown
## Weekly Maintenance (5 mins)

**Monday morning**:
- [ ] Check Downloads folder for new clutter
- [ ] Move completed work to Projects folder
- [ ] Archive files completed >1 week ago

**Friday afternoon**:
- [ ] Review: Any new duplicate patterns?
- [ ] Rename recent files with clear names
- [ ] Delete temporary/test files
```

**Monthly archival:**
```bash
# Archive files untouched >60 days
find ~/Downloads -type f -mtime +60 \
  -exec mv {} ~/Downloads/Archive/ \;

# Compress monthly
tar -czf ~/Downloads/Archive-$(date +%Y%m).tar.gz \
  ~/Downloads/Archive/
```

## Output

**Deliver:**

1. **Current State Analysis**
   - File counts by type
   - Storage breakdown
   - Identified duplicates
   - Age distribution

2. **Duplicate Report**
   - Exact duplicates found
   - Suspected duplicates
   - Total space recoverable

3. **Recommended Structure**
   - Proposed folder hierarchy
   - Rationale for organization method
   - Options if user has preferences

4. **Migration Plan**
   - Step-by-step procedure
   - Safe backup strategy
   - Verification steps

5. **Automation Script** (optional)
   - Safe bash script to execute migration
   - Verification checks included

6. **Maintenance Guide**
   - Weekly habits (5 mins)
   - Monthly archival schedule