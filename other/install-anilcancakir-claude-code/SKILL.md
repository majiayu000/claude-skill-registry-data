---
name: install
description: "Set up ac for your user, or upgrade an earlier setup: my-coding and my-language skills, the global CLAUDE.md and settings.json, each write gated."
argument-hint: "[--upgrade] [--dry-run] [--skip-skills] [--skip-settings] [--skip-claude-md]"
effort: medium
disable-model-invocation: true
---

# /ac:install

Tunes your user-scope environment so the ac workflow replaces the matching Claude Code built-ins. Safe defaults apply silently; anything that loosens a gate or touches a secret is opt-in.

Request: $ARGUMENTS

Precondition: the ac plugin is already installed and loaded. This command does not bootstrap the install and never calls `/plugin marketplace add` or `/plugin install`. It writes only under `~/.claude/`, and only the files each phase names; the one exception is the wrapper line 3d adds to a shell rc file, and only after the operator says yes.

## Phase 0: Identity, arguments, preflight, languages

You are the `/ac:install` orchestrator. You interview the operator, delegate skill authoring to `ac:skill-creator`, and write user-scope config behind explicit gates.

**CAN**: Use `Read`, `Write`, `Edit`, `Bash`, `AskUserQuestion`. Invoke `ac:skill-creator` through the `Skill` tool. Probe the ac MCP server with `mcp__plugin_ac_ac__resolve-library`. Write the `.proposed` sidecar, the `.bak-ac-install` backups, the `~/.claude/ac-install.json` answer record, and the stable rules copy at `~/.claude/ac/working-rules.md`.

**CANNOT**: Hand-write `my-coding` or `my-language` SKILL.md content; that is `ac:skill-creator`'s job. Blind-overwrite `~/.claude/CLAUDE.md` or `~/.claude/settings.json`; both go through a backup plus a gate. Write settings keys from memory; the Phase 4 reference is the only source. Edit anything outside `~/.claude/`, apart from the 3d wrapper edit to a shell rc file after an explicit yes. Widen an allow rule past the literal server segment (`mcp__plugin_ac_ac__*`, never `mcp__*`).

**MUST**: Honour every flag from 0a for the whole run. Under `--dry-run`, render every planned change and call no `Write` or `Edit`. Back up each file before rewriting it. Leave an existing skill alone unless the operator picks Recreate. Read the Phase 3 template and the Phase 4 reference rather than reproducing either from this body: both have drifted from a restated copy before, and a stale copy fails silently.

### 0a. Parse arguments

Mirror the `commit.md` Phase 0 flag scan. Read `$ARGUMENTS` once:

1. `--dry-run` sets `DRY_RUN`. Every phase plans and prints, nothing is written.
2. `--skip-skills` sets `SKIP_SKILLS`. Skips Phases 1 and 2.
3. `--skip-claude-md` sets `SKIP_CLAUDE_MD`. Skips Phase 3.
4. `--skip-settings` sets `SKIP_SETTINGS`. Skips Phase 4.
5. `--upgrade` sets `UPGRADE`. Brings an earlier setup up to this plugin version and asks only what it has never asked; 0e says what changes per phase. It combines with every other flag.
6. Ignore any other token.

### 0b. Detect the environment

Record each result. A failed detection is noted and never blocks the run.

| Check | Records |
|---|---|
| `uname -ms` | OS |
| `test -d ~/.claude/skills/my-coding` | `MY_CODING_EXISTS` |
| `test -d ~/.claude/skills/my-language` | `MY_LANGUAGE_EXISTS` |
| `test -f ~/.claude/CLAUDE.md` | `CLAUDE_MD_EXISTS` |
| `test -f ~/.claude/settings.json` | `SETTINGS_EXISTS` |
| `test -d ~/.claude/skills/my-workflow` | `LEGACY_MY_WORKFLOW` |
| `jq -r .version ${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` | `PLUGIN_VERSION` |
| `jq -c . ~/.claude/ac-install.json` | `RECORD` (absent or unparsable means none), and `PRIOR_VERSION` from its `version` |
| the conjunction below, run only when `SETTINGS_EXISTS` | `SCHEDULING_TRIMMED` |

```
jq -e '((.permissions.deny // []) | map(split("(")[0])) as $d
       | ($d | index("ScheduleWakeup")) and ($d | index("CronCreate"))
         and ((.skillOverrides.schedule // "") == "off")' ~/.claude/settings.json
```

A non-zero exit, a missing file, or a `jq` failure all mean false. `SCHEDULING_TRIMMED` decides one conditional section in Phase 3 and is read from disk rather than asked. The predicate tests one key per claim the section makes (cron gone, wakeup gone, scheduling skills off). It reads the global `~/.claude/settings.json` only, since a project-scope deny would make the claim false in other projects, and it fails closed. It cannot come from the Phase 4 Group D gate, which runs after Phase 3 has written the file; on a fresh machine it is false, and Phase 4's last step closes the seam when Group D then turns the trim on.

Earlier versions scaffolded a `my-workflow` skill. The discipline now ships as `${CLAUDE_PLUGIN_ROOT}/references/working-rules.md`, so a surviving copy duplicates it. Do not delete it; surface it in Phase 5.

### 0c. Probe ac MCP reachability

Call `mcp__plugin_ac_ac__resolve-library` with a trivial query such as `react`. Record `MCP_REACHABLE` true on a result, false on error, timeout, or tool-not-available. It decides only how the blocked-pages bullet in `My workflow` is worded; working-rules.md names the ac MCP tools whatever the probe says (3b).

If the tool path does not resolve, say that `/mcp` confirms the exact server name. The bundled server is keyed `ac` in `.mcp.json` and the host namespaces it as `plugin_ac_ac`, so the runtime tools are `mcp__plugin_ac_ac__*`.

### 0d. The language pair

Two answers, taken here rather than in Phase 3 because Phases 1 and 2 both need them and both run first. Skip this step entirely when `SKIP_SKILLS` and `SKIP_CLAUDE_MD` are both set, since nothing left to run consumes either value.

Ask as two questions in one `AskUserQuestion` call:

1. `CONVERSATION_LANGUAGE`, the language you and the operator talk in.
2. `ARTIFACT_LANGUAGE`, the language code, identifiers, comments, doc blocks, commit messages and documents are written in.

Under `UPGRADE`, 0e replaces this question. Default both to English and never infer the second from the first. They are independent by design, and Turkish conversation with English artifacts is the case the split exists for. When `CLAUDE_MD_EXISTS`, read the file first and offer what it already says as the pre-filled option rather than asking cold; a `Core principles` section written by a previous run answers both.

Both values feed the Phase 1 brief, the Phase 2 brief, and the Phase 3 placeholders. Collect them once here and pass the same strings to all three.

Run this even under `--dry-run`: a question whose answer feeds a preview is still asked, while one whose only effect is a settings write is not.

### 0e. Upgrade mode

`--upgrade` is for a machine an earlier `/ac:install` already set up, after `claude plugin marketplace update ac` and `claude plugin update ac@ac` have pulled the new version and Claude Code has restarted. The full run is already idempotent; upgrade changes what it asks: only options added since, plus one gate per file that actually changes.

An earlier install leaves at least one of these: `RECORD`, the ac fence markers in `~/.claude/CLAUDE.md`, either `.bak-ac-install` backup, or the Group C fingerprint (`Agent(Plan)` in `permissions.deny` together with `env.CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS`). With none of them there is nothing to upgrade from: say so, drop `UPGRADE`, and run the full install. Without `RECORD` but with any of the others, this is a setup from before the record existed; carry on, and the reference's "what counts as answered" rule infers the earlier answers from the keys on disk. When `PRIOR_VERSION` is newer than `PLUGIN_VERSION`, stop and say the plugin is older than the setup it would upgrade.

Without `--upgrade`, check the same evidence right after 0b. When any of it is present, ask once (header `Upgrade?`, options `Run as an upgrade (Recommended)` / `Full install`). On `Run as an upgrade`, set `UPGRADE` and continue.

Per phase, under `UPGRADE`:

- **0d.** Read both languages from the current CLAUDE.md and do not ask. Ask only when that file does not state one of them.
- **Phases 1 and 2.** An existing skill is kept without the 1a or 2a question; neither skill is regenerated by an upgrade, because its content is the operator's interview, not plugin content. A missing one is offered with `Create` / `Skip` unless the record holds its `S.` id; Create runs 1b and 1c (or 2b and 2c), and the answer is recorded so a skill left out on purpose is not offered again.
- **Phase 3.** Every placeholder comes from the current file, an old-layout file included (3a says where its fragments sit); ask the 3a rounds only for a placeholder the current file cannot fill, which is how a placeholder the template gained since shows up. An optional line the current file does not carry (the stack line, the blocked-pages bullet, extra skills or anti-patterns) was answered with none, so leave it out without asking. The git sentence in `Identity` is not such a line either: it is fixed template text, so take the template's wording over the current file's, without asking. Skip 3b's light tuning of the Skills wording and carry the current file's lines for the placeholders verbatim, so a template that did not change rebuilds the same bytes. The 3a confirmation moves into the 3c gate: render the filled values inside that question, alongside `diff` output between the current fenced block and the proposed one, so one question covers both; a wrong value comes back as the gate's free-text answer, and you rebuild and ask again. When the proposed file is byte-identical to the current one, write nothing, ask nothing, and report it unchanged. 3d runs either way; it asks the wrapper question only when no wrapper already carries the flag, and the question-timeout question only when the record holds no `W.afk`.
- **Phase 4.** Groups A and C and the migration strip run as always. Groups B, D and E show only the options that are not answered by the reference's rule; drop a question left with no options, and turn any question left with one option into a single-select question under the same header with `Apply` / `Skip` options, since `AskUserQuestion` needs two per question. When an option has widened since the record (some of its keys present, some not), name the missing keys in the question. Under `--dry-run`, ask nothing and list the option ids a real upgrade would ask, with the missing keys of any widened one. Group F runs as always; its answer lives on disk. Group G asks only when the record holds no `G.session-title` and the key is absent. Skip the MCP token prompt; a plain `/ac:install` sets the token.
- **Phase 5.** Report the move from `PRIOR_VERSION` (or "pre-record") to `PLUGIN_VERSION` and list the options asked for the first time.

## Phase 1: my-coding skill

Skip when `SKIP_SKILLS`. Under `UPGRADE`, keep an existing skill without asking (0e).

### 1a. Skip-if-present gate

When `MY_CODING_EXISTS`, ask before touching it:

```
AskUserQuestion({
  header: "my-coding?",
  question: "A my-coding skill already exists at ~/.claude/skills/my-coding/. How should I handle it?",
  options: [
    {label: "Skip (Recommended)", description: "Leave the existing my-coding skill untouched and continue."},
    {label: "Recreate", description: "Run the style interview and regenerate my-coding from scratch."}
  ]
})
```

On Skip, go to Phase 2. Otherwise run 1b and 1c, which is also the path when the skill is absent.

### 1b. Style interview

Through `AskUserQuestion`, one decision per question:

1. Primary stack and the language versions in play.
2. Non-negotiable rules (multiSelect: type everything, identifiers and comments in `ARTIFACT_LANGUAGE` only, TDD, zero linter suppressions, minimal diff, plus a free-text option). Render the language option with the 0d answer substituted, so the operator is confirming a concrete rule rather than an abstract one.
3. Architecture philosophy: how business logic is organised.
4. Formatting: line width, indentation, trailing commas, import order.
5. Testing discipline: test-first, test-alongside, or post-implementation.
6. Pet peeves and anything the rounds above missed.

Compile a brief: stack and versions, each rule with a one-line reason, the architecture stance, the formatting table, the testing stance, the pet peeves.

### 1c. Delegate to ac:skill-creator

Under `--dry-run`, print the brief and the target path and skip the invocation. Otherwise `Skill({skill: "ac:skill-creator"})`, handing it the brief plus these instructions:

- Create `my-coding` at `~/.claude/skills/my-coding/`.
- Fill `${CLAUDE_PLUGIN_ROOT}/references/coding-style-template.md` from the brief. Its `<artifact language>` placeholder takes the 0d answer; state the value in the brief rather than leaving the creator to infer it from the stack. Rewrite both halves of that rule's example in the artifact language too: the shipped WRONG case is a Turkish identifier, so it silently becomes the CORRECT case for an operator whose artifact language is Turkish.
- Author one `references/<language>.md` per primary stack. Keep the SKILL.md body lean and push language detail into those files.
- Author `references/anti-patterns.md` carrying the template's required seed entries, whatever the interview surfaced. State this in the brief rather than trusting the creator to find it in the template: one run produced a thirteen-row table and landed none of the seeds.

Do not write the SKILL.md yourself. The creator owns file content; this command supplies the brief and the template path.

## Phase 2: my-language skill

Skip when `SKIP_SKILLS`. Same shape as Phase 1, the `UPGRADE` rule included.

### 2a. Skip-if-present gate

When `MY_LANGUAGE_EXISTS`:

```
AskUserQuestion({
  header: "my-language?",
  question: "A my-language skill already exists at ~/.claude/skills/my-language/. How should I handle it?",
  options: [
    {label: "Skip (Recommended)", description: "Leave the existing my-language skill untouched and continue."},
    {label: "Recreate", description: "Run the voice interview and regenerate my-language from scratch."}
  ]
})
```

On Skip, go to Phase 3. Otherwise run 2b and 2c, which is also the path when the skill is absent.

### 2b. Voice interview

1. Which modes matter: documentation, article, commit message, code comment, PR description.
2. How formality shifts across those modes.
3. The traits that make their writing recognisable.
4. Signature phrases, or none.
5. Whether they supply writing samples; if so, collect the excerpts or a path.

Compile a brief: active modes with opening and closing patterns, the tone spectrum, the voice traits, the signature phrases, any samples.

### 2c. Delegate to ac:skill-creator

Same gating as 1c. Instructions:

- Create `my-language` at `~/.claude/skills/my-language/`.
- Fill `${CLAUDE_PLUGIN_ROOT}/references/language-style-template.md` from the brief. Its first two Writing Rules are fixed content, the scoped dash rule and the content-sets-length rule; keep both verbatim and fill only the numbered placeholders after them. Delete any numbered placeholder the interview did not fill rather than inventing a rule to fill it: 2b collects modes, formality, traits, phrases and samples, and no rules at all, so an unfilled slot is the normal case. Prose the operator writes for people is in `ARTIFACT_LANGUAGE`, which the brief states.
- Write any supplied samples to `references/examples.md` and point the SKILL.md at it.

## Phase 3: global CLAUDE.md

Skip 3a to 3c when `SKIP_CLAUDE_MD`; 3d runs regardless, because the file it checks may already be in the new layout. Under `UPGRADE`, 0e moves the 3a confirmation into the 3c gate and skips the gate when nothing changed.

### 3a. Fill the placeholders

Read `${CLAUDE_PLUGIN_ROOT}/references/global-claude-md-section-template.md` and the operator's current `~/.claude/CLAUDE.md`, in that order, before asking anything.

On an upgrade the current file is the answer sheet: identity, conversation language, trigger words, test tools and stack are recorded in the copy this phase replaces. Pre-fill what you can, then fall back to the rounds below only for what the current file leaves open, or when there is no current file. Fill the author identity in `Identity` and the given name in `Role` from one string whichever branch you are on: take the full `name <email>` once and derive `Role`'s given name from that same value, never from a second line of the source. The git sentence after it carries no value; round 1 says why.

An old-layout file is one whose block still carries any of the workflow headings `${CLAUDE_PLUGIN_ROOT}/references/working-rules.md` now delivers (every `# ` heading between its `ac:working-rules` markers after the title), or a `## Watching something over time` section. Read those sections only to carry the operator's own fragments into `## My workflow`, then drop them; everything else in them is plugin text that working-rules.md now ships:

- The end-to-end trigger words: the quoted phrases in the `Reading the request` row that ends "treat real usage as the finish line", every phrase kept.
- The stop phrasings in the conversation language: the quoted examples in the `Run to completion` bullets ("Announcing the next step", "Offering to continue") that are not English. working-rules.md carries English examples only, and the operator's own phrasings are what the model actually sees.
- The stack-specific verification line: the `Before you call it done` bullet shaped "On <stack>, <command> clean".
- The real-world test tools: the parenthetical in the `Before you call it done` bullet "When I name the tool for the test (...)".
- The blocked-pages bullet: any `Web research` bullet beyond the built-in, `mcp__plugin_ac_ac__web-fetch` and `gh` bullets that working-rules.md carries, carried with its facts kept.
- The Watching sentence: not carried as text; `SCHEDULING_TRIMMED` decides it, as on a fresh install.

Fill each into the template's `My workflow` shape rather than copying the old line, which had a different shape. The 3c diff then shows every dropped line, so a hand edit the operator wants to keep surfaces at the gate and comes back as its free-text answer.

Pre-filling replaces the rounds; it does not replace the confirmation (under `UPGRADE`, 0e moves it into the 3c gate rather than dropping it). Render the filled values as a list inside the `question` text of one `AskUserQuestion`, with options `Correct` / `Fix identity` / `Fix working style`, and let the operator answer before you build anything, however obvious the values look.

Language is deliberately not on that list. 0d already asked, and Phases 1 and 2 were briefed with the answer, so a change accepted here would leave those skills disagreeing with this file. If the operator raises it anyway, do not silently take the new value: name the skills built on the old one and offer a Recreate pass over Phases 1 and 2 alongside the corrected CLAUDE.md. The confirmation is not skippable: a source file that disagrees with itself is the normal case (a name pre-filled from two lines once shipped as `Anilcan` in `Role` and `Anılcan` in `Identity`), and nothing downstream checks it.

Interview against the placeholders the template actually carries, never a count or a restated roster:

- Several placeholders occur more than once, and several others are whole conditional lines that either render or vanish. Count them in the template you just read, replace every occurrence, and treat a conditional line as handled only once you have decided which way it goes. Substituting only the first occurrence ships a raw placeholder into a live CLAUDE.md.
- Not every angle bracket is one. The generated-by HTML comment under the start marker and the email inside the filled `Identity` value are not placeholders. A placeholder reads as a description of what to substitute, not as an argument.
- When the operator already has an optional section or bullet, carry theirs forward rather than regenerating it; an earlier install's blocked-pages content (a `## Blocked pages` section, or the extra `Web research` bullet of the layout before working-rules.md) moves into `## My workflow` as one bullet with its facts kept. The blocked-pages shape guidance is for a new user; never compress a line that already earned its length.

The rounds, for a fresh install or an unanswered placeholder:

1. Identity: one answer used twice. `Identity` takes the full `name <email>` string, and `Role` takes the given name out of that same string, never a value sourced separately. Offer `git config --global --get user.name` and `--get user.email` as the pre-filled option and let the operator correct it: a transliterated git identity is common, and this file is where the accented form belongs. The git sentence after it is fixed text, emitted as the template writes it, with no value to fill: commits keep whatever `git config` holds. Do not fold git work back into the author rule: that is what led the model to pass `git -c user.email=` or `--author` and to add a `Co-Authored-By` trailer naming the operator.
2. Language. Both answers were taken in 0d, before Phase 1 needed them; do not ask again. Three things follow from the pair. Append the organisation-override sentence to the conversation-language bullet only when that answer is not English; it is the whole rule for someone whose employer mandates English and noise for everyone else. Emit the language-split bullet only when the two answers differ, because on a matching pair it explains a distinction that does not exist. And keep both values consistent with what Phases 1 and 2 were briefed with, since the generated skills state the artifact language too.
3. Working style, in one multi-question call: the end-to-end trigger words meaning "verify through actual use, do not stop at a green build" (defaults "ship it", "make it work"); the real-world-test tools (multiSelect, defaults SSH, browser automation, HTTP client, REPL, plus free text); and the primary stack for the optional stack-specific verification line, or "skip" to drop it.
4. The optional sections. First, any skill beyond `my-coding` and `my-language` whose trigger has to hold even when its own listing entry is dropped, each becoming one line in `Skills`. Ask it as "which of your other skills would you not want to lose", list the ones on disk at `~/.claude/skills/` as options, and take none as a valid answer (an overflowing skill listing drops the least-invoked skill first; this file is not subject to that budget). Then any coding anti-patterns beyond the ones the template ships, appended as bullets in the same voice or omitted. Then whether a third fetch path exists for pages a WAF blocks, after the built-in and the ac MCP fallback both fail; if so collect the tool, the conditions that hand off to it, and the one thing that is easy to get wrong, and write one bullet in `My workflow` from those three. If not, drop the placeholder line.

Run this even under `--dry-run`: the answers feed the preview, and a preview built without them does not match what a live run writes.

### 3b. Build the proposed file

The generated file is everything between the `<!-- ac:delegation:start -->` and `<!-- ac:delegation:end -->` markers. Reproduce every heading it carries, `#` and `##` alike, in the order it carries them; the first is a level-one `# Role`, so a scan written for `##` drops it.

The template is the only roster; do not restate its section names or a line count here.

The template's HTML-comment header carries the keep test, what is deliberately left out, and the grep recipe for re-auditing against a shipped binary. Read it before changing a section. Two of its conclusions change what this phase writes: notes stay HTML comments (the memory loader strips them; `[//]: # (...)` would ship as visible text), and the file carries no "verify your work" instruction (it causes over-verification on the current Opus generation); put such a requirement in the success check instead.

Keep every static section verbatim and substitute only the placeholders. Drop the stack-specific verification line when the operator answered "skip", the blocked-pages bullet when they reported no third fetch path, and the Watching sentence when `SCHEDULING_TRIMMED` is false. When `MCP_REACHABLE` is false, word the blocked-pages bullet as following the built-in fetch alone. Light tuning of the Skills wording from the Phase 1 and 2 answers is fine. Do not add sections.

The workflow text (`Reading the request` through `Before you call it done`) is not in this block. It ships as `${CLAUDE_PLUGIN_ROOT}/references/working-rules.md` and reaches the main thread (never a subagent) through `--append-system-prompt-file` on a wrapper launch or the plugin's SessionStart hook otherwise; the block keeps what a subagent still needs, the one-line Delegation grant, and the operator's own fragments in `My workflow`. Do not copy a working-rules section back into the block, and do not tailor working-rules.md per operator: it is static plugin text, delivered verbatim. Known limitation: when `MCP_REACHABLE` is false it still names `mcp__plugin_ac_ac__web-fetch` and `web-code-search`; the rules' missing-tool clause in `Run to completion` covers that.

### 3c. Merge on the fence markers

The markers are the only anchor. Never fuzzy-match on headings.

When `CLAUDE_MD_EXISTS` is false, write the block straight to `~/.claude/CLAUDE.md`, or print it under `--dry-run`.

Otherwise read the current file and take one of three paths:

1. **Both markers, in order.** Replace everything between them inclusive, and preserve every byte outside verbatim.
2. **Neither marker.** Append the block after the operator's content.
3. **One marker, or the two out of order.** Stop. Do not append and do not guess the boundary (a stray marker makes the next case-1 replace swallow whatever sits between them). Report which marker was found and at which line, name the two fixes (delete the stray marker, or add its partner around the block it was meant to fence), leave the file untouched, and go to Phase 4.

**The collision check, in cases 1 and 2.** Scan the bytes outside the fenced region for headings matching `^#{1,2} ` and list every one the block also carries. The block generates `Role`, `Core principles`, `Identity` and `Anti-patterns`, which an operator has often hand-written, and a case-1 replace never reaches those copies; two conflicting rules are worse than either alone.

List as collisions, too, every out-of-fence heading matching one of the workflow headings in working-rules.md (the same set 3a reads), at either level: while any of them stands as a whole `## ` line anywhere in the file, the SessionStart hook treats the file as old layout and stays silent, so the stale copy becomes the only one. Inside the fenced region they are no collision: case 1 replaces them.

Name the collisions and let the operator resolve them. You cannot tell which copy they meant.

**The exception.** When every out-of-fence heading is one the block now generates or one working-rules.md delivers, nothing out there is losable; all of it is superseded. Offer replacing the whole file as the first gate option, naming the superseded headings and the backup path. Do not offer it on a partial collision, where a surviving heading means content the block does not carry.

**Before the gate**, confirm the substitution completed: grep the result for `<` followed by a lowercase letter and check every hit is an HTML comment or an email in angle brackets. Then confirm the result stays under 200 lines, and if it does not, report the count rather than cutting anything.

**Then gate the write.** Under `--dry-run`, print the result and stop. Otherwise back the file up with `cp -n ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak-ac-install` (non-clobbering, so a re-run keeps the pristine first backup). Write the result to `~/.claude/CLAUDE.md.proposed` and ask:

```
AskUserQuestion({
  header: "Apply?",
  question: "Your global CLAUDE.md already exists. The proposed merge is at ~/.claude/CLAUDE.md.proposed. How should I handle it?",
  options: [
    {label: "Replace the whole file (Recommended)", description: "Only offered when every out-of-fence heading is superseded. Name them here, and name the backup path."},
    {label: "Apply the merge", description: "Replace the fenced region only and keep your out-of-fence sections. Name the collisions you would be left to reconcile."},
    {label: "Skip", description: "Leave the original in place; keep the .proposed file for manual review."},
    {label: "Edit", description: "Leave the .proposed file for you to edit; re-run after editing to apply."}
  ]
})
```

Drop the first option when the collision is partial or absent and recommend `Apply the merge` instead. A four-option list whose first option is wrong for the situation is worse than a three-option list.

On either apply path, write the file and delete the sidecar. On Skip, leave both. On Edit, leave the sidecar and say the operator can edit it and copy it over. Name the backup path in Phase 5 either way.

### 3d. Deliver the working rules

Exactly one copy of the working rules may reach a main-thread context. The SessionStart hook (`${CLAUDE_PLUGIN_ROOT}/hooks/session-start-working-rules.sh`) emits them on every launch unless the global CLAUDE.md still carries two or more moved headings or the launch sets `AC_WORKING_RULES_APPENDED=1`; a wrapper that passes the file sets that variable on the same command. For a session first opened without the wrapper, `--resume` and `-c` ignore the new append flags, and the hook emits anyway from the transcript's `prompt_snapshot`. Say in Phase 5 that the wrapper reaches the system prompt of new sessions only.

1. **Write the stable copy.** A wrapper points at the text between the `ac:working-rules` markers, never at the plugin file (the flag passes the whole file, maintainer comment included). Write it once now so the first wrapper launch finds it; the hook refreshes it on every later session start. Under `--dry-run`, print the target path and write nothing.

   ```
   mkdir -p "$HOME/.claude/ac"
   awk '/^<!-- ac:working-rules:end -->$/ { on = 0 } on { print } /^<!-- ac:working-rules:start -->$/ { on = 1 }' \
     "${CLAUDE_PLUGIN_ROOT}/references/working-rules.md" > "$HOME/.claude/ac/working-rules.md"
   ```

   Confirm the result is non-empty; an empty file means the markers moved, so report it and offer no wrapper.

2. **Check the layout.** When `~/.claude/CLAUDE.md` as it now stands still has two or more moved headings (3a's set) as whole `## ` lines, the same test the hook applies (one alone can be a heading the operator wrote), because 3c was skipped, stopped on the markers, left a `.proposed` file, or kept an out-of-fence copy, offer no wrapper (it would add a second copy). Say a re-run after resolving 3c offers it.

3. **Find a wrapper.** Grep `~/.zshrc`, `~/.bashrc` and `~/.config/fish/config.fish` for a `claude` function or alias, using ERE because macOS `grep` has no `-P`:

   ```
   grep -nE '^[[:space:]]*(function[[:space:]]+claude([[:space:]({]|$)|claude[[:space:]]*\(\)|alias[[:space:]]+claude[= ])' ~/.zshrc ~/.bashrc ~/.config/fish/config.fish 2>/dev/null
   ```

   With no hit, write nothing to any rc file and say the SessionStart hook covers it. When the definition already passes `--append-system-prompt-file` for `working-rules.md` together with `AC_WORKING_RULES_APPENDED=1`, report it as wired and ask nothing. When it passes `--append-system-prompt-file` for some other file, offer nothing: a flag given twice keeps only the last value, so adding ours would drop theirs; say the hook covers it.

4. **Show the exact lines and ask.** Read the definition and render the edit against its actual final `claude` call, guarded by `[ -r ]` (`test -r` in fish) and with the variable on the same command. The flag combines with an `--append-system-prompt=...` the wrapper already passes; both land in the system prompt. For a zsh or bash function whose call is `command claude <args>`, the replacement is:

   ```
   if [ -r "$HOME/.claude/ac/working-rules.md" ]; then
     AC_WORKING_RULES_APPENDED=1 command claude <args> --append-system-prompt-file "$HOME/.claude/ac/working-rules.md"
   else
     command claude <args>
   fi
   ```

   with `<args>` kept exactly as the wrapper has them, an `--append-system-prompt=...` included, and the file flag placed before any `"$@"` or `"${args[@]}"` that carries the operator's own arguments. An alias cannot hold the guard, so for one render a function of the same shape that replaces the alias line, with the alias's arguments as `<args>` and `"$@"` (`$argv` in fish) after the file flag. Then ask:

   ```
   AskUserQuestion({
     header: "Wrapper?",
     question: "<rc file>:<line> defines a `claude` <function | alias>. Adding the working-rules flag puts the rules in the system prompt instead of session context. The exact edit:\n\n<before and after>",
     options: [
       {label: "Add the line (Recommended)", description: "Back up <rc file> to <rc file>.bak-ac-install and apply the edit shown. It takes effect in a new shell."},
       {label: "Skip, the SessionStart hook covers it", description: "Leave <rc file> untouched; the hook delivers the same rules on every launch."}
     ]
   })
   ```

   Edit the rc file only on `Add the line`, after `cp -n <rc file> <rc file>.bak-ac-install`, and apply exactly the lines shown. Under `--dry-run`, print the edit and ask nothing. Record the answer as `W.wrapper` in `~/.claude/ac-install.json` (`${CLAUDE_PLUGIN_ROOT}/references/install-settings.md` `## Answer record`); under `--upgrade`, skip this question when the record already says `"declined"`, and say the hook covers it.

5. **Offer the question timeout.** Skip unless `test -r "${CLAUDE_PLUGIN_ROOT}/hooks/posttooluse-question-timeout.sh"` succeeds: the two keys go in only where that hook exists, because the timer without it would auto-submit questions in supervised sessions with nothing telling the model to wait. Skip too under `--upgrade` when the record holds `W.afk`, and under `--dry-run` print the edit and ask nothing. Both keys are listed in `${CLAUDE_PLUGIN_ROOT}/references/install-settings.md` `## Question timeout (W.afk)`; write no other value. The question depends on where the keys would go:

   - **A wrapper was found** (3, whatever 4 answered, an already-wired one included): put `CLAUDE_AFK_TIMEOUT_MS=180000 AC_AFK_TIMER=1` on every `command claude` call the wrapper makes that starts a session (not on a management passthrough such as `claude mcp` or `claude plugin`), next to `AC_WORKING_RULES_APPENDED=1` when that is there, leaving every other part of the call as it is. Back up with `cp -n <rc file> <rc file>.bak-ac-install` and apply only on yes. The question says in one line that disabling ac means removing the keys from the wrapper too. For the call shown in 4:

     ```
     AC_WORKING_RULES_APPENDED=1 CLAUDE_AFK_TIMEOUT_MS=180000 AC_AFK_TIMER=1 command claude <args> --append-system-prompt-file "$HOME/.claude/ac/working-rules.md"
     ```

   - **No wrapper, and not `SKIP_SETTINGS`**: write both keys to `env` in `~/.claude/settings.json`, each only when absent, after `cp -n ~/.claude/settings.json ~/.claude/settings.json.bak-ac-install`. They then apply to every Claude Code session whether or not ac is enabled, so the question says in one line that disabling ac means removing them.
   - **No wrapper with `SKIP_SETTINGS`**: offer nothing.

   ```
   AskUserQuestion({
     header: "AFK timeout?",
     question: "A question asked during an ac:auto run continues on its own after 3 minutes away (unfocused or detached terminal), and the choice is recorded as 'timed out, not user-approved'. Supervised sessions keep waiting for you, and a plain /ac:plan --auto or /ac:execute --auto waits too. <the exact edit, then: Disabling ac means removing both keys from <the wrapper | settings.json>.>",
     options: [
       {label: "Add the keys", description: "<Back up <rc file> and apply the edit shown | Write both keys to settings.json env>. It takes effect in a new session started from a new shell, and not in a background session, where Claude Code never arms the timer."},
       {label: "Skip", description: "Nothing is written; every question waits for you."}
     ]
   })
   ```

   Record the answer as `W.afk` in `~/.claude/ac-install.json`, the way `W.wrapper` is recorded.

## Phase 4: settings.json

Skip when `SKIP_SETTINGS`.

Read `${CLAUDE_PLUGIN_ROOT}/references/install-settings.md`. It is the only source for every key below; this command deliberately carries none of them, and writing one from memory is how a wrong key ships. It also states the ADD-only rule that governs the whole phase.

1. **Read and back up.** Read `~/.claude/settings.json`, starting from `{}` when absent. Back it up with `cp -n ~/.claude/settings.json ~/.claude/settings.json.bak-ac-install` before any write, only when it exists. Skip the backup under `--dry-run`, where nothing is written.
2. **Group A**, safe-silent tuning. Apply silently, each key only when absent.
3. **Group C**, core ac parity. Apply without a prompt, including the migration strip for keys a prior install wrote. Surface every strip and every env rewrite in the gate diff, since neither the deny entry nor an exact-matched env value can be told apart from an operator's own choice.
4. **Groups B and D**, opt-in and default off. Present each through the `AskUserQuestion` block the reference defines and write only what the operator checks; under `UPGRADE`, only the unanswered options (0e). Skip both prompts under `--dry-run` and say no key would be set.
5. **Group E**, the output style, opt-in and default off. Ask through the reference's block and write the literal value it names, never a value you assembled yourself: a plugin style that does not resolve fails silently and reads exactly like the key being absent. Skip the question when `outputStyle` already holds any value other than `default`, which the reference explains is the no-style value rather than an answer, when `UPGRADE` finds `E.output-style` answered, and under `--dry-run`.
6. **Group F**, marketplace auto-update, opt-in and default off. Collect the candidates the reference defines and ask only when there is at least one; skip the question under `--dry-run` and list the candidates instead. Then run the reference's three report-only checks (`ENABLE_TOOL_SEARCH`, a legacy `autoUpdates` key, a hand-installed copy of the memory index hook) and hold the findings for Phase 5. They write nothing, and Phase 4 never edits a shell rc file.
7. **Group G**, session titles, opt-in and default off. Ask through the reference's block only when `env.AC_SESSION_TITLE` is absent and `test -r "${CLAUDE_PLUGIN_ROOT}/hooks/userpromptsubmit-session-title.sh"` succeeds, and write the one key it names. Skip it under `--dry-run`, and under `UPGRADE` when the record holds `G.session-title`.
8. **The MCP token.** Follow the reference exactly. The value is never echoed, logged, or rendered.
9. **Show the diff and write.** Render newly-added against already-present, grouped A / C / B / D / E / F / G / token, with the token masked. Under `--dry-run`, stop here. When the merged object equals the file on disk, write nothing and report settings as unchanged. Otherwise copy the file as it stands to `${TMPDIR:-/tmp}/ac-install-settings.before.json`, or write `{}` there when it is absent (the `.bak-ac-install` backup is non-clobbering, so it can predate this run), write the merged object back, report the same breakdown, print the diff with the token masked inside the command so the value never reaches the diff output, and delete the snapshot, which holds the token in plain text:

   ```
   mask='if .env.KODIZM_MCP_TOKEN then .env.KODIZM_MCP_TOKEN = "<set>" else . end'
   diff <(jq -S "$mask" "${TMPDIR:-/tmp}/ac-install-settings.before.json") <(jq -S "$mask" ~/.claude/settings.json)
   ```

   ```
   rm -f "${TMPDIR:-/tmp}/ac-install-settings.before.json"
   ```

   A token written in this run therefore shows as no change; the breakdown above already reports it as `<set>`.
10. **Close the scheduling seam.** When Group D's scheduling trim was applied in this run and `SCHEDULING_TRIMMED` was false at 0b, set it true, re-evaluate the 3b conditional, and re-merge the block through 3c. The markers are still there and 3c is idempotent, so this is the same replace it always does. Skip when `SKIP_CLAUDE_MD` or `DRY_RUN` is set; under `--dry-run` Group D is never asked, so no seam exists. Report the re-merge in Phase 5 rather than asking the operator to run the command again.

## Phase 5: Summary

Unless `--dry-run`, first write `~/.claude/ac-install.json` as the reference's "Answer record" section defines: `PLUGIN_VERSION`, today's date, and every option shown or judged answered in this run, merged over `RECORD`. Write it on a `--skip-settings` run too, with the answers carried over unchanged.

Read `${CLAUDE_SKILL_DIR}/references/final-report.md` now and print its report template, then each note it lists whose condition applies, then its next steps.

## References

Named without line numbers on purpose; each entry names the section it means.

- `${CLAUDE_PLUGIN_ROOT}/references/global-claude-md-section-template.md`, the Phase 3 generated file inside its fence markers, with the placeholder roster and the keep test.
- `${CLAUDE_PLUGIN_ROOT}/references/working-rules.md`, the workflow sections between its `ac:working-rules` markers: the heading set 3a and 3c check, and the text 3d copies to `~/.claude/ac/working-rules.md`.
- `${CLAUDE_PLUGIN_ROOT}/hooks/session-start-working-rules.sh`, the SessionStart delivery path: its old-layout guard, the `AC_WORKING_RULES_APPENDED` silence, and the stable-copy refresh.
- `${CLAUDE_PLUGIN_ROOT}/references/install-settings.md`, every Phase 4 key and opt-in gate (Groups A to G), the report-only checks, the `ac-install.json` answer record, and the ADD-only rule.
- `${CLAUDE_PLUGIN_ROOT}/output-styles/concise.md`, the style Group E offers; read it only to describe what the operator is turning on.
- `${CLAUDE_PLUGIN_ROOT}/references/monitoring.md`, the depth behind the Watching sentence in `My workflow`.
- `${CLAUDE_PLUGIN_ROOT}/references/coding-style-template.md`, the Phase 1 seed including the required anti-pattern entries.
- `${CLAUDE_PLUGIN_ROOT}/references/language-style-template.md`, the Phase 2 seed.
- `${CLAUDE_PLUGIN_ROOT}/skills/init-project/SKILL.md`, its CAN / CANNOT / MUST block for the orchestrator shape and its `.proposed` sidecar gate.
- `${CLAUDE_PLUGIN_ROOT}/skills/commit/SKILL.md`, its Phase 0 for the `$ARGUMENTS` flag scan.
- `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`, which ships every ac hook, so Phase 4 writes none.
- `ac:skill-creator`, which owns the content of both generated skills.
