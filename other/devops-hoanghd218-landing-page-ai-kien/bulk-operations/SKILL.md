---
name: bulk-operations
description: Efficiently update multiple Azure DevOps work items at once. Use when the user wants to update many work items, bulk state changes, mass updates, batch operations, or update work items in a loop. Use when user mentions "bulk", "batch", "multiple items", "all tasks", "update several", or "mass update".
---

# Bulk Operations Reference (Verified)

## Performance Insight

**Direct bash for loops are approximately 10x faster than sub-agents for bulk operations.**

This is because:
1. No agent spawning overhead
2. Direct CLI execution
3. Can use `-o none` to skip JSON parsing

## Recommended Patterns

### Fast Bulk State Update

```bash
# Update multiple work items to same state
for id in 1858 1859 1860; do
  az boards work-item update --id $id --state "Done" -o none && echo "Updated $id"
done
```

### Update from Query Results

```bash
# Query IDs then update each
ids=$(az boards query --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.State] = 'Active' AND [System.TeamProject] = 'ProjectName'" -o tsv | cut -f1)

for id in $ids; do
  az boards work-item update --id $id --state "Resolved" -o none && echo "Updated $id"
done
```

### Bulk Assignment

```bash
for id in 1001 1002 1003; do
  az boards work-item update --id $id --assigned-to "user@domain.com" -o none && echo "Assigned $id"
done
```

### Bulk Field Update

```bash
for id in 1001 1002 1003; do
  az boards work-item update --id $id --fields "Microsoft.VSTS.Common.Priority=1" -o none && echo "Updated priority for $id"
done
```

### Bulk Add Discussion Comment

```bash
for id in 1001 1002 1003; do
  az boards work-item update --id $id --discussion "Reviewed in sprint planning" -o none && echo "Commented on $id"
done
```

## Output Optimization

Use `-o none` to suppress JSON output when you don't need the response:

```bash
# With output (slower)
az boards work-item update --id 1234 --state "Done" -o json

# Without output (faster)
az boards work-item update --id 1234 --state "Done" -o none
```

## Error Handling

### Continue on Error

```bash
for id in 1001 1002 1003; do
  az boards work-item update --id $id --state "Done" -o none 2>/dev/null && echo "OK: $id" || echo "FAIL: $id"
done
```

### Stop on First Error

```bash
for id in 1001 1002 1003; do
  az boards work-item update --id $id --state "Done" -o none || { echo "Failed on $id"; break; }
  echo "Updated $id"
done
```

### Collect Failures

```bash
failed_ids=""
for id in 1001 1002 1003; do
  if ! az boards work-item update --id $id --state "Done" -o none 2>/dev/null; then
    failed_ids="$failed_ids $id"
  fi
done
[ -n "$failed_ids" ] && echo "Failed IDs:$failed_ids"
```

## Counting Operations

### Quick Count from Query

```bash
az boards query --wiql "SELECT [System.Id] FROM WorkItems WHERE ..." --output table | tail -n +3 | wc -l
```

Note: `tail -n +3` skips the header rows in table output.

### Count Before Bulk Update

```bash
count=$(az boards query --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.State] = 'Active' AND [System.TeamProject] = 'ProjectName'" -o tsv | wc -l)
echo "Will update $count items"
```

## Anti-Patterns to Avoid

### Don't Use Sub-Agents for Bulk Ops

```bash
# SLOW - spawns sub-agent for each item
# Avoid patterns that create new agent instances per item
```

### Don't Parse Full JSON for Each Update

```bash
# SLOW - full JSON parsing with extra extraction
for id in 1001 1002 1003; do
  az boards work-item update --id $id --state "Done" --query "id" -o tsv  # Unnecessary if you already know the ID
done

# FAST - suppress output
for id in 1001 1002 1003; do
  az boards work-item update --id $id --state "Done" -o none && echo "Updated $id"
done
```

## Parallel Execution (Advanced)

For very large batches, consider parallel execution with background jobs:

```bash
# Run updates in parallel (use with caution - may hit rate limits)
for id in 1001 1002 1003 1004 1005; do
  az boards work-item update --id $id --state "Done" -o none &
done
wait
echo "All updates complete"
```

**Caution:** Parallel execution may hit Azure DevOps API rate limits. Use sparingly.

## Typical Use Cases

1. **Sprint Cleanup** - Move all remaining items to next sprint
2. **Bulk Close** - Close all resolved items at end of sprint
3. **Mass Reassignment** - Reassign items when team member leaves
4. **Priority Reset** - Update priorities after planning session
5. **Tag Application** - Add tags to multiple related items
