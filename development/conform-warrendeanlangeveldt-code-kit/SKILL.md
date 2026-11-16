---
name: conform
description: Bring an existing codebase to the project's standards and engineering principles. Measures its structure (large files, import cycles, dead code, services read straight from the environment), suggests the standards (those the code already follows, and those it should move to, structural ones included), proposes a target architecture (modules, layer rules and lanes), audits the code against each standard the person adopts, records every breach in the baseline as evidence, and drafts a refactor pathway (a conformance milestone per standard, layer by layer, with the splits and moves) for the plan. Use for a brownfield project, when the person wants the code refactored to the standards, when code-kit next says the project has no standards or a standard has breaches no story covers, or runs /code-kit:conform [standard ids].
---

# Conform existing code to the standards

Only the lead runs this. The CLI is `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs"`, from the project root; below it's `code-kit`.

New code is held to a standard as soon as it's adopted. Existing code that breaks it is recorded, file by file, in the baseline (`.claude/code-kit.baseline.json`), and brought to it two ways: by the refactor stories of its conformance milestone, and by every story that changes one of those files, which must fix its recorded breaches before it merges (verify refuses it otherwise). The breaches only ever shrink, except on the branch that adopts the standard.

The argument names standards to audit or plan (`PAT-1 ARC-2`). With none, start from step 1.

## 1. The standards

Run `code-kit standards`, and `code-kit conform measure` for the code's structure: the files over 500 lines (`--lines N` for another size), the import cycles, the files nothing imports, and the files that read the environment themselves. They are evidence for the structural standards below, not breaches yet.

- **None yet:** suggest them as `/code-kit:init`'s Standards section describes (`${CLAUDE_PLUGIN_ROOT}/skills/init/SKILL.md`), in two groups:
  - **What the code already follows**, inferred from it with the evidence ("41 of 43 modules reach the database through repositories"), as init does.
  - **What it should move to:** the engineering principles and patterns the project's docs ask for (architecture, decisions, ADRs, principles) and the code doesn't follow yet, and the ones its stack and size call for that nothing covers (data access behind one boundary, no business rules in handlers or screens, secrets from the environment, one way to call each external service). For each, say what it is, why, how much of the code breaks it today (a rough count from a first look), and whether it's `required` or `recommended`. A pattern the code follows both ways is put to the person as a choice, with both counts.
- **Some already:** offer the ones the code should move to that the file doesn't have, the same way.
- **The structural ones**, each with its evidence, whenever the code shows the need:
  - **One responsibility per module** (god classes and god modules): a file or class that mixes data access, business rules, presentation or several features. The measure's large files are where to look; the audit says which responsibilities each mixes and how to split it.
  - **Service providers** (dependency inversion): each external service (the database, email, payments, a model provider, storage, queues) behind one interface, its implementation wired in one place (a provider, container or composition root), and configuration read once and passed in. Evidence: the measure's files that read the environment themselves, and the audit's handlers and components that construct a client or call a service's SDK directly.
  - **No import cycles**: the measure finds them exactly.
  - **No dead code**: the measure's files nothing imports, once each is checked not to be an entry point a framework or a script loads.
  - **One place for each rule** (no duplicated logic): the audit finds the same rule or calculation written in several files.
  - **Modules by feature, with a public surface**: a feature's code reached through its entry point, not its internals, where the code is organised by feature or should be.

Standards are guardrails, and guardrails are the person's: write nothing until they approve, edit or drop each one. Then write them to `docs/standards.md` (or `docs.standards`) on a branch, `lead/conform-<ids>`, with the person's `standards` approval.

## 2. The target architecture

Where the code has no layer rules, or the ones it has don't describe how it should be built, propose the target: the modules or layers the code should have (for example domain, services, data access, providers, interface), what each may import, the packages each may not use (the interface layer may not use the database client), and the lane that owns each. Put each existing folder in its layer, and name the files that belong in another layer or in a module that doesn't exist yet: they become moves and splits in the audit.

Draft it as `/code-kit:init` drafts a config (`${CLAUDE_PLUGIN_ROOT}/skills/init/SKILL.md`): write `.claude/code-kit.draft.json` from the live config with the new `layers` and `lanes`, run `code-kit diff --config .claude/code-kit.draft.json` and `code-kit baseline --config .claude/code-kit.draft.json`, and show the person the layers, the rules, the lanes, and how many imports break the rules today. Nothing is enforced until they approve. Then copy the draft over the config on the branch, and run `code-kit baseline --write`: on the branch that adopts layers, or changes their rules, their violations are recorded, and new code is held to them at once. The commit needs the person's config approval.

## 3. The audit

For each standard being adopted (new on this branch, or tightened), find where the code breaks it. A breach is evidence: the file, where in it, and what breaks the standard, in one line ("line 42: the handler queries the database itself"). Never a guess.

- **Enforced by a layer rule:** `code-kit baseline` already finds these; `code-kit baseline --write` records them. Don't record them again.
- **Checked or advice:** audit the code layer by layer with read-only agents, one per layer or per few hundred files, in parallel. Start each with the Agent tool (any type outside the lanes; code-kit's hooks hold such agents read-only), giving it the standards to look for with their why, the files to read (`git ls-files` under the layer's paths, without tests and generated files), and this answer shape:

  ```json
  {
    "breaches": [
      {
        "standard": "PAT-1",
        "file": "src/api/orders.ts",
        "breach": "line 42: the handler queries the database itself"
      }
    ]
  }
  ```

  Tell it to read every file it's given, to report only what it saw, with the line, and to report nothing for a file that meets the standard.

Check a sample of each agent's breaches yourself, then record each:

```bash
code-kit conform record PAT-1 src/api/orders.ts --breach "line 42: the handler queries the database itself"
```

A breach fixed by splitting the file, or moving it to the layer or module it belongs in, says where to, so its story does exactly that:

```bash
code-kit conform record ARC-2 src/orders.ts --breach "mixes the order rules, their storage and the email" --split "src/orders/rules.ts, src/orders/repository.ts, src/orders/notify.ts"
code-kit conform record ARC-1 src/api/pricing.ts --breach "business rules in the interface layer" --move src/domain/pricing.ts
```

A measured kind is recorded in one go, once the person has adopted its standard: `code-kit conform record PRI-3 --measured cycles` (or `large`, `unused`, `env`). Take out any the person excuses with `conform fixed` before committing.

`code-kit conform` then shows each standard's breaches by file. Commit the standards file and the baseline together on the branch. verify accepts breaches only for the standards this branch adopts, and the commit needs the person's `standards` approval.

## 4. The refactor pathway

```bash
code-kit conform plan            # every standard with breaches no open story covers
code-kit conform plan PAT-1      # one
```

It drafts the pathway: a conformance milestone per standard, the layer rules' recorded violations first (`**Conforms:** layers`), then required standards and structure before detail (architecture, patterns, policies, conventions, then principles). A split or a move is a story of its own, its new files in its `**Files:**`. Each milestone's stories go through the layers in dependency order, so what other layers import is refactored first. A story takes at most five files of one lane's folder, and depends on the same standard's stories in the layers it imports. The first story of each milestone waits on the last of the one before. Each story carries `**Requirements:** none`, `**Conforms:**` (its standard), `**Files:**`, `**Depends on:**` and `**Size:**`, lists its breaches, and asks for tests that pin down what the files do first, where they have none.

Show the person the pathway: how many milestones and stories, and the order. They decide where the milestones go among the feature milestones (each is its own milestone, never mixed into a feature one). Then add the milestones to the plan as they approve them, and commit the plan with the standards and the baseline, or on its own if those are merged already.

## 5. After

- Refactor stories are dispatched like any other. Their lane runs `code-kit conform --story <id>` for what to fix, fixes each breach without changing what the code does, and runs `code-kit conform fixed <standard> <file>` for it; verify refuses the branch while a breach in its files is still recorded. A split's breach comes out only once its new files exist, and a move's once the file is at its new path and gone from the old one. A layer rules story fixes the imports and runs `code-kit baseline --write`.
- Any other story that changes a file with recorded breaches fixes them too, except a split or a move, which its own story does (`code-kit conform --for <files>` lists them); verify refuses it otherwise. A breach too large to fix in that story is a reason to schedule its refactor story first, not to merge around it.
- In review, check each breach taken out is really fixed, and that behaviour didn't change: the same tests pass, none weakened. A breach removed from the baseline but still in the code is sent back.
- `code-kit conform` shows the progress: each standard's breaches, its stories and what's not planned yet. `code-kit next` says when a standard has breaches no story covers.
