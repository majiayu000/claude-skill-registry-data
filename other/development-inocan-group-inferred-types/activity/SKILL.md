---
name: activity
description: Generate Linear activity reports for date ranges.
---

# Linear Activity Reporter

Linear MCP를 사용하여 특정 기간의 활동을 수집하고 시간별 마크다운 리포트를 생성한다.

## Workflow

### 1. Fetch User and Team Data

```python
user = mcp__linear__get_user(query="me")
teams = mcp__linear__list_teams(limit=250)
```

- **Error**: See [Troubleshooting](#troubleshooting)
- **Multiple teams**: Use `AskUserQuestion` with multiSelect for team selection

### 2. Calculate Date Range

| User Request | Action |
|--------------|--------|
| Explicit date | Use as target_date |
| Relative ("yesterday", "어제") | Calculate with `date` command |
| Not specified | Use `AskUserQuestion` to prompt |

Convert to ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`

### 3. Collect Activity Data

Execute parallel MCP calls for each team:

| Data Type | MCP Function | Key Filters |
|-----------|--------------|-------------|
| Issues Created | `list_issues` | `assignee="me"`, `createdAt` |
| Issues Updated | `list_issues` | `assignee="me"`, `updatedAt` |
| Comments | `list_comments` | `issueId` (filter by date client-side) |
| Projects | `list_projects` | `member="me"`, `createdAt`/`updatedAt` |
| Cycles | `list_cycles` | `teamId`, filter date client-side |

For API details: [references/api-reference.md](references/api-reference.md)

### 4. Process and Group Data

1. **Convert UTC to local timezone** (detect with `datetime.now().astimezone()`)
2. **Group by hour** (00-23) and team
3. **Categorize** by activity type

### 5. Generate Reports

Output to `~/.claude/tmp/linear-activity/reports/`:
- `YYYY-MM-DD.md` - Human-readable markdown
- `YYYY-MM-DD.json` - Machine-readable (for calendar-sync)

For format specification: [references/output-template.md](references/output-template.md)

**Activity Icons:**
| Icon | Type |
|------|------|
| 🆕 | Issue Created |
| 📝 | Issue Updated |
| 💬 | Issue Comment |
| 📊 | Project Created |
| 🔧 | Project Updated |
| 🔄 | Cycle Created/Updated |

## Usage Examples

| Request | Result |
|---------|--------|
| "어제 Linear 활동 보여줘" | Yesterday's activities, all teams |
| "2025-11-01부터 오늘까지 이슈 리포트 생성" | Date range report |
| "지난주 Linear 활동 정리" | Last 7 days report |
| "Engineering 팀의 나의 활동 요약" | Specific team filter |

## Integration with calendar-sync

Generated JSON reports are compatible with calendar-sync skill:

```
1. Generate report → ~/.claude/tmp/linear-activity/reports/YYYY-MM-DD.json
2. Run calendar-sync → Generates gcalcli commands → Adds to Google Calendar
```

## Troubleshooting

### Linear MCP Connection Error

**Symptom**: `mcp__linear__get_user` fails

**Solutions**:
1. Verify MCP configuration in `~/.claude.json`
2. Test connection: `mcp__linear__list_teams()`
3. Check Linear workspace access
4. Re-authenticate if needed

### No Activities Found

**Cause**: No activities in date range or filters too restrictive

**Solutions**:
- Expand date range
- Check `assignee="me"` filter
- Verify team access

### Missing Issues/Projects

**Cause**: API limit (250 items) or filter restrictions

**Solutions**:
- Narrow date range
- Check team/project filters
- Split large datasets into multiple queries

### Timezone Display Issues

**Solution**: Set timezone explicitly: `export TZ=Asia/Seoul`

## References

- [references/api-reference.md](references/api-reference.md) - Linear MCP API functions and parameters
- [references/output-template.md](references/output-template.md) - Report format specification and JSON schema
