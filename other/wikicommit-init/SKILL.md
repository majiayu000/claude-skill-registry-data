---
name: wikicommit-init
description: Initialize WikiCommit directory structure, schema, and configuration in a repository. Use this only when someone explicitly asks to set up WikiCommit in a repository. It writes .wikicommit/, root configuration files and workflows, so do not use it to refresh or inspect a repository that already has .wikicommit/ — wikicommit-update refreshes one and wikicommit-status inspects it without writing.
disable-model-invocation: true
---

# wikicommit-init

> **Paths in this file.** `references/…`, `scripts/…` and `../<other-skill>/…` are relative to this Skill's directory — the one holding this `SKILL.md`, which the runtime names when it loads the Skill — not to the repository root, because the Skills may be installed under `.claude/skills/` or `.agents/skills/`. Commands still run from the repository root, so spell the path out from there (`python <this Skill's directory>/scripts/…`). Paths starting with `.wikicommit/` are repository-root paths as before.

Generates WikiCommit's `.wikicommit/` directory structure, schema, and configuration files in the repository.

## Prerequisites

Confirm the following with the user (use the default value if there is no answer):

1. **Primary language** (primary_lang): `en` (default). This is the source language of the wiki the user is creating (not the language of the WikiCommit tool itself). Users who want a Japanese-language wiki should explicitly answer `ja`. **Any other answer is supported and produces a wiki in that language, but WikiCommit's own labels — the review banner, the sources box, page properties, and the generated index/overview pages — have translations for ten languages (`en`, `ja`, `de`, `es`, `fr`, `it`, `pl`, `pt`, `ru`, `zh`) and render in English on a wiki in any other language** (page bodies and Quartz's own chrome still follow the chosen language). `init.py` prints this as a `NOTE:` line when it applies, so there is no need to pre-empt it here; the published pages deliberately say nothing about it, which makes that line the only place it is stated.
2. **Wiki theme** (theme): free text, empty (default, skip with a blank Enter). Used by `wikicommit-generate`'s exclude judgment to automatically skip entities unrelated to the wiki's topic; leaving it empty disables that judgment (all entities are generated as before). **It answers "what is this wiki about" — and only that.** Two neighbouring questions have their own files, both of which `init.py` writes a template for in Processing Flow step 2: "which sources do we take in" is `.wikicommit/source-policy.md`, and "granted a subject is relevant, may we write about it at all" is `.wikicommit/entity-policy.md`. Neither exists yet at this point, so name them as the place to write those policies *after* init finishes rather than telling the user to open one now. Say so when prompting, without spelling out all three axes — the prompt only has to keep the answer to this one: a source-selection rule written here is read only when deciding whether an already-ingested entity gets a page, where it is pure noise, and is never read at the point it would matter; a "do not write about X" rule written here is read at the right moment but gets weighed as relevance, which is a different question and gives a different answer for a subject that is squarely on-topic and still off-limits. Example prompt:

   ```
   What is this wiki's theme? (free text, optional — leave blank to skip)
   Describe the subject matter only. Which sources to take in, and which subjects
   are off-limits even when relevant, each have their own file alongside it
   (.wikicommit/source-policy.md and .wikicommit/entity-policy.md).
   e.g. "Knowledge base for an internal engineering org. Personal-blog-style topics are out of scope."
   ```

   Just hold the answer for now — if non-blank, it also drives an obvious-type judgment that runs later,
   in Processing Flow step 3, once `init.py` has actually created `.wikicommit/` (see that step for why
   it can't run here yet: this repository's root path isn't confirmed until prerequisite 3 below, and
   `.wikicommit/schema/` doesn't exist until `init.py` runs in step 2).

   Then ask the one switch that lives in the second of those two files, immediately after, as part of
   the same exchange rather than as a step of its own:

   ```
   Skip pages about living individuals? [y/N]
   Public figures acting in their public capacity, and historical figures, are normally
   in scope — this is about people who happen to be named in your sources, not about
   everyone alive. You can add finer rules to .wikicommit/entity-policy.md afterwards.
   ```

   **A blank Enter is no**, which is the current behaviour and what every repository created so far has.
   On a yes, pass `--exclude-living-persons` to `init.py` in step 2.

   **Why this one question and not the prose**: the two policy files are prose read afresh on every run,
   so writing them after init works — the next run picks them up. A switch does not behave that way. It
   has a default, it acts without saying so, and the window it acts in is the first `/wikicommit-generate`,
   which is the first thing a user does after init and the run whose pages most other pages end up linking
   to. Neither direction can be undone afterwards: pages already written survive a change of the switch
   (the regeneration mode does not re-run the entity-extraction pass), and entities already excluded are
   not revisited by re-registering the same source (its hash still matches, so the later passes never run).
   Asking is the only way the value reflects a decision.

   **Say who is in, not only who is out.** The wording above is deliberate: the switch turns on "living",
   while what actually separates risk is whether someone is a public figure, and `entity-policy.md`'s own
   template warns about this. Keeping people out via `theme` alone can leave a wiki with zero `Person`
   pages, historical figures included; a question that does not say who is in invites that over-exclusion.

   **Non-interactive runs do not ask.** Do not pass the flag, and say so once instead, the same way this
   Skill handles a type proposal it cannot get an answer for:

   ```
   NOTE: exclude_living_persons is false in .wikicommit/entity-policy.md (the default).
   Decide it before the first /wikicommit-generate — afterwards, turning it on does not
   remove pages that already exist.
   ```

   **A re-init never rewrites the file.** `.wikicommit/entity-policy.md` holds prose the user has been
   writing, so it is skipped whenever it already exists, and there is deliberately no `--update-<field>`
   path for this switch the way `--update-theme` exists for `theme`: that flag exists because `config.yml`
   is generated wholesale and re-init skips it, whereas here the whole file is the user's to edit and the
   one-line change is trivial to make by hand. Passing `--exclude-living-persons` against an existing file
   prints a `NOTE:` and changes nothing.

   **You will still ask the question on a re-init, and that is fine** — whether `.wikicommit/` already
   exists is only determined in Processing Flow step 1, after this exchange (the same ordering that keeps
   the obvious-type judgment in step 3 rather than here). Ask it, pass the flag on a yes in both forms of
   step 2, and relay the `NOTE:` if it appears: a repository predating `entity-policy.md` gets the switch
   set, and one that already has the file keeps its own decision. What must not happen is the user
   answering yes and hearing nothing back, so step 2 spells out which lines to relay.

3. **Repository root path**: current directory (default)
4. **Publish with Quartz v5**: confirm in two stages (local build/preview and automatic
   GitHub Pages publishing are independent choices; a user who only wants to preview the wiki locally
   should not be forced into enabling GitHub Pages).

   a. Local build/preview:

      ```
      Set up Quartz v5? Quartz v5 is the static site generator that builds your wiki into a
      browsable website. Answering Y lets you preview the wiki locally anytime with
      `/wikicommit-serve` — you don't have to wait for a deploy to see how it looks.
      [Y/n]
      ```

      If Y (default), pass `--quartz` to `init.py`. If N, do not pass it (only `.wikicommit/` is
      generated) and skip sub-step b below — do not ask it.

   b. Automatic GitHub Pages publishing (only ask if a. was answered Y):

      ```
      Also set up automatic publishing to GitHub Pages? This adds .github/workflows/deploy.yml, so
      every merge to main automatically rebuilds and republishes the wiki, and enables GitHub Pages
      (Source: GitHub Actions) on this repository.
      ⚠️ For private repositories, this requires GitHub Pro/Team/Enterprise. On the free plan,
         deploy.yml will fail with a 404 on private repositories.
      [Y/n]
      ```

      If Y (default), pass `--quartz-pages` in addition to `--quartz`. If N, pass `--quartz` alone
      (local build/preview only — no GitHub Pages, no `deploy.yml`; this can be added later by
      re-running `wikicommit-init` and answering Y here).
      If the target repository is known to be private, recommend N given the caveat above.

## Processing Flow

1. Check whether `.wikicommit/` already exists:
   - Does not exist → run `init.py` without `--no-overwrite`
   - Exists → add `--no-overwrite` and run. Notify the user that existing configuration will be
     preserved, and that `.wikicommit/scripts/` is the one exception — it is refreshed to the
     installed Skills' version even under `--no-overwrite`, because it is WikiCommit's
     own distribution payload rather than the user's content (a stale `_version.py` would stamp new
     pages with the old version in `generated_with` / `translated_with`)

2. Run the following command with the confirmed values:

   **New repository:**

   ```bash
   python scripts/init.py \
     --primary-lang <primary_lang> \
     [--exclude-living-persons] \
     [--quartz] \
     [--quartz-pages] \
     [--repo-url="$(gh repo view --json url -q .url)"]
   ```

   **Adding to an existing repository (when `.wikicommit/` already exists):**

   ```bash
   python scripts/init.py \
     --primary-lang <primary_lang> \
     --no-overwrite \
     [--exclude-living-persons] \
     [--quartz] \
     [--quartz-pages] \
     [--repo-url="$(gh repo view --json url -q .url)"]
   ```

   If the user answered the theme prompt with non-blank text, add `--theme` to the **New repository**
   form above; do not add it to the **Adding to an existing repository** form — `--theme` has no effect
   there: an already-existing `config.yml` is always skipped wholesale under
   `--no-overwrite`, silently discarding whatever the user just answered at the theme prompt. Use
   `--update-theme` afterward instead — a dedicated flag that rewrites only the `theme` value of the
   existing `config.yml`, leaving the rest of the file untouched. Skip it if the user left the theme
   prompt blank — a blank answer means "leave it as is," not "clear it," and `--update-theme` always
   overwrites unconditionally once invoked (that is the point of it being a separate, explicitly-named
   flag rather than folded into `--theme` itself: it signals an intentional overwrite of whatever theme
   value — set or still empty — was there before).

   In both cases, embed the theme text with a quoted-delimiter heredoc via command substitution, never
   as a bare double-quoted string — the answer is free-form text, and shell metacharacters such as
   `` ` ``, `$(...)`, or `"` in a plain `--theme="<theme text>"` would be interpreted by the shell. The
   heredoc value is also always a single `--theme=...` shell word, so text starting with `-` is not
   misparsed as an option:

   ```bash
   --theme="$(cat <<'EOF'
   <theme text>
   EOF
   )"
   ```

   ```bash
   python scripts/init.py --update-theme="$(cat <<'EOF'
   <theme text>
   EOF
   )" [--repo-root <path>]
   ```

   Pass `--exclude-living-persons` if, and only if, the user answered Y to the living-individuals switch in
   Prerequisite 2 — in **both** forms above, unlike `--theme`. It behaves differently from `--theme` on an
   existing repository because it writes a different file: `.wikicommit/entity-policy.md` is copied with
   `always_skip_existing`, so a repository that already has one keeps it untouched (`init.py` says so and
   changes nothing), while a repository initialized before that file existed gets one with the switch
   already set. Leave the flag off on a blank Enter — omitting it is what produces the `false` default, and
   there is no flag that sets it back.

   **Relay two lines from `init.py`'s output whenever you passed this flag**, because both mean the answer
   you collected did not take effect and neither one fails the run:

   - `NOTE: .wikicommit/entity-policy.md already existed, so --exclude-living-persons was not applied.` —
     tell the user, and that the one-line change is theirs to make in that file. This is the expected
     outcome on a repository that already has the file; the Prerequisite 2 question is asked before the
     existence check in step 1 above, so it does get asked in that case.
   - `WARNING: could not set exclude_living_persons in ...` (stderr) — tell the user the switch is still
     `false` and the file needs editing by hand.

   Both matter more than they look: by the time the user notices, the first `/wikicommit-generate` has
   usually already run, and turning the switch on afterwards does not remove pages that already exist.

   Do not pass `--targets` — it is no longer collected in the Prerequisites step, so `config.yml` is always
   generated with `targets: []`. The translation pipeline itself is Phase 4 scope and not yet
   implemented; once it lands, users configure `targets` by hand-editing `config.yml`.
   Only pass `--quartz` if the user answered Y to the Quartz local build/preview confirmation (4a).
   Only pass `--quartz-pages` if the user additionally answered Y to the GitHub Pages confirmation
   (4b) — never pass `--quartz-pages` without `--quartz` (`init.py` rejects that combination with
   exit code 1; sub-step 4b is only ever asked when 4a was already Y, so this should not occur in
   practice, but the check exists as a safety net in `init.py` itself).
   Always pass `--repo-url` whenever you pass `--quartz`, and only then (it is what fills in the
   footer's GitHub link in `quartz.config.yaml`; without `--quartz` that file is never generated and
   the flag does nothing). It is not gated on any user answer — omitting it on a repository that does
   have a GitHub remote silently ships a footer with no link to the wiki's own repository.
   Write it exactly as the `$(gh repo view --json url -q .url)` command substitution shown above rather
   than pasting a URL you resolved yourself — the value then never passes through you, and a repository
   with no GitHub remote makes `gh` fail and the substitution expand to the empty string, which
   `init.py` treats the same as omitting the flag. **In that no-remote case, `init.py` drops the footer's
   GitHub entry entirely** rather than leaving the upstream Quartz URL or a literal placeholder there;
   the footer still renders, without a links list. `init.py` reports this with a
   `NOTE: quartz.config.yaml: no --repo-url resolved ...` line — when you see it, tell the user, and
   that they can add the link by hand in `quartz.config.yaml` once the repository has a remote.

   `init.py` prints a second `NOTE:` line — `NOTE: WikiCommit ships its own labels in en/ja/de/... only ...` —
   when `primary_lang` is not one of the ten languages listed in Prerequisite 1. **Relay it to the user too.** Prerequisite 1
   deliberately does not pre-empt it, and the published pages deliberately say nothing about the
   fallback, so this line is the only place anyone is told; left sitting in `init.py`'s output it
   reaches nobody. Say what falls back to English and
   what does not, and that they can supply the missing labels if they want them translated.

   Add `--repo-root <path>` if a non-default repository root was specified.

   When `--quartz` is given, in addition to `.lychee.toml` / `.markdownlint.json`, it also generates
   `quartz.config.yaml` / `package.json` / `prebuild-symlinks.cjs` / `repair-plugin-builds.cjs`
   (retries any Quartz community plugin whose build failed after a successful clone,
   since Quartz's own installer marks that state "installed" and never retries it on its own)
   / `install-local-plugins.cjs` (run by `package.json`'s `postinstall`, so leaving it
   uncommitted makes every fresh-clone `npm install` die with MODULE_NOT_FOUND)
   / `quartz-plugins/`
   (a custom plugin providing the review_status banner and JSON-LD embedding, including the pre-built `dist/`)
   / `.github/ISSUE_TEMPLATE/report.md` (backs the banner's report link)
   at the repository root — everything needed for `/wikicommit-serve` to work locally.
   When `--quartz-pages` is additionally given, it also generates `.github/workflows/deploy.yml`
   (this is the one file that actually opts the repository into automatic GitHub Pages
   publishing on every merge to main; `--quartz` alone never generates it).
   `.lychee.toml` / `.markdownlint.json` are always generated regardless of `--quartz`
   (they are required by `wikicommit-merge`'s quality checks).
   These root-level files are never overwritten if they already exist, regardless of `--no-overwrite`
   (to avoid breaking existing configuration when running init on an existing repository).

3. If `init.py` succeeds (exit code 0), guide the user through the next steps:

   **Obvious-type judgment**: runs here,
   not in Prerequisites, because it needs two things Prerequisites can't yet guarantee: the confirmed
   repository root (prerequisite 3, asked after the theme prompt) and `.wikicommit/schema/` actually
   existing with the 6 base type files in it (only true once `init.py` has just run, immediately above).
   This whole sub-step is best-effort end to end — any failure at any point falls through silently to the
   lychee auto-install below, and never stops the overall init flow. Skip it entirely if the theme answer
   from Prerequisites was blank — a blank theme gives nothing to reason from.

   Otherwise:

   i. Ensure the shared Schema.org vocabulary cache is available (lazily built on first use, same call
      `wikicommit-generate` Pass 2b and `wikicommit-collect`'s Type Proposal step make):

      ```bash
      python .wikicommit/scripts/check_schema_org_type.py --list-type-names
      ```

      This prints the 933 type names without their descriptions — stage one of type recall.
      Sub-step ii picks candidates from it and reads only those descriptions.

      Non-zero exit (vocabulary fetch failed, e.g. no network) → skip the rest of this sub-step.
      Zero exit → record that the vocabulary cache now exists on disk (`.wikicommit/schemaorg-vocab.json`)
      — this becomes the `--vocab-cache-created` flag passed to `print_next_steps.py` at the end of this
      step. The default printed command is `git add -A`, which picks this file up whether or not it was
      created; the flag governs the selective fallback list printed beneath it, which lists paths
      individually and would abort on one that does not exist. It is committed like any
      other WikiCommit output, per that script's own docstring.

   ii. Using the `--list-type-names` output and the theme text alone, judge whether a Schema.org standard
      type — beyond the base types `init.py` always writes (`schema.base_types` in `config.yml`)
      — is **obviously** implied by the theme, not merely plausible. The bar is deliberately strict, so
      that a firing is rare but worth it — e.g. a theme like "Knowledge base for home cooking" obviously implies
      `schema:Recipe` (individual recipes are near-certain to be a core topic), whereas
      a vague or broad theme with no single unmistakably-implied type should yield zero candidates, same
      as leaving theme blank. **Re-scan `.wikicommit/schema/` on disk right now** (not from memory of
      Prerequisites) and skip any type that already has a file there — this directory only just gained
      its base type files moments ago in step 2 above, so this is the first point where that scan is
      trustworthy.

      **This step's evidence is the weakest of the three type-proposal routes** — one sentence of
      `theme`, before a single source has been read — so read the description of every candidate
      before proposing it (stage two):

      ```bash
      python .wikicommit/scripts/check_schema_org_type.py --describe \
        "$(cat <<'EOF'
      <Candidate1>
      EOF
      )" \
        "$(cat <<'EOF'
      <Candidate2>
      EOF
      )"
      ```

      Each candidate name goes through its own quote-delimited heredoc, for the same reason sub-step
      iv's `--property` values do — these are names this step itself just proposed, not values an
      earlier script already verified. Drop any candidate whose actual definition does not match what
      the theme obviously implies, and any name that comes back as `ERROR:` (a name not in the
      vocabulary was invented rather than recalled). With a bar this strict the candidate list is
      short or empty, so this costs nothing in the common case.

   iii. For each candidate found, list it for the user and ask for approval, Enter-based (default **N**
      on a blank Enter — this suggestion must never be added silently):

      ```
      Based on the theme you entered ("Knowledge base for home cooking"), this
      Schema.org type seems clearly implied: schema:Recipe (individual recipes
      are a near-certain topic for this theme).

      Add this type now? [y/N]
      ```

   iv. **For each approved type, read `.wikicommit/schema-authoring.md` and follow it** to verify the
      type, pick and verify its properties, and write `.wikicommit/schema/<Type>.md`.
      `init.py` expanded that file in step 2, so it is already on disk here — the same reason
      `.wikicommit/schema/` itself is (this step is ordered after step 2 deliberately). It holds the
      whole procedure: browsing `--list-properties`, verifying each candidate with `--property`
      heredocs, dropping what comes back `ERROR:`, the standard-type file format with
      `.wikicommit/schema/default.md` and `.wikicommit/schema/Person.md` (both just written by
      `init.py`) as the fixed style references for the frontmatter, the body as a list of reader
      questions (not copied from those two files' bodies), and how to write `granularity`. Four paths write type
      files and only the judgment differs between them, so the procedure lives in one place.

      What this step supplies on top of it:

      - **`provenance: init-theme`** — do not copy `Person.md`'s own `provenance: default`; each write
        site stamps its own origin.
      - **"Installed" here means what exists at this moment**: a base type `init.py` just wrote, or a
        type approved earlier in this same step. The shared procedure tells you to name only installed
        types in a deference rule; this is what that set is, right now.
      - **A deference rule written at this step has gone unfollowed before** — the entity-extraction
        pass kept choosing the new type over the one it deferred to. Write it where it applies, and know
        that it only works if that pass honors it.

      Three things this step is accountable for even if that Read is skipped: **every property goes
      through `check_schema_org_type.py` before it enters `properties:`**, **one `granularity` rule
      starts with `Boundary —`** (em dash, not a colon), and **`provenance` is `init-theme`**.

      **If `.wikicommit/schema-authoring.md` is not present** — which here means `init.py` did not
      finish writing the template tree, since it is `update: overwrite` and arrives on every init —
      read `scripts/templates/schema-authoring.md` instead: that is
      the source `init.py` copies from, so it is there whenever this Skill itself is. Say that the
      template tree looks incomplete and name the file that is missing under `.wikicommit/`, and go
      on with the procedure from the Skill-tree copy. Only if neither copy is readable, drop the
      approved types and carry on with the rest of step 3 — the base types `init.py` wrote are still
      there, so the wiki is usable, and `/wikicommit-status` reports the missing file as
      distribution drift afterwards.

   v. Writing the file is the one narrow exception to the "the agent must not write to
      `.wikicommit/schema/` directly" rule in Notes below — it only ever *adds* a file that is not
      there yet (step ii's on-disk re-scan is what makes that guarantee actually hold), and never
      edits or overwrites one `init.py` wrote. No PR is involved (same as every other file `wikicommit-init`
      produces): the new file just becomes part of the "Commit the generated foundational files" step
      of the guidance printed at the end of this step, which stages it with `git add -A`. **Do not
      commit it here and now** — that commit happens once, at the end of step 3, where it is offered
      to the user as a whole.

   First, attempt to auto-install `lychee` (used for external link validation). This runs
   regardless of whether `--quartz` was specified — `.lychee.toml` is always generated either way.
   Unlike the GitHub Pages step below, this needs no prior user confirmation: it only installs a
   local dev tool and never touches Git or `main`.

   i. Check whether `lychee` is already installed:

      ```bash
      lychee --version
      ```

      - Exit code 0 → already installed → skip step ii
      - Exit code non-zero → proceed to step ii

   ii. Attempt to install it via `cargo`. Compiling lychee from source (its dependency tree
      includes reqwest/tokio/hyper) commonly takes several minutes, which exceeds a typical
      agent's default command timeout (120 seconds in Claude Code) — run it with an extended
      timeout (Claude Code allows up to 10 minutes) so a slow-but-successful compile isn't
      mistaken for a failure:

      ```bash
      cargo install lychee
      ```

   This step never stops the overall init flow, regardless of the outcome. Record whether lychee
   ended up installed (already present in step i, or `cargo install lychee` exited 0 in step ii) —
   this becomes the `--lychee-installed` flag passed to `print_next_steps.py` at the end of this
   step (see below).

   Next, attempt to auto-install `markitdown` (the Python package `wikicommit-generate` uses to extract
   `type: url` / `type: wikicommit` sources, and as its fallback for file extensions with no dedicated
   Skill — see `wikicommit-generate`'s Prerequisite Skills table). Like the lychee step above, this runs
   unconditionally and needs no prior user confirmation — it only installs a local Python package and
   never touches Git or `main`.

   i. Check whether `markitdown` is already installed:

      ```bash
      markitdown --version
      ```

      This is informational only — always proceed to step ii regardless of the result. `markitdown
      --version` only reports whether the core package is present, not whether the `[pdf]` extra
      (needed for PDF parsing) is installed alongside it, so a bare "already installed" cannot be
      trusted to skip the install step (a pre-existing plain `markitdown` would otherwise never get it).

   ii. Attempt to install it via `pip` (this project assumes a Python environment throughout, unlike
      lychee's Rust/`cargo` toolchain). This is safe to run even when step i reported markitdown as
      already installed — `pip install` on an already-satisfied requirement is a fast no-op:

      ```bash
      pip install 'markitdown[pdf]'
      ```

   This step never stops the overall init flow, regardless of the outcome. Record whether
   markitdown ended up installed (already present, or `pip install 'markitdown[pdf]'` exited 0) —
   this becomes the `--markitdown-installed` flag passed to `print_next_steps.py` below,
   independently of the lychee outcome above.

   Next, attempt to auto-install `markdown-it-py` the same way (unconditionally, no prior
   confirmation, best-effort). `.wikicommit/scripts/check_raw_html.py` parses each page with it,
   and without it the check stops every `/wikicommit-merge` that changes a page — so a wiki
   initialized without it cannot merge its first page.

   ```bash
   python -c "import markdown_it" || python -m pip install markdown-it-py
   python -c "import markdown_it"
   ```

   Record whether it ended up installed (the second import check exits 0) — this becomes the
   `--markdown-it-installed` flag passed to `print_next_steps.py` below. Use the same `python`
   that runs `.wikicommit/scripts/`, and install through `python -m pip` rather than a bare `pip`:
   a `pip` bound to another interpreter is the one way the install can "succeed" without helping,
   which is also why the install's exit code is not what decides the flag. This step never stops
   the overall init flow.

   Next, attempt to enable the repository setting "Allow GitHub Actions to create and approve pull
   requests" (Settings → Actions → General → Workflow permissions). This runs unconditionally,
   regardless of `--quartz`/`--quartz-pages` (unlike the GitHub Pages step below) —
   `review-issue-close-sync.yml` is generated in every variant, and without this
   setting its `Commit and open PR` step fails once a reviewer closes a tracking Issue. There is no Y/n prompt for this — just attempt it and report the result, same
   best-effort pattern as the GitHub Pages step below.

   i. Skip straight to the fallback guidance below (no `gh api` calls) if `gh auth status` fails,
      or if `gh repo view --json nameWithOwner -q .nameWithOwner` fails (same repo-resolution
      safety rationale as the GitHub Pages step's note below — print
      `Detected repository: <owner>/<repo>`; since this step runs before the GitHub Pages step
      below, its own repo-resolution print can reuse this result instead of repeating it).

   ii. Otherwise, `gh api repos/{owner}/{repo}/actions/permissions/workflow` (GET-before-PUT, not
      a blind PUT). Non-zero exit → fallback. Zero exit → parse `can_approve_pull_request_reviews`;
      already `true` → record as enabled, done. `false` → note `default_workflow_permissions`
      from this same response (must be preserved verbatim below) and proceed to step iii.

   iii. `gh api -X PUT repos/{owner}/{repo}/actions/permissions/workflow -F
      can_approve_pull_request_reviews=true -f default_workflow_permissions=<value from step ii>`
      (re-sending the existing value so this sub-step never silently changes that unrelated
      field). Exit 0 → record as enabled. Non-zero → fallback.

   Never stops the overall init flow; proceed to the GitHub Pages step below regardless of the
   outcome. Record whether the setting ended up enabled — this becomes the
   `--actions-pr-permission-enabled` flag passed to `print_next_steps.py` at the end of this step
   (omit it on any failure/skip above; the script prints the manual fallback on its own then).

   When `--quartz-pages` was specified (this GitHub Pages activation sub-step is skipped entirely
   when `--quartz` was given without `--quartz-pages` — proceed straight to the "Also attempt to set
   up Quartz v5's dependencies" paragraph below in that case):

   First, attempt to enable GitHub Pages (Source: GitHub Actions) automatically. The user already
   consented to this in the Prerequisites Y/n confirmation (4b), so do not ask again — just do it
   and report the result.

   a. Skip straight to the fallback guidance below (do not run `gh api`) if `gh auth status` fails
      (`gh` not authenticated).

   b. Otherwise, before touching Pages at all, resolve and print which repository `gh` will operate on
      (GitHub Pages enablement is a hard-to-reverse, shared-system operation, and `gh api
      repos/{owner}/{repo}/pages` silently trusts whatever `gh` resolves the current repository to
      without ever showing it; a misconfigured or leftover remote — e.g. still pointing at a real
      repository during isolated test work — could enable Pages on the wrong repository with no
      on-screen indication). The "Allow GitHub Actions to create and approve pull requests" sub-step
      above already ran this same resolution and print unconditionally — reuse that result here
      instead of repeating the call and the print, unless that sub-step fell back to manual guidance
      (in which case redo it here):

      ```bash
      gh repo view --json nameWithOwner -q .nameWithOwner
      ```

      Print `Detected repository: <owner>/<repo>` using this output. `gh repo view` resolves the
      current repository using `gh`'s own remote-detection logic, which is not limited to a remote
      literally named `origin` — a GitHub remote named `github`, `upstream`, or anything else resolves
      exactly the same way, so do not additionally require `git remote get-url origin` — this single
      `gh repo view` call is both the existence check and the resolution step. If this command itself fails (e.g. no remote resolves
      to a GitHub repository `gh` can view), treat it the same as the auth check in step a — skip
      straight to the fallback guidance below.
      This is informational only — do not pause for confirmation (the user already consented in the
      Prerequisites Y/n confirmation (4b); this step only makes the target visible, per SKILL.md's
      existing non-blocking policy for this sub-step).

   c. Check first whether Pages is already enabled, then only create it if not
      (a GET-before-POST check, not a POST followed by guessing from error text):

      ```bash
      gh api repos/{owner}/{repo}/pages
      ```

      `gh api` resolves `{owner}` and `{repo}` from the current repository's GitHub remote automatically.

      - Exit code 0 → Pages is already enabled (idempotent case — a previous run or manual setup) →
        extract the `html_url` field from this same response (e.g. `gh api repos/{owner}/{repo}/pages
        --jq .html_url`) and record it for the `--pages-html-url` flag below (the API's
        `html_url` is used as-is rather than hand-built from `{owner}`/`{repo}`, since it resolves
        correctly for project pages, user/org pages, and custom domains alike) and skip step d below
      - Exit code non-zero (typically because no Pages site exists yet) → proceed to step d

   d. Create the Pages site:

      ```bash
      gh api repos/{owner}/{repo}/pages -X POST -f build_type=workflow
      ```

      - Exit code 0 → extract `html_url` from this response the same way as step c above and record
        it for the `--pages-html-url` flag below
      - Exit code non-zero (e.g. private repo without GitHub Pro/Team/Enterprise, insufficient `gh`
        permissions) → no `html_url` is available

   When (a) is skipped, (b) fails, or (d) fails with a real error, no `html_url` is available —
   omit `--pages-html-url` when calling `print_next_steps.py` below; the script prints the
   `⚠️ Could not enable GitHub Pages automatically` fallback guidance on its own in that case.

   **Then finish the README, only if step 2's `init.py` output logged `CREATED: README.md`**.
   init writes a README.md only into a repository that had none, and under
   `--quartz-pages` it leaves a marker where the published-site link goes, because that link is
   only known now. Resolve the marker whether or not an `html_url` was obtained — a README must not
   be handed over with the marker still in it:

   ```bash
   python scripts/init.py --finish-readme [--site-url "<html_url>"]
   ```

   Pass `--site-url` with the `html_url` recorded above, exactly as the API returned it; omit it when
   none was obtained, and the marker is removed instead. **Do not run this when `CREATED: README.md`
   was not logged in this run** — a README from an earlier run is the user's file, even if its marker
   is still there.

   This step never stops the overall init flow — proceed to the Quartz dependencies step below
   regardless of the outcome.

   Also attempt to set up Quartz v5's dependencies automatically whenever `--quartz` was specified
   (this runs regardless of `--quartz-pages`, and regardless of the GitHub Pages step above's
   outcome when that step did run), unless step 2's `init.py` output logged
   `SKIPPED: package.json (already exists)` — in that case the repository has its own pre-existing
   `package.json` that is not the WikiCommit template, and auto-running `npm install` would install
   and execute that project's own dependencies and lifecycle scripts without the user's
   confirmation, so skip this step (e below) entirely and pass `--package-json-skipped` to
   `print_next_steps.py` at the end of this step instead (without this, the "Preview
   the wiki locally" step in the guidance still unconditionally tells the user to run
   `/wikicommit-serve`, which would fail with "missing script" since the WikiCommit template's
   `scripts`/`devDependencies` were never merged into the pre-existing `package.json`). The script
   prints a warning explaining the required manual merge, and keeps both lines of the "Set up
   Quartz v5" step unchanged — `git submodule add` and `npm install` themselves don't depend on the
   `preview`/`build` scripts being present.

   `package.json`'s `postinstall` hook runs `git submodule update --init --recursive` (a no-op when
   `quartz` hasn't been added as a submodule yet) and then, only if `quartz/` exists, installs the
   submodule's own dependencies inside it — the template guards this step on `quartz/`'s existence,
   so a first-time init (before the user has run `git submodule add`, below) is skipped rather than
   crashing with `ENOENT`. This means `npm install` below always exits 0 regardless of whether the
   submodule has been added yet; only checking for `quartz/` afterward distinguishes "fully set up"
   from "top-level dependencies only".

   e. Otherwise (package.json was not skipped), determine Quartz v5's setup status and run
      `npm install` if needed by calling the setup-state script (script delegation pattern; this
      replaces a multi-branch `test -d` decision walked as prose):

      ```bash
      python scripts/check_quartz_setup.py
      ```

      It always exits 0 and prints one JSON line, e.g. `{"status": "fully_set_up"}`. Record the
      `status` field verbatim — this becomes the `--quartz-status` flag passed to
      `print_next_steps.py` below, which decides both the announcement line above the numbered list
      and whether/how the "Set up Quartz v5" step appears in it (e.g. `npm_install_failed_submodule_exists`
      keeps only the `npm install` line — re-running `git submodule add` on a path already
      registered in the index fails with `fatal: 'quartz' already exists in the index`).

      Whenever `quartz/` already exists (`status` is `fully_set_up`,
      `npm_install_completed_fully_set_up`, or `npm_install_failed_submodule_exists`), the script
      also attempts `npm run install-plugins` itself and includes the outcome as an
      `install_plugins_ok` boolean field in the same JSON line (otherwise a
      `--no-overwrite --quartz` re-init that finds Quartz already set up never surfaces this
      guidance anywhere, since the "Set up Quartz v5" step that normally carries it is the one
      being omitted). When present, pass it through as `--install-plugins-status ok` or
      `--install-plugins-status failed` to `print_next_steps.py` below; omit the flag entirely when
      the field is absent from the JSON (quartz/ did not exist yet, so the attempt could not run).

      This step never stops the overall init flow, regardless of the outcome — like the GitHub
      Pages step above and the lychee step earlier in this section, it is unconditionally best-effort.

   Finally, render and print the complete "Next steps" guidance by calling the templating script
   (script delegation pattern):

   ```bash
   python scripts/print_next_steps.py \
     --variant <none|quartz_only|quartz_pages> \
     [--lychee-installed] [--markitdown-installed] [--markdown-it-installed] \
     [--actions-pr-permission-enabled] \
     [--package-json-skipped] [--quartz-status <status>] \
     [--install-plugins-status <ok|failed>] \
     [--pages-html-url <url>] [--vocab-cache-created] [--readme-created] [--repo-root <path>]
   ```

   - `--variant`: `none` if `--quartz` was not passed to `init.py` in step 2; `quartz_only` if
     `--quartz` was passed without `--quartz-pages`; `quartz_pages` if both were passed.
   - `--repo-root`: pass the same value you passed to `init.py` in step 2, whenever a non-default
     repository root was specified there. The note under the printed `git add -A` reads that
     repository's `.gitignore` to decide which of its two shapes to print, so pointing
     this script at a different root than `init.py` makes that note and the `GITIGNORE_READY:` line
     answer about two different files. Omit it whenever you omitted it for `init.py`.
   - `--vocab-cache-created`: pass this whenever the obvious-type judgment's step i above got a zero
     exit from `--list-type-names` (regardless of whether any type ended up approved in step iii — the
     vocabulary cache file is written to disk as soon as that call succeeds); omit it if that call was
     skipped (blank theme) or failed (non-zero exit, e.g. no network).
   - `--lychee-installed` / `--markitdown-installed` / `--markdown-it-installed`: pass whichever of these ended up installed,
     per the auto-install steps above.
   - `--actions-pr-permission-enabled`: pass this whenever the "Allow GitHub Actions to create and
     approve pull requests" setting ended up enabled (already `true`, or the `PUT` succeeded) per
     the sub-step above; omit it on any failure/skip there, regardless of `--variant` (this setting
     is unconditional — `review-issue-close-sync.yml` ships in every variant).
   - `--package-json-skipped` / `--quartz-status`: only meaningful when `--variant` is
     `quartz_only` or `quartz_pages`. Pass `--package-json-skipped` if step 2's `init.py` output
     logged `SKIPPED: package.json (already exists)`; otherwise pass `--quartz-status <status>`
     with the `status` value recorded from `check_quartz_setup.py` above.
   - `--install-plugins-status`: only meaningful alongside `--quartz-status` (omit whenever
     `--package-json-skipped` is passed instead, or when `check_quartz_setup.py`'s JSON had no
     `install_plugins_ok` field). Pass `ok` or `failed` based on that field's value.
   - `--pages-html-url`: only meaningful when `--variant` is `quartz_pages` — pass the `html_url`
     recorded above, if any (omit it if the GitHub Pages activation fell back to manual guidance).
   - `--readme-created`: pass this whenever step 2's `init.py` output logged `CREATED: README.md`.
     That README already carries the licensing section and, when an `html_url` was obtained,
     the published-site link, so the guidance suggesting them is dropped (the "once you enable
     Pages manually" reminder stays when no `html_url` was obtained — that README has no link), and the selective `git add` list names README.md
     only in this case.

   Print the script's stdout output to the user verbatim — it is the complete guidance (any
   `✅`/`⚠️` announcement lines, the numbered "Next steps" list, and the `quartz_only` variant's
   trailing note about GitHub Pages not being set up, where applicable). It always exits 0.

   Finally, **offer to run that guidance's "Commit the generated foundational files" commands**
   — you already hold every value they depend on, so handing them back for the user
   to reconstruct costs something and buys nothing. The Notes at the end of this file say why this
   is not a prohibited write. **Hold the offer back** in the cases below, saying which one applied.
   None of them is about permission. The first three end it — the printed guidance is then the
   answer, as it was before this offer existed; the last one only postpones it, and the last
   sub-step of this step says how it resumes:

   - **Non-interactive run.** Silence is not consent; do not commit unasked.
   - **The `.gitignore` does not carry WikiCommit's patterns** (`init.py` printed
     `GITIGNORE_READY: no (missing: ...)`, i.e. WikiCommit was added to a repository that already
     had files of its own, or the repository predates a pattern the template gained later). Then
     `node_modules/`, `.wikicommit/.cache/` or `.wikicommit/run/` may not be ignored and
     `git add -A` would sweep in that repository's own untracked work. The printed guidance
     already explains this and offers the selective path; leave the choice to whoever knows what
     else is in the tree. **Read the printed line rather than the `.gitignore` itself** — the
     condition is about what is in the file, and `init.py` has already answered that
     deterministically, including the Quartz section it appends after the copy.
     Do not key this on `SKIPPED: .gitignore (already exists)`: that logs on **every** re-init,
     because `.gitignore` is `always_skip_existing`, so it would stop the offer in a repository
     WikiCommit made itself — where `-A` is exactly as safe as it was the first time.
   - **The working tree already has uncommitted wiki pages in it** — run

     ```bash
     git status --porcelain -uall -- '.wikicommit/entity/**/*.md' '.wikicommit/view/**/*.md' '.wikicommit/source/**/*.md'
     ```

     and hold the offer back if it reports anything at all. A re-init in a repository
     WikiCommit made itself answers `GITIGNORE_READY: yes`, and by then those directories can
     hold pages `/wikicommit-generate` wrote and `/wikicommit-merge` has not taken yet. `git add -A`
     would sweep them into this commit and `git push` would put them on the current branch, which is
     the one route the whole justification for this offer rules out: it rests on the commit holding
     no LLM-authored knowledge, and generated pages are exactly that. Say that `/wikicommit-merge`
     owns those files and leave the printed guidance as the answer, the same as the two cases above.
     This is not about `.gitignore` — those paths are tracked on purpose — so the `GITIGNORE_READY:`
     line says nothing about it.

     **Both halves of that command matter.** Scoping to `*.md` is what keeps a *first* init — the
     case this whole offer was built for — from tripping it: `init.py` creates those three trees
     holding nothing but `.gitkeep`, so a directory-level `git status --porcelain` reports
     `?? .wikicommit/entity/` and would withhold the offer every single time. And `-uall` is what
     makes the `*.md` scope work at all: without it git collapses an untracked directory into one
     `?? dir/` line that the pathspec then does not match, so a brand-new page under a brand-new
     `Person/` would go unseen — the case this condition exists for.
   - **The printed list still has a "Set up Quartz v5" step above the commit step** (the
     `--quartz`/`--quartz-pages` variants where `check_quartz_setup.py` did not report Quartz as
     fully set up). Committing ahead of that `git submodule add` / `npm install` splits the
     foundational commit, leaving `.gitmodules`, `quartz` and `package-lock.json` for a second
     one. **This case is deferred rather than skipped — see the last sub-step of this step**:
     on a first `--quartz` run it always holds, so skipping outright means Quartz users never
     reach the offer at all.

   With none of those in the way show `git status --short --untracked-files=all` and ask **once**
   — not per command, and not again after a no — naming the commit message the guidance just
   printed (`Run the
   foundational commit for you? It stages everything not excluded by .gitignore, shown above,
   commits it as "…", and pushes.`). `--untracked-files=all` is what makes "shown above" true:
   plain `git status --short` collapses an untracked directory into one `?? dir/` line, so a fresh
   wiki repository shows three lines for the ~769 files `-A` would stage, and nothing of the tree's
   own untracked work inside those directories is visible either.
   **Default to no**: this is outward-facing and hard to undo, the same reason the GitHub Pages
   activation earlier in this step asks before acting.

   On a yes, run `git add -A`, then `git commit` with that message, then `git push`, stopping at
   the first failure. **Do not also run the `package-lock.json` command the guidance prints** — that
   line is the selective path's substitute for `-A`, which already staged the file, and running a
   `git add` after the commit could only leave something staged and uncommitted. Give the commit the
   same trailers `wikicommit-merge` writes, passed through a quoted heredoc:

   <!-- commit-trailers:start (this block is identical in wikicommit-merge, -schema-propose, -update, -init and -organize; tests/test_commit_trailer_vendor_table.py holds them together) -->
   **Commit trailers.** Always write `Generated-By:   <current model ID>`: the ID of the model actually running this Skill, exactly as the runtime reports it — the same self-reported value `wikicommit-generate` writes into a page's `generated_by` (keep any suffix; do not shorten or normalize it; never hardcode one). Then choose `<Co-Authored-By line>` from the start of that same ID, so the two lines can never name different vendors:

   | `<current model ID>` starts with | `<Co-Authored-By line>` |
   |---|---|
   | `claude-`, or `claude-` after a provider prefix ending in `anthropic.` (Bedrock, e.g. `us.anthropic.claude-…`) | `Co-Authored-By: <Claude display name> <noreply@anthropic.com>` — the model's human-readable name, or just `Claude` when it is not known with confidence |
   | `gpt-` or `codex` | `Co-Authored-By: Codex <noreply@openai.com>` |
   | anything else | **no `Co-Authored-By` line at all** — `Generated-By` already records the model |

   GitHub resolves a co-author by the email address and shows that vendor's avatar on the commit, so a line naming a vendor that did not run this Skill misattributes it; writing none is the correct answer for a model not in the table. Decide by the model, not by the harness running it — one harness can run models from more than one vendor. If the harness appends its own co-author line after this message, leave it; an identical duplicate does no harm.
   <!-- commit-trailers:end -->

   Carrying them is the point — most of this commit is deterministic template output, but step 3's
   obvious-type judgment may have put a `.wikicommit/schema/<Type>.md` into it, and that file the
   model did author.

   **Best-effort end to end.** Any failure — no remote, no upstream, branch protection,
   unauthenticated, a pre-commit hook — is reported with its own output and handed back to the
   printed guidance; `wikicommit-init` never aborts over it. Say how far it got: a `git push` that
   fails after a successful `git commit` leaves the commit in place, so what remains is the push
   alone, not the whole block.

   **When that last case is the only thing in the way, wait for Quartz and come back to the
   offer**. This is not an extra courtesy — without it the offer is unreachable for
   every `--quartz`/`--quartz-pages` user: `check_quartz_setup.py` can only report Quartz as fully
   set up when `quartz/` already exists, which on a first run it never does, so `_QUARTZ_SETUP_FULL`
   is always printed and the condition always holds. Re-running `/wikicommit-init` afterwards
   would also reach it (a repository WikiCommit made itself keeps answering
   `GITIGNORE_READY: yes`). **Keep waiting here rather than sending the user away to re-run**:
   finishing Quartz setup and coming back within the same session is one continuous action, and
   re-running `/wikicommit-init` is a second invocation the user has to think to make.

   **One exception ends this case rather than deferring it: `--package-json-skipped`.** When step 2's
   `init.py` logged `SKIPPED: package.json (already exists)`, step 3.e never ran on purpose — and
   re-running `check_quartz_setup.py` here would run `npm install` against that repository's own
   pre-existing `package.json`, installing and executing its dependencies and lifecycle scripts
   unasked, which is precisely what step 3.d refuses to do. The reprint could not drop the step
   anyway: with that flag `print_next_steps.py` keeps "Set up Quartz v5" whatever the status says.
   So treat this like the cases that end the offer above — leave the printed guidance as the
   answer and say that
   the `package.json` merge is what the commit is waiting on.

   Ask them to run the printed "Set up Quartz v5" commands now and to say when they are done —
   **you do not run them** (`git submodule add` stays with the user; see the Notes). On a no or a
   "later", leave the printed guidance as the answer exactly as the skip cases above do and do not
   press — but the hold is not spent: if they come back later in this session saying Quartz setup is
   done, resume from the steps below then (the intervening work is usually the policy files, so
   "later" here is the common answer, not a decline). On a yes:

   1. Re-run `check_quartz_setup.py` (step 3.e above). It is safe to re-run: with `node_modules/`
      and `quartz/node_modules/` both present it skips `npm install` and reports `fully_set_up`,
      and its `npm run install-plugins` attempt is a fast no-op once the plugins are in place.
   2. Re-run `print_next_steps.py` with **exactly the flags you passed before, except
      `--quartz-status` and `--install-plugins-status`**, which take the values just recorded.
      Nothing else has changed in the minutes since — you still hold all of it, so do not re-derive
      it and do not ask the user to supply it. Print the output verbatim, as before.
   3. The "Set up Quartz v5" step is now gone from that output, so
      **apply the offer above to this reprinted guidance** (a standalone "Install Quartz community
      plugins" step may remain above the commit step if that attempt failed — that is not the
      condition above and does not hold the offer back) — the single `git status --short
      --untracked-files=all` confirmation, default no, the same commands and trailers.

   If the re-check still reports Quartz as not fully set up (their `git submodule add` or
   `npm install` failed), print the reprinted guidance, say that the commit is still waiting on
   that step, and stop. Do not ask again and do not loop.

4. If `init.py` fails (exit code 1), display the stdout and stderr output to the user and stop.

## Enabling comments (giscus)

Off by default, and this is a manual, one-time setup a human performs — not a step `init.py` runs. Nothing here is done on the user's behalf.

**Point them at `.wikicommit/guides/enabling-comments.md`** rather than walking them through it. That guide is written for a human, ships with every init, and is refreshed by later ones; this file is not — it is agent instructions, it loads in full on every Skill invocation, and its own advice was only ever shown "when they ask for it", which meant nobody found it.

What is worth knowing here, because it shapes what the agent should and should not offer to do:

- **It gives a reader somewhere to put a thought they are not yet sure enough about to open an Issue over** — "these two pages don't quite agree" being the one that matters most, since a contradiction between pages generated in different batches is out of reach of every automated check by design.
- **Three prerequisites are giscus's own** (a public repository, the giscus GitHub App installed, Discussions on with an Announcements-type category) and a missed one **fails at read time, not at build time** — the site builds, the box just does not work. The App step in particular cannot be confirmed from the command line, so never report the setup as complete on the strength of the config alone.
- **Existing wikis do not get the config block by re-initializing.** `quartz.config.yaml` carries the repository's own `pageTitle`/`baseUrl`/links, so it is never overwritten; the guide says how to copy the block in by hand.
- **Do not wire reactions or discussions to `review_status`.** A 👍 means "this was good", not "I read this and had nothing to report"; there is no principled threshold on a running count for a two-valued field; `reviewed` is a claim this wiki makes to its readers and closing a tracking Issue needs write access, which reacting does not; and a discussion only comes into existence once someone reacts, so "pages nobody has looked at yet" would stop being listable.

## Skill auto-invocation guard (`.claude/settings.json`)

`init.py` merges three `skillOverrides` entries into `.claude/settings.json`, setting `wikicommit-generate`, `wikicommit-merge` and `wikicommit-translate` to **`name-only`**. Those three do not carry `disable-model-invocation`, so that unattended runs have a path at all, which also made it possible for a model to start them off a passing request. `name-only` hides the description — the mechanism a model matches against — while leaving the name and the `/` menu intact, so a prompt that says `/wikicommit-generate` still works and **nothing has to be flipped to run unattended**. `user-invocable-only` would: it blocks model invocation outright, and turning it back to `on` is all-or-nothing, re-enabling auto-invocation for every Skill in the repository at once.

**Tell the user this is there, and that they can change it.** Editing `.claude/settings.json` by hand is the whole interface — there is no flag and no prompt. Setting a Skill to `on` restores its description and lets a model start it; `off` removes it from the `/` menu entirely.

**Existing repositories do not get this.** It arrives only on a repository that runs `/wikicommit-init` from here on, which is the same "new and old coexist" rule the rest of this file follows. The guard that does reach an already-installed wiki is the narrowed Skill description, and that travels with `npx skills add`. **Do not describe a wiki initialized before this as protected.**

**A key that already has a value is never touched**, under any flag including `--no-overwrite`. An operator who set one to `on` is running unattended deliberately, and a re-init quietly putting it back would stop those runs while printing a success line. `init.py` prints one of `CREATED:` / `UPDATED:` (only the absent keys were added) / `SKIPPED:` (all three already present) so the user can see which of those happened. If the file exists but is not a readable JSON object, it is left strictly alone and a `WARNING:` says the guard is **not** in place — rewriting it would destroy settings the script cannot read.

## Notes

- **README.md: init writes one only when there is none, and never edits one that exists.** An existing README is very likely a file with its own structure (especially when WikiCommit is added to an existing repository), so an automatic insertion risks breaking it — which is why, when a README is already there (in the root, `.github/` or `docs/`, under any extension or case), the link and licensing wording stay display-only suggestions in the guidance. When there is none, `init.py` writes a fixed English template with the repository name filled in (no LLM-written text, so it rides in the foundational commit), and `--finish-readme` fills in the published-site link in the same run. The agent itself still never edits README.md; a README from an earlier run is the user's file
- Call `init.py`. Do not manually create directories in the agent itself (script delegation pattern)
- Writing to `.wikicommit/schema/` is done by `init.py`. The agent must not write to it directly, with one narrow exception: step 3's obvious-type judgment may write a new `.wikicommit/schema/<Type>.md` file the user approved there — it only ever adds a file that isn't already there, never edits or overwrites one `init.py` wrote. This is the first and weakest of three type-proposal entry points — it judges from the `theme` sentence alone, before any source has been read, so its approval bar is the strictest of the three; `wikicommit-collect`'s Type Proposal step judges from candidate titles and search summaries, and `wikicommit-generate` Pass 2b judges from the full source text. All three skip types that already have a file under `.wikicommit/schema/`, so they are not redundant with each other
- `init.py` does not fetch the Quartz v5 core (`quartz/` directory) automatically. Adding the git submodule involves network and git operations, so the user must run it manually per the next-steps guidance above
- **The foundational commit: the agent offers to run it, after asking once.** The rule is that **an LLM's commits go through a PR** so that every LLM-*authored* page reaches `main` through a diff a person can review. The foundational commit contains no LLM-authored knowledge (deterministic `init.py` template expansion, plus type files the user approved with Enter), and **no PR route is available to it**: `/wikicommit-init` is often a repository's first commit, so there may be no base branch to open a PR against, and possibly no remote at all. So: ask once, default no, run on a yes, and fall back to the printed guidance on a no, on a non-interactive run, or on any failure. The hold-back cases in step 3 keep that premise true: a `.gitignore` without WikiCommit's patterns (`GITIGNORE_READY: no`) means `git add -A` would reach beyond WikiCommit's own output; uncommitted pages under `.wikicommit/entity/` / `.wikicommit/view/` / `.wikicommit/source/` are LLM-authored and belong to `/wikicommit-merge`. Key the `.gitignore` case on `init.py`'s `GITIGNORE_READY:` line, which answers from the file's contents (`_root_outputs.missing_gitignore_patterns()`, shared with `print_next_steps.py` so the offer and the printed note never disagree) — not on the `SKIPPED: .gitignore` log line, which appears on every re-init. A pending "Set up Quartz v5" step is **deferred, not skipped**: it holds on every first `--quartz` run, so the agent asks the user to finish Quartz setup, re-checks the status, reprints the guidance without that step, and makes the offer against the reprint — except under `--package-json-skipped`, where the re-check would run `npm install` against the repository's own `package.json`. See step 3's final sub-step for the commands and the trailers
- **`git submodule add` stays with the user, and the reason is not the one above.** A submodule changes the repository's structure and fails in its own way, with its own recovery; it is out of scope here
- The `gh api repos/{owner}/{repo}/pages` call in step 3 only runs when `--quartz-pages` was specified (`--quartz` alone sets up local build/preview only and never touches GitHub Pages). It is a GitHub *repository setting* change (enabling Pages), not a write to `main` or to the wiki content, so the agent runs it directly — unlike the `git add`/`commit`/`push` commands above, it does not need to be deferred to the user. It is unconditionally best-effort: any failure (missing remote, unauthenticated `gh`, plan restriction, permissions) falls back to printed manual instructions and never aborts `wikicommit-init`
- The `gh api repos/{owner}/{repo}/actions/permissions/workflow` calls in step 3 (enabling "Allow GitHub Actions to create and approve pull requests") run unconditionally, regardless of `--quartz`/`--quartz-pages` — unlike the Pages setting immediately above, this one backs `review-issue-close-sync.yml`, which every variant generates. It is the same kind of GitHub *repository setting* change as the Pages call, so the agent runs it directly and does not defer it to the user. It is unconditionally best-effort: any failure (missing remote, unauthenticated `gh`, insufficient token scope) falls back to printed manual instructions and never aborts `wikicommit-init`. The GET-before-PUT check exists to make the change idempotent and to avoid silently overwriting the unrelated `default_workflow_permissions` field the same API endpoint also controls
- The `lychee --version` / `cargo install lychee` calls in step 3 only install a local dev tool — they touch neither Git nor `main` — so the agent runs them directly and unconditionally (no prior user confirmation needed, unlike the Quartz Y/n prerequisite). Like the GitHub Pages step, this is best-effort: any failure (`cargo` missing, network unreachable) falls back to the printed manual instructions and never aborts `wikicommit-init`
- The `markitdown --version` / `pip install 'markitdown[pdf]'` calls in step 3 mirror the lychee handling above — a local Python package install that touches neither Git nor `main`, so the agent runs them directly and unconditionally, independently of the lychee outcome. `markitdown` is required by `wikicommit-generate`'s URL extraction and its `.pdf` fallback (hence the `[pdf]` extra). It is best-effort: any failure (`pip` missing, network unreachable) falls back to the printed manual instructions and never aborts `wikicommit-init`
- The `python -c "import markdown_it"` / `python -m pip install markdown-it-py` call in step 3 is the same kind of best-effort local install. It is not optional the way markitdown is: `check_raw_html.py` is a blocking gate that fails closed without the package (stderr `ERROR:`, exit 1), so a wiki without it cannot merge any page. When the install fails, the printed guidance carries `pip install markdown-it-py` as its own step; `/wikicommit-update` makes the same check for repositories initialized before the check needed it
- The `check_quartz_setup.py` call in step 3.d (when `--quartz` was specified, and only if `init.py` actually generated `package.json` rather than skipping a pre-existing one — see step 3 above) mirrors the lychee "check first, only act if needed" pattern: its `node_modules` / `quartz/node_modules` pre-check avoids re-running a possibly slow `npm install` when a `--no-overwrite` re-init finds Quartz v5 already fully set up, and it runs `npm install` itself when needed. `npm install` touches neither Git history nor `main` (the `git submodule update` its `postinstall` may run only affects the working tree), so the agent runs the script directly without prior user confirmation. Because `postinstall` guards on `quartz/`'s existence, `npm install` exits 0 either way; the script distinguishes "fully set up" from "top-level dependencies only" by checking for `quartz/` afterward and reports one JSON contract, so the agent does not branch on exit codes. Any `npm install` failure is reported as one of the `npm_install_failed_*` statuses, which keep `npm install` in the printed manual instructions; the script always exits 0 and never aborts `wikicommit-init`
- `print_next_steps.py` (step 3's final call) owns the "Next steps" guidance text itself — which lines to show/omit/reword is fully determined by the flags the preceding sub-steps already computed (variant, install statuses, GitHub Pages `html_url`, Quartz setup status). It only ever formats and prints text to stdout — it never touches Git, `main`, or `.wikicommit/schema/`, so the agent runs it directly and prints its output to the user verbatim, same as the other auto-run steps in step 3
- The "Set up Quartz v5" guidance line (`print_next_steps.py`'s `_QUARTZ_SETUP_FULL`/`_QUARTZ_SETUP_NPM_ONLY`) appends `npm run install-plugins` after `git submodule add` / `npm install`, with a note that the first run commonly takes several minutes. `check_quartz_setup.py` cannot auto-run this itself on a first-time init: at the point it runs, `quartz/` does not exist yet. Putting it in the same manual block means the user pays this cost once, right after adding the submodule, rather than it landing on whichever `/wikicommit-serve` run first calls `npm run install-plugins` and timing out there
- **`--no-overwrite --quartz` re-init and `npm run install-plugins`**: when `quartz/` already exists and is fully set up, the "Set up Quartz v5" step is omitted, yet `node_modules` says nothing about whether the separate `npx quartz plugin install --from-config` step has ever run. So whenever `quartz/` exists (`fully_set_up`, `npm_install_completed_fully_set_up`, `npm_install_failed_submodule_exists`), `check_quartz_setup.py` also runs `npm run install-plugins` best-effort and reports `install_plugins_ok`. `print_next_steps.py` uses that field: success gets a `✅ Quartz community plugins installed` announcement. In the two fully-set-up statuses, success omits the step and failure prints a standalone `_INSTALL_PLUGINS_STEP` reminder; in `npm_install_failed_submodule_exists`, success drops the now-redundant `npm run install-plugins` line (→ `_QUARTZ_SETUP_NPM_INSTALL_ONLY`) and failure keeps it (`_QUARTZ_SETUP_NPM_ONLY`). Same local, Git-free operation, so no additional user confirmation is needed
- **`repair-plugin-builds.cjs`**: `npm run install-plugins` can leave a plugin permanently stuck. Quartz's installer writes a plugin's `quartz.lock.json` entry as soon as `git clone` succeeds, before the plugin's own build (run in the plugin's own directory); if that build fails, the entry stays, so later runs treat the plugin as installed and skip it forever, and `npx quartz plugin install` still exits 0. `repair-plugin-builds.cjs` (appended to the `install-plugins` npm script) treats a plugin as stuck when its directory exists in `quartz/.quartz/plugins/` but has no `dist/`, deletes that directory and lockfile entry, and re-runs `npx quartz plugin install --from-config` (bounded to 3 attempts, then an error naming the plugin and the command to run inside its directory). Adding `shiki` to the root `package.json` does not help: each plugin builds with its own directory as `cwd`, never touching this repo's root `node_modules`
