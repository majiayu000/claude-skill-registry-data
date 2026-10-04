---
name: licensing-review
description: Verify a third-party library, asset, model, font, dataset or copied snippet is safe to ship under the project's licensing stance, and record it. Use before adding or upgrading any dependency, before downloading any asset, and before a release.
---

The always-on prohibitions live in the selected `licensing` stance. Resolve its shared source
with `citizen stances --json`; runtime projections carry the same policy. This is the procedure.

## Before adopting or upgrading

1. **Read the authoritative license**, not the marketplace blurb or the README badge. Check
   the exact version you are taking.
2. **Inspect the actual package**, including transitive dependencies and any separately
   licensed textures, data, fonts or bundled code inside it.
3. **For dual licensing**, record which qualifying option you are taking. Where terms are
   combined rather than alternative, all of them must comply.
4. **Check authorship and provenance.** An uploader's claim does not establish ownership.
   Reject game rips, unlicensed copies, and anything with missing, conflicting or suspect
   rights.
5. **Recheck on upgrade.** Terms change between versions. Pin a floor you have actually run
   against.
6. **No new third-party dependency without a reason the reviewer will accept.** In a shared
   repo that means an issue or a note in the PR; in a solo repo it means one sentence in the
   commit.

If nothing compliant fits, adapt a compliant base or create original work. Do not weaken the
policy to use a download. Catalog availability is not asset clearance.

## Record it

Every incorporated component goes in the project's third-party manifest with:

- Source URL
- Creator or rightsholder
- Exact version, or asset hash
- License identifier, and the preserved license text
- Modifications made
- Required attribution

## Notices that actually ship

- Keep `THIRD_PARTY_NOTICES` and any credits screen current.
- Preserve copyright, license and disclaimer text. Include required NOTICE content and license
  links. Identify modifications where the license requires it.
- **A repo-only notice is insufficient if recipients do not receive it.** Verify the notices
  are in the actual distribution before release.
- Maintain this automatically. Do not hand routine compliance work to the user.

## CC BY specifically

Preserve the recipient's licensed rights. Review EULA and DRM packaging, and do not apply
additional restrictions to that content. If the intended distribution cannot comply within
this policy, choose another asset. Never claim that one credit line alone satisfies every
license.

## At release

Verify every shipped third-party component has a recorded qualifying license and that notices
are present in the built artifact. Report unresolved items plainly. Do not delete existing
work to clear a finding, and do not claim an audit happened when it did not.
