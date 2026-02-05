---
created: "2025-10-21 14:35"
updated: "2025-10-21 14:35"
system_type: "claude-code-skill"
status: "active"
---

# Daily Workflow Automation Skill

## Overview

**Purpose**: Automatically processes daily notes when users mention diary extraction, end-of-day workflows, or ask "what did I work on today". Extracts entries from `### 🧠 Notes` sections, classifies them using AI, routes them to appropriate context/diary/insights/ideas files, and updates memory systems (Serena + Graphiti).

**Type**: Claude Code Skill (Auto-triggered)

**Status**: Active (Phase 1 Implementation Complete)

**Replaces**: `/extract-daily-content` command (manual slash command)

## Location

### Primary Files

- [.claude/skills/daily-workflow/SKILL.md](.claude/skills/daily-workflow/SKILL.md) - Main skill workflow (loads when triggered)
- [.claude/skills/daily-workflow/reference/templates.md](.claude/skills/daily-workflow/reference/templates.md) - Daily note template documentation
- [.claude/skills/daily-workflow/reference/formatting-rules.md](.claude/skills/daily-workflow/reference/formatting-rules.md) - Entry transformation rules
- [.claude/skills/daily-workflow/scripts/extract_content.py](.claude/skills/daily-workflow/scripts/extract_content.py) - Deterministic extraction script

### Configuration

- [.claude/skills/README.md](.claude/skills/README.md) - Skill registry and testing guide
- [98-templates/daily-note.md](98-templates/daily-note.md) - Daily note template with `### 🧠 Notes` section
- `.claude/commands/.extract-daily-content-tracker.json` - Extraction tracker (auto-created)

### Related Files

- `.claude/commands/extract-daily-content.md` - Original command (now deprecated in favor of skill)
- `00 - Daily/` - Daily notes directory (extraction source)
- `04-resources/diary.md` - Primary diary destination
- `04-resources/context.md` - Primary context destination
- `01-areas/p-dev/insights.md` - Primary insights destination
- `04-resources/ideas.md` - Primary ideas destination

## Architecture

### Components

1. **SKILL.md** ([.claude/skills/daily-workflow/SKILL.md:1](.claude/skills/daily-workflow/SKILL.md#L1))
   - Purpose: Main skill file with frontmatter trigger description
   - Auto-loaded by Claude Code when conversation matches triggers
   - Contains: Quick workflow, classification rules, context areas, critical rules
   - Token-efficient: ~350 lines (under 500 line best practice)

2. **Extraction Script** ([.claude/skills/daily-workflow/scripts/extract_content.py:1](.claude/skills/daily-workflow/scripts/extract_content.py#L1))
   - Purpose: Deterministic file I/O, pattern matching, data structure operations
   - Key functions:
     - `find_daily_note(date_str)` - Locate daily note files by date
     - `extract_notes_section(filepath)` - Extract `### 🧠 Notes` content
     - `split_entries(notes_content)` - Split into individual entries
     - `check_duplicate(entry, existing_entries)` - Fuzzy matching (80% threshold)
     - `format_cross_link(daily_note_path)` - Generate wikilinks
   - Handles: Tracker management, file creation with frontmatter, atomic appends

3. **Reference Documentation** ([.claude/skills/daily-workflow/reference/](.claude/skills/daily-workflow/reference/))
   - `templates.md` - Daily note structure, Dataview patterns, entry recognition
   - `formatting-rules.md` - Transformation rules, cross-linking format, deduplication

### Data Flow

```
Daily Note (00 - Daily/)
  ↓
### 🧠 Notes Section Extraction (Python script)
  ↓
Entry Splitting (by blank lines)
  ↓
AI Classification (Claude/MCP)
  ├─ Diary Entry (preserve narrative)
  ├─ Insight (preserve reflective tone)
  ├─ Context (transform to factual)
  └─ Idea (preserve speculative tone)
  ↓
Confidence Scoring (0-1.0)
  ↓
Routing Decision (>0.8 for secondary)
  ├─ Primary: Always route to main file
  └─ Secondary: Route to area-specific files (if >80% confidence)
  ↓
Transformation (for context entries only)
  ├─ Remove: pronouns, dates, feelings
  ├─ Extract: topical facts
  └─ Custom formulation: per context area
  ↓
Deduplication Check (fuzzy match 80%)
  ↓
Append to Destination Files
  ├─ With cross-links: *From:* [[daily-note#section]]
  └─ With related links: *Related:* [[context-area]]
  ↓
Smart Memory Detection
  ├─ Serena Memory (technical patterns)
  └─ Graphiti Memory (strategic insights)
  ↓
Tracker Update (mark processed, except today)
```

### Integration Points

- **Serena MCP**: Pattern matching, file operations
  - `mcp__serena__list_dir` - Find daily notes
  - `mcp__serena__search_for_pattern` - Extract sections
  - `mcp__serena__find_file` - Locate context files
  - `mcp__serena__write_memory` - Update Serena memories

- **Graphiti MCP**: Knowledge graph storage (3 instances)
  - `graphiti-mokai` - MOKAI business insights
  - `graphiti-finance` - Financial insights
  - `graphiti-personal` - Personal insights

- **Daily Notes Template** ([98-templates/daily-note.md:327](98-templates/daily-note.md#L327))
  - `### 🧠 Notes` section (extraction target)
  - Dataview queries for tasks, events, projects

- **Context Areas** (24 files across PARA structure)
  - Business: `mokai`, `mokhouse`, `accounting`, `crypto`, `soletrader`, `smsf`, `safia`, `trust`
  - Personal Development: `learning`, `mindset`, `psychedelics`
  - Health & Fitness: `health-fitness`, `diet`, `medical`, `gym`
  - Tech: `tech`, `ableton`, `mac`, `ai`, `engineering`
  - Other: `claude-code`, `harry`, `people`

## Configuration

### Skill Trigger Phrases

Auto-triggers when user says:
- "What did I work on today?"
- "Extract content from my daily note"
- "I'm done for today"
- "Wrapping up"
- "Daily summary"
- "End of day"
- References "### 🧠 Notes" section

### Environment Variables

None required (uses Claude Code's built-in AI and MCP connections)

### Setup Requirements

1. **Enable skill in Claude Code**:
   - Settings > Capabilities > Skills > Enable
   - Restart Claude Code after enabling

2. **Ensure daily note template is configured**:
   - Template location: [98-templates/daily-note.md](98-templates/daily-note.md)
   - Must include `### 🧠 Notes` section

3. **Verify destination files exist**:
   - `04-resources/diary.md`
   - `04-resources/context.md`
   - `01-areas/p-dev/insights.md`
   - `04-resources/ideas.md`

4. **Optional: Pre-create area-specific files** (auto-created if missing):
   - `business/mokai/diary-mokai.md`
   - `business/mokai/CLAUDE.md`
   - etc.

## Usage

### Auto-Triggering (Primary Method)

**Natural conversation triggers**:

```plaintext
User: "What did I work on today?"
→ Skill activates, scans today's daily note, extracts and classifies entries

User: "Extract content from my daily note"
→ Skill activates with explicit extraction intent

User: "I'm done for today, extract my notes"
→ End-of-day trigger, processes today's entries
```

### Manual Script Execution (Testing/Debugging)

```bash
# Extract specific date
python .claude/skills/daily-workflow/scripts/extract_content.py 2025-10-21

# Scan for unprocessed notes
python .claude/skills/daily-workflow/scripts/extract_content.py --scan-unprocessed
```

### Common Scenarios

**Scenario 1: End-of-Day Extraction**
```plaintext
User: "Done for today"
Claude: [Activates daily-workflow skill]
  1. Scans today's daily note
  2. Extracts 5 entries from ### 🧠 Notes
  3. Classifies: 2 Diary, 1 Insight, 1 Context, 1 Idea
  4. Presents routing plan with confidence scores
  5. User approves: "y"
  6. Routes entries to appropriate files
  7. Detects memory opportunities (Serena + Graphiti)
  8. Updates tracker
```

**Scenario 2: Specific Date Extraction**
```plaintext
User: "Extract content from my note on October 19th"
Claude: [Activates daily-workflow skill with date context]
  1. Locates 🌤️ Fri - 19th Oct 25.md
  2. Extracts and processes entries
  3. Routes to destinations
```

**Scenario 3: Batch Processing**
```plaintext
User: "Process all unprocessed daily notes from this week"
Claude: [Activates daily-workflow skill]
  1. Scans for unprocessed notes (excluding today)
  2. Processes each chronologically
  3. Presents combined routing decisions
  4. Executes after approval
```

### Approval Flow

After classification, user chooses:

- **[y]es** - Approve all routing decisions and execute
- **[n]o** - Cancel extraction
- **[e]dit** - Modify routing decisions before execution
- **[s]kip entry** - Skip specific entries

For memory updates:

- **[a] Update all** - Update all suggested memories (confidence >0.80)
- **[s] Selective** - Choose which memories to update
- **[n] Skip** - No memory updates
- **[l] Later** - Queue for end-of-day batch review

## Examples

### Example 1: Daily Diary Entry to Context Transformation

**Original Daily Note Entry** ([00 - Daily/🌤️ Mon - 21st Oct 25.md](00 - Daily/)):
```markdown
### 🧠 Notes

Today I built a Supabase database for financial tracking for MOKAI. Took forever to set up auth but got it working. Will use for invoice management.
```

**AI Classification**:
- Type: Context (96% confidence)
- Reason: Factual technical information
- Primary: `04-resources/context.md`
- Secondary: `business/mokai/CLAUDE.md` (98%), `tech/CLAUDE.md` (94%)

**Routed to** `04-resources/context.md`:
```markdown
- Supabase: Financial tracking database with auth, for invoice management
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
```

**Routed to** `tech/CLAUDE.md`:
```markdown
- Supabase: Financial tracking database with auth
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
  *Related:* [[business/mokai/context-mokai]]
```

**Routed to** `business/mokai/CLAUDE.md`:
```markdown
- Financial tracking system: Supabase database for invoice management
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
  *Related:* [[tech/context-tech]]
```

### Example 2: Smart Memory Detection

**Entry**: "Created new workflow using Supabase triggers for invoice automation"

**Detection**:
```yaml
System: Serena
Memory: system_patterns_and_guidelines
Confidence: 0.87
Update: "Invoice automation: Supabase triggers reduce manual data entry"

System: Graphiti
Instance: graphiti-mokai
Confidence: 0.85
Episode: "MOKAI invoice automation using Supabase triggers for financial workflow optimization"
```

### Example 3: Multi-Area Routing

**Entry**: "Finished mixing Nintendo track for MOK HOUSE client. Client approved on first submission."

**Classification**:
- Type: Diary (94% confidence)
- Primary: `04-resources/diary.md`
- Secondary: `business/mokhouse/diary-mokhouse.md` (97%)

**Result**:
- Original narrative preserved in both files
- Cross-links added bidirectionally
- No transformation (diary entries keep narrative voice)

## Dependencies

### External Services
None (uses Claude Code's built-in capabilities)

### Python Packages (Built-in)
- `os`, `re`, `json`, `sys` - Standard library
- `pathlib` - File path operations
- `datetime` - Date parsing and formatting
- `difflib` - Fuzzy matching for deduplication

### Internal Dependencies
- **Claude Code Skills System** - Auto-trigger mechanism
- **Serena MCP** - File operations, pattern matching, memory management
- **Graphiti MCP** - Knowledge graph storage (3 instances)
- **Daily Notes Template** - `### 🧠 Notes` section format
- **PARA Structure** - Context area organization (01-areas, 04-resources)

## Troubleshooting

### Common Issues

**Issue 1: Skill not triggering automatically**
- Cause: Skills not enabled in Claude Code settings
- Solution: Settings > Capabilities > Skills > Enable, then restart Claude Code

**Issue 2: Missing `### 🧠 Notes` section in extraction**
- Cause: Daily note uses different heading format
- Solution: Ensure daily note template matches exact format (case-sensitive, emoji included)

**Issue 3: Entries classified incorrectly**
- Cause: Ambiguous entry content or insufficient context
- Solution: Use edit mode `[e]` to correct classification, AI learns from patterns

**Issue 4: Too many secondary destinations**
- Cause: Confidence threshold too low
- Solution: Currently set to 0.8 (80%), can be increased for stricter routing

**Issue 5: Diary files not auto-created**
- Cause: File permission issues or incorrect path
- Solution: Verify write permissions, check directory structure exists

**Issue 6: Duplicate entries appended**
- Cause: Fuzzy matching threshold too low
- Solution: Currently 80% similarity, can be increased to prevent duplicates

**Issue 7: Memory detection missing opportunities**
- Cause: Entry doesn't contain trigger keywords
- Solution: Review detection keywords in [SKILL.md:119](.claude/skills/daily-workflow/SKILL.md#L119), adjust confidence threshold

**Issue 8: Wrong Graphiti instance selected**
- Cause: Routing logic based on area doesn't match entry content
- Solution: Use selective mode `[s]` to manually specify correct instance

### Debugging

```bash
# Check tracker status
cat .claude/commands/.extract-daily-content-tracker.json | jq '.'

# View last processed file
cat .claude/commands/.extract-daily-content-tracker.json | jq '.processed_files | to_entries | last'

# Reset tracker (force re-extraction)
rm .claude/commands/.extract-daily-content-tracker.json

# Test Python script directly
python .claude/skills/daily-workflow/scripts/extract_content.py --scan-unprocessed

# Verify daily note format
grep -A 10 "### 🧠 Notes" "00 - Daily/🌤️ $(date +"%a - %eth %b %y").md"
```

## Monitoring & Maintenance

### Logs
- Skill activation: Visible in Claude Code conversation (no separate logs)
- Tracker file: `.claude/commands/.extract-daily-content-tracker.json` tracks:
  - Last scan timestamp
  - Processed files with modification times
  - Entries processed per file
  - Routing decisions with confidence scores

### Monitoring
```bash
# Check recent extractions
jq '.processed_files | to_entries | map({date: .value.processed_at, count: .value.entries_count}) | sort_by(.date) | reverse | .[0:5]' .claude/commands/.extract-daily-content-tracker.json

# Total entries processed
jq '.entries_processed' .claude/commands/.extract-daily-content-tracker.json
```

### Update Frequency
- **Skill logic**: Update SKILL.md when workflow changes
- **Templates**: Update reference/templates.md when daily note format changes
- **Formatting rules**: Update reference/formatting-rules.md when transformation rules change
- **Python script**: Update when new extraction features needed

## Related Systems

- [MOKAI Daily Operations Skill](.claude/skills/mokai-daily-ops/SKILL.md) - MOKAI-specific daily workflow
- [MOK HOUSE Operations Skill](.claude/skills/mokhouse-operations/SKILL.md) - MOK HOUSE business workflow
- [Extract Daily Content Command](.claude/commands/extract-daily-content.md) - Original manual command (deprecated)
- [Daily Note Template](98-templates/daily-note.md) - Template with extraction target section
- [Serena MCP Memory](04-resources/guides/mcp/serena-mcp.md) - Memory management system
- [Graphiti Knowledge Graph](04-resources/guides/mcp/graphiti-mcp.md) - Knowledge graph storage

## Future Enhancements

### Phase 2 (Planned)
1. **Auto-categorization during writing**: Real-time classification as user types in daily note
2. **Batch processing UI**: Interactive dashboard for reviewing and approving batches
3. **Machine learning improvements**: Learn from user corrections to improve classification accuracy
4. **Custom context areas**: User-defined context areas beyond the 24 default ones
5. **Export functionality**: Export extracted data to external tools (Notion, Roam, etc.)

### Phase 3 (Exploration)
1. **Voice input integration**: Extract from voice-dictated daily notes
2. **Mobile app sync**: Sync extractions from mobile daily notes
3. **Collaboration features**: Share context/insights with team members
4. **Analytics dashboard**: Visualize entry patterns, productivity trends
5. **AI summarization**: Generate weekly/monthly summaries from extracted entries

## Change Log

- **2025-10-21**: Initial implementation
  - Created skill structure with SKILL.md, reference files, Python script
  - Implemented auto-trigger mechanism based on conversation context
  - Added AI classification for 4 entry types (Diary/Insight/Context/Idea)
  - Configured routing to 24 context areas with confidence scoring
  - Integrated Serena and Graphiti memory detection
  - Documented comprehensive formatting and transformation rules
  - Created deduplication logic with 80% fuzzy matching
  - Implemented tracker system for incremental processing
  - Added cross-linking and bidirectional references
  - Updated skills README with testing instructions

## Testing & Validation

### Manual Testing Checklist

After implementing or modifying the skill:

- [ ] Skill triggers on phrase "What did I work on today?"
- [ ] Extracts entries from `### 🧠 Notes` section correctly
- [ ] Classifies entries into correct types (Diary/Insight/Context/Idea)
- [ ] Routes to primary destinations (all types)
- [ ] Routes to secondary destinations when confidence >80%
- [ ] Transforms diary narratives to factual statements for context files
- [ ] Creates cross-links with correct format
- [ ] Auto-creates missing diary files with frontmatter
- [ ] Deduplicates entries (fuzzy match 80%)
- [ ] Updates tracker after successful extraction
- [ ] Does NOT mark today's note as processed
- [ ] Detects Serena memory opportunities
- [ ] Detects Graphiti memory opportunities (correct instance)
- [ ] Presents approval flow to user
- [ ] Handles user corrections in edit mode

### Validation Commands

```bash
# Verify skill files exist
ls -lah .claude/skills/daily-workflow/
ls -lah .claude/skills/daily-workflow/reference/
ls -lah .claude/skills/daily-workflow/scripts/

# Check SKILL.md line count (should be <500)
wc -l .claude/skills/daily-workflow/SKILL.md

# Verify Python script is executable
ls -l .claude/skills/daily-workflow/scripts/extract_content.py | grep -q 'x' && echo "Executable" || echo "Not executable"

# Test Python script
python .claude/skills/daily-workflow/scripts/extract_content.py --scan-unprocessed
```

### Success Criteria

- ✅ Correctly classify entry types (>90% accuracy with AI)
- ✅ Route to appropriate areas with good confidence (>80% for secondary)
- ✅ Show clear reasoning for routing decisions
- ✅ Allow easy manual override via approval flow
- ✅ Create valid cross-links bidirectionally
- ✅ Auto-create diary files with proper frontmatter
- ✅ Track all routing decisions in tracker JSON
- ✅ Handle incremental runs efficiently (skip already processed)
- ✅ Maintain file integrity across all destinations
- ✅ Respect >80% confidence threshold for secondary routing
- ✅ Transform diary to context correctly (remove pronouns, dates, feelings)
- ✅ Preserve narrative in diary files
- ✅ Detect memory opportunities with >75% confidence

## Notes

- **Token Efficiency**: SKILL.md kept under 500 lines, uses progressive disclosure pattern
- **Auto-Detection**: Triggers automatically based on frontmatter description
- **Hybrid Approach**: Skill for common workflows, command as manual fallback
- **Smart Context**: Only loads reference files when needed (not pre-loaded)
- **Incremental Processing**: Tracker ensures files aren't re-processed unnecessarily
- **Today's Note**: Always re-processes today's note (allows same-day updates)
- **Deduplication**: 80% fuzzy match threshold prevents near-duplicates
- **Confidence Threshold**: 80% for secondary routing balances precision and recall
- **Memory Detection**: Suggests Serena/Graphiti updates but requires user approval
- **Cross-Linking**: Bidirectional links maintain vault connectivity
