---
name: publish-github-skills-exercise
description: "Prepare a GitHub Skills exercise for publication, contribution, or rollout. Use this when the user asks for release readiness, final checklist, README/marketplace copy, PR description, validation evidence, launch notes, or publishing guidance for a GitHub Skills-style exercise."
---

# Publish GitHub Skills exercise

Use this skill for final release preparation after an exercise has been built and reviewed.

## Publication workflow

1. Confirm the repository communicates the exercise clearly.
2. Confirm the learner flow has been validated from a fresh start.
3. Confirm workflow permissions, triggers, and reset behavior are safe.
4. Confirm exercise workflows are disabled by default so nothing runs until the learner starts.
5. Confirm all images, links, snippets, and badges render correctly.
6. Prepare release or contribution copy.
7. Identify any remaining risks and the owner of each follow-up.

## If publishing a repository is requested

> [!IMPORTANT]
> Never publish or transfer without explicit authorization that names the target owner and repository.

Confirm which path applies before running anything:

- publish to a personal account,
- publish to an organization,
- transfer an existing repository from one organization to another.

### Path A: publish to a personal account or organization

1. Confirm target owner/repository and whether a remote already exists.
2. **Confirm the intended visibility explicitly.** Ask the user whether the exercise should be public or
   private, and use the matching flag. Never default to public: a repository meant to be private is exposed
   the moment it is created, and flipping the flag afterwards does not undo that exposure.

   Public is the common choice for GitHub Skills exercises, because private repositories consume Actions
   minutes. Surface that as a recommendation, not as a silent default.

3. If the target repository does not exist, confirm you have permission to create repositories in the target owner. For
   an organization, that is the `Create repositories` permission, plus admin on the new repository to set the
   template flag. If it already exists, confirm admin access to change its Actions and template settings.
4. If the target repository does not exist, create it with Actions disabled before any content exists, so nothing
   runs on first push. If it already exists, do not run `gh repo create`; disable Actions before pushing, and
   do not change the existing repository's visibility unless the user explicitly asks for that change:

   > ![Static Badge](https://img.shields.io/badge/Terminal-text?logo=gnometerminal&labelColor=0969da&color=ddf4ff)
   >
   > ```bash
   > # Run the create command only for a new repository.
   > # VISIBILITY is --public or --private, exactly as the user confirmed above.
   > gh repo create ORG/REPO VISIBILITY --description "Exercise: TITLE"
   > gh api -X PUT repos/ORG/REPO/actions/permissions -F enabled=false
   > ```

5. Push repository content.
6. Apply repository settings:

   > ![Static Badge](https://img.shields.io/badge/Terminal-text?logo=gnometerminal&labelColor=0969da&color=ddf4ff)
   >
   > ```bash
   > gh api -X PATCH repos/ORG/REPO -F is_template=true
   > gh api -X PUT repos/ORG/REPO/topics -f names[]=skills-exercise
   > ```

7. Re-enable Actions, then set the workflow enablement state:

   > ![Static Badge](https://img.shields.io/badge/Terminal-text?logo=gnometerminal&labelColor=0969da&color=ddf4ff)
   >
   > ```bash
   > gh api -X PUT repos/ORG/REPO/actions/permissions -F enabled=true
   > gh workflow list --all --repo ORG/REPO
   > ```

8. Verify only the start workflow (`Step 0`) is enabled. Disable every later step workflow; they are enabled
   by the preceding step as the learner progresses.
9. Verify the README Copy Exercise badge uses the published `template_owner` and `template_name`, and that its
   `visibility` parameter matches the visibility the user confirmed.

### Path B: transfer between organizations

Pre-checks before transferring:

- You are an owner or admin of the source repository and can create repositories in the destination org.
- No repository with the same name already exists in the destination org.
- Record the current workflow enablement state so you can restore it after transfer.
- Warn the user that the old `owner/repo` URL will redirect, but forks, stars, and existing copies keep
  pointing at the redirect.

Transfer:

> ![Static Badge](https://img.shields.io/badge/Terminal-text?logo=gnometerminal&labelColor=0969da&color=ddf4ff)
>
> ```bash
> gh api -X POST repos/SOURCE_ORG/REPO/transfer -f new_owner=DEST_ORG
> gh repo view DEST_ORG/REPO --json name,owner,isTemplate,visibility
> ```

Post-transfer fixes, all of which are commonly missed:

1. Update the README Copy Exercise badge `template_owner` and `template_name` to the new owner. This is the
   single most common breakage after a transfer.
2. Re-verify the template flag survived the transfer; re-apply with
   `gh api -X PATCH repos/DEST_ORG/REPO -F is_template=true` if needed.
3. Re-verify Actions are enabled and that only `Step 0` is enabled.
4. Re-check any absolute links, badges, or `uses:` references that name the old owner.
5. Re-check repository secrets, variables, and branch protection; these do not always carry over.
6. Confirm the destination org's Actions policy allows the actions this exercise uses
   (`actions/checkout`, `skills/exercise-toolkit`, `skills/action-keyphrase-checker` when used, `GrantBirki/comment`,
   `peter-evans/find-comment`).

### Failure handling

If permissions block any step, report the exact failing command, the permission required, and the shortest
manual recovery path. Do not retry destructive operations or work around a permission failure.

## Release-readiness checklist

- README includes title, Welcome block, learner audience, prerequisites, duration, start path, and support path.
- The Copy Exercise badge uses the correct `template_owner` and `template_name` for the published location.
- Exercise steps match the stated objectives.
- Every step has a Theory block with real content and at least one Activity block.
- Copilot prompts and terminal commands in activities use the standard badge blocks.
- No placeholder text remains anywhere in `README.md` or `.github/`: not only `replace-me`, but bare
  skeleton tokens (`OWNER`, `REPO`, `ORG`, `TITLE`, `FEATURE`) and bracketed slots such as `[Step name]`.
- Step content and step workflows align by number; the final workflow is `N-last-step.yml` and the review
  content is `.github/steps/x-review.md`.
- Every `skills/exercise-toolkit` reference uses the same pinned release tag.
- Workflows use least-privilege permissions and have clear trigger behavior.
- Exercise workflows are disabled by default and only run as the learner progresses through the exercise.
- Validation evidence is available: tests, dry run, or documented manual checks.
- Reset/retry behavior is documented and safe for repeated learners.
- No source content contains repository-specific absolute URLs unless required.
- Exercise images are stored in `.github/images` and referenced with relative paths.
- `[!NOTE]`, `[!IMPORTANT]`, and `[!TIP]` callouts are left-justified (no indentation).
- License, attribution, and contribution notes are present where needed.

Expected callout formatting:

> [!NOTE]
> This is a note

> [!IMPORTANT]
> This is an important item to be aware of for this exercise

> [!TIP]
> It is a good idea and recommended to do this tip

## Output template

```markdown
## Publish recommendation

## Release summary

## Validation evidence

## Final checklist

## Publish or transfer plan

## Suggested PR description

## Suggested release notes

## Remaining risks
```

Be direct if the exercise is not publishable yet. Include the shortest concrete path to readiness.
