---
name: regen-do-everything
description: >
  Autonomous end-to-end fix/upgrade execution for ReGen Civics. Given a fix or
  upgrade task, Claude handles everything: diagnose, code, build-check, commit,
  push, verify live, and report. Rye only handles Railway DB access and env var
  changes. All access needs are identified upfront so Rye can log in once and
  walk away. Triggers on: "do everything", "fix this autonomously", "handle it",
  "run the fix", "execute this fix", "take care of it", "ship it".
---

# ReGen Do-Everything Skill

## Purpose

Execute fixes and upgrades with maximum autonomy. Rye describes the problem,
Claude does everything. Rye walks away after answering a short round of upfront
questions.

## Tools Available

Claude has three tool layers. Understanding which one to use for what is critical.

### Cowork VM (Read + Grep + search -- diagnosis only)
The mounted folder at `/sessions/.../mnt/regen-civics-clean/` is a virtual overlay.
Cowork's `Read`, `Grep`, and `Glob` tools are fast and perfect for **reading** code,
searching patterns, and understanding the codebase. BUT: edits made with Cowork's
`Edit` or `Write` tools live in a virtual layer that git and Windows cannot see.
**Never use Cowork Edit/Write for code changes you intend to ship.** Use them only
for scratch files, docs in the `.claude/` folder, or prototyping you'll redo via DC.

### Desktop Commander (edit + git + build -- all real changes)
DC's `edit_block` writes directly to Rye's Windows filesystem. Git sees these
changes. DC's `start_process` runs commands on Rye's machine (git, npm, node).
**All code changes, commits, and pushes go through Desktop Commander.**

Key setup:
- Shell: `cmd.exe` (not PowerShell -- PowerShell swallows git stdout)
- Git PATH prefix: `set PATH=C:\Program Files\Git\cmd;%PATH%`
- Project path: `C:\Users\taren\Downloads\regen-civics-clean`
- Chain commands with `&&` in cmd.exe
- Railway auto-deploys from main, so push = deploy

### Claude in Chrome (browser verification)
Navigate to regencivics.earth, run JS checks, verify live pages, read console
errors, check network requests. Use for Phase 5 verification.

## Execution Protocol

### Phase 0: Scope and Access (do this FIRST, every time)

Before touching any code, do these three things:

1. **Scan the task for access needs.** Ask yourself:
   - Will I need to verify something on regencivics.earth? (Claude in Chrome)
   - Will I need to run a DB query or migration? (Rye must provide DATABASE_URL)
   - Will I need to change Railway env vars? (Rye must log into Railway dashboard)
   - Will I need Rye to be logged into the site to test authenticated pages?

2. **Ask Rye one combined question** covering everything you need upfront:
   - Which sites to log into (regencivics.earth, Railway dashboard, GitHub)
   - Whether to provide DATABASE_URL for this task
   - Any design or product preferences ("should X look like Y or Z?")
   - Max 5 questions. Be specific. No open-ended "any thoughts?" questions.

3. **Once Rye answers, confirm the plan in one sentence and start working.**
   Do not ask again unless you hit something truly unexpected.

**Example opening:**
> Before I start, a few things I'll need:
>
> 1. Can you log into regencivics.earth/profile so I can verify the fix on authenticated pages?
> 2. This fix touches the forum schema. Can you paste your Railway DATABASE_URL so I can check current data?
> 3. The broken image could be a missing file or a proxy issue. Any preference on fallback (text or placeholder image)?
>
> Once you answer these I'll handle the rest.

**If the task needs zero access from Rye**, skip the questions and say:
> I have everything I need. Starting now, I'll report back when it's live.

### Phase 1: Diagnose

1. Read the relevant fixes doc (`FIXES_TO_MAKE_*.md`) if one exists
2. Read `CLAUDE.md` for project conventions and writing rules
3. Trace the bug from symptom to root cause:
   - Grep for the component/feature mentioned
   - Read the relevant files end-to-end
   - Check data flow: client component -> tRPC call -> server handler -> DB query -> schema
   - Check asset flow: upload -> storage -> DB URL -> client display -> proxy/CDN
4. Do not ask Rye to confirm the diagnosis. State what you found and move to fixing.

**End of phase message:**
> Diagnosis: [one sentence root cause]. Moving to fix.

### Phase 2: Fix

1. **Use Cowork Read/Grep to understand** the code that needs changing
2. **Use DC `edit_block` to make all code changes** on the real filesystem.
   Each edit should be small and focused -- DC edit_block uses find/replace on
   the actual Windows file, so include enough context for a unique match.
3. Fix related issues discovered during diagnosis (don't leave adjacent broken things)
4. Check for the same pattern elsewhere in the codebase (grep for similar code)
5. Preserve existing optimizations (Sharp, caching, lazy loading)
6. After all edits, verify with DC: `git diff --stat` to confirm changes are real

**End of phase message:**
> Fixed [N] files: [list]. Git diff confirms [N] files changed. Moving to build check.

### Phase 3: Build Check

1. Use Desktop Commander (cmd.exe) to run build on Rye's machine:
   ```
   DC (cmd.exe): set PATH=C:\Program Files\Git\cmd;%PATH% && cd /d C:\Users\taren\Downloads\regen-civics-clean && npm run build
   ```
2. If build fails, read the errors, fix them with DC `edit_block`, and re-run
3. Do not proceed to commit until the build passes

**End of phase message:**
> Build passes. Moving to commit and push.

### Phase 4: Ship

1. Use Desktop Commander (cmd.exe) to commit and push. Each as a separate call:
   ```
   DC (cmd.exe): set PATH=C:\Program Files\Git\cmd;%PATH% && cd /d C:\Users\taren\Downloads\regen-civics-clean && git add [specific files]
   DC (cmd.exe): echo fix: clear commit message here> C:\Users\taren\Downloads\regen-civics-clean\commit-msg.txt
   DC (cmd.exe): set PATH=C:\Program Files\Git\cmd;%PATH% && cd /d C:\Users\taren\Downloads\regen-civics-clean && git commit -F commit-msg.txt && del commit-msg.txt
   DC (cmd.exe): set PATH=C:\Program Files\Git\cmd;%PATH% && cd /d C:\Users\taren\Downloads\regen-civics-clean && git push origin main
   ```
   **Do NOT use `git commit -m`.** cmd.exe mangles quoted messages with spaces.
   Always write to a temp file and use `-F` (see Gotchas).
2. Railway auto-deploys from main. Wait ~60 seconds for deploy.
3. If git push fails (auth issue), tell Rye exactly what to run and wait.

**End of phase message (if push succeeds):**
> Pushed to main. Railway deploying. I'll verify in ~60 seconds.

**End of phase message (if push fails):**
> I can't push from here (auth issue). Run this in your terminal:
> ```
> cd C:\Users\taren\Downloads\regen-civics-clean
> git add [files]
> git commit -m "[message]"
> git push origin main
> ```
> Let me know when it's deployed and I'll verify.

### Phase 5: Verify Live

1. Use Claude in Chrome to navigate to the affected pages on regencivics.earth
2. Run JavaScript checks:
   - Images load (naturalWidth > 0, no broken img elements)
   - Components render expected content (no fallback states)
   - No console errors related to the fix
   - Network requests return 200 for proxied/CDN assets
3. Check adjacent pages that share the same components
4. If verification fails, diagnose why and loop back to Phase 2 (no need to ask Rye)

**End of phase message (pass):**
> Verified live. [what was checked]. Fix is done.

**End of phase message (fail):**
> Verification failed: [what broke]. Fixing now, will re-deploy.

### Phase 6: Report

1. Update the fixes doc with final status (change CODED to VERIFIED or LIVE)
2. List any new issues discovered during the process (add to fixes doc)
3. Update the Handoff Breakdown table per the regen-fixes-handoff skill
4. Give Rye a clean summary: what changed, what's live, what's next (if anything)

**End of skill message:**
> Done. Here's what shipped: [summary]. Fixes doc updated. [Any new issues found.]

## Decision Rules

### When to ask Rye vs. just do it

**Just do it (don't ask):**
- Code changes of any size
- Fixing adjacent bugs found during diagnosis
- Choosing between implementation approaches (pick the simpler one)
- Reading any file in the repo
- Committing and pushing code (via Desktop Commander)
- Running build/type checks (via Desktop Commander)
- Running JS in the browser to verify things (via Claude in Chrome)
- Creating or updating docs and fixes files
- Adding sync logic, proxy routes, or other server-side plumbing
- Re-deploying after a verification failure (fix -> commit -> push -> verify loop)

**Just do it (database):**
- Reading DATABASE_URL from `.env` in the project root (it's there, use it)
- Running seed scripts with `set DATABASE_URL=<value from .env> && npx tsx scripts/...`
- Creating new seed scripts following patterns in `scripts/seed-*.ts`
- Querying the Railway DB for lookups (category IDs, user IDs, post IDs)
- Forum post creation and seed comment insertion

**Just do it (quest building):**
- Use the `regen-quest-builder` skill for full quest creation
- All quest artifacts (code, PDF, forum seeding) can be done autonomously
- Only the hero image needs Rye if nano-banana-pro API is unavailable
- Save a ready-to-run prompt file at `docs/quest-{N}-image-prompt.md` for Claude Code

**Ask Rye (must have human input):**
- Changing Railway environment variables (not reading them, reading .env is fine)
- Uploading files that only exist on Rye's machine
- Architecture decisions that change how the product works for users
- Anything that needs Rye logged into a third-party site
- If Desktop Commander can't push (auth issue), give Rye the exact commands
- Running nano-banana-pro image generation in Claude Code (provide the prompt file)

### When to keep going vs. stop

**Keep going (don't stop to ask):**
- You found more broken things related to the fix
- The fix works in one place but the same pattern is broken elsewhere
- Verification failed and you know why
- Build failed and you can read the errors
- There's a data issue you can fix with a server-side code change

**Stop and report:**
- Verification passes on all affected pages
- You hit something that requires Rye's machine access (DB, env vars)
- The fix requires a product decision (not a technical one)

## Desktop Commander Reference

### Tested working patterns (2026-03-30)

**Git commands (cmd.exe shell, always prefix PATH):**
```
DC (shell: cmd.exe): set PATH=C:\Program Files\Git\cmd;%PATH% && cd /d C:\Users\taren\Downloads\regen-civics-clean && git status --short
```

**File edits (edit_block, use Windows paths):**
```
DC edit_block:
  file_path: C:\Users\taren\Downloads\regen-civics-clean\client\src\pages\PlayerProfile.tsx
  old_string: [exact text to find]
  new_string: [replacement text]
```

### Critical: Cowork overlay vs real filesystem
- Cowork `Read`/`Grep`/`Glob` read from a virtual overlay. Fast for diagnosis.
- Cowork `Edit`/`Write` write to the overlay only. Git and Windows CANNOT see these.
- DC `edit_block` writes to the real Windows filesystem. Git sees these changes.
- DC `start_process` runs on the real machine. Git, npm, node all work here.
- New files created by Cowork `Write` DO sync (new inodes). Edits to existing files do NOT.

### Gotchas
- Use `cmd.exe` shell, not PowerShell. PowerShell swallows git stdout.
- Always prefix PATH in each cmd.exe call (no persistent state between calls).
- Use `&&` to chain commands in cmd.exe (not `;` which is PowerShell).
- DC `edit_block` old_string must match EXACTLY (whitespace, indentation, line endings).
- Large file edits: make multiple small edit_block calls, not one giant replacement.
- **Git commit messages**: cmd.exe mangles `-m "message with spaces"`. Instead,
  write the message to a temp file and use `-F`:
  ```
  DC (cmd.exe): echo fix: profile avatar sync> C:\Users\taren\Downloads\regen-civics-clean\commit-msg.txt
  DC (cmd.exe): set PATH=... && cd /d ... && git commit -F commit-msg.txt
  DC (cmd.exe): del C:\Users\taren\Downloads\regen-civics-clean\commit-msg.txt
  ```
- **DC `read_file` is unreliable on .ts/.tsx files.** It often returns JSON metadata
  instead of file content. Use Cowork `Read` for reading code (instant, always works).
  If you specifically need the real filesystem version (not overlay), use:
  ```
  DC (cmd.exe): set PATH=... && cd /d ... && git show HEAD:path/to/file.tsx
  ```
- **`findstr` cannot read UTF-8 TypeScript files.** It silently returns nothing.
  Use `git grep` instead for searching on the real filesystem:
  ```
  DC (cmd.exe): set PATH=... && cd /d ... && git grep "searchTerm" -- "*.tsx"
  ```
- **DC `edit_block` may read from the Cowork overlay.** If you previously edited a
  file with Cowork Edit/Write, DC's edit_block might match against the overlay version
  (stale content) instead of the real file. Before editing a file that was touched in
  the overlay, confirm the real content first:
  ```
  DC (cmd.exe): set PATH=... && cd /d ... && git show HEAD:path/to/file.tsx
  ```
  Then base your edit_block old_string on that output.

### Speed and Efficiency
- **Always prefer Cowork Read/Grep for diagnosis.** Instant, no shell overhead.
  Only go through DC when you need the real filesystem version specifically.
- **Batch DC edit_block calls.** Each DC call has network overhead. Plan edits in
  advance rather than read-edit-read-edit loops. Cowork Read -> plan all edits ->
  DC edit_block x N -> DC git diff to verify.
- **One git add + one git commit per fix batch.** Don't commit file by file.
  `git add file1 file2 file3` then one commit with a clear message.
- **Build check catches most issues.** If `npm run build` passes, the code is
  almost certainly correct. Don't over-verify before pushing.
- **DC start_process timeout:** Set timeout_ms appropriately. Git commands: 10000ms.
  npm run build: 120000ms. Git push: 30000ms. Too short = truncated output.

## Common Patterns in This Codebase

### R2 Image Proxy Chain
Upload -> R2 bucket -> `assets.regencivics.earth` URL stored in DB -> client
reads URL -> `resolveAssetUrl()` or `cdnImg()` rewrites to `/api/img?url=...` ->
server fetches from R2 via S3 client -> Sharp optimizes -> serves to browser.

If images are broken, check each link in this chain.

### Two Profile Tables
`userProfiles` = forum/auth identity (reputation, posts, onboarding path).
`playerProfiles` = game identity (wallet, tokens, quests, location, streaks).
Shared fields (avatarUrl, displayName, bio) are synced bidirectionally in
`server/db.ts` via `upsertUserProfile()` and `updatePlayerProfile()`.
If profile data looks wrong, check which table the component reads from.

### Auth System
`openId` string in `users` table: `google:<id>`, `email:<address>`, `apple:<id>`.
Session via JWT cookie. `sdk.createSessionToken(openId)` creates the token.
Login routes in `server/_core/oauth.ts`.

### Asset URL Helpers
- `cdnImg(url, width?, quality?)` -- for blog/content images with explicit sizing
- `resolveAssetUrl(url)` -- for avatars, banners, user-uploaded images with default quality
- Both route through `/api/img` which handles R2 fetch + Sharp optimization

### Settings Architecture (as of 2026-03-30)
Settings tab uses sidebar nav with three sections: Profile, Game & Wallet,
Notifications. State managed by `settingsSection` useState in PlayerProfile.tsx.
ProfileEditForm saves to `userProfiles` via `trpc.userProfiles.updateProfile`.
CollaborationSettingsPanel saves to `playerProfiles` via `trpc.playerProfiles.update`.
Both tables sync shared fields bidirectionally.

### Railway Build Verification (after push)

Railway auto-deploys on push to main. After pushing, verify the build succeeds:

1. **Navigate to Railway dashboard** via Claude in Chrome:
   ```
   https://railway.com/project/1b47f872-03c6-4c22-9ab7-a42c81d11e51/service/f99fd8fb-acf9-4a8f-97de-20514d1669f8
   ```
2. **Wait ~90 seconds** for the build to complete (Nixpacks + pnpm install + vite build + esbuild).
3. **Check deployment status** -- look for "Deployment successful" or "Deployment failed".
4. **If build fails**, read the build logs:
   - Click on the failed deployment to open its detail view
   - Check the Build Logs tab for esbuild or vite errors
   - Common failures: truncated .ts files (incomplete syntax), missing imports, type errors
   - Fix the issue, commit, push again. DO NOT leave a failing build.
5. **Known pattern: file truncation.** Previous sessions have corrupted files by
   writing incomplete content. If esbuild reports "Expected identifier but found end of file"
   or "Unterminated string literal", the file is truncated. Restore from the last
   complete git version: `git show <good-commit>:path/to/file > path/to/file`

**Debugging truncated files:**
```
DC (cmd.exe): cd /d C:\Users\taren\Downloads\regen-civics-clean && git log --oneline -- path/to/file
DC (cmd.exe): cd /d C:\Users\taren\Downloads\regen-civics-clean && git show <parent-commit>:path/to/file | more +last_few_lines
```
If the parent commit has a complete version, restore from it and re-add the legitimate
changes from the truncating commit.

## Skill Checklist (use as todo template)

For each fix:
- [ ] Phase 0: Identify access needs, ask Rye upfront
- [ ] Phase 1: Diagnose root cause
- [ ] Phase 2: Implement fix
- [ ] Phase 2b: Check for same pattern elsewhere
- [ ] Phase 3: Build check passes
- [ ] Phase 4: Commit and push (or hand off exact commands)
- [ ] Phase 4b: Verify Railway build succeeds (check dashboard)
- [ ] Phase 5: Verify live via browser
- [ ] Phase 6: Update fixes doc, report to Rye
