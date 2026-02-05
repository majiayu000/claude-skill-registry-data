---
name: protect
description: Annotate passing code with protection levels (@protected/@immutable/@maintainable). Use when stabilizing working features to prevent regressions.
---

# Code Protection Skill

## What This Skill Does

Systematically annotates passing code with protection levels to prevent regressions:
- Reviews manual test results to identify passing features
- Annotates code with appropriate protection levels
- Documents protected files in CODE_PROTECTION_POLICY.md
- Creates bug tasks for failing features
- Establishes baseline for pre-commit enforcement

## Protection Levels

**@immutable** - Never change
- Stable APIs that must remain backward compatible
- External integrations (Whisper API, GitHub API)
- Core data structures referenced across codebase
- Use when: Breaking changes would affect users or external systems

**@protected** - Refactor only
- Working features that pass manual tests
- Can be refactored for performance/clarity
- Cannot change behavior without approval
- Use when: Feature works correctly, needs protection from regressions

**@maintainable** - Bug fixes allowed
- Features with known bugs but working core functionality
- Can be modified to fix bugs
- Behavior changes allowed with justification
- Use when: Feature mostly works but has edge case issues

## When Claude Should Use This

Use this skill when the user:
- Says "annotate passing code" or "protect working features"
- Wants to lock down stable functionality
- Mentions "prevent regressions" or "code protection"
- References PROTECT-001 task or Phase 0 stabilization
- Has completed manual testing and wants to protect passing features

## Workflow Process

### 1. Review Manual Test Results

**Read test documentation:**
```bash
# Look for manual test results
find . -name "MANUAL_TEST*.md" -o -name "TEST_RESULTS*.md"
```

**Identify passing features:**
- Review each test case
- Mark tests as: ✅ PASS, ❌ FAIL, ⚠️ PARTIAL
- Extract passing feature list
- Note failing features for bug tasks

**Example test result format:**
```markdown
## Test 1: Voice Panel
✅ Opens with backtick key
✅ Recording works
❌ Transcription fails (timeout error)
⚠️ Insert to editor works but slow

Verdict: PARTIAL - Core functionality works, needs performance fix
```

### 2. Analyze Code for Protection Level

**For each passing feature, determine protection level:**

**Choose @immutable if:**
- External API calls (Whisper, GitHub, npm)
- Data formats that persist (TOML schema, JSON config)
- CLI commands that users depend on
- Extension activation sequence
- Breaking changes would affect users

**Choose @protected if:**
- UI components that work correctly
- Feature workflows that pass tests
- Services with correct business logic
- Can be refactored but behavior must stay same
- Most common protection level

**Choose @maintainable if:**
- Features with known bugs
- Partial test passes
- Needs improvement but core works
- Bug fixes expected

### 3. Annotate Code with Protection Comments

**Annotation format:**
```typescript
/**
 * @protected
 * Locked: 2025-11-06 (v0.16.7)
 * Test: MANUAL_TEST_v0.16.7.md - Test 2.1 (Voice Panel opens with backtick)
 * Status: PASSING - Core functionality works
 *
 * Voice panel activation via backtick key.
 * DO NOT modify without approval - breaks user workflow.
 */
export function activateVoicePanel() {
    // implementation
}
```

**For @immutable APIs:**
```typescript
/**
 * @immutable
 * Locked: 2025-11-06 (v0.16.7)
 * API: External Whisper API integration
 * Status: STABLE - Backward compatible
 *
 * Whisper API client for transcription.
 * NEVER change interface - external dependency.
 */
export class WhisperClient {
    // implementation
}
```

**For @maintainable code:**
```typescript
/**
 * @maintainable
 * Locked: 2025-11-06 (v0.16.7)
 * Test: MANUAL_TEST_v0.16.7.md - Test 3.2 (Sprint loader partial pass)
 * Status: PARTIAL - Works but has bugs
 * Known issues: Slow loading (>2s), occasional TOML parse errors
 *
 * Sprint loader service.
 * Bug fixes allowed - performance and parsing issues known.
 */
export class SprintLoader {
    // implementation
}
```

**Placement rules:**
- Place annotation IMMEDIATELY before function/class/export
- Include lock date (today's date)
- Reference test case from manual test document
- Note status (PASSING, STABLE, PARTIAL)
- Explain why protected and what breaks if changed

### 4. Document in CODE_PROTECTION_POLICY.md

**Create or update the protection policy document:**

```markdown
# Code Protection Policy

**Status:** ✅ ACTIVE (v0.16.7 - 2025-11-06)

## Protected Files

### @immutable Files (Never Change)
| File | Lock Date | Test Reference | Reason |
|------|-----------|----------------|--------|
| vscode-lumina/src/services/whisperClient.ts | 2025-11-06 | Test 1.1 | External API integration |
| vscode-lumina/src/services/githubClient.ts | 2025-11-06 | Test 4.2 | GitHub API integration |

### @protected Files (Refactor Only)
| File | Lock Date | Test Reference | Reason |
|------|-----------|----------------|--------|
| vscode-lumina/src/extension.ts | 2025-11-06 | Test 1.0 | Extension activation |
| vscode-lumina/src/commands/SprintLoader.ts | 2025-11-06 | Test 2.3 | Sprint loading |
| vscode-lumina/src/services/AutoTerminalSelector.ts | 2025-11-06 | Test 3.1 | Terminal selection |

### @maintainable Files (Bug Fixes Allowed)
| File | Lock Date | Test Reference | Known Issues |
|------|-----------|----------------|--------------|
| vscode-lumina/src/commands/voicePanel.ts | 2025-11-06 | Test 1.2 | Slow insert, timeout errors |

## Enforcement

Protection enforced via:
1. Pre-commit hook (validates protection on commit)
2. Static analysis (scripts/validate-protection.js)
3. Code review (reviewer checks for unauthorized changes)
4. CI/CD pipeline (blocks merges with protection violations)

## Override Process

If you need to modify protected code:

1. **Document justification** in commit message:
   ```
   PROTECTED: Fix critical bug in WhisperClient

   Justification: Whisper API changed, breaking compatibility.
   Files modified: vscode-lumina/src/services/whisperClient.ts
   Protection level: @immutable → requires architecture approval
   Approval: [Reference issue/PR/discussion]
   ```

2. **Get approval** (based on protection level):
   - @immutable: Architecture review + user impact assessment
   - @protected: Technical lead approval
   - @maintainable: Self-approval (document justification)

3. **Update tests** after change:
   - Re-run manual tests
   - Update test document with new results
   - Update protection annotation if status changes

## Audit Trail

View protection changes via git log:
```bash
# Show all protected code changes
git log --grep="PROTECTED:" --oneline

# Show changes to specific protected file
git log --grep="PROTECTED:" -- vscode-lumina/src/services/whisperClient.ts
```
```

### 5. Create Bug Tasks for Failing Features

**For each failing test, create a bug task:**

**Task format:**
```toml
[tasks.BUG-001]
id = "BUG-001"
name = "Fix voice panel transcription timeout"
phase = "phase-0b-ux-polish"
assigned_engineer = "engineer_1"
status = "pending"
description = "Transcription fails with timeout error after 30s"
estimated_lines = 50
estimated_time = "1-2 hours"
dependencies = ["PROTECT-001"]
agent = "infrastructure-agent"

deliverables = [
    "Increase timeout to 60s",
    "Add retry logic (3 attempts)",
    "Update error message to be user-friendly",
    "Test with long recordings (>2min)"
]

validation_criteria = [
    "Transcription completes for 2min recording",
    "Timeout error no longer occurs",
    "Retry logic works (verify in logs)"
]

why = """
Manual test Test 1.3 failed: Transcription timeout after 30s.
Whisper API can take 45-60s for long recordings.
Needs longer timeout + retry for reliability.
"""

context = """
Test reference: MANUAL_TEST_v0.16.7.md - Test 1.3
Error: "Whisper API timeout after 30000ms"
File: vscode-lumina/src/services/whisperClient.ts:142

Current timeout: 30s
Whisper API avg response: 15-45s (varies by length)
Long recordings (>2min): 45-60s response time

Fix: Increase timeout to 60s, add 3-retry logic
"""
```

**Add bug tasks to sprint TOML:**
- Group under `phase-0b-ux-polish`
- Depend on PROTECT-001 (after protection annotations)
- Assign to appropriate agent
- Include test reference and error details

### 6. Verify Protection Annotations

**Run validation script (after PROTECT-002 completes):**
```bash
node scripts/validate-protection.js
```

**Manual verification checklist:**
- [ ] All passing features annotated
- [ ] Protection level appropriate for each file
- [ ] Annotations include lock date + test reference
- [ ] CODE_PROTECTION_POLICY.md lists all protected files
- [ ] Bug tasks created for all failing features
- [ ] Each bug task references test case

## Example: Complete Protection Workflow

**Scenario: Protect Voice Panel feature after manual testing**

**Step 1: Review test results**
```markdown
# MANUAL_TEST_v0.16.7.md

## Test 1: Voice Panel
1.1 Open panel with backtick key → ✅ PASS
1.2 Start recording → ✅ PASS
1.3 Stop recording → ✅ PASS
1.4 Transcribe audio → ❌ FAIL (timeout)
1.5 Insert into editor → ✅ PASS

Verdict: PARTIAL - 4/5 pass, transcription timeout issue
```

**Step 2: Determine protection levels**
- Voice panel activation (Test 1.1) → @protected (UI feature, works)
- Recording logic (Test 1.2-1.3) → @protected (core feature, works)
- Transcription (Test 1.4) → @maintainable (has bug, needs fix)
- Editor insertion (Test 1.5) → @protected (works, but slow)

**Step 3: Annotate code**

File: `vscode-lumina/src/commands/voicePanel.ts`
```typescript
/**
 * @protected
 * Locked: 2025-11-06 (v0.16.7)
 * Test: MANUAL_TEST_v0.16.7.md - Test 1.1
 * Status: PASSING
 *
 * Activates voice panel when backtick key pressed.
 * DO NOT modify without approval - user workflow depends on this.
 */
export function activateVoicePanel() { ... }

/**
 * @maintainable
 * Locked: 2025-11-06 (v0.16.7)
 * Test: MANUAL_TEST_v0.16.7.md - Test 1.4 (FAIL)
 * Status: PARTIAL - Timeout errors on long recordings
 * Known issue: 30s timeout too short for Whisper API
 *
 * Transcription logic - bug fix needed for timeout.
 */
async function transcribeAudio() { ... }
```

**Step 4: Update CODE_PROTECTION_POLICY.md**
```markdown
## @protected Files
- vscode-lumina/src/commands/voicePanel.ts (activateVoicePanel) - Test 1.1

## @maintainable Files
- vscode-lumina/src/commands/voicePanel.ts (transcribeAudio) - Test 1.4 (timeout bug)
```

**Step 5: Create bug task**
```toml
[tasks.BUG-001]
id = "BUG-001"
name = "Fix transcription timeout"
# ... (see format above)
```

**Step 6: Commit**
```bash
git add vscode-lumina/src/commands/voicePanel.ts docs/CODE_PROTECTION_POLICY.md internal/sprints/ACTIVE_SPRINT.toml
git commit -m "PROTECT-001: Annotate voice panel with protection levels

- @protected: activateVoicePanel (Test 1.1 PASS)
- @maintainable: transcribeAudio (Test 1.4 FAIL - timeout)
- Created BUG-001 for transcription timeout fix
- Updated CODE_PROTECTION_POLICY.md

Files: 3 files changed, 45 insertions(+)"
```

## Integration with Other Protection Tasks

**PROTECT-001 → PROTECT-002 → PROTECT-003**

1. **PROTECT-001 (This Skill):** Annotate code with protection levels
2. **PROTECT-002:** Build pre-commit enforcement (validates annotations)
3. **PROTECT-003:** Complete CODE_PROTECTION_POLICY.md documentation

**After PROTECT-002 completes:**
- Pre-commit hook will validate protection annotations
- Modifications to @protected files will require approval
- Commit messages must include "PROTECTED:" prefix
- Audit trail in git log

**After PROTECT-003 completes:**
- CODE_PROTECTION_POLICY.md fully documented
- Developers know override process
- Enforcement mechanisms explained
- Audit commands available

## Related Files

- `internal/sprints/ACTIVE_SPRINT.toml` - PROTECT-001 task definition
- `docs/CODE_PROTECTION_POLICY.md` - Protection policy (created by this skill)
- `scripts/validate-protection.js` - Validation script (created in PROTECT-002)
- `.git/hooks/pre-commit` - Pre-commit enforcement (updated in PROTECT-002)
- `.claude/CLAUDE.md` - Known Issues section (references historical bugs)

## Historical Context

**Why code protection is critical:**

### v0.13.23: Native dependency broke extension (9 hours to fix)
- Added `@nut-tree-fork/nut-js` to package.json
- Extension activation failed for all users
- Required replacing with VS Code APIs
- Prevention: @immutable annotation on package.json dependencies

### v0.15.31-32: Runtime npm dependency broke extension (2 hours to fix)
- Added `glob` package at runtime
- Extension excluded it via --no-dependencies flag
- Activation failed for all users
- Prevention: @protected annotation on dependency imports

**Protection prevents repeat of costly bugs.**

**Pattern:** Lock down working code, fix bugs separately, prevent regressions.

## Tips

**Start with high-impact files:**
1. extension.ts (activation)
2. whisperClient.ts (external API)
3. Core services (sprint loading, terminal selection)
4. Working UI features

**Batch annotations by file:**
- Annotate all functions in one file together
- Keep protection consistent within a file
- Update CODE_PROTECTION_POLICY.md after each file

**Create bug tasks immediately:**
- Don't delay bug task creation
- Include all failing tests
- Reference original test document
- Group in phase-0b-ux-polish

**Document reasoning:**
- Explain why this protection level
- Note what breaks if changed
- Reference test case
- Include status (PASSING/STABLE/PARTIAL)
