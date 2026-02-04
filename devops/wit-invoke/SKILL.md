---
name: wit-invoke
description: Call Azure DevOps REST APIs via az devops invoke command. Use when you need to access Azure DevOps features not available in the CLI, such as work item comments, search, boards, backlogs, capacities, or any wit/work/search API endpoint. Use when the user mentions "invoke", "REST API", "API call", or needs features like comments, search, board columns, or team capacity.
---

# Azure DevOps REST API via az devops invoke (Verified)

## CRITICAL LIMITATIONS - READ FIRST

1. **--in-file requires actual file path** - Does NOT accept stdin (`-`):
   ```bash
   # WRONG - will fail:
   echo '{}' | az devops invoke --in-file -

   # CORRECT:
   echo '{"searchText": "query"}' > /tmp/request.json
   az devops invoke --in-file /tmp/request.json
   ```

2. **Comments API doesn't work via invoke** - Use `--discussion` on update instead:
   ```bash
   # WRONG - returns 404:
   az devops invoke --area wit --resource comments --route-parameters workItemId=123

   # CORRECT - add comment via update:
   az boards work-item update --id 123 --discussion "My comment" -o json
   ```

3. **Route parameters must match exactly** - Missing or extra params cause KeyError

## Command Pattern

```bash
az devops invoke \
  --area {AREA} \
  --resource {RESOURCE} \
  --route-parameters {key}={value} \
  --http-method {GET|POST|PUT|PATCH|DELETE} \
  --in-file {file.json} \
  --api-version {VERSION} \
  -o json
```

## Verified Working Examples

### Search Work Items (VERIFIED)

Create search payload:
```bash
echo '{"searchText": "pipeline", "$top": 10}' > /tmp/search.json
```

Execute search:
```bash
az devops invoke \
  --area search \
  --resource workitemsearchresults \
  --http-method POST \
  --in-file /tmp/search.json \
  --api-version 7.0 \
  -o json
```

With JMESPath query for clean output:
```bash
az devops invoke \
  --area search \
  --resource workitemsearchresults \
  --http-method POST \
  --in-file /tmp/search.json \
  --api-version 7.0 \
  --query "results[].{id:fields.\"system.id\", title:fields.\"system.title\", state:fields.\"system.state\"}" \
  -o table
```

### List Boards (VERIFIED)

```bash
az devops invoke \
  --area work \
  --resource boards \
  --route-parameters project=ProjectName team="TeamName" \
  --api-version 7.0 \
  -o json
```

### Get Board Columns (VERIFIED)

```bash
az devops invoke \
  --area work \
  --resource columns \
  --route-parameters project=ProjectName team="TeamName" board=Features \
  --api-version 7.0 \
  -o json
```

### Get Backlogs (VERIFIED)

```bash
az devops invoke \
  --area work \
  --resource backlogs \
  --route-parameters project=ProjectName team="TeamName" \
  --api-version 7.0 \
  -o json
```

### Get Team Capacity

```bash
az devops invoke \
  --area work \
  --resource capacities \
  --route-parameters project=ProjectName team="TeamName" iterationId={GUID} \
  --api-version 7.0 \
  -o json
```

## Verified Areas and Resources

### work (Boards & Backlogs)

| Resource | Route Parameters | Verified |
|----------|-----------------|----------|
| boards | project, team | YES |
| columns | project, team, board | YES |
| backlogs | project, team | YES |
| capacities | project, team, iterationId | - |
| teamdaysoff | project, team, iterationId | - |

### search

| Resource | Method | Verified |
|----------|--------|----------|
| workitemsearchresults | POST | YES |

### wit (Work Item Tracking)

| Resource | Note |
|----------|------|
| comments | NOT WORKING via invoke - use `az boards work-item update --discussion` instead |

## API Discovery

To see ALL available API areas and resources:
```bash
az devops invoke -o json > api-discovery.json
```

This returns 214 areas with 1,407+ resources.

## Tips

1. **Use temp files for POST bodies** - Create in /tmp/, clean up after
2. **Quote team names with spaces** - `team="Team Name"`
3. **Check resource names** - Some use camelCase, others lowercase
4. **Use --query for filtering** - JMESPath queries reduce output
5. **Try 7.0 first** - Fall back to preview versions if needed
