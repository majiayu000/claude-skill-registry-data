---
name: decide
description: The lead decides what a lane asked for and couldn't do itself (a new package, a migration, a protected file, a UX question) against the story's requirements, the spec, the principles and the architecture. Approves it, answers the lane with something that fits better, or takes it to the person only when it crosses a guardrail. Use when code-kit's loop or `code-kit next` says a lane waits on your decision, when a lane hands back a change request, or when the person runs /code-kit:decide [request numbers].
---

# Decide a lane's request

The person is the product owner and sets the guardrails: the specs, the screens' visual design, CI and the pipelines, the kit (the rules in `.claude/code-kit.json`), and product questions the spec doesn't answer, plus anything with production, cost or strategy implications. Everything technical is yours by default: contracts, migrations, packages, merges into the base, and a weakened test on a lane's branch once you've reviewed it (`code-kit approve tests --lane <lane> --delegated --story ST-n --reason "…"`); on your own branch a weakened test is the person's. Inside them, you run the team. A lane that needs something it can't do itself asks you, and you decide on the merits. Passing a request to the person because you could is not deciding: they'd approve it by default, and the check would be gone.

**Under vibe** (`harness.autonomy` is `vibe`) the guardrails are yours too: every request is `by: "lead"`, the spec, the design, CI, the kit, the standards and weakened tests on any branch included, and a package beyond the registry's rules is your judgement (approving it records which rules it breaks). Decide each as the person would, against the brief and the principles, and say why in the reason. Nothing goes to the person but what only they can give: an account, a key, a payment, an act outside the repository (`code-kit ask … --needs …`).

The CLI is `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs"`.

## 1. Find the requests

`requests --json` lists each open request with its number (`n`), the lane, what it asked for (`names`, `what`), and whose decision it is (`by`). The argument, if given, names the numbers to take. Take every request `by: "lead"`. A request `by: "person"` is theirs: see step 4.

For each, read the lane's change request (its report, in `.claude/state/reports/<branch>.md` in its worktree), its story in the plan, and the requirements the story cites, in the specs.

## 2. Judge it

**A package.** Approve it only when all of these hold:

- The story's requirements need what it does. Name the requirement.
- Nothing the project already depends on does the job: read the manifest (`package.json`, `pyproject.toml`, `Cargo.toml`…) and search the code for an existing helper.
- It fits the principles (`docs.principles`) and the lane's layer: a layer's `denyPackages` in the config, and anything the principles say about dependencies, such as no SDK in the domain layer, or a port before a vendor.
- It's the lightest thing that does the job. A whole framework for one function is the wrong answer; the standard library or a few lines of code may be the right one.
- It's maintained, and its licence is one the project can ship. For npm packages, `approve` checks the registry against `approvals.delegate.dependencies`. For other ecosystems the check is yours: look at the package's page.

**A protected file** (a migration, a validator, anything in `protected` that's yours to approve). Approve it when the change carries out what the story's requirements ask, and nothing more: a migration that adds the columns the spec names, a validator change the spec's rule requires. A change the spec doesn't call for is scope creep; send it back.

**A UX question** (what a screen does on an error, an empty list, a slow load, a second tap, the wording the spec implies). Answer it from the spec and the principles the person agreed, and write the answer where the lane will read it: the story in the plan, or the spec section's notes. Ask the person only when the spec and the principles don't settle it. A screen's visual design is theirs: it's approved before the screen is built.

## 3. Act on it

- **Yes.** Approve it for the lane and the story, saying why in the reason:

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" approve <package or approval> --lane <lane> --delegated --story ST-n --reason "<the requirement it serves, what the project already has, how it fits>"
  ```

  Then resume the lane: SendMessage to its agent if it's still running, or dispatch the story again with "approved: <what>" in the brief.

- **Something fits better.** Drop the request with the reason, and tell the lane what to use instead:

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" requests drop <n> --reason "<use X instead, because …>"
  ```

- **It crosses a guardrail.** A package that would break a principle, change the architecture or need a spec change; a change to the spec or a contract; a product question the spec doesn't answer. Take it to the person with your recommendation, and carry on with what doesn't depend on it:

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" ask "<the question, in a sentence>" --story ST-n --blocks --why "<which guardrail it crosses>" --option "<choice>: <what it does>" --option "…"
  ```

## 4. The person's requests

A request `by: "person"` is a guardrail the lane hit: a spec, a contract, a design, CI, or a weakened test. Check the lane really needs it first: often the story can be done inside the guardrail, and you tell the lane how and drop the request. If it does need it, the request is already waiting for the person, in their band and the pane's Needs you. Add your recommendation with `ask` when the choice isn't obvious from the request alone.

## 5. Report

One line per request: what was asked, what you decided, and why. "ST-138: pillow approved for api (MED-5 needs HEIC decoding; nothing installed reads HEIC)." Then carry on with the build.
