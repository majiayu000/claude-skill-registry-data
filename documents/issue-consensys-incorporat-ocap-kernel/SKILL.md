---
name: issue
description: Files a GitHub issue for one finding, labeled by kind and area.
unsandboxed: true
---

When asked to file an issue, follow these steps:

1. **Search first.** Search open issues for the function, file or symptom, e.g.
   `gh issue list --search "<symbol or phrase>"`. If an issue already covers the
   finding, comment there instead of filing.

2. **One finding per issue.** Separate findings get separate issues, even when
   one review turned them up. Two reports about the same line of code are one
   finding.

3. **Labels.** Run `gh label list --limit 100` and read the descriptions. Pick:

   - Exactly one kind: `bug`, `enhancement`, `chore`, `documentation`, `tests`
     or `research`. Between `bug` and `enhancement`, ask whether the current
     behavior contradicts what the code or docs promise; if it does, it is a
     `bug`.
   - Exactly one `area: *` label, by its description. If two fit, pick the one
     where the fix lands.
   - `security` as well, when the finding breaks one of the three properties in
     Mark Miller's security model:
     - confidentiality or integrity, across any vat or peer boundary;
     - availability, only when a peer is the attacker. A vat that exhausts
       resources is outside the model.

4. **Umbrella.** If an open tracking issue covers this work, make the new issue
   its sub-issue with `--parent <parent>` rather than writing a "Related:" line.
   For an issue that already exists, run `gh issue edit <number> --parent <parent>`.

5. **Title and body.** The title states the symptom as a sentence. The body is
   plain paragraphs:

   - what happens and where, naming the file and symbol;
   - what that leads to;
   - a proposal, if there is one;
   - how it was found, e.g. "Raised in the review of #1094."

6. **File.**

   ```sh
   gh issue create --title "<title>" --body-file <file> \
     --label <kind> --label "area: <name>" [--label security] [--parent <parent>]
   ```

   Report the issue URL.
