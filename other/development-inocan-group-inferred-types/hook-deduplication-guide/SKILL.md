---
name: hook-deduplication-guide
description: Use PROACTIVELY when developing Claude Code hooks to implement content-based deduplication and prevent duplicate insight storage across sessions
---

# Hook Deduplication Guide

## Overview

This skill guides you through implementing robust deduplication for Claude Code hooks, using content-based hashing instead of session-based tracking. Prevents duplicate insights from being stored while allowing multiple unique insights per session.

**Based on 1 insight**:
- Hook Deduplication Session Management (hooks-and-events, 2025-11-03)

**Key Capabilities**:
- Content-based deduplication using SHA256 hashes
- Session-independent duplicate detection
- Efficient hash storage with rotation
- State management best practices

## When to Use This Skill

**Trigger Phrases**:
- "implement hook deduplication"
- "prevent duplicate insights in hooks"
- "content-based deduplication for hooks"
- "hook state management patterns"

**Use Cases**:
- Developing new Claude Code hooks that store data
- Refactoring hooks to prevent duplicates
- Implementing efficient state management for hooks
- Debugging duplicate data issues in hooks

**Do NOT use when**:
- Creating hooks that don't store data (read-only hooks)
- Session-based deduplication is actually desired
- Hook doesn't run frequently enough to need deduplication

## Response Style

Educational and practical - explain the why behind content-based vs. session-based deduplication, then guide implementation with code examples.

---

## Workflow

### Phase 1: Choose Deduplication Strategy

**Purpose**: Determine whether content-based or session-based deduplication is appropriate.

**Steps**:

1. **Assess hook behavior**:
   - How often does the hook run? (per message, per session, per event)
   - What data is being stored? (insights, logs, metrics)
   - Is the same content likely to appear across sessions?

2. **Evaluate deduplication needs**:
   - **Content-based**: Use when the same insight/data might appear in different sessions
     - Example: Extract-explanatory-insights hook (same insight might appear in multiple conversations)
   - **Session-based**: Use when duplicates should only be prevented within a session
     - Example: Error logging (same error in different sessions should be logged)

3. **Recommend strategy**:
   - For insights/lessons-learned: Content-based (SHA256 hashing)
   - For session logs/events: Session-based (session ID tracking)
   - For unique events: No deduplication needed

**Output**: Clear recommendation on deduplication strategy.

**Common Issues**:
- **Unsure which to use**: Default to content-based for data that's meant to be unique (insights, documentation)
- **Performance concerns**: Content-based hashing is fast (<1ms for typical content)

---

### Phase 2: Implement Content-Based Deduplication

**Purpose**: Set up SHA256 hash-based deduplication with state management.

**Steps**:

1. **Create state directory**:
   ```bash
   mkdir -p ~/.claude/state/hook-state/
   ```

2. **Initialize hash storage file**:
   ```bash
   HASH_FILE="$HOME/.claude/state/hook-state/content-hashes.txt"
   touch "$HASH_FILE"
   ```

3. **Implement hash generation**:
   ```bash
   # Generate SHA256 hash of content
   compute_content_hash() {
     local content="$1"
     echo -n "$content" | sha256sum | awk '{print $1}'
   }
   ```

4. **Check for duplicates**:
   ```bash
   # Returns 0 if content is new, 1 if duplicate
   is_duplicate() {
     local content="$1"
     local content_hash=$(compute_content_hash "$content")

     if grep -Fxq "$content_hash" "$HASH_FILE"; then
       return 1  # Duplicate found
     else
       return 0  # New content
     fi
   }
   ```

5. **Store hash after processing**:
   ```bash
   store_content_hash() {
     local content="$1"
     local content_hash=$(compute_content_hash "$content")
     echo "$content_hash" >> "$HASH_FILE"
   }
   ```

6. **Integrate into hook**:
   ```bash
   # In your hook script
   content="extracted insight or data"

   if is_duplicate "$content"; then
     # Skip - duplicate content
     echo "Duplicate detected, skipping..." >&2
     exit 0
   fi

   # Process new content
   process_content "$content"

   # Store hash to prevent future duplicates
   store_content_hash "$content"
   ```

**Output**: Working content-based deduplication in your hook.

**Common Issues**:
- **Hash file grows too large**: Implement rotation (see Phase 3)
- **False positives**: Ensure content normalization (whitespace, formatting)

---

### Phase 3: Implement Hash Rotation

**Purpose**: Prevent hash file from growing indefinitely.

**Steps**:

1. **Set rotation limit**:
   ```bash
   MAX_HASHES=10000  # Keep last 10,000 hashes
   ```

2. **Implement rotation logic**:
   ```bash
   rotate_hash_file() {
     local hash_file="$1"
     local max_hashes="${2:-10000}"

     # Count current hashes
     local current_count=$(wc -l < "$hash_file")

     # Rotate if needed
     if [ "$current_count" -gt "$max_hashes" ]; then
       tail -n "$max_hashes" "$hash_file" > "${hash_file}.tmp"
       mv "${hash_file}.tmp" "$hash_file"
       echo "Rotated hash file: kept last $max_hashes hashes" >&2
     fi
   }
   ```

3. **Call rotation periodically**:
   ```bash
   # After storing new hash
   store_content_hash "$content"
   rotate_hash_file "$HASH_FILE" 10000
   ```

**Output**: Self-maintaining hash storage with bounded size.

**Common Issues**:
- **Rotation too aggressive**: Increase MAX_HASHES
- **Rotation too infrequent**: Consider checking count before every append

---

### Phase 4: Testing and Validation

**Purpose**: Verify deduplication works correctly.

**Steps**:

1. **Test duplicate detection**:
   ```bash
   # First run - should process
   echo "Test insight" | your_hook.sh
   # Check: Content was processed

   # Second run - should skip
   echo "Test insight" | your_hook.sh
   # Check: Duplicate detected message
   ```

2. **Test multiple unique items**:
   ```bash
   echo "Insight 1" | your_hook.sh  # Processed
   echo "Insight 2" | your_hook.sh  # Processed
   echo "Insight 3" | your_hook.sh  # Processed
   echo "Insight 1" | your_hook.sh  # Skipped (duplicate)
   ```

3. **Verify hash file**:
   ```bash
   cat ~/.claude/state/hook-state/content-hashes.txt
   # Should show 3 unique hashes (not 4)
   ```

4. **Test rotation**:
   ```bash
   # Generate more than MAX_HASHES entries
   for i in {1..10500}; do
     echo "Insight $i" | your_hook.sh
   done

   # Verify file size bounded
   wc -l ~/.claude/state/hook-state/content-hashes.txt
   # Should be ~10000, not 10500
   ```

**Output**: Confirmed working deduplication with proper rotation.

---

## Reference Materials

- [Original Insight](data/insights-reference.md) - Full context on hook deduplication patterns

---

## Important Reminders

- **Use content-based deduplication for insights/documentation** - prevents duplicates across sessions
- **Use session-based deduplication for logs/events** - same event in different sessions is meaningful
- **Normalize content before hashing** - whitespace differences shouldn't create false negatives
- **Implement rotation** - prevent unbounded hash file growth
- **Hash storage location**: `~/.claude/state/hook-state/` (not project-specific)
- **SHA256 is fast** - no performance concerns for typical hook data
- **Test both paths** - verify both new content and duplicates work correctly

**Warnings**:
- ⚠️  **Do not use session ID alone** - prevents same insight in different sessions from being stored
- ⚠️  **Do not skip rotation** - hash file will grow indefinitely
- ⚠️  **Do not hash before normalization** - formatting changes will cause false negatives

---

## Best Practices

1. **Choose the Right Strategy**: Content-based for unique data, session-based for session-specific events
2. **Normalize Before Hashing**: Strip whitespace, lowercase if appropriate, consistent formatting
3. **Efficient Storage**: Use grep -Fxq for fast hash lookups (fixed-string, line-match, quiet)
4. **Bounded Growth**: Implement rotation to prevent file bloat
5. **Clear Logging**: Log when duplicates are detected for debugging
6. **State Location**: Use ~/.claude/state/hook-state/ for cross-project state

---

## Troubleshooting

### Duplicates not being detected

**Symptoms**: Same content processed multiple times

**Solution**:
1. Check hash file exists and is writable
2. Verify store_content_hash is called after processing
3. Check content normalization (whitespace differences)
4. Verify grep command uses -Fxq flags

**Prevention**: Test deduplication immediately after implementation

---

### Hash file growing too large

**Symptoms**: Hash file exceeds MAX_HASHES significantly

**Solution**:
1. Verify rotate_hash_file is called
2. Check MAX_HASHES value is reasonable
3. Manually rotate if needed: `tail -n 10000 hashes.txt > hashes.tmp && mv hashes.tmp hashes.txt`

**Prevention**: Call rotation after every hash storage

---

### False positives (new content marked as duplicate)

**Symptoms**: Different content being skipped

**Solution**:
1. Check for hash collisions (extremely unlikely with SHA256)
2. Verify content is actually different
3. Check normalization isn't too aggressive
4. Review recent hashes in file

**Prevention**: Use consistent normalization, test with diverse content

---

## Next Steps

After implementing deduplication:
1. Monitor hash file growth over time
2. Tune MAX_HASHES based on usage patterns
3. Consider adding metrics (duplicates prevented, storage size)
4. Share pattern with team for other hooks

---

## Metadata

**Source Insights**:
- Session: abc123-session-id
- Date: 2025-11-03
- Category: hooks-and-events
- File: docs/lessons-learned/hooks-and-events/2025-11-03-hook-deduplication.md

**Skill Version**: 0.1.0
**Generated**: 2025-11-16
**Last Updated**: 2025-11-16
