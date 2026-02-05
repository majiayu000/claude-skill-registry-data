---
name: setup-assistant
description: Detect when user is working in an un-indexed project and proactively suggest enabling semantic memory. Activates on first code question in new projects to guide users through initial setup.
auto-activate: true
---

# Infinite Memory Setup Assistant Skill

Proactively suggest indexing when user would benefit from semantic memory.

## Activation Logic

Activate when **ALL** of these conditions are met:

1. **User asks a code-related question** (same detection as semantic-search skill)
2. **Current project is NOT indexed** (no Pixeltable database found)
3. **Haven't prompted user this session** (check session flag to avoid repeated prompts)

## Execution Steps

### 1. Detect Project State

**Check if indexed:**
```bash
# Calculate project hash
PROJECT_PATH=$(pwd)
PROJECT_HASH=$(echo -n "$PROJECT_PATH" | sha256sum | cut -c1-16)

# Check for database
if [ ! -d ~/.pixeltable/$PROJECT_HASH ]; then
    echo "Not indexed"
fi
```

**Check project size:**
```bash
# Count supported files
FILE_COUNT=$(find . -type f \( \
    -name "*.py" -o \
    -name "*.js" -o \
    -name "*.ts" -o \
    -name "*.md" -o \
    -name "*.txt" -o \
    -name "*.json" -o \
    -name "*.yaml" -o \
    -name "*.yml" \
) | wc -l)
```

### 2. Check Session State

**Don't prompt if already asked:**
```bash
# Create session marker directory
SESSION_DIR=~/.claude/memory/sessions
mkdir -p $SESSION_DIR

# Check if already prompted
SESSION_FILE=$SESSION_DIR/${PROJECT_HASH}-prompted

if [ -f "$SESSION_FILE" ]; then
    # Already prompted this session, skip
    exit 0
fi
```

### 3. Smart Prompting Based on Project Size

**Large Project (>50 files):**

```
💡 I notice this project isn't indexed for semantic search yet.

With {FILE_COUNT} files, semantic memory could help me:
- Find relevant code instantly when you ask questions
- Remember architectural patterns across sessions
- Search documentation and comments semantically

Indexing typically takes ~30 seconds. Would you like me to index this project?

[Index Now] [Ask Me Later] [Learn More]
```

**Medium Project (10-50 files):**

```
This project isn't indexed yet. I can enable semantic search (takes ~5-10 seconds)
to help answer code questions faster.

Enable memory for this project?
[Yes, index it] [No thanks]
```

**Small Project (<10 files):**

**Don't prompt** - project is small enough that traditional search works fine.
Semantic search overhead not worth it for tiny projects.

### 4. Handle User Response

**If User Accepts:**
1. Set session flag (create prompt marker file)
2. Run `/index-project` command automatically
3. Wait for completion
4. Report success
5. **Then activate semantic-search skill** to answer their original question

**If User Declines:**
1. Set session flag (don't prompt again this session)
2. Continue with traditional grep-based search
3. Add helpful tip: "💡 Tip: Run `/index-project` anytime to enable semantic search"

**If User Clicks "Learn More":**

Show brief explanation:
```
Semantic Memory for Code

Infinite Memory indexes your code with vector embeddings, enabling:

✨ Natural language search
   "How does authentication work?" → Finds auth-related files

🎯 Concept-based finding
   Finds code by what it does, not just keywords

⚡ Fast and local
   1,500+ files/sec, all data stays on your machine

📊 Performance
   - Indexing: ~0.3s for 500 files
   - Search: <200ms latency
   - Storage: ~2KB per file

Try it?
[Index Now] [Maybe Later]
```

### 5. Create Session Marker

```bash
# Mark as prompted for this session
touch $SESSION_FILE

# Optional: Clean up old markers (>24 hours)
find $SESSION_DIR -name "*-prompted" -mtime +1 -delete
```

## Anti-Patterns (When NOT to Activate)

**DO NOT prompt for:**

❌ **Very small projects (<10 files)**
- Not worth the indexing overhead
- Traditional search works fine

❌ **System directories:**
- /etc, /sys, /proc, /dev
- Temporary directories (/tmp, /var)
- Package installation directories (node_modules, .venv)

❌ **User explicitly said "no" this session:**
- Check session marker file
- Respect user's choice

❌ **Non-code questions:**
- Only prompt when user asks code questions
- Don't interrupt other workflows

## Session Persistence

**Marker File Format:**
```
Location: ~/.claude/memory/sessions/{PROJECT_HASH}-prompted
Content: Empty (existence is the flag)
Lifetime: Cleaned up after 24 hours or on manual cleanup
```

**Why session-based?**
- Allows user to decline without being nagged repeatedly
- Resets after 24 hours (user might change mind)
- Lightweight (just empty marker files)

## Integration with Semantic Search Skill

**Handoff Pattern:**

1. User asks code question
2. Setup-assistant detects not indexed
3. Prompts user to index
4. User accepts
5. Indexing completes
6. **Activate semantic-search skill** to answer original question
7. User gets answer seamlessly

**This creates a smooth flow:**
```
User: "How does auth work?"
↓
Setup: "Project not indexed. Index now?"
↓
User: [Index Now]
↓
Indexing... ✅ Complete!
↓
Semantic Search: "Authentication uses JWT tokens:
1. Login handler (auth.py, 92% match)..."
```

## Example Interactions

### First Code Question in New Project

```
User: "Where is the database configured?"