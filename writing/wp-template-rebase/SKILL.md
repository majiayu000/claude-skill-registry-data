---
name: wp-template-rebase
description: >
  Rebase an overridden WordPress or WooCommerce template onto the version currently installed,
  keeping its customizations and explaining what each one is for. The override can live in a
  theme or child theme, in a plugin that serves its own copies of another project's templates, or
  in a standalone file. Diffs the override
  against the pristine template of the release it was copied from, replays the customizations onto
  the current upstream template, annotates them with begin and end markers, and bumps the @version
  header. Covers WooCommerce templates, parent theme templates copied into a child theme, other
  plugins' templates, and WordPress core.
  Triggers: "update this template override", "this WooCommerce template is out of date", "rebase
  the overridden templates", "version X is out of date, the core version is Y", "refresh the
  theme's woocommerce templates", "bring in the new template but keep my changes", "outdated
  templates in the WooCommerce status report", "which templates is this theme overriding".
---

# WordPress template rebase

Refreshing an overridden template means reconstructing what somebody customized in the first place,
which is the part nobody writes down. This skill makes that mechanical: the customizations are
recovered by diffing the override against the pristine template of the release it was copied from,
replayed onto the current upstream template by a real three-way merge, and left annotated so the
next pass is cheap. A rebase is a diff plus a merge plus a verification pass, not a reading of the
new template and a hopeful rewrite.

## Hard rules

1. **Both sides always come from the project's public repository at the matching tag.** Never diff
   against the copy installed on the site. That copy can have been hand-edited, and the base side
   is an older release that is not installed at all, so mixing sources makes the two ends
   inconsistent. The site is read only for version numbers. See `references/sources.md`.
2. **Never invent a base version.** Either the override's `@version` gives it exactly, or it is
   inferred, and an inferred base downgrades the run to "ask before writing".
3. **Never write a file that fails any of the three verification checks** in Phase 5. A rebase that
   cannot be verified is a rewrite, and rewriting is what this skill exists to avoid.
4. **Never bump `@version` to the project version.** It becomes the `@version` of the fetched target
   template, which is usually an older number. Confusing the two is the most common mistake in this
   job, so read "Two version numbers" in `references/sources.md` before touching a header.
5. **Read the code around the template, not just the template.** That is the theme, or the plugin,
   that holds the override. A customization's purpose usually lives outside the file, in the filter
   that drives it. Reporting the objective without checking that code produces a
   description of the syntax, which is useless to the person reviewing it.

## Inputs

Any of these:

- **A theme or child theme**, or a subfolder of one such as `woocommerce/`.
- **A plugin that carries overrides** of another project's templates, served through a filter such
  as `woocommerce_locate_template`. They usually sit in the plugin's own `templates/` folder with
  no `woocommerce/` prefix, so `templates/emails/email-addresses.php` overrides WooCommerce's
  `templates/emails/email-addresses.php`. Point at the plugin root and only `templates/` and any
  registry folder in it are scanned, or point at a subfolder to scan exactly that.
- **A standalone file** outside any install, such as a copy someone sent over. It needs `--as`, the
  path it would have inside a theme, and either `--wp-root` or `--installed` to say which release
  to compare against. With `--installed` no site is needed at all.

**Invoked with no target, ask for one.** Infer one only when the session has already been working
in a single unambiguous set of files and no second candidate is plausible. A site merely mentioned
earlier in the conversation is not that, and neither is a file that happened to be open, whatever is
sitting in `references/cache/`, or the theme scanned last. This skill edits real templates on real
sites, so a wrong guess means editing production somewhere nobody asked about: when in doubt, ask
and stop there. A bare theme or site name is not a target either, resolve it to a path before
Phase 0.

## Scripts

All are read-only, take no credentials, and cache into `references/cache/` which is gitignored.

```bash
# Inventory a theme, a plugin, a folder or one file: what is overridden, from which project, how stale.
scripts/scan-overrides.sh "/path/to/htdocs/wp-content/themes/mytheme"
scripts/scan-overrides.sh "/path/to/htdocs/wp-content/plugins/myplugin"
scripts/scan-overrides.sh --as woocommerce/emails/email-addresses.php --installed 11.1.2 ~/file.php
scripts/scan-overrides.sh --as woocommerce/emails/email-addresses.php --wp-root /path/to/htdocs ~/file.php
scripts/scan-overrides.sh --offline "/path/..."     # no network, upstream column reads "?"

# Fetch one pristine file at one release. Prints the cached path. Exit 2 means no such file there.
scripts/fetch-upstream.sh --kind plugin --slug woocommerce --version 9.8.0 \
    --path templates/emails/email-addresses.php
scripts/fetch-upstream.sh --kind theme --slug storefront --version 4.6.2 --path single.php
scripts/fetch-upstream.sh --kind core --version 6.8 --path wp-includes/theme-compat/header.php
scripts/fetch-upstream.sh --kind github --repo owner/name --version 1.2.3 --path templates/x.php

# Releases available for a wordpress.org project, oldest first. Used by base inference.
scripts/list-versions.sh --kind theme --slug storefront --max 4.6.2 --sample 10

# Run every Phase 5 check on a rebased file. Exit 3 means at least one failed.
scripts/verify-rebase.sh --base b.php --ours o.php --target t.php --merged m.php
```

## Workflow

### Phase 0: resolve the targets

Run `scripts/scan-overrides.sh` on the target and show its table before doing anything else. It
works out whether the target sits in a theme, a plugin or neither, locates the WordPress root, reads
the theme, parent theme or plugin headers, classifies each override, and reports staleness against
the real upstream release.

Classification order, which the script applies and which matters when a path is ambiguous. For a
plugin, a leading `templates/` is stripped first, since that folder is the plugin's own template
root. For a standalone file, the path given with `--as` is used.

1. A first segment in `references/projects.tsv`, such as `woocommerce/`, means that project, at its
   registered template root.
2. In a theme, the same relative path existing in the parent theme means the parent theme.
3. In a plugin, another installed plugin shipping `templates/<path>` means that plugin. If more than
   one does, the first is assumed and the report says so: check which one the plugin's template
   loader actually overrides.
4. A first segment matching an installed plugin slug means that plugin, at `templates/<rest>`.
5. A match under `wp-includes/theme-compat/` means WordPress core.
6. Otherwise it is a custom template, not an override.

**A file that fetches as 404 at the installed version is not an override.** It is either custom, or
upstream removed or renamed it. Both cases are reported and skipped, never merged. A real example:
`emails/supplier-processing-order.php`, in a Storefront child theme and later in a site plugin, is a
custom WooCommerce email paired with its own `WC_Email` subclass, and only looks like an override
because of where it sits.

Then let the user pick what to process, unless they already named a single file.

### Phase 1: fetch base and target

- **base** = `fetch-upstream.sh` at the tag equal to the override's `@version`.
  **Sanity check**: the fetched file's own `@version` must equal the override's. If it does not, the
  header lies or was hand-edited, so fall through to inference.
- **target** = `fetch-upstream.sh` at the tag equal to the installed project version.
- **No `@version` in the override**: infer the base by the procedure in `references/sources.md`,
  coarse sweep with `list-versions.sh --sample`, deduplicate by hash, keep the revision with the
  smallest diff, then refine around it. Record that the base was inferred: it changes the decision
  in Phase 5.

### Phase 2: isolate and understand the customizations

```bash
diff -u "$BASE" "$OURS"     # the customization set
diff -u "$BASE" "$TARGET"   # what upstream actually changed, hunk by hunk
```

For each hunk of the first diff:

- Classify it: addition, replacement, removal, or pure whitespace and reformatting. Whitespace-only
  hunks are noise, drop them rather than carrying them forward, and say so in the report.
- Reuse any existing marker text or docblock note as the stated intent.
- **Grep the theme or plugin holding the override for every custom hook name it introduces.** A
  filter such as `mytheme_show_item_price` will have its counterpart in `functions.php`,
  `includes/` or the plugin's modules. For a standalone file there is nothing to grep, so ask where
  its hooks are consumed. That code is what the customization is actually for. It also
  catches a **dead customization**, one whose hook nothing filters any more, which is worth
  reporting rather than carrying forward silently.

### Phase 3: mechanical merge

```bash
git merge-file -p --diff3 "$OURS" "$BASE" "$TARGET" > "$MERGED"
```

`git merge-file` works outside a repository, so no scratch repo is needed. Clean hunks land
deterministically, and that is the whole point: no reasoning step gets the opportunity to quietly
drop an upstream change. Only the conflicts need judgement.

### Phase 4: resolve, adapt, annotate

Resolve each conflict by **keeping upstream's structure and re-expressing the customization inside
it**, guided by the intent from Phase 2 rather than by the old line shapes. When upstream has
rewritten a region, a customization that was three lines may become one line somewhere else. That is
an adaptation, and the report has to say so.

Then annotate every customization in the file, including the ones the skill did not introduce.

**Marker format.** Default to PHP comments, because HTML comments are emitted into the rendered page
or into the email source where recipients can read them. Use HTML comments only where the file
already uses that style consistently and the block is pure markup.

```php
<?php // BEGIN mytheme: billing address cell behind a filter, hidden on this site ?>
<?php if ( apply_filters( 'mytheme_show_billing_address', true ) ) : ?>
	...
<?php endif; ?>
<?php // END mytheme ?>
```

**Where a customization replaced or removed core code, keep that code commented out inside the
block**, labelled with the version it came from. Pure additions get markers but no commented core
code, because there is nothing they replaced.

```php
<?php
// BEGIN mytheme: last name removed, the checkout hides it too
/* Core 11.0.0 had:
<p class="woocommerce-form-row form-row-last">
	<label for="account_last_name"><?php esc_html_e( 'Last name', 'woocommerce' ); ?></label>
	<input type="text" class="input-text" name="account_last_name" id="account_last_name" />
</p>
*/
?>
<?php // END mytheme ?>
```

**The marker owner is derived from the site being worked on, never assumed.** `mytheme` above is a
placeholder, not a default. Work down this list and stop at the first that yields a name:

1. An attribution already present in that file, or in the other overrides beside it, in whatever
   form it takes: a trailing `// Acme`, an `<!-- added by Acme -->`, a docblock note. Matching what is
   already there keeps a file consistent with its neighbours.
2. The `Author` header of the theme's `style.css`, or of the plugin's main file.
3. The theme or plugin name, or failing that its text domain.

**Never carry a name over from another project, another site, or an example in this skill.** The
marker says who owns the customization on this site, so a wrong one credits somebody else's work,
and on a site handed between agencies that is actively misleading. If none of the three yields
anything usable, ask rather than guess.

**Comment out core code with `/* */`, never with `//`.** Template code contains `?>`, and a `?>`
inside a one-line comment still closes PHP mode, so everything after it leaks to the browser or the
email as literal text. Inside a block comment `?>` is inert. Verified 2026-08-28 against PHP 8.
The only thing to watch in a block comment is a literal `*/` in the code being commented out.

Finally, update the docblock:

- Bump `@version` to the **target template's** `@version`.
- Maintain a `Customizations:` list summarising each marked block in one line, so the next pass can
  read the intent before diffing anything.

```php
 * @version 10.6.0
 *
 * Customizations:
 * - Billing address cell wrapped in mytheme_show_billing_address.
 * - Shipping cell also prints the billing phone as a fallback, and the billing email.
```

### Phase 5: verify, then decide

Four checks. All must pass before writing without asking. **Run the script, do not improvise
greps**: an unescaped regex character in an ad-hoc grep reports a missing upstream change that is
actually present, and sends the whole pass chasing a phantom.

```bash
scripts/verify-rebase.sh --base "$BASE" --ours "$OURS" --target "$TARGET" --merged "$MERGED"
```

1. **Lint**: `php -l` on the merged file.
2. **Upstream coverage**: every non-blank line of the target appears in the merged file, ignoring
   indentation, since customizations reindent the code they wrap. A missing upstream line is the
   failure this skill exists to prevent, so an unexplained one blocks the write.
3. **Customization coverage**: every line ours added over base appears in the merged file. Lines
   listed here are not automatically failures, a deliberately adapted or re-marked line shows up
   too, but **every one of them must be explained in the report**.
4. **Stale variables**: a variable referenced in the merged file that is never assigned there and
   does not appear anywhere in the target. This is the failure mode nothing else catches: upstream
   deletes a variable, a customization still passes it to a hook, the merge reports no conflict and
   `php -l` passes, and the template raises an undefined variable notice at runtime with an empty
   value reaching whatever the hook renders. The check reads PHP's own token stream rather than the
   raw text, so a variable named in a comment is not mistaken for a reference.

**Closing invariant, the strongest signal available**: `diff "$TARGET" "$MERGED"` must contain
nothing but the annotated customization blocks, and their count must equal the number of
customizations found in Phase 2. If it contains anything else, something was invented or lost.
State the count in the report either way.

## Confidence gate

**Write** when the base was resolved exactly from the version header, every customization has a
clear objective, no conflict was resolved ambiguously, and all three checks pass.

**Ask first** when any of these hold:

- the base was inferred rather than taken from a matching `@version`,
- a customization's objective could not be established from the template and the code around it,
- upstream restructured a region so a customization had to be adapted rather than carried,
- a customization looks dead, its hook no longer used anywhere,
- markers are being retrofitted onto a change whose purpose had to be guessed.

**Do not rebase, and say why** when upstream rewrote the template beyond recognition, the template
was removed or renamed upstream, or the customization set cannot be expressed against the new
structure. Recommend the alternative instead: drop the override in favour of the hooks the new
template exposes, or restart the override from the current upstream file and reapply the
customizations deliberately. **An override that cannot be rebased honestly is worse than no
override**, because it silently freezes the site on old markup.

Before the first write of a run, ask how to handle the original: overwrite, overwrite and keep a
backup copy, or stage the result and hand over the path. Keep that answer for the rest of the run.

**A `.bak` left inside the theme is usually readable over HTTP**, since the server will not run a
file that no longer ends in `.php` and serves its source as plain text instead. That exposes the
template, and any comment in it, to anyone who guesses the name. Say so when that option is chosen,
and remind the user to delete it once they are satisfied with the result.

After writing, read the file back and compare it against the staged result. A write over SFTP or a
network mount can truncate or fail silently, and a half-written template is worse than a stale one.

## Report

Follow `references/report-template.md`. Per template: the version table, what upstream brought in,
one block per customization giving what it is, what it is for including the supporting theme or plugin code,
what upstream did to that region, and how it was carried across, then the verification results and
the decision.

The customization blocks are the part worth writing carefully. Everything else is bookkeeping.

## Cost notes

- Every fetch is cached under `references/cache/<kind>/<slug>/<version>/<path>`, so a second run on
  the same theme is nearly free. The cache is gitignored and safe to delete.
- Base inference is the expensive path, roughly 10 to 15 fetches per file. Prefer a template with an
  `@version` header, and where a project has a GitHub repository use the commits-for-path API call
  instead of sweeping releases.
- `scan-overrides.sh` makes one fetch per file. Use `--offline` for a quick structural look.
